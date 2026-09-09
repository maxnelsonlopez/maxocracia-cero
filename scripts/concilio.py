# -*- coding: utf-8 -*-
"""CLI del Concilio — ciclo y control remoto desde la consola del custodio.

Comandos:
    python scripts/concilio.py                       # ciclo F0-F2 (default)
    python scripts/concilio.py status                # estado + últimos ciclos
    python scripts/concilio.py pausar                # pausa limpiamente
    python scripts/concilio.py reanudar              # reactiva
    python scripts/concilio.py detener               # detiene (requiere reanudar)
    python scripts/concilio.py mensaje "texto"       # directiva para el próximo ciclo
    python scripts/concilio.py ciclo --oracles 5 --dry-run   # explícito

Todo el control es un archivo (scratch/concilio/control.json) con nonce
T13: el custodio gobierna sin abrir sesión; el Concilio siempre deja
bitácora auditable y NUNCA toca el historial de git (guard activo).
"""

import argparse
import json
import sys
from pathlib import Path

# Permite importar maxocontracts cuando se corre como script directo.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from maxocontracts.concilio import (  # noqa: E402
    ACTIVE,
    Control,
    CycleLockError,
    run_cycle,
)

try:
    from dotenv import load_dotenv  # noqa: E402

    load_dotenv(encoding="utf-8")
except ImportError:  # pragma: no cover
    pass


def _control(workspace: str) -> Control:
    return Control(workspace)


def cmd_status(args) -> int:
    control = _control(args.workspace)
    data = control.leer()
    print(f"estado del Concilio : {data.get('estado')} (nonce {data.get('nonce')})")
    insts = data.get("instrucciones", [])
    print(f"directivas en cola  : {len(insts)}")
    for i, texto in enumerate(insts[-3:], 1):
        print(f"  {i}. {texto[:120]}")
    lock = Path(args.workspace) / "concilio.lock"
    print(f"lock de ejecución   : {'OCUPADO' if lock.exists() else 'libre'}")
    from maxocontracts.oracles import engines

    motores = engines.available_engines()
    print(
        f"motores configurados: {', '.join(m.name + '/' + m.model for m in motores) or '(ninguno)'}"
    )
    print(f"orden de la cadena   : {', '.join(engines.DEFAULT_ORDER)}")
    cycles_dir = Path(args.workspace) / "cycles"
    if cycles_dir.exists():
        ciclos = sorted(cycles_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[:3]
        print(f"últimos ciclos ({len(ciclos)}):")
        for ciclo in ciclos:
            resumen = ciclo / "resumen.md"
            estado = "?"
            if (ciclo / "ciclo.json").exists():
                try:
                    estado = json.loads((ciclo / "ciclo.json").read_text(encoding="utf-8")).get(
                        "ejecutable", "?"
                    )
                    estado = "EJECUTABLE" if estado is True else ("en cola" if estado is False else estado)
                except (OSError, ValueError):
                    pass
            primera = ""
            if resumen.exists():
                lineas = resumen.read_text(encoding="utf-8").splitlines()
                primera = next((l for l in lineas if l.startswith("- Quórum")), "")[:110]
            print(f"  • {ciclo.name} · {estado} · {primera}")
    return 0


def cmd_state_op(args, accion: str) -> int:
    control = _control(args.workspace)
    data = getattr(control, accion)()
    print(f"[OK] {accion} → estado '{data.get('estado')}' (nonce {data.get('nonce')})")
    return 0


def cmd_mensaje(args) -> int:
    control = _control(args.workspace)
    data = control.mensaje(args.texto)
    print(f"[OK] directiva encolada (nonce {data.get('nonce')}): {args.texto[:120]}")
    print("Se entregará a los oráculos en el próximo ciclo (frontera F2).")
    return 0


def cmd_ciclo(args) -> int:
    try:
        manifest = run_cycle(
            root=args.root,
            workspace=args.workspace,
            max_oracles=max(1, min(5, args.oracles)),
            dry_run=args.dry_run,
            canon_max_chars=args.canon_chars,
            engine_order=tuple(a.strip() for a in args.orden.split(",")) if args.orden else None,
        )
    except CycleLockError as exc:
        print(f"[concilio] lock: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:  # noqa: BLE001
        print(f"[concilio] error: {exc}", file=sys.stderr)
        return 1
    if manifest.get("pausado"):
        print(f"=== CICLO PAUSADO POR EL CUSTODIO ({manifest.get('estado')}) ===")
        print(f"cycle_id: {manifest['cycle_id']} · bitácora: {manifest['artefactos'].get('bitacora')}")
        return 0
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Concilio de la Maxocracia")
    parser.add_argument("--workspace", default="scratch/concilio", help="workspace de artefactos")
    sub = parser.add_subparsers(dest="accion")

    p_ciclo = sub.add_parser("ciclo", help="ejecuta el ciclo F0-F2")
    p_ciclo.add_argument("--root", default=".")
    p_ciclo.add_argument("--oracles", type=int, default=5)
    p_ciclo.add_argument("--dry-run", action="store_true")
    p_ciclo.add_argument("--canon-chars", type=int, default=160_000)
    p_ciclo.add_argument(
        "--orden", default=None,
        help="cadena de motores: deepseek,nvidia,openrouter (default: CONCILIO_ENGINE_ORDER)",
    )

    sub.add_parser("status", help="estado del Concilio y últimos ciclos")
    sub.add_parser("pausar", help="pausa limpiamente")
    sub.add_parser("reanudar", help="reactiva")
    sub.add_parser("detener", help="detiene hasta reanudar explícito")
    p_msg = sub.add_parser("mensaje", help="encola una directiva del custodio")
    p_msg.add_argument("texto")

    args = parser.parse_args(argv)
    if args.accion is None:
        # compatibilidad: sin subcomando = ciclo
        args.accion = "ciclo"
        args.root = "."
        args.oracles = 5
        args.dry_run = False
        args.canon_chars = 160_000
        args.orden = None

    if args.accion == "ciclo":
        return cmd_ciclo(args)
    if args.accion == "status":
        return cmd_status(args)
    if args.accion == "pausar":
        return cmd_state_op(args, "pausar")
    if args.accion == "reanudar":
        return cmd_state_op(args, "reanudar")
    if args.accion == "detener":
        return cmd_state_op(args, "detener")
    if args.accion == "mensaje":
        return cmd_mensaje(args)
    print(f"acción desconocida: {args.accion}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
