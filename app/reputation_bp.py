from flask import Blueprint, jsonify, request
from .utils import get_db

bp = Blueprint("reputation", __name__, url_prefix="/reputation")


@bp.route("/<int:user_id>", methods=["GET"])
def get_reputation(user_id):
    db = get_db()
    row = db.execute(
        "SELECT score, reviews_count FROM reputation WHERE user_id = ?", (user_id,)
    ).fetchone()
    if row is None:
        return jsonify({"user_id": user_id, "score": 0.0, "reviews_count": 0})
    return jsonify(
        {
            "user_id": user_id,
            "score": row["score"],
            "reviews_count": row["reviews_count"],
        }
    )


@bp.route("/review", methods=["POST"])
def add_review():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    score = float(data.get("score") or 0)
    db = get_db()
    cur = db.execute(
        "SELECT id, score, reviews_count FROM reputation WHERE user_id = ?", (user_id,)
    ).fetchone()
    if cur is None:
        db.execute(
            "INSERT INTO reputation (user_id, score, reviews_count, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (user_id, score, 1),
        )
    else:
        new_count = cur["reviews_count"] + 1
        new_score = ((cur["score"] * cur["reviews_count"]) + score) / new_count
        db.execute(
            "UPDATE reputation SET score = ?, reviews_count = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
            (new_score, new_count, user_id),
        )
    db.commit()
    return jsonify({"message": "review added"}), 201
