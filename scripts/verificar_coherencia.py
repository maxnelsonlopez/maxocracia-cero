# -*- coding: utf-8 -*-
"""Verificación de coherencia del canon — UN comando, sin ambigüedad.

Misión del ciclo-20260909-114428 (elegida 90%): la coherencia axiomática del
repo se valida hoy con varios pasos (validador conceptual + sus tests);
esto los concentra en un solo comando con veredicto duro (exit code).

    .venv\\Scripts\\python.exe scripts\\verificar_coherencia.py [--suite]

--suite añade la suite completa de pytest (pesada; por defecto solo se corre
el validador conceptual + sus tests, que es la coherencia axiomática en sí).
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = REPO / ".venv" / "Scripts" / "python.exe"


def _run(cmd, timeout=1800):
    """subprocess.run con captura; mockeable en tests."""
    return subprocess.run(
        cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout, check=False
    )


def _resumen(out: str, err: str) -> str:
    tail = " ".join((out or err).strip().splitlines()[-1:])
    return tail[-180:]


def checks_incluir(con_suite: bool):
    """Lista de comprobaciones (orden de importancia axiomática)."""
    return [
        (
            "Integridad del corpus (¿el Concilio lee todo lo que dice leer?)",
            [str(PY), "scripts/auditar_canon.py"],
        ),
        (
            "Validador conceptual (axiomas en todo el repo)",
            [str(PY), "scripts/validador_conceptual.py"],
        ),
        (
            "Tests del validador",
            [str(PY), "-m", "pytest", "tests/test_validador_conceptual.py", "-q"],
        ),
    ] + (
        [
            (
                "Suite completa de pytest",
                [str(PY), "-m", "pytest", "-q"],
            )
        ]
        if con_suite
        else []
    )


def ejecutar(con_suite: bool) -> int:
    """Corre cada comprobación y devuelve 0 si todo pasa, 1 si algo falla."""
    fallos = 0
    for nombre, cmd in checks_incluir(con_suite):
        print(f"-> {nombre} ...")
        try:
            proc = _run(cmd)
        except (subprocess.TimeoutExpired, OSError) as exc:
            print(f"  [XX] ERROR de ejecucion: {str(exc)[:120]}")
            fallos += 1
            continue
        if proc.returncode == 0:
            print(f"  [OK] verde ({_resumen(proc.stdout, proc.stderr)})")
        else:
            fallos += 1
            print(f"  [XX] ROJO ({_resumen(proc.stdout, proc.stderr)})")
    if fallos:
        print(f"\n>> COHERENCIA: {fallos} comprobacion(es) fallaron.")
        return 1
    print("\n>> COHERENCIA: VERDE. El canon esta en paz.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verificación de coherencia en un comando")
    parser.add_argument("--suite", action="store_true", help="incluye la suite completa de pytest")
    args = parser.parse_args(argv)
    return ejecutar(con_suite=args.suite)


if __name__ == "__main__":
    raise SystemExit(main())
