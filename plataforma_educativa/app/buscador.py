# -*- coding: utf-8 -*-
"""Buscador educativo independiente (B1) — semillas verificadas + motores abiertos.

Diseño canónico: ``docs/architecture/DISENO_BUSCADOR_EDUCATIVO_GRATUITO.md``
Estado del arte: ``docs/architecture/ESTADO_DEL_ARTE_BUSCADOR_EDUCATIVO.md``

Principios del diseño (P1-P8), aplicados aquí:

- **$0 y sin dependencias nuevas**: solo librería estándar (urllib/json/re).
- **Fail-open**: ningún motor aguas arriba (Zenodo, SearXNG, Wayback) rompe la
  búsqueda; si falla, se reporta en ``motores_fail_open`` y sigue.
- **Etiqueta, no censura (P3)**: los resultados llevan una banda de
  confiabilidad con razones visibles; NINGÚN resultado se oculta.
- **Local primero (P2)**: no hay APIs de pago; las semillas viven en la base
  local y los motores son abiertos (Zenodo público, SearXNG auto-hospedado).

B1 cubre: semillas canónicas (``seeds/maxocracia.json``), capa Zenodo (API
pública sin token), capa SearXNG opcional (``BUSCADOR_SEARXNG_URL``), rescate
Wayback (availability) y score de confiabilidad Nivel 1 (heurístico, sin red).

El score Nivel 2 (LLM juez local → OpenRouter free → nada) es B4; la tabla
``buscador_parameters`` ya queda gobernable para el Parlamento Educativo
(patrones M9: procedencia T13 y votación con cooldown).
"""

import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# Constantes de motores abiertos (todas las fuentes son gratuitas y con
# contrato estable — ver tabla de fuentes en el diseño, §2 y §3).
# --------------------------------------------------------------------------

ZENODO_API = "https://zenodo.org/api/records"
WAYBACK_AVAILABILITY = "https://archive.org/wayback/available"

# Infraestructura educativa abierta: basta con pertenecer a estos dominios
# para la banda "rastreable" (la plataforma M15 ya verifica estos enlaces).
DOMINIOS_ABIERTOS = (
    "wikipedia.org",
    "wikimedia.org",
    "wikiversidad.org",
    "zenodo.org",
    "archive.org",
    "openalex.org",
    "eric.ed.gov",
    "oercommons.org",
    "merlot.org",
    "doi.org",
)

_USER_AGENT = (
    "MaxocraciaEduBuscador/0.1 (buscador educativo sin tracking; "
    "https://github.com/maxnelsonlopez/maxocracia-cero)"
)

_DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s\"<>]+)")
_HTML_RE = re.compile(r"<[^>]+>")

# Bandas de confiabilidad (de mayor a menor). "Desconocida" no excluye: es
# información honesta sobre procedencia (P3: etiqueta, no censura).
BANDAS = ("verificada", "rastreable", "desconocida")


def _now():
    return datetime.now(timezone.utc).isoformat()


def _timeout():
    return float(os.environ.get("BUSCADOR_UPSTREAM_TIMEOUT", "6"))


def _http_get_json(url, timeout=None):
    """GET JSON con User-Agent propio. Levanta excepción si algo falla —
    el fail-open de cada motor la captura y la reporta (nunca silencio)."""
    req = urllib.request.Request(
        url, headers={"User-Agent": _USER_AGENT, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout or _timeout()) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


# --------------------------------------------------------------------------
# Score de confiabilidad — Nivel 1 (heurístico, $0, sin red)
# --------------------------------------------------------------------------

def _seed_por_url(conn, url):
    """Busca una semilla por URL exacta o por el DOI contenido en la URL."""
    u = (url or "").strip()
    row = conn.execute("SELECT * FROM buscador_seeds WHERE url = ?", (u,)).fetchone()
    if row is not None:
        return row
    m = _DOI_RE.search(u)
    if m:
        doi = m.group(1).rstrip(".")
        row = conn.execute(
            "SELECT * FROM buscador_seeds WHERE url LIKE ? LIMIT 1", (f"%{doi}%",)
        ).fetchone()
    return row


def score_nivel1(conn, url):
    """Score de confiabilidad Nivel 1: mide PROCEDENCIA verificable, nunca
    conformidad de opinión. Devuelve banda + razones + motor (trazabilidad T13)."""
    u = (url or "").strip()
    razones = []

    row = _seed_por_url(conn, u)
    if row is not None:
        if row["verificada"]:
            razones.append("semilla verificada de la comunidad educativa (regla M15)")
            banda = "verificada"
        else:
            razones.append("semilla candidata: pendiente de verificación humana")
            banda = "rastreable"
        return {"banda": banda, "razones": razones, "motor": "heuristico:v1"}

    if _DOI_RE.search(u):
        razones.append("identificador persistente (DOI) de archivo académico abierto")
        banda = "rastreable"
    else:
        host = urllib.parse.urlparse(u).netloc.lower()
        if any(host == d or host.endswith("." + d) for d in DOMINIOS_ABIERTOS):
            razones.append("dominio de infraestructura educativa abierta")
            banda = "rastreable"
        else:
            banda = "desconocida"
            razones.append("sin señales de procedencia todavía: desconocida no significa excluida (P3)")

    if u.startswith("https://"):
        razones.append("conexión cifrada (HTTPS)")
    return {"banda": banda, "razones": razones, "motor": "heuristico:v1"}


# --------------------------------------------------------------------------
# Motores (cada uno devuelve resultados normalizados; falla → excepción, que
# ``buscar()`` captura y reporta: fail-open con memoria).
# --------------------------------------------------------------------------

def engine_semasillas(conn, query, limite=20):
    """Capa semillas: el bloque GARANTIZADO. Las verificadas primero; las
    candidatas al final con su banda honesta (nada se oculta, P3)."""
    tokens = [t for t in re.split(r"\s+", (query or "").lower()) if t]
    if not tokens:
        return []
    filas = conn.execute(
        "SELECT * FROM buscador_seeds ORDER BY verificada DESC, id ASC"
    ).fetchall()
    resultados = []
    for fila in filas:
        paja = " ".join(
            filter(
                None,
                [
                    fila["titulo"],
                    fila["resumen"] or "",
                    fila["url"],
                    fila["etiquetas"] or "",
                    fila["fuente"],
                ],
            )
        ).lower()
        if all(t in paja for t in tokens):
            resultados.append(
                {
                    "capa": "semillas",
                    "titulo": fila["titulo"],
                    "url": fila["url"],
                    "resumen": fila["resumen"] or "",
                    "fuente": fila["fuente"],
                    "tipo": fila["tipo"],
                    "identidad_id": fila["identidad_id"],
                    "fecha": fila["fecha"],
                    "verificada": bool(fila["verificada"]),
                }
            )
            if len(resultados) >= limite:
                break
    return resultados


def _limpia_html(texto, maximo=320):
    limpio = _HTML_RE.sub(" ", texto or "").replace("&nbsp;", " ")
    limpio = re.sub(r"\s+", " ", limpio).strip()
    return limpio[:maximo] + ("…" if len(limpio) > maximo else "")


def engine_zenodo(query, size=None):
    """Capa académica: API pública de Zenodo, sin token (verificado 03-09-2026)."""
    if size is None:
        size = int(os.environ.get("BUSCADOR_ZENODO_SIZE", "5"))
    url = ZENODO_API + "?" + urllib.parse.urlencode(
        {"q": query, "size": size, "sort": "bestmatch"}
    )
    data = _http_get_json(url) or {}
    resultados = []
    for h in (data.get("hits") or {}).get("hits") or []:
        meta = h.get("metadata") or {}
        doi = (h.get("doi") or "").strip()
        enlace = (
            "https://doi.org/" + doi
            if doi
            else (h.get("links") or {}).get("self_html") or ""
        )
        if not enlace:
            continue
        autores = ", ".join(
            (c.get("name") or "").strip() for c in meta.get("creators") or [] if c.get("name")
        )
        resultados.append(
            {
                "capa": "academica",
                "titulo": (meta.get("title") or "").strip() or "(sin título)",
                "url": enlace,
                "resumen": _limpia_html(meta.get("description") or ""),
                "fuente": "zenodo",
                "tipo": "paper",
                "autores": autores,
                "fecha": meta.get("publication_date"),
                "doi": doi,
            }
        )
    return resultados


def engine_searxng(query):
    """Capa web general: SearXNG auto-hospedado con lente educativa (JSON API).
    Sin BUSCADOR_SEARXNG_URL la capa está desactivada — eso no es un fallo."""
    base = os.environ.get("BUSCADOR_SEARXNG_URL", "").strip().rstrip("/")
    if not base:
        return []
    url = base + "/search?" + urllib.parse.urlencode(
        {"q": query, "format": "json", "language": "es"}
    )
    data = _http_get_json(url) or {}
    resultados = []
    for r in (data.get("results") or [])[:10]:
        enlace = (r.get("url") or "").strip()
        if not enlace:
            continue
        resultados.append(
            {
                "capa": "web",
                "titulo": (r.get("title") or "").strip() or "(sin título)",
                "url": enlace,
                "resumen": (r.get("content") or "").strip(),
                "fuente": "searxng:" + str(r.get("engine") or ""),
            }
        )
    return resultados


def wayback_rescate(url):
    """Rescate de enlaces muertos: el snapshot más cercano en Wayback Machine
    (API availability, gratuita). Devuelve dict o None si nunca se archivó."""
    q = WAYBACK_AVAILABILITY + "?" + urllib.parse.urlencode({"url": url})
    data = _http_get_json(q) or {}
    closest = (data.get("archived_snapshots") or {}).get("closest")
    if not closest:
        return None
    return {
        "snapshot_url": closest.get("url"),
        "timestamp": closest.get("timestamp"),
        "status": closest.get("status"),
    }


# --------------------------------------------------------------------------
# Búsqueda unificada (fusión de capas con transparencia)
# --------------------------------------------------------------------------

def buscar(conn, query):
    """Fusiona las capas con transparencia total:

    - semillas verificadas primero (bloque garantizado, §5.3 del diseño);
    - luego académico (Zenodo) y web (SearXNG, si está configurada);
    - todo resultado lleva banda + razones (P3/P4);
    - un motor caído NO rompe nada: se lista en ``motores_fail_open``.
    """
    resultados = []
    por_capa = {}
    fail_open = []

    def _agregar(items):
        for r in items:
            u = (r.get("url") or "").strip()
            if not u or any(x["url"] == u for x in resultados):
                continue
            r["url"] = u
            if "banda" not in r:
                veredicto = score_nivel1(conn, u)
                r["banda"] = veredicto["banda"]
                r["razones"] = veredicto["razones"]
                r["motor_score"] = veredicto["motor"]
            resultados.append(r)
            por_capa[r["capa"]] = por_capa.get(r["capa"], 0) + 1

    _agregar(engine_semasillas(conn, query))

    try:
        _agregar(engine_zenodo(query))
    except Exception as exc:  # fail-open: la búsqueda sigue sin Zenodo
        fail_open.append(f"zenodo: {exc.__class__.__name__}")

    try:
        _agregar(engine_searxng(query))
    except Exception as exc:  # fail-open: la búsqueda sigue sin SearXNG
        fail_open.append(f"searxng: {exc.__class__.__name__}")

    return {
        "query": query,
        "resultados": resultados,
        "por_capa": por_capa,
        "motores_fail_open": fail_open,
        "principios": (
            "etiqueta-no-censura: ningún resultado se oculta; las bandas "
            "explican la procedencia (P3/P4). Sin ads, sin tracking (P1)."
        ),
    }


def format_searx(data):
    """Formato compatible con el motor ``json_engine`` de SearXNG: así la
    lente educativa de cualquier instancia puede federar nuestras semillas."""
    return {
        "results": [
            {"title": r["titulo"], "url": r["url"], "content": r["resumen"]}
            for r in data.get("resultados", [])
        ]
    }


# --------------------------------------------------------------------------
# Siembra canónica y parámetros gobernable
# --------------------------------------------------------------------------

SEEDS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "seeds",
    "maxocracia.json",
)

_PARAMETROS_CANON = {
    "buscador_zenodo_size": "5",
    "buscador_searxng_capa": "1",
    "buscador_score_ttl_dias": "90",
}


def sync_seeds_file(db_path, ruta=None):
    """Siembra las semillas canónicas de ``seeds/maxocracia.json`` —
    idempotente por ``seed_key``. La verificación humana NUNCA se revierte al
    resincronizar (``verificada = MAX(actual, canónica)``)."""
    ruta = ruta or SEEDS_FILE
    if not os.path.exists(ruta):
        return 0
    with open(ruta, encoding="utf-8") as fh:
        canon = json.load(fh)
    # El archivo puede ser una lista directa o un objeto {"semillas": [...]}.
    items = canon.get("semillas", []) if isinstance(canon, dict) else canon
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    n = 0
    for s in items:
        conn.execute(
            "INSERT INTO buscador_seeds "
            "(seed_key, tipo, titulo, url, resumen, fuente, identidad_id, etiquetas, "
            " idioma, verificada, fecha, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(seed_key) DO UPDATE SET "
            "  titulo = excluded.titulo, resumen = excluded.resumen, "
            "  url = excluded.url, tipo = excluded.tipo, fuente = excluded.fuente, "
            "  identidad_id = excluded.identidad_id, etiquetas = excluded.etiquetas, "
            "  idioma = excluded.idioma, fecha = excluded.fecha, "
            "  verificada = MAX(buscador_seeds.verificada, excluded.verificada)",
            (
                s["seed_key"],
                s.get("tipo", "web"),
                s["titulo"],
                s["url"],
                s.get("resumen", ""),
                s.get("fuente", "web"),
                s.get("identidad_id"),
                s.get("etiquetas", ""),
                s.get("idioma", "es"),
                1 if s.get("verificada") else 0,
                s.get("fecha"),
                _now(),
            ),
        )
        n += 1
    conn.commit()
    conn.close()
    return n


def sync_parametros(conn):
    """Parámetros por defecto del buscador (idempotente). En B4 pasan al
    Parlamento Educativo: el voto escribe valor + procedencia (patrón M9)."""
    for clave, valor in _PARAMETROS_CANON.items():
        conn.execute(
            "INSERT OR IGNORE INTO buscador_parameters (parametro, valor, procedencia, updated_at) "
            "VALUES (?, ?, 'canon-B1', ?)",
            (clave, valor, _now()),
        )


def sync_parametros_db(db_path):
    """Variante para el arranque (create_app): conexión propia, commit y cierre."""
    conn = sqlite3.connect(db_path)
    try:
        sync_parametros(conn)
        conn.commit()
    finally:
        conn.close()


def get_parametros(conn):
    filas = conn.execute("SELECT * FROM buscador_parameters ORDER BY parametro").fetchall()
    return {f["parametro"]: {"valor": f["valor"], "procedencia": f["procedencia"]} for f in filas}
