# -*- coding: utf-8 -*-
"""Expande una huella del ledger a su texto (Capa 3 del corpus).

El ledger (C1) conserva fecha + obra + huella; la prosa íntegra vive en el
archivo de git (tags `corpus/registro-pre-ledger-*`). Esta herramienta cierra
el circuito: dada una huella, muestra el texto original.

    .venv\\Scripts\\python.exe scripts\\expandir_huella.py <ref> [--archivo RUTA] [--lineas N]
    .venv\\Scripts\\python.exe scripts\\expandir_huella.py corpus/registro-pre-ledger-20261009 --archivo docs/architecture/atribuciones_sinteticas.md

Sale 0 mostrando el texto (acotado con aviso) o 1 si la huella no resuelve.
"""

import argparse
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _git(args, timeout=30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )


def huella_resuelve(ref: str) -> bool:
    """La huella existe en el archivo (tag, commit o rama)."""
    if not ref or not ref.strip():
        return False
    proc = _git(["cat-file", "-e", ref.strip() + "^{commit}"])
    return proc.returncode == 0


def expandir(ref: str, archivo: str = "", max_lineas: int = 60) -> str:
    """Texto de la huella: archivo@ref, o el mensaje si no se pide archivo."""
    ref = (ref or "").strip()
    if not huella_resuelve(ref):
        return ""
    if archivo:
        proc = _git(["show", f"{ref}:{archivo.strip()}"])
    else:
        proc = _git(["log", "-1", "--format=%H%n%an%n%ad%n%n%B", ref])
    if proc.returncode != 0:
        return ""
    texto = proc.stdout
    lineas = texto.splitlines()
    if len(lineas) > max_lineas:
        texto = "\n".join(lineas[:max_lineas])
        texto += f"\n… [{len(lineas) - max_lineas} líneas más en {ref}]"
    return texto


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Expande una huella del ledger (C3)")
    parser.add_argument("ref", help="tag, commit o rama (p. ej. corpus/registro-pre-ledger-20261009)")
    parser.add_argument("--archivo", default="", help="ruta del archivo en esa ref")
    parser.add_argument("--lineas", type=int, default=60, help="máximo de líneas (default 60)")
    args = parser.parse_args(argv)

    texto = expandir(args.ref, archivo=args.archivo, max_lineas=args.lineas)
    if not texto:
        print(f"[XX] la huella '{args.ref}' no resuelve en el archivo")
        return 1
    print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
