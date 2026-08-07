"""
Perfil de protección de usuarios (Ola 3B, escalera de equidad).

Endpoints:
- GET  /protection/profile   - Mi perfil (declarado + efectivo + topes)
- POST /protection/profile   - Declarar mi nivel y acompañante
"""

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .protection import caps_for, get_profile, protection_level, set_profile
from .utils import get_db

protection_bp = Blueprint("protection", __name__, url_prefix="/protection")


@protection_bp.route("/profile", methods=["GET"])
@token_required
def my_profile(current_user):
    uid = current_user.get("user_id") or current_user.get("id")
    if uid is None:
        return jsonify({"error": "token sin identidad válida"}), 403
    uid = int(uid)
    profile = get_profile(uid)
    effective = protection_level(uid)
    return jsonify({
        "profile": profile,
        "protection_level": effective,
        "caps": caps_for(effective),
    })


@protection_bp.route("/profile", methods=["POST"])
@token_required
def update_my_profile(current_user):
    """
    Declarar mi nivel de protección (autodeclaración, T13).

    Body JSON:
    {
        "level": "assisted" | "shielded" | "standard",
        "companion_user_id": 5,        # opcional: acompañante humano
        "declared_age": 71,            # opcional
        "declared_education": "primaria"  # opcional
    }
    """
    uid = current_user.get("user_id") or current_user.get("id")
    if uid is None:
        return jsonify({"error": "token sin identidad válida"}), 403
    uid = int(uid)

    data = request.get_json() or {}
    level = data.get("level")
    if level not in ("standard", "assisted", "shielded"):
        return jsonify({"error": "level must be standard, assisted or shielded"}), 400

    companion = data.get("companion_user_id")
    if companion is not None:
        companion = int(companion)
        if companion == uid:
            return jsonify({"error": "no puedes ser tu propio acompañante"}), 400
        row = get_db().execute(
            "SELECT 1 FROM users WHERE id = ?", (companion,)
        ).fetchone()
        if row is None:
            return jsonify({"error": "acompañante no es un usuario real"}), 400

    declared_age = data.get("declared_age")
    if declared_age is not None:
        try:
            declared_age = int(declared_age)
        except (TypeError, ValueError):
            return jsonify({"error": "invalid declared_age"}), 400

    profile = set_profile(
        user_id=uid,
        level=level,
        companion_user_id=companion,
        declared_age=declared_age,
        declared_education=(data.get("declared_education") or "").strip() or None,
    )
    return jsonify({
        "success": True,
        "profile": profile,
        "protection_level": protection_level(uid),
    })
