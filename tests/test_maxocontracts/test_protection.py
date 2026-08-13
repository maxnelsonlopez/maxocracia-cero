"""
Tests de la Ola 3B — Escalera de salvaguardas para personas vulnerables.

Cubre (blindaje_anti_gamificacion_equidad.md §4):
- Perfil de protección: declaración, heurístico (necesidad Alta), topes.
- Shielded: bloqueo de creación sin oráculo en vivo; co-testigo obligatorio.
- Assisted/shielded: paráfrasis obligatoria y revisión oracular pre-firma.
- Topes de exposición: por contrato y por semana.
- Piso de reflexión según perfil.
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


def user_headers(client, uid):
    from app.jwt_utils import create_token

    token = create_token({"user_id": uid})
    return {"Authorization": f"Bearer {token}"}


def set_level(client, uid, level, companion=None):
    body = {"level": level}
    if companion:
        body["companion_user_id"] = companion
    res = client.post(
        "/protection/profile", headers=user_headers(client, uid), json=body
    )
    assert res.status_code == 200, res.get_json()
    return res


class FakeOracle:
    """Oráculo en vivo simulado: disponible y siempre aprueba (para tests)."""

    def __init__(self):
        pass

    def is_available(self):
        return True

    def critique(self, contract_id, contract_data):
        from maxocontracts.oracles.live_oracle import CritiqueResult

        return CritiqueResult(
            contract_id=contract_id,
            valid=True,
            issues=[],
            recommendations=[],
            reasoning="Auditoría de protección aprobada (oráculo de prueba)",
            oracle_id="fake-oracle",
        )


def create_contract(client, headers, contract_id, participants, terms=None, **extra):
    return client.post(
        "/contracts/",
        headers=headers,
        json={
            "contract_id": contract_id,
            "civil_description": "Contrato con protección",
            "participants": participants,
            "terms": terms
            or [
                {
                    "term_id": "term-1",
                    "civil_text": "Acción balanceada",
                    "vhv": {"t": 2.0, "v": 0, "h": 2.0},
                },
            ],
            **extra,
        },
    )


def backdate_contract(client, contract_id, days=2):
    """Simula un contrato creado hace `days` días: el periodo de reflexión
    ya transcurrió y la firma es legalmente posible."""
    with client.application.app_context():
        db = get_db()
        db.execute(
            "UPDATE maxo_contracts SET created_at = datetime('now', ?) WHERE contract_id = ?",
            (f"-{days} days", contract_id),
        )
        db.commit()


# ---------------------------------------------------------------------------
# Perfil de protección
# ---------------------------------------------------------------------------


class TestProfile:
    def test_declare_and_read_profile(self, client, auth_header):
        res = set_level(client, 1, "assisted", companion=2)
        assert res.get_json()["protection_level"] == "assisted"

        res = client.get("/protection/profile", headers=auth_header)
        data = res.get_json()
        assert data["protection_level"] == "assisted"
        assert data["caps"]["contract_hours"] == 20
        assert data["caps"]["reflection_hours"] == 24

    def test_invalid_level_rejected(self, client, auth_header):
        res = client.post(
            "/protection/profile", headers=auth_header, json={"level": "superuser"}
        )
        assert res.status_code == 400

    def test_self_companion_rejected(self, client, auth_header):
        res = client.post(
            "/protection/profile",
            headers=auth_header,
            json={"level": "assisted", "companion_user_id": 1},
        )
        assert res.status_code == 400

    def test_heuristic_high_urgency_need(self, client, auth_header):
        # user-4 tiene una necesidad de urgencia Alta en el dominio de formularios
        with client.application.app_context():
            db = get_db()
            db.execute(
                "INSERT INTO participants (id, name, email, city, neighborhood, offer_description, need_description, need_urgency, consent_given) "
                "VALUES (1, 'Sara', 'sara@test.com', 'Medellín', 'Centro', 'Acompañamiento', 'Salud', 'Alta', 1)"
            )
            db.execute(
                "INSERT INTO participant_needs (participant_id, description, categories, urgency, status) "
                "VALUES (1, 'Atención médica urgente', '[\"salud\"]', 'Alta', 'active')"
            )
            db.commit()

        res = client.get("/protection/profile", headers=user_headers(client, 4))
        assert res.get_json()["protection_level"] == "assisted"


# ---------------------------------------------------------------------------
# Shielded: oráculo en vivo obligatorio + co-testigo
# ---------------------------------------------------------------------------


class TestShielded:
    def test_creation_blocked_without_live_oracle(self, client, auth_header):
        set_level(client, 1, "shielded")
        res = create_contract(client, auth_header, "ctr-sh-1", [{"user_id": 1}])
        assert res.status_code == 503
        assert res.get_json()["code"] == "PROTECTION_ORACLE_REQUIRED"

    def test_creation_ok_with_live_oracle(self, client, auth_header, monkeypatch):
        monkeypatch.setattr("app.contracts_bp.LiveOracle", FakeOracle)
        set_level(client, 1, "shielded")
        res = create_contract(client, auth_header, "ctr-sh-2", [{"user_id": 1}])
        assert res.status_code == 201

    def test_witness_required_for_activation(self, client, auth_header, monkeypatch):
        monkeypatch.setattr("app.contracts_bp.LiveOracle", FakeOracle)
        set_level(client, 1, "shielded")
        create_contract(
            client,
            auth_header,
            "ctr-sh-3",
            [
                {"user_id": 1},
                {"user_id": 2},
            ],
            min_reflection_hours=72,
        )
        backdate_contract(client, "ctr-sh-3", days=4)
        client.post(
            "/contracts/ctr-sh-3/accept",
            headers=user_headers(client, 1),
            json={
                "term_id": "term-1",
                "user_id": 1,
                "comprehension": True,
                "paraphrase": "Prometo cumplir este acuerdo",
            },
        )
        client.post(
            "/contracts/ctr-sh-3/accept",
            headers=user_headers(client, 2),
            json={"term_id": "term-1", "user_id": 2},
        )

        res = client.post("/contracts/ctr-sh-3/activate", headers=auth_header)
        assert res.status_code == 400
        assert res.get_json()["code"] == "WITNESS_REQUIRED"

        # Las partes no pueden ser testigos
        res = client.post(
            "/contracts/ctr-sh-3/witness", headers=user_headers(client, 2)
        )
        assert res.status_code == 400

        # user-3 (ajeno a las partes) es testigo
        res = client.post(
            "/contracts/ctr-sh-3/witness", headers=user_headers(client, 3)
        )
        assert res.status_code == 200

        res = client.post("/contracts/ctr-sh-3/activate", headers=auth_header)
        assert res.status_code == 200
        assert res.get_json()["state"] == "active"


# ---------------------------------------------------------------------------
# Paráfrasis y revisión oracular (assisted)
# ---------------------------------------------------------------------------


class TestComprehension:
    def test_assisted_sign_requires_paraphrase(self, client, auth_header, monkeypatch):
        monkeypatch.setattr("app.contracts_bp.LiveOracle", FakeOracle)
        set_level(client, 1, "assisted")
        create_contract(
            client,
            auth_header,
            "ctr-cp-1",
            [{"user_id": 1}, {"user_id": 2}],
            min_reflection_hours=24,
        )
        backdate_contract(client, "ctr-cp-1", days=2)

        # Sin paráfrasis -> 400
        res = client.post(
            "/contracts/ctr-cp-1/accept",
            headers=auth_header,
            json={"term_id": "term-1", "user_id": 1},
        )
        assert res.status_code == 400
        assert res.get_json()["code"] == "PROTECTION_PARAPHRASE_REQUIRED"

        # Con paráfrasis y comprensión -> 200 (oráculo disponible)
        res = client.post(
            "/contracts/ctr-cp-1/accept",
            headers=auth_header,
            json={
                "term_id": "term-1",
                "user_id": 1,
                "comprehension": True,
                "paraphrase": "Entiendo que doy dos horas de mi tiempo",
            },
        )
        assert res.status_code == 200

        # La paráfrasis queda registrada (T13)
        with client.application.app_context():
            row = (
                get_db()
                .execute(
                    "SELECT paraphrase FROM maxo_contract_term_approvals "
                    "WHERE contract_id = 'ctr-cp-1' AND term_id = 'term-1' AND participant_id = 'user-1'"
                )
                .fetchone()
            )
            assert row["paraphrase"].startswith("Entiendo que")

    def test_assisted_sign_blocked_without_live_oracle(self, client, auth_header):
        """La degradación elegante está PROHIBIDA para perfiles protegidos."""
        set_level(client, 1, "assisted")
        create_contract(
            client,
            auth_header,
            "ctr-cp-2",
            [{"user_id": 1}, {"user_id": 2}],
            min_reflection_hours=24,
        )
        backdate_contract(client, "ctr-cp-2", days=2)
        res = client.post(
            "/contracts/ctr-cp-2/accept",
            headers=auth_header,
            json={
                "term_id": "term-1",
                "user_id": 1,
                "comprehension": True,
                "paraphrase": "Entiendo que doy dos horas de mi tiempo",
            },
        )
        assert res.status_code == 503
        assert res.get_json()["code"] == "PROTECTION_ORACLE_REQUIRED"

    def test_protected_delegate_requires_paraphrase(
        self, client, auth_header, monkeypatch
    ):
        monkeypatch.setattr("app.contracts_bp.LiveOracle", FakeOracle)
        set_level(client, 1, "assisted")
        res = client.post(
            "/parties/",
            headers=auth_header,
            json={
                "party_id": "coop-7",
                "party_type": "cooperative",
                "display_name": "Coop",
                "members": {"delegates": ["user-1", "user-2"], "quorum": 1.0},
            },
        )
        assert res.status_code == 201
        create_contract(
            client,
            auth_header,
            "ctr-cp-3",
            [
                {"user_id": 1},
                {"user_id": 2},
                {"party_id": "coop-7"},
            ],
            min_reflection_hours=24,
        )
        backdate_contract(client, "ctr-cp-3", days=2)

        # user-1 (asistido) firma como delegado sin paráfrasis -> 400
        res = client.post(
            "/contracts/ctr-cp-3/accept",
            headers=auth_header,
            json={"term_id": "term-1", "party_id": "coop-7"},
        )
        assert res.status_code == 400

        # Con paráfrasis -> voto registrado
        res = client.post(
            "/contracts/ctr-cp-3/accept",
            headers=auth_header,
            json={
                "term_id": "term-1",
                "party_id": "coop-7",
                "comprehension": True,
                "paraphrase": "Entiendo el quorum de mi cooperativa",
            },
        )
        assert res.status_code == 202


# ---------------------------------------------------------------------------
# Topes de exposición
# ---------------------------------------------------------------------------


class TestExposureCaps:
    def test_shielded_contract_cap(self, client, auth_header, monkeypatch):
        monkeypatch.setattr("app.contracts_bp.LiveOracle", FakeOracle)
        set_level(client, 1, "shielded")  # tope 8h por contrato

        res = create_contract(
            client,
            auth_header,
            "ctr-cap-1",
            [
                {"user_id": 1},
                {"user_id": 2},
            ],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": "Diez horas de trabajo",
                    "vhv": {"t": 10.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                },
            ],
        )
        assert res.status_code == 400
        assert res.get_json()["code"] == "PROTECTION_CAP_EXCEEDED"

        # Dentro del tope (7h) -> OK
        res = create_contract(
            client,
            auth_header,
            "ctr-cap-2",
            [
                {"user_id": 1},
                {"user_id": 2},
            ],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": "Siete horas de trabajo",
                    "vhv": {"t": 7.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                },
            ],
        )
        assert res.status_code == 201

    def test_assisted_weekly_cap(self, client, auth_header):
        set_level(client, 1, "assisted")  # tope semanal 40h
        create_contract(
            client,
            auth_header,
            "ctr-cap-3",
            [
                {"user_id": 1},
                {"user_id": 2},
            ],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": "Veinte horas de trabajo",
                    "vhv": {"t": 20.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                },
            ],
        )
        # Segundo contrato: 25h más -> 45h > 40h
        res = create_contract(
            client,
            auth_header,
            "ctr-cap-4",
            [
                {"user_id": 1},
                {"user_id": 2},
            ],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": "Veinticinco horas de trabajo",
                    "vhv": {"t": 25.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                },
            ],
        )
        assert res.status_code == 400
        assert res.get_json()["code"] == "PROTECTION_CAP_EXCEEDED"


# ---------------------------------------------------------------------------
# Piso de reflexión
# ---------------------------------------------------------------------------


class TestReflectionFloor:
    def test_assisted_floor_enforced(self, client, auth_header):
        set_level(client, 1, "assisted")  # piso 24h
        res = create_contract(
            client, auth_header, "ctr-rf-1", [{"user_id": 1}], min_reflection_hours=0
        )
        assert res.status_code == 400
        assert res.get_json()["code"] == "PROTECTION_REFLECTION_FLOOR"

        res = create_contract(
            client, auth_header, "ctr-rf-2", [{"user_id": 1}], min_reflection_hours=30
        )
        assert res.status_code == 201
        assert res.get_json()["min_reflection_hours"] == 30

    def test_shielded_default_reflection(self, client, auth_header, monkeypatch):
        monkeypatch.setattr("app.contracts_bp.LiveOracle", FakeOracle)
        set_level(client, 1, "shielded")  # piso 72h
        res = create_contract(client, auth_header, "ctr-rf-3", [{"user_id": 1}])
        assert res.status_code == 201
        assert res.get_json()["min_reflection_hours"] == 72
