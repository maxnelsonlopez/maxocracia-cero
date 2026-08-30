# -*- coding: utf-8 -*-
"""Sincronizador de la Biblioteca de la Ciudad (M15).

Convierte archivos markdown de ``materials/`` en filas de la tabla
``materials`` de la plataforma educativa. Es la vía canónica de inserción de
material: escribir un ``.md`` con mini front-matter y correr el sincronizador.

Formato de cada archivo (las primeras líneas antes de la primera línea vacía
son ``clave: valor``; el resto es el contenido markdown):

    titulo: Fracciones con trozos de pizza
    tema: fracciones
    orden: 1
    autor: siembra

    <contenido de la guía>

Reglas:
- Idempotente: mismo ``material_key`` (``<tema>#g<orden>``) = una fila,
  actualizada si el archivo cambió (el tejido muta; la genealogía queda en git).
- Solo se sincronizan temas que existen en la base; los huérfanos se reportan.
- No toca los enlaces sembrados (``material_key`` ``<tema>#w1``) — otro canal.

Uso:
    .venv\\Scripts\\python.exe plataforma_educativa/sync_materials.py
"""

import os
import sqlite3
import sys
from datetime import datetime, timezone

# Raíz de la plataforma (donde viven materials/ y la base por defecto).
_PLATFORM_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MATERIALS_DIR = os.path.join(_PLATFORM_ROOT, "materials")
DEFAULT_DB_PATH = os.path.join(_PLATFORM_ROOT, "plataforma_educativa.db")


def _now():
    return datetime.now(timezone.utc).isoformat()


def parse_material_file(text):
    """Parsea el contenido de un archivo .md de material.

    Devuelve dict(titulo, tema, orden, autor, contenido) o None si el archivo
    no cumple el formato (tema y título obligatorios, contenido no vacío).
    """
    lines = text.splitlines()
    meta = {}
    body_start = None
    for i, line in enumerate(lines):
        if not line.strip():
            body_start = i + 1
            break
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip().lower()] = value.strip()
        else:
            # Línea no-meta antes del cuerpo: formato inválido.
            return None
    if body_start is None:
        body_start = len(lines)
    contenido = "\n".join(lines[body_start:]).strip()
    tema = (meta.get("tema") or "").strip()
    titulo = (meta.get("titulo") or "").strip()
    if not tema or not titulo or not contenido:
        return None
    try:
        orden = int(meta.get("orden") or 1)
    except (TypeError, ValueError):
        orden = 1
    idioma = (meta.get("idioma") or "es").strip()[:2].lower() or "es"
    if not idioma.isalpha():
        idioma = "es"
    return {
        "titulo": titulo[:200],
        "tema": tema,
        "orden": max(1, orden),
        "idioma": idioma,
        "autor": (meta.get("autor") or "siembra").strip()[:80] or "siembra",
        "contenido": contenido,
    }


def sync_materials(db_path=None, materials_dir=None):
    """Sincroniza todos los ``.md`` del directorio en la base de datos.

    Devuelve dict con ``added``, ``updated`` y ``warnings`` (temas huérfanos o
    archivos mal formados). No lanza excepción por un archivo inválido: lo
    reporta y sigue (el tejido se revisa, no se rompe por una pieza).
    """
    db_path = db_path or DEFAULT_DB_PATH
    materials_dir = materials_dir or DEFAULT_MATERIALS_DIR
    result = {"added": 0, "updated": 0, "warnings": []}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # El sincronizador asegura su propia tabla (DDL idempotente): la
        # inserción fácil no depende de reiniciar la app primero.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS materials ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "topic_id INTEGER NOT NULL REFERENCES topics(id),"
            "material_key TEXT NOT NULL UNIQUE,"
            "titulo TEXT NOT NULL,"
            "tipo TEXT NOT NULL DEFAULT 'guia' CHECK(tipo IN ('guia', 'enlace')),"
            "fuente TEXT NOT NULL DEFAULT 'oev',"
            "url TEXT,"
            "contenido TEXT,"
            "autor TEXT NOT NULL DEFAULT 'siembra',"
            "orden INTEGER NOT NULL DEFAULT 0,"
            "created_at TEXT NOT NULL)"
        )
        topic_ids = {
            row["slug"]: row["id"]
            for row in conn.execute("SELECT id, slug FROM topics").fetchall()
        }
        if not os.path.isdir(materials_dir):
            return result  # sin directorio de materiales: nada que hacer

        files = sorted(f for f in os.listdir(materials_dir) if f.endswith(".md"))
        for filename in files:
            path = os.path.join(materials_dir, filename)
            with open(path, encoding="utf-8") as fh:
                parsed = parse_material_file(fh.read())
            if parsed is None:
                result["warnings"].append(f"{filename}: formato inválido (se ignora)")
                continue
            topic_id = topic_ids.get(parsed["tema"])
            if topic_id is None:
                result["warnings"].append(
                    f"{filename}: tema '{parsed['tema']}' no existe (se ignora)"
                )
                continue
            key = f"{parsed['tema']}#{parsed['idioma']}g{parsed['orden']}"
            before = conn.execute(
                "SELECT contenido FROM materials WHERE material_key = ?", (key,)
            ).fetchone()
            conn.execute(
                "INSERT INTO materials "
                "(topic_id, material_key, titulo, tipo, fuente, url, contenido, autor, orden, idioma, created_at) "
                "VALUES (?, ?, ?, 'guia', 'oev', NULL, ?, ?, ?, ?, ?) "
                "ON CONFLICT(material_key) DO UPDATE SET "
                "titulo = excluded.titulo, contenido = excluded.contenido, "
                "autor = excluded.autor, orden = excluded.orden, idioma = excluded.idioma",
                (
                    topic_id,
                    key,
                    parsed["titulo"],
                    parsed["contenido"],
                    parsed["autor"],
                    parsed["orden"],
                    parsed["idioma"],
                    _now(),
                ),
            )
            if before is None:
                result["added"] += 1
            elif before["contenido"] != parsed["contenido"]:
                result["updated"] += 1
        conn.commit()
    finally:
        conn.close()
    return result


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    db_path = argv[0] if argv else None
    result = sync_materials(db_path=db_path)
    print(f"Biblioteca sincronizada: {result['added']} nuevas, {result['updated']} actualizadas.")
    for warning in result["warnings"]:
        print(f"  ⚠ {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
