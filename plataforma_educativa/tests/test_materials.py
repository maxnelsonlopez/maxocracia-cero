# -*- coding: utf-8 -*-
"""Test 14: la Biblioteca de la Ciudad (M15) — material educativo por tema.

La biblioteca tiene dos capas: enlaces al mundo (sembrados y verificados) y
guías propias en markdown que llegan por el sincronizador. Los endpoints solo
leen; la inserción canónica es ``sync_materials`` (test_sync_materials.py).
"""

import uuid

from app.db import get_db


def _register(client, username):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    return client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    ).get_json()["token"]


def test_materials_requires_auth(client):
    """Sin token no se abre la biblioteca (login_required)."""
    resp = client.get("/api/topics/1/materials")
    assert resp.status_code == 401


def test_topic_materials_includes_seeded_wikipedia_links(client, app):
    """Todo tema sembrado tiene al menos un enlace al mundo (Wikipedia)."""
    token = _register(client, "lectora")
    with app.app_context():
        topic = get_db().execute(
            "SELECT id, slug FROM topics WHERE slug = 'conteo'"
        ).fetchone()
    resp = client.get(
        f"/api/topics/{topic['id']}/materials", headers={"X-Auth-Token": token}
    )
    assert resp.status_code == 200
    materials = resp.get_json()["materials"]
    assert len(materials) == 1
    m = materials[0]
    assert m["tipo"] == "enlace"
    assert m["fuente"] == "wikipedia"
    assert m["url"].startswith("https://es.wikipedia.org/wiki/")
    assert m["tiene_contenido"] is False


def test_material_detail_returns_guia_markdown(client, app):
    """Las guías propias se sirven completas (markdown) y sueltas."""
    token = _register(client, "constructora")
    with app.app_context():
        db = get_db()
        topic = db.execute("SELECT id FROM topics WHERE slug = 'conteo'").fetchone()
        cur = db.execute(
            "INSERT INTO materials (topic_id, material_key, titulo, tipo, fuente, "
            "url, contenido, autor, orden, created_at) "
            "VALUES (?, ?, ?, 'guia', 'oev', NULL, ?, 'siembra', 2, ?)",
            (topic["id"], "conteo#g2", "Guía de conteo", "**Qué es en una frase**\nContar es...", "2026-08-30T00:00:00+00:00"),
        )
        db.commit()
        material_id = cur.lastrowid
        # La guía ya estaba en la tabla: también puede llegar por sync; aquí
        # probamos la lectura exacta.
        resp = client.get(
            f"/api/materials/{material_id}", headers={"X-Auth-Token": token}
        )
    assert resp.status_code == 200
    material = resp.get_json()["material"]
    assert material["tipo"] == "guia"
    assert material["tiene_contenido"] is True
    assert material["titulo"] == "Guía de conteo"


def test_material_detail_404(client):
    """Un material inexistente responde 404 (nada de silencios)."""
    token = _register(client, "buscadora")
    resp = client.get("/api/materials/999999", headers={"X-Auth-Token": token})
    assert resp.status_code == 404


def test_materials_404_for_unknown_topic(client):
    """La biblioteca de un tema inexistente responde 404."""
    token = _register(client, "curiosa")
    resp = client.get(
        "/api/topics/999999/materials", headers={"X-Auth-Token": token}
    )
    assert resp.status_code == 404


def test_materials_sorted_by_orden(client, app):
    """La biblioteca se ordena por 'orden' (guías primero si así se siembra)."""
    token = _register(client, "ordenada")
    with app.app_context():
        db = get_db()
        topic = db.execute("SELECT id FROM topics WHERE slug = 'conteo'").fetchone()
        db.execute(
            "INSERT INTO materials (topic_id, material_key, titulo, tipo, fuente, url, "
            "contenido, autor, orden, created_at) "
            "VALUES (?, 'conteo#g9', 'Guía 9', 'guia', 'oev', NULL, 'texto', 'siembra', 9, ?)",
            (topic["id"], "2026-08-30T00:00:00+00:00"),
        )
        db.commit()
    resp = client.get(
        f"/api/topics/{topic['id']}/materials", headers={"X-Auth-Token": token}
    )
    assert resp.status_code == 200
    ordenes = [m["orden"] for m in resp.get_json()["materials"]]
    assert ordenes == sorted(ordenes)


def test_evidence_visible_back_in_biblioteca_propia(client, app):
    """El material que la persona aportó (M13) sigue visible con su detalle."""
    token = _register(client, "vacuadora")
    with app.app_context():
        db = get_db()
        branch_id = db.execute("SELECT id FROM branches ORDER BY id LIMIT 1").fetchone()["id"]
        cur = db.execute(
            "INSERT INTO topics (branch_id, slug, titulo, descripcion, orden, prereq_ids, dificultad) "
            "VALUES (?, ?, 'Tema', 'descripción', 998, '[]', 1)",
            (branch_id, "bib_" + uuid.uuid4().hex[:8]),
        )
        topic_id = cur.lastrowid
        for i in range(3):
            db.execute(
                "INSERT INTO questions (topic_id, pregunta, opciones, correcta, explicacion) "
                "VALUES (?, ?, ?, ?, ?)",
                (topic_id, f"¿Pregunta {i}?", '["a", "b", "c", "d"]', 0, "explicación"),
            )
        db.commit()
    # Aprobar el tema (respuestas correctas) para poder aportar material.
    resp = client.post(
        f"/api/topics/{topic_id}/test",
        headers={"X-Auth-Token": token},
        json={"answers": [0, 0, 0]},
    )
    assert resp.status_code == 200
    resp = client.post(
        f"/api/topics/{topic_id}/evidence",
        headers={"X-Auth-Token": token},
        json={"tipo": "texto", "titulo": "Mi guía de conteo", "texto": "Contar es repartir platos."},
    )
    assert resp.status_code == 201
    # Se ve en el árbol (badge) y en el detalle del tema: la obra nunca se pierde.
    tree = client.get("/api/tree", headers={"X-Auth-Token": token}).get_json()
    topic = next(t for b in tree["branches"] for t in b["topics"] if t["id"] == topic_id)
    assert topic["evidence"] is not None
    assert topic["evidence"]["titulo"] == "Mi guía de conteo"
    assert topic["evidence"]["texto"] == "Contar es repartir platos."
