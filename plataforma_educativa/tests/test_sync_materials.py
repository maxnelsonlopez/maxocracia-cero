# -*- coding: utf-8 -*-
"""Test 16: el sincronizador de la Biblioteca (M15) — .md → tabla materials.

La inserción canónica: un archivo con mini front-matter, idempotente por
material_key (repitir no duplica), y honesto (los huérfanos se reportan,
nunca se botan en silencio).
"""

import os

import pytest

from sync_materials import parse_material_file, sync_materials


def _write(dir_path, name, text):
    path = os.path.join(dir_path, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


# --------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------

def test_parse_valid_material():
    text = "titulo: Guía de conteo\ntema: conteo\norden: 2\n\n# Qué aprenderás\nContar es..."
    parsed = parse_material_file(text)
    assert parsed is not None
    assert parsed["titulo"] == "Guía de conteo"
    assert parsed["tema"] == "conteo"
    assert parsed["orden"] == 2
    assert parsed["autor"] == "siembra"
    assert parsed["contenido"].startswith("# Qué aprenderás")


def test_parse_rejects_missing_fields():
    assert parse_material_file("tema: conteo\n\nsin título") is None
    assert parse_material_file("titulo: X\ntema: conteo\n\n") is None
    assert parse_material_file("titulo: X\n\ncuerpo") is None


def test_parse_defaults_orden():
    parsed = parse_material_file("titulo: X\ntema: conteo\n\ncuerpo")
    assert parsed["orden"] == 1


# --------------------------------------------------------------------------
# Sincronizador
# --------------------------------------------------------------------------

def test_sync_inserts_and_is_idempotent(app, tmp_path):
    """Primera corrida siembra; la segunda no duplica (idempotencia)."""
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    _write(
        str(materials_dir),
        "conteo.md",
        "titulo: Conteo, la llave\ntema: conteo\norden: 1\n\n**Qué es**\nContar es mapear.\n",
    )
    db_path = app.config["DATABASE"]

    first = sync_materials(db_path=db_path, materials_dir=str(materials_dir))
    assert first["added"] == 1
    assert first["updated"] == 0
    assert first["warnings"] == []

    second = sync_materials(db_path=db_path, materials_dir=str(materials_dir))
    assert second["added"] == 0
    assert second["updated"] == 0


def test_sync_updates_when_content_changes(app, tmp_path):
    """El tejido muta: cambiar el contenido actualiza, no duplica."""
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    _write(str(materials_dir), "conteo.md", "titulo: Conteo\ntema: conteo\norden: 1\n\nversión 1\n")
    sync_materials(db_path=app.config["DATABASE"], materials_dir=str(materials_dir))
    _write(str(materials_dir), "conteo.md", "titulo: Conteo\ntema: conteo\norden: 1\n\nversión 2\n")
    result = sync_materials(db_path=app.config["DATABASE"], materials_dir=str(materials_dir))
    assert result["updated"] == 1
    assert result["added"] == 0


def test_sync_reports_orphan_topic(app, tmp_path):
    """Un tema que no existe en la base se reporta, no se siembra a ciegas."""
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    _write(
        str(materials_dir),
        "fantasma.md",
        "titulo: Fantasía\ntema: no_existe_ni_aquí\norden: 1\n\ncontenido\n",
    )
    result = sync_materials(db_path=app.config["DATABASE"], materials_dir=str(materials_dir))
    assert result["added"] == 0
    assert any("no_existe_ni_aquí" in w for w in result["warnings"])


def test_sync_reports_malformed_file(app, tmp_path):
    """Un `.md` mal formado se reporta y sigue con los demás."""
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    _write(str(materials_dir), "roto.md", "esto no es front-matter\n\ncontenido\n")
    result = sync_materials(db_path=app.config["DATABASE"], materials_dir=str(materials_dir))
    assert result["added"] == 0
    assert any("roto.md" in w for w in result["warnings"])
