# -*- coding: utf-8 -*-
"""Test 15: compartir la luz (M15) — espacio compartido voluntario y retractable.

Opt-in explícito (default apagado), retratable al instante, SIN RANKING
(orden alfabético, jamás por puntaje) y sin datos privados en el muro.
"""

import pytest
from app.db import get_db


def _register(client, username):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    return client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    ).get_json()["token"]


def _make_topic(app, slug):
    with app.app_context():
        db = get_db()
        branch_id = db.execute("SELECT id FROM branches ORDER BY id LIMIT 1").fetchone()["id"]
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, 'Tema', 'descripción', 997, '[]', 1)",
            (branch_id, slug),
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


def test_share_is_opt_in_by_default(client):
    """Nadie brilla sin elegirlo: la luz por defecto está apagada."""
    token = _register(client, "apagada")
    me = client.get("/api/me", headers={"X-Auth-Token": token}).get_json()
    assert me["user"]["share_progress"] is False
    lights = client.get(
        "/api/community/lights", headers={"X-Auth-Token": token}
    ).get_json()
    assert lights["total_lights"] == 0


def test_share_on_appears_and_off_vanishes_immediately(client):
    """Encender muestra la luz; apagarla la retira al instante (retractable)."""
    token = _register(client, "brillante")
    resp = client.post(
        "/api/me/share-progress",
        headers={"X-Auth-Token": token},
        json={"on": True},
    )
    assert resp.status_code == 200
    assert resp.get_json()["share_progress"] is True

    lights = client.get(
        "/api/community/lights", headers={"X-Auth-Token": token}
    ).get_json()
    assert lights["total_lights"] == 1
    assert lights["lights"][0]["username"] == "brillante"
    assert len(lights["lights"][0]["branches"]) >= 1
    assert "email" not in lights["lights"][0]

    resp = client.post(
        "/api/me/share-progress",
        headers={"X-Auth-Token": token},
        json={"on": False},
    )
    assert resp.get_json()["share_progress"] is False
    lights = client.get(
        "/api/community/lights", headers={"X-Auth-Token": token}
    ).get_json()
    assert lights["total_lights"] == 0


def test_lights_show_progress_averages_but_never_rank(client, app):
    """El muro muestra el progreso de cada luz, sin exponer detalles privados."""
    token = _register(client, "obrera")
    topic_id = _make_topic(app, "luz_" + token[:8])
    client.post(
        "/api/topics/" + str(topic_id) + "/start",
        headers={"X-Auth-Token": token},
        json={},
    )
    client.post(
        "/api/topics/" + str(topic_id) + "/test",
        headers={"X-Auth-Token": token},
        json={"answers": [0, 0, 0]},
    )
    client.post(
        "/api/me/share-progress", headers={"X-Auth-Token": token}, json={"on": True}
    )
    lights = client.get(
        "/api/community/lights", headers={"X-Auth-Token": token}
    ).get_json()
    assert lights["total_lights"] == 1
    light = lights["lights"][0]
    assert light["best_score"] == 100
    assert sum(b["pct"] for b in light["branches"]) > 0


def test_lights_sorted_alphabetically_not_by_progress(client, app):
    """Cero ranking: el orden del muro es alfabético, jamás por puntaje."""
    token_a = _register(client, "ana")
    token_z = _register(client, "zulma")
    # Ana tiene el mejor puntaje posible; Zulma apenas empieza.
    topic_id = _make_topic(app, "light_rank")
    client.post(
        f"/api/topics/{topic_id}/start", headers={"X-Auth-Token": token_a}, json={}
    )
    client.post(
        f"/api/topics/{topic_id}/test",
        headers={"X-Auth-Token": token_a},
        json={"answers": [0, 0, 0]},
    )
    for token in (token_a, token_z):
        client.post(
            "/api/me/share-progress", headers={"X-Auth-Token": token}, json={"on": True}
        )
    lights = client.get(
        "/api/community/lights", headers={"X-Auth-Token": token_a}
    ).get_json()
    order = [l["username"] for l in lights["lights"]]
    assert order == sorted(order, key=str.lower)  # ana antes que zulma
    assert order == ["ana", "zulma"]  # la mejor nota no la trepa al tope


def test_by_branch_counts_only_lit_districts(client, app):
    """Los conteos por barrio suman solo las luces con obras, sin nombres."""
    token = _register(client, "farolera")
    topic_id = _make_topic(app, "branch_lights")
    client.post(
        f"/api/topics/{topic_id}/start", headers={"X-Auth-Token": token}, json={}
    )
    client.post(
        f"/api/topics/{topic_id}/test",
        headers={"X-Auth-Token": token},
        json={"answers": [0, 0, 0]},
    )
    client.post(
        "/api/me/share-progress", headers={"X-Auth-Token": token}, json={"on": True}
    )
    data = client.get(
        "/api/community/lights", headers={"X-Auth-Token": token}
    ).get_json()
    assert data["by_branch"]  # al menos el barrio de la obra cuenta 1
    branch0 = data["by_branch"][0]
    assert set(branch0.keys()) == {"nombre", "lights"}
