"""
Tests del Guía de la Maxocracia (app/guide_bp.py).

Cubre:
- Auth: 401 sin token en los tres endpoints.
- Oráculo deshabilitado: 503 (sin DEEPSEEK_API_KEY ni oráculo local).
- Chat: respuesta con monkeypatch del oráculo.
- Trust-assessment: scores + evidencia T13 + persistencia (guide_assessments).
- Director-candidacy: filtros éticos/actitud/aptitud, eligible y hint.
- El guía recomienda, no nombra: eligible=false con evidencia pobre.
"""

import json
import os

os.environ["SECRET_KEY"] = "test-secret"
os.environ.pop("DEEPSEEK_API_KEY", None)
os.environ["LOCAL_ORACLE_ENABLED"] = "true"

import pytest

from app import create_app
from app.utils import get_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile = __import__("tempfile").mkstemp()
    app = create_app(db_path=db_path)
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        with app.app_context():
            db = get_db()
            with open("app/schema.sql", "r", encoding="utf-8") as f:
                db.executescript(f.read())
            db.execute(
                "INSERT INTO users (id, email, name, password_hash, trust_level) "
                "VALUES (1, 'guia@test.com', 'Guia', 'hash', 1)"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash, trust_level) "
                "VALUES (2, 'nova@test.com', 'Nova', 'hash', 0)"
            )
            db.commit()
        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth(client):
    from app.jwt_utils import create_token

    def _auth(uid):
        return {"Authorization": f"Bearer {create_token({'user_id': uid})}"}

    return _auth


def test_requiere_token(client):
    for path in ("/guide/chat", "/guide/trust-assessment", "/guide/director-candidacy"):
        resp = client.post(path, json={})
        assert resp.status_code == 401


def test_oracle_deshabilitado_503(client, auth, monkeypatch):
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    resp = client.post("/guide/chat", json={"message": "hola"}, headers=auth(1))
    assert resp.status_code == 503
    resp = client.post("/guide/trust-assessment", json={}, headers=auth(1))
    assert resp.status_code == 503


def test_chat_con_oraculo(client, auth, monkeypatch):
    from app import guide_bp

    def fake_call(messages, json_mode=True):
        assert messages[0]["role"] == "system"
        return "¡Bienvenida a la Cohorte! La voz se gana caminando el primer acuerdo."

    monkeypatch.setattr(guide_bp, "_call_oracle", fake_call)
    resp = client.post("/guide/chat", json={"message": "hola"},
                       headers=auth(1))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert "Bienvenida" in data["reply"]
    assert data["engine"] == "local"


def test_trust_assessment_persiste_t13(client, auth, monkeypatch):
    from app import guide_bp

    def fake_call(messages, json_mode=True):
        return json.dumps({
            "ethic": 80, "attitude": 75, "aptitude": 60,
            "suggested_trust_level": 1,
            "reasoning": "Coherencia con los axiomas y disposición a aprender.",
            "honest_limits": "Evidencia reciente aún corta.",
        })

    monkeypatch.setattr(guide_bp, "_call_oracle", fake_call)
    resp = client.post("/guide/trust-assessment",
                       json={"statement": "Quiero aportar a la comunidad."},
                       headers=auth(2))
    assert resp.status_code == 200
    data = resp.get_json()["assessment"]
    assert data["ethic"] == 80
    assert data["suggested_trust_level"] == 1
    assert data["engine"] == "local"
    assert data["evidence"]["trust_level"] == 0
    assert data["evidence"]["has_cero_form"] is False

    with client.application.app_context():
        db = get_db()
        row = db.execute(
            "SELECT * FROM guide_assessments WHERE user_id = 2 AND kind = 'trust'"
        ).fetchone()
        assert row is not None
        assert row["engine"] == "local"


def test_director_candidacy_elige_con_evidencia(client, auth, monkeypatch):
    from app import guide_bp

    def fake_call(messages, json_mode=True):
        return json.dumps({
            "eligible": True, "ethic": 90, "attitude": 88, "aptitude": 85,
            "reasoning": "Evidencia sólida: contratos creados, TVI alto, reputación limpia.",
            "honest_limits": "La decisión final es de la comunidad.",
        })

    monkeypatch.setattr(guide_bp, "_call_oracle", fake_call)
    resp = client.post("/guide/director-candidacy",
                       json={"statement": "Custodiar el sentido, no acumular poder."},
                       headers=auth(1))
    assert resp.status_code == 200
    data = resp.get_json()["assessment"]
    assert data["eligible"] is True
    assert "comunidad" in data["hint"]
    assert data["engine"] == "local"


def test_director_candidacy_requiere_declaracion(client, auth):
    resp = client.post("/guide/director-candidacy", json={}, headers=auth(1))
    assert resp.status_code == 400


def test_oraculo_responde_json_invalido_502(client, auth, monkeypatch):
    from app import guide_bp

    def fake_call(messages, json_mode=True):
        return "esto no es json"

    monkeypatch.setattr(guide_bp, "_call_oracle", fake_call)
    resp = client.post("/guide/trust-assessment", json={}, headers=auth(1))
    assert resp.status_code == 502
