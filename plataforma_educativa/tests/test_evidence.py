# -*- coding: utf-8 -*-
"""Test 13: vacuación sin muros (M13) — material de enseñanza propio.

La regla de oro no espera alumnos: tema aprobado + material (texto/audio/video/
imagen) = 'listo para enseñar'; con la primera ronda de mentoría se cierra la
maestría. Además: el test exige prerrequisitos (A4 de la auditoría de la plataforma).
"""

import uuid

from app.db import get_db


def _register(client, username):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    return client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    ).get_json()["token"]


def _make_topic(app, with_prereq=False):
    with app.app_context():
        db = get_db()
        branch_id = db.execute("SELECT id FROM branches ORDER BY id LIMIT 1").fetchone()["id"]
        prereq = '["otra_inexistente"]' if with_prereq else "[]"
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, 'Tema', 'descripción', 996, ?, 1)",
            (branch_id, "evi_" + uuid.uuid4().hex[:8], prereq),
        )
        topic_id = cur.lastrowid
        for i in range(3):
            db.execute(
                "INSERT INTO questions (topic_id, pregunta, opciones, correcta, explicacion) "
                "VALUES (?, ?, ?, ?, ?)",
                (topic_id, f"¿Pregunta {i}?", '["a", "b", "c", "d"]', 0, "explicación"),
            )
        db.commit()
        return topic_id


def _pass_test(client, token, topic_id):
    return client.post(
        f"/api/topics/{topic_id}/test",
        headers={"X-Auth-Token": token},
        json={"answers": [0, 0, 0]},
    )


def test_evidence_requires_passed(client, app):
    """Sin aprobar el tema no se aporta material (la obra sale de lo que sabes)."""
    token = _register(client, "novata")
    topic_id = _make_topic(app)
    resp = client.post(
        f"/api/topics/{topic_id}/evidence",
        headers={"X-Auth-Token": token},
        json={"tipo": "texto", "titulo": "Guía", "texto": "contenido"},
    )
    assert resp.status_code == 400


def test_evidence_ok_and_ready_to_teach(client, app):
    """Aprobado + material = 'listo para enseñar' (la cola de tutores)."""
    token = _register(client, "maestra")
    topic_id = _make_topic(app)
    assert _pass_test(client, token, topic_id).status_code == 200

    resp = client.post(
        f"/api/topics/{topic_id}/evidence",
        headers={"X-Auth-Token": token},
        json={"tipo": "texto", "titulo": "Guía de fracciones", "texto": "Piensa en una pizza..."},
    )
    assert resp.status_code == 201

    tree = client.get("/api/tree", headers={"X-Auth-Token": token}).get_json()
    topic = next(t for b in tree["branches"] for t in b["topics"] if t["id"] == topic_id)
    assert topic["ready_to_teach"] is True
    assert topic["evidence"]["tipo"] == "texto"
    assert topic["estado"] == "test_passed"


def test_evidence_video_needs_url(client, app):
    token = _register(client, "videota")
    topic_id = _make_topic(app)
    _pass_test(client, token, topic_id)
    # Sin URL -> 400.
    resp = client.post(
        f"/api/topics/{topic_id}/evidence",
        headers={"X-Auth-Token": token},
        json={"tipo": "video", "titulo": "Demo"},
    )
    assert resp.status_code == 400
    # Con URL -> 201.
    resp = client.post(
        f"/api/topics/{topic_id}/evidence",
        headers={"X-Auth-Token": token},
        json={"tipo": "video", "titulo": "Demo", "url": "https://ejemplo.org/demo.mp4"},
    )
    assert resp.status_code == 201


def test_regla_de_oro_cierra_la_maestria(client, app):
    """Material + primera ronda de mentoría = mastered (la vacuación completa)."""
    from app.api_routes import _upsert_user_state

    token = _register(client, "oro")
    with app.app_context():
        db = get_db()
        local_id = db.execute("SELECT id FROM users WHERE username = 'oro'").fetchone()["id"]
    topic_id = _make_topic(app)
    _pass_test(client, token, topic_id)
    client.post(
        f"/api/topics/{topic_id}/evidence",
        headers={"X-Auth-Token": token},
        json={"tipo": "texto", "titulo": "Guía", "texto": "contenido"},
    )

    # El incremento de mentor_rounds al ser asignado como monitor:
    with app.app_context():
        _upsert_user_state(local_id, topic_id, mentor_rounds=1)

    tree = client.get("/api/tree", headers={"X-Auth-Token": token}).get_json()
    topic = next(t for b in tree["branches"] for t in b["topics"] if t["id"] == topic_id)
    assert topic["estado"] == "mastered"
    assert topic["ready_to_teach"] is False


def test_test_exige_prerrequisitos(client, app):
    """A4: el test en un tema bloqueado devuelve 403 (no se salta el árbol)."""
    token = _register(client, "saltarina")
    topic_id = _make_topic(app, with_prereq=True)
    resp = _pass_test(client, token, topic_id)
    assert resp.status_code == 403
    assert "árbol" in resp.get_json()["error"]
