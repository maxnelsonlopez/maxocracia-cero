# -*- coding: utf-8 -*-
"""B7 Biblioteca privada: ingiere archivos PROPIOS al corpus local (solo fragmentos visibles).

Formatos: .pdf (requiere pypdf) + texto plano (.txt, .md, .markdown, sin
dependencias). Recursivo por subcarpetas.

Uso (desde la raíz del repo)::

    $env:BIBLIOTECA_PDF_DIR = "E:\\libros"
    .venv\\Scripts\\python.exe plataforma_educativa/ingest_biblioteca.py

Reglas de la casa (duras):

- Solo archivos propios y SIN DRM: un PDF cifrado se OMITE y se reporta;
  jamás se vulnera (la cerradura ajena no se fuerza).
- Idempotente por hash de contenido: repetir no duplica; re-ingerir actualiza.
- Lo no indexable se REPORTA (nada se ignora en silencio).
- La API solo sirve FRAGMENTOS de estos libros (snippet FTS5 o recorte):
  el texto completo nunca sale del disco del dueño (Verbo Justo + M15).
- La base del dueño no se commitea (``plataforma_educativa.db`` está en
  ``.gitignore``); el disco externo nunca se copia al repo.
"""

import hashlib
import os
import sqlite3
import sys
from datetime import datetime, timezone

_PLATFORM_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.environ.get(
    "PLATAFORMA_EDUCATIVA_DB", os.path.join(_PLATFORM_ROOT, "plataforma_educativa.db")
)

MAX_TEXTO = 200_000  # tope por libro: la biblioteca cabe en casa
MIN_TEXTO = 50  # menos que esto suele ser escaneo sin OCR (se reporta)


class PDFCifrado(Exception):
    """El PDF tiene cerradura: se omite, no se fuerza."""


def _ahora():
    return datetime.now(timezone.utc).isoformat()


def extrae_pdf(ruta):
    """Extrae (titulo, autor, paginas, texto) o levanta PDFCifrado/ValueError."""
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ValueError("Falta pypdf: pip install -r plataforma_educativa/requirements.txt")
    lector = PdfReader(ruta)
    if lector.is_encrypted:
        raise PDFCifrado(os.path.basename(ruta))
    textos = []
    for pagina in lector.pages:
        try:
            textos.append(pagina.extract_text() or "")
        except Exception:
            textos.append("")
    texto = "\n".join(textos)
    texto = " ".join(texto.split())
    meta = lector.metadata or {}
    titulo = (meta.get("/Title") or "").strip() or None
    autor = (meta.get("/Author") or "").strip() or None
    return titulo, autor, len(lector.pages), texto


EXTENSIONES = {".pdf", ".txt", ".md", ".markdown"}


def lee_plano(ruta):
    """Texto plano (utf-8 tolerante): sin dependencias, sin DRM posible."""
    with open(ruta, encoding="utf-8", errors="replace") as fh:
        texto = " ".join(fh.read().split())
    return None, None, None, texto


def lee_catalogo(pdf_dir):
    """Catálogo del curador (``catalogo.json`` junto a los libros): licencia,
    visibilidad y curaduría por ruta relativa. Si falta o está roto, todo
    nace closed + privada (fail-closed: sin licencia no hay nivel 1)."""
    import json

    try:
        with open(os.path.join(pdf_dir, "catalogo.json"), encoding="utf-8") as fh:
            datos = json.load(fh)
        return {i["ruta_relativa"]: i for i in datos.get("items", []) if i.get("ruta_relativa")}
    except (OSError, ValueError):
        return {}


def ingest_biblioteca(db_path=None, pdf_dir=None, limite_texto=MAX_TEXTO):
    """Ingiere los archivos indexables de ``pdf_dir`` a ``buscador_docs``
    (capa biblioteca). Recursivo. Lee el catálogo del curador para licencia,
    visibilidad, curaduría y categoría. Devuelve el reporte
    ``{ingeridos, actualizados, omitidos:[{archivo, motivo}]}``."""
    db_path = db_path or DEFAULT_DB_PATH
    pdf_dir = pdf_dir or os.environ.get("BIBLIOTECA_PDF_DIR", "")
    if not pdf_dir or not os.path.isdir(pdf_dir):
        raise ValueError("Fija BIBLIOTECA_PDF_DIR a una carpeta existente (tu disco).")
    catalogo = lee_catalogo(pdf_dir)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    reporte = {"ingeridos": 0, "actualizados": 0, "omitidos": []}
    for raiz, _dirs, archivos in os.walk(pdf_dir):
        for nombre in sorted(archivos):
            if nombre == "catalogo.json":
                continue
            ruta = os.path.join(raiz, nombre)
            rel = os.path.relpath(ruta, pdf_dir).replace(os.sep, "/")
            ext = os.path.splitext(nombre)[1].lower()
            try:
                if ext not in EXTENSIONES:
                    raise ValueError(f"formato no indexable ({ext or 'sin extensión'}: pdf/txt/md)")
                with open(ruta, "rb") as fh:
                    crudo = fh.read()
                if not crudo:
                    raise ValueError("vacío")
                if ext == ".pdf":
                    titulo, autor, paginas, texto = extrae_pdf(ruta)
                    tipo, detalle = "libro", f"{autor or 'autor en el archivo'} — {paginas} pág."
                else:
                    titulo, autor, _pags, texto = lee_plano(ruta)
                    tipo, detalle = "texto", "texto plano"
                if len(texto) < MIN_TEXTO:
                    raise ValueError("sin texto extraíble (¿escaneo sin OCR?)")
                url = "biblioteca-privada:" + hashlib.sha256(crudo).hexdigest()[:24]
                titulo = titulo or os.path.splitext(nombre)[0]
                resumen = f"📚 Biblioteca privada: {detalle}"
                entrada = catalogo.get(rel, {})
                licencia = (entrada.get("licencia") or "closed").strip() or "closed"
                visibilidad = (entrada.get("visibilidad") or "privada").strip()
                if visibilidad not in ("privada", "publica"):
                    visibilidad = "privada"
                curaduria = (entrada.get("curaduria") or "").strip()
                categoria = (entrada.get("categoria") or rel.split("/")[0] if "/" in rel else "").strip()
                existe = conn.execute(
                    "SELECT id FROM buscador_docs WHERE url = ?", (url,)
                ).fetchone()
                conn.execute(
                    "INSERT INTO buscador_docs "
                    "(url, capa, titulo, resumen, texto, idioma, tipo, indexed_at, "
                    " licencia, visibilidad, curaduria, categoria) "
                    "VALUES (?, 'biblioteca', ?, ?, ?, 'es', ?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(url) DO UPDATE SET "
                    "titulo = excluded.titulo, resumen = excluded.resumen, "
                    "texto = excluded.texto, indexed_at = excluded.indexed_at, "
                    "licencia = excluded.licencia, visibilidad = excluded.visibilidad, "
                    "curaduria = excluded.curaduria, categoria = excluded.categoria",
                    (url, titulo, resumen, texto[:limite_texto], tipo, _ahora(),
                     licencia, visibilidad, curaduria, categoria),
                )
                if existe:
                    reporte["actualizados"] += 1
                else:
                    reporte["ingeridos"] += 1
            except PDFCifrado:
                reporte["omitidos"].append({"archivo": nombre, "motivo": "cifrado (no se fuerza)"})
            except Exception as exc:
                reporte["omitidos"].append({"archivo": nombre, "motivo": str(exc)[:80]})
    conn.commit()
    conn.close()
    return reporte


ingest_pdfs = ingest_biblioteca  # alias heredado (B7 inicial)


def main(argv):
    pdf_dir = argv[0] if argv else None
    try:
        reporte = ingest_biblioteca(pdf_dir=pdf_dir)
    except ValueError as exc:
        print(f"ingest_biblioteca: {exc}")
        return 1
    print(f"ingeridos={reporte['ingeridos']} actualizados={reporte['actualizados']} "
          f"omitidos={len(reporte['omitidos'])}")
    for om in reporte["omitidos"]:
        print(f"  - {om['archivo']}: {om['motivo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
