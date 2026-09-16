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
    model_alternatives: Tuple[str, ...] = ()

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
        "default_model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        # Los modelos :free de OpenRouter ROTAN y se retiran sin aviso (09-09:
        # glm-4.5-air:free respondió 404 "unavailable for free"; 15-09-2026:
        # deepseek-r1-0528:free y qwen3.6-plus:free también cayeron). Lista
        # vigente según https://openrouter.ai/collections/free-models (09-2026).
        # La cadena prueba alternativas gratuitas y deja la config con la que
        # respondió. Límites free: 20 RPM; 50/día sin créditos, 1000/día con
        # 10+ créditos (docs/api-reference/limits). Cada 404/429 fallido TAMBIÉN
        # consume cuota: por eso la lista prioriza modelos vivos y el ciclo
        # pausa entre llamadas (CONCILIO_PAUSA_SEGUNDOS).
        "model_alternatives": (
            "nvidia/nemotron-3-super-120b-a12b:free",
            "nvidia/nemotron-3.5-lightning:free",
            "poolside/laguna-s-2.1:free",
            "thinkingmachines/inkling:free",
            "cohere/north-mini-code:free",
            "openrouter/free",
        ),
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

# Orden preferido de la cadena (decisión del custodio 15-09-2026, temporal:
# OpenRouter principal mientras no hay ingresos para recargar DeepSeek
# —antes 09-09: DeepSeek principal—. Los gratuitos rotan y a veces caen,
# y la cadena los releva con la firma T13 del motor que respondió).
# Se puede forzar sin tocar código con CONCILIO_ENGINE_ORDER.
DEFAULT_ORDER: Tuple[str, ...] = ("openrouter", "nvidia", "deepseek", "local")

# Límites de los modelos :free de OpenRouter (docs/api-reference/limits):
# 20 req/min siempre; 50 req/día sin créditos, 1000/día con 10+ créditos.
# Un ciclo F0-F2 son 10 llamadas (5 firmas + 5 votos) + 3 de F4: cabe en la
# cuota free con 1 ciclo/día, siempre que no se queme cuota en reintentos.
OPENROUTER_FREE_RPM = 20
OPENROUTER_FREE_RPD_SIN_CREDITOS = 50
OPENROUTER_FREE_RPD_CON_CREDITOS = 1000


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
        model_alternatives=tuple(spec.get("model_alternatives", ())),
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


def _retry_after_seconds(resp: Any, default: float = 0.0) -> float:
    """Segundos de espera que pide el proveedor (header Retry-After).

    OpenRouter devuelve 429 con `Retry-After` (y `X-RateLimit-Reset` en los
    límites de plataforma). Best-effort: cualquier valor ilegible → default.
    """
    try:
        headers = getattr(resp, "headers", None) or {}
        raw = (
            headers.get("Retry-After", "")
            or headers.get("retry-after", "")
            or headers.get("X-RateLimit-Reset", "")
        )
        return max(0.0, float(str(raw).strip().split(",")[0]))
    except (TypeError, ValueError, AttributeError):
        return default


def _request_headers(cfg: EngineConfig) -> Dict[str, str]:
    """Cabeceras por motor. OpenRouter recomienda HTTP-Referer + X-Title."""
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }
    if cfg.name == "openrouter":
        ref = (os.environ.get("OPENROUTER_SITE_URL") or "https://localhost/maxocracia").strip()
        title = (os.environ.get("OPENROUTER_APP_TITLE") or "Maxocracia-Concilio").strip()
        if ref:
            headers["HTTP-Referer"] = ref
        if title:
            headers["X-Title"] = title
    return headers


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
    fallos de conexión. En 429 honra `Retry-After`; en OpenRouter, agotados
    los reintentos del mismo modelo, rota a la siguiente alternativa :free
    (los límites free son por cuenta, pero repartir entre modelos evita
    el model-level throttling del proveedor). Lanza EngineError al agotar
    los intentos; la firma externa (engine, model) la reporta el llamador.
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
    headers = _request_headers(cfg)

    last_error: Optional[str] = None
    alternatives = list(cfg.model_alternatives)
    extra_tries = len(alternatives)
    for attempt in range(max_retries + 1 + extra_tries):
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
        # Modelo retirado/cambiado (OpenRouter :free rota sin aviso): probar
        # la siguiente alternativa gratuita y actualizar cfg.model — así la
        # firma T13 posterior sigue siendo la verdad del motor que respondió.
        if resp.status_code == 404 and alternatives:
            body = resp.text.lower()
            if "unavailable" in body or "not found" in body or "model" in body:
                nuevo = alternatives.pop(0)
                logger.warning(
                    "[%s] modelo %s no disponible (404: %s); probando %s",
                    cfg.name, cfg.model, resp.text[:120], nuevo,
                )
                cfg.model = nuevo
                payload["model"] = nuevo
                continue
        if resp.status_code in RETRYABLE_STATUS:
            espera = _retry_after_seconds(resp)
            last_error = f"[{cfg.name}] HTTP {resp.status_code}: {resp.text[:200]}"
            if attempt < max_retries:
                logger.warning(
                    "%s (intento %d/%d)", last_error, attempt + 1, max_retries
                )
                if espera:
                    time.sleep(min(espera, 60.0))
                continue
            # Reintentos del mismo modelo agotados: en OpenRouter se rota al
            # siguiente :free (cada 429/5xx fallido también consume cuota
            # diaria: no tiene sentido insistir en el mismo modelo caído).
            if alternatives:
                nuevo = alternatives.pop(0)
                logger.warning(
                    "[%s] %s persistente; rotando %s -> %s",
                    cfg.name, resp.status_code, cfg.model, nuevo,
                )
                cfg.model = nuevo
                payload["model"] = nuevo
                if espera:
                    time.sleep(min(espera, 60.0))
                continue
            raise EngineError(last_error)
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
    max_retries: int = 2,
) -> Tuple[str, EngineConfig]:
    """Prueba los motores disponibles en orden y devuelve (texto, motor usado).

    La identidad del motor (name/model) es la firma T13 del resultado:
    el llamador debe persistirla junto al análisis. `max_retries` acota los
    reintentos por motor (el fallback del Concilio usa 1: cada intento de
    120s en un proveedor caído alarga el ciclo minutos).
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
                max_retries=max_retries,
            )
            logger.info("motor %s/%s respondió (%d chars)", cfg.name, cfg.model, len(text))
            return text, cfg
        except EngineError as exc:
            errors.append(str(exc))
            logger.warning("motor %s falló, siguiente: %s", cfg.name, exc)
    raise EngineError("Todos los motores fallaron: " + " | ".join(errors))
