# -*- coding: utf-8 -*-
"""Tests del respaldo nocturno (scripts/respaldo_comun.py)."""

import sqlite3

import scripts.respaldo_comun as respaldo


def _sembrar(path):
    with sqlite3.connect(str(path)) as conn:
        conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT)")
        conn.execute("INSERT INTO t (v) VALUES ('memoria')")
        conn.commit()


def test_respaldo_copia_y_poda(tmp_path, monkeypatch):
    origen = tmp_path / "comun.db"
    _sembrar(origen)
    destino = tmp_path / "respaldos"
    monkeypatch.setattr(respaldo, "ORIGENES", {"comun": origen})
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


def test_respaldo_dos_origenes(tmp_path, monkeypatch):
    comun = tmp_path / "comun.db"
    edu = tmp_path / "edu.db"
    _sembrar(comun)
    _sembrar(edu)
    destino = tmp_path / "respaldos"
    monkeypatch.setattr(respaldo, "ORIGENES", {"comun": comun, "edu": edu})
    monkeypatch.setattr(respaldo, "DESTINO_DIR", destino)

    assert respaldo.main() == 0

    assert len(list(destino.glob("comun-*.db"))) == 1
    assert len(list(destino.glob("edu-*.db"))) == 1


def test_respaldo_sin_origen_no_falla(tmp_path, monkeypatch):
    monkeypatch.setattr(respaldo, "ORIGENES", {"comun": tmp_path / "no-existe.db"})
    monkeypatch.setattr(respaldo, "DESTINO_DIR", tmp_path / "respaldos")
    assert respaldo.main() == 0
