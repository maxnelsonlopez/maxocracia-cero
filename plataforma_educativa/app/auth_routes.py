# -*- coding: utf-8 -*-
"""Rutas de autenticación: registro y login."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import issue_token
from .db import get_db

auth_bp = Blueprint("auth", __name__)

# Roles: el primer usuario registrado es coordinador (ve "generar semana").
MAX_EMAIL_LEN = 254


def _count_users():
    row = get_db().execute("SELECT COUNT(*) AS n FROM users").fetchone()
    return row["n"]


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """Crea un usuario. El email es opcional (columna nullable)."""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = data.get("email") or ""

    if not username or not password:
        return jsonify({"error": "username y password son obligatorios."}), 400
    if email and len(email) > MAX_EMAIL_LEN:
        return jsonify({"error": "email demasiado largo."}), 400

    db = get_db()
    exists = db.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()
    if exists:
        return jsonify({"error": "El nombre de usuario ya existe."}), 409

    is_first = _count_users() == 0
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
def login():
    """Valida credenciales y devuelve un token nuevo."""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
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
