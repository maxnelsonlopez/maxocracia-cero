# -*- coding: utf-8 -*-
"""Test 9: triada de mentoría en la Plataforma Educativa.

La validación se hace en tres capas (Educación Siamesa §2c); la capa de
opinión es la triada: mentor + par + oráculo con veto. Solo el coordinador
puede verificar; el oráculo tiene veto, no voto.
"""


def _register(client, username):
    return client.post(
        "/api/auth/register", json={"username": username, "password": "secreto"}
    )


def _login(client, username):
    resp = client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    )
    return resp.get_json()["token"]


def _headers(token):
    return {"X-Auth-Token": token}


def _first_topic_id(client, token):
    branches = client.get("/api/tree", headers=_headers(token)).get_json()["branches"]
    return next(t for t in branches[0]["topics"] if not t["prereq_ids"])["id"]


def test_verify_requires_coordinator(client):
    _register(client, "coord")  # Primer usuario -> coordinador.
    _register(client, "alumno")
    token = _login(client, "alumno")
    topic_id = _first_topic_id(client, token)

    resp = client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(token),
        json={"user_id": 1, "mentor_ok": True, "peer_ok": True},
    )
    assert resp.status_code == 403


def test_validate_mentor_peer_no_veto(client):
    """Mentor + par aprueban y el oráculo no veta -> validated (tres capas)."""
    _register(client, "coord")
    _register(client, "alumno")
    coord_token = _login(client, "coord")
    alumno_token = _login(client, "alumno")
    topic_id = _first_topic_id(client, alumno_token)
    alumno_id = client.get("/api/me", headers=_headers(alumno_token)).get_json()["user"]["id"]

    resp = client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(coord_token),
        json={"user_id": alumno_id, "mentor_ok": True, "peer_ok": True, "oracle_veto": False},
    )
    assert resp.status_code == 200
    triada = resp.get_json()["triada"]
    assert triada["outcome"] == "validated"
    assert triada["mentor_ok"] is True
    assert triada["peer_ok"] is True
    assert triada["oracle_veto"] is False

    # El árbol expone la triada del aprendiz.
    tree = client.get("/api/tree", headers=_headers(alumno_token)).get_json()["branches"]
    topic = next(t for t in tree[0]["topics"] if t["id"] == topic_id)
    assert topic["triada"]["outcome"] == "validated"


def test_oracle_veto_blocks(client):
    """El oráculo con veto bloquea la validación (no se compensa con avales)."""
    _register(client, "coord")
    _register(client, "alumno")
    coord_token = _login(client, "coord")
    alumno_token = _login(client, "alumno")
    topic_id = _first_topic_id(client, alumno_token)
    alumno_id = client.get("/api/me", headers=_headers(alumno_token)).get_json()["user"]["id"]

    resp = client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(coord_token),
        json={"user_id": alumno_id, "mentor_ok": True, "peer_ok": True, "oracle_veto": True},
    )
    assert resp.get_json()["triada"]["outcome"] == "vetoed"


def test_incomplete_triada_is_pending(client):
    """Falta el par -> pendiente (la triada no se aprueba incompleta)."""
    _register(client, "coord")
    _register(client, "alumno")
    coord_token = _login(client, "coord")
    alumno_token = _login(client, "alumno")
    topic_id = _first_topic_id(client, alumno_token)
    alumno_id = client.get("/api/me", headers=_headers(alumno_token)).get_json()["user"]["id"]

    resp = client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(coord_token),
        json={"user_id": alumno_id, "mentor_ok": True, "peer_ok": False},
    )
    assert resp.get_json()["triada"]["outcome"] == "pending"


def test_verify_requires_user_id(client):
    _register(client, "coord")
    coord_token = _login(client, "coord")
    topic_id = _first_topic_id(client, coord_token)
    resp = client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(coord_token),
        json={"mentor_ok": True, "peer_ok": True},
    )
    assert resp.status_code == 400


def test_tree_exposes_triada_none_until_verified(client):
    _register(client, "coord")
    _register(client, "alumno")
    alumno_token = _login(client, "alumno")
    topic_id = _first_topic_id(client, alumno_token)
    tree = client.get("/api/tree", headers=_headers(alumno_token)).get_json()["branches"]
    topic = next(t for t in tree[0]["topics"] if t["id"] == topic_id)
    assert topic["triada"] is None


def test_verify_upserts_outcome(client):
    """Verificar dos veces: la segunda actualiza (no duplica, UNIQUE)."""
    _register(client, "coord")
    _register(client, "alumno")
    coord_token = _login(client, "coord")
    alumno_token = _login(client, "alumno")
    topic_id = _first_topic_id(client, alumno_token)
    alumno_id = client.get("/api/me", headers=_headers(alumno_token)).get_json()["user"]["id"]

    client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(coord_token),
        json={"user_id": alumno_id, "mentor_ok": True, "peer_ok": False},
    )
    resp = client.post(
        f"/api/topics/{topic_id}/mentorship/verify",
        headers=_headers(coord_token),
        json={"user_id": alumno_id, "mentor_ok": True, "peer_ok": True, "oracle_veto": False},
    )
    triada = resp.get_json()["triada"]
    assert triada["outcome"] == "validated"

    with client.application.app_context():
        from app.db import get_db

        db = get_db()
        count = db.execute(
            "SELECT COUNT(*) AS n FROM mentorship_triadas WHERE user_id = ? AND topic_id = ?",
            (alumno_id, topic_id),
        ).fetchone()["n"]
        assert count == 1
