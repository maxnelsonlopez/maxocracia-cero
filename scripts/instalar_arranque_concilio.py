r"""Instala/desinstala la tarea de arranque del Concilio (al iniciar sesión).

    .venv\Scripts\python.exe scripts\instalar_arranque_concilio.py
    .venv\Scripts\python.exe scripts\instalar_arranque_concilio.py --quitar

Usa el Programador de tareas de Windows (no requiere admin para tareas del
usuario). La tarea solo DESPIERTA al Concilio; las pausas/paradas viven en
scratch/concilio/control.json (el custodio manda).
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TASK_NAME = "MaxocraciaConcilio"
PY = REPO / ".venv" / "Scripts" / "python.exe"
SCRIPT = REPO / "scripts" / "autostart_concilio.py"


def _task_command() -> str:
    # sin comillas internas: schtasks no las tolera (las rutas no tienen
    # espacios en este repo; si cambiara, ajustar aquí).
    return f"{PY} {SCRIPT}"


def _instalar_startup_folder() -> int:
    """Carpeta de Inicio (sin privilegios): pythonw, sin consola visible."""
    import os

    startup = (
        Path(os.environ["APPDATA"])
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )
    startup.mkdir(parents=True, exist_ok=True)
    pyw = PY.with_name("pythonw.exe")
    if not pyw.exists():
        pyw = PY
    cmd_file = startup / "MaxocraciaConcilio.cmd"
    cmd_file.write_text(
        f'@echo off\r\n"{pyw}" "{SCRIPT}"\r\n',
        encoding="utf-8",
    )
    print(f"[OK] Autoarranque en carpeta de Inicio: {cmd_file}")
    print("     El Concilio despertará con tu sesión de Windows; pausa con:")
    print("     python scripts/concilio.py pausar")
    return 0


def instalar() -> int:
    r = subprocess.run(
        "schtasks /Create /TN "
        f'"{TASK_NAME}" /TR "{_task_command()}" /SC ONLOGON /RL LIMITED /F',
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r.returncode == 0:
        print(r.stdout.strip())
        print(f"[OK] Tarea '{TASK_NAME}' registrada (al iniciar sesión).")
        print("     Pausa: python scripts/concilio.py pausar")
        return 0
    # Acceso denegado o entorno restringido → carpeta de Inicio (sin admin).
    print(
        f"[info] schtasks no disponible ({r.stderr.strip()[:80]}); usando la "
        "carpeta de Inicio..."
    )
    return _instalar_startup_folder()


def quitar() -> int:
    r = subprocess.run(
        ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=60,
    )
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode


if __name__ == "__main__":
    if "--quitar" in sys.argv:
        raise SystemExit(quitar())
    raise SystemExit(instalar())
