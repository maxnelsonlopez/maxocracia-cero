"""
Oráculo Sintético de Votaciones — análisis de propuestas con LLM.

Porta el motor de análisis del demo "Oráculos Dinámicos" (Gemini) a una cadena
de oráculos ejecutada en el BACKEND (la API key nunca viaja al navegador):

1. DeepSeek API (principal) — si DEEPSEEK_API_KEY está configurada.
2. Modelo local OpenAI-compatible (fallback, default http://localhost:1337/v1,
   modelo "Qwen3-8B-Q4_K_M" — el hub local de Jan del usuario).

El análisis produce (esquema del demo, adaptado a los axiomas reales):
- vhv:            estimación del Vector de Huella Vital (TV, VA, RF, TimeFactor)
- axiomReport:    validación axiomática (TRUTH/TIME/LIFE + INV1/INV3/INV4)
- oracleOpinions: opiniones de 4 oráculos sintéticos (Economic, Social,
                  Environmental, Futurist)
- engine/model:   firma T13 de qué oráculo produjo el análisis

Transparencia (T13): el resultado se persiste en `maxo_community_analysis`
y se expone públicamente en el detalle de la propuesta.

Variables de entorno:
- DEEPSEEK_API_KEY     (obligatoria para la nube; sin ella se usa solo local)
- DEEPSEEK_BASE_URL    (default: https://api.deepseek.com)
- DEEPSEEK_MODEL       (default: deepseek-chat)
- LOCAL_ORACLE_BASE_URL (default: http://localhost:1337/v1)
- LOCAL_ORACLE_MODEL    (default: Qwen3-8B-Q4_K_M)
- LOCAL_ORACLE_ENABLED  (default: true; "false" para deshabilitar el fallback)
"""

import json
import logging
import os
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
ORACLE_TIMEOUT = 120

SYSTEM_PROMPT = """\
Eres el MOTOR MAXOCRACIA, una IA de gobernanza que opera bajo los axiomas de la \
Maxocracia (Edición 3 Dinámica). Analizas una propuesta de decisión humana y \
generas, en JSON estricto:

1) "vhv" — Vector de Huella Vital estimado:
   - vitalTime (TV): horas de vida humana consumidas (estimación).
   - affectedLives (VA): número de personas impactadas (directa e indirectamente).
   - finiteResources (RF): degradación de recursos finitos, escala 0-1000.
   - timeFactor: multiplicador de impacto a largo plazo (0.1 corto plazo, 2.0 siete generaciones).
   - confidence: confianza del cálculo (0.0-1.0).

2) "axiomReport" — validación axiomática (0-100, con razonamiento):
   - TRUTH: ¿se basa en realidad verificable? (T13 transparencia).
   - TIME: ¿respeta la igualdad temporal fundamental (T2) y el TVI (T0/T1)?
   - LIFE: ¿maximiza vida y minimiza sufrimiento? (T16 Minimizar Daño, INV1 gamma >= 1).
   - Cada ítem: {"type": "TRUTH|TIME|LIFE", "passed": bool, "score": 0-100, "reasoning": str}.

3) "oracleOpinions" — opiniones de 4 oráculos sintéticos que debaten:
   - Economic (eficiencia, recursos, viabilidad a largo plazo).
   - Social (comunidad, equidad, sufrimiento/alegría humana, SDV-H).
   - Environmental (naturaleza, sostenibilidad, recursos finitos, SDV-A).
   - Futurist (consecuencias a generaciones T+7, precaución intergeneracional T14).
   - Cada ítem: {"role": "...", "verdict": "Approve|Reject|Modify", "analysis": str, "confidence": 0.0-1.0}.

Reglas: sé crítico y objetivo; adhiérete estrictamente a la filosofía Maxocracia; \
no inventes datos; si la información es insuficiente, baja la confianza y dilo en el razonamiento.
Responde ÚNICAMENTE con el objeto JSON.
"""


def _base_url() -> str:
    return os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _model() -> str:
    return os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)


def _api_key() -> str:
    return os.environ.get("DEEPSEEK_API_KEY", "")


def is_available() -> bool:
    """True si hay alguna fuente disponible: DeepSeek (nube) o modelo local."""
    return bool(_api_key()) or _local_enabled()


def _call_llm(
    base_url: str,
    api_key: str,
    model: str,
    messages: List[dict],
    temperature: float = 0.2,
    json_mode: bool = True,
    timeout: int = ORACLE_TIMEOUT,
) -> Dict[str, Any]:
    """Llamada HTTP a un endpoint OpenAI-compatible (DeepSeek o local)."""
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2500,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=timeout,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"{model} respondió {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    content = data["choices"][0]["message"].get("content") or "{}"
    return json.loads(content)


def _call_deepseek(messages: List[dict], temperature: float = 0.2) -> Dict[str, Any]:
    """Llama al oráculo DeepSeek (nube, principal)."""
    return _call_llm(
        base_url=_base_url(),
        api_key=_api_key(),
        model=_model(),
        messages=messages,
        temperature=temperature,
        json_mode=True,
        timeout=ORACLE_TIMEOUT,
    )


def _local_base_url() -> str:
    return os.environ.get("LOCAL_ORACLE_BASE_URL", "http://localhost:1337/v1")


def _local_model() -> str:
    return os.environ.get("LOCAL_ORACLE_MODEL", "Qwen3-8B-Q4_K_M")


def _local_enabled() -> bool:
    return os.environ.get("LOCAL_ORACLE_ENABLED", "true").lower() != "false"


def _call_local(messages: List[dict], temperature: float = 0.2) -> Dict[str, Any]:
    """Llama al oráculo local (Jan / llama.cpp, fallback).

    El servidor local puede no soportar response_format; se reintenta sin él.
    """
    try:
        return _call_llm(
            base_url=_local_base_url(),
            api_key="",
            model=_local_model(),
            messages=messages,
            temperature=temperature,
            json_mode=True,
            timeout=120,
        )
    except Exception:
        return _call_llm(
            base_url=_local_base_url(),
            api_key="",
            model=_local_model(),
            messages=messages,
            temperature=temperature,
            json_mode=False,
            timeout=120,
        )


def analyze_proposal(title: str, description: str) -> Dict[str, Any]:
    """
    Analiza una propuesta con el oráculo: DeepSeek (nube) con fallback local.

    Cadena de disponibilidad:
        1. DeepSeek API (si DEEPSEEK_API_KEY está configurada).
        2. Modelo local OpenAI-compatible (si LOCAL_ORACLE_ENABLED, default true).

    Returns:
        dict con claves: vhv, axiomReport, oracleOpinions, model, engine
    """
    if not is_available():
        raise RuntimeError("oracle_disabled")

    prompt = (
        f"PROPUESTA TÍTULO: {title}\n"
        f"DESCRIPCIÓN: {description}\n\n"
        "Analiza esta propuesta ahora. Devuelve el JSON estructurado."
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    errors = []
    if _api_key():
        try:
            result = _call_deepseek(messages, temperature=0.2)
            engine = "deepseek"
            model = _model()
        except Exception as e:
            logger.warning(f"Oráculo DeepSeek no disponible: {e}")
            errors.append(f"deepseek: {e}")
            result = None
            engine = None
            model = None
    else:
        result = None
        engine = None
        model = None

    if result is None and _local_enabled():
        try:
            result = _call_local(messages, temperature=0.2)
            engine = "local"
            model = _local_model()
        except Exception as e:
            logger.warning(f"Oráculo local no disponible: {e}")
            errors.append(f"local: {e}")

    if result is None:
        raise RuntimeError(
            "oracle_unavailable: " + ("; ".join(errors) if errors else "sin fuentes configuradas")
        )

    vhv = result.get("vhv") or {}

    def _clamp(value, lo, hi, default=0.0):
        try:
            return max(lo, min(hi, float(value)))
        except (TypeError, ValueError):
            return default

    vital_time = _clamp(vhv.get("vitalTime"), 0.0, 1e12)
    affected_lives = _clamp(vhv.get("affectedLives"), 0.0, 1e9)
    finite_resources = _clamp(vhv.get("finiteResources"), 0.0, 1000.0)
    time_factor = _clamp(vhv.get("timeFactor"), 0.1, 2.0, default=1.0)
    confidence = _clamp(vhv.get("confidence"), 0.0, 1.0)

    raw = (vital_time * affected_lives * finite_resources) * time_factor
    vhv = {
        "vitalTime": vital_time,
        "affectedLives": affected_lives,
        "finiteResources": finite_resources,
        "timeFactor": time_factor,
        "confidence": confidence,
        "totalScore": raw,
    }

    return {
        "vhv": vhv,
        "axiomReport": result.get("axiomReport") or [],
        "oracleOpinions": result.get("oracleOpinions") or [],
        "model": model or "",
        "engine": engine or "",
    }
