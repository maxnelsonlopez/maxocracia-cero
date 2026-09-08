# Instala la guarda de historial de git en .git/hooks/pre-push
# Decreto del custodio (03-09-2026): blindar contra comandos que atenten
# contra el historial. El hook bloquea cualquier push que NO sea
# fast-forward (rewrites / force / borrado de refs) hacia el remoto.
#
# Uso: .venv\Scripts\python.exe scripts\instalar_guardas_git.py
#      (o .venv\Scripts\python.exe scripts\instalar_guardas_git.py --quitar)

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOK = REPO / ".git" / "hooks" / "pre-push"
GUARD = REPO / "scripts" / "git_hooks" / "pre_push_guard.py"


def git_dir() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--git-dir"], cwd=REPO, capture_output=True, text=True, timeout=15
    ).stdout.strip()
    if not out:
        raise SystemExit("No se detectó repo git en " + str(REPO))
    return Path(out) if Path(out).is_absolute() else REPO / out


def instalar() -> None:
    hooks = git_dir() / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    # El sh de git for Windows ejecuta #!-scripts; usamos un shim POSIX que
    # llama al guard con el python del proyecto.
    shim = (
        "#!/bin/sh\n"
        f'REPO="{REPO.as_posix()}"\n'
        'PY="$REPO/.venv/Scripts/python.exe"\n'
        'if [ ! -x "$PY" ]; then PY="python"; fi\n'
        '$PY "$REPO/scripts/git_hooks/pre_push_guard.py" || exit 1\n'
    )
    (hooks / "pre-push").write_text(shim, encoding="utf-8")
    head = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True
    ).stdout.strip()
    print(f"[OK] Guarda instalada: {hooks / 'pre-push'}")
    print(f"     Core: {GUARD} (commit {head})")


def quitar() -> None:
    target = HOOK
    if target.exists():
        target.unlink()
        print(f"[OK] Guarda removida: {target}")
    else:
        print("No hay guarda instalada.")


if __name__ == "__main__":
    if "--quitar" in sys.argv:
        quitar()
    else:
        instalar()
