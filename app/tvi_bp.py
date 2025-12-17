from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .tvi import TVIManager

tvi_bp = Blueprint("tvi", __name__, url_prefix="/tvi")
tvi_manager = TVIManager()


@tvi_bp.route("", methods=["POST"])
@token_required
def log_tvi(current_user):
    data = request.get_json()

    required_fields = ["start_time", "end_time", "category"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    valid_categories = ["MAINTENANCE", "INVESTMENT", "WASTE", "WORK", "LEISURE"]
    if data["category"] not in valid_categories:
        return (
            jsonify({"error": f"Invalid category. Must be one of {valid_categories}"}),
            400,
        )

    try:
        user_id = current_user["user_id"]
        entry = tvi_manager.log_tvi(
            user_id=user_id,
            start_time=data["start_time"],
            end_time=data["end_time"],
            category=data["category"],
            description=data.get("description"),
        )
        return jsonify(entry), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error " + str(e)}), 500


@tvi_bp.route("", methods=["GET"])
@token_required
def get_tvis(current_user):
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    user_id = current_user["user_id"]
    entries = tvi_manager.get_user_tvis(user_id, limit, offset)
    return jsonify(entries), 200


@tvi_bp.route("/stats", methods=["GET"])
@token_required
def get_stats(current_user):
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    user_id = current_user["user_id"]
    stats = tvi_manager.calculate_ccp(user_id, start_date, end_date)
    return jsonify(stats), 200


@tvi_bp.route("/community-stats", methods=["GET"])
def get_community_stats():
    # Public endpoint (no token required) as per transparency incentive
    stats = tvi_manager.get_community_stats()
    return jsonify(stats), 200
