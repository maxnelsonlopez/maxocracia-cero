# -*- coding: utf-8 -*-
"""Tests del respaldo nocturno (scripts/respaldo_comun.py)."""

import sqlite3

import scripts.respaldo_comun as respaldo


def test_respaldo_copia_y_poda(tmp_path, monkeypatch):
    origen = tmp_path / "comun.db"
    with sqlite3.connect(str(origen)) as conn:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("INSERT INTO t (v) VALUES ('memoria')")
        conn.commit()
    destino = tmp_path / "respaldos"
    monkeypatch.setattr(respaldo, "ORIGEN", origen)
    monkeypatch.setattr(respaldo, "DESTINO_DIR", destino)
    monkeypatch.setattr(respaldo, "DIAS", 14)

    vieja = destino / "comun-2000-01-01.db"
    vieja.parent.mkdir(parents=True, exist_ok=True)
    vieja.write_bytes(b"vieja")

    assert respaldo.main() == 0

    copias = sorted(p.name for p in destino.glob("comun-*.db"))
    assert len(copias) == 1  # la vieja se podó, la de hoy quedó
    with sqlite3.connect(str(destino / copias[0])) as conn:
        assert conn.execute("SELECT v FROM t").fetchone()[0] == "memoria"


def test_respaldo_sin_origen_no_falla(tmp_path, monkeypatch):
    monkeypatch.setattr(respaldo, "ORIGEN", tmp_path / "no-existe.db")
    monkeypatch.setattr(respaldo, "DESTINO_DIR", tmp_path / "respaldos")
    assert respaldo.main() == 0
