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
