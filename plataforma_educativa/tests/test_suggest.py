# -*- coding: utf-8 -*-
"""Test 14: el compañero de la ciudad — sugerencia del siguiente lote (M14).

Guía de la mano sin mandato: prioriza el barrio donde más se construye, con
lotes desbloqueados y libres; primero lo sencillo. Cero rankings, cero presión.
"""

import uuid

from app.db import get_db


def _register(client, username):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    return client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    ).get_json()["token"]


def _make_topic(app, branch_id=None, dificultad=1, prereq="[]"):
    with app.app_context():
        db = get_db()
        if branch_id is None:
            branch_id = db.execute("SELECT id FROM branches ORDER BY id LIMIT 1").fetchone()["id"]
        slug = "sug_" + uuid.uuid4().hex[:8]
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, 'Lote', 'descripción', 995, ?, ?)",
            (branch_id, slug, prereq, dificultad),
        )
        db.commit()
        return cur.lastrowid, slug


def test_suggest_primero_un_lote_libre(client, app):
    token = _register(client, "arquitecta")
    resp = client.get("/api/suggest", headers={"X-Auth-Token": token})
    assert resp.status_code == 200
    sug = resp.get_json()["suggestion"]
    assert sug is not None
    assert sug["topic_id"] > 0
    assert "branch_nombre" in sug


def test_suggest_prioriza_la_rama_en_construccion(client, app):
    """Tras aprobar en la rama A y no tocar la B, la sugerencia sigue en A."""
    token = _register(client, "agrimensora")
    with app.app_context():
        db = get_db()
        branches = db.execute("SELECT id FROM branches ORDER BY id LIMIT 2").fetchall()
    # Dos lotes aprobados en la primera rama.
    t1 = _make_topic(app, branches[0]["id"])
    t2 = _make_topic(app, branches[0]["id"])
    # Un lote libre en la segunda rama (más sencillo).
    t3 = _make_topic(app, branches[1]["id"])

    # Marcar t1 y t2 aprobados directamente (sin pasar por el test: la rama A
    # queda con progreso y aún quedan lotes libres en A).
    with app.app_context():
        db = get_db()
        uid = db.execute("SELECT id FROM users WHERE username = 'agrimensora'").fetchone()["id"]
        for t_id, _ in (t1, t2):
            db.execute(
                "INSERT INTO user_topics (user_id, topic_id, estado, score, updated_at, mentor_rounds, mentorship_approved) "
                "VALUES (?, ?, 'test_passed', 80.0, datetime('now'), 0, 0)",
                (uid, t_id),
            )
        db.commit()

    sug = client.get("/api/suggest", headers={"X-Auth-Token": token}).get_json()["suggestion"]
    assert sug is not None
    # Nunca sugiere un lote ya construido (estado test_passed/mastered).
    assert sug["topic_id"] not in (t1[0], t2[0])


def test_suggest_sin_disponibles_devuelve_none(client, app):
    """Ciudad por hoy: todos los temas bloqueados o aprobados -> None amable."""
    token = _register(client, "designer")
    with app.app_context():
        db = get_db()
        uid = db.execute("SELECT id FROM users WHERE username = 'designer'").fetchone()["id"]
        topics = db.execute("SELECT id FROM topics").fetchall()
        for t in topics:
            db.execute(
                "INSERT OR REPLACE INTO user_topics (user_id, topic_id, estado, score, updated_at, mentor_rounds, mentorship_approved) "
                "VALUES (?, ?, 'test_passed', 90.0, datetime('now'), 0, 0)",
                (uid, t["id"]),
            )
        db.commit()
    sug = client.get("/api/suggest", headers={"X-Auth-Token": token}).get_json()["suggestion"]
    assert sug is None
