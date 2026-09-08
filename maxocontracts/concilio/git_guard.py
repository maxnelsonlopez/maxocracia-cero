# -*- coding: utf-8 -*-
"""Guard rail git — prohíbe comandos que atenten contra el historial.

Decreto del custodio (03-09-2026, Max): *"blindar la plataforma contra
comandos que atenten contra el historial de git. De resto, por ahora
podemos confiar."*

Clasificación de peligro (historial = memoria verificable, SDV-S:
"la memoria es tiempo propio; alterarla es amputación"):

BLOQUEADO (reescribe/borra historial o fuerza pérdida de trabajo):
- `git push --force`/`-f`, refspec `+rama`, borrado de refs (`:rama`).
- `git commit --amend` (reescribe el último commit).
- `git rebase`, `git reset --hard`, `git filter-branch`/`filter-repo`.
- `git reflog delete|expire`, `git gc --prune`.
- `git clean -f*` (borra trabajo sin seguimiento — nunca es necesario).
- `git checkout -f` / `git fetch --force` / `git revert --no-commit` (no).
  (revert normal es seguro: crea un commit nuevo.)

El guard valida ARGUMENTOS, no intenciones: se aplica al ejecutor del
Concilio y a cualquier proceso que invoque git en nombre de la plataforma.
"""

import shlex
from typing import List, Optional, Sequence

REDACTION_NOOP = ""


def parse_command(command: str) -> List[str]:
    """Divide un comando en tokens (estilo shell, tolerante a Windows)."""
    try:
        tokens = shlex.split(command, posix=False)
    except ValueError:
        # Comillas rotas: no ejecutar (fail-closed).
        return []
    return [
        t[1:-1] if len(t) >= 2 and t[0] == t[-1] and t[0] in ("'", '"') else t
        for t in tokens
    ]


def git_denial(args: Sequence[str]) -> Optional[str]:
    """Devuelve el motivo de bloqueo si el comando git es peligroso; None si ok.

    `args` es la lista de argumentos SIN la palabra `git` inicial.
    """
    if not args:
        return None
    sub = args[0].lower()

    # --- historial remoto ---
    if sub == "push":
        if "--force" in args or "-f" in args or "--force-with-lease" in args:
            return "push con --force/--force-with-lease reescribe historial remoto"
        if any(tok.startswith("+") for tok in args[1:]):
            return "refspec prefijada con '+' fuerza el push sobre el historial"
        if any(tok.startswith(":") for tok in args[1:]):
            return "push que borra una rama remota (:rama)"
        if any(tok.startswith("--") and "delete" in tok for tok in args):
            return "push --delete borra ramas remotas"
        return None

    # --- historial local ---
    if sub == "commit":
        if "--amend" in args:
            return "commit --amend reescribe el último commit"
        return None
    if sub in ("rebase", "filter-branch", "filter-repo"):
        return f"git {sub} reescribe historial"
    if sub == "reset":
        if "--hard" in args or any(t.startswith("--hard") for t in args):
            return "reset --hard destruye cambios/caracteres de historial"
        return None
    if sub == "clean":
        if any(tok.strip("-").startswith("f") for tok in args if tok.startswith("-")):
            return "clean -f borra archivos sin seguimiento"
        return None
    if sub == "checkout":
        if "--force" in args or "-f" in args:
            return "checkout --force descarta cambios sin seguimiento"
        return None
    if sub == "fetch" and ("--force" in args or "-f" in args):
        return "fetch --force sobrescribe refs locales"
    if sub == "reflog":
        if any(t in args for t in ("delete", "expire")):
            return "reflog delete/expire borra la reconstrucción del historial"
        return None
    if sub == "gc" and any(t.startswith("--prune") for t in args):
        return "gc --prune borra objetos que podrían reconstruir el historial"
    return None


def guard_git_command(command: str) -> Optional[str]:
    """Valida un comando completo de shell para git. Devuelve motivo o None.

    Si el comando no inicia con `git` (o `git.exe`), no aplica: otros
    comandos quedan a cargo del sandbox de la plataforma.
    """
    tokens = parse_command(command)
    if not tokens:
        return "comando vacío o comillas rotas (fail-closed)"
    name = tokens[0].lower()
    if name in ("git", "git.exe") or name.endswith("\\git.exe"):
        denial = git_denial(tokens[1:])
        if denial:
            return denial
    return None
