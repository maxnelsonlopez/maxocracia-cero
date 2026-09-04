# -*- coding: utf-8 -*-
"""API del Buscador educativo (B1) — semillas + motores abiertos con fail-open.

Reglas de acceso coherentes con el diseño (P1/P6):

- **Lectura pública** (buscar, score, archivo, parámetros): buscar es un
  derecho; sin cuentas, sin ads, sin tracking. Así la lente SearXNG puede
  federar las semillas vía ``?format=searx`` sin credenciales.
- **Escritura solo coordinador** (siembra/verificación): la regla M15 manda —
  los enlaces se verifican antes de sembrar, con ojos humanos.
"""

import os
import urllib.parse

from flask import Blueprint, g, jsonify, request

from .auth import login_required
from .db import get_db
from . import buscador

buscador_bp = Blueprint("buscador", __name__)


def _es_coordinador():
    fila = get_db().execute(
        "SELECT is_coordinator FROM users WHERE id = ?", (g.user_id,)
    ).fetchone()
    return bool(fila and fila["is_coordinator"])


# --------------------------------------------------------------------------
# Lectura (pública)
# --------------------------------------------------------------------------

@buscador_bp.route("/api/buscador", methods=["GET"])
def buscar():
    """Búsqueda unificada: semillas verificadas + Zenodo + SearXNG (opcional).

    ``?format=searx`` devuelve el formato del motor ``json_engine`` de SearXNG
    para que la lente educativa federe nuestras semillas.
    """
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify({"error": "Falta la consulta (?q=)."}), 400
    data = buscador.buscar(get_db(), q)
    if (request.args.get("format") or "").lower() == "searx":
        return jsonify(buscador.format_searx(data))
    return jsonify(data), 200


@buscador_bp.route("/api/buscador/score", methods=["GET"])
def score():
    """Score de confiabilidad Nivel 1 de una URL (banda + razones + motor)."""
    url = (request.args.get("url") or "").strip()
    if not url:
        return jsonify({"error": "Falta la URL (?url=)."}), 400
    return jsonify(buscador.score_nivel1(get_db(), url)), 200


@buscador_bp.route("/api/buscador/archivo", methods=["GET"])
def archivo():
    """Rescate Wayback Machine: el snapshot más cercano de una URL.
    Fail-open: si Wayback no responde, se informa y se devuelve 200."""
    url = (request.args.get("url") or "").strip()
    if not url:
        return jsonify({"error": "Falta la URL (?url=)."}), 400
    try:
        snap = buscador.wayback_rescate(url)
    except Exception as exc:  # fail-open: la memoria no bloquea el presente
        return (
            jsonify(
                {
                    "url": url,
                    "archivo": None,
                    "fail_open": f"wayback: {exc.__class__.__name__}",
                }
            ),
            200,
        )
    return jsonify({"url": url, "archivo": snap}), 200


@buscador_bp.route("/api/buscador/seeds", methods=["GET"])
def listar_seeds():
    """Lista completa de semillas (verificadas primero)."""
    filas = get_db().execute(
        "SELECT * FROM buscador_seeds ORDER BY verificada DESC, id ASC"
    ).fetchall()
    return jsonify({"seeds": [dict(f) for f in filas]}), 200


@buscador_bp.route("/api/buscador/parametros", methods=["GET"])
def parametros():
    """Parámetros vigentes del buscador (con procedencia T13). En B4 los vota
    el Parlamento Educativo con el patrón M9."""
    return jsonify({"parametros": buscador.get_parametros(get_db())}), 200


@buscador_bp.route("/api/buscador/corpus", methods=["GET"])
def corpus():
    """Búsqueda solo en el corpus propio (memoria local, sin red aguas
    arriba). Pública: la memoria de la ciudad se lee sin pedir papeles."""
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify({"error": "Falta la consulta (?q=)."}), 400
    try:
        items = buscador.engine_corpus(get_db(), q)
    except Exception as exc:
        return jsonify({"query": q, "resultados": [], "fail_open": f"corpus: {exc.__class__.__name__}"}), 200
    for r in items:
        if "banda" not in r:
            veredicto = buscador.score_nivel1(get_db(), r["url"])
            r["banda"] = veredicto["banda"]
            r["razones"] = veredicto["razones"]
            r["motor_score"] = veredicto["motor"]
    return jsonify({"query": q, "resultados": items}), 200


@buscador_bp.route("/api/buscador/feeds", methods=["GET"])
def listar_feeds():
    """Feeds registrados (candidatos + verificados, con su estado)."""
    filas = get_db().execute("SELECT * FROM buscador_feeds ORDER BY id ASC").fetchall()
    return jsonify({"feeds": [dict(f) for f in filas]}), 200


# --------------------------------------------------------------------------
# Escritura (solo coordinador — regla M15)
# --------------------------------------------------------------------------

@buscador_bp.route("/api/buscador/seeds", methods=["POST"])
@login_required
def crear_seed():
    if not _es_coordinador():
        return jsonify({"error": "Solo el coordinador siembra (regla M15)."}), 403
    body = request.get_json(silent=True) or {}
    url = (body.get("url") or "").strip()
    titulo = (body.get("titulo") or "").strip()
    if not url or not titulo:
        return jsonify({"error": "Faltan campos obligatorios: url, titulo."}), 400

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return jsonify({"error": "URL inválida (se espera http/https)."}), 400

    seed_key = (body.get("seed_key") or "").strip()
    if not seed_key:
        seed_key = "web:" + parsed.netloc.lower() + (parsed.path or "/")
    fuente = (body.get("fuente") or parsed.netloc.lower()).strip()
    nueva = get_db().execute(
        "INSERT INTO buscador_seeds "
        "(seed_key, tipo, titulo, url, resumen, fuente, identidad_id, etiquetas, idioma, verificada, fecha, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, datetime('now')) "
        "ON CONFLICT(seed_key) DO UPDATE SET titulo = excluded.titulo, resumen = excluded.resumen "
        "RETURNING id",
        (
            seed_key,
            (body.get("tipo") or "web").strip(),
            titulo,
            url,
            (body.get("resumen") or "").strip(),
            fuente,
            (body.get("identidad_id") or "").strip() or None,
            (body.get("etiquetas") or "").strip(),
            (body.get("idioma") or "es").strip()[:2],
            (body.get("fecha") or "").strip() or None,
        ),
    ).fetchone()
    get_db().commit()
    # La siembra nueva nace CANDIDATA (verificada = 0): se verifica con el
    # endpoint de verificación tras comprobar la URL (regla M15).
    fila = get_db().execute(
        "SELECT * FROM buscador_seeds WHERE id = ?", (nueva["id"],)
    ).fetchone()
    return jsonify({"seed": dict(fila), "nota": "candidata: verificar antes de sembrar (M15)"}), 201


@buscador_bp.route("/api/buscador/feeds", methods=["POST"])
@login_required
def crear_feed():
    """Registra un feed candidato (nace sin verificar, regla M15)."""
    if not _es_coordinador():
        return jsonify({"error": "Solo el coordinador siembra feeds (regla M15)."}), 403
    body = request.get_json(silent=True) or {}
    url = (body.get("url") or "").strip()
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "URL inválida (se espera http/https)."}), 400
    try:
        fila = buscador.registrar_feed(
            get_db(),
            url,
            tipo=(body.get("tipo") or "blog"),
            titulo=(body.get("titulo") or ""),
            idioma=(body.get("idioma") or "es"),
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"feed": dict(fila), "nota": "candidato: verificar antes de ingerir (M15)"}), 201


@buscador_bp.route("/api/buscador/feeds/<int:feed_id>/verificar", methods=["POST"])
@login_required
def verificar_feed(feed_id):
    """Verificación HTTP + parse real del feed (regla M15). Fail-open: si
    la red falla, se informa con 502 sin romper nada."""
    if not _es_coordinador():
        return jsonify({"error": "Solo el coordinador verifica (regla M15)."}), 403
    try:
        fila = buscador.verificar_feed(get_db(), feed_id)
    except LookupError:
        return jsonify({"error": "Feed no encontrado."}), 404
    except Exception as exc:
        return jsonify({"error": "verificación", "fail_open": f"red: {exc.__class__.__name__}"}), 502
    return jsonify({"feed": dict(fila)}), 200


@buscador_bp.route("/api/buscador/feeds/<int:feed_id>/ingerir", methods=["POST"])
@login_required
def ingerir_feed(feed_id):
    """Ingiere un feed VERIFICADO al corpus (idempotente por URL).
    403 si es candidato (M15); 502 si la red falla (fail-open)."""
    if not _es_coordinador():
        return jsonify({"error": "Solo el coordinador ingiere (regla M15)."}), 403
    try:
        n = buscador.ingerir_feed(get_db(), feed_id)
    except LookupError:
        return jsonify({"error": "Feed no encontrado."}), 404
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
    except Exception as exc:
        return jsonify({"error": "ingesta", "fail_open": f"red: {exc.__class__.__name__}"}), 502
    return jsonify({"ingeridos": n}), 200


@buscador_bp.route("/api/buscador/seeds/<int:seed_id>/materializar", methods=["POST"])
@login_required
def materializar_seed(seed_id):
    """Materializa una semilla verificada al corpus (P8: la memoria vive
    en casa). 403 si es candidata (M15)."""
    if not _es_coordinador():
        return jsonify({"error": "Solo el coordinador materializa (regla M15)."}), 403
    try:
        doc = buscador.materializar_seed(get_db(), seed_id)
    except LookupError:
        return jsonify({"error": "Semilla no encontrada."}), 404
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
    return jsonify({"doc": dict(doc)}), 201


@buscador_bp.route("/api/buscador/seeds/<int:seed_id>/verificar", methods=["POST"])
@login_required
def verificar_seed(seed_id):
    """Marca/desmarca la verificación humana de una semilla (regla M15)."""
    if not _es_coordinador():
        return jsonify({"error": "Solo el coordinador verifica (regla M15)."}), 403
    body = request.get_json(silent=True) or {}
    verificada = 1 if body.get("verificada", True) else 0
    cursor = get_db().execute(
        "UPDATE buscador_seeds SET verificada = ? WHERE id = ?", (verificada, seed_id)
    )
    get_db().commit()
    if cursor.rowcount == 0:
        return jsonify({"error": "Semilla no encontrada."}), 404
    fila = get_db().execute(
        "SELECT * FROM buscador_seeds WHERE id = ?", (seed_id,)
    ).fetchone()
    return jsonify({"seed": dict(fila)}), 200
