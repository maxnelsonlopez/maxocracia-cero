# -*- coding: utf-8 -*-
"""Índice navegable del canon — la tabla de contenidos viva del Concilio.

Misión del ciclo-20260909-114428 (elegida 90%): que cada oráculo (y cada
humano) pueda orientarse por área con un comando, antes de leer el corpus
completo. Determinista: solo lee el repo, nunca escribe fuera del out.

    .venv\\Scripts\\python.exe scripts\\canon_index.py [--out scratch/concilio/canon_index.md]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Áreas canónicas (orden de lectura: teoría primero, luego mapas → motor → código).
AREAS = [
    ("docs/book/edicion_3_dinamica", "Libro (Edición 3 Dinámica)"),
    ("docs/theory", "Teoría"),
    ("docs/architecture", "Mapas y arquitectura"),
    ("maxocontracts", "Motor de dominio (puro)"),
    ("app", "Backend Flask"),
    ("plataforma_educativa/app", "Plataforma educativa (OEV)"),
    ("tests", "Tests"),
    ("scripts", "Herramientas"),
]

HEADING_RE = re.compile(r"^#{1,3}\s+(.+)$", re.MULTILINE)
SKIP_PARTS = {"__pycache__", "node_modules", ".venv", ".git", ".next"}


def _git_head() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or "?"
    except Exception:  # noqa: BLE001
        return "?"


def build_index(root: Path, max_files: int = 60) -> str:
    """Genera el índice (texto markdown) — nunca depende de la red."""
    lines = [
        "# Índice navegable del canon — Maxocracia",
        "",
        f"- Git: {_git_head()}"
        + " · Uso: los oráculos leen esto para orientarse; el corpus completo "
        "sigue en `read_canon()`.",
        "",
    ]
    for rel_base, etiqueta in AREAS:
        base = root / rel_base
        if not base.exists():
            continue
        lines.append(f"\n## {etiqueta} (`{rel_base}/`)\n")
        encontrados = 0
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.suffix not in (".md", ".py"):
                continue
            if any(seg in SKIP_PARTS for seg in p.parts):
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            rel = p.relative_to(base)
            heads = [m.group(1).strip() for m in list(HEADING_RE.finditer(text))[:5]]
            lines.append(f"- **{rel}** · {len(text)} caracteres")
            for h in heads:
                lines.append(f"  - {h[:90]}")
            encontrados += 1
            if encontrados >= max_files:
                lines.append(f"- … (resto del área no mostrado; límite {max_files} por área)")
                break
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Índice navegable del canon")
    parser.add_argument(
        "--out", default="scratch/concilio/canon_index.md",
        help="ruta de salida (default: scratch/concilio/canon_index.md)",
    )
    parser.add_argument("--stdout", action="store_true", help="imprime en consola")
    args = parser.parse_args(argv)

    indice = build_index(REPO)
    if args.stdout:
        print(indice)
        return 0
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(indice, encoding="utf-8")
    lineas = len(indice.splitlines())
    print(f"[OK] Índice del canon: {out} ({lineas} líneas) · Git {_git_head()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
