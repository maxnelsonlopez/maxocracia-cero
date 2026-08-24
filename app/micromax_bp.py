from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .micromax import MicroMaxManager

micromax_bp = Blueprint("micromax", __name__, url_prefix="/api/micromax")
manager = MicroMaxManager()


@micromax_bp.route("/household", methods=["POST"])
@token_required
def create_household(current_user):
    data = request.get_json() or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "El nombre del hogar es requerido."}), 400

    try:
        from .utils import get_db

        db = get_db()
        user_row = db.execute(
            "SELECT name, email FROM users WHERE id = ?", (current_user["user_id"],)
        ).fetchone()
        user_name = (
            user_row["name"]
            if (user_row and user_row["name"])
            else (
                user_row["email"]
                if user_row
                else current_user.get("email") or "Usuario"
            )
        )

        # Create household
        household = manager.create_household(name)
        # Automatically join the creator as a member
        join_res = manager.join_household(
            household["invite_code"], current_user["user_id"], user_name
        )
        return jsonify({"household": household, "member": join_res["member"]}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/household/join", methods=["POST"])
@token_required
def join_household(current_user):
    data = request.get_json() or {}
    invite_code = data.get("invite_code")

    if not invite_code:
        return jsonify({"error": "El código de invitación es requerido."}), 400

    try:
        from .utils import get_db

        db = get_db()
        user_row = db.execute(
            "SELECT name, email FROM users WHERE id = ?", (current_user["user_id"],)
        ).fetchone()
        user_name = (
            user_row["name"]
            if (user_row and user_row["name"])
            else (
                user_row["email"]
                if user_row
                else current_user.get("email") or "Usuario"
            )
        )

        res = manager.join_household(invite_code, current_user["user_id"], user_name)
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/household", methods=["GET"])
@token_required
def get_household(current_user):
    try:
        member = manager.get_member(current_user["user_id"])
        if not member:
            return jsonify({"household": None, "members": []}), 200

        from .utils import get_db

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM micromax_households WHERE id = ?", (member["household_id"],)
        )
        household = cursor.fetchone()

        if not household:
            return jsonify({"household": None, "members": []}), 200

        members = manager.get_household_members(member["household_id"])
        return jsonify({"household": dict(household), "members": members}), 200
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/member/config", methods=["POST"])
@token_required
def update_member_config(current_user):
    data = request.get_json() or {}

    # Validation helper
    try:
        monthly_income = float(data.get("monthly_income", 0))
        work_hours = float(data.get("work_hours", 0))
        travel_hours = float(data.get("travel_hours", 0))
        sleep_hours = float(data.get("sleep_hours", 56))
        ceh_mode = str(data.get("ceh_mode") or "bridge")
        hourly_rate = float(data.get("hourly_rate", 0))

        member = manager.update_member_config(
            current_user["user_id"],
            monthly_income,
            work_hours,
            travel_hours,
            sleep_hours,
            ceh_mode=ceh_mode,
            hourly_rate=hourly_rate,
        )
        return jsonify(member), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/cdd", methods=["POST"])
@token_required
def log_cdd(current_user):
    data = request.get_json() or {}

    required = [
        "task_name",
        "duration_hours",
        "effort_factor",
        "mental_factor",
        "scope_factor",
    ]
    for req in required:
        if req not in data:
            return jsonify({"error": f"Falta el campo requerido: {req}"}), 400

    try:
        log = manager.log_cdd(
            user_id=current_user["user_id"],
            task_name=data["task_name"],
            duration_hours=float(data["duration_hours"]),
            effort_factor=float(data["effort_factor"]),
            mental_factor=float(data["mental_factor"]),
            scope_factor=float(data["scope_factor"]),
            attention_factor=float(data.get("attention_factor", 1.0)),
            fragmentation_factor=float(data.get("fragmentation_factor", 1.0)),
            loneliness_factor=float(data.get("loneliness_factor", 1.0)),
            logged_date=data.get("logged_date"),
            v_ucv=float(data.get("v_ucv", 0.0)),
            r_units=float(data.get("r_units", 0.0)),
            r_notes=str(data.get("r_notes", "") or ""),
        )
        return jsonify(log), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/cdd", methods=["GET"])
@token_required
def get_cdd_logs(current_user):
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    try:
        logs = manager.get_cdd_logs(current_user["user_id"], limit, offset)
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/safety-survey", methods=["POST"])
@token_required
def save_safety_survey(current_user):
    data = request.get_json() or {}
    answers = data.get("answers")

    if not answers or not isinstance(answers, dict):
        return jsonify({"error": "Respuestas de la encuesta ESI requeridas."}), 400

    try:
        res = manager.save_safety_survey(
            current_user["user_id"],
            answers,
            wants_support=data.get("wants_support"),
        )
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/safety-survey", methods=["GET"])
@token_required
def get_safety_survey(current_user):
    try:
        survey = manager.get_safety_survey(current_user["user_id"])
        if not survey:
            return jsonify(None), 200
        return jsonify(survey), 200
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/audit", methods=["POST"])
@token_required
def log_audit(current_user):
    data = request.get_json() or {}

    required = [
        "audit_date",
        "conflicts_count",
        "weapon_count",
        "accusations_count",
        "threats_count",
    ]
    for req in required:
        if req not in data:
            return jsonify({"error": f"Falta el campo requerido: {req}"}), 400

    try:
        audit = manager.log_audit(
            user_id=current_user["user_id"],
            audit_date=data["audit_date"],
            conflicts_count=int(data["conflicts_count"]),
            weapon_count=int(data["weapon_count"]),
            accusations_count=int(data["accusations_count"]),
            threats_count=int(data["threats_count"]),
            s1_hours=float(data.get("s1_hours", 0)),
            s2_score=float(data.get("s2_score", 0)),
            s3_score=float(data.get("s3_score", 0)),
            s4_score=float(data.get("s4_score", 0)),
            s5_score=float(data.get("s5_score", 0)),
            duration_weeks=int(data.get("duration_weeks", 4)),
        )
        return jsonify(audit), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/audits", methods=["GET"])
@token_required
def get_audits(current_user):
    try:
        audits = manager.get_audits(current_user["user_id"])
        return jsonify(audits), 200
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/checkin", methods=["POST"])
@token_required
def log_checkin(current_user):
    """Check-in de gamma domestica (Cap. 16.5 s16.5.6): el latido del hogar."""
    data = request.get_json() or {}
    try:
        gamma = float(data.get("gamma"))
    except (TypeError, ValueError):
        return jsonify({"error": "Gamma debe ser un numero entre 0.5 y 1.5."}), 400

    try:
        res = manager.log_checkin(
            current_user["user_id"], gamma, note=str(data.get("note", "") or "")
        )
        return jsonify(res), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/checkins", methods=["GET"])
@token_required
def get_checkins(current_user):
    limit = request.args.get("limit", 30, type=int)
    try:
        return jsonify(manager.get_checkins(current_user["user_id"], limit)), 200
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@micromax_bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard(current_user):
    try:
        member = manager.get_member(current_user["user_id"])
        if not member:
            return (
                jsonify({"error": "No eres miembro de ningún hogar MicroMaxocracia."}),
                404,
            )

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        three_accounts = manager.calculate_three_accounts(
            member["household_id"],
            start_date,
            end_date,
            requester_user_id=current_user["user_id"],
        )
        toxicity = manager.calculate_toxicity_indices(
            member["household_id"], requester_user_id=current_user["user_id"]
        )
        wellbeing = manager.get_household_wellbeing(
            member["household_id"], requester_user_id=current_user["user_id"]
        )
        survey = manager.get_safety_survey(current_user["user_id"])

        return (
            jsonify(
                {
                    "three_accounts": three_accounts,
                    "toxicity": toxicity,
                    "wellbeing": wellbeing,
                    "safety_survey": survey,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
