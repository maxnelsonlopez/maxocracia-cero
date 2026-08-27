# -*- coding: utf-8 -*-
"""Test 6: generar semana, inscribirse y la regla de reunión llena (409)."""

from app.db import get_db

WEEK = "2030-W01"


def _register(client, username):
    return client.post("/api/auth/register", json={"username": username, "password": "secreto"})


def _login(client, username):
    resp = client.post("/api/auth/login", json={"username": username, "password": "secreto"})
    return resp.get_json()["token"]


def _headers(token):
    return {"X-Auth-Token": token}


def _start_first_topic(client, token):
    """El primer tema sin prerequisitos del árbol (el 'conteo' de Matemáticas)."""
    branches = client.get("/api/tree", headers=_headers(token)).get_json()["branches"]
    topic = next(t for t in branches[0]["topics"] if not t["prereq_ids"])
    client.post(f"/api/topics/{topic['id']}/start", headers=_headers(token), json={})
    return topic["id"]


def _set_availability(client, token):
    client.post(
        "/api/availability",
        headers=_headers(token),
        json={"week": WEEK, "slots": ["LUN 19:00"]},
    )


def _correct_answers(app, topic_id):
    with app.app_context():
        db = get_db()
        return [r["correcta"] for r in db.execute(
            "SELECT correcta FROM questions WHERE topic_id = ? ORDER BY id", (topic_id,)
        ).fetchall()]


def test_generate_requires_coordinator(client):
    """Solo el coordinador puede generar la semana."""
    _register(client, "coord")  # Primer usuario -> coordinador.
    _register(client, "normal")
    normal_token = _login(client, "normal")

    resp = client.post(
        f"/api/meetings/generate?week={WEEK}", headers=_headers(normal_token), json={}
    )
    assert resp.status_code == 403


def test_generate_creates_meetings_and_full_rejects_extra(client, app):
    """Generar semana + inscribirse hasta llenar (8) + un extra -> 409."""
    _register(client, "coord")
    coord_token = _login(client, "coord")

    # Tres estudiantes que empiezan el mismo tema y dan disponibilidad.
    for name in ("s1", "s2", "s3"):
        _register(client, name)
        token = _login(client, name)
        _start_first_topic(client, token)
        _set_availability(client, token)

    resp = client.post(
        f"/api/meetings/generate?week={WEEK}", headers=_headers(coord_token), json={}
    )
    assert resp.status_code == 201
    meetings = resp.get_json()["meetings"]
    assert len(meetings) == 1
    meeting = meetings[0]
    assert len(meeting["participants"]) == 3
    assert meeting["monitor_id"] is None  # Nadie está calificado para monitorear.

    meeting_id = meeting["id"]

    # Cinco estudiantes más se inscriben de a uno hasta llegar a 8.
    for name in ("s4", "s5", "s6", "s7", "s8"):
        _register(client, name)
        token = _login(client, name)
        resp_join = client.post(
            f"/api/meetings/{meeting_id}/join", headers=_headers(token), json={}
        )
        assert resp_join.status_code == 200, resp_join.get_data(as_text=True)

    listing = client.get(f"/api/meetings?week={WEEK}", headers=_headers(coord_token)).get_json()
    full_meeting = next(m for m in listing["meetings"] if m["id"] == meeting_id)
    assert full_meeting["participants_count"] == 8
    assert full_meeting["estado"] == "full"

    # El noveno intento debe fallar con 409.
    _register(client, "s9")
    token9 = _login(client, "s9")
    resp_409 = client.post(
        f"/api/meetings/{meeting_id}/join", headers=_headers(token9), json={}
    )
    assert resp_409.status_code == 409


def test_generate_assigns_monitor_if_qualified(client, app):
    """Si hay un usuario calificado (mastered + mentor_rounds>=1) se le asigna de monitor."""
    _register(client, "coord")
    coord_token = _login(client, "coord")

    # Mentor: aprueba el tema, acumula una ronda de mentoría y da disponibilidad.
    _register(client, "mentor")
    mentor_token = _login(client, "mentor")
    topic_id = _start_first_topic(client, mentor_token)
    answers = _correct_answers(app, topic_id)
    client.post(
        f"/api/topics/{topic_id}/test", headers=_headers(mentor_token), json={"answers": answers}
    )
    _set_availability(client, mentor_token)
    with app.app_context():
        db = get_db()
        mentor_id = db.execute("SELECT id FROM users WHERE username = 'mentor'").fetchone()["id"]
        # La vacuación: el skill se gana enseñando → mastered + mentor_rounds>=1.
        db.execute(
            "UPDATE user_topics SET estado = 'mastered', mentor_rounds = 1 "
            "WHERE user_id = ? AND topic_id = ?",
            (mentor_id, topic_id),
        )
        db.commit()

    # Un estudiante para que exista al menos una reunión.
    _register(client, "st")
    st_token = _login(client, "st")
    _start_first_topic(client, st_token)
    _set_availability(client, st_token)

    resp = client.post(
        f"/api/meetings/generate?week={WEEK}", headers=_headers(coord_token), json={}
    )
    assert resp.status_code == 201
    meeting = resp.get_json()["meetings"][0]
    assert meeting["monitor_id"] == mentor_id, "Debe asignarse al monitor calificado."


def test_join_nonexistent_meeting_returns_404(client):
    _register(client, "coord")
    _register(client, "st")
    token = _login(client, "st")
    resp = client.post("/api/meetings/99999/join", headers=_headers(token), json={})
    assert resp.status_code == 404


def test_attend_requires_monitor_or_coordinator(client):
    _register(client, "coord")
    coord_token = _login(client, "coord")
    _register(client, "st")
    st_token = _login(client, "st")

    # Un estudiante que no es monitor ni coordinador no puede marcar asistencias
    # aunque la reunión exista; usamos una reunión creada manualmente.
    with client.application.app_context():
        db = get_db()
        topic_id = db.execute("SELECT id FROM topics ORDER BY id LIMIT 1").fetchone()["id"]
        cur = db.execute(
            "INSERT INTO meetings (fecha, hora_inicio, duracion_min, topic_id, monitor_id, "
            "estado, week, created_at) VALUES ('2030-01-01', '19:00', 120, ?, NULL, 'open', ?, 't')",
            (topic_id, WEEK),
        )
        meeting_id = cur.lastrowid
        db.commit()

    resp = client.post(
        f"/api/meetings/{meeting_id}/attend", headers=_headers(st_token), json={"asistio": True}
    )
    assert resp.status_code == 403
    # El coordinador sí puede.
    resp_ok = client.post(
        f"/api/meetings/{meeting_id}/attend", headers=_headers(coord_token), json={"asistio": True}
    )
    assert resp_ok.status_code == 200
