# -*- coding: utf-8 -*-
"""Respaldo nocturno de las memorias — la plaza no se improvisa.

Copia en caliente con la API de backup de SQLite (segura con los servidores
arriba) a scratch/respaldos/ y poda a 14 días:
- comun.db (Maxocracia) -> comun-AAAA-MM-DD.db
- plataforma_educativa/plataforma_educativa.db (escuela) -> edu-AAAA-MM-DD.db
Lo corre la tarea programada MaxocraciaRespaldo (3:00 am).
"""

import sqlite3
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ORIGENES = {
    "comun": REPO / "comun.db",
    "edu": REPO / "plataforma_educativa" / "plataforma_educativa.db",
}
DESTINO_DIR = REPO / "scratch" / "respaldos"
DIAS = 14


def _respaldar(nombre: str, origen: Path, hoy: date) -> None:
    destino = DESTINO_DIR / f"{nombre}-{hoy.isoformat()}.db"
    with sqlite3.connect(str(origen)) as src, sqlite3.connect(str(destino)) as dst:
        src.backup(dst)
    print(f"[respaldo] OK {destino.name}")


def main() -> int:
    DESTINO_DIR.mkdir(parents=True, exist_ok=True)
    hoy = date.today()
    hechas = 0
    for nombre, origen in ORIGENES.items():
        if not origen.exists():
            print(f"[respaldo] sin origen: {origen} (nada que copiar)")
            continue
        _respaldar(nombre, origen, hoy)
        hechas += 1
    limite = hoy - timedelta(days=DIAS)
    for copia in DESTINO_DIR.glob("*.db"):
        try:
            fecha = date.fromisoformat("-".join(copia.stem.split("-")[-3:]))
        except ValueError:
            continue
        if fecha < limite:
            copia.unlink()
    copias = sorted(p.name for p in DESTINO_DIR.glob("*.db"))
    print(f"[respaldo] {hechas} copias ({len(copias)} guardadas, poda a {DIAS}d)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
