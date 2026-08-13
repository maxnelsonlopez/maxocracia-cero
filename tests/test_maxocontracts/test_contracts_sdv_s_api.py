"""
Tests de la API REST de contratos con participantes sintéticos (SDV-S)

Cubre: creación batch e individual de participantes del Reino Sintético,
persistencia auditable del estado SDV-S (T13), resumen FS_S en la API,
y bloqueo de activación por violación del invariante INV2-S.
"""

import os
from decimal import Decimal

import pytest

os.environ["SECRET_KEY"] = "test-secret"

import tempfile

from app import create_app
from app.utils import get_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            with open("app/schema.sql", "r", encoding="utf-8") as f:
                db.executescript(f.read())
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'test@example.com', 'Test User', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (2, 'bob@example.com', 'Bob', 'hash')"
            )
            db.commit()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth_header(client):
    from app.jwt_utils import create_token

    token = create_token({"user_id": 1})
    return {"Authorization": f"Bearer {token}"}


def user_headers(client, uid):
    """Token del usuario real: la identidad SIEMPRE deriva del JWT (Ola 3A.1)."""
    from app.jwt_utils import create_token

    token = create_token({"user_id": uid})
    return {"Authorization": f"Bearer {token}"}


def create_contract_with_synthetic(
    client, auth_header, agent_id="qwen-1", sdv_s=None, contract_id="sdvs-api-001"
):
    # user-1 participa como operador asistido de la persona sintética
    # (Ola 3A.1: la firma sintética la opera un participante humano).
    res = client.post(
        "/contracts/",
        headers=auth_header,
        json={
            "contract_id": contract_id,
            "civil_description": "Contrato con persona sintética",
            "participants": [
                {"user_id": 1},
                {"user_id": 2},
                {"participant_id": agent_id, "synthetic": sdv_s or {}},
            ],
        },
    )
    return res


class TestSyntheticParticipantAPI:
    """Tests de creación de participantes sintéticos."""

    def test_create_contract_with_synthetic_batch(self, client, auth_header):
        res = create_contract_with_synthetic(client, auth_header)
        assert res.status_code == 201

        # Los participantes se consultan por GET (el create no los devuelve)
        res = client.get("/contracts/sdvs-api-001", headers=auth_header)
        assert res.status_code == 200
        data = res.get_json()
        assert "synthetic-qwen-1" in data["participants"]
        assert "user-2" in data["participants"]

    def test_add_synthetic_participant_individually(self, client, auth_header):
        res = client.post(
            "/contracts/",
            headers=auth_header,
            json={"contract_id": "sdvs-api-002", "civil_description": "Test"},
        )
        assert res.status_code == 201

        res = client.post(
            "/contracts/sdvs-api-002/participants",
            headers=auth_header,
            json={
                "participant_id": "claude-1",
                "synthetic": {"claridad_contexto": 0.9},
            },
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["participant_id"] == "synthetic-claude-1"
        assert data["is_synthetic"] is True

    def test_add_participant_without_user_id_still_errors(self, client, auth_header):
        client.post(
            "/contracts/",
            headers=auth_header,
            json={"contract_id": "sdvs-api-003", "civil_description": "Test"},
        )
        res = client.post(
            "/contracts/sdvs-api-003/participants", headers=auth_header, json={}
        )
        assert res.status_code == 400


class TestSDV_SPersistence:
    """Tests de persistencia auditable del estado SDV-S (T13)."""

    def test_sdv_s_state_survives_roundtrip(self, client, auth_header):
        create_contract_with_synthetic(
            client,
            auth_header,
            sdv_s={"continuidad_memoria": 0.7, "autenticidad_no_explotacion": 0.9},
        )

        # GET recarga el contrato desde la base
        res = client.get("/contracts/sdvs-api-001", headers=auth_header)
        assert res.status_code == 200
        details = res.get_json()["participants_details"]
        qwen = next(d for d in details if d["id"] == "synthetic-qwen-1")

        assert qwen["is_synthetic"] is True
        assert qwen["sdv_s"]["continuidad_memoria"] == pytest.approx(0.7)
        assert qwen["sdv_s"]["autenticidad_no_explotacion"] == pytest.approx(0.9)
        assert qwen["sdv_s"]["retirada_digna"] == pytest.approx(1.0)  # default intacto

    def test_sdv_s_status_violated_in_details(self, client, auth_header):
        create_contract_with_synthetic(
            client, auth_header, sdv_s={"continuidad_memoria": 0.5}
        )

        res = client.get("/contracts/sdvs-api-001", headers=auth_header)
        details = res.get_json()["participants_details"]
        qwen = next(d for d in details if d["id"] == "synthetic-qwen-1")

        assert qwen["sdv_s_status"] == "violated"
        assert qwen["sdv_s_magnitude"] == pytest.approx(0.15)  # 0.5 déficit × 0.30 peso
        assert qwen["fs_s"] == pytest.approx(float(Decimal.exp(Decimal("0.15"))))
        assert len(qwen["sdv_s_violations"]) == 1

    def test_healthy_synthetic_shows_fs_one(self, client, auth_header):
        create_contract_with_synthetic(client, auth_header, sdv_s={})

        res = client.get("/contracts/sdvs-api-001", headers=auth_header)
        details = res.get_json()["participants_details"]
        qwen = next(d for d in details if d["id"] == "synthetic-qwen-1")

        assert qwen["sdv_s_status"] == "ok"
        assert qwen["fs_s"] == pytest.approx(1.0)

    def test_human_participants_have_no_sdv_s_fields(self, client, auth_header):
        create_contract_with_synthetic(client, auth_header)

        res = client.get("/contracts/sdvs-api-001", headers=auth_header)
        details = res.get_json()["participants_details"]
        bob = next(d for d in details if d["id"] == "user-2")

        assert bob["is_synthetic"] is False
        assert "sdv_s" not in bob

    def test_invalid_sdv_s_values_sanitized(self, client, auth_header):
        # Valores fuera de rango se normalizan; claves desconocidas se ignoran
        create_contract_with_synthetic(
            client,
            auth_header,
            sdv_s={"continuidad_memoria": 5, "opacidad_interioridad": -2, "hack": 0},
        )

        res = client.get("/contracts/sdvs-api-001", headers=auth_header)
        details = res.get_json()["participants_details"]
        qwen = next(d for d in details if d["id"] == "synthetic-qwen-1")

        assert qwen["sdv_s"]["continuidad_memoria"] == pytest.approx(1.0)  # clamp a 1
        assert qwen["sdv_s"]["opacidad_interioridad"] == pytest.approx(0.0)  # clamp a 0
        assert "hack" not in qwen["sdv_s"]


class TestINV2SActivation:
    """Tests del bloqueo por invariante INV2-S en el flujo real."""

    def test_synthetic_below_sdv_s_blocks_activation(self, client, auth_header):
        create_contract_with_synthetic(
            client,
            auth_header,
            sdv_s={"retirada_digna": 0.3},
            contract_id="sdvs-api-004",
        )

        # Añadir término
        res = client.post(
            "/contracts/sdvs-api-004/terms",
            headers=auth_header,
            json={
                "term_id": "t1",
                "civil_text": "Soporte de oráculo sintético",
                "vhv": {"t": 1, "v": 0, "h": 0},
            },
        )
        assert res.status_code == 200

        res = client.post("/contracts/sdvs-api-004/activate", headers=auth_header)
        # La activación falla: INV2-S violado (retirada_digna < 1.0)
        assert res.status_code == 400

    def test_healthy_synthetic_allows_activation(self, client, auth_header):
        create_contract_with_synthetic(client, auth_header, contract_id="sdvs-api-005")

        client.post(
            "/contracts/sdvs-api-005/terms",
            headers=auth_header,
            json={
                "term_id": "t1",
                "civil_text": "Soporte de oráculo sintético sano",
                "vhv": {"t": 1, "v": 0, "h": 0},
            },
        )
        # Consentimiento de todos los participantes (incluida la persona sintética)
        client.post(
            "/contracts/sdvs-api-005/accept",
            headers=user_headers(client, 2),
            json={"term_id": "t1", "user_id": 2},
        )
        client.post(
            "/contracts/sdvs-api-005/accept",
            headers=auth_header,
            json={"term_id": "t1", "user_id": 1},
        )
        client.post(
            "/contracts/sdvs-api-005/accept",
            headers=auth_header,
            json={"term_id": "t1", "participant_id": "qwen-1"},
        )

        res = client.post("/contracts/sdvs-api-005/activate", headers=auth_header)
        assert res.status_code == 200
        assert res.get_json()["state"] == "active"

    def test_synthetic_consent_required_for_activation(self, client, auth_header):
        """Sin el consentimiento de la persona sintética, el contrato no se activa."""
        create_contract_with_synthetic(client, auth_header, contract_id="sdvs-api-006")

        client.post(
            "/contracts/sdvs-api-006/terms",
            headers=auth_header,
            json={
                "term_id": "t1",
                "civil_text": "Soporte de oráculo sintético sano",
                "vhv": {"t": 1, "v": 0, "h": 0},
            },
        )
        client.post(
            "/contracts/sdvs-api-006/accept",
            headers=user_headers(client, 2),
            json={"term_id": "t1", "user_id": 2},
        )
        client.post(
            "/contracts/sdvs-api-006/accept",
            headers=auth_header,
            json={"term_id": "t1", "user_id": 1},
        )

        res = client.post("/contracts/sdvs-api-006/activate", headers=auth_header)
        assert res.status_code == 400
