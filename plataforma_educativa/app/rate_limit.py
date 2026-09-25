# -*- coding: utf-8 -*-
"""Límite básico de intentos para las rutas de autenticación.

La plataforma educativa quedó expuesta por el túnel de Cloudflare sin ningún
freno a la fuerza bruta. Este módulo añade una ventana deslizante en memoria
por (scope, IP, usuario) sin dependencias externas.

Cloudflare inyecta ``CF-Connecting-IP`` (no falsificable a través del túnel),
así que se usa como clave de IP; si no existe, cae a ``remote_addr``.

Nota de escala: el almacén vive en ``current_app.extensions`` (un proceso).
Si algún día hay varios workers, moverlo a Redis.
"""

import os
import threading
import time
from functools import wraps

from flask import current_app, jsonify, request

_LOCK = threading.Lock()
_DEFAULT_ATTEMPTS = 10
_DEFAULT_WINDOW = 60.0


def _client_ip():
    return (
        request.headers.get("CF-Connecting-IP") or request.remote_addr or "desconocida"
    )


def _number(key, default):
    value = current_app.config.get(key)
    if value is None:
        value = os.environ.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _store():
    return current_app.extensions.setdefault("auth_rate_limit", {})


def _hit(key):
    """Registra un intento. Devuelve (permitido, retry_after_segundos)."""
    attempts = _number("AUTH_RATE_LIMIT_ATTEMPTS", _DEFAULT_ATTEMPTS)
    window = _number("AUTH_RATE_LIMIT_WINDOW", _DEFAULT_WINDOW)
    now = time.monotonic()

    with _LOCK:
        events = [t for t in _store().get(key, []) if now - t < window]
        if len(events) >= attempts:
            retry = max(1, int(window - (now - events[0])) + 1)
            _store()[key] = events
            return False, retry
        events.append(now)
        _store()[key] = events
        return True, 0


def rate_limit(scope, username_field=None):
    """Decorador: limita intentos por IP y, opcionalmente, por usuario.

    ``username_field`` busca ese campo en el JSON para añadir una clave por
    identidad (evita que una sola cuenta sea bombardeada desde muchas IPs).
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if current_app.config.get("RATE_LIMIT_DISABLED"):
                return fn(*args, **kwargs)

            allowed, retry = _hit(f"{scope}:ip:{_client_ip()}")
            if not allowed:
                return _too_many(retry)

            if username_field:
                payload = request.get_json(silent=True) or {}
                username = str(payload.get(username_field) or "").strip().lower()
                if username:
                    allowed, retry = _hit(f"{scope}:user:{username}")
                    if not allowed:
                        return _too_many(retry)

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def _too_many(retry):
    response = jsonify(
        {"error": "Demasiados intentos. Espera un momento antes de reintentar."}
    )
    response.status_code = 429
    response.headers["Retry-After"] = str(retry)
    return response
