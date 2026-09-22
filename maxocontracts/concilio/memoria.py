# -*- coding: utf-8 -*-
"""Memoria causal del Concilio — aprendizaje, no changelog (propuesta de Aster).

Secuencia que preserva (la "memoria de aprendizaje"):
    CREÍAMOS X → HICIMOS Y → OBSERVAMOS Z → DESCUBRIMOS W → DECIDIMOS Q → AHORA CREEMOS X'

Formato de registro (JSONL, por ciclo y candidato):
    {
      "cycle_id": "...", "candidate_id": "...",
      "hypothesis": "Creemos que X mejorará Y bajo estas condiciones",
      "expected_signal": "...", "change": {"base_commit": "...", "result_commit": "...", "files": [...]},
      "evidence": [...], "decision": "ratify|revoke|queue",
      "outcome": "...", "unexpected_effects": [], "uncertainties": [],
      "changed_mind": [], "next_hypothesis": "..."
    }

Decisiones válidas (F5, Aster §5): RATIFY (suficiente evidencia), REVOKE
(reversible: la investigación NO se borra), QUEUE (estado constitucional:
"no sabemos" — conservar, no integrar, no destruir).
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List

FICHA = Path("aprendizaje.jsonl")

VALID_DECISIONS = {"ratify", "revoke", "queue"}

REQUIRED_FIELDS = ("cycle_id", "candidate_id", "hypothesis", "decision")


class RegistroAprendizajeError(ValueError):
    """Un registro de aprendizaje no cumple el contrato mínimo."""


def registrar_aprendizaje(workspace: str, record: Dict[str, Any]) -> Path:
    """Añade un aprendizaje al archivo de memoria (append-only, JSONL)."""
    for campo in REQUIRED_FIELDS:
        if not str(record.get(campo, "") or "").strip():
            raise RegistroAprendizajeError(f"Falta el campo obligatorio '{campo}'")
    decision = str(record.get("decision", "")).strip().lower()
    if decision not in VALID_DECISIONS:
        raise RegistroAprendizajeError(
            f"decision inválida '{decision}': debe ser 'ratify'|'revoke'|'queue'"
        )
    record["decision"] = decision
    record.setdefault("ts", time.time())
    path = Path(workspace) / FICHA
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


def leer_aprendizajes(workspace: str, n: int = 5) -> List[Dict[str, Any]]:
    """Últimos `n` aprendizajes (los más recientes al final)."""
    path = Path(workspace) / FICHA
    if not path.exists():
        return []
    registros: List[Dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    registros.append(json.loads(line))
                except (ValueError, TypeError):
                    continue
    return registros[-n:]


# --- Cuarta dimensión: memoria de desacuerdos (Aster, 09-09-2026) ---
# No solo guardamos lo que decidimos: guardamos qué alternativas se
# descartaron, quién las defendió y por qué. Un civilización puede cometer
# dos veces el mismo error si solo conserva la decisión final.

FICHA_DESACUERDOS = Path("desacuerdos.jsonl")


def registrar_desacuerdo(workspace: str, record: Dict[str, Any]) -> Path:
    """Registra una alternativa descartada (memoria institucional anti-amnesia)."""
    for campo in ("question", "discarded_alternative", "defended_by", "reason"):
        if not str(record.get(campo, "") or "").strip():
            raise RegistroAprendizajeError(
                f"Falta el campo obligatorio '{campo}' del desacuerdo"
            )
    record.setdefault("ts", time.time())
    path = Path(workspace) / FICHA_DESACUERDOS
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


def leer_desacuerdos(workspace: str, n: int = 5) -> List[Dict[str, Any]]:
    """Últimos desacuerdos registrados (contra la amnesia institucional)."""
    path = Path(workspace) / FICHA_DESACUERDOS
    if not path.exists():
        return []
    registros: List[Dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    registros.append(json.loads(line))
                except (ValueError, TypeError):
                    continue
    return registros[-n:]


# --- Métricas de aprendizaje (Aster §8, con la defensa anti-gamificación) ---
# Regla: un aprendizaje necesita SOBREVIVIR al ciclo que lo produjo
# (latencia epistemológica). Estas métricas son SEÑALES de observación,
# jamás objetivos: quien las convierta en meta estará jugando el juego.


def metricas_aprendizaje(workspace: str) -> Dict[str, Any]:
    """Contadores honestos de la memoria causal.

    `valid_learnings_per_cycle` (provisional): aprendizajes ratificados con
    hipótesis y outcome registrado — la definición completa exige citación
    posterior o ratificación humana (v0.2 doc §3.2); se reporta como
    "provisional" hasta que exista uso en ciclos posteriores.
    """
    registros = leer_aprendizajes(workspace, n=10_000)
    total = len(registros)
    por_decision = {d: 0 for d in VALID_DECISIONS}
    changed_mind = 0
    for r in registros:
        por_decision[str(r.get("decision", ""))] = (
            por_decision.get(str(r.get("decision", "")), 0) + 1
        )
        if r.get("changed_mind"):
            changed_mind += 1
    validos = sum(
        1
        for r in registros
        if r.get("decision") == "ratify" and r.get("hypothesis") and r.get("outcome")
    )
    revisiones = 0
    for r in registros:
        revisiones += len(
            r.get("evidence", []) if isinstance(r.get("evidence"), list) else []
        )
    return {
        "total": total,
        "por_decision": por_decision,
        "valid_learnings_per_cycle_provisional": validos,
        "reversal_rate": round(por_decision["revoke"] / total, 3) if total else 0.0,
        "changed_mind_rate": round(changed_mind / total, 3) if total else 0.0,
        "reviews_registradas": revisiones,
        "advertencia": (
            "señales de observación, no objetivos; valid_learnings exige "
            "latencia epistemológica (citación posterior o ratificación humana)"
        ),
    }
