# -*- coding: utf-8 -*-
"""Tests del Parlamento Educativo — umbral canónico del puente años<->índice
(rama educativa M5/M8; gobierna SDV-H IV, Cap. 11/14, T13).

La LEY (INV2-EDU: >= 12 años, maxocontracts) no se vota; se vota la plenitud
aspiracional del puente (12-30). Cubre: validación axiomática, creación de la
propuesta crítica, ejecución vinculante al aprobarse, rechazo sin efecto,
anti-flip-flop, y el uso del canónico por el analizador SDV.
"""

import os
import tempfile

os.environ["SECRET_KEY"] = "test-secret"
os.environ.pop("DEEPSEEK_API_KEY", None)

import pytest

from app import create_app
from app.sdv_analyzer import SDVAnalyzer, educacion_indice
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
                    "INSERT INTO users (id, email, name, password_hash, trust_level) VALUES (?, ?, ?, 'hash', 1)",
                    (uid, f"{name.lower()}@test.com", name),
                )
            # Recién llegada (N0): la voz en la gobernanza se gana caminando
            # el primer acuerdo (escalera de confianza, Cap. 13).
            db.execute(
                "INSERT INTO users (id, email, name, password_hash, trust_level) VALUES (?, ?, ?, 'hash', 0)",
                (5, "n0@test.com", "Recien"),
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


def _propose(client, auth, **over):
    payload = {
        "umbral_anios": over.get("umbral_anios", 14),
        "reason": over.get("reason", "plenitud aspiracional de la cohorte"),
        "deadline_hours": over.get("deadline_hours", 72),
    }
    return client.post(
        "/voting/parliament/educativo", json=payload, headers=auth(over.get("uid", 1))
    )


class TestValidacionAxiomatica:
    def test_umbral_bajo_la_ley_rechazado(self, client, auth):
        """El piso legal no se vota: 11.9 años viola INV2-EDU."""
        resp = _propose(client, auth, umbral_anios=11.9)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "PARAM_AXIOM_VIOLATION"
        assert "12" in resp.get_json()["error"]

    def test_umbral_sobre_limite_sano_rechazado(self, client, auth):
        resp = _propose(client, auth, umbral_anios=31)
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "PARAM_AXIOM_VIOLATION"

    def test_umbral_no_numerico_rechazado(self, client, auth):
        resp = _propose(client, auth, umbral_anios="doce")
        assert resp.status_code == 400

    def test_boolean_rechazado(self, client, auth):
        """True es subclase de int: un bool JSON no es un umbral."""
        resp = _propose(client, auth, umbral_anios=True)
        assert resp.status_code == 400

    def test_nan_rechazado(self, client, auth):
        """NaN no es un umbral: ni < 12 ni > 30 pero no es finito (JSON
        permissivo lo admite; el parlamento no se confunde)."""
        resp = _propose(client, auth, umbral_anios=float("nan"))
        assert resp.status_code == 400
        assert "finito" in resp.get_json()["error"]

    def test_infinito_rechazado(self, client, auth):
        resp = _propose(client, auth, umbral_anios=float("inf"))
        assert resp.status_code == 400

    def test_menos_infinito_rechazado(self, client, auth):
        resp = _propose(client, auth, umbral_anios=float("-inf"))
        assert resp.status_code == 400

    def test_umbral_en_frontera_maxima_aceptado(self, client, auth):
        resp = _propose(client, auth, umbral_anios=30)
        assert resp.status_code == 201

    def test_sin_auth_rechazado(self, client):
        resp = client.post(
            "/voting/parliament/educativo", json={"umbral_anios": 14}
        )
        assert resp.status_code == 401

    def test_recien_llegado_n0_no_puede_proponer(self, client, auth):
        """Escalera de confianza (Cap. 13): proponer en el parlamento es
        gobernar; un N0 recibe y firma, no propone."""
        resp = _propose(client, auth, umbral_anios=14, uid=5)
        assert resp.status_code == 403
        assert resp.get_json()["code"] == "TRUST_LEVEL_REQUIRED"

    def test_sin_campo_rechazado(self, client, auth):
        resp = client.post("/voting/parliament/educativo", json={}, headers=auth(1))
        assert resp.status_code == 400


class TestCreacionPropuesta:
    def test_propone_umbral_valido_como_critical(self, client, auth):
        resp = _propose(client, auth, umbral_anios=14)
        assert resp.status_code == 201
        prop = resp.get_json()["proposal"]
        assert prop["category"] == "critical"
        assert prop["quorum_ratio"] == 0.6
        assert prop["majority_ratio"] == 0.75
        assert prop["status"] == "open"
        assert prop["action"]["type"] == "set_edu_umbral"
        assert prop["action"]["params"]["umbral_anios"] == 14.0

    def test_umbral_float_aceptado(self, client, auth):
        resp = _propose(client, auth, umbral_anios=12.5)
        assert resp.status_code == 201

    def test_umbral_igual_a_ley_aceptado(self, client, auth):
        """Confirmar el canon también es una decisión comunitaria."""
        resp = _propose(client, auth, umbral_anios=12)
        assert resp.status_code == 201

    def test_get_publico_muestra_pendiente_y_canon(self, client, auth):
        _propose(client, auth, umbral_anios=14)
        data = client.get("/voting/parliament/educativo").get_json()
        assert data["current"]["umbral_anios"] == 12.0
        assert data["current"]["provenance"] == "canon_sdv_h"
        assert data["history"] == []
        assert len(data["pending_proposals"]) == 1
        assert data["audit_hash"]


class TestEjecucionVinculante:
    def _aprobar(self, client, auth, pid, voters=(1, 2, 3)):
        for uid in voters:
            client.post(
                f"/voting/proposals/{pid}/vote",
                json={"option": "Aprobar"},
                headers=auth(uid),
            )

    def test_flujo_completo_aprobado_aplica_umbral(self, client, auth):
        pid = _propose(client, auth, umbral_anios=14).get_json()["proposal"]["id"]
        self._aprobar(client, auth, pid)
        resp = client.post(
            f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True)
        )
        assert resp.get_json()["proposal"]["result"] == "passed"
        with client.application.app_context():
            db = get_db()
            row = db.execute(
                "SELECT umbral_anios FROM edu_parameters ORDER BY id DESC LIMIT 1"
            ).fetchone()
            assert row["umbral_anios"] == 14.0
        data = client.get("/voting/parliament/educativo").get_json()
        assert data["current"]["umbral_anios"] == 14.0
        assert data["current"]["provenance"] == "comunidad"
        assert data["history"][0]["proposal_id"] == pid
        assert data["history"][0]["umbral_anios"] == 14.0

    def test_umbral_rechazado_no_aplica(self, client, auth):
        pid = _propose(client, auth, umbral_anios=16).get_json()["proposal"]["id"]
        client.post(
            f"/voting/proposals/{pid}/vote",
            json={"option": "Aprobar"},
            headers=auth(1),
        )
        client.post(
            f"/voting/proposals/{pid}/vote",
            json={"option": "Aprobar"},
            headers=auth(2),
        )
        client.post(
            f"/voting/proposals/{pid}/vote",
            json={"option": "Mantener"},
            headers=auth(3),
        )
        resp = client.post(
            f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True)
        )
        assert resp.get_json()["proposal"]["result"] == "rejected"
        data = client.get("/voting/parliament/educativo").get_json()
        assert data["current"]["umbral_anios"] == 12.0
        assert data["current"]["provenance"] == "canon_sdv_h"
        assert data["history"] == []

    def test_cooldown_anti_flip_flop(self, client, auth):
        """Tras una resolución, el umbral no puede saltar de nuevo de inmediato
        (Cap. 14: la palabra y el poder tienen fecha de vencimiento)."""
        pid = _propose(client, auth, umbral_anios=14).get_json()["proposal"]["id"]
        self._aprobar(client, auth, pid)
        client.post(
            f"/voting/proposals/{pid}/close", json={}, headers=auth(1, admin=True)
        )
        resp = _propose(client, auth, umbral_anios=18)
        assert resp.status_code == 409
        assert resp.get_json()["code"] == "EDU_COOLDOWN"


class TestAnalizadorConUmbral:
    def _participante(self, client, auth, anos, email="edu@test.com"):
        with client.application.app_context():
            db = get_db()
            cur = db.execute(
                """
                INSERT INTO participants
                    (name, email, city, neighborhood, offer_description,
                     need_description, need_urgency, need_human_dimensions,
                     educacion_anos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "Estudiante",
                    email,
                    "Bogota",
                    "Centro",
                    "ensenar matematicas",
                    "crecer",
                    "Baja",
                    "[]",
                    anos,
                ),
            )
            db.commit()
            return cur.lastrowid

    def test_sin_resoluciones_usa_canon_12(self, client, auth):
        pid = self._participante(client, auth, 12)
        with client.application.app_context():
            db = get_db()
            score = SDVAnalyzer(db).estimate_participant_sdv(pid)
            assert score.educacion == educacion_indice(12) == 1.0

    def test_con_resolucion_usa_umbral_comunitario(self, client, auth):
        pid = self._participante(client, auth, 12, email="edu2@test.com")
        with client.application.app_context():
            db = get_db()
            db.execute(
                """
                INSERT INTO edu_parameters (umbral_anios, updated_by, notes)
                VALUES (14.0, 1, 'decisión comunitaria de prueba, T13')
                """
            )
            db.commit()
            score = SDVAnalyzer(db).estimate_participant_sdv(pid)
            # La ley se cumple (12 años) pero la plenitud aspiracional no:
            # 0.1 + 0.9 * (12/14) = 0.871 → 0.87 tras el redondeo del analyzer
            # (entropía δ — la base no se gradúa).
            assert score.educacion == 0.87
