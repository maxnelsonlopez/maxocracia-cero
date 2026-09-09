# -*- coding: utf-8 -*-
"""F4 conceptual — revisión multi-modelo del RESULTADO (Aster §4, v0.3).

Regla: **el agente que realizó un cambio no es la única autoridad que decide
que funcionó** y la revisión **no repite la votación F2**: revisa el diff y
la evidencia contra el mandato. Se pregunta «¿el cambio implementado sigue
realizando lo que F2 aprobó?» y se captura explícitamente:
qué aprobó cada revisor, qué criticó, qué incertidumbre encontró y si
**cambió de opinión** (cambiar de opinión ante evidencia nueva es deber del
administrador — administración humano-sintética §5).

Diseño (diseño G3 + v0.2 §1): ejecutor → revisor A (proveedor 1) → revisor B
(proveedor 2) → Disidente (proveedor distinto si hay 3+).
"""

from typing import Any, Dict, List, Optional, Tuple

from ..oracles import engines
from .cycle import _parse_json  # extracción JSON tolerante (misma casa)

REVISOR_SYSTEM = """\
Eres {role} del CONCILIO DE LA MAXOCRACIA, en la fase F4 (verificación).

NO estás votando la propuesta de nuevo: estás auditando el RESULTADO.
Pregunta central: ¿el cambio implementado sigue realizando lo que la
propuesta aprobó en F2? Compara mandato ↔ diff real ↔ evidencia.

PROPUESTA APROBADA (F2):
{proposal}

DIFF (cambios reales):
{diff}

EVIDENCIA DETERMINISTA:
{evidence}

Reglas: 1) el canon manda (T13, T16/T17, invariantes INV1-4, INV2-S);
2) no inventes: solo lo que ves en el diff/evidencia; 3) si ves divergencia
entre propuesta y diff, dilo: es precisamente lo que buscas
("los tests pueden pasar y aun así el cambio apartarse del mandato").
{dissidente_parrafo}
Responde ÚNICAMENTE JSON:
{{"verdict": "approve|modify|reject",
"criticisms": ["..."], "uncertainties": ["..."],
"changed_mind": {{"desde": "approve|reject|desconocido", "hacia": "..."}},
"confidence": 0.0,
"reasoning": "..."}}
"""

DISSIDENTE_PARRAFO = (
    "Además actúa como Disidente Permanente (Cap. 19): maximiza la distancia "
    "crítica racional — no eres contreras, buscas lo mejor para la comunidad; "
    "registra tu postura inicial y si la evidencia te hizo cambiarla."
)


def _prompt_revisor(role: str, proposal: str, diff: str, evidence: str) -> Tuple[str, str]:
    parrafo = DISSIDENTE_PARRAFO if role.lower().startswith("dissident") else ""
    system = REVISOR_SYSTEM.format(
        role=role, proposal=proposal, diff=diff, evidence=evidence,
        dissidente_parrafo=parrafo,
    )
    user = (
        "INSTRUCCIÓN: audita el resultado. Si falta información, baja la "
        "confianza y dilo. Criticar con fundamento es un deber, no un fallo."
    )
    return system, user


def revisar_candidato(
    proposal: str,
    diff: str,
    evidence: str,
    env: Optional[Dict[str, str]] = None,
    order: Optional[Tuple[str, ...]] = None,
    roles=("Revisor A", "Revisor B", "Dissident"),
) -> List[Dict[str, Any]]:
    """Revisión multi-modelo: A (motor 1) → B (motor 2) → Disidente.

    Cada revisión es independiente (no ve las demás). La firma T13
    engine/model se conserva en cada veredicto; el `changed_mind` es la
    señal de aprendizaje (nunca un objetivo).
    """
    motores = engines.available_engines(env=env, order=order)
    if not motores:
        raise engines.EngineError("Ningún motor configurado para la revisión")
    revisiones: List[Dict[str, Any]] = []
    for i, role in enumerate(roles):
        # diversidad real: motor distinto por revisor (si hay suficientes)
        motor = motores[i % len(motores)]
        system, user = _prompt_revisor(role, proposal, diff, evidence)
        try:
            text, cfg, _fallback = _call_revision(motor, system, user)
            parsed = _parse_json(text)
        except (ValueError, engines.EngineError):
            revisiones.append(
                {
                    "role": role,
                    "engine": motor.name,
                    "model": motor.model,
                    "verdict": "reject",
                    "criticisms": ["El revisor no pudo ser consultado (fallo de motor)"],
                    "uncertainties": ["infra"],
                    "confidence": 0.0,
                    "fallback": True,
                }
            )
            continue
        revisiones.append(
            {
                "role": role,
                "engine": cfg.name,
                "model": cfg.model,
                "fallback": _fallback,
                "verdict": str(parsed.get("verdict", "modify")),
                "criticisms": parsed.get("criticisms", []),
                "uncertainties": parsed.get("uncertainties", []),
                "changed_mind": parsed.get("changed_mind"),
                "confidence": float(parsed.get("confidence", 0.5) or 0.5),
                "reasoning": str(parsed.get("reasoning", ""))[:600],
            }
        )
    return revisiones


def _call_revision(engine_cfg, system: str, user: str):
    """Motor designado con fallback a la cadena (igual que el ciclo F1/F2)."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    try:
        text = engines.call_engine(
            engine_cfg, messages, want_json=True, max_tokens=3000,
            timeout=180, max_retries=1, backoff_seconds=3.0,
        )
        return text, engine_cfg, False
    except engines.EngineError:
        order = tuple(
            m.name for m in engines.available_engines() if m.name != engine_cfg.name
        )
        text, cfg = engines.chain_call(
            system, user, order=order or None, want_json=True,
            max_tokens=3000, timeout=180,
        )
        return text, cfg, True
