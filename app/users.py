from flask import Blueprint, jsonify, request

from .jwt_utils import admin_required
from .utils import get_db

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=["GET"])
def list_users():
    db = get_db()
    cur = db.execute(
        "SELECT id, email, name, alias, city, neighborhood, created_at FROM users LIMIT 100"
    )
    users = [dict(row) for row in cur.fetchall()]
    return jsonify(users)


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    row = db.execute(
        "SELECT id, email, name, alias, city, neighborhood, values_json, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@bp.route("/<int:user_id>/trust", methods=["POST"])
@admin_required
def promote_trust(current_user, user_id):
    """
    Escalera de confianza (Cap. 13): asciende a un integrante de N0
    (recién llegado) a N1 (integrado) — la comunidad decide cuándo alguien
    tiene voz en la gobernanza. Registro auditable (T13).
    """
    db = get_db()
    row = db.execute(
        "SELECT id, email, trust_level FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    if int(row["trust_level"] or 0) >= 1:
        return jsonify({"success": True, "user_id": user_id, "trust_level": row["trust_level"]})

    db.execute("UPDATE users SET trust_level = 1 WHERE id = ?", (user_id,))
    db.execute(
        "INSERT INTO maxo_arrivals (email, source, honeypot_hit, status) VALUES (?, 'community_ascension', 0, 'promoted')",
        (str(row["email"]).strip().lower(),),
    )
    db.commit()
    return jsonify({"success": True, "user_id": user_id, "trust_level": 1})


@bp.route("", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    email = data.get("email")
    name = data.get("name")
    alias = data.get("alias")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    db = get_db()
    from werkzeug.security import generate_password_hash

    try:
        db.execute(
            "INSERT INTO users (email, name, alias, password_hash) VALUES (?, ?, ?, ?)",
            (email, name, alias, generate_password_hash(password)),
        )
        db.commit()
    except Exception:
        # Don't expose internal error details to prevent information leakage
        return jsonify({"error": "Failed to create user"}), 500
    return jsonify({"message": "user created"}), 201
