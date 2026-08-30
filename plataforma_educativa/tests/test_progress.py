# -*- coding: utf-8 -*-
"""Test 4: progreso — prerequisitos y umbral del test (70%)."""

import uuid

from app.db import get_db


def _token(client, username="estudiante"):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    resp = client.post("/api/auth/login", json={"username": username, "password": "secreto"})
    return resp.get_json()["token"]


def _headers(token):
    return {"X-Auth-Token": token}


def _make_topic(app, n_questions):
    """Inserta un tema sin prerrequisitos con ``n_questions`` preguntas (correcta=0)."""
    with app.app_context():
        db = get_db()
        branch_id = db.execute(
            "SELECT id FROM branches ORDER BY id LIMIT 1"
        ).fetchone()["id"]
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, 'Tema de prueba', 'descripción', 999, '[]', 1)",
            (branch_id, "test_topic_" + uuid.uuid4().hex[:8]),
        )
        topic_id = cur.lastrowid
        for i in range(n_questions):
            db.execute(
                "INSERT INTO questions (topic_id, pregunta, opciones, correcta, explicacion) "
                "VALUES (?, ?, ?, ?, ?)",
                (topic_id, f"¿Pregunta {i}?", '["a", "b", "c", "d"]', 0, "explicación"),
            )
        db.commit()
        return topic_id


def _branch_id_of_first_branch(app):
    with app.app_context():
        return get_db().execute("SELECT id FROM branches ORDER BY id LIMIT 1").fetchone()["id"]


def _first_topic_with_prereq(client, token):
    """Encuentra un tema del árbol que tenga prerrequisitos."""
    branches = client.get("/api/tree", headers=_headers(token)).get_json()["branches"]
    for branch in branches:
        for topic in branch["topics"]:
            if topic["prereq_ids"]:
                return topic
    return None


def test_start_with_prereq_not_approved_returns_403(client):
    """Empezar un tema con prerrequisito no aprobado -> 403."""
    token = _token(client)
    topic = _first_topic_with_prereq(client, token)
    assert topic is not None, "El seed debe tener al menos un tema con prerrequisitos."

    resp = client.post(
        f"/api/topics/{topic['id']}/start", headers=_headers(token), json={}
    )
    assert resp.status_code == 403


def test_start_marks_learning(client):
    """Empezar un tema sin prerrequisitos marca el estado 'learning'."""
    token = _token(client)
    branches = client.get("/api/tree", headers=_headers(token)).get_json()["branches"]
    topic = next(t for t in branches[0]["topics"] if not t["prereq_ids"])

    resp = client.post(
        f"/api/topics/{topic['id']}/start", headers=_headers(token), json={}
    )
    assert resp.status_code == 200
    assert resp.get_json()["estado"]["estado"] == "learning"


def test_test_with_70_percent_becomes_test_passed(client, app):
    """Aprobando >=70% el tema pasa a 'test_passed'."""
    token = _token(client)
    topic_id = _make_topic(app, 10)

    client.post(f"/api/topics/{topic_id}/start", headers=_headers(token), json={})
    # 7 de 10 correctas => 70% exacto.
    answers = [0] * 7 + [1] * 3
    resp = client.post(
        f"/api/topics/{topic_id}/test", headers=_headers(token), json={"answers": answers}
    )
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["passed"] is True
    assert body["estado"]["estado"] == "test_passed"


def test_test_below_70_not_passed(client, app):
    """Por debajo del 70% el tema NO queda aprobado."""
    token = _token(client)
    topic_id = _make_topic(app, 10)

    client.post(f"/api/topics/{topic_id}/start", headers=_headers(token), json={})
    # 6 de 10 correctas => 60% (< 70).
    answers = [0] * 6 + [1] * 4
    resp = client.post(
        f"/api/topics/{topic_id}/test", headers=_headers(token), json={"answers": answers}
    )
    body = resp.get_json()
    assert body["passed"] is False
    assert body["estado"]["estado"] != "test_passed"


def test_mastered_requires_mentor_rounds(client, app):
    """Dominar (mastered) exige aprobar el test, material propio (M13) Y haber
    mentoreado >=1 reunión — la regla de oro: la maestría se gana enseñando."""
    token = _token(client)
    topic_id = _make_topic(app, 4)

    client.post(f"/api/topics/{topic_id}/start", headers=_headers(token), json={})
    answers = [0] * 4  # 100%.
    resp = client.post(
        f"/api/topics/{topic_id}/test", headers=_headers(token), json={"answers": answers}
    )
    # Sin mentor_rounds -> solo test_passed.
    assert resp.get_json()["estado"]["estado"] == "test_passed"

    # Ahora simulamos que el usuario ya ha mentoreado una reunión.
    with app.app_context():
        db = get_db()
        user_id = db.execute("SELECT id FROM users WHERE username = 'estudiante'").fetchone()["id"]
        db.execute(
            "UPDATE user_topics SET mentor_rounds = 1 WHERE user_id = ? AND topic_id = ?",
            (user_id, topic_id),
        )
        db.commit()

    # Mentoría SIN material todavía: la maestría espera la obra (M13).
    resp2 = client.post(
        f"/api/topics/{topic_id}/test", headers=_headers(token), json={"answers": answers}
    )
    assert resp2.get_json()["estado"]["estado"] == "test_passed"

    # Con material propio la vacuación se cierra.
    ev = client.post(
        f"/api/topics/{topic_id}/evidence",
        headers=_headers(token),
        json={"tipo": "texto", "titulo": "Mi guía", "texto": "contenido"},
    )
    assert ev.status_code == 201
    resp3 = client.post(
        f"/api/topics/{topic_id}/test", headers=_headers(token), json={"answers": answers}
    )
    assert resp3.get_json()["estado"]["estado"] == "mastered"
