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
WAYBACK_CDX = "https://web.archive.org/cdx/search/cdx"
# Capas abiertas directas (B5): APIs públicas, sin clave, $0. La familia
# Wikimedia como referencia general (la que la biblioteca M15 ya siembra
# verificada) y OpenAlex como academia con DOI y citas (diseño §3C).
OPENALEX_API = "https://api.openalex.org/works"

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


def _http_get_bytes(url, timeout=None, accept="*/*"):
    """GET crudo con User-Agent propio. Punto único de red (testeable):

    devuelve ``(status, bytes, content_type)``. Levanta excepción si algo
    falla — el fail-open de cada motor la captura y la reporta (nunca
    silencio). Los tests reemplazan esta función por dobles (sin red real).
    """
    req = urllib.request.Request(
        url, headers={"User-Agent": _USER_AGENT, "Accept": accept}
    )
    with urllib.request.urlopen(req, timeout=timeout or _timeout()) as resp:
        return (
            getattr(resp, "status", 200) or 200,
            resp.read(),
            (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower(),
        )


def _http_get_json(url, timeout=None):
    """GET JSON con User-Agent propio. Levanta excepción si algo falla —
    el fail-open de cada motor la captura y la reporta (nunca silencio)."""
    _status, raw, _ctype = _http_get_bytes(url, timeout=timeout, accept="application/json")
    return json.loads(raw.decode("utf-8", "replace"))


def _http_get_text(url, timeout=None):
    """GET texto (RSS/Atom/HTML) con User-Agent propio. Devuelve
    ``(status, texto)`` con decodificación tolerante."""
    status, raw, _ctype = _http_get_bytes(url, timeout=timeout, accept="*/*")
    return status, raw.decode("utf-8", "replace")


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


def engine_wikimedia(query, dominio, fuente, size):
    """Motor genérico de la familia Wikimedia (misma API pública, sin clave;
    solo cambia el dominio). Lo que la biblioteca M15 ya verifica, ahora
    también se encuentra — y las hermanas que enseñan (Wikibooks,
    Wikiversidad) entran con el mismo código."""
    url = "https://" + dominio + "/w/api.php?" + urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": max(1, size),
            "format": "json",
            "formatversion": "2",
        }
    )
    data = _http_get_json(url) or {}
    resultados = []
    for h in (data.get("query") or {}).get("search") or []:
        titulo = (h.get("title") or "").strip()
        if not titulo:
            continue
        resultados.append(
            {
                "capa": "referencia",
                "titulo": titulo,
                "url": "https://" + dominio + "/wiki/"
                + urllib.parse.quote(titulo.replace(" ", "_")),
                "resumen": _limpia_html(h.get("snippet") or ""),
                "fuente": fuente,
                "tipo": "referencia",
            }
        )
    return resultados


def engine_wikipedia(query, size=None):
    """Capa referencia: Wikipedia en español (API pública, sin clave)."""
    if size is None:
        size = int(os.environ.get("BUSCADOR_WIKIPEDIA_SIZE", "5"))
    return engine_wikimedia(query, "es.wikipedia.org", "wikipedia", size)


def engine_wikibooks(query, size=None):
    """Capa referencia: Wikibooks en español (libros de texto libres)."""
    if size is None:
        size = int(os.environ.get("BUSCADOR_WIKIMEDIA_SIZE", "3"))
    return engine_wikimedia(query, "es.wikibooks.org", "wikibooks", size)


def engine_wikiversity(query, size=None):
    """Capa referencia: Wikiversidad en español (recursos de aprendizaje)."""
    if size is None:
        size = int(os.environ.get("BUSCADOR_WIKIMEDIA_SIZE", "3"))
    return engine_wikimedia(query, "es.wikiversity.org", "wikiversidad", size)


def _resumen_openalex(indice, max_palabras=40):
    """Reconstruye el inicio del resumen desde el índice invertido de
    OpenAlex (stdlib: ordenar posiciones y cortar)."""
    if not isinstance(indice, dict) or not indice:
        return ""
    colocadas = {}
    for palabra, posiciones in indice.items():
        for p in posiciones or []:
            colocadas[p] = palabra
    texto = " ".join(colocadas[p] for p in sorted(colocadas))
    palabras = texto.split()
    return (" ".join(palabras[:max_palabras]) + ("…" if len(palabras) > max_palabras else ""))


def engine_openalex(query, size=None):
    """Capa académica (II): OpenAlex, API pública sin clave (diseño §3C).
    DOI + citas + año: procedencia rastreable por construcción."""
    if size is None:
        size = int(os.environ.get("BUSCADOR_OPENALEX_SIZE", "5"))
    url = OPENALEX_API + "?" + urllib.parse.urlencode(
        {
            "search": query,
            "per-page": max(1, size),
            "select": "id,doi,title,publication_year,authorships,abstract_inverted_index,cited_by_count",
        }
    )
    data = _http_get_json(url) or {}
    resultados = []
    for w in data.get("results") or []:
        titulo = (w.get("title") or "").strip()
        doi = (w.get("doi") or "").strip()
        enlace = doi or (w.get("id") or "").strip()
        if not titulo or not enlace:
            continue
        autores = [a.get("author", {}).get("display_name", "") for a in w.get("authorships") or []]
        autores = [a for a in autores if a][:3]
        resumen = _resumen_openalex(w.get("abstract_inverted_index"))
        if w.get("cited_by_count"):
            resumen = (resumen + " " if resumen else "") + f"[{w['cited_by_count']} citas]"
        resultados.append(
            {
                "capa": "academica",
                "titulo": titulo,
                "url": enlace,
                "resumen": resumen,
                "fuente": "openalex",
                "tipo": "paper",
                "autores": ", ".join(autores),
                "fecha": str(w.get("publication_year") or ""),
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
# B2 — Corpus verificado: feeds + ingesta + índice local (todo stdlib, $0)
#
# Regla M15: un feed nace CANDIDATO (verificada = 0); solo la verificación
# HTTP + parse real lo habilita para ingesta. La ingesta es idempotente por
# URL del documento. La búsqueda del corpus es local (FTS5, con fallback a
# LIKE si el SQLite no trae FTS5 compilado) — fail-open documentado.
# --------------------------------------------------------------------------

def parse_feed(xml_texto):
    """Parsea un feed RSS o Atom (stdlib xml.etree) y devuelve items
    ``[{titulo, url, resumen, fecha}]``. Sin red, función pura (testeable).

    Acepta RSS 2.0 (channel/item) y Atom (entry). Los namespaces se ignoran
    por sufijo (``{ns}tag`` → ``tag``) para no depender de prefijos.
    """
    import xml.etree.ElementTree as ET

    def _local(tag):
        return tag.rsplit("}", 1)[-1] if "}" in tag else tag

    def _texto(el, nombres):
        for hijo in el:
            if _local(hijo.tag).lower() in nombres:
                return (hijo.text or "").strip()
        return ""

    def _enlace(el):
        for hijo in el:
            if _local(hijo.tag).lower() == "link":
                href = (hijo.get("href") or "").strip()
                if href:
                    return href
                if (hijo.text or "").strip().startswith("http"):
                    return (hijo.text or "").strip()
        return ""

    raiz = ET.fromstring((xml_texto or "").strip() or "<vacio/>")
    items = []
    for el in raiz.iter():
        nombre = _local(el.tag).lower()
        if nombre not in ("item", "entry"):
            continue
        titulo = _texto(el, {"title"}) or "(sin título)"
        url = _enlace(el) or _texto(el, {"link", "id", "guid"})
        if not url.startswith("http"):
            continue
        items.append(
            {
                "titulo": titulo,
                "url": url.strip(),
                "resumen": _limpia_html(_texto(el, {"description", "summary", "content", "encoded"})),
                "fecha": _texto(el, {"pubdate", "published", "updated", "date"}),
            }
        )
    return items


def wayback_first_capture(url):
    """Primera captura Wayback (CDX) de una URL/dominio: señal de longevidad
    del diseño §3A. Devuelve el timestamp o None. Fail-open: levanta
    excepción y el llamador la reporta (la memoria no bloquea el presente)."""
    q = WAYBACK_CDX + "?" + urllib.parse.urlencode(
        {"url": url, "limit": 1, "output": "json"}
    )
    data = _http_get_json(q) or []
    if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
        return str(data[1][0]) if len(data[1]) > 0 else None
    if isinstance(data, dict):
        return None
    return None


def registrar_feed(conn, url, tipo="blog", titulo="", idioma="es"):
    """Registra un feed candidato (verificada = 0). Idempotente por URL."""
    u = (url or "").strip()
    if not u.startswith(("http://", "https://")):
        raise ValueError("URL inválida (se espera http/https).")
    if tipo not in ("blog", "youtube", "web"):
        tipo = "blog"
    fila = conn.execute(
        "INSERT INTO buscador_feeds (url, tipo, titulo, idioma, verificada, created_at) "
        "VALUES (?, ?, ?, ?, 0, ?) "
        "ON CONFLICT(url) DO UPDATE SET tipo = excluded.tipo, titulo = excluded.titulo "
        "RETURNING id",
        (u, tipo, (titulo or "").strip(), (idioma or "es")[:2], _now()),
    ).fetchone()
    conn.commit()
    return conn.execute("SELECT * FROM buscador_feeds WHERE id = ?", (fila["id"],)).fetchone()


def verificar_feed(conn, feed_id):
    """Verificación HTTP + parse real (regla M15). Solo con 200 y contenido
    parseable (feed con ≥1 item, o HTML con <title>) marca verificada = 1.
    Actualiza last_fetch/last_status siempre (memoria del intento)."""
    fila = conn.execute("SELECT * FROM buscador_feeds WHERE id = ?", (feed_id,)).fetchone()
    if fila is None:
        raise LookupError("Feed no encontrado.")
    try:
        status, texto = _http_get_text(fila["url"])
    except Exception:
        conn.execute(
            "UPDATE buscador_feeds SET last_fetch = ?, last_status = NULL WHERE id = ?",
            (_now(), feed_id),
        )
        conn.commit()
        raise
    conn.execute(
        "UPDATE buscador_feeds SET last_fetch = ?, last_status = ? WHERE id = ?",
        (_now(), status, feed_id),
    )
    ok = False
    if status == 200 and texto:
        try:
            ok = len(parse_feed(texto)) >= 1
        except Exception:
            ok = False
        if not ok:
            m = re.search(r"<title[^>]*>(.*?)</title>", texto, re.IGNORECASE | re.DOTALL)
            ok = bool(m and _limpia_html(m.group(1)))
    if ok:
        conn.execute("UPDATE buscador_feeds SET verificada = 1 WHERE id = ?", (feed_id,))
    conn.commit()
    return conn.execute("SELECT * FROM buscador_feeds WHERE id = ?", (feed_id,)).fetchone()


def _wayback_mejor_esfuerzo(url):
    """Primera captura Wayback sin romper la ingesta (fail-open → None)."""
    try:
        return wayback_first_capture(url)
    except Exception:
        return None


def ingerir_feed(conn, feed_id, max_items=20):
    """Ingiere los items de un feed VERIFICADO al corpus (idempotente por
    URL del documento). Falla con PermissionError si no está verificado
    (M15); la red que falle levanta excepción (el endpoint la reporta)."""
    fila = conn.execute("SELECT * FROM buscador_feeds WHERE id = ?", (feed_id,)).fetchone()
    if fila is None:
        raise LookupError("Feed no encontrado.")
    if not fila["verificada"]:
        raise PermissionError("Feed candidato: verificar antes de ingerir (M15).")
    _status, texto = _http_get_text(fila["url"])
    items = parse_feed(texto)[: max(1, max_items)]
    n = 0
    for it in items:
        conn.execute(
            "INSERT INTO buscador_docs "
            "(url, feed_id, capa, titulo, resumen, texto, idioma, tipo, fecha, wayback_ts, indexed_at) "
            "VALUES (?, ?, 'corpus', ?, ?, ?, ?, 'web', ?, ?, ?) "
            "ON CONFLICT(url) DO UPDATE SET titulo = excluded.titulo, resumen = excluded.resumen",
            (
                it["url"],
                feed_id,
                it["titulo"],
                it.get("resumen", ""),
                it.get("resumen", ""),
                fila["idioma"],
                it.get("fecha") or None,
                _wayback_mejor_esfuerzo(it["url"]),
                _now(),
            ),
        )
        n += 1
    conn.execute(
        "UPDATE buscador_feeds SET last_fetch = ?, last_status = 200 WHERE id = ?",
        (_now(), feed_id),
    )
    conn.commit()
    return n


def materializar_seed(conn, seed_id):
    """Materializa una semilla al corpus (el texto propio vive en casa, P8):
    copia verificada del registro con el resumen como texto inicial.
    Idempotente por URL. Solo semillas verificadas (M15)."""
    semilla = conn.execute("SELECT * FROM buscador_seeds WHERE id = ?", (seed_id,)).fetchone()
    if semilla is None:
        raise LookupError("Semilla no encontrada.")
    if not semilla["verificada"]:
        raise PermissionError("Semilla candidata: verificar antes de materializar (M15).")
    conn.execute(
        "INSERT INTO buscador_docs "
        "(url, seed_id, capa, titulo, resumen, texto, idioma, tipo, fecha, wayback_ts, indexed_at) "
        "VALUES (?, ?, 'corpus', ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(url) DO UPDATE SET titulo = excluded.titulo, resumen = excluded.resumen",
        (
            semilla["url"],
            seed_id,
            semilla["titulo"],
            semilla["resumen"] or "",
            semilla["resumen"] or "",
            semilla["idioma"] or "es",
            semilla["tipo"] or "web",
            semilla["fecha"],
            _wayback_mejor_esfuerzo(semilla["url"]),
            _now(),
        ),
    )
    conn.commit()
    return conn.execute("SELECT * FROM buscador_docs WHERE url = ?", (semilla["url"],)).fetchone()


def _fts_disponible(conn):
    fila = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'buscador_docs_fts'"
    ).fetchone()
    return fila is not None


def _tokens_fts(query):
    toks = [re.sub(r'["*:.^()\[\]]', "", t) for t in re.split(r"\s+", (query or "").lower()) if t]
    return [t for t in toks if t]


def _fragmento(texto, tokens, ventana=300):
    """Recorte honesto alrededor del primer hallazgo (suelo sin FTS5)."""
    bajo = (texto or "").lower()
    pos = -1
    for t in tokens:
        i = bajo.find(t.lower())
        if i >= 0 and (pos < 0 or i < pos):
            pos = i
    if pos < 0:
        return (texto or "")[:ventana]
    inicio = max(0, pos - 120)
    trozo = (texto or "")[inicio : inicio + ventana]
    return ("…" if inicio > 0 else "") + trozo + ("…" if inicio + ventana < len(texto or "") else "")


def engine_corpus(conn, query, limite=10):
    """Capa corpus: el tejido propio (feeds verificados + semillas
    materializadas + biblioteca privada B7). FTS5 si está compilado; si no,
    LIKE (fail-open).

    Regla B7: la biblioteca privada solo muestra FRAGMENTOS (snippet FTS5 o
    recorte): el texto completo nunca sale del disco del dueño.

    Devuelve resultados normalizados con capa = 'corpus'. Nunca hace red:
    es memoria local, siempre disponible (P2).
    """
    tokens = _tokens_fts(query)
    if not tokens:
        return []
    filas = []
    fragmentos = {}
    if _fts_disponible(conn):
        try:
            match = " AND ".join(f'"{t}"*' for t in tokens)
            filas = conn.execute(
                "SELECT d.*, snippet(buscador_docs_fts, 2, '', '', ' … ', 24) AS frag "
                "FROM buscador_docs_fts f "
                "JOIN buscador_docs d ON d.id = f.rowid "
                "WHERE buscador_docs_fts MATCH ? LIMIT ?",
                (match, limite),
            ).fetchall()
            fragmentos = {f["id"]: (f["frag"] or "") for f in filas}
        except sqlite3.OperationalError:
            filas = []  # el LIKE de abajo es el suelo (fail-open)
    if not filas:
        like = "%" + "%".join(tokens) + "%"
        conds = " AND ".join(["(titulo || ' ' || resumen || ' ' || texto) LIKE ?"] * len(tokens))
        params = [f"%{t}%" for t in tokens] if len(tokens) > 1 else [like]
        try:
            filas = conn.execute(
                f"SELECT * FROM buscador_docs WHERE {conds} LIMIT ?",
                (*params, limite),
            ).fetchall()
        except sqlite3.OperationalError:
            return []
    resultados = []
    for f in filas:
        if (f["capa"] or "") == "biblioteca":
            resumen = fragmentos.get(f["id"]) or _fragmento(f["texto"], tokens)
            fuente = "biblioteca privada"
            visibilidad = f["visibilidad"] or "privada"
        else:
            resumen = f["resumen"] or ""
            fuente = ("feed:" + str(f["feed_id"])) if f["feed_id"] else ("seed:" + str(f["seed_id"] or ""))
            visibilidad = "publica"
        resultados.append(
            {
                "capa": "corpus",
                "titulo": f["titulo"],
                "url": f["url"],
                "resumen": resumen,
                "fuente": fuente,
                "visibilidad": visibilidad,
                "tipo": f["tipo"],
                "fecha": f["fecha"],
                "wayback_ts": f["wayback_ts"],
            }
        )
    return resultados


# --------------------------------------------------------------------------
# B3 — Score con memoria: cache con TTL + razones del corpus (todo local)
#
# El Nivel 1 es barato, pero el Nivel 2 (B4, LLM juez) no: por eso el score
# vive en ``buscador_scores`` con caducidad. El TTL se lee del parámetro
# gobernable ``buscador_score_ttl_dias`` (90 días, canon-B1). Transparencia
# total (P4): el endpoint dice si el veredicto vino de cache o se calculó.
#
# Además el corpus enriquece sus resultados con memoria PROPIA (sin red):
# procedencia verificada (semilla/feed) y longevidad Wayback guardada en
# ``wayback_ts`` (diseño §5.2: antigüedad como señal anti-spam honesta).
# --------------------------------------------------------------------------

def _ttl_dias(conn):
    try:
        return int((get_parametros(conn).get("buscador_score_ttl_dias") or {}).get("valor", 90))
    except (TypeError, ValueError):
        return 90


def score_cache_get(conn, url, nivel=1):
    """Lee el score cacheado. Devuelve None si no existe o caducó (la
    entrada caducada se borra: la memoria caduca, no miente)."""
    fila = conn.execute(
        "SELECT * FROM buscador_scores WHERE url = ? AND nivel = ?", (url, nivel)
    ).fetchone()
    if fila is None:
        return None
    try:
        edad = (datetime.now(timezone.utc) - datetime.fromisoformat(fila["scored_at"])).days
    except (TypeError, ValueError):
        return None
    if edad > max(_ttl_dias(conn), 0):
        conn.execute("DELETE FROM buscador_scores WHERE url = ? AND nivel = ?", (url, nivel))
        conn.commit()
        return None
    try:
        razones = json.loads(fila["razones_json"] or "[]")
    except (TypeError, ValueError):
        razones = []
    return {"banda": fila["banda"], "razones": razones, "motor": fila["motor"]}


def score_cache_set(conn, url, nivel, banda, razones, motor):
    """Guarda un score (idempotente por url+nivel)."""
    conn.execute(
        "INSERT INTO buscador_scores (url, nivel, banda, razones_json, motor, scored_at, ttl_dias) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(url, nivel) DO UPDATE SET "
        "banda = excluded.banda, razones_json = excluded.razones_json, "
        "motor = excluded.motor, scored_at = excluded.scored_at, ttl_dias = excluded.ttl_dias",
        (url, nivel, banda, json.dumps(list(razones or [])), motor, _now(), _ttl_dias(conn)),
    )
    conn.commit()


def score_con_cache(conn, url, nivel=1):
    """Score Nivel 1 con memoria: cache vigente o cómputo + guardado.
    Devuelve el veredicto más ``cache: hit|miss`` (trazabilidad P4)."""
    u = (url or "").strip()
    hit = score_cache_get(conn, u, nivel)
    if hit is not None:
        return {"banda": hit["banda"], "razones": hit["razones"], "motor": hit["motor"], "cache": "hit"}
    veredicto = score_nivel1(conn, u)
    score_cache_set(conn, u, nivel, veredicto["banda"], veredicto["razones"], veredicto["motor"])
    return {"banda": veredicto["banda"], "razones": veredicto["razones"],
            "motor": veredicto["motor"], "cache": "miss"}


def enriquecer_corpus(conn, resultado):
    """Añade al resultado del corpus sus razones propias (local, sin red):

    - semilla verificada materializada → banda verificada;
    - feed verificado → razón de procedencia comunitaria;
    - ``wayback_ts`` → razón de longevidad (memoria larga, §3A).
    Mutación in-situ; devuelve el mismo dict."""
    if resultado.get("capa") != "corpus":
        return resultado
    fila = conn.execute("SELECT * FROM buscador_docs WHERE url = ?", (resultado["url"],)).fetchone()
    if fila is None:
        return resultado
    razones = list(resultado.get("razones") or [])
    if fila["seed_id"]:
        sem = conn.execute(
            "SELECT verificada FROM buscador_seeds WHERE id = ?", (fila["seed_id"],)
        ).fetchone()
        if sem and sem["verificada"]:
            resultado["banda"] = "verificada"
            razones.insert(0, "semilla verificada materializada en el corpus (B2)")
    elif fila["feed_id"]:
        feed = conn.execute(
            "SELECT verificada, titulo FROM buscador_feeds WHERE id = ?", (fila["feed_id"],)
        ).fetchone()
        if feed and feed["verificada"]:
            nombre = (feed["titulo"] or "").strip() or ("feed " + str(fila["feed_id"]))
            razones.insert(0, f"del corpus verificado de la comunidad ({nombre})")
    elif (fila["capa"] or "") == "biblioteca":
        if (fila["visibilidad"] or "privada") == "publica":
            razones.insert(
                0, f"🌍 publicada por el curador (licencia: {fila['licencia'] or 'closed'})"
            )
        else:
            razones.insert(
                0, "📚 biblioteca privada del dueño: solo fragmentos, nunca el texto completo (B7)"
            )
    if fila["wayback_ts"]:
        razones.append(f"memoria larga: archivado desde {fila['wayback_ts']} (Wayback, §3A)")
    resultado["razones"] = razones
    return resultado


# --------------------------------------------------------------------------
# B4 — El juez trabaja de noche: cola del Nivel 2 + parámetros vinculantes
#
# La búsqueda NUNCA espera al LLM: el Nivel 1 responde al instante y el juez
# puntúa por lotes las urls nuevas (cola ``buscador_score_queue``). Cuando el
# Nivel 2 existe y está vigente, refina al Nivel 1 (``mejor_score``); si
# caducó o nunca existió, el heurístico sigue (fail-open).
#
# Los parámetros los gobierna el parlamento: el voto escribe valor +
# procedencia con cooldown de 14 días (patrón M9). La deliberación vive en la
# asamblea; aquí queda registrado lo resuelto, por quién y cuándo (T13).
# --------------------------------------------------------------------------

COOLDOWN_RESOLUCION_DIAS = 14


def _lote_juez():
    try:
        return max(1, int(os.environ.get("BUSCADOR_JUEZ_LOTE", "10")))
    except (TypeError, ValueError):
        return 10


def encolar_pendientes_nivel2(conn, limite=200):
    """Encola las urls del tejido propio (semillas + corpus) sin veredicto
    Nivel 2 vigente. Idempotente por url. Devuelve cuántas quedaron pendientes."""
    candidatas = {}
    for fila in conn.execute("SELECT url, titulo FROM buscador_seeds").fetchall():
        candidatas[fila["url"]] = fila["titulo"] or ""
    for fila in conn.execute("SELECT url, titulo FROM buscador_docs").fetchall():
        candidatas.setdefault(fila["url"], fila["titulo"] or "")
    nuevas = 0
    for url, titulo in list(candidatas.items())[: max(1, limite)]:
        if score_cache_get(conn, url, 2) is not None:
            continue
        conn.execute(
            "INSERT INTO buscador_score_queue (url, titulo, estado, intentos, created_at, updated_at) "
            "VALUES (?, ?, 'pendiente', 0, ?, ?) "
            "ON CONFLICT(url) DO UPDATE SET updated_at = excluded.updated_at",
            (url, titulo, _now(), _now()),
        )
        nuevas += 1
    conn.commit()
    return nuevas


def ejecutar_cola_nivel2(conn, lote=None):
    """Procesa UN lote de la cola con el juez (lote = BUSCADOR_JUEZ_LOTE).
    Guarda cada veredicto como Nivel 2 (motor trazable) y marca la url
    procesada o fallida (con intentos). Levanta ``SinJuez`` si no hay juez:
    la noche puede esperar, el día sigue con Nivel 1."""
    from . import score_engine

    lote = lote or _lote_juez()
    pendientes = conn.execute(
        "SELECT * FROM buscador_score_queue WHERE estado = 'pendiente' ORDER BY created_at LIMIT ?",
        (lote,),
    ).fetchall()
    if not pendientes:
        return {"procesadas": 0, "fallidas": 0, "motor": "ninguno"}
    items = []
    for p in pendientes:
        fila = conn.execute("SELECT titulo, resumen, fuente FROM buscador_seeds WHERE url = ?", (p["url"],)).fetchone()
        if fila is None:
            fila = conn.execute(
                "SELECT titulo, resumen, 'corpus' AS fuente FROM buscador_docs WHERE url = ?", (p["url"],)
            ).fetchone()
        items.append(
            {
                "url": p["url"],
                "titulo": (fila["titulo"] if fila else None) or p["titulo"] or "",
                "resumen": (fila["resumen"] if fila else None) or "",
                "fuente": (fila["fuente"] if fila else None) or "",
            }
        )
    veredictos, motor = score_engine.juzgar_lote(items)
    procesadas = fallidas = 0
    for v in veredictos:
        try:
            score_cache_set(conn, v["url"], 2, v["banda"], v["razones"], motor)
            conn.execute(
                "UPDATE buscador_score_queue SET estado = 'procesada', updated_at = ? WHERE url = ?",
                (_now(), v["url"]),
            )
            procesadas += 1
        except Exception:
            conn.execute(
                "UPDATE buscador_score_queue SET estado = 'fallida', intentos = intentos + 1, updated_at = ? "
                "WHERE url = ?",
                (_now(), v["url"]),
            )
            fallidas += 1
    conn.commit()
    return {"procesadas": procesadas, "fallidas": fallidas, "motor": motor}


def mejor_score(conn, url):
    """El mejor veredicto vigente: Nivel 2 si existe, si no Nivel 1.
    Devuelve banda + razones + motor + nivel (P4: el refinamiento se nota)."""
    n2 = score_cache_get(conn, (url or "").strip(), 2)
    if n2 is not None:
        return {"banda": n2["banda"], "razones": n2["razones"], "motor": n2["motor"], "nivel": 2}
    v1 = score_nivel1(conn, url)
    return {"banda": v1["banda"], "razones": v1["razones"], "motor": v1["motor"], "nivel": 1}


def estado_cola(conn):
    """Foto de la cola nocturna + veredictos Nivel 2 vigentes (pública)."""
    filas = conn.execute(
        "SELECT estado, COUNT(*) AS n FROM buscador_score_queue GROUP BY estado"
    ).fetchall()
    conteo = {f["estado"]: f["n"] for f in filas}
    n2 = conn.execute("SELECT COUNT(*) AS n FROM buscador_scores WHERE nivel = 2").fetchone()["n"]
    return {
        "pendientes": conteo.get("pendiente", 0),
        "procesadas": conteo.get("procesada", 0),
        "fallidas": conteo.get("fallida", 0),
        "veredictos_nivel2": n2,
    }


def resolver_parametro(conn, parametro, valor, resolucion):
    """Registra lo resuelto por la asamblea sobre un parámetro (patrón M9):
    valor + procedencia obligatoria + cooldown de 14 días por parámetro.
    Levanta LookupError (parámetro ajeno), ValueError (sin procedencia) o
    PermissionError (cooldown vigente: la prisa no gobierna)."""
    actual = conn.execute(
        "SELECT * FROM buscador_parameters WHERE parametro = ?", (parametro,)
    ).fetchone()
    if actual is None:
        raise LookupError("Parámetro no gobernable.")
    if not (resolucion or "").strip():
        raise ValueError("Toda resolución cita su procedencia (T13).")
    ultima = conn.execute(
        "SELECT * FROM buscador_parameter_resolutions WHERE parametro = ? "
        "ORDER BY id DESC LIMIT 1",
        (parametro,),
    ).fetchone()
    if ultima is not None:
        try:
            edad = (datetime.now(timezone.utc) - datetime.fromisoformat(ultima["created_at"])).days
        except (TypeError, ValueError):
            edad = COOLDOWN_RESOLUCION_DIAS + 1
        if edad < COOLDOWN_RESOLUCION_DIAS:
            raise PermissionError(
                f"cooldown vigente: faltan {COOLDOWN_RESOLUCION_DIAS - edad} días (anti-flip-flop)"
            )
    cursor = conn.execute(
        "INSERT INTO buscador_parameter_resolutions (parametro, valor, resolucion, created_at) "
        "VALUES (?, ?, ?, ?)",
        (parametro, (valor or "").strip(), resolucion.strip(), _now()),
    )
    conn.execute(
        "UPDATE buscador_parameters SET valor = ?, procedencia = ?, updated_at = ? WHERE parametro = ?",
        ((valor or "").strip(), f"parlamento-B4#{cursor.lastrowid}", _now(), parametro),
    )
    conn.commit()
    return conn.execute(
        "SELECT * FROM buscador_parameter_resolutions WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()


def listar_resoluciones(conn, limite=50):
    """Historial vinculante del parlamento (lo resuelto, por orden)."""
    return conn.execute(
        "SELECT * FROM buscador_parameter_resolutions ORDER BY id DESC LIMIT ?",
        (max(1, limite),),
    ).fetchall()


def publicar_doc(conn, doc_id, licencia, nota=""):
    """Interruptor del curador (M15): publica un documento de la biblioteca
    con licencia explícita y nota de procedencia. Sin licencia no-closed no
    hay nivel 1: levanta ValueError. Solo cambia visibilidad + licencia (el
    texto completo jamás se sirve por API)."""
    fila = conn.execute("SELECT * FROM buscador_docs WHERE id = ?", (doc_id,)).fetchone()
    if fila is None:
        raise LookupError("Documento no encontrado.")
    lic = (licencia or "").strip() or "closed"
    if lic.lower() == "closed":
        raise ValueError("Sin licencia explícita no hay nivel 1 (fail-closed).")
    curaduria = (fila["curaduria"] or "").strip()
    if (nota or "").strip():
        curaduria = (curaduria + "\n" if curaduria else "") + f"[Publicado: {nota.strip()} — {_now()}]"
    conn.execute(
        "UPDATE buscador_docs SET licencia = ?, visibilidad = 'publica', curaduria = ? WHERE id = ?",
        (lic, curaduria, doc_id),
    )
    conn.commit()
    return conn.execute("SELECT * FROM buscador_docs WHERE id = ?", (doc_id,)).fetchone()


# --------------------------------------------------------------------------
# Búsqueda unificada (fusión de capas con transparencia)
# --------------------------------------------------------------------------

def buscar(conn, query):
    """Fusiona las capas con transparencia total.

    Orden canónico (la memoria propia manda, §5.3; la referencia general
    sigue, la academia después, la web al fondo):

    1. semillas (bloque garantizado) · 2. corpus · 3. referencia (Wikipedia
    y hermanas) · 4. académica (Zenodo + OpenAlex) · 5. web (SearXNG).

    Todo resultado lleva banda + razones (P3/P4); un motor caído NO rompe
    nada: se lista en ``motores_fail_open``.
    """

    ORDEN = ("semillas", "corpus", "referencia", "academica", "web")
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
                veredicto = mejor_score(conn, u)  # B4: Nivel 2 vigente refina
                r["banda"] = veredicto["banda"]
                r["razones"] = veredicto["razones"]
                r["motor_score"] = veredicto["motor"]
                r["nivel_score"] = veredicto["nivel"]
            resultados.append(r)
            por_capa[r["capa"]] = por_capa.get(r["capa"], 0) + 1

    _agregar(engine_semasillas(conn, query))

    try:
        _agregar(engine_corpus(conn, query))
    except Exception as exc:  # el corpus es local: si falla, se reporta
        fail_open.append(f"corpus: {exc.__class__.__name__}")

    for motor, nombre in (
        (engine_wikipedia, "wikipedia"),
        (engine_wikibooks, "wikibooks"),
        (engine_wikiversity, "wikiversidad"),
    ):
        try:
            _agregar(motor(query))
        except Exception as exc:  # fail-open: la búsqueda sigue sin la hermana
            fail_open.append(f"{nombre}: {exc.__class__.__name__}")

    try:
        _agregar(engine_zenodo(query))
    except Exception as exc:  # fail-open: la búsqueda sigue sin Zenodo
        fail_open.append(f"zenodo: {exc.__class__.__name__}")

    try:
        _agregar(engine_openalex(query))
    except Exception as exc:  # fail-open: la búsqueda sigue sin OpenAlex
        fail_open.append(f"openalex: {exc.__class__.__name__}")

    try:
        _agregar(engine_searxng(query))
    except Exception as exc:  # fail-open: la búsqueda sigue sin SearXNG
        fail_open.append(f"searxng: {exc.__class__.__name__}")

    for r in resultados:  # B3: el corpus aporta sus razones propias (local)
        if r.get("capa") == "corpus":
            try:
                enriquecer_corpus(conn, r)
            except Exception as exc:
                fail_open.append(f"corpus-enriquecer: {exc.__class__.__name__}")

    return {
        "query": query,
        "resultados": resultados,
        "por_capa": por_capa,
        "orden_capas": list(ORDEN),
        "motores_fail_open": fail_open,
        "principios": (
            "etiqueta-no-censura: ningún resultado se oculta; las bandas "
            "explican la procedencia (P3/P4). Sin ads, sin tracking (P1)."
        ),
    }


def format_searx(data):
    """Formato compatible con el motor ``json_engine`` de SearXNG: así la
    lente educativa de cualquier instancia puede federar nuestras semillas.

    Lo privado NUNCA se federa: solo cruza lo publicado por el curador
    (visibilidad publica + licencia no closed). Opacidad Sagrada, Cap. 16.5."""
    return {
        "results": [
            {"title": r["titulo"], "url": r["url"], "content": r["resumen"]}
            for r in data.get("resultados", [])
            if not (r.get("fuente") == "biblioteca privada"
                    and r.get("visibilidad", "privada") != "publica")
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
