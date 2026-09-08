# -*- coding: utf-8 -*-
"""CLI del Concilio — ejecuta un ciclo F0-F2.

Uso (raíz del repo):
    .venv\\Scripts\\python.exe scripts\\concilio.py [--root R] [--workspace W]
        [--oracles N] [--dry-run] [--canon-chars N]

Salida: resumen del ciclo y rutas de los artefactos (firmas, agenda votada,
bitácora JSONL, manifiesto). NO edita el código vivo: escribe en scratch/.
"""

import argparse
import json
import sys
from pathlib import Path

# Permite importar maxocontracts cuando se corre como script directo.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from maxocontracts.concilio import CycleLockError, run_cycle  # noqa: E402

try:
    from dotenv import load_dotenv

    # El Flask carga .env en run.py; un script autónomo debe cargarlo solo.
    load_dotenv(encoding="utf-8")
except ImportError:  # pragma: no cover - python-dotenv es dependencia del repo
    pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Concilio de la Maxocracia: ciclo F0-F2")
    parser.add_argument("--root", default=".", help="raíz del repo (default: cwd)")
    parser.add_argument("--workspace", default="scratch/concilio", help="workspace de artefactos")
    parser.add_argument("--oracles", type=int, default=5, help="oráculos participantes (1-5)")
    parser.add_argument("--dry-run", action="store_true", help="sin llamadas a motores")
    parser.add_argument("--canon-chars", type=int, default=160_000, help="tope del corpus (caracteres)")
    args = parser.parse_args(argv)

    try:
        manifest = run_cycle(
            root=args.root,
            workspace=args.workspace,
            max_oracles=max(1, min(5, args.oracles)),
            dry_run=args.dry_run,
            canon_max_chars=args.canon_chars,
        )
    except CycleLockError as exc:
        print(f"[concilio] lock: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:  # noqa: BLE001
        print(f"[concilio] error: {exc}", file=sys.stderr)
        return 1

    print("=== CICLO COMPLETADO ===")
    print(f"cycle_id: {manifest['cycle_id']}")
    print(f"motores: {', '.join(m['engine'] + '/' + m['model'] for m in manifest['motores'])}")
    print(f"oráculos: {len(manifest['oraculos'])} ({', '.join(manifest['oraculos'])})")
    print(f"consenso: {manifest['consensus']:.0%} · quórum OK: {manifest['quorum_ok']}")
    print(f"estado: {'EJECUTABLE' if manifest['ejecutable'] else 'EN COLA'}")
    print("artefactos:")
    for key, path in manifest["artefactos"].items():
        print(f"  {key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
