# -*- coding: utf-8 -*-
"""Ciclo F0-F2 del Concilio: despertar, absorción del canon y agenda votada.

F0 Despertar  — abre sesión de custodia (lock, mandato, motores disponibles).
F1 Absorción  — cada oráculo lee el corpus y firma su comprensión (JSON firmado).
F2 Agenda     — cada oráculo propone candidatos desde la agenda y vota;
                agregación con consenso >=75% y quórum de 3 (canon Cap 14.3);
                AVA: "axioms.ok == False" convierte su voto en rechazo
                automático (Cap 14.4).

El ciclo NO edita el código vivo: escribe artefactos en el workspace
(por defecto `scratch/concilio/cycles/<id>/`): firma por oráculo, agenda
votada en texto civil y manifiesto `ciclo.json` con la firma T13 de cada
llamada (engine/model).
"""

import json
import re
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..oracles import engines
from .bitacora import Bitacora
from .canon import read_agenda, read_canon

# Roles del AVA (Cap 14.3/14.4): el Disidente es un rol, no un contreras.
ORACLE_ROLES = ("Economic", "Social", "Environmental", "Futurist", "Dissident")

REQUIRED_QUORUM = 3
CONSENSUS_MIN = 0.75

LOCK_STALE_SECONDS = 6 * 3600


class CycleLockError(RuntimeError):
    """Ya hay un ciclo del Concilio en marcha (lock de ejecución)."""


class CorpoUnavailableError(RuntimeError):
    """No hay motores configurados ni corpus disponible."""


def _parse_json(text: str) -> Dict[str, Any]:
    """Extrae el primer objeto JSON del texto del modelo (tolerante)."""
    text = text.strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except (ValueError, TypeError):
        pass
    for block in re.findall(r"```(?:json)?\s*(.*?)```", text, re.DOTALL):
        try:
            parsed = json.loads(block.strip())
            if isinstance(parsed, dict):
                return parsed
        except (ValueError, TypeError):
            continue
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        candidate = json.loads(text[start : i + 1])
                        if isinstance(candidate, dict):
                            return candidate
                    except (ValueError, TypeError):
                        break
    raise ValueError("El oráculo no devolvió JSON válido")


# --- Plantillas de prompt ---

FIRMA_SYSTEM = """\
Eres el oráculo sintético {role} del CONCILIO DE LA MAXOCRACIA.
Demuestra que comprendiste el canon antes de proponer trabajo.

Reglas inviolables (canon):
1. La teoría (libro, Ed. 3 Dinámica) tiene prioridad: T0–T15 son índices
   del libro (nunca se renumeran); T16/T17 son de ingeniería.
2. No inventes: toda cita debe corresponder al corpus (axioma, §, archivo).
   Si no sabes, declara incertidumbre y baja la confianza.
3. Invariantes innegociables: INV1 (γ≥1), INV2 (SDV-H), INV2-S (SDV-S),
   INV3 (VHV no ocultable, T13), INV4 (retractabilidad).
4. CAPA DE TERNURA: "los axiomas son el esqueleto; la ternura es el corazón".

Responde ÚNICAMENTE JSON:
{{"firma": {{"summary": "resumen del canon", "axiom_quotes": ["cita textual"],
"critical_question": "1 pregunta crítica", "confidence": 0.0}}}}
"""

AGENDA_SYSTEM = """\
Eres el oráculo sintético {role} del CONCILIO DE LA MAXOCRACIA.
El Concilio vota QUÉ trabajar sobre el repositorio real de la Maxocracia.

Reglas:
1. Fidelidad al canon (G1): cada propuesta cita su fuente (backlog, mapa,
   leyenda del corpus). Prohibido renumerar axiomas o alterar invariantes.
2. Candidato acotado (~1-2 días de un agente), verificable (tests, rutas
   concretas), con riesgos y axiomas que toca.
3. AVA sobre TI (Cap 14.4): valida TRUTH/TIME/LIFE/RESOURCES; si una
   propuesta viola un axioma → tu voto es "reject" y "axioms.ok" = false
   (rechazo automático).
4. No inventes fuentes: si no está en el corpus, dilo con confianza baja.

AGENDA (pendientes reales del proyecto):
{agenda}

Responde ÚNICAMENTE JSON:
{{"axioms": {{"ok": true, "reasoning": "..."}},
"proposals": [{{"title": "...", "source": "cita fuente", "why": "...",
"risks": "...", "tests": "...", "axioms": ["..."], "vote": "approve|reject|modify",
"confidence": 0.0}}],
"veto": null}}
"""


def _firma_user(canon: str) -> str:
    return f"CANON (léelo y cítalo):\n{canon}"


def _agenda_user(canon: str, agenda: str) -> str:
    return (
        f"CANON (base de verdad):\n{canon}\n\n"
        "INSTRUCCIÓN: propón 1-3 candidatos con su voto, desde la AGENDA (si "
        "ninguna te convence, propón desde el canon con fuente explícita)."
    )


# --- Lock ---

def _acquire_lock(workspace: Path) -> Path:
    """Lock por archivo con PID; rechaza ciclos simultáneos (si no es stale)."""
    lock_path = workspace / "concilio.lock"
    workspace.mkdir(parents=True, exist_ok=True)
    if lock_path.exists():
        age = time.time() - lock_path.stat().st_mtime
        if age < LOCK_STALE_SECONDS:
            raise CycleLockError(
                f"Hay un ciclo en marcha (lock {lock_path}, {int(age)}s de vida)"
            )
    lock_path.write_text(
        json.dumps({"pid": os_getpid(), "ts": time.time()}),
        encoding="utf-8",
    )
    return lock_path


def os_getpid() -> int:
    import os

    return os.getpid()


def _release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except OSError:
        pass


# --- Punto de llamada (mockeable en tests) ---

def _call(engine_cfg, system: str, user: str, want_json: bool = True):
    """Una llamada a un motor con firma T13. Mockeable en tests."""
    text = engines.call_engine(
        engine_cfg, [{"role": "system", "content": system}, {"role": "user", "content": user}],
        want_json=want_json, max_tokens=4000,
    )
    return text


def _git_head(root: str) -> str:
    """HEAD de git (best-effort; nunca bloquea el ciclo)."""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return out.stdout.strip() or "?"
    except Exception:  # noqa: BLE001
        return "?"


def run_cycle(
    root: str,
    workspace: str = "scratch/concilio",
    env: Optional[Dict[str, str]] = None,
    max_oracles: int = 5,
    dry_run: bool = False,
    canon_max_chars: int = 160_000,
) -> Dict[str, Any]:
    """Ejecuta F0-F2 y devuelve el resumen del ciclo (con rutas de artefactos)."""
    root_path = Path(root)
    workspace_path = Path(workspace)

    # F0 — Despertar
    lock_path = _acquire_lock(workspace_path)
    cycle_id = f"ciclo-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    cycle_dir = workspace_path / "cycles" / cycle_id
    bitacora = Bitacora(cycle_dir)

    try:
        motores = engines.available_engines(env=env)
        bitacora.log(
            {
                "fase": "F0",
                "evento": "despertar",
                "cycle_id": cycle_id,
                "motores": [
                    {"engine": m.name, "model": m.model} for m in motores
                ],
                "git_head": _git_head(str(root_path)),
                "dry_run": dry_run,
            }
        )
        if not motores:
            raise CorpoUnavailableError("Ningún motor configurado (faltan API keys)")

        canon = read_canon(str(root_path), total_max_chars=canon_max_chars)
        agenda = read_agenda(str(root_path))
        bitacora.log(
            {"fase": "F1", "evento": "corpus", "canon_chars": len(canon), "agenda_chars": len(agenda)}
        )
        if not canon.strip():
            raise CorpoUnavailableError("Corpus canónico vacío (¿root del repo correcto?)")

        # Asignación de roles a motores: diversidad primero (el Disidente
        # jamás comparte motor con el Economic si hay más de un motor).
        roles: List[Tuple[str, Any]] = []
        for i, role in enumerate(ORACLE_ROLES[:max_oracles]):
            engine = motores[i % len(motores)]
            roles.append((role, engine))
        if len(motores) > 1:
            dissident = next((r for r in roles if r[0] == "Dissident"), None)
            if dissident:
                first_engine = roles[0][1].name
                alt = next(m for m in motores if m.name != first_engine)
                roles = [
                    (r, alt) if (r == "Dissident" and e.name == first_engine) else (r, e)
                    for r, e in roles
                ]

        # F1 — Firma de comprensión (por oráculo, sin ver el trabajo ajeno)
        firmas: List[Dict[str, Any]] = []
        for role, engine in roles:
            system = FIRMA_SYSTEM.format(role=role)
            user = _firma_user(canon)
            if dry_run:
                firma = {"summary": "[dry-run]", "axiom_quotes": [], "critical_question": "", "confidence": 0.0}
                t13 = {"engine": engine.name, "model": engine.model, "dry_run": True}
            else:
                text = _call(engine, system, user, want_json=True)
                parsed = _parse_json(text)
                firma = parsed.get("firma") or {"summary": text[:400], "axiom_quotes": [], "critical_question": "", "confidence": 0.0}
                t13 = {"engine": engine.name, "model": engine.model}
            firmas.append({"role": role, **t13, "firma": firma})
            bitacora.log(
                {"fase": "F1", "evento": "firma", "role": role, **t13, "confidence": firma.get("confidence")}
            )

        # F2 — Propuestas y votación (independientes entre sí)
        votos: List[Dict[str, Any]] = []
        for role, engine in roles:
            system = AGENDA_SYSTEM.format(role=role, agenda=agenda or "(sin agenda: propón desde el canon)")
            user = _agenda_user(canon, agenda or "(sin agenda: propón desde el canon)")
            if dry_run:
                resp = {"axioms": {"ok": True, "reasoning": "[dry-run]"}, "proposals": [], "veto": None}
                t13 = {"engine": engine.name, "model": engine.model, "dry_run": True}
            else:
                text = _call(engine, system, user, want_json=True)
                resp = _parse_json(text)
                t13 = {"engine": engine.name, "model": engine.model}
            axioms_ok = bool(resp.get("axioms", {}).get("ok", False))
            proposals = [
                p for p in resp.get("proposals", []) if isinstance(p, dict)
            ]
            votos.append(
                {
                    "role": role,
                    **t13,
                    "axioms_ok": axioms_ok,
                    "axioms_reasoning": str(resp.get("axioms", {}).get("reasoning", "")),
                    "proposals": [
                        {
                            "title": str(p.get("title", "")),
                            "source": str(p.get("source", "")),
                            "why": str(p.get("why", "")),
                            "risks": str(p.get("risks", "")),
                            "tests": str(p.get("tests", "")),
                            "axioms": p.get("axioms", []),
                            "vote": str(p.get("vote", "modify")),
                            "confidence": float(p.get("confidence", 0.5) or 0.5),
                        }
                        for p in proposals
                    ],
                }
            )
            bitacora.log(
                {
                    "fase": "F2",
                    "evento": "voto",
                    "role": role,
                    **t13,
                    "axioms_ok": axioms_ok,
                    "n_proposals": len(proposals),
                }
            )

        # Agregación (canon Cap 14.3: consenso 75% + quórum de validadores).
        # Semántica del AVA (Cap 14.4): un oráculo cuyo "axioms.ok" es False
        # convierte TODOS sus votos en rechazo automático — no desaparece del
        # denominador, sino que empuja el consenso hacia abajo.
        quorum_ok = len(votos) >= REQUIRED_QUORUM
        approves = 0
        for v in votos:
            if not v["axioms_ok"]:
                continue
            if any(p["vote"] == "approve" for p in v["proposals"]):
                approves += 1
        validos = [v for v in votos if v["axioms_ok"]]
        consensus = (approves / len(votos)) if votos else 0.0
        ejecutable = quorum_ok and consensus >= CONSENSUS_MIN

        # ranking de propuestas: por votos approve, luego confianza media
        ranking: List[Dict[str, Any]] = []
        for v in votos:
            for p in v["proposals"]:
                ranking.append(
                    {
                        "title": p["title"],
                        "source": p["source"],
                        "vote": p["vote"],
                        "role": v["role"],
                        "engine": v["engine"],
                        "model": v["model"],
                        "confidence": p["confidence"],
                    }
                )
        approved_titles = [r["title"] for r in ranking if r["vote"] == "approve"]
        selected = sorted(
            ranking,
            key=lambda r: (r["vote"] == "approve", r["confidence"]),
            reverse=True,
        )[:3] if ejecutable else []

        # Artefactos
        firmas_path = cycle_dir / "firmas.json"
        with open(firmas_path, "w", encoding="utf-8") as fh:
            json.dump(firmas, fh, ensure_ascii=False, indent=2)

        agenda_path = cycle_dir / "agenda_votada.md"
        lines = [
            f"# Agenda votada del Concilio — {cycle_id}",
            "",
            f"- Motores: {', '.join(m.name + '/' + m.model for m in motores)}",
            f"- Quórum: {len(votos)} oráculos (mínimo {REQUIRED_QUORUM}) · Consenso: {consensus:.0%} "
            f"(mínimo {CONSENSUS_MIN:.0%})",
            f"- Estado: **{'EJECUTABLE' if ejecutable else 'EN COLA'}**"
            + (" (dry-run, sin llamadas)" if dry_run else ""),
            "",
            "## Propuestas (por oráculo)",
            "",
        ]
        for v in votos:
            lines.append(f"### {v['role']} · {v['engine']}/{v['model']} · AVA: "
                         f"{'OK' if v['axioms_ok'] else 'RECHAZO AXIOMÁTICO'}")
            if not v["proposals"]:
                lines.append("- (sin propuestas) ")
            for p in v["proposals"]:
                lines.append(
                    f"- **{p['title']}** — voto: {p['vote']} ({p['confidence']:.0%})\n"
                    f"  - fuente: {p['source']}\n  - por qué: {p['why']}\n"
                    f"  - riesgos: {p['risks']}\n  - tests: {p['tests']}\n"
                    f"  - axiomas: {', '.join(p['axioms']) if p['axioms'] else '—'}"
                )
            if not v["axioms_ok"]:
                lines.append(f"  - motivo AVA: {v['axioms_reasoning']} ")
        if ejecutable:
            lines.append("\n## Elegidas (orden de prioridad)")
            for i, s in enumerate(selected, 1):
                lines.append(f"{i}. {s['title']} — {s['vote']} ({s['confidence']:.0%}) "
                             f"[{s['engine']}/{s['model']}]")
            lines.append(
                "\n> La ejecución (F3) exige mandato de sesión de custodia, trabajo "
                "en scratch/, suite en verde y revisión cruzada antes de F5."
            )
        else:
            lines.append("\n## Resultado")
            if not quorum_ok:
                lines.append("Quórum insuficiente (mínimo 3 oráculos): la agenda queda en cola "
                             "— ningún desempate automático (canon: el desacuerdo es calidad).")
            else:
                lines.append("Sin consenso ≥75%: la agenda queda en cola. El Disidente tiene "
                             "registrado su análisis en firmas.json.")
        with open(agenda_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

        manifest = {
            "cycle_id": cycle_id,
            "fases": "F0-F2",
            "git_head": _git_head(str(root_path)),
            "motores": [{"engine": m.name, "model": m.model} for m in motores],
            "oraculos": [v["role"] for v in votos],
            "quorum_ok": quorum_ok,
            "consensus": round(consensus, 3),
            "ejecutable": ejecutable,
            "dry_run": dry_run,
            "artefactos": {
                "firmas": str(firmas_path),
                "agenda": str(agenda_path),
                "bitacora": str(bitacora.events_path),
                "manifest": str(bitacora.manifest_path),
            },
        }
        manifest_path = bitacora.write_manifest(manifest)
        bitacora.log({"fase": "CIERRE", "evento": "manifest", "ejecutable": ejecutable, "manifest": str(manifest_path)})
        return manifest
    finally:
        _release_lock(lock_path)
