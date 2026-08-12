"""
Tests de la Votación Comunitaria (Gobernanza Operativa, Cap 14).

Cubre:
- Creación de propuestas con categorías y umbrales (operational/critical/emergency).
- Votación: un voto por persona, opciones válidas, propuesta cerrada.
- Quórum: no alcanzado -> quorum_not_met; alcanzado -> passed/rejected.
- Consenso crítico del 75% (Cap 14) para categoría critical.
- Cierre manual por admin y detalle público (T13).
"""

import os
import tempfile

os.environ["SECRET_KEY"] = "test-secret"
os.environ.pop("DEEPSEEK_API_KEY", None)

import pytest

from app import create_app
from app.utils import get_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        with app.app_context():
            db = get_db()
            with open("app/schema.sql", "r", encoding="utf-8") as f:
                db.executescript(f.read())
            for uid, name in [(1, "Max"), (2, "Ana"), (3, "Luis"), (4, "Sara")]:
                # Integrantes establecidos de la Cohorte (N1): tienen voz
                # en la gobernanza (Puente de Llegada, Cap. 13)
                db.execute(
                    "INSERT INTO users (id, email, name, password_hash, trust_level) VALUES (?, ?, ?, 'hash', 1)",
                    (uid, f"{name.lower()}@test.com", name),
                )
            db.commit()
        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth(client):
    from app.jwt_utils import create_token

    def _auth(uid, admin=False):
        payload = {"user_id": uid}
        if admin:
            payload["is_admin"] = True
        return {"Authorization": f"Bearer {create_token(payload)}"}

    return _auth


def _create(client, auth, **over):
    payload = {
        "title": over.get("title", "Ajustamos la tolerancia de matching?"),
        "description": over.get("description", "Propuesta operativa de la Cohorte Cero"),
        "category": over.get("category", "operational"),
        "options": over.get("options", ["Si", "No"]),
        "reason": over.get("reason", ""),
        "deadline_hours": over.get("deadline_hours", 72),
    }
    return client.post("/voting/proposals", json=payload, headers=auth(1))


def test_crear_propuesta_operativa(client, auth):
    resp = _create(client, auth)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["proposal"]["status"] == "open"
    assert data["proposal"]["category"] == "operational"
    assert data["proposal"]["quorum_ratio"] == 0.5
    assert data["proposal"]["majority_ratio"] == 0.5


def test_crear_propuesta_critical_consenso_75(client, auth):
    resp = _create(client, auth, category="critical",
                   title="Ajustamos el valor del Maxo?")
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["proposal"]["majority_ratio"] == 0.75


def test_crear_propuesta_categoria_invalida(client, auth):
    resp = _create(client, auth, category="filosofica")
    assert resp.status_code == 400


def test_crear_propuesta_opciones_invalidas(client, auth):
    resp = _create(client, auth, options=["Solo una"])
    assert resp.status_code == 400


def test_votar_y_quorum_no_alcanzado(client, auth):
    pid = _create(client, auth).get_json()["proposal"]["id"]
    resp = client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(1))
    assert resp.status_code == 200

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["proposal"]["result"] == "quorum_not_met"  # 1 voto de 4 usuarios


def test_votacion_un_voto_por_persona(client, auth):
    pid = _create(client, auth).get_json()["proposal"]["id"]
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(1))
    resp = client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(1))
    assert resp.status_code == 409


def test_opcion_invalida(client, auth):
    pid = _create(client, auth).get_json()["proposal"]["id"]
    resp = client.post(f"/voting/proposals/{pid}/vote", json={"option": "Quizas"}, headers=auth(1))
    assert resp.status_code == 400


def test_consenso_critico_75_porciento(client, auth):
    pid = _create(client, auth, category="critical").get_json()["proposal"]["id"]
    for uid in (1, 2, 3):
        client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(uid))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()["proposal"]
    assert data["result"] == "passed"  # 3/4 quorum ok, 3/3 = 100% > 75%
    assert data["result_detail"]["winner"] == "Si"


def test_consenso_critico_rechazado_por_minoria(client, auth):
    pid = _create(client, auth, category="critical").get_json()["proposal"]["id"]
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(1))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(3))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()["proposal"]
    assert data["result"] == "rejected"  # 3/4 quorum ok, 2/3 = 66% < 75%


def test_emergency_requiere_mayoria_60(client, auth):
    pid = _create(client, auth, category="emergency",
                  title="Veto por sufrimiento sintetico").get_json()["proposal"]["id"]
    for uid in (1, 2, 3):
        client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(uid))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    assert resp.get_json()["proposal"]["result"] == "passed"


def test_votar_propuesta_cerrada(client, auth):
    pid = _create(client, auth).get_json()["proposal"]["id"]
    client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    resp = client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))
    assert resp.status_code == 409


def test_detalle_publico_incluye_votos(client, auth):
    pid = _create(client, auth).get_json()["proposal"]["id"]
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))

    resp = client.get(f"/voting/proposals/{pid}")
    data = resp.get_json()
    assert data["status"] == "open"
    assert len(data["votes"]) == 1
    assert data["votes"][0]["user_id"] == 2


def test_stats_publicas(client, auth):
    resp = client.get("/voting/stats")
    assert resp.status_code == 200
    assert "audit" in resp.get_json()


FAKE_ANALYSIS = {
    "vhv": {"vitalTime": 100, "affectedLives": 5, "finiteResources": 300,
            "timeFactor": 1.2, "confidence": 0.8},
    "axiomReport": [
        {"type": "TRUTH", "passed": True, "score": 90, "reasoning": "Datos verificables"},
        {"type": "TIME", "passed": True, "score": 75, "reasoning": "Respeta T2"},
        {"type": "LIFE", "passed": False, "score": 40, "reasoning": "Aumenta sufrimiento"},
    ],
    "oracleOpinions": [
        {"role": "Economic", "verdict": "Approve", "analysis": "Rentable", "confidence": 0.8},
        {"role": "Social", "verdict": "Reject", "analysis": "Desplaza comunidad", "confidence": 0.9},
    ],
}


def test_analisis_oraculo_persiste_y_expone(client, auth, monkeypatch):
    """El análisis DeepSeek se persiste (T13) y aparece en el detalle público."""
    import app.voting_bp as voting_bp
    from app import voting_oracle

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(voting_oracle, "_call_deepseek", lambda messages, temperature=0.2: FAKE_ANALYSIS)

    pid = _create(client, auth).get_json()["proposal"]["id"]
    resp = client.post(f"/voting/proposals/{pid}/analyze", json={}, headers=auth(1))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["oracle_analysis"]["analysis"]["vhv"]["vitalTime"] == 100
    assert data["oracle_analysis"]["analysis"]["vhv"]["totalScore"] == 180000  # (100*5*300)*1.2
    assert len(data["oracle_analysis"]["analysis"]["axiomReport"]) == 3
    assert len(data["oracle_analysis"]["analysis"]["oracleOpinions"]) == 2

    detail = client.get(f"/voting/proposals/{pid}").get_json()
    assert detail["oracle_analysis"]["analysis"]["oracleOpinions"][1]["verdict"] == "Reject"


def test_analisis_sin_fuentes_devuelve_503(client, auth, monkeypatch):
    """Sin API key de DeepSeek y con el fallback local deshabilitado -> 503."""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    pid = _create(client, auth).get_json()["proposal"]["id"]
    resp = client.post(f"/voting/proposals/{pid}/analyze", json={}, headers=auth(1))
    assert resp.status_code == 503


def test_analisis_fallback_local_cuando_deepseek_falla(client, auth, monkeypatch):
    """Si DeepSeek falla, el oráculo local (Jan) produce el análisis (engine=local)."""
    import app.voting_bp as voting_bp
    from app import voting_oracle

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(voting_oracle, "_call_deepseek", lambda m, temperature=0.2: (_ for _ in ()).throw(RuntimeError("nube caída")))
    monkeypatch.setattr(voting_oracle, "_call_local", lambda m, temperature=0.2: FAKE_ANALYSIS)

    pid = _create(client, auth).get_json()["proposal"]["id"]
    resp = client.post(f"/voting/proposals/{pid}/analyze", json={}, headers=auth(1))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["oracle_analysis"]["analysis"]["engine"] == "local"
    assert data["oracle_analysis"]["analysis"]["model"] == "Qwen3-8B-Q4_K_M"


def test_analisis_propuesta_inexistente(client, auth):
    resp = client.post("/voting/proposals/9999/analyze", json={}, headers=auth(1))
    assert resp.status_code == 404


def test_delegacion_arrastra_voto(client, auth):
    """El delegatario vota y arrastra al delegante que no votó (democracia líquida)."""
    pid = _create(client, auth, category="critical").get_json()["proposal"]["id"]

    resp = client.post("/voting/delegations", json={"delegatee_user_id": 2}, headers=auth(1))
    assert resp.status_code == 200

    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(3))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(4))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()["proposal"]
    # 3 votos directos (quorum 3/4) + 1 delegado (usuario 1 -> usuario 2, votó Si)
    # efectivos: Si=2, No=2 -> empate 50% < 75% (crítica), rechazada
    assert data["result_detail"]["votes_cast"] == 3
    assert data["result_detail"]["delegated_votes"] == 1
    assert data["result_detail"]["effective_votes"] == 4
    assert data["result"] == "rejected"


def test_voto_directo_anula_delegacion(client, auth):
    """Si el delegante vota directamente, su voto manda sobre la delegación."""
    pid = _create(client, auth).get_json()["proposal"]["id"]
    client.post("/voting/delegations", json={"delegatee_user_id": 2}, headers=auth(1))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(1))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(3))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()["proposal"]
    # directos: No(1), Si(2), Si(3) -> Si=2/3 aprobada; el voto No de 1 anula la delegación
    assert data["result_detail"]["delegated_votes"] == 0
    assert data["result"] == "passed"


def test_delegacion_a_si_mismo_rechazada(client, auth):
    resp = client.post("/voting/delegations", json={"delegatee_user_id": 1}, headers=auth(1))
    assert resp.status_code == 400


def test_delegacion_publica_t13(client, auth):
    client.post("/voting/delegations", json={"delegatee_user_id": 2}, headers=auth(1))
    resp = client.get("/voting/delegations")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["delegator_user_id"] == 1
    assert data[0]["delegatee_user_id"] == 2


def test_revocar_delegacion(client, auth):
    client.post("/voting/delegations", json={"delegatee_user_id": 2}, headers=auth(1))
    resp = client.delete("/voting/delegations", headers=auth(1))
    assert resp.status_code == 200
    assert resp.get_json()["revoked"] is True
    assert client.get("/voting/delegations").get_json() == []


def _seed_tvi(client, uid, hours, tag=0):
    """Registra TVI (vida consciente) para un usuario con fechas únicas."""
    from datetime import datetime, timedelta
    start = datetime(2026, 8, 1, 8, 0) + timedelta(hours=tag)
    end = start + timedelta(hours=hours)
    with client.application.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO tvi_entries (user_id, start_time, end_time, duration_seconds, category) "
            "VALUES (?, ?, ?, ?, 'WORK')",
            (uid, start.isoformat(), end.isoformat(), int(hours * 3600)),
        )
        db.commit()


def test_ponderacion_tvi_cambia_resultado(client, auth):
    """Participación Inteligente (Cap. 14): la voz del que más vida consciente
    ha invertido pesa más. Sin ponderar el resultado sería rejected (66%);
    con TVI (5x) el consenso crítico se alcanza (85%)."""
    _seed_tvi(client, 2, 40.0, tag=1)  # Ana: 40h registradas
    pid = _create(client, auth, category="critical").get_json()["proposal"]["id"]
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(1))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(3))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()["proposal"]
    detail = data["result_detail"]
    assert data["result"] == "passed"  # con pesos: Si = 1 + 5 = 6/7 = 85.7%
    assert detail["tvi_weighting"] == "participation_intelligence"
    assert detail["winner_fraction"] == round(2 / 3, 4)  # conteo simple sigue siendo 66%
    assert detail["weighted_fraction"] == round(6 / 7, 4)
    assert detail["option_weights"] == {"Si": 6.0, "No": 1.0}
    assert detail["tvi_hours"] == {"1": 0.0, "2": 40.0, "3": 0.0}


def test_ponderacion_sin_tvi_retrocompatible(client, auth):
    """Sin TVI registrado, todos pesan 1: el resultado no cambia (comportamiento previo)."""
    pid = _create(client, auth, category="critical").get_json()["proposal"]["id"]
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(1))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(2))
    client.post(f"/voting/proposals/{pid}/vote", json={"option": "No"}, headers=auth(3))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    data = resp.get_json()["proposal"]
    detail = data["result_detail"]
    assert data["result"] == "rejected"  # 66% < 75%, igual que sin ponderación
    assert detail["winner_fraction"] == detail["weighted_fraction"] == round(2 / 3, 4)
    assert detail["option_weights"] == {"Si": 2.0, "No": 1.0}


def test_ponderacion_normalizada_al_mayor_tvi(client, auth):
    """El peso se normaliza al mayor TVI de la propuesta: 40h -> 5x, 10h -> 2x."""
    _seed_tvi(client, 2, 40.0, tag=1)
    _seed_tvi(client, 4, 10.0, tag=2)
    pid = _create(client, auth, category="operational").get_json()["proposal"]["id"]
    for uid in (2, 4):
        client.post(f"/voting/proposals/{pid}/vote", json={"option": "Si"}, headers=auth(uid))

    resp = client.post(f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True))
    detail = resp.get_json()["proposal"]["result_detail"]
    assert detail["option_weights"] == {"Si": 7.0}  # 5 + 2
    assert detail["tvi_hours"] == {"2": 40.0, "4": 10.0}
