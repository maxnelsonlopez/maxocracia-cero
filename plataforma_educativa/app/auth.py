# -*- coding: utf-8 -*-
"""Autenticación por token simple.

Al iniciar sesión se emite un token aleatorio que se guarda en memoria
(``app.extensions["auth_tokens"]``, token -> user_id). Los endpoints protegidos
lo reciben en el encabezado ``X-Auth-Token``.

En producción se reemplazaría por un sistema de sesiones robusto (JWT o token
persistente en base de datos); para el MVP el token en memoria es suficiente y
conserva la propiedad de que "revisa el servidor" (los tokens no son
adivinables).
"""

import functools
import secrets

from flask import current_app, g, jsonify, request

_STORE_KEY = "auth_tokens"


def _store():
    return current_app.extensions.setdefault(_STORE_KEY, {})


def issue_token(user_id):
    """Emite un token nuevo para el usuario y lo registra en memoria."""
    token = secrets.token_hex(24)
    _store()[token] = user_id
    return token


def resolve_token(token):
    """Devuelve el user_id asociado a un token, o ``None``."""
    return _store().get(token)


def revoke_token(token):
    """Invalida un token (aunque el MVP no expone logout, queda el helper)."""
    _store().pop(token, None)


def login_required(fn):
    """Decorador: exige un token válido en ``X-Auth-Token``.

    Guarda el ``user_id`` autenticado en ``g.user_id`` para el resto del
    endpoint. Si el token falta o no es válido responde 401.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Auth-Token")
        user_id = resolve_token(token) if token else None
        if user_id is None:
            return jsonify({"error": "Autenticación requerida."}), 401
        g.user_id = user_id
        return fn(*args, **kwargs)

    return wrapper
