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


# --- Destilado de memoria (Capa 1, 09-10-2026, hito 4) ---
# La ventana deslizante (últimos 5) olvida por edad, no por digestión: una
# civilización pierde lo aprendido en el ciclo 6 aunque siga valiendo en el
# 60. El destilado comprime TODOS los registros en reglas por veredicto con
# cobertura declarada; `read_agenda` lo prefiere cuando está fresco y solo
# entonces jubila la ventana.

DESTILADO = Path("memoria_destilada.md")


def _corta(valor: object, n: int) -> str:
    return str(valor or "").strip().replace("\n", " ")[:n]


def sintetizar_memoria(workspace: str, max_chars: int = 3_000) -> Path:
    """Digiere todos los registros en un destilado acotado y determinista.

    Sin relojes ni muestreos: la misma memoria siempre produce el mismo
    destilado (la frescura se decide por cobertura, no por fecha).
    """
    apr = leer_aprendizajes(workspace, n=10_000)
    des = leer_desacuerdos(workspace, n=10_000)
    por_decision = {"ratify": 0, "revoke": 0, "queue": 0}
    for r in apr:
        d = str(r.get("decision", ""))
        por_decision[d] = por_decision.get(d, 0) + 1
    lineas = [
        "# Memoria destilada del Concilio (C1: digestión, no ventana)",
        f"- cobertura: {len(apr)} aprendizajes · {len(des)} desacuerdos",
        "- veredictos: "
        f"ratify={por_decision.get('ratify', 0)} "
        f"revoke={por_decision.get('revoke', 0)} "
        f"queue={por_decision.get('queue', 0)}",
        "",
        "## Reglas ratificadas (constrúyelas, no las repitas)",
    ]
    ratificadas = [
        f"- ({_corta(r.get('cycle_id'), 40)}) {_corta(r.get('hypothesis'), 160)}"
        f" → {_corta(r.get('outcome'), 160)}"
        for r in apr
        if r.get("decision") == "ratify" and r.get("outcome")
    ]
    lineas += ratificadas or ["- (ninguna todavía)"]
    lineas.append("")
    lineas.append("## Revocadas (no reintentar sin evidencia nueva)")
    revocadas = [
        f"- ({_corta(r.get('cycle_id'), 40)}) {_corta(r.get('hypothesis'), 160)}"
        f" ✗ {_corta(r.get('outcome'), 160)}"
        for r in apr
        if r.get("decision") == "revoke"
    ]
    lineas += revocadas or ["- (ninguna)"]
    lineas.append("")
    lineas.append("## Abiertas (QUEUE: lo que aún no sabemos)")
    abiertas = [
        f"- ({_corta(r.get('cycle_id'), 40)}) {_corta(r.get('next_hypothesis'), 180)}"
        for r in apr
        if r.get("decision") == "queue" and r.get("next_hypothesis")
    ]
    lineas += abiertas or ["- (ninguna)"]
    lineas.append("")
    lineas.append("## Objeciones vigentes (no re-proponer sin evidencia nueva)")
    objeciones = [
        f"- {_corta(r.get('question'), 120)}: descartada "
        f"«{_corta(r.get('discarded_alternative'), 120)}» "
        f"({_corta(r.get('defended_by'), 40)}: {_corta(r.get('reason'), 120)})"
        for r in des
    ]
    lineas += objeciones or ["- (ninguna)"]
    cuerpo = "\n".join(lineas) + "\n"
    if len(cuerpo) > max_chars:
        cuerpo = cuerpo[:max_chars] + "\n… [destilado recortado; regenerar tras podar]"
    path = Path(workspace) / DESTILADO
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(cuerpo, encoding="utf-8")
    return path


def leer_memoria_destilada(workspace: str, max_chars: int = 3_000) -> str:
    """El destilado solo si está fresco: debe cubrir todo lo registrado.

    Frescura por cobertura, no por fecha: si se registró algo después de
    sintetizar, el destilado está rancio y se devuelve vacío (la agenda cae
    a la ventana heredada en vez de citar memoria amputada).
    """
    import re

    path = Path(workspace) / DESTILADO
    if not path.exists():
        return ""
    try:
        texto = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    marca = re.search(r"cobertura: (\d+) aprendizajes · (\d+) desacuerdos", texto)
    if not marca:
        return ""
    frescos = int(marca.group(1)) == len(
        leer_aprendizajes(workspace, n=10_000)
    ) and int(marca.group(2)) == len(leer_desacuerdos(workspace, n=10_000))
    if not frescos:
        return ""
    if len(texto) > max_chars:
        texto = texto[:max_chars] + "\n… [destilado recortado]"
    return texto


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
