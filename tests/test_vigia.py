# -*- coding: utf-8 -*-
"""Tests del vigía (scripts/vigia_plataformas.py). Sin red: solo disco y texto."""

import scripts.vigia_plataformas as vigia


def test_antiguedad_respaldo(tmp_path):
    assert vigia.antiguedad_respaldo(tmp_path) == "SIN COPIAS"
    copia = tmp_path / "comun-2000-01-01.db"
    copia.write_bytes(b"x")
    assert "comun-2000-01-01.db" in vigia.antiguedad_respaldo(tmp_path)


def test_ultimo_ciclo(tmp_path):
    assert vigia.ultimo_ciclo(tmp_path / "no-existe") == "sin ciclos"
    d = tmp_path / "cycles" / "ciclo-20260925-120552-aaa"
    d.mkdir(parents=True)
    (d / "ciclo.json").write_text(
        '{"consensus": 1.0, "ejecutable": true}', encoding="utf-8"
    )
    texto = vigia.ultimo_ciclo(tmp_path / "cycles")
    assert "ciclo-20260925-120552-aaa" in texto
    assert "EJECUTABLE" in texto


def test_revisar_http_cuenta_401_como_viva(tmp_path):
    # 401/403 = hay guardián respondiendo: la plataforma vive.
    ok, detalle = vigia.revisar_http("http://localhost:9/")
    assert ok is False
    assert detalle
