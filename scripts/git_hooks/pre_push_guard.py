# -*- coding: utf-8 -*-
"""Pre-push guard — bloquea empujes que reescriben el historial remoto.

Decreto del custodio (03-09-2026): "blindar la plataforma contra comandos
que atenten contra el historial de git".

Regla del hook: por cada ref empujada, si el commit remoto actual NO es
ancestro del local (es decir: el historial sería reescrito/destruido),
se bloquea el push. Instalado por `scripts/instalar_guardas_git.ps1`.

Uso directo (stdin con líneas `local_ref local_sha remote_ref remote_sha`):
    python scripts/git_hooks/pre_push_guard.py
"""

import subprocess
import sys
from typing import List, Optional


def check_ancestor(local_sha: str, remote_sha: str, git_dir: str) -> Optional[str]:
    """None si el historial es seguro; motivo si el push reescribiría la memoria.

    Casos:
    - remote_sha = 0…0 → rama nueva: nada que proteger.
    - local_sha = 0…0 y remote_sha real → borrado de ref remota: bloqueado.
    - remote_sha no existe → no hay nada que proteger (el remoto validará).
    - remote_sha existe y NO es ancestro de local_sha → reescritura: bloqueado.
    """
    zeros = "0" * 40
    if remote_sha == zeros:
        return None
    if local_sha == zeros:
        return (
            f"PUSH BLOQUEADO (guard de historial): la ref remota {remote_sha[:8]} "
            "sería BORRADA con este push — la memoria publicada no se destruye. "
            "Si la rama ya no sirve, archívala; no la borres."
        )
    existe = subprocess.run(
        ["git", "cat-file", "-e", remote_sha + "^{commit}"],
        cwd=git_dir,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if existe.returncode != 0:
        return None  # sha desconocido: nada que proteger
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", remote_sha, local_sha],
        cwd=git_dir,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode != 0:
        return (
            f"PUSH BLOQUEADO (guard de historial): {remote_sha[:8]} no es ancestro "
            f"de {local_sha[:8]} — este push reescribiría la memoria verificable. "
            "Deshaz con git revert o git reset --soft; jamás con --force."
        )
    return None


def parse_push_lines(lines: List[str]):
    for line in lines:
        parts = line.split()
        if len(parts) == 4:
            yield parts  # local_ref local_sha remote_ref remote_sha


def main() -> int:
    git_dir = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    for local_ref, local_sha, remote_ref, remote_sha in parse_push_lines(
        sys.stdin.read().splitlines()
    ):
        motivo = check_ancestor(local_sha, remote_sha, git_dir)
        if motivo:
            print(f"[pre-push guard] {remote_ref}: {motivo}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
