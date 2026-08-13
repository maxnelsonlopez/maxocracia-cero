"""
Tests del Blindaje Anti-Gamificación (Ola 3A).

Cubre los vectores del análisis de riesgo (blindaje_anti_gamificacion_equidad.md):
- R1  Suplantación de firma -> 403 IDENTITY_MISMATCH
- R2  Reescritura de contratos -> 409 CONTRACT_CONFLICT
- R3  Secuestro de gobernanza -> 403 GOVERNANCE_FORBIDDEN / quórum de delegados
- R5  γ fuera de rango [0.5, 1.5] -> 400 + fuente del reporte (reported_by)
- R6  T17: asimetría declarada -> activación bloqueada hasta reconocimiento
- R7/R8 Cláusulas prohibidas y lenguaje civil -> 400
- R9  Obligaciones sin parte responsable -> 400 UNASSIGNED_OBLIGATION
- R10/R11 Ventanas temporales (deadline y reflexión) -> 423
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
    """Token del usuario real: la identidad SIEMPRE deriva del JWT (Ola 3A.1)."""
    from app.jwt_utils import create_token

    token = create_token({"user_id": uid})
    return {"Authorization": f"Bearer {token}"}


def make_party(client, auth_header, party_id, party_type, name, members=None):
    res = client.post(
        "/parties/",
        headers=auth_header,
        json={
            "party_id": party_id,
            "party_type": party_type,
            "display_name": name,
            "members": members or {},
        },
    )
    assert res.status_code == 201, res.get_json()
    return res.get_json()["party"]


def create_contract(client, headers, contract_id, participants, terms=None, **extra):
    return client.post(
        "/contracts/",
        headers=headers,
        json={
            "contract_id": contract_id,
            "civil_description": "Contrato de blindaje",
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


# ---------------------------------------------------------------------------
# R1 — Identidad vinculada al token
# ---------------------------------------------------------------------------


class TestIdentity:
    def test_sign_as_other_user_rejected(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-id-1", [{"user_id": 1}, {"user_id": 2}]
        )
        res = client.post(
            "/contracts/ctr-id-1/accept",
            headers=auth_header,
            json={"term_id": "term-1", "user_id": 2},
        )
        assert res.status_code == 403
        assert res.get_json()["code"] == "IDENTITY_MISMATCH"

    def test_sign_own_term_ok(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-id-2", [{"user_id": 1}, {"user_id": 2}]
        )
        res = client.post(
            "/contracts/ctr-id-2/accept",
            headers=auth_header,
            json={"term_id": "term-1", "user_id": 1},
        )
        assert res.status_code == 200

    def test_delegate_spoofing_has_no_effect(self, client, auth_header):
        make_party(
            client,
            auth_header,
            "coop-7",
            "cooperative",
            "Coop",
            members={
                "delegates": ["user-1", "user-2"],
                "quorum": 1.0,
            },
        )
        create_contract(
            client,
            auth_header,
            "ctr-id-3",
            [
                {"user_id": 1},
                {"user_id": 2},
                {"party_id": "coop-7"},
            ],
        )
        # user-1 (token 1) envía delegate_id de user-2: el sistema IGNORA el
        # campo y firma como el actor real del token (el voto es de user-1).
        res = client.post(
            "/contracts/ctr-id-3/accept",
            headers=auth_header,
            json={"term_id": "term-1", "party_id": "coop-7", "delegate_id": "user-2"},
        )
        assert res.status_code == 202
        assert res.get_json()["delegate_id"] == "user-1"

    def test_nps_for_other_rejected(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-id-4", [{"user_id": 1}, {"user_id": 2}]
        )
        res = client.post(
            "/contracts/ctr-id-4/nps",
            headers=auth_header,
            json={"participant_id": "user-2", "score": 9},
        )
        assert res.status_code == 403


# ---------------------------------------------------------------------------
# R2 — Inmutabilidad de contratos
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_recreate_active_contract_conflict(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-imm-1", [{"user_id": 1}, {"user_id": 2}]
        )
        for uid in (1, 2):
            client.post(
                "/contracts/ctr-imm-1/accept",
                headers=user_headers(client, uid),
                json={"term_id": "term-1", "user_id": uid},
            )
        assert (
            client.post(
                "/contracts/ctr-imm-1/activate", headers=auth_header
            ).status_code
            == 200
        )

        res = create_contract(client, auth_header, "ctr-imm-1", [{"user_id": 1}])
        assert res.status_code == 409
        assert res.get_json()["code"] == "CONTRACT_CONFLICT"

    def test_recreate_others_draft_conflict(self, client, auth_header):
        create_contract(client, auth_header, "ctr-imm-2", [{"user_id": 1}])
        # user-2 intenta re-crear el borrador de user-1
        res = create_contract(
            client, user_headers(client, 2), "ctr-imm-2", [{"user_id": 2}]
        )
        assert res.status_code == 409

    def test_recreate_own_draft_allowed(self, client, auth_header):
        create_contract(client, auth_header, "ctr-imm-3", [{"user_id": 1}])
        res = create_contract(client, auth_header, "ctr-imm-3", [{"user_id": 1}])
        assert res.status_code == 201


# ---------------------------------------------------------------------------
# R3 — Autoridad sobre las partes
# ---------------------------------------------------------------------------


class TestPartyAuthority:
    def test_non_owner_update_forbidden(self, client, auth_header):
        make_party(
            client,
            auth_header,
            "coop-7",
            "cooperative",
            "Coop de Max",
            members={
                "delegates": ["user-1", "user-2"],
                "quorum": 1.0,
            },
        )
        # user-3 intenta secuestrar la gobernanza
        res = client.put(
            "/parties/coop-7",
            headers=user_headers(client, 3),
            json={
                "members": {"delegates": ["user-3"], "quorum": 1.0},
            },
        )
        assert res.status_code == 403
        assert res.get_json()["code"] == "GOVERNANCE_FORBIDDEN"

    def test_owner_update_ok(self, client, auth_header):
        make_party(
            client,
            auth_header,
            "coop-7",
            "cooperative",
            "Coop de Max",
            members={
                "delegates": ["user-1", "user-2"],
                "quorum": 1.0,
            },
        )
        res = client.put(
            "/parties/coop-7",
            headers=auth_header,
            json={
                "members": {"delegates": ["user-1"], "quorum": 1.0},
            },
        )
        assert res.status_code == 200

    def test_delegate_quorum_governance_change(self, client, auth_header):
        make_party(
            client,
            auth_header,
            "coop-7",
            "cooperative",
            "Coop de Max",
            members={
                "delegates": ["user-1", "user-2", "user-3"],
                "quorum": 0.6,
            },
        )
        proposal = {"delegates": ["user-2", "user-3", "user-4"], "quorum": 0.6}

        # user-2 vota
        res = client.post(
            "/parties/coop-7/governance-change",
            headers=user_headers(client, 2),
            json={"members": proposal, "reason": "Renovación"},
        )
        assert res.status_code == 202
        assert res.get_json()["applied"] is False
        assert res.get_json()["votes"] == 1

        # No-delegado no puede votar
        res = client.post(
            "/parties/coop-7/governance-change",
            headers=user_headers(client, 4),
            json={"members": proposal},
        )
        assert res.status_code == 403

        # user-3 vota -> quórum (2 de 3) -> se aplica
        res = client.post(
            "/parties/coop-7/governance-change",
            headers=user_headers(client, 3),
            json={"members": proposal},
        )
        assert res.status_code == 200
        assert res.get_json()["applied"] is True

        res = client.get("/parties/coop-7", headers=auth_header)
        assert res.get_json()["party"]["members"]["delegates"] == [
            "user-2",
            "user-3",
            "user-4",
        ]

    def test_non_owner_delete_forbidden(self, client, auth_header):
        make_party(
            client,
            auth_header,
            "coop-7",
            "cooperative",
            "Coop de Max",
            members={
                "delegates": ["user-1"],
                "quorum": 1.0,
            },
        )
        res = client.delete("/parties/coop-7", headers=user_headers(client, 2))
        assert res.status_code == 403


# ---------------------------------------------------------------------------
# R5 — γ con fuente y topes
# ---------------------------------------------------------------------------


class TestWellnessSource:
    def test_wellness_out_of_range_rejected(self, client, auth_header):
        res = create_contract(
            client, auth_header, "ctr-g-1", [{"user_id": 1, "wellness": 2.0}]
        )
        assert res.status_code == 400
        assert "rango" in res.get_json()["error"]

        create_contract(client, auth_header, "ctr-g-2", [{"user_id": 1}])
        res = client.post(
            "/contracts/ctr-g-2/participants",
            headers=auth_header,
            json={"user_id": 2, "wellness": 0.4},
        )
        assert res.status_code == 400

    def test_wellness_reported_by_recorded(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-g-3", [{"user_id": 1, "wellness": 1.2}]
        )
        with client.application.app_context():
            row = (
                get_db()
                .execute(
                    "SELECT reported_by FROM maxo_contract_participants "
                    "WHERE contract_id = 'ctr-g-3' AND participant_id = 'user-1'"
                )
                .fetchone()
            )
            assert row["reported_by"] == "user-1"


# ---------------------------------------------------------------------------
# R6 — T17 ejecutable: asimetría declarada
# ---------------------------------------------------------------------------


class TestAsymmetry:
    def _imbalanced(self, client, auth_header, contract_id):
        """user-1 carga 10h vs user-2 3h -> 76.9% > 70%: flag activo."""
        return create_contract(
            client,
            auth_header,
            contract_id,
            [
                {"user_id": 1},
                {"user_id": 2},
            ],
            terms=[
                {
                    "term_id": "do",
                    "civil_text": "Max ofrece diez horas",
                    "vhv": {"t": 10.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-1",
                },
                {
                    "term_id": "give",
                    "civil_text": "Ana ofrece tres horas",
                    "vhv": {"t": 3.0, "v": 0, "h": 0},
                    "assigned_participant_id": "user-2",
                },
            ],
            min_reflection_hours=0,
        )

    def test_imbalance_flagged_but_creatable(self, client, auth_header):
        res = self._imbalanced(client, auth_header, "ctr-asym-1")
        assert res.status_code == 201
        assert res.get_json()["requires_asymmetry_acknowledgment"] is True

    def test_activation_blocked_without_acknowledgment(self, client, auth_header):
        self._imbalanced(client, auth_header, "ctr-asym-2")
        for uid in (1, 2):
            for term in ("do", "give"):
                client.post(
                    "/contracts/ctr-asym-2/accept",
                    headers=user_headers(client, uid),
                    json={"term_id": term, "user_id": uid},
                )
        res = client.post("/contracts/ctr-asym-2/activate", headers=auth_header)
        assert res.status_code == 400
        assert res.get_json()["code"] == "ASYMMETRY_UNACKNOWLEDGED"
        assert set(res.get_json()["missing"]) == {"user-1", "user-2"}

    def test_activation_after_full_acknowledgment(self, client, auth_header):
        self._imbalanced(client, auth_header, "ctr-asym-3")
        for uid in (1, 2):
            for term in ("do", "give"):
                client.post(
                    "/contracts/ctr-asym-3/accept",
                    headers=user_headers(client, uid),
                    json={"term_id": term, "user_id": uid},
                )
            res = client.post(
                "/contracts/ctr-asym-3/acknowledge-asymmetry",
                headers=user_headers(client, uid),
                json={"party_id": f"user-{uid}"},
            )
            assert res.status_code == 200
        res = client.post("/contracts/ctr-asym-3/activate", headers=auth_header)
        assert res.status_code == 200
        assert res.get_json()["state"] == "active"


# ---------------------------------------------------------------------------
# R7/R8 — Cláusulas prohibidas y lenguaje civil
# ---------------------------------------------------------------------------


class TestProhibitedClauses:
    def test_retraction_waiver_rejected(self, client, auth_header):
        res = create_contract(
            client,
            auth_header,
            "ctr-proh-1",
            [{"user_id": 1}],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": "Sin derecho a retractarse nunca",
                    "vhv": {"t": 1.0, "v": 0, "h": 0},
                },
            ],
        )
        assert res.status_code == 400
        assert "prohibida" in res.get_json()["error"]

    def test_exclusivity_rejected_on_add_term(self, client, auth_header):
        create_contract(client, auth_header, "ctr-proh-2", [{"user_id": 1}])
        res = client.post(
            "/contracts/ctr-proh-2/terms",
            headers=auth_header,
            json={
                "term_id": "t1",
                "civil_text": "Exclusividad total con el taller",
                "vhv": {"t": 1.0, "v": 0, "h": 0},
            },
        )
        assert res.status_code == 400

    def test_legalese_rejected(self, client, auth_header):
        long_text = " ".join(["palabra"] * 45)
        res = create_contract(
            client,
            auth_header,
            "ctr-proh-3",
            [{"user_id": 1}],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": long_text,
                    "vhv": {"t": 1.0, "v": 0, "h": 0},
                },
            ],
        )
        assert res.status_code == 400
        assert "palabras" in res.get_json()["error"]


# ---------------------------------------------------------------------------
# R9 — Obligaciones sin parte responsable
# ---------------------------------------------------------------------------


class TestUnassignedObligations:
    def test_unassigned_heavy_term_rejected(self, client, auth_header):
        res = create_contract(
            client,
            auth_header,
            "ctr-ob-1",
            [{"user_id": 1}],
            terms=[
                {
                    "term_id": "t1",
                    "civil_text": "Diez horas de trabajo",
                    "vhv": {"t": 10.0, "v": 0, "h": 0},
                },  # sin assigned_participant_id
            ],
        )
        assert res.status_code == 400
        assert res.get_json()["code"] == "UNASSIGNED_OBLIGATION"


# ---------------------------------------------------------------------------
# R10/R11 — Ventanas temporales
# ---------------------------------------------------------------------------


class TestTimeWindows:
    def test_signature_deadline_expired(self, client, auth_header):
        create_contract(
            client,
            auth_header,
            "ctr-win-1",
            [{"user_id": 1}],
            signature_deadline="2020-01-01T00:00:00",
        )
        res = client.post(
            "/contracts/ctr-win-1/accept",
            headers=auth_header,
            json={"term_id": "term-1", "user_id": 1},
        )
        assert res.status_code == 423
        assert res.get_json()["code"] == "SIGNATURE_DEADLINE_EXPIRED"

    def test_reflection_window_blocks_signing(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-win-2", [{"user_id": 1}], min_reflection_hours=24
        )
        res = client.post(
            "/contracts/ctr-win-2/accept",
            headers=auth_header,
            json={"term_id": "term-1", "user_id": 1},
        )
        assert res.status_code == 423
        assert res.get_json()["code"] == "REFLECTION_PENDING"

    def test_reflection_zero_allows_immediate(self, client, auth_header):
        create_contract(
            client, auth_header, "ctr-win-3", [{"user_id": 1}], min_reflection_hours=0
        )
        res = client.post(
            "/contracts/ctr-win-3/accept",
            headers=auth_header,
            json={"term_id": "term-1", "user_id": 1},
        )
        assert res.status_code == 200
