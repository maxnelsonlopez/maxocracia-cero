import json
import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.jwt_utils import create_token
from app.micromax import init_micromax_tables
from app.utils import init_db


@pytest.fixture
def client():
    """Create test client with temporary database."""
    db_fd, db_path = tempfile.mkstemp(prefix="test_micromax_", suffix=".db")
    os.close(db_fd)

    app = create_app(db_path=db_path)
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})

    with app.app_context():
        init_db()
        init_micromax_tables(app)

        # Add test users
        db = sqlite3.connect(db_path)
        db.execute(
            "INSERT INTO users (id, email, name, alias, password_hash) VALUES (?, ?, ?, ?, ?)",
            (
                1,
                "alice@example.com",
                "Alice",
                "alice",
                generate_password_hash("Password1"),
            ),
        )
        db.execute(
            "INSERT INTO users (id, email, name, alias, password_hash) VALUES (?, ?, ?, ?, ?)",
            (2, "bob@example.com", "Bob", "bob", generate_password_hash("Password1")),
        )
        db.commit()
        db.close()

    with app.test_client() as client:
        yield client

    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture
def auth_headers():
    def _headers(user_id, email, is_admin=0):
        token = create_token({"user_id": user_id, "email": email, "is_admin": is_admin})
        return {"Authorization": f"Bearer {token}"}

    return _headers


def test_micromax_flow(client, auth_headers):
    # 1. Get household (should return None/empty)
    res = client.get(
        "/api/micromax/household", headers=auth_headers(1, "alice@example.com")
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["household"] is None

    # 2. Create household
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Casa de Alice"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["household"]["name"] == "Casa de Alice"
    invite_code = data["household"]["invite_code"]
    assert invite_code is not None

    # 3. Bob joins household
    res = client.post(
        "/api/micromax/household/join",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"invite_code": invite_code}),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["household"]["name"] == "Casa de Alice"
    assert data["member"]["name"] == "Bob"

    # 4. Get household (should now show both)
    res = client.get(
        "/api/micromax/household", headers=auth_headers(1, "alice@example.com")
    )
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["members"]) == 2

    # 5. Save config for Alice
    res = client.post(
        "/api/micromax/member/config",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "monthly_income": 1000,
                "work_hours": 40,
                "travel_hours": 5,
                "sleep_hours": 56,
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["monthly_income"] == 1000

    # 6. Save safety survey for Alice (all false = score 0)
    res = client.post(
        "/api/micromax/safety-survey",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "answers": {
                    "q1": False,
                    "q2": False,
                    "q3": False,
                    "q4": False,
                    "q5": False,
                    "q6": False,
                }
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["score"] == 0
    assert not data["blocked"]

    # 7. Log CDD task for Alice
    res = client.post(
        "/api/micromax/cdd",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "task_name": "Lavar platos",
                "duration_hours": 1.5,
                "effort_factor": 1.2,
                "mental_factor": 1.1,
                "scope_factor": 1.0,
                "attention_factor": 1.0,
                "fragmentation_factor": 1.0,
                "loneliness_factor": 1.0,
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.get_json()
    # 1.5 * (1.2 * 1.1 * 1.0) * (1.0 * 1.0 * 1.0) = 1.5 * 1.32 = 1.98 VHV
    assert data["calculated_vhv"] == 1.98

    # 8. Get CDD logs for Alice
    res = client.get("/api/micromax/cdd", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["task_name"] == "Lavar platos"

    # 9. Get dashboard
    res = client.get(
        "/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com")
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "three_accounts" in data
    assert "toxicity" in data
    assert "safety_survey" in data
    assert "alerts" in data["toxicity"]
    assert data["toxicity"]["alerts"]["ice"] is False
    assert data["toxicity"]["alerts"]["idb"] is False
    assert data["toxicity"]["alerts"]["idp"] is False

    # 10. Log an audit
    res = client.post(
        "/api/micromax/audit",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "audit_date": "2026-05-19",
                "conflicts_count": 1,
                "weapon_count": 0,
                "accusations_count": 0,
                "threats_count": 0,
                "s1_hours": 0.0,
                "s2_score": 1.0,
                "s3_score": 1.0,
                "s4_score": 1.0,
                "s5_score": 1.0,
                "duration_weeks": 4,
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201

    # 11. Verify toxicity calculation on dashboard
    res = client.get(
        "/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com")
    )
    assert res.status_code == 200
    data = res.get_json()
    # Conflicts = 1, baseline = 2. ICE = 1/2 * (1 + 0) = 0.5
    assert data["toxicity"]["ice"] == 0.5


RED_ANSWERS = {
    "q1": True,
    "q2": True,
    "q3": True,
    "q4": False,
    "q5": False,
    "q6": False,
}


def _join(client, auth_headers, user_id, email, invite_code):
    return client.post(
        "/api/micromax/household/join",
        headers=auth_headers(user_id, email),
        data=json.dumps({"invite_code": invite_code}),
        content_type="application/json",
    )


def _log_cdd(client, auth_headers, user_id, email, task="Tarea invisible", hours=2.0):
    return client.post(
        "/api/micromax/cdd",
        headers=auth_headers(user_id, email),
        data=json.dumps(
            {
                "task_name": task,
                "duration_hours": hours,
                "effort_factor": 1.0,
                "mental_factor": 1.0,
                "scope_factor": 1.0,
            }
        ),
        content_type="application/json",
    )


def test_escudo_rojo_no_silencia_el_registro_propio(client, auth_headers):
    """Regresion (Cap. 16.5 - Derecho al Registro Protegido): una ESI en rojo
    NUNCA bloquea que la persona registre su propio trabajo invisible."""
    # Alice crea el hogar; Bob entra y responde rojo
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )
    invite_code = res.get_json()["household"]["invite_code"]
    assert _join(client, auth_headers, 2, "bob@example.com", invite_code).status_code == 200

    res = client.post(
        "/api/micromax/safety-survey",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"answers": RED_ANSWERS}),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["score"] == 3
    assert data["protection_mode"] == "shielded"
    # Compatibilidad: ya no se reporta como bloqueado
    assert data["blocked"] is False
    assert data["can_log"] is True

    # El registro propio sigue funcionando (antes lanzaba 'Access Blocked')
    res = _log_cdd(client, auth_headers, 2, "bob@example.com")
    assert res.status_code == 201
    assert res.get_json()["calculated_vhv"] == 2.0

    # Y Bob ve sus propios registros completos
    res = client.get("/api/micromax/cdd", headers=auth_headers(2, "bob@example.com"))
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_escudo_oculta_cifras_a_los_demas_pero_no_a_la_persona(client, auth_headers):
    """Las cifras del miembro protegido salen de totales/cuotas para los demas
    (nada inferible por diferencia); ella ve el hogar completo."""
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )
    invite_code = res.get_json()["household"]["invite_code"]
    assert _join(client, auth_headers, 2, "bob@example.com", invite_code).status_code == 200

    # Config de Alice para tener CEH en la mezcla
    client.post(
        "/api/micromax/member/config",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {"monthly_income": 1000, "work_hours": 40, "travel_hours": 5, "sleep_hours": 56}
        ),
        content_type="application/json",
    )

    # Bob (protegido) registra trabajo; Alice tambien
    assert _log_cdd(client, auth_headers, 2, "bob@example.com", hours=4.0).status_code == 201
    assert _log_cdd(client, auth_headers, 1, "alice@example.com", hours=1.0).status_code == 201

    client.post(
        "/api/micromax/safety-survey",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"answers": RED_ANSWERS}),
        content_type="application/json",
    )

    # Vista de ALICE (no protegida): Bob aparece protegido y sin cifras;
    # los totales solo contienen a Alice.
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    members = {m["name"]: m for m in res.get_json()["three_accounts"]["members"]}
    bob_view = members["Bob"]
    alice_view = members["Alice"]
    assert bob_view["protegido"] is True
    assert bob_view["cdd"] is None and bob_view["equilibrio"] is None
    assert alice_view["cdd"] == 1.0
    assert alice_view["cdd_share"] == 100.0
    assert res.get_json()["three_accounts"]["totals"]["total_cdd"] == 1.0

    # Vista de BOB (el protegido): ve todo, incluidas sus propias cifras
    res = client.get("/api/micromax/dashboard", headers=auth_headers(2, "bob@example.com"))
    assert res.status_code == 200
    members = {m["name"]: m for m in res.get_json()["three_accounts"]["members"]}
    assert members["Bob"]["cdd"] == 4.0
    assert members["Bob"]["protegido"] is True
    assert members["Alice"]["cdd"] == 1.0


def test_esi_wants_support_es_privado_y_opt_in(client, auth_headers):
    """El opt-in de apoyo viaja con la encuesta, lo ve solo quien lo declaro y no
    altera el puntaje ESI."""
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )
    invite_code = res.get_json()["household"]["invite_code"]
    assert _join(client, auth_headers, 2, "bob@example.com", invite_code).status_code == 200

    answers = {f"q{i}": False for i in range(1, 7)}
    res = client.post(
        "/api/micromax/safety-survey",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"answers": dict(answers), "wants_support": True}),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["score"] == 0
    assert data["wants_support"] is True
    assert data["protection_mode"] == "standard"

    res = client.get(
        "/api/micromax/safety-survey", headers=auth_headers(2, "bob@example.com")
    )
    assert res.get_json()["wants_support"] is True

    # La vista del hogar (de Alice) jamas incluye la encuesta de Bob
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    survey = res.get_json().get("safety_survey")
    assert survey is None or survey.get("member_id") != 2


def test_compatibilidad_vector_vhv_en_cdd(client, auth_headers):
    """Cap. 16.5: cada tarea puede portar su vector [T, V, R] opcional sin romper
    el escalar ponderado que alimenta el equilibrio."""
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )
    assert res.status_code == 201

    # Con vector completo (ej. cuidado de persona dependiente con insumos)
    res = client.post(
        "/api/micromax/cdd",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "task_name": "Cuidado de mama",
                "duration_hours": 3.0,
                "effort_factor": 1.5,
                "mental_factor": 1.3,
                "scope_factor": 1.2,
                "v_ucv": 0.5,
                "r_units": 4.0,
                "r_notes": "medicamentos y transporte",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["vhv_vector"] == {"T": 3.0, "V": 0.5, "R": 4.0}
    assert data["r_notes"] == "medicamentos y transporte"
    # El escalar ponderado sigue intacto: 3 * (1.5*1.3*1.2) = 7.02
    assert data["calculated_vhv"] == 7.02

    # Sin campos nuevos: retrocompatible (defaults a cero)
    res = client.post(
        "/api/micromax/cdd",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "task_name": "Lavar platos",
                "duration_hours": 1.0,
                "effort_factor": 1.0,
                "mental_factor": 1.0,
                "scope_factor": 1.0,
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201
    assert res.get_json()["vhv_vector"] == {"T": 1.0, "V": 0.0, "R": 0.0}

    # Componentes negativos rechazados (V: una vida afectada no se des-afecta)
    res = client.post(
        "/api/micromax/cdd",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "task_name": "X",
                "duration_hours": 1.0,
                "effort_factor": 1.0,
                "mental_factor": 1.0,
                "scope_factor": 1.0,
                "v_ucv": -1,
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 400


def test_credito_regenerativo_r_negativo(client, auth_headers):
    """Cap. 16.5 s16.5.14 / EVV 1.2 s4.3: el cuidado del Reino Natural se registra
    con R negativo (devolver mas de lo tomado)."""
    client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Conjunto Los Sauces"}),
        content_type="application/json",
    )
    res = client.post(
        "/api/micromax/cdd",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps(
            {
                "task_name": "Jornada de reforestacion del humedal",
                "duration_hours": 4.0,
                "effort_factor": 1.3,
                "mental_factor": 1.0,
                "scope_factor": 1.5,
                "r_units": -12.0,
                "r_notes": "40 arboles nativos plantados; captura neta estimada",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["vhv_vector"] == {"T": 4.0, "V": 0.0, "R": -12.0}
    assert data["r_notes"] == "40 arboles nativos plantados; captura neta estimada"


def test_ceh_canonica_tvi_homogeneiza_las_cuentas(client, auth_headers):
    """Cap. 16.5 s16.5.4: cuando todo el hogar usa modo canonico, la CEH se mide en
    horas de vida vendidas — el dinero deja de comprar peso en el equilibrio."""
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )
    invite_code = res.get_json()["household"]["invite_code"]
    assert _join(client, auth_headers, 2, "bob@example.com", invite_code).status_code == 200

    # Alice gana 1000 con tarifa 50/h -> 20 h vendidas; Bob gana 400 con tarifa 20/h -> 20 h.
    # En fiat la brecha es 71/29; en TVI vendido es 50/50.
    for uid, email, income, rate in [
        (1, "alice@example.com", 1000, 50),
        (2, "bob@example.com", 400, 20),
    ]:
        res = client.post(
            "/api/micromax/member/config",
            headers=auth_headers(uid, email),
            data=json.dumps(
                {
                    "monthly_income": income,
                    "work_hours": 40,
                    "travel_hours": 5,
                    "sleep_hours": 56,
                    "ceh_mode": "canonical",
                    "hourly_rate": rate,
                }
            ),
            content_type="application/json",
        )
        assert res.status_code == 200
        assert res.get_json()["ceh_mode"] == "canonical"

    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    ta = res.get_json()["three_accounts"]
    members = {m["name"]: m for m in ta["members"]}
    assert members["Alice"]["ceh_share"] == 50.0
    assert members["Bob"]["ceh_share"] == 50.0
    assert ta["totals"]["ceh_unit"] == "tvi"
    assert ta["totals"]["total_ceh"] == 40.0
    assert ta["pesos"] == {"p1": 0.6, "p2": 0.3, "p3": 0.1}

    # Modo mixto: fallback seguro a fiat (unidad homogenea garantizada)
    client.post(
        "/api/micromax/member/config",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps(
            {
                "monthly_income": 400,
                "work_hours": 40,
                "travel_hours": 5,
                "sleep_hours": 56,
                "ceh_mode": "bridge",
                "hourly_rate": 20,
            }
        ),
        content_type="application/json",
    )
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    ta = res.get_json()["three_accounts"]
    assert ta["totals"]["ceh_unit"] == "fiat"
    members = {m["name"]: m for m in ta["members"]}
    assert members["Alice"]["ceh_share"] == 71.43
    assert members["Bob"]["ceh_share"] == 28.57


def test_ceh_mode_invalido_rechazado(client, auth_headers):
    res = client.post(
        "/api/micromax/member/config",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"ceh_mode": "fiat_total"}),
        content_type="application/json",
    )
    assert res.status_code == 400


def test_gamma_domestica_latido_e_inv1_hogar(client, auth_headers):
    """Cap. 16.5 s16.5.6: check-ins de bienestar; INV1-Hogar escucha las caidas."""
    client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )

    # Gamma fuera del canon [0.5, 1.5] rechazada
    res = client.post(
        "/api/micromax/checkin",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"gamma": 1.9}),
        content_type="application/json",
    )
    assert res.status_code == 400

    # Subida tranquila
    res = client.post(
        "/api/micromax/checkin",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"gamma": 1.2, "note": "buena semana"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    assert res.get_json()["inv1"] is False

    # Caida: se escucha siempre (INV1)
    res = client.post(
        "/api/micromax/checkin",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"gamma": 0.8, "note": "semana dura"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    assert res.get_json()["inv1"] is True

    # Serie propia completa
    res = client.get("/api/micromax/checkins", headers=auth_headers(1, "alice@example.com"))
    serie = res.get_json()
    assert len(serie) == 2
    assert serie[0]["gamma"] == 0.8  # la mas reciente primero

    # Dashboard: ultimo gamma + alerta INV1-Hogar activa
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    wb = res.get_json()["wellbeing"]
    assert wb["inv1_hogar_alert"] is True
    assert wb["members"][0]["gamma"] == 0.8


def test_escudo_oculta_el_angusto_ajeno_pero_la_persona_se_ve_su_propio(client, auth_headers):
    """El gamma de un protegido nunca cruza la pantalla de sus convivientes;
    ella si se ve a si misma y su INV1 propio."""
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Hogar"}),
        content_type="application/json",
    )
    invite_code = res.get_json()["household"]["invite_code"]
    assert _join(client, auth_headers, 2, "bob@example.com", invite_code).status_code == 200

    client.post(
        "/api/micromax/safety-survey",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"answers": RED_ANSWERS}),
        content_type="application/json",
    )
    # Bob reporta angusto (gamma bajo)
    res = client.post(
        "/api/micromax/checkin",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"gamma": 0.6, "note": "privado"}),
        content_type="application/json",
    )
    assert res.status_code == 201 and res.get_json()["inv1"] is True

    # Vista de ALICE: el angusto de Bob no existe en su pantalla
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    wb = res.get_json()["wellbeing"]
    bob_view = next(m for m in wb["members"] if m["name"] == "Bob")
    alice_view = next(m for m in wb["members"] if m["name"] == "Alice")
    assert bob_view["protegido"] is True
    assert bob_view["gamma"] is None and bob_view["inv1"] is None
    assert wb["inv1_hogar_alert"] is False  # nada filtrado por inferencia

    # Vista de BOB: ve su propio angusto y su INV1 personal
    res = client.get("/api/micromax/dashboard", headers=auth_headers(2, "bob@example.com"))
    wb = res.get_json()["wellbeing"]
    bob_view = next(m for m in wb["members"] if m["name"] == "Bob")
    assert bob_view["gamma"] == 0.6
    assert bob_view["inv1"] is True
    assert wb["inv1_hogar_alert"] is True
