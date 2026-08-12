from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db

bp = Blueprint("resources", __name__, url_prefix="/resources")


@bp.route("", methods=["POST"])
@token_required
def create_resource(current_user):
    data = request.get_json() or {}
    uid = current_user.get("user_id")
    title = data.get("title")
    description = data.get("description")
    if uid is None or not title:
        return jsonify({"error": "título es requerido"}), 400
    db = get_db()
    db.execute(
        "INSERT INTO resources (user_id, title, description, category, available) VALUES (?, ?, ?, ?, 1)",
        (uid, title, description, data.get("category")),
    )
    db.commit()
    return jsonify({"message": "resource created"}), 201


@bp.route("", methods=["GET"])
def list_resources():
    db = get_db()
    cur = db.execute(
        "SELECT * FROM resources WHERE available = 1 ORDER BY created_at DESC"
    )
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)


@bp.route("/<int:res_id>/claim", methods=["POST"])
@token_required
def claim_resource(current_user, res_id):
    data = request.get_json() or {}
    requester_id = current_user.get("user_id")
    if requester_id is None:
        return jsonify({"error": "autenticación requerida"}), 401
    requester_id = int(requester_id)
    if data.get("requester_id") is not None and int(data.get("requester_id")) != requester_id:
        return jsonify({"error": "no puedes reclamar en nombre de otro usuario"}), 403
    db = get_db()
    cur = db.execute(
        "SELECT available FROM resources WHERE id = ?", (res_id,)
    ).fetchone()
    if cur is None:
        return jsonify({"error": "resource not found"}), 404
    if not cur["available"]:
        return jsonify({"error": "resource not available"}), 400
    db.execute("UPDATE resources SET available = 0 WHERE id = ?", (res_id,))
    db.commit()
    return jsonify({"message": "resource claimed"}), 200
