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


def cmd_revisar(args) -> int:
    """F4: revisión multi-modelo de un candidato (resultado, no voto)."""
    import os

    from maxocontracts.concilio.revision import revisar_candidato

    orden = None
    raw = os.environ.get("CONCILIO_ENGINE_ORDER", "").strip()
    if raw:
        orden = tuple(n.strip() for n in raw.split(",") if n.strip())
    try:
        diff_text = args.diff
        if diff_text.startswith("@"):  # conveniencia: leer el diff desde un archivo
            diff_text = Path(diff_text[1:]).read_text(encoding="utf-8")
        revisiones = revisar_candidato(
            proposal=args.propuesta,
            diff=diff_text or "(diff no proporcionado: revisar en el diff real)",
            evidence=args.evidencia or "(sin evidencia determinista)",
            order=orden,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[concilio] F4 error: {exc}", file=sys.stderr)
        return 1
    print("=== F4 — REVISIÓN MULTI-MODELO ===")
    for r in revisiones:
        print(
            f"- {r['role']} [{r['engine']}/{r['model']}"
            f"{' (fallback)' if r.get('fallback') else ''}]: {r['verdict']} "
            f"({r['confidence']:.0%})"
        )
        for c in r.get("criticisms", []):
            print(f"    crítica: {str(c)[:180]}")
        for u in r.get("uncertainties", []):
            print(f"    incertidumbre: {str(u)[:180]}")
        if r.get("changed_mind"):
            cm = r["changed_mind"]
            print(f"    changed_mind: {cm.get('desde')} -> {str(cm.get('hacia'))[:120]}")
    return 0


def cmd_decidir(args) -> int:
    """F5: RATIFY / REVOKE / QUEUE — escribe el aprendizaje (memoria causal)."""
    from maxocontracts.concilio import (
        RegistroAprendizajeError,
        registrar_aprendizaje,
    )

    decision = args.decision.lower()
    try:
        path = registrar_aprendizaje(
            args.workspace,
            {
                "cycle_id": args.cycle,
                "candidate_id": args.candidato,
                "hypothesis": args.hipotesis or "(hipótesis no registrada)",
                "expected_signal": args.señal or "",
                "decision": decision,
                "outcome": args.outcome or "",
                "evidence": args.evidencia.split(",") if args.evidencia else [],
                "changed_mind": [],
                "next_hypothesis": args.siguiente_hipotesis or "",
            },
        )
    except RegistroAprendizajeError as exc:
        print(f"[concilio] F5 error: {exc}", file=sys.stderr)
        return 1
    print(f"[OK] aprendizaje registrado ({decision}): {path}")
    if decision == "revoke":
        print("  > La investigación NO se borra: queda en el registro y su historia.")
        print("  > Integra la reversión con git revert (nunca --force; el guard vigila).")
    elif decision == "queue":
        print("  > 'No sabemos' es un estado constitucional: conservar, no integrar, no destruir.")
    return 0


def cmd_metricas(args) -> int:
    """Métricas de la memoria causal (señales, nunca objetivos)."""
    from maxocontracts.concilio import metricas_aprendizaje

    m = metricas_aprendizaje(args.workspace)
    print("=== MÉTRICAS DE APRENDIZAJE (observación, no metas) ===")
    for k, v in m.items():
        print(f"- {k}: {v}")
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
    p_ciclo.add_argument("--canon-chars", type=int, default=90_000)
    p_ciclo.add_argument(
        "--orden", default=None,
        help="cadena de motores: openrouter,nvidia,deepseek (default: CONCILIO_ENGINE_ORDER)",
    )

    sub.add_parser("status", help="estado del Concilio y últimos ciclos")
    sub.add_parser("pausar", help="pausa limpiamente")
    sub.add_parser("reanudar", help="reactiva")
    sub.add_parser("detener", help="detiene hasta reanudar explícito")
    p_msg = sub.add_parser("mensaje", help="encola una directiva del custodio")
    p_msg.add_argument("texto")

    p_rev = sub.add_parser("revisar", help="F4: revisión multi-modelo del resultado")
    p_rev.add_argument("--propuesta", required=True, help="propuesta aprobada en F2")
    p_rev.add_argument("--diff", default="", help="diff real (o ruta al archivo)")
    p_rev.add_argument("--evidencia", default="", help="evidencia determinista (resumen)")

    p_dec = sub.add_parser("decidir", help="F5: ratify|revoke|queue + registro de aprendizaje")
    p_dec.add_argument("--cycle", required=True, help="cycle_id")
    p_dec.add_argument("--candidato", required=True, help="título o id del candidato")
    p_dec.add_argument("--decision", required=True, choices=["ratify", "revoke", "queue"])
    p_dec.add_argument("--hipotesis", default="")
    p_dec.add_argument("--senal", dest="señal", default="")
    p_dec.add_argument("--outcome", default="")
    p_dec.add_argument("--evidencia", default="")
    p_dec.add_argument("--siguiente-hipotesis", dest="siguiente_hipotesis", default="")

    sub.add_parser("metricas", help="métricas de la memoria causal")

    args = parser.parse_args(argv)
    if args.accion is None:
        # compatibilidad: sin subcomando = ciclo
        args.accion = "ciclo"
        args.root = "."
        args.oracles = 5
        args.dry_run = False
        args.canon_chars = 90_000
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
    if args.accion == "revisar":
        return cmd_revisar(args)
    if args.accion == "decidir":
        return cmd_decidir(args)
    if args.accion == "metricas":
        return cmd_metricas(args)
    print(f"acción desconocida: {args.accion}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
