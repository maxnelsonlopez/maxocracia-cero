# -*- coding: utf-8 -*-
"""Vigía de las plataformas — ojos del custodio cada mañana.

Revisa sin tocar: app (:5001), escuela (:5050), túnel (edge responde),
frescura del respaldo, último ciclo del Concilio y disco. Escribe
scratch/vigia/reporte-AAAA-MM-DD.md y sale 0 si todo respira, 1 si algo
pide manos. Lo corre la tarea programada VigiaDiaria (7:00 am); el oráculo
de sesión lo lee al despertar.
"""

import json
import shutil
import sqlite3
import time
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REPORTE_DIR = REPO / "scratch" / "vigia"
RESPALDOS_DIR = REPO / "scratch" / "respaldos"
CYCLES_DIR = REPO / "scratch" / "concilio" / "cycles"


def revisar_http(url: str, timeout: int = 15):
    """(ok, detalle): GET simple; 401 cuenta como viva (hay guardián)."""
    inicio = time.time()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return True, f"{r.status} en {time.time() - inicio:.1f}s"
    except Exception as e:
        codigo = getattr(e, "code", None)
        if codigo in (401, 403):
            return True, f"{codigo} (con guardián) en {time.time() - inicio:.1f}s"
        return False, f"{type(e).__name__}: {e}"[:160]


def antiguedad_respaldo(destino: Path) -> str:
    copias = sorted(destino.glob("*.db"))
    if not copias:
        return "SIN COPIAS"
    dias = (time.time() - copias[-1].stat().st_mtime) / 86400
    return f"{copias[-1].name} ({dias:.1f} días)"


def ultimo_ciclo(ciclos: Path) -> str:
    if not ciclos.exists():
        return "sin ciclos"
    carpetas = sorted((p for p in ciclos.iterdir() if p.is_dir()))
    if not carpetas:
        return "sin ciclos"
    ultima = carpetas[-1]
    try:
        meta = json.loads((ultima / "ciclo.json").read_text(encoding="utf-8"))
        consenso = meta.get("consensus", "?")
        estado = "EJECUTABLE" if meta.get("ejecutable") else "en cola"
    except (OSError, ValueError):
        consenso, estado = "?", "?"
    return f"{ultima.name} (consenso {consenso}, {estado})"


def main() -> int:
    lineas = [f"# Vigía — {date.today().isoformat()}", ""]
    fallos = 0

    for nombre, url in [
        ("plaza", "http://localhost:5001/"),
        ("escuela", "http://localhost:5050/"),
        ("túnel", "https://start.maxocracia.com/"),
    ]:
        ok, detalle = revisar_http(url)
        lineas.append(f"- {nombre}: {'OK' if ok else 'CAÍDO'} — {detalle}")
        fallos += 0 if ok else 1

    lineas.append(f"- respaldo: {antiguedad_respaldo(RESPALDOS_DIR)}")
    lineas.append(f"- concilio: {ultimo_ciclo(CYCLES_DIR)}")
    libre_gb = shutil.disk_usage(str(REPO)).free / 1e9
    lineas.append(f"- disco libre: {libre_gb:.1f} GB")
    try:
        usuarios = (
            sqlite3.connect(str(REPO / "comun.db"))
            .execute("SELECT COUNT(*) FROM users")
            .fetchone()[0]
        )
        lineas.append(f"- almas en la plaza: {usuarios}")
    except Exception as e:  # la plaza manda; el vigía solo mira
        lineas.append(f"- almas: no se pudo contar ({e})")
        fallos += 1

    REPORTE_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTE_DIR / f"reporte-{date.today().isoformat()}.md").write_text(
        "\n".join(lineas) + "\n", encoding="utf-8"
    )
    print("\n".join(lineas))
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
