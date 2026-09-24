# -*- coding: utf-8 -*-
"""Respaldo nocturno de comun.db — la memoria de la plaza no se improvisa.

Copia en caliente con la API de backup de SQLite (segura con el servidor
arriba) a scratch/respaldos/comun-AAAA-MM-DD.db y poda a 14 días.
Lo corre la tarea programada MaxocraciaRespaldo (3:00 am).
"""

import sqlite3
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ORIGEN = REPO / "comun.db"
DESTINO_DIR = REPO / "scratch" / "respaldos"
DIAS = 14


def main() -> int:
    if not ORIGEN.exists():
        print(f"[respaldo] sin origen: {ORIGEN} (nada que copiar)")
        return 0
    DESTINO_DIR.mkdir(parents=True, exist_ok=True)
    hoy = date.today()
    destino = DESTINO_DIR / f"comun-{hoy.isoformat()}.db"
    with sqlite3.connect(str(ORIGEN)) as src, sqlite3.connect(str(destino)) as dst:
        src.backup(dst)
    limite = hoy - timedelta(days=DIAS)
    for copia in DESTINO_DIR.glob("comun-*.db"):
        try:
            fecha = date.fromisoformat(copia.stem.replace("comun-", ""))
        except ValueError:
            continue
        if fecha < limite:
            copia.unlink()
    copias = sorted(p.name for p in DESTINO_DIR.glob("comun-*.db"))
    print(f"[respaldo] OK {destino.name} ({len(copias)} copias, poda a {DIAS}d)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
