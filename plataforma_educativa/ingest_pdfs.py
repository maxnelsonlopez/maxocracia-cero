# -*- coding: utf-8 -*-
"""B7 Biblioteca privada: ingiere PDFs PROPIOS al corpus local (solo fragmentos visibles).

Uso (desde la raíz del repo)::

    $env:BIBLIOTECA_PDF_DIR = "E:\\libros"
    .venv\\Scripts\\python.exe plataforma_educativa/ingest_pdfs.py

Reglas de la casa (duras):

- Solo archivos propios y SIN DRM: un PDF cifrado se OMITE y se reporta;
  jamás se vulnera (la cerradura ajena no se fuerza).
- Idempotente por hash de contenido: repetir no duplica; re-ingerir actualiza.
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


def ingest_pdfs(db_path=None, pdf_dir=None, limite_texto=MAX_TEXTO):
    """Ingiere los .pdf de ``pdf_dir`` a ``buscador_docs`` (capa biblioteca).
    Devuelve el reporte ``{ingeridos, actualizados, omitidos:[{archivo, motivo}]}``."""
    db_path = db_path or DEFAULT_DB_PATH
    pdf_dir = pdf_dir or os.environ.get("BIBLIOTECA_PDF_DIR", "")
    if not pdf_dir or not os.path.isdir(pdf_dir):
        raise ValueError("Fija BIBLIOTECA_PDF_DIR a una carpeta existente (tu disco).")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    reporte = {"ingeridos": 0, "actualizados": 0, "omitidos": []}
    for raiz, _dirs, archivos in os.walk(pdf_dir):
        for nombre in sorted(archivos):
            if not nombre.lower().endswith(".pdf"):
                continue
            ruta = os.path.join(raiz, nombre)
            try:
                with open(ruta, "rb") as fh:
                    crudo = fh.read()
                if not crudo:
                    raise ValueError("vacío")
                titulo, autor, paginas, texto = extrae_pdf(ruta)
                if len(texto) < MIN_TEXTO:
                    raise ValueError("sin texto extraíble (¿escaneo sin OCR?)")
                url = "biblioteca-privada:" + hashlib.sha256(crudo).hexdigest()[:24]
                titulo = titulo or os.path.splitext(nombre)[0]
                resumen = "📚 Biblioteca privada: {} — {} pág.".format(
                    autor or "autor en el archivo", paginas
                )
                existe = conn.execute(
                    "SELECT id FROM buscador_docs WHERE url = ?", (url,)
                ).fetchone()
                conn.execute(
                    "INSERT INTO buscador_docs "
                    "(url, capa, titulo, resumen, texto, idioma, tipo, indexed_at) "
                    "VALUES (?, 'biblioteca', ?, ?, ?, 'es', 'libro', ?) "
                    "ON CONFLICT(url) DO UPDATE SET "
                    "titulo = excluded.titulo, resumen = excluded.resumen, "
                    "texto = excluded.texto, indexed_at = excluded.indexed_at",
                    (url, titulo, resumen, texto[:limite_texto], _ahora()),
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


def main(argv):
    pdf_dir = argv[0] if argv else None
    try:
        reporte = ingest_pdfs(pdf_dir=pdf_dir)
    except ValueError as exc:
        print(f"ingest_pdfs: {exc}")
        return 1
    print(f"ingeridos={reporte['ingeridos']} actualizados={reporte['actualizados']} "
          f"omitidos={len(reporte['omitidos'])}")
    for om in reporte["omitidos"]:
        print(f"  - {om['archivo']}: {om['motivo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
