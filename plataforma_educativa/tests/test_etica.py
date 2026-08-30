# -*- coding: utf-8 -*-
"""Test 17: la categoría Ética (M16) — la casa en lenguaje común.

Los fundamentos del sistema explicados sin jerga propia; la jerga se nombra
SOLO en el puente final. Verifica: siembra idempotente, cadena de
prerrequisitos, banco de preguntas (situaciones, no doctrina), enlaces del
mundo, orden de barrio (la Ética primero) y la auditoría anti-jerga
determinista sobre los archivos de la biblioteca.
"""

import os
import re

import pytest
from app.db import get_db

# Jerga propia: prohibida en los temas 1-11 (permitida en el puente).
_JERGA = re.compile(r"\b(VHV|TVI|SDV|Maxo\w*|EIR|Maxocracia|oráculo|oracle|INV[-\s]?|OEV)\b", re.IGNORECASE)
_MATERIALS_DIR = os.path.join(os.path.dirname(__file__), "..", "materials")


def _register(client, username):
    client.post("/api/auth/register", json={"username": username, "password": "secreto"})
    return client.post(
        "/api/auth/login", json={"username": username, "password": "secreto"}
    ).get_json()["token"]


def test_etica_branch_seeded_with_12_topics(app):
    """La rama Ética nace orden 0 con sus 12 temas (idempotente por slug)."""
    with app.app_context():
        db = get_db()
        branch = db.execute("SELECT * FROM branches WHERE slug = 'etica'").fetchone()
        assert branch is not None
        assert branch["orden"] == 0
        branch2 = db.execute("SELECT COUNT(*) AS n FROM branches WHERE slug = 'etica'").fetchone()["n"]
        assert branch2 == 1  # dos pasadas no duplican
        topics = db.execute(
            "SELECT * FROM topics WHERE branch_id = ? ORDER BY orden", (branch["id"],)
        ).fetchall()
        assert len(topics) == 12
        order = [t["orden"] for t in topics]
        assert order == list(range(1, 13))
        # Cadena 1→12 (solo el primero sin prerrequisitos).
        assert json_loads(topics[0]["prereq_ids"]) == []
        for a, b in zip(topics, topics[1:]):
            assert json_loads(b["prereq_ids"]) == [a["id"]]


def json_loads(s):
    import json
    return json.loads(s or "[]")


def test_etica_questions_are_situations(app):
    """Cada tema ético tiene ≥3 preguntas (el test no es catecismo)."""
    with app.app_context():
        db = get_db()
        branch = db.execute("SELECT id FROM branches WHERE slug = 'etica'").fetchone()
        topics = db.execute(
            "SELECT id FROM topics WHERE branch_id = ?", (branch["id"],)
        ).fetchall()
        for topic in topics:
            q_count = db.execute(
                "SELECT COUNT(*) AS n FROM questions WHERE topic_id = ?", (topic["id"],)
            ).fetchone()["n"]
            assert q_count >= 3, f"el tema {topic['id']} tiene {q_count} preguntas"


def test_etica_wikipedia_links_seeded(app):
    """Cada tema ético tiene su enlace al mundo verificado."""
    with app.app_context():
        db = get_db()
        branch = db.execute("SELECT id FROM branches WHERE slug = 'etica'").fetchone()
        topics = db.execute(
            "SELECT id FROM topics WHERE branch_id = ?", (branch["id"],)
        ).fetchall()
        for topic in topics:
            m = db.execute(
                "SELECT * FROM materials WHERE topic_id = ? AND tipo = 'enlace'",
                (topic["id"],),
            ).fetchone()
            assert m is not None
            assert m["url"].startswith("https://es.wikipedia.org/wiki/")


def test_etica_is_first_branch_in_tree(client, app):
    """La Ética aparece primero en el árbol: los valores primero, la técnica después."""
    token = _register(client, "vecina")
    tree = client.get("/api/tree", headers={"X-Auth-Token": token}).get_json()
    assert tree["branches"][0]["slug"] == "etica"


def test_materials_served_per_user_language(client, app):
    """La biblioteca se sirve en la lengua de la persona (estructura i18n)."""
    token = _register(client, "traductora")
    with app.app_context():
        db = get_db()
        topic = db.execute(
            "SELECT id FROM topics WHERE slug = 'etica_la_vida_se_cuenta'"
        ).fetchone()
        db.execute(
            "INSERT INTO materials (topic_id, material_key, titulo, tipo, fuente, url, "
            "contenido, autor, orden, idioma, created_at) "
            "VALUES (?, 'etica_la_vida_se_cuenta#eng1', 'The life counts', 'guia', 'oev', NULL, "
            "'English body', 'siembra', 1, 'en', ?)",
            (topic["id"], "2026-08-30T00:00:00+00:00"),
        )
        db.commit()
        topic_id = topic["id"]

    # Por defecto (es): solo la guía en español (y el enlace español).
    resp = client.get(f"/api/topics/{topic_id}/materials", headers={"X-Auth-Token": token})
    assert resp.get_json()["lang"] == "es"
    titulos_es = [m["titulo"] for m in resp.get_json()["materials"]]
    assert "The life counts" not in titulos_es

    # Cambiar a inglés y verificar que el idioma viaja.
    client.post(
        "/api/me/idioma", headers={"X-Auth-Token": token}, json={"idioma": "en"}
    )
    resp = client.get(f"/api/topics/{topic_id}/materials", headers={"X-Auth-Token": token})
    assert resp.get_json()["lang"] == "en"
    titulos_en = [m["titulo"] for m in resp.get_json()["materials"]]
    assert "The life counts" in titulos_en

    # ?lang= sobreescribe (pruebas y traducciones) y valida códigos.
    resp = client.get(f"/api/topics/{topic_id}/materials?lang=es", headers={"X-Auth-Token": token})
    assert resp.get_json()["lang"] == "es"
    resp = client.post(
        "/api/me/idioma", headers={"X-Auth-Token": token}, json={"idioma": "123"}
    )
    assert resp.status_code == 400


def test_etica_guides_free_of_jargon_except_bridge():
    """Auditoría determinista: cero jerga propia en los temas 1-11 de la Ética.

    El puente final (etica_el_idioma_de_la_ciudad) es EL lugar donde los
    conceptos se nombran — y debe nombrarlos.
    """
    files = sorted(
        f for f in os.listdir(_MATERIALS_DIR)
        if f.startswith("etica_") and f.endswith(".es.md")
    )
    assert len(files) == 12
    guides = 0
    for f in files:
        with open(os.path.join(_MATERIALS_DIR, f), encoding="utf-8") as fh:
            content = fh.read()
        if "el_idioma_de_la_ciudad" in f:
            for term in ("VHV", "TVI", "SDV", "Maxo", "EIR", "OEV"):
                assert term in content, f"el puente debe nombrar {term}"
        else:
            guides += 1
            assert not _JERGA.search(content), f"{f} contiene jerga propia: {_JERGA.findall(content)}"
    assert guides == 11
