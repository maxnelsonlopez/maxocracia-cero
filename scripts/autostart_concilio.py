# -*- coding: utf-8 -*-
r"""Arranque del Concilio con el PC — semilla de autonomía (decreto 09-09-2026).

Registrado como tarea de Windows al iniciar sesión (MaxocraciaConcilio):

    .venv\Scripts\python.exe scripts\instalar_arranque_concilio.py      # instalar
    .venv\Scripts\python.exe scripts\instalar_arranque_concilio.py --quitar

Reglas (autonomía con respeto):
1. Si el custodio pausó/detuvo (control.json) → no despierta.
2. Si el último ciclo tiene menos de `CONCILIO_AUTOSTART_GAP_HOURS` (12) →
   ya hay trabajo fresco; no repetir (los créditos de DeepSeek son del
   custodio, no un pozo sin fondo).
3. Lock: el propio ciclo rechaza dos concilios simultáneos.
4. Todo queda en bitácora/`autostart.log`; el historial de git sigue blindado.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKSPACE = REPO / "scratch" / "concilio"
CONTROL = WORKSPACE / "control.json"
LOCK = WORKSPACE / "concilio.lock"
CYCLES = WORKSPACE / "cycles"
PY = REPO / ".venv" / "Scripts" / "python.exe"


def _last_cycle_age_hours() -> float:
    if not CYCLES.exists():
        return 1e9
    ciclos = [p for p in CYCLES.iterdir() if p.is_dir()]
    if not ciclos:
        return 1e9
    latest = max(p.stat().st_mtime for p in ciclos)
    return (time.time() - latest) / 3600.0


def main() -> int:
    if not (REPO / ".git").exists():
        print("[concilio] no es un repo git; nada que hacer", file=sys.stderr)
        return 0
    # 1. El custodio manda: pausa/parada = silencio.
    if CONTROL.exists():
        try:
            estado = json.loads(CONTROL.read_text(encoding="utf-8")).get(
                "estado", "activo"
            )
        except (OSError, ValueError):
            estado = "activo"
        if estado != "activo":
            print(f"[concilio] custodio pausó ({estado}); no despierta")
            return 0
    # 2. Trabajo fresco: no gastar créditos en repetir.
    gap_h = float(os.environ.get("CONCILIO_AUTOSTART_GAP_HOURS", "12"))
    if _last_cycle_age_hours() < gap_h:
        print(f"[concilio] ciclo reciente (<{gap_h:g}h); no repite")
        return 0
    print(f"[concilio] despertando ({time.strftime('%Y-%m-%d %H:%M')})...")
    log = WORKSPACE / "autostart.log"
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as fh:
        fh.write(f"\n===== {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
        result = subprocess.run(
            [
                str(PY),
                "scripts/concilio.py",
                "ciclo",
                "--orden",
                "deepseek,nvidia,openrouter",
            ],
            cwd=REPO,
            stdout=fh,
            stderr=subprocess.STDOUT,
            timeout=1800,
        )
        fh.write(f"===== exit {result.returncode} =====\n")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
