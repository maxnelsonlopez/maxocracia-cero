# -*- coding: utf-8 -*-
"""Tests de la Biblioteca privada (B7): ingestor PDF + fragmentos sin filtrar.

Regla de la casa: tests SIN red (aquí ni siquiera hay red: todo es disco
temporal). Los PDF de prueba se construyen en memoria: uno mínimo válido
con xref real y uno cifrado con PdfWriter.
"""

import io
import os
import sqlite3

import pytest

import ingest_pdfs
from app import buscador, create_app


def pdf_minimo(texto):
    """Un PDF válido de una página con xref real (suficiente para pypdf)."""
    contenido = b"BT /F1 18 Tf 50 100 Td (" + texto.encode("latin-1") + b") Tj ET"
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(contenido)).encode() + b" >> stream\n" + contenido + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    pdf = b"%PDF-1.4\n"
    offsets = []
    for i, cuerpo in enumerate(objs, start=1):
        offsets.append(len(pdf))
        pdf += str(i).encode() + b" 0 obj\n" + cuerpo + b"\nendobj\n"
    x = len(pdf)
    pdf += b"xref\n0 " + str(len(objs) + 1).encode() + b"\n"
    pdf += b"0000000000 65535 f \n"
    for o in offsets:
        pdf += str(o).encode().zfill(10) + b" 00000 n \n"
    pdf += (b"trailer << /Size " + str(len(objs) + 1).encode() + b" /Root 1 0 R >>\n"
            b"startxref\n" + str(x).encode() + b"\n%%EOF\n")
    return pdf


def pdf_cifrado():
    from pypdf import PdfWriter

    w = PdfWriter()
    w.add_blank_page(100, 100)
    w.encrypt("secreto")
    buf = io.BytesIO()
    w.write(buf)
    return buf.getvalue()


@pytest.fixture()
def biblioteca(tmp_path):
    d = tmp_path / "libros"
    d.mkdir()
    (d / "fotosintesis.pdf").write_bytes(pdf_minimo("La fotosintesis es vida y luz. " * 60))
    (d / "cerrado.pdf").write_bytes(pdf_cifrado())
    (d / "roto.pdf").write_bytes(b"esto no es un pdf")
    (d / "notas.txt").write_text("no es pdf, se ignora")
    return str(d)


def test_ingiere_valido_omite_resto(app, biblioteca):
    reporte = ingest_pdfs.ingest_pdfs(db_path=app.config["DATABASE"], pdf_dir=biblioteca)
    assert reporte["ingeridos"] == 1 and reporte["actualizados"] == 0
    motivos = {o["archivo"]: o["motivo"] for o in reporte["omitidos"]}
    assert "cifrado" in motivos["cerrado.pdf"]  # la cerradura no se fuerza
    assert "roto.pdf" in motivos

    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    fila = conn.execute("SELECT * FROM buscador_docs WHERE capa = 'biblioteca'").fetchone()
    conn.close()
    assert fila["tipo"] == "libro" and fila["titulo"] == "fotosintesis"
    assert fila["url"].startswith("biblioteca-privada:")


def test_idempotente_por_contenido(app, biblioteca):
    ingest_pdfs.ingest_pdfs(db_path=app.config["DATABASE"], pdf_dir=biblioteca)
    reporte = ingest_pdfs.ingest_pdfs(db_path=app.config["DATABASE"], pdf_dir=biblioteca)
    assert reporte == {"ingeridos": 0, "actualizados": 1, "omitidos": reporte["omitidos"]}
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    n = conn.execute("SELECT COUNT(*) AS n FROM buscador_docs WHERE capa = 'biblioteca'").fetchone()["n"]
    conn.close()
    assert n == 1


def test_sin_carpeta_falla_explicito(app, tmp_path):
    with pytest.raises(ValueError):
        ingest_pdfs.ingest_pdfs(db_path=app.config["DATABASE"], pdf_dir=str(tmp_path / "noexiste"))


def test_busqueda_muestra_fragmento_no_el_libro(app, client, biblioteca):
    ingest_pdfs.ingest_pdfs(db_path=app.config["DATABASE"], pdf_dir=biblioteca)
    data = client.get("/api/buscador/corpus?q=fotosintesis").get_json()
    doc = next(r for r in data["resultados"] if r["fuente"] == "biblioteca privada")
    assert "fotosintesis" in doc["resumen"].lower()
    assert len(doc["resumen"]) < 500  # fragmento, jamás el libro (60 repeticiones)
    assert doc["banda"] == "desconocida"  # privada = no verificable por otros (honesto)
    assert any("fragmentos" in z for z in doc["razones"])

    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    fila = conn.execute("SELECT * FROM buscador_docs WHERE capa = 'biblioteca'").fetchone()
    conn.close()
    assert len(fila["texto"]) > len(doc["resumen"]) * 5  # el texto vive en casa, no viaja
