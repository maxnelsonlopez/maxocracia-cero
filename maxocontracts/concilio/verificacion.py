# -*- coding: utf-8 -*-
"""F4 determinista — evidencia dura sobre un candidato ejecutado (Aster §3).

Regla del Concilio: **el agente que realizó un cambio no es la única
autoridad que decide que funcionó.** Aquí se recoge la parte que una máquina
puede verificar sin opinión: suite de tests + anatomía del diff.

`evidencia_determinista` devuelve:
    {
      "tests": {"ran": bool, "status": "pass|fail", "total": int, "failed": int,
                "duration_s": float},
      "diff": {"files_changed": int, "insertions": int, "deletions": int},
      "validador_conceptual": {"ran": bool, "status": "pass|fail"} | ausente
    }

Nada aquí confía en un modelo: es la capa que precede (y fundamenta) la
revisión multi-modelo del diseño G3.
"""

import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional

PASSED_RE = re.compile(r"(\d+)\s+passed")
FAILED_RE = re.compile(r"(\d+)\s+failed")
DIFF_RE = re.compile(
    r"(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?"
)


def _run(cmd, cwd: str, timeout: int):
    """subprocess.run con captura; mockeable en tests."""
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False
    )


def _parse_pytest(output: str, returncode: int) -> Dict[str, Any]:
    total = int(PASSED_RE.search(output).group(1)) if PASSED_RE.search(output) else 0
    failed = int(FAILED_RE.search(output).group(1)) if FAILED_RE.search(output) else 0
    return {
        "ran": True,
        "status": "pass" if returncode == 0 and failed == 0 else "fail",
        "total": total,
        "failed": failed,
    }


def _parse_diff_stat(output: str) -> Dict[str, int]:
    match = DIFF_RE.search(output)
    if not match:
        return {"files_changed": 0, "insertions": 0, "deletions": 0}
    return {
        "files_changed": int(match.group(1) or 0),
        "insertions": int(match.group(2) or 0),
        "deletions": int(match.group(3) or 0),
    }


def evidencia_determinista(
    root: str,
    base_commit: Optional[str] = None,
    suite_cmd: Optional[str] = None,
    timeout: int = 1800,
) -> Dict[str, Any]:
    """Ejecuta la suite pedida y mide la anatomía del diff contra el base.

    `suite_cmd` es una lista (args) o una cadena; default: pytest -q.
    `base_commit` (opcional) permite medir el diff de la rama del candidato.
    """
    root_path = Path(root)
    py = root_path / ".venv" / "Scripts" / "python.exe"
    cmd = (
        [str(py), "-m", "pytest", "-q"]
        if suite_cmd is None
        else (suite_cmd.split() if isinstance(suite_cmd, str) else list(suite_cmd))
    )
    t0 = time.time()
    try:
        proc = _run(cmd, str(root_path), timeout)
        tests = _parse_pytest(proc.stdout, proc.returncode)
        tests["duration_s"] = round(time.time() - t0, 1)
    except (subprocess.TimeoutExpired, OSError) as exc:
        tests = {"ran": False, "status": "fail", "total": 0, "failed": 0, "error": str(exc)[:200]}

    diff_cmd = ["git", "diff", "--stat"]
    if base_commit:
        diff_cmd.append(f"{base_commit}..HEAD")
    try:
        diff_proc = _run(diff_cmd, str(root_path), 60)
        diff = _parse_diff_stat(diff_proc.stdout)
    except (subprocess.TimeoutExpired, OSError):
        diff = {"files_changed": 0, "insertions": 0, "deletions": 0}

    return {"tests": tests, "diff": diff}
