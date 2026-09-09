# -*- coding: utf-8 -*-
"""Rondas de mantenimiento (anti-δ) — teoría OEV §1.1: la base nunca se gradúa.

Misión del Concilio primigenio (3ª elegida del ciclo-20260909-024012):
los lotes dominados que pasan N semanas sin tocar requieren Ronda; repasar
devuelve el brillo. Cuidado, no sanción: el que más Ronda necesita, más
acompañado va.
"""

import uuid
from datetime import datetime, timedelta, timezone

from app.db import get_db


def _token(client, username="estudiante_r"):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    resp = client.post("/api/auth/login", json={"username": username, "password": "secreto"})
    return resp.get_json()["token"]


def _headers(token):
    return {"X-Auth-Token": token}


def _user_id(app, username):
    with app.app_context():
        return get_db().execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()["id"]


def _make_topic(app):
    with app.app_context():
        db = get_db()
        branch_id = db.execute(
            "SELECT id FROM branches ORDER BY id LIMIT 1"
        ).fetchone()["id"]
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, "
            "prereq_ids, dificultad) VALUES (?, ?, 'Lote de Ronda', "
            "'descripción', 997, '[]', 1)",
            (branch_id, "round_" + uuid.uuid4().hex[:8]),
        )
        topic_id = cur.lastrowid
        for i in range(2):
            db.execute(
                "INSERT INTO questions (topic_id, pregunta, opciones, correcta, "
                "explicacion) VALUES (?, ?, ?, ?, ?)",
                (topic_id, f"¿Pregunta {i}?", '["a", "b", "c", "d"]', 0, "explicación"),
            )
        db.commit()
        return topic_id


def _seed_dominio(app, user_id, topic_id, updated_at):
    """Siembra un lote dominado (mastered) con la fecha de último toque."""
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO user_topics (user_id, topic_id, estado, score, updated_at, "
            "mentor_rounds, mentorship_approved, evidence, rounds, last_round_at) "
            "VALUES (?, ?, 'mastered', 90, ?, 1, 1, 'material', 0, NULL)",
            (user_id, topic_id, updated_at),
        )
        db.commit()


def test_rounds_requiere_ronda_tras_semanas(app, client):
    """Un lote dominado sin tocar hace >4 semanas: requiere Ronda."""
    token = _token(client)
    uid = _user_id(app, "estudiante_r")
    topic_id = _make_topic(app)
    viejo = (datetime.now(timezone.utc) - timedelta(weeks=6)).isoformat()
    _seed_dominio(app, uid, topic_id, viejo)

    data = client.get("/api/me/rounds", headers=_headers(token)).get_json()
    assert data["pending"] == 1
    lot = next(l for l in data["lots"] if l["topic_id"] == topic_id)
    assert lot["needs_round"] is True
    assert lot["estado"] == "mastered"
    assert lot["rounds"] == 0


def test_rounds_lote_fresco_no_molesta(app, client):
    """Un lote dominado reciente: brillo intacto, sin Ronda pendiente."""
    token = _token(client)
    uid = _user_id(app, "estudiante_r")
    topic_id = _make_topic(app)
    fresco = datetime.now(timezone.utc).isoformat()
    _seed_dominio(app, uid, topic_id, fresco)

    data = client.get("/api/me/rounds", headers=_headers(token)).get_json()
    assert data["pending"] == 0
    assert next(l for l in data["lots"] if l["topic_id"] == topic_id)["needs_round"] is False


def test_round_devuelve_brillo(app, client):
    """Repasar: rounds += 1, last_round_at reciente y la Ronda se apaga."""
    token = _token(client)
    uid = _user_id(app, "estudiante_r")
    topic_id = _make_topic(app)
    viejo = (datetime.now(timezone.utc) - timedelta(weeks=6)).isoformat()
    _seed_dominio(app, uid, topic_id, viejo)

    resp = client.post(
        f"/api/topics/{topic_id}/round", headers=_headers(token)
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["rounds"] == 1
    assert body["needs_round"] is False

    data = client.get("/api/me/rounds", headers=_headers(token)).get_json()
    assert data["pending"] == 0
    lot = next(l for l in data["lots"] if l["topic_id"] == topic_id)
    assert lot["rounds"] == 1
    assert lot["last_round_at"] is not None


def test_round_lote_no_dominado(app, client):
    """La Ronda cuida lo aprendido: un lote pendiente no recibe Ronda."""
    token = _token(client)
    topic_id = _make_topic(app)
    resp = client.post(f"/api/topics/{topic_id}/round", headers=_headers(token))
    assert resp.status_code == 400
    assert "no está dominado" in resp.get_json()["error"]


def test_rounds_sin_lotes(app, client):
    token = _token(client, username="nadie_r")
    data = client.get("/api/me/rounds", headers=_headers(token)).get_json()
    assert data == {"lots": [], "pending": 0}


def test_rounds_requiere_token(client):
    assert client.get("/api/me/rounds").status_code == 401
    assert client.post("/api/topics/1/round").status_code == 401
