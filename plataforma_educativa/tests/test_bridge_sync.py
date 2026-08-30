# -*- coding: utf-8 -*-
"""Test 12: sincronización automática del OEV → puente (M12).

Al alcanzar ``mastered`` (test ≥70% + mentor_rounds ≥ 1), el nodo reporta al
puente de :5001 con su token de servicio, en best-effort: sin configuración o
sin identidad federada, el nodo sigue siendo autónomo y no se rompe.
"""

import json
import uuid
from unittest import mock

from app.db import get_db


def _register_user(client, username):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    return client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    ).get_json()["token"]


def _federate(client, username, maxo_user_id):
    """Convierte al usuario local en federado (vínculo JIT, M12)."""
    with client.application.app_context():
        db = get_db()
        db.execute(
            "UPDATE users SET maxo_user_id = ? WHERE username = ?",
            (maxo_user_id, username),
        )
        db.commit()


def _make_topic(app):
    with app.app_context():
        db = get_db()
        branch_id = db.execute("SELECT id FROM branches ORDER BY id LIMIT 1").fetchone()["id"]
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, 'Tema de sincronía', 'descripción', 997, '[]', 1)",
            (branch_id, "sync_" + uuid.uuid4().hex[:8]),
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


def _seed_test_passed_with_mentor(app, user_id, topic_id):
    """Deja el tema en 'test_passed' con mentoría ya hecha: el próximo test
    aprovado lo lleva a 'mastered' (la transición que dispara el reporte)."""
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO user_topics (user_id, topic_id, estado, score, updated_at, mentor_rounds, mentorship_approved) "
            "VALUES (?, ?, 'test_passed', 70.0, datetime('now'), 1, 0)",
            (user_id, topic_id),
        )
        db.commit()


def test_sin_configuracion_no_reporte(client, app, monkeypatch):
    """Nodo autónomo: sin URL/token de puente, mastery no rompe ni llama."""
    monkeypatch.delenv("EDU_BRIDGE_URL", raising=False)
    monkeypatch.delenv("EDU_BRIDGE_SERVICE_TOKEN", raising=False)
    token = _register_user(client, "autonoma")
    topic_id = _make_topic(app)
    with mock.patch("app.api_routes.urllib.request.urlopen") as urlopen:
        resp = client.post(
            f"/api/topics/{topic_id}/test",
            headers={"X-Auth-Token": token},
            json={"answers": [0, 0, 0]},
        )
        assert resp.status_code == 200
        # Sin mentoría: queda test_passed, nada que sincronizar.
        urlopen.assert_not_called()


def test_mastered_reporta_al_puente(client, app, monkeypatch):
    """Al vacuar (mastered) con identidad federada, el nodo reporta al puente
    con su token de servicio y el user_id MAXO, sin JWT humano."""
    token = _register_user(client, "viajera")
    with client.application.app_context():
        db = get_db()
        local_id = db.execute(
            "SELECT id FROM users WHERE username = 'viajera'"
        ).fetchone()["id"]
    _federate(client, "viajera", 4242)
    topic_id = _make_topic(app)
    _seed_test_passed_with_mentor(app, local_id, topic_id)

    monkeypatch.setenv("EDU_BRIDGE_URL", "http://maxo.test:5001")
    monkeypatch.setenv("EDU_BRIDGE_SERVICE_TOKEN", "secreto-del-nodo")

    # La regla de oro (M13): material propio + mentoría previa cierra la
    # maestría AQUÍ (la transición dispara el reporte al puente).
    with mock.patch("app.api_routes.urllib.request.urlopen") as urlopen:
        ev = client.post(
            f"/api/topics/{topic_id}/evidence",
            headers={"X-Auth-Token": token},
            json={"tipo": "texto", "titulo": "Guía", "texto": "contenido"},
        )
        assert ev.status_code == 201
        assert urlopen.called, "el nodo debe reportar la maestría al puente"
        request = urlopen.call_args[0][0]
        assert "edu-bridge/sync-mastery" in request.full_url
        sent_headers = {k.lower(): v for k, v in getattr(request, "headers", {}).items()}
        assert sent_headers.get("x-edu-bridge-token") == "secreto-del-nodo"
        payload = json.loads(request.data.decode("utf-8"))
        assert payload["user_id"] == 4242
        assert payload["triada_approved"] is True
        assert payload["mentor_rounds"] == 1
        assert payload["topic_slug"].startswith("sync_")
        assert payload["branch_slug"]

    with mock.patch("app.api_routes.urllib.request.urlopen") as urlopen:
        resp = client.post(
            f"/api/topics/{topic_id}/test",
            headers={"X-Auth-Token": token},
            json={"answers": [0, 0, 0]},
        )
        assert resp.status_code == 200
        urlopen.assert_not_called()  # ya estaba mastered: no hay re-reporte


def test_puente_caido_no_rompe_el_nodo(client, app, monkeypatch):
    """Best-effort: si el puente falla, la vida del nodo sigue."""
    token = _register_user(client, "resiliente")
    with client.application.app_context():
        db = get_db()
        local_id = db.execute(
            "SELECT id FROM users WHERE username = 'resiliente'"
        ).fetchone()["id"]
    _federate(client, "resiliente", 777)
    topic_id = _make_topic(app)
    _seed_test_passed_with_mentor(app, local_id, topic_id)

    monkeypatch.setenv("EDU_BRIDGE_URL", "http://maxo.test:5001")
    monkeypatch.setenv("EDU_BRIDGE_SERVICE_TOKEN", "secreto-del-nodo")

    # Regla de oro (M13): material + mentoría previa -> mastery al subir la obra.
    def _boom(*args, **kwargs):
        raise IOError("puente caído")

    with mock.patch(
        "app.api_routes.urllib.request.urlopen", side_effect=_boom
    ) as urlopen:
        ev = client.post(
            f"/api/topics/{topic_id}/evidence",
            headers={"X-Auth-Token": token},
            json={"tipo": "texto", "titulo": "Guía", "texto": "contenido"},
        )
        assert ev.status_code == 201  # el nodo sigue vivo con el puente caído
        assert urlopen.called
        resp = client.post(
            f"/api/topics/{topic_id}/test",
            headers={"X-Auth-Token": token},
            json={"answers": [0, 0, 0]},
        )
        assert resp.status_code == 200
        assert urlopen.called


def test_sin_identidad_federada_no_reporte(client, app, monkeypatch):
    """Usuario local sin maxo_user_id: no hay a quién informar, no llama."""
    monkeypatch.setenv("EDU_BRIDGE_URL", "http://maxo.test:5001")
    monkeypatch.setenv("EDU_BRIDGE_SERVICE_TOKEN", "secreto-del-nodo")
    token = _register_user(client, "localita")
    topic_id = _make_topic(app)
    with client.application.app_context():
        db = get_db()
        local_id = db.execute(
            "SELECT id FROM users WHERE username = 'localita'"
        ).fetchone()["id"]
    _seed_test_passed_with_mentor(app, local_id, topic_id)

    with mock.patch("app.api_routes.urllib.request.urlopen") as urlopen:
        resp = client.post(
            f"/api/topics/{topic_id}/test",
            headers={"X-Auth-Token": token},
            json={"answers": [0, 0, 0]},
        )
        assert resp.status_code == 200
        urlopen.assert_not_called()
