# -*- coding: utf-8 -*-
"""Ejecutor guardado del Concilio — subprocesos con blindaje git.

Decreto del custodio (03-09-2026): el Concilio puede tocar código, con una
única prohibición dura: atentar contra el historial de git (memoria
verificable). Todo lo demás queda bajo la confianza del mandato + tests.

Uso:
    exec = EjecutorGuardado(root, on_event=bitacora.log)
    exec.run("git add maxocontracts")
    exec.run("git commit -m ...")          # permitido
    exec.run("git reset --hard")           # GuardDeniedError
"""

import subprocess
from pathlib import Path
from typing import Callable, List, Optional

from .git_guard import guard_git_command, parse_command


class GuardDeniedError(RuntimeError):
    """Un comando fue bloqueado por el guard de git (historial intocable)."""


class EjecutorGuardado:
    """Ejecuta comandos de shell con el guard git activo.

    Todo evento queda en `on_event` (una función tipo bitácora T13); se
    registra el nombre del comando y su resultado, jamás claves ni secretos.
    """

    def __init__(
        self,
        root: str,
        on_event: Optional[Callable[[dict], None]] = None,
        timeout: int = 300,
    ):
        self.root = str(Path(root))
        self.on_event = on_event or (lambda event: None)
        self.timeout = timeout

    def run(self, command: str) -> subprocess.CompletedProcess:
        """Ejecuta `command` con guard git. Lanza GuardDeniedError si aplica."""
        denial = guard_git_command(command)
        tokens = parse_command(command)
        self.on_event(
            {
                "tipo": "shell",
                "comando": tokens[0] if tokens else "(vacío)",
                "args": len(tokens) - 1 if tokens else 0,
                "guard_git": "bloqueado" if denial else "permitido",
            }
        )
        if denial:
            self.on_event({"tipo": "shell", "evento": "GUARD_DENIED", "motivo": denial})
            raise GuardDeniedError(denial)
        result = subprocess.run(
            tokens,
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=self.timeout,
            check=False,
        )
        self.on_event(
            {
                "tipo": "shell",
                "evento": "resultado",
                "comando": tokens[0] if tokens else "",
                "returncode": result.returncode,
            }
        )
        return result
