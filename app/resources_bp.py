from flask import Blueprint, jsonify, request
from .utils import get_db

bp = Blueprint("resources", __name__, url_prefix="/resources")


@bp.route("", methods=["POST"])
def create_resource():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    title = data.get("title")
    description = data.get("description")
    db = get_db()
    db.execute(
        "INSERT INTO resources (user_id, title, description, category, available) VALUES (?, ?, ?, ?, 1)",
        (user_id, title, description, data.get("category")),
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
def claim_resource(res_id):
    data = request.get_json() or {}
    user_id = data.get("user_id")
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
