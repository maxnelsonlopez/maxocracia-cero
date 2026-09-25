# -*- coding: utf-8 -*-
"""Autenticación híbrida: tokens locales y síntesis de identidad JWT.

Soporta dos modalidades de acceso:
1. Tokens locales en memoria (``X-Auth-Token`` -> user_id), conservando la
   autonomía fractal del OEV cuando opera de forma independiente.
2. Tokens JWT de Maxocracia (``Authorization: Bearer <jwt>`` o ``X-Auth-Token``),
   permitiendo UNA sola puerta de acceso desde la plataforma principal con
   aprovisionamiento Just-In-Time (JIT) en la base local.
"""

import functools
import os
import secrets
import time
from datetime import datetime, timezone

import jwt
from flask import current_app, g, jsonify, request
from werkzeug.security import generate_password_hash

from .db import get_db

_STORE_KEY = "auth_tokens"
JWT_ALGORITHM = "HS256"


def _candidate_secrets():
    """Claves con las que se acepta verificar un JWT de Maxocracia.

    Orden: JWT_SECRET_KEY (clave dedicada de firma, migración recomendada) y
    SECRET_KEY (compatibilidad). Sin ninguna, la federación queda fail-closed:
    una constante pública en el código permitiría forjar JWTs.
    """
    candidates = []
    sources = []
    if current_app:
        sources.extend(
            [
                current_app.config.get("JWT_SECRET_KEY"),
                os.environ.get("JWT_SECRET_KEY"),
                # Gracia de rotación: la clave anterior sigue validando
                # mientras los clientes renuevan (se retira tras el periodo).
                current_app.config.get("JWT_SECRET_KEY_PREVIOUS"),
                os.environ.get("JWT_SECRET_KEY_PREVIOUS"),
                current_app.config.get("SECRET_KEY"),
            ]
        )
    sources.append(os.environ.get("SECRET_KEY"))
    for value in sources:
        if value and value not in candidates:
            candidates.append(value)
    return candidates


def _get_secret_key():
    """Primera clave candidata (o error si la federación no está configurada)."""
    candidate_keys = _candidate_secrets()
    if candidate_keys:
        return candidate_keys[0]
    raise RuntimeError(
        "SECRET_KEY no configurada en la Plataforma Educativa: la federación JWT "
        "requiere compartir la clave de Maxocracia (JWT_SECRET_KEY o SECRET_KEY)."
    )


def _store():
    return current_app.extensions.setdefault(_STORE_KEY, {})


def _token_ttl():
    """Vida útil del token local en segundos (default 30 días).

    ``PLATAFORMA_EDUCATIVA_TOKEN_TTL=0`` lo expira de inmediato (tests).
    """
    raw = os.environ.get("PLATAFORMA_EDUCATIVA_TOKEN_TTL", str(30 * 24 * 3600))
    try:
        return max(0.0, float(raw))
    except (TypeError, ValueError):
        return 30 * 24 * 3600.0


def issue_token(user_id):
    """Emite un token nuevo para el usuario y lo registra en memoria con su
    fecha de emisión (antes vivía para siempre)."""
    token = secrets.token_hex(24)
    _store()[token] = {"user_id": user_id, "issued_at": time.time()}
    return token


def resolve_token(token):
    """Devuelve el user_id asociado a un token local vigente, o ``None``.

    Un token expirado se elimina del almacén y no vuelve a servir.
    """
    entry = _store().get(token)
    if not entry:
        return None
    if time.time() - entry["issued_at"] > _token_ttl():
        _store().pop(token, None)
        return None
    return entry["user_id"]


def revoke_token(token):
    """Invalida un token en memoria."""
    _store().pop(token, None)


def _resolve_jwt_user(token):
    """Verifica un JWT de Maxocracia y resuelve o aprovisiona (JIT) el usuario local.

    Returns:
        tuple (local_user_id, maxo_user_id) o None si el token es inválido.
    """
    candidate_keys = _candidate_secrets()
    if not candidate_keys:
        raise RuntimeError(
            "SECRET_KEY no configurada en la Plataforma Educativa: la federación "
            "JWT requiere compartir la clave de Maxocracia (JWT_SECRET_KEY o "
            "SECRET_KEY)."
        )

    payload = None
    for secret in candidate_keys:
        try:
            payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
            break
        except jwt.ExpiredSignatureError:
            # Firma válida pero vencida: no insistir con otra clave.
            return None
        except jwt.InvalidTokenError:
            continue
        except Exception:
            continue
    if payload is None:
        return None

    maxo_user_id = payload.get("user_id")
    if not maxo_user_id:
        return None

    email = payload.get("email")
    is_admin = bool(payload.get("is_admin"))
    alias = payload.get("alias") or payload.get("name")

    db = get_db()
    # 1. Buscar por maxo_user_id vinculado
    row = db.execute(
        "SELECT * FROM users WHERE maxo_user_id = ?", (maxo_user_id,)
    ).fetchone()
    if row:
        # Sincronizar rol de coordinador si el usuario es admin en Maxocracia
        if is_admin and not row["is_coordinator"]:
            db.execute("UPDATE users SET is_coordinator = 1 WHERE id = ?", (row["id"],))
            db.commit()
        return row["id"], maxo_user_id

    # 2. Buscar por email si existe
    if email:
        row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            db.execute(
                "UPDATE users SET maxo_user_id = ?, is_coordinator = MAX(is_coordinator, ?) WHERE id = ?",
                (maxo_user_id, 1 if is_admin else 0, row["id"]),
            )
            db.commit()
            return row["id"], maxo_user_id

    # 3. Aprovisionamiento JIT de nuevo usuario federado
    base_username = (
        alias or (email.split("@")[0] if email else f"user_{maxo_user_id}")
    ).strip()
    if not base_username:
        base_username = f"user_{maxo_user_id}"

    # Evitar colisión de username local
    candidate_username = base_username
    counter = 1
    while True:
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (candidate_username,)
        ).fetchone()
        if not existing:
            break
        candidate_username = f"{base_username}_{counter}"
        counter += 1

    cur = db.execute(
        "INSERT INTO users (username, password_hash, email, is_coordinator, maxo_user_id, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            candidate_username,
            generate_password_hash(secrets.token_hex(16)),
            email or None,
            1 if is_admin else 0,
            maxo_user_id,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    db.commit()
    return cur.lastrowid, maxo_user_id


def extract_token_from_request():
    """Extrae el token de autenticación de las cabeceras (X-Auth-Token o Authorization: Bearer)."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()
    return request.headers.get("X-Auth-Token")


def login_required(fn):
    """Decorador: exige un token válido (local en memoria o JWT federado).

    Guarda en ``g``:
    - ``g.user_id``: ID de usuario local en la base del OEV.
    - ``g.maxo_user_id``: ID de usuario en Maxocracia si es federado (o None).
    - ``g.is_federated``: booleano indicando si la sesión proviene de Maxocracia.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        token = extract_token_from_request()
        if not token:
            return jsonify({"error": "Autenticación requerida."}), 401

        # 1. Intentar resolver como token local en memoria
        local_user_id = resolve_token(token)
        if local_user_id is not None:
            g.user_id = local_user_id
            g.maxo_user_id = None
            g.is_federated = False
            return fn(*args, **kwargs)

        # 2. Intentar resolver como JWT federado de Maxocracia
        try:
            jwt_result = _resolve_jwt_user(token)
        except RuntimeError as exc:
            return (
                jsonify({"error": str(exc), "code": "FEDERATION_NOT_CONFIGURED"}),
                503,
            )
        if jwt_result is not None:
            g.user_id, g.maxo_user_id = jwt_result
            g.is_federated = True
            return fn(*args, **kwargs)

        return jsonify({"error": "Autenticación requerida."}), 401

    return wrapper
