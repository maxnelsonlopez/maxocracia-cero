"""
Forms Blueprint - API endpoints for Red de Apoyo forms system.

Provides REST API for:
- Formulario CERO (Participant Registration)
- Formulario A (Exchange Registration)
- Formulario B (Follow-up Reports)
- Dashboard analytics
"""

from flask import Blueprint, jsonify, request

from .auth import token_required
from .forms_manager import FormsManager
from .utils import get_db

forms_bp = Blueprint("forms", __name__, url_prefix="/forms")


# ==================== FORMULARIO CERO ====================


@forms_bp.route("/participant", methods=["POST"])
def register_participant():
    """
    Register a new participant (Formulario CERO).

    Request body should include all required participant fields.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    db = get_db()
    manager = FormsManager(db)

    success, message, participant_id = manager.register_participant(data)

    if success:
        return (
            jsonify(
                {"success": True, "message": message, "participant_id": participant_id}
            ),
            201,
        )
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/participants", methods=["GET"])
@token_required
def get_participants(current_user):
    """
    Get list of participants with pagination.

    Query params:
    - limit: Number of results (default 50)
    - offset: Offset for pagination (default 0)
    - status: Filter by status (active/inactive/paused)
    """
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    status = request.args.get("status")

    # Validate limit
    if limit > 100:
        limit = 100

    db = get_db()
    manager = FormsManager(db)

    participants = manager.get_participants(limit=limit, offset=offset, status=status)

    return (
        jsonify(
            {
                "participants": participants,
                "count": len(participants),
                "limit": limit,
                "offset": offset,
            }
        ),
        200,
    )


@forms_bp.route("/participants/<int:participant_id>", methods=["GET"])
@token_required
def get_participant(current_user, participant_id):
    """Get details of a specific participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)

    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    return jsonify(participant), 200


# ==================== FORMULARIO A (EXCHANGES) ====================


@forms_bp.route("/exchange", methods=["POST"])
@token_required
def register_exchange(current_user):
    """
    Register an exchange (Formulario A).

    Request body should include all required exchange fields.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    db = get_db()
    manager = FormsManager(db)

    success, message, exchange_id = manager.register_exchange(data)

    if success:
        return (
            jsonify({"success": True, "message": message, "exchange_id": exchange_id}),
            201,
        )
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/exchanges", methods=["GET"])
@token_required
def get_exchanges(current_user):
    """
    Get list of exchanges with pagination and filters.

    Query params:
    - limit: Number of results (default 50)
    - offset: Offset for pagination (default 0)
    - urgency: Filter by urgency (Alta/Media/Baja)
    - giver_id: Filter by giver
    - receiver_id: Filter by receiver
    """
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    urgency = request.args.get("urgency")
    giver_id = request.args.get("giver_id", type=int)
    receiver_id = request.args.get("receiver_id", type=int)

    if limit > 100:
        limit = 100

    db = get_db()
    cursor = db.cursor()

    # Build query with filters
    query = "SELECT * FROM interchange WHERE 1=1"
    params = []

    if urgency:
        query += " AND urgency = ?"
        params.append(urgency)

    if giver_id:
        query += " AND giver_id = ?"
        params.append(giver_id)

    if receiver_id:
        query += " AND receiver_id = ?"
        params.append(receiver_id)

    query += " ORDER BY date DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)

    exchanges = []
    for row in cursor.fetchall():
        exchange = dict(zip([d[0] for d in cursor.description], row))
        exchanges.append(exchange)

    return (
        jsonify(
            {
                "exchanges": exchanges,
                "count": len(exchanges),
                "limit": limit,
                "offset": offset,
            }
        ),
        200,
    )


@forms_bp.route("/exchanges/<int:exchange_id>", methods=["GET"])
@token_required
def get_exchange(current_user, exchange_id):
    """Get details of a specific exchange."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM interchange WHERE id = ?", (exchange_id,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Intercambio no encontrado"}), 404

    exchange = dict(zip([d[0] for d in cursor.description], row))
    return jsonify(exchange), 200


# ==================== FORMULARIO B (FOLLOW-UPS) ====================


@forms_bp.route("/follow-up", methods=["POST"])
@token_required
def register_followup(current_user):
    """
    Register a follow-up report (Formulario B).

    Request body should include all required follow-up fields.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    db = get_db()
    manager = FormsManager(db)

    success, message, followup_id = manager.register_followup(data)

    if success:
        return (
            jsonify({"success": True, "message": message, "followup_id": followup_id}),
            201,
        )
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/follow-ups", methods=["GET"])
@token_required
def get_followups(current_user):
    """
    Get list of follow-ups with pagination and filters.

    Query params:
    - limit: Number of results (default 50)
    - offset: Offset for pagination (default 0)
    - priority: Filter by priority (high/medium/low/closed)
    - participant_id: Filter by participant
    """
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    priority = request.args.get("priority")
    participant_id = request.args.get("participant_id", type=int)

    if limit > 100:
        limit = 100

    db = get_db()
    cursor = db.cursor()

    # Build query with filters
    query = "SELECT * FROM follow_ups WHERE 1=1"
    params = []

    if priority:
        query += " AND follow_up_priority = ?"
        params.append(priority)

    if participant_id:
        query += " AND participant_id = ?"
        params.append(participant_id)

    query += " ORDER BY follow_up_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)

    followups = []
    for row in cursor.fetchall():
        followup = dict(zip([d[0] for d in cursor.description], row))
        # Parse JSON fields
        import json

        for field in ["new_needs_detected", "new_offers_detected", "actions_required"]:
            if followup.get(field):
                try:
                    followup[field] = json.loads(followup[field])
                except:
                    pass
        followups.append(followup)

    return (
        jsonify(
            {
                "follow_ups": followups,
                "count": len(followups),
                "limit": limit,
                "offset": offset,
            }
        ),
        200,
    )


@forms_bp.route("/follow-ups/participant/<int:participant_id>", methods=["GET"])
@token_required
def get_participant_followups(current_user, participant_id):
    """Get all follow-ups for a specific participant."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT * FROM follow_ups 
        WHERE participant_id = ? 
        ORDER BY follow_up_date DESC
    """,
        (participant_id,),
    )

    followups = []
    for row in cursor.fetchall():
        followup = dict(zip([d[0] for d in cursor.description], row))
        # Parse JSON fields
        import json

        for field in ["new_needs_detected", "new_offers_detected", "actions_required"]:
            if followup.get(field):
                try:
                    followup[field] = json.loads(followup[field])
                except:
                    pass
        followups.append(followup)

    return (
        jsonify(
            {
                "participant_id": participant_id,
                "follow_ups": followups,
                "count": len(followups),
            }
        ),
        200,
    )


# ==================== DASHBOARD ====================


@forms_bp.route("/dashboard/stats", methods=["GET"])
@token_required
def get_dashboard_stats(current_user):
    """
    Get aggregate statistics for the dashboard.

    Returns metrics like:
    - Total participants
    - Total exchanges
    - UTH mobilized
    - Urgency distribution
    - Resolution rate
    - Active alerts
    """
    db = get_db()
    manager = FormsManager(db)

    stats = manager.get_dashboard_stats()

    return jsonify(stats), 200


@forms_bp.route("/dashboard/alerts", methods=["GET"])
@token_required
def get_active_alerts(current_user):
    """
    Get all high-priority follow-ups that need immediate attention.
    """
    db = get_db()
    manager = FormsManager(db)

    alerts = manager.get_active_alerts()

    return jsonify({"alerts": alerts, "count": len(alerts)}), 200


@forms_bp.route("/dashboard/network", methods=["GET"])
@token_required
def get_network_flow(current_user):
    """
    Get network flow data (who gives, who receives, hub nodes).
    """
    db = get_db()
    manager = FormsManager(db)

    network = manager.get_network_flow()

    return jsonify(network), 200
