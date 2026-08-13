"""
Tests del Puente D de la Ola 4: la plaza pública (verificador ciudadano).

Cubre:
- GET /verificador/contract/<id>: acceso público SIN login, hash canónico.
- Verificación por hash: coincidencia / no coincidencia / sin hash.
- Estabilidad: el hash canónico NO cambia con las transiciones de estado.
- Sanitización: sin emails ni fuentes personales (Opacidad Sagrada).
- GET /verificador/cohort: bienestar agregado del barrio sin login.
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

            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'a@test.com', 'Alice', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (2, 'b@test.com', 'Bob', 'hash')"
            )
            db.commit()

        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


def auth(client, uid=1):
    from app.jwt_utils import create_token

    token = create_token({"user_id": uid})
    return {"Authorization": f"Bearer {token}"}


def _create_contract_with_terms(client, contract_id="plaza-1"):
    """Contrato con 2 partes y 2 términos (activable)."""
    h = auth(client)
    assert (
        client.post(
            "/contracts/",
            headers=h,
            json={
                "contract_id": contract_id,
                "civil_description": "Intercambio de la plaza",
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            f"/contracts/{contract_id}/participants",
            headers=h,
            json={
                "user_id": 1,
                "wellness": 1.0,
            },
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"/contracts/{contract_id}/participants",
            headers=h,
            json={
                "user_id": 2,
                "wellness": 1.0,
            },
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"/contracts/{contract_id}/terms",
            headers=h,
            json={
                "term_id": "term-1",
                "civil_text": "Alice presta 5 horas a Bob",
                "vhv": {"t": 5, "v": 0, "h": 0},
                "assigned_participant_id": "user-1",
            },
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"/contracts/{contract_id}/terms",
            headers=h,
            json={
                "term_id": "term-2",
                "civil_text": "Bob devuelve un servicio de diseño",
                "vhv": {"t": 5, "v": 0, "h": 0},
                "assigned_participant_id": "user-2",
            },
        ).status_code
        == 200
    )
    return h


def test_verifier_public_without_login(client):
    """El visitante sin cuenta audita un contrato real (criterio de salida)."""
    _create_contract_with_terms(client)

    res = client.get("/verificador/contract/plaza-1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["contract_id"] == "plaza-1"
    assert data["civil_description"] == "Intercambio de la plaza"
    assert len(data["canonical_hash"]) == 64
    assert data["terms_count"] == 2
    assert {t["term_id"] for t in data["terms"]} == {"term-1", "term-2"}
    assert len(data["participants"]) == 2
    assert data["hash_matches"] is None


def test_verifier_hash_match(client):
    """Hash correcto -> integridad confirmada."""
    _create_contract_with_terms(client)
    canonical = client.get("/verificador/contract/plaza-1").get_json()["canonical_hash"]

    res = client.get(f"/verificador/contract/plaza-1?hash={canonical}")
    assert res.status_code == 200
    assert res.get_json()["hash_matches"] is True


def test_verifier_hash_mismatch(client):
    """Hash alterado -> el acuerdo NO coincide (alarma de integridad)."""
    _create_contract_with_terms(client)

    res = client.get("/verificador/contract/plaza-1?hash=" + "0" * 64)
    assert res.status_code == 200
    assert res.get_json()["hash_matches"] is False


def test_verifier_hash_stable_across_states(client):
    """El hash canónico cubre lo inmutable: activar el contrato NO lo cambia."""
    h = _create_contract_with_terms(client)

    before = client.get("/verificador/contract/plaza-1").get_json()["canonical_hash"]

    # Aceptar ambos términos por ambas partes y activar (DRAFT -> ACTIVE)
    for term in ("term-1", "term-2"):
        for uid in (1, 2):
            assert client.post(
                "/contracts/plaza-1/accept",
                headers=auth(client, uid),
                json={
                    "term_id": term,
                    "user_id": uid,
                },
            ).status_code in (200, 201)
    assert client.post("/contracts/plaza-1/activate", headers=h).status_code in (
        200,
        201,
    )

    after = client.get("/verificador/contract/plaza-1").get_json()
    assert after["canonical_hash"] == before
    assert after["state"] == "active"


def test_verifier_hash_changes_with_content(client):
    """Contenido distinto -> huella distinta (el hash no miente)."""
    _create_contract_with_terms(client, contract_id="plaza-1")
    _create_contract_with_terms(client, contract_id="plaza-2")

    h1 = client.get("/verificador/contract/plaza-1").get_json()["canonical_hash"]
    h2 = client.get("/verificador/contract/plaza-2").get_json()["canonical_hash"]
    assert h1 != h2


def test_verifier_sanitized_no_personal_data(client):
    """Opacidad Sagrada: la plaza no expone emails ni fuentes personales."""
    _create_contract_with_terms(client)

    raw = client.get("/verificador/contract/plaza-1").get_data(as_text=True)
    assert "a@test.com" not in raw
    assert "b@test.com" not in raw
    assert "reported_by" not in raw
    assert "password" not in raw.lower()

    data = client.get("/verificador/contract/plaza-1").get_json()
    participant = data["participants"][0]
    assert "email" not in participant
    assert set(participant.keys()) == {
        "participant_id",
        "party_type",
        "is_collective",
        "wellness",
        "checkins_count",
        "last_checkin_wellness",
        "last_checkin_at",
    }


def test_verifier_unknown_contract(client):
    res = client.get("/verificador/contract/nope")
    assert res.status_code == 404


def test_verifier_cohort_public(client):
    """Métricas agregadas del barrio sin login (criterio de salida)."""
    h = _create_contract_with_terms(client)
    assert (
        client.post(
            "/contracts/plaza-1/checkin",
            headers=h,
            json={
                "wellness": 0.95,
                "participant_id": "user-2",
            },
        ).status_code
        == 201
    )

    res = client.get("/verificador/cohort")
    assert res.status_code == 200
    data = res.get_json()
    assert data["plaza"] == "Cohorte Cero"
    assert data["totals"]["contracts"] == 1
    assert data["totals"]["terms"] == 2
    assert data["totals"]["checkins_total"] == 1
    assert data["totals"]["states"]["draft"] == 1
    assert (
        abs(data["wellness"]["avg"] - 0.975) < 1e-4
    )  # (1.0 de Alice + 0.95 de Bob) / 2
    assert data["wellness"]["with_latido"] == 1
    assert data["wellness"]["without_latido"] == 1
    assert data["wellness"]["source"] == "checkins"
    assert data["totals"]["tvi_total_h"] == 10.0


def test_verifier_cohort_empty_db(client):
    """Una plaza vacía responde con estructura sin romperse."""
    res = client.get("/verificador/cohort")
    assert res.status_code == 200
    data = res.get_json()
    assert data["totals"]["contracts"] == 0
    assert data["wellness"]["avg"] is None
    assert data["wellness"]["source"] is None
