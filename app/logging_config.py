# -*- coding: utf-8 -*-
"""Logging estructurado JSON sin información sensible (plan de seguridad §3.4).

Reglas del plan (`docs/architecture/PLAN_ENDURECIMIENTO_SEGURIDAD.md` §3.4):
- Nunca loguear: tokens, γ verdadero de protegidos (Modo Escudo, §16.5.12),
  contenido de ESI, hashes T13 con datos personales.
- El T13 es la evidencia: se loguea su hash, no su contenido.

Mecánica:
- `SanitizingFilter`: redacta patrones de secretos (JWT, Bearer, claves API)
  en el mensaje y los argumentos de cada registro.
- `JsonFormatter`: una línea JSON por registro; las claves de `extra` cuyo
  nombre coincida con campos sensibles (esi, gamma, wellness, token, api_key,
  secret, password, authorization…) se redactan recursivamente.
- `setup_json_logging()`: opt-in con `LOG_JSON=1`; si no se activa, la app
  mantiene su comportamiento actual (logs de desarrollo).
"""

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict

# Patrones de secretos conocidos (formato de las claves que usa el proyecto)
_REDACT_PATTERNS = [
    # JWT (header.payload.signature)
    re.compile(r"eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}"),
    # Authorization Bearer
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{10,}"),
    # Claves API conocidas: sk-…, nvapi-…, gsk_…, ak-…
    re.compile(r"(?i)(?:sk|nvapi|gsk_|ak)-[A-Za-z0-9_\-]{10,}"),
]

# Nombres de campos que jamás deben aparecer en un log (valor → "<redactado>")
_SENSITIVE_FIELDS = {
    "token",
    "jwt",
    "access_token",
    "refresh_token",
    "authorization",
    "api_key",
    "apikey",
    "secret",
    "password",
    "passwd",
    "esi",
    "gamma_protegido",
    "wellness_protegido",
    "escudo",
    "shield",
}

REDACTED = "<redactado>"


def redact_text(text: str) -> str:
    """Redacta patrones de secretos en texto libre."""
    if not text:
        return text
    for pattern in _REDACT_PATTERNS:
        text = pattern.sub(REDACTED, text)
    return text


def sanitize_value(value: Any, key: str = "") -> Any:
    """Redacta recursivamente según el nombre del campo (clave sensible).

    El nombre del campo manda sobre el valor: un float bajo "gamma_protegido"
    se redacta igual que un string (los números también delatan).
    """
    base = key.lower().lstrip("_")
    if base in _SENSITIVE_FIELDS:
        return REDACTED
    if isinstance(value, dict):
        return {k: sanitize_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize_value(v, key) for v in value]
    if not isinstance(value, str):
        return value
    return redact_text(value)


class SanitizingFilter(logging.Filter):
    """Filtro de registro: redacta secretos en msg/args/extra."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        if isinstance(record.msg, str):
            record.msg = redact_text(record.msg)
        if record.args:
            try:
                record.args = sanitize_value(record.args)
            except Exception:  # noqa: BLE001 - nunca romper el logging
                record.args = (REDACTED,)
            if isinstance(record.args, dict):
                record.args = sanitize_value(record.args)
        if isinstance(getattr(record, "extra", None), dict):
            record.extra = sanitize_value(record.extra)
        return True


class JsonFormatter(logging.Formatter):
    """Un objeto JSON por línea: {ts, level, logger, msg, **extra}."""

    def format(self, record: logging.LogRecord) -> str:
        entry: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": redact_text(record.getMessage()),
        }
        extra = getattr(record, "extra", None)
        if isinstance(extra, dict):
            entry.update(sanitize_value(extra))
        # Campos estándar del LogRecord que la app haya puesto en `extra` vía
        # `log(..., extra={...})` ya pasan por sanitize_value; los demás se omiten.
        return json.dumps(entry, ensure_ascii=False, default=str)


def setup_json_logging(level: int = logging.INFO) -> logging.Handler:
    """Instala el handler JSON (sanitizado) en el logger raíz de app.

    Opt-in: create_app/run.py solo lo llaman con LOG_JSON=1. Devuelve el
    handler para que los tests puedan inspeccionarlo.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(SanitizingFilter())
    root = logging.getLogger("app")
    root.setLevel(level)
    root.addHandler(handler)
    return handler
