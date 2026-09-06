# -*- coding: utf-8 -*-
"""La Lupa de la ciudad (B6) — el meta-panorama de un artículo de referencia.

El canon manda (repaso de los caps. 1-4, Edición 3 Dinámica):

- **Ojo Claro (Axioma 5, Cap. 2)**: separar el HECHO (qué cambió, quién,
  cuándo, cuánto) de la INTERPRETACIÓN (por qué, con qué intención). La lupa
  muestra lo primero; lo segundo lo juzgan ojos humanos (M15), jamás la máquina.
- **Verbo Justo (Axioma 6, Cap. 2)**: ni más ni menos que toda la verdad
  necesaria — el diff palabra por palabra, sin recortes convenientes.
- **Protocolo de Disenso (T15, Cap. 3)**: el consenso total es sospechoso. La
  versión estable de un artículo es un consenso que merece lupa: la lupa es el
  disidente permanente del relato.
- **Sistema inmune cultural (Cap. 1 §1.3)**: distinguir qué ideas integrar y
  cuáles rechazar. La lupa es ese sistema inmune hecho código.
- **Accesibilidad del valor (Principio Sexto, Cap. 4)**: si unos pocos editores
  coordinados saben más del artículo que quien lo lee, no hay lectura libre.
  La lupa reduce esa asimetría.

Todo con la librería estándar y las APIs públicas de Wikimedia (sin clave):
historial de revisiones + contenido de revisiones. ``difflib`` (stdlib) hace
el diff de palabras en casa — el wikitexto nunca sale a terceros.
"""

import collections
import difflib
import re
import urllib.parse

from . import buscador

WIKI_API = "https://es.wikipedia.org/w/api.php"

# Indicios de reversión en el resumen de edición (es + en). Heurística
# documentada: cuenta como "revertida", no como veredicto (Ojo Claro).
_PATRON_REVERSION = re.compile(
    r"revert|deshech|deshac|revierte|vandalismo|deshacer", re.IGNORECASE
)
# Editor anónimo: IP clásica o cuenta temporal (~2026-...).
_PATRON_ANONIMO = re.compile(r"^(\d{1,3}\.\d{1,3}\.|[0-9a-f]*:|~)")


def titulo_desde_url(url):
    """Extrae el título canónico de una URL de Wikipedia en español."""
    u = (url or "").strip()
    if "/wiki/" not in u:
        return ""
    titulo = u.split("/wiki/", 1)[1].split("#")[0].split("?")[0]
    return urllib.parse.unquote(titulo).replace("_", " ").strip()


def _es_anonimo(usuario):
    return bool(_PATRON_ANONIMO.match(usuario or ""))


def _es_bot(usuario):
    return (usuario or "").lower().endswith("bot")


def panorama(titulo, limite=50):
    """Meta-panorama del artículo: protección, muestra de revisiones y
    señales agregadas (reversiones, anonimato, concentración, saltos de
    tamaño). Todo son HECHOS contados; la lectura es humana (Ojo Claro)."""
    t = (titulo or "").strip()
    if not t:
        raise ValueError("Falta el título del artículo.")
    url = WIKI_API + "?" + urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "revisions|info",
            "titles": t,
            "rvlimit": max(1, min(int(limite or 50), 100)),
            "rvprop": "ids|timestamp|user|comment|size|flags",
            "inprop": "protection",
            "format": "json",
            "formatversion": "2",
        }
    )
    data = buscador._http_get_json(url) or {}
    paginas = (data.get("query") or {}).get("pages") or []
    if not paginas or paginas[0].get("missing"):
        raise LookupError("Artículo no encontrado.")
    pagina = paginas[0]
    revs = pagina.get("revisions") or []

    revisiones = [
        {
            "revid": r.get("id"),
            "fecha": r.get("timestamp"),
            "usuario": r.get("user") or "",
            "resumen": r.get("comment") or "",
            "tamano": r.get("size") or 0,
            "reversion": bool(_PATRON_REVERSION.search(r.get("comment") or "")),
            "anonimo": _es_anonimo(r.get("user")),
        }
        for r in revs
    ]
    n = len(revisiones)
    revertidas = sum(1 for r in revisiones if r["reversion"])
    anonimas = sum(1 for r in revisiones if r["anonimo"])
    por_editor = collections.Counter(r["usuario"] for r in revisiones)
    saltos = []
    for vieja, nueva in zip(revisiones[1:], revisiones[:-1]):
        delta = (nueva["tamano"] or 0) - (vieja["tamano"] or 0)
        if abs(delta) >= 1000:
            saltos.append(
                {"de": vieja["revid"], "a": nueva["revid"], "delta": delta,
                 "fecha": nueva["fecha"], "usuario": nueva["usuario"]}
            )
    return {
        "titulo": pagina.get("title") or t,
        "proteccion": [
            {"tipo": p.get("type"), "nivel": p.get("level")}
            for p in pagina.get("protection") or []
            if p.get("level") and p.get("level") != "all"
        ],
        "muestra": n,
        "primera_vista": revisiones[-1]["fecha"] if revisiones else None,
        "ultima_vista": revisiones[0]["fecha"] if revisiones else None,
        "revertidas": revertidas,
        "anonimas": anonimas,
        "proporcion_reversiones": round(revertidas / n, 3) if n else 0,
        "indicios_guerra": n >= 10 and (revertidas / n) >= 0.3,
        "top_editores": [
            {"usuario": u, "ediciones": c, "bot": _es_bot(u)}
            for u, c in por_editor.most_common(5)
        ],
        "saltos_tamano": saltos[:10],
        "revisiones": [
            {k: r[k] for k in ("revid", "fecha", "usuario", "resumen", "tamano", "reversion", "anonimo")}
            for r in revisiones
        ],
    }


def contenido_revision(revid):
    """Wikitexto completo de una revisión (para el diff local)."""
    try:
        rid = int(revid)
    except (TypeError, ValueError):
        raise ValueError("revid inválido.")
    url = WIKI_API + "?" + urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "revisions",
            "revids": rid,
            "rvprop": "content",
            "rvslots": "main",
            "format": "json",
            "formatversion": "2",
        }
    )
    data = buscador._http_get_json(url) or {}
    paginas = (data.get("query") or {}).get("pages") or []
    if not paginas or not (paginas[0].get("revisions") or []):
        raise LookupError("Revisión no encontrada.")
    return paginas[0]["revisions"][0]["slots"]["main"]["content"] or ""


def diff_palabras(viejo, nuevo, max_fragmentos=60, max_largo=280):
    """Diff palabra por palabra (difflib, local): lo quitado y lo puesto,
    en fragmentos legibles. Verbo Justo: se muestra TODO lo que cambió
    (hasta el tope, avisando el total real)."""
    a, b = (viejo or "").split(), (nuevo or "").split()
    comparador = difflib.SequenceMatcher(None, a, b, autojunk=False)
    quitadas, puestas = [], []
    n_quitadas = n_puestas = 0
    for etiqueta, i1, i2, j1, j2 in comparador.get_opcodes():
        if etiqueta == "delete":
            n_quitadas += i2 - i1
            if len(quitadas) < max_fragmentos:
                quitadas.append(" ".join(a[i1:i2])[:max_largo])
        elif etiqueta == "insert":
            n_puestas += j2 - j1
            if len(puestas) < max_fragmentos:
                puestas.append(" ".join(b[j1:j2])[:max_largo])
        elif etiqueta == "replace":
            n_quitadas += i2 - i1
            n_puestas += j2 - j1
            if len(quitadas) < max_fragmentos:
                quitadas.append(" ".join(a[i1:i2])[:max_largo])
            if len(puestas) < max_fragmentos:
                puestas.append(" ".join(b[j1:j2])[:max_largo])
    return {
        "quitadas": quitadas,
        "puestas": puestas,
        "n_quitadas_total": n_quitadas,
        "n_puestas_total": n_puestas,
        "truncado": len(quitadas) == max_fragmentos or len(puestas) == max_fragmentos,
    }


def comparar(de_revid, a_revid):
    """Compara dos revisiones: trae ambos textos y difiere en casa."""
    viejo = contenido_revision(de_revid)
    nuevo = contenido_revision(a_revid)
    resultado = diff_palabras(viejo, nuevo)
    resultado["de"] = int(de_revid)
    resultado["a"] = int(a_revid)
    return resultado
