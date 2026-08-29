"""
Tests del Parlamento de Parámetros (Cap. 11): la comunidad ajusta α, β, γ, δ
por votación crítica con restricciones axiomáticas, y la aprobación se
ejecuta con procedencia auditable (T13).

Cubre:
- POST /voting/parliament/params: propuesta con acción vinculante.
- Violaciones axiomáticas rechazadas (β=0, γ<1, α=0, δ<0).
- Aprobación con quórum crítico 60% y consenso 75% → parámetros aplicados,
  caché limpiada e historial de resoluciones.
- Sin quórum o rechazo → sin cambios.
- GET público: actuales + historial + propuestas abiertas (T13).
"""

import os
import tempfile

os.environ["SECRET_KEY"] = "test-secret"

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

            # 4 usuarios para quórum crítico (60% → 3 votos); el 1 es admin
            # (el cierre manual de propuestas es facultad administrativa).
            # Todos son integrantes establecidos (N1): tienen voz.
            for uid in range(1, 5):
                db.execute(
                    "INSERT INTO users (id, email, name, password_hash, is_admin, trust_level) VALUES (?, ?, ?, 'hash', ?, 1)",
                    (uid, f"u{uid}@test.com", f"Usuario {uid}", 1 if uid == 1 else 0),
                )
            # Parámetros iniciales (defaults del esquema)
            db.execute(
                "INSERT INTO vhv_parameters (alpha, beta, gamma, delta, notes) VALUES (100.0, 2000.0, 1.0, 100.0, 'inicial')"
            )
            db.commit()

        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


def auth(client, uid=1):
    from app.jwt_utils import create_token

    token = create_token({"user_id": uid, "is_admin": 1 if uid == 1 else 0})
    return {"Authorization": f"Bearer {token}"}


def _propose(client, params, uid=1, **extra):
    return client.post(
        "/voting/parliament/params",
        headers=auth(client, uid),
        json={
            **params,
            **extra,
        },
    )


def _close_proposal(client, proposal_id, uid=1):
    return client.post(
        f"/voting/proposals/{proposal_id}/close", headers=auth(client, uid)
    )


def _params_in_db(client):
    with client.application.app_context():
        db = get_db()
        row = db.execute(
            "SELECT alpha, beta, gamma, delta FROM vhv_parameters ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return {k: float(row[k]) for k in ("alpha", "beta", "gamma", "delta")}


def test_propose_valid_params(client):
    """Propuesta válida: categoría crítica, acción vinculante, lenguaje civil."""
    res = _propose(
        client, {"alpha": 120.0, "beta": 2500.0, "gamma": 1.5, "delta": 80.0}
    )
    assert res.status_code == 201
    prop = res.get_json()["proposal"]
    assert prop["category"] == "critical"
    assert prop["options"] == ["Aprobar", "Mantener"]
    assert prop["action"] == {
        "type": "set_vhv_params",
        "params": {"alpha": 120.0, "beta": 2500.0, "gamma": 1.5, "delta": 80.0},
    }
    assert "100" in prop["description"] and "120" in prop["description"]
    assert "γ ≥ 1" in prop["description"]


def test_propose_axiom_violations_rejected(client):
    """El parlamento no puede premiar el sufrimiento ni ignorar la vida."""
    cases = [
        {"alpha": 0, "beta": 2000.0, "gamma": 1.0, "delta": 100.0},
        {"alpha": 100.0, "beta": 0, "gamma": 1.0, "delta": 100.0},
        {"alpha": 100.0, "beta": 2000.0, "gamma": 0.5, "delta": 100.0},
        {"alpha": 100.0, "beta": 2000.0, "gamma": 1.0, "delta": -5},
        # NaN e infinito no son parámetros: las comparaciones axiomáticas
        # con NaN son False y quedarían pasar (guardarraíl de finitud).
        {"alpha": float("nan"), "beta": 2000.0, "gamma": 1.0, "delta": 100.0},
        {"alpha": 100.0, "beta": float("inf"), "gamma": 1.0, "delta": 100.0},
        # True es subclase de int: un bool JSON no es un peso (symetría con
        # el Parlamento Educativo, que ya lo rechaza).
        {"alpha": True, "beta": 2000.0, "gamma": 1.0, "delta": 100.0},
    ]
    for params in cases:
        res = _propose(client, params)
        assert res.status_code == 400, f"{params} debió violar axioma"
        assert res.get_json()["code"] == "PARAM_AXIOM_VIOLATION"


def test_approved_proposal_applies_params(client):
    """Quórum crítico + consenso 75% → los pesos se aplican con procedencia."""
    res = _propose(
        client, {"alpha": 150.0, "beta": 3000.0, "gamma": 1.2, "delta": 50.0}
    )
    prop_id = res.get_json()["proposal"]["id"]

    # 3 de 4 usuarios votan Aprobar (quórum 0.75 ≥ 0.6; mayoría 1.0 ≥ 0.75)
    for uid in (1, 2, 3):
        assert (
            client.post(
                f"/voting/proposals/{prop_id}/vote",
                headers=auth(client, uid),
                json={
                    "option": "Aprobar",
                },
            ).status_code
            == 200
        )
    payload = _close_proposal(client, prop_id).get_json()["proposal"]
    assert payload["result"] == "passed"
    assert payload["result_detail"]["action_applied"] is True

    # Parámetros aplicados
    assert _params_in_db(client) == {
        "alpha": 150.0,
        "beta": 3000.0,
        "gamma": 1.2,
        "delta": 50.0,
    }

    # Historial de resolución con procedencia (T13)
    with client.application.app_context():
        db = get_db()
        row = db.execute(
            "SELECT proposal_id, alpha, beta FROM maxo_parameter_resolutions ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert row["proposal_id"] == prop_id
        assert row["alpha"] == 150.0
        notes = db.execute(
            "SELECT notes FROM vhv_parameters ORDER BY id DESC LIMIT 1"
        ).fetchone()["notes"]
        assert f"#{prop_id}" in notes and "Parlamento" in notes


def test_rejected_proposal_no_change(client):
    """Consenso insuficiente → los pesos actuales se mantienen."""
    before = _params_in_db(client)
    res = _propose(
        client, {"alpha": 500.0, "beta": 2000.0, "gamma": 1.0, "delta": 100.0}
    )
    prop_id = res.get_json()["proposal"]["id"]

    # 3 votos: 2 Aprobar, 1 Mantener → mayoría 2/3 = 0.667 < 0.75 → rechazada
    for uid, opt in ((1, "Aprobar"), (2, "Aprobar"), (3, "Mantener")):
        client.post(
            f"/voting/proposals/{prop_id}/vote",
            headers=auth(client, uid),
            json={"option": opt},
        )
    payload = _close_proposal(client, prop_id).get_json()["proposal"]
    assert payload["result"] == "rejected"

    assert _params_in_db(client) == before


def test_quorum_not_met_no_change(client):
    """Sin quórum (1 de 4 votos) → nada cambia."""
    before = _params_in_db(client)
    res = _propose(
        client, {"alpha": 999.0, "beta": 2000.0, "gamma": 1.0, "delta": 100.0}
    )
    prop_id = res.get_json()["proposal"]["id"]
    client.post(
        f"/voting/proposals/{prop_id}/vote",
        headers=auth(client, 1),
        json={"option": "Aprobar"},
    )
    payload = _close_proposal(client, prop_id).get_json()["proposal"]
    assert payload["result"] == "quorum_not_met"
    assert _params_in_db(client) == before


def test_parliament_public_view(client):
    """GET público: actuales + historial + propuestas abiertas (T13)."""
    res = _propose(
        client, {"alpha": 110.0, "beta": 2000.0, "gamma": 1.0, "delta": 100.0}
    )
    prop_id = res.get_json()["proposal"]["id"]
    for uid in (1, 2, 3):
        client.post(
            f"/voting/proposals/{prop_id}/vote",
            headers=auth(client, uid),
            json={"option": "Aprobar"},
        )
    _close_proposal(client, prop_id)

    data = client.get("/voting/parliament/params").get_json()
    assert data["current"]["alpha"] == 110.0
    assert len(data["history"]) == 1
    assert data["history"][0]["proposal_id"] == prop_id
    assert len(data["audit_hash"]) == 16

    # Propuesta abierta sin cerrar aparece como pendiente
    _propose(client, {"alpha": 200.0, "beta": 2000.0, "gamma": 1.0, "delta": 100.0})
    data = client.get("/voting/parliament/params").get_json()
    assert len(data["pending_proposals"]) == 1


def test_normal_proposals_unaffected(client):
    """Las propuestas normales (sin acción) se cierran sin efectos raros."""
    res = client.post(
        "/voting/proposals",
        headers=auth(client),
        json={
            "title": "Mejora de la sede",
            "description": "Pintar la sede de la Cohorte",
            "category": "operational",
            "options": ["Sí", "No"],
        },
    )
    prop_id = res.get_json()["proposal"]["id"]
    before = _params_in_db(client)
    for uid in (1, 2, 3):
        client.post(
            f"/voting/proposals/{prop_id}/vote",
            headers=auth(client, uid),
            json={"option": "Sí"},
        )
    payload = _close_proposal(client, prop_id).get_json()["proposal"]
    assert payload["result"] == "passed"
    assert _params_in_db(client) == before
    assert "action_applied" not in payload["result_detail"]
