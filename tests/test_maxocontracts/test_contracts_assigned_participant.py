"""
Tests de la vinculación de términos a partes (assigned_participant).

Cubre:
- Creación batch con assigned_participant_id por término.
- Persistencia y rehidratación (save/load).
- Endpoint add_term con assigned_participant_id.
- Respuesta del detalle del contrato.
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
            for uid, name in [(1, "Max"), (2, "Ana"), (3, "Luis")]:
                db.execute(
                    "INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, 'hash')",
                    (uid, f"{name.lower()}@test.com", name),
                )
            db.commit()
        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth_header(client):
    from app.jwt_utils import create_token

    token = create_token({"user_id": 1})
    return {"Authorization": f"Bearer {token}"}


def test_create_contract_with_assigned_terms(client, auth_header):
    """Creación batch: cada término queda vinculado a su parte obligada."""
    res = client.post(
        "/contracts/",
        headers=auth_header,
        json={
            "contract_id": "ctr-asignado-1",
            "civil_description": "Max ofrece 10 horas de trabajo",
            "participants": [
                {"user_id": 1, "wellness": 1.0},
                {"user_id": 2, "wellness": 1.0},
                {"user_id": 3, "wellness": 1.0},
            ],
            "terms": [
                {
                    "term_id": "trabajo-10h",
                    "civil_text": "Max ofrece 10 horas de trabajo",
                    "vhv": {"t": 10.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                },
                {
                    "term_id": "entrega-objeto",
                    "civil_text": "Ana entrega un objeto a cambio",
                    "vhv": {"t": 1.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-2",
                },
                {
                    "term_id": "avala-luis",
                    "civil_text": "Luis avala la reciprocidad",
                    "vhv": {"t": 0.5, "v": 0, "h": 0},
                    "assigned_participant_id": "user-3",
                },
            ],
        },
    )
    assert res.status_code == 201

    # Detalle: los términos conservan su parte asignada
    res = client.get("/contracts/ctr-asignado-1", headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()

    assigned = {t["term_id"]: t["assigned_participant"] for t in data["terms"]}
    assert assigned == {
        "trabajo-10h": "user-1",
        "entrega-objeto": "user-2",
        "avala-luis": "user-3",
    }
    assert len(data["participants"]) == 3


def test_assignment_survives_rehydration(client, auth_header):
    """La asignación persiste tras recargar el contrato desde la BD."""
    client.post(
        "/contracts/",
        headers=auth_header,
        json={
            "contract_id": "ctr-asignado-2",
            "civil_description": "Intercambio con parte asignada",
            "participants": [{"user_id": 1}, {"user_id": 2}],
            "terms": [
                {
                    "term_id": "obligacion-a",
                    "civil_text": "La Parte A se obliga a trabajar 10 horas",
                    "vhv": {"t": 10.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                }
            ],
        },
    )

    # Nueva petición = nueva carga desde la BD (rehidratación)
    res = client.get("/contracts/ctr-asignado-2", headers=auth_header)
    data = res.get_json()
    assert data["terms"][0]["assigned_participant"] == "user-1"


def test_add_term_with_assignment(client, auth_header):
    """El endpoint add_term acepta y persiste la parte asignada."""
    client.post(
        "/contracts/",
        headers=auth_header,
        json={
            "contract_id": "ctr-asignado-3",
            "civil_description": "Contrato incremental",
            "participants": [{"user_id": 1}, {"user_id": 2}],
        },
    )

    res = client.post(
        "/contracts/ctr-asignado-3/terms",
        headers=auth_header,
        json={
            "term_id": "servicio-5h",
            "civil_text": "La Parte B presta 5 horas de servicio",
            "vhv": {"t": 5.0, "v": 0, "h": 0},
            "assigned_participant_id": "user-2",
        },
    )
    assert res.status_code == 200
    assert res.get_json()["assigned_participant"] == "user-2"

    res = client.get("/contracts/ctr-asignado-3", headers=auth_header)
    assert res.get_json()["terms"][0]["assigned_participant"] == "user-2"


def test_term_without_assignment_defaults_none(client, auth_header):
    """Sin asignación explícita, el campo es null (compatibilidad)."""
    client.post(
        "/contracts/",
        headers=auth_header,
        json={
            "contract_id": "ctr-asignado-4",
            "civil_description": "Contrato sin asignación",
            "participants": [{"user_id": 1}, {"user_id": 2}],
            "terms": [
                {
                    "term_id": "generico",
                    "civil_text": "Término genérico",
                    "vhv": {"t": 1.0, "v": 0, "h": 0},
                }
            ],
        },
    )

    res = client.get("/contracts/ctr-asignado-4", headers=auth_header)
    assert res.get_json()["terms"][0]["assigned_participant"] is None
