# -*- coding: utf-8 -*-
"""Rutas de autenticación: registro y login."""

import hmac
import os
import sqlite3
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import issue_token
from .db import get_db
from .rate_limit import rate_limit

auth_bp = Blueprint("auth", __name__)

# Roles: el primer usuario registrado es coordinador (ve "generar semana").
# El rol se funda SOLO desde casa (sin túnel) o con el token de bootstrap:
# si la BD se recrea, un desconocido por la puerta pública no puede reclamar
# el mando. PLATAFORMA_EDUCATIVA_BOOTSTRAP_TOKEN habilita fundarlo remoto.
MAX_EMAIL_LEN = 254
USERNAME_MIN_LEN = 2
USERNAME_MAX_LEN = 50
PASSWORD_MIN_LEN = 6
PASSWORD_MAX_LEN = 128


def _count_users():
    row = get_db().execute("SELECT COUNT(*) AS n FROM users").fetchone()
    return row["n"]


def _puede_fundar_coordinador():
    """True si este registro puede reclamar el rol fundador.

    Por la puerta pública (Cloudflare inyecta `CF-Connecting-IP`) NO se funda:
    una BD nueva no le entrega el mando al primero que llegue. Desde casa
    (sin cabecera de túnel) o con el token de bootstrap sí.
    """
    bootstrap = os.environ.get("PLATAFORMA_EDUCATIVA_BOOTSTRAP_TOKEN", "")
    presented = request.headers.get("X-Bootstrap-Token", "")
    if bootstrap and hmac.compare_digest(presented, bootstrap):
        return True
    return not request.headers.get("CF-Connecting-IP")


@auth_bp.route("/api/auth/register", methods=["POST"])
@rate_limit("register", username_field="username")
def register():
    """Crea un usuario. El email es opcional (columna nullable)."""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = data.get("email") or ""

    if not username or not password:
        return jsonify({"error": "username y password son obligatorios."}), 400
    if not (USERNAME_MIN_LEN <= len(username) <= USERNAME_MAX_LEN) or any(
        c in username for c in "\r\n\t"
    ):
        return (
            jsonify(
                {
                    "error": (
                        f"username inválido: entre {USERNAME_MIN_LEN} y "
                        f"{USERNAME_MAX_LEN} caracteres, sin saltos de línea."
                    )
                }
            ),
            400,
        )
    if not (PASSWORD_MIN_LEN <= len(password) <= PASSWORD_MAX_LEN):
        return (
            jsonify(
                {
                    "error": (
                        f"password inválido: entre {PASSWORD_MIN_LEN} y "
                        f"{PASSWORD_MAX_LEN} caracteres."
                    )
                }
            ),
            400,
        )
    if email and len(email) > MAX_EMAIL_LEN:
        return jsonify({"error": "email demasiado largo."}), 400

    db = get_db()
    try:
        # BEGIN IMMEDIATE serializa el conteo con la inserción: sin esto dos
        # registros simultáneos en una BD vacía podrían fundar dos coordinadores.
        db.execute("BEGIN IMMEDIATE")

        exists = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if exists:
            db.rollback()
            return jsonify({"error": "El nombre de usuario ya existe."}), 409

        is_first = _count_users() == 0 and _puede_fundar_coordinador()
        cur = db.execute(
            "INSERT INTO users (username, password_hash, email, is_coordinator, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                username,
                generate_password_hash(password),
                email or None,
                1 if is_first else 0,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        db.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        db.rollback()
        return jsonify({"error": "El nombre de usuario ya existe."}), 409
    except Exception:
        db.rollback()
        raise

    token = issue_token(user_id)

    return (
        jsonify(
            {
                "token": token,
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": email or None,
                    "is_coordinator": bool(is_first),
                },
            }
        ),
        201,
    )


@auth_bp.route("/api/auth/login", methods=["POST"])
@rate_limit("login", username_field="username")
def login():
    """Valida credenciales y devuelve un token nuevo."""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Credenciales inválidas."}), 401

    token = issue_token(user["id"])
    return (
        jsonify(
            {
                "token": token,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "is_coordinator": bool(user["is_coordinator"]),
                },
            }
        ),
        200,
    )
