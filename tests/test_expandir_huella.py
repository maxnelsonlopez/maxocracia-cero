# -*- coding: utf-8 -*-
"""Tests de la Capa 3: el archivo responde (hito 6, 09-10-2026).

La prueba de fuego del "nada se pierde": la prosa DeepSeek que el ledger
comprimió debe recuperarse íntegra desde el tag de archivo.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import expandir_huella as c3

TAG = "corpus/registro-pre-ledger-20261009"
REGISTRO = "docs/architecture/atribuciones_sinteticas.md"


def test_el_tag_de_archivo_resuelve():
    assert c3.huella_resuelve(TAG) is True


def test_huella_inexistente_no_resuelve():
    assert c3.huella_resuelve("corpus/no-existe-00000000") is False
    assert c3.huella_resuelve("") is False
    assert c3.expandir("corpus/no-existe-00000000", archivo=REGISTRO) == ""


def test_el_archivo_recupera_la_prosa_destilada():
    """Lo que el ledger comprimió, el tag lo devuelve: nada se perdió."""
    texto = c3.expandir(TAG, archivo=REGISTRO, max_lineas=10_000)
    assert "el puente constructor" in texto
    # prosa vieja que ya NO está en el archivo vivo, pero sí en el tag
    assert "oráculo en vivo como motor de negociación" in texto
    vivo = (REPO / REGISTRO).read_text(encoding="utf-8")
    assert "oráculo en vivo como motor de negociación" not in vivo


def test_expandir_acota_con_aviso():
    texto = c3.expandir(TAG, archivo=REGISTRO, max_lineas=5)
    assert len(texto.splitlines()) <= 7  # 5 + aviso
    assert "líneas más" in texto


def test_el_comando_sale_cero_con_huella_buena(capsys):
    assert c3.main([TAG, "--archivo", REGISTRO, "--lineas", "70"]) == 0
    assert "puente constructor" in capsys.readouterr().out


def test_el_comando_sale_uno_con_huella_mala(capsys):
    assert c3.main(["corpus/no-existe-00000000"]) == 1
    assert "no resuelve" in capsys.readouterr().out
