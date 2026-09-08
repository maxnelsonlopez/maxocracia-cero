"""
Registro de motores LLM para oráculos — proveedores intercambiables (Concilio).

Contrato OpenAI-compatible: `{base_url}/chat/completions`.

Cada motor se resuelve desde variables de entorno con el patrón
`{PROVIDER}_API_KEY` / `{PROVIDER}_BASE_URL` / `{PROVIDER}_MODEL`
(mismos nombres que ya usan `voting_oracle.py`, `live_oracle.py` y
`plataforma_educativa/app/score_engine.py`), de modo que añadir un
proveedor gratuito no reescribe nada: solo se registra y se configuran
sus variables.

Degradación elegante (canon: el proveedor es intercambiable, el fallo del
proveedor no es un fallo del sistema — `administracion_humano_sintetica.md`
§7): `available_engines()` solo incluye motores con clave configurada y
`chain_call()` intenta en orden, devolviendo el texto del primero que
responda junto con su par (engine, model) — la firma T13 del análisis que
produjo el resultado.

Diseño: `docs/architecture/concilio_oraculos_sinteticos_piloto.md` (§5).
"""

import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 120
DEFAULT_MAX_TOKENS = 4000

# HTTPs que merecen reintento (cuota, sobrecarga, picos transitorios)
RETRYABLE_STATUS = {429, 500, 502, 503, 529}


class EngineError(RuntimeError):
    """El motor (proveedor) falló: red, HTTP o respuesta ilegible."""


@dataclass
class EngineConfig:
    """Configuración resuelta de un motor LLM (OpenAI-compatible)."""

    name: str
    api_key: str
    base_url: str
    model: str
    json_mode: bool = True
    timeout: int = DEFAULT_TIMEOUT

    def endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"


# Registro canónico de motores: qué variables de entorno y qué defaults.
ENGINE_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "nvidia": {
        "api_key_env": "NVIDIA_NIM_API_KEY",
        "base_url_env": "NVIDIA_NIM_BASE_URL",
        "model_env": "NVIDIA_NIM_MODEL",
        "default_base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "deepseek-ai/deepseek-v4-flash-0731",
        "json_mode": True,
    },
    "openrouter": {
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url_env": "OPENROUTER_BASE_URL",
        "model_env": "OPENROUTER_MODEL",
        "default_base_url": "https://openrouter.ai/api/v1",
        "default_model": "z-ai/glm-4.5-air:free",
        "json_mode": True,
    },
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url_env": "DEEPSEEK_BASE_URL",
        "model_env": "DEEPSEEK_MODEL",
        "default_base_url": "https://api.deepseek.com",
        "default_model": "deepseek-chat",
        "json_mode": True,
    },
    "local": {
        "api_key_env": "LOCAL_ORACLE_API_KEY",
        "base_url_env": "LOCAL_ORACLE_BASE_URL",
        "model_env": "LOCAL_ORACLE_MODEL",
        "default_base_url": "http://localhost:1337/v1",
        "default_model": "Qwen3-8B-Q4_K_M",
        "json_mode": False,
    },
}

# Orden preferido de la cadena: gratuito-talla completa → agregador → propio → local.
DEFAULT_ORDER: Tuple[str, ...] = ("nvidia", "openrouter", "deepseek", "local")


def resolve_engine(name: str, env: Optional[Dict[str, str]] = None) -> Optional[EngineConfig]:
    """Resuelve un motor desde el entorno; None si falta su API key."""
    spec = ENGINE_DEFAULTS.get(name)
    if spec is None:
        return None
    env = env if env is not None else os.environ
    api_key = (env.get(spec["api_key_env"]) or "").strip()
    if not api_key:
        return None
    base_url = env.get(spec["base_url_env"]) or spec["default_base_url"]
    model = env.get(spec["model_env"]) or spec["default_model"]
    timeout = DEFAULT_TIMEOUT
    try:
        timeout = int(env.get(f"{name.upper()}_TIMEOUT") or DEFAULT_TIMEOUT)
    except (TypeError, ValueError):
        pass
    return EngineConfig(
        name=name,
        api_key=api_key,
        base_url=base_url,
        model=model,
        json_mode=bool(spec["json_mode"]),
        timeout=timeout,
    )


def available_engines(
    env: Optional[Dict[str, str]] = None, order: Optional[Tuple[str, ...]] = None
) -> List[EngineConfig]:
    """Motores listos para usar, en el orden de la cadena."""
    order = order if order is not None else DEFAULT_ORDER
    engines = []
    for name in order:
        cfg = resolve_engine(name, env=env)
        if cfg is not None:
            engines.append(cfg)
    return engines


def call_engine(
    cfg: EngineConfig,
    messages: List[Dict[str, str]],
    temperature: float = 0.2,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    want_json: bool = False,
    timeout: Optional[int] = None,
    max_retries: int = 2,
    backoff_seconds: float = 2.0,
) -> str:
    """Una llamada a un motor. Devuelve el texto de la primera elección.

    Reintenta con backoff ante errores transitorios (429/5xx, incluido el
    529 "Service temporarily overloaded" observado en NVIDIA NIM) y ante
    fallos de conexión. Lanza EngineError al agotar los intentos; la firma
    externa (engine, model) la reporta el llamador, que es quien sabe qué
    motor pidió.
    """
    payload: Dict[str, Any] = {
        "model": cfg.model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    # response_format solo en motores que lo soportan (el patrón local reintenta
    # sin él; aquí se evita enviarlo cuando el motor lo declara inseguro).
    if want_json and cfg.json_mode:
        payload["response_format"] = {"type": "json_object"}
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }

    last_error: Optional[str] = None
    for attempt in range(max_retries + 1):
        if attempt:
            time.sleep(backoff_seconds * attempt)
        try:
            resp = requests.post(
                cfg.endpoint(),
                json=payload,
                headers=headers,
                timeout=timeout or cfg.timeout,
            )
        except requests.RequestException as exc:
            last_error = f"[{cfg.name}] no se pudo contactar: {exc}"
            logger.warning("%s (intento %d/%d)", last_error, attempt, max_retries)
            continue
        if resp.status_code in RETRYABLE_STATUS and attempt < max_retries:
            last_error = f"[{cfg.name}] HTTP {resp.status_code}: {resp.text[:200]}"
            logger.warning(
                "%s (intento %d/%d)", last_error, attempt + 1, max_retries
            )
            continue
        if resp.status_code != 200:
            raise EngineError(f"[{cfg.name}] HTTP {resp.status_code}: {resp.text[:200]}")
        try:
            data = resp.json()
            return str(data["choices"][0]["message"]["content"] or "")
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise EngineError(f"[{cfg.name}] respuesta ilegible: {exc}") from exc
    raise EngineError(last_error or f"[{cfg.name}] sin respuesta")


def chain_call(
    system: str,
    user: str,
    env: Optional[Dict[str, str]] = None,
    order: Optional[Tuple[str, ...]] = None,
    want_json: bool = False,
    temperature: float = 0.2,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    timeout: Optional[int] = None,
) -> Tuple[str, EngineConfig]:
    """Prueba los motores disponibles en orden y devuelve (texto, motor usado).

    La identidad del motor (name/model) es la firma T13 del resultado:
    el llamador debe persistirla junto al análisis.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    engines = available_engines(env=env, order=order)
    if not engines:
        raise EngineError("Ningún motor configurado (faltan API keys)")
    errors = []
    for cfg in engines:
        try:
            text = call_engine(
                cfg,
                messages,
                temperature=temperature,
                max_tokens=max_tokens,
                want_json=want_json,
                timeout=timeout,
            )
            logger.info("motor %s/%s respondió (%d chars)", cfg.name, cfg.model, len(text))
            return text, cfg
        except EngineError as exc:
            errors.append(str(exc))
            logger.warning("motor %s falló, siguiente: %s", cfg.name, exc)
    raise EngineError("Todos los motores fallaron: " + " | ".join(errors))
