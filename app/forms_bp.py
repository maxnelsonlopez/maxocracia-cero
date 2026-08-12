"""
Forms Blueprint - API endpoints for Red de Apoyo forms system.

Provides REST API for:
- Formulario CERO (Participant Registration)
- Formulario A (Exchange Registration)
- Formulario B (Follow-up Reports)
- Dashboard analytics
- Matching Engine (Motor de Emparejamiento SDV)
"""

import sqlite3

from flask import Blueprint, jsonify, request

from .auth import token_required
from .forms_manager import FormsManager
from .matching import MatchingEngine
from .sdv_analyzer import SDVAnalyzer
from .utils import get_db

forms_bp = Blueprint("forms", __name__, url_prefix="/forms")

FOLLOW_UP_TYPES = (
    "verification_completed",
    "update_in_progress",
    "situation_evolution",
    "new_urgent_need",
    "need_resolved",
    "spontaneous_feedback",
    "routine_check",
)
FOLLOW_UP_PRIORITIES = ("high", "medium", "low", "closed")
SITUATION_CHANGES = (
    "improved_significantly",
    "improved_slightly",
    "same",
    "worsened_slightly",
    "worsened_significantly",
    "first_evaluation",
)
ACTIVE_INTERCHANGES_STATUSES = ("receiving_help", "giving_help", "both", "none", "paused")
INTERCHANGES_WORKING_WELL = ("very_well", "minor_difficulties", "significant_problems", "needs_adjustment")
EMOTIONAL_STATES = ("very_good", "good", "neutral", "worried", "bad", "alert_signs", "could_not_evaluate")


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
    search = request.args.get("search")

    # Validate limit
    if limit > 100:
        limit = 100

    db = get_db()
    manager = FormsManager(db)

    participants = manager.get_participants(
        limit=limit, offset=offset, status=status, search=search
    )

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


@forms_bp.route("/participants/<int:participant_id>", methods=["PUT"])
@token_required
def update_participant(current_user, participant_id):
    """Update details of a specific participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    # Authorization check: must be owner or admin
    if participant["email"] != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización para realizar esta acción"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    success, message = manager.update_participant(participant_id, data)
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/participants/<int:participant_id>", methods=["DELETE"])
@token_required
def delete_participant(current_user, participant_id):
    """Delete a specific participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    # Authorization check: must be owner or admin
    if participant["email"] != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización para realizar esta acción"}), 403

    success, message = manager.delete_participant(participant_id)
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/participants/<int:participant_id>/offers", methods=["GET"])
@token_required
def get_participant_offers(current_user, participant_id):
    """Get all secondary offers of a participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    # Authorization check: must be owner or admin
    if participant["email"] != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    offers = manager.get_participant_offers(participant_id)
    return jsonify({"offers": offers}), 200


@forms_bp.route("/participants/<int:participant_id>/offers", methods=["POST"])
@token_required
def add_participant_offer(current_user, participant_id):
    """Add a secondary offer for a participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    # Authorization check: must be owner or admin
    if participant["email"] != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    success, message, offer_id = manager.add_participant_offer(participant_id, data)
    if success:
        return jsonify({"success": True, "message": message, "offer_id": offer_id}), 201
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/offers/<int:offer_id>", methods=["PUT"])
@token_required
def update_offer(current_user, offer_id):
    """Update a secondary offer."""
    db = get_db()
    manager = FormsManager(db)

    # Authorization check
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.email FROM participants p
        JOIN participant_offers o ON p.id = o.participant_id
        WHERE o.id = ?
    """, (offer_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Oferta no encontrada"}), 404

    email = row[0]
    if email != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    success, message = manager.update_participant_offer(offer_id, data)
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/offers/<int:offer_id>", methods=["DELETE"])
@token_required
def delete_offer(current_user, offer_id):
    """Delete a secondary offer."""
    db = get_db()
    manager = FormsManager(db)

    # Authorization check
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.email FROM participants p
        JOIN participant_offers o ON p.id = o.participant_id
        WHERE o.id = ?
    """, (offer_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Oferta no encontrada"}), 404

    email = row[0]
    if email != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    success, message = manager.delete_participant_offer(offer_id)
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/participants/<int:participant_id>/needs", methods=["GET"])
@token_required
def get_participant_needs(current_user, participant_id):
    """Get all secondary needs of a participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    # Authorization check: must be owner or admin
    if participant["email"] != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    needs = manager.get_participant_needs(participant_id)
    return jsonify({"needs": needs}), 200


@forms_bp.route("/participants/<int:participant_id>/needs", methods=["POST"])
@token_required
def add_participant_need(current_user, participant_id):
    """Add a secondary need for a participant."""
    db = get_db()
    manager = FormsManager(db)

    participant = manager.get_participant(participant_id)
    if not participant:
        return jsonify({"error": "Participante no encontrado"}), 404

    # Authorization check: must be owner or admin
    if participant["email"] != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    success, message, need_id = manager.add_participant_need(participant_id, data)
    if success:
        return jsonify({"success": True, "message": message, "need_id": need_id}), 201
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/needs/<int:need_id>", methods=["PUT"])
@token_required
def update_need(current_user, need_id):
    """Update a secondary need."""
    db = get_db()
    manager = FormsManager(db)

    # Authorization check
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.email FROM participants p
        JOIN participant_needs n ON p.id = n.participant_id
        WHERE n.id = ?
    """, (need_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Necesidad no encontrada"}), 404

    email = row[0]
    if email != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    success, message = manager.update_participant_need(need_id, data)
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": message}), 400


@forms_bp.route("/needs/<int:need_id>", methods=["DELETE"])
@token_required
def delete_need(current_user, need_id):
    """Delete a secondary need."""
    db = get_db()
    manager = FormsManager(db)

    # Authorization check
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.email FROM participants p
        JOIN participant_needs n ON p.id = n.participant_id
        WHERE n.id = ?
    """, (need_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Necesidad no encontrada"}), 404

    email = row[0]
    if email != current_user.get("email") and not current_user.get("is_admin"):
        return jsonify({"error": "No tienes autorización"}), 403

    success, message = manager.delete_participant_need(need_id)
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": message}), 400


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


@forms_bp.route("/exchanges/<int:exchange_id>", methods=["PUT"])
@token_required
def update_exchange(current_user, exchange_id):
    """
    Actualiza un intercambio.

    Solo permite modificar campos existentes en la tabla `interchange`.
    Autorización: admin o alguna de las partes del intercambio (giver/receiver).
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM interchange WHERE id = ?", (exchange_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Intercambio no encontrado"}), 404

    exchange = dict(zip([d[0] for d in cursor.description], row))
    if not current_user.get("is_admin"):
        user_id = current_user.get("user_id")
        if user_id not in (exchange.get("giver_id"), exchange.get("receiver_id")):
            return jsonify({"error": "No tienes autorización para realizar esta acción"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    editable_fields = [
        "date", "giver_id", "receiver_id", "type", "description", "urgency",
        "uth_hours", "uvc_score", "urf_units", "urf_description",
        "economic_value_approx", "vhv_time_seconds", "vhv_lives",
        "vhv_resources_json", "impact_resolution_score", "reciprocity_status",
        "human_dimension_attended", "coordination_method",
        "requires_followup", "followup_scheduled_date", "facilitator_notes",
    ]

    updates = {k: v for k, v in data.items() if k in editable_fields}
    if not updates:
        return jsonify({"error": "No se proporcionaron campos válidos"}), 400

    if "urgency" in updates and updates["urgency"] not in ("Alta", "Media", "Baja"):
        return jsonify({"error": "Urgencia inválida"}), 400

    if "coordination_method" in updates and updates["coordination_method"] not in (
        "max_direct", "participants_alone", "intermediary", "other"
    ):
        return jsonify({"error": "Método de coordinación inválido"}), 400

    try:
        set_clause = ", ".join(f"{field} = ?" for field in updates)
        cursor.execute(
            f"UPDATE interchange SET {set_clause} WHERE id = ?",
            list(updates.values()) + [exchange_id],
        )
        db.commit()
        return jsonify({"success": True, "message": "Intercambio actualizado exitosamente"}), 200
    except sqlite3.Error as e:
        return jsonify({"success": False, "error": f"Error de base de datos: {e}"}), 400


@forms_bp.route("/exchanges/<int:exchange_id>", methods=["DELETE"])
@token_required
def delete_exchange(current_user, exchange_id):
    """
    Elimina un intercambio.

    Autorización: admin o alguna de las partes del intercambio (giver/receiver).
    Los seguimientos asociados conservan su `related_interchange_id` en NULL
    (ON DELETE SET NULL en el esquema).
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT giver_id, receiver_id FROM interchange WHERE id = ?", (exchange_id,)
    )
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Intercambio no encontrado"}), 404

    giver_id, receiver_id = row
    if not current_user.get("is_admin"):
        user_id = current_user.get("user_id")
        if user_id not in (giver_id, receiver_id):
            return jsonify({"error": "No tienes autorización para realizar esta acción"}), 403

    cursor.execute("DELETE FROM interchange WHERE id = ?", (exchange_id,))
    db.commit()
    return jsonify({"success": True, "message": "Intercambio eliminado exitosamente"}), 200


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

    # JSON fields to parse in follow-up records
    json_fields = ["new_needs_detected", "new_offers_detected", "actions_required"]

    followups = []
    for row in cursor.fetchall():
        followup = dict(zip([d[0] for d in cursor.description], row))
        # Use FormsManager helper to parse JSON fields
        FormsManager._parse_json_fields(followup, json_fields)
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

    # JSON fields to parse in follow-up records
    json_fields = ["new_needs_detected", "new_offers_detected", "actions_required"]

    followups = []
    for row in cursor.fetchall():
        followup = dict(zip([d[0] for d in cursor.description], row))
        # Use FormsManager helper to parse JSON fields
        FormsManager._parse_json_fields(followup, json_fields)
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


@forms_bp.route("/follow-ups/<int:followup_id>", methods=["PUT"])
@token_required
def update_followup(current_user, followup_id):
    """
    Actualiza un seguimiento.

    Solo permite modificar campos existentes en la tabla `follow_ups`.
    Autorización: admin o el participante asociado al seguimiento.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT fu.*, p.email AS participant_email
        FROM follow_ups fu
        LEFT JOIN participants p ON p.id = fu.participant_id
        WHERE fu.id = ?
        """,
        (followup_id,),
    )
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Seguimiento no encontrado"}), 404

    followup = dict(zip([d[0] for d in cursor.description], row))
    if not current_user.get("is_admin"):
        email = current_user.get("email")
        if not email or followup.get("participant_email") != email:
            return jsonify({"error": "No tienes autorización para realizar esta acción"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    editable_fields = [
        "follow_up_date", "participant_id", "related_interchange_id",
        "follow_up_type", "current_situation", "need_level", "situation_change",
        "active_interchanges_status", "interchanges_working_well",
        "new_needs_detected", "new_offers_detected", "emotional_state",
        "community_connection", "actions_required", "follow_up_priority",
        "next_follow_up_date", "facilitator_notes", "learnings",
    ]

    updates = {k: v for k, v in data.items() if k in editable_fields}
    if not updates:
        return jsonify({"error": "No se proporcionaron campos válidos"}), 400

    if "follow_up_type" in updates and updates["follow_up_type"] not in FOLLOW_UP_TYPES:
        return jsonify({"error": "Tipo de seguimiento inválido"}), 400

    if "follow_up_priority" in updates and updates["follow_up_priority"] not in FOLLOW_UP_PRIORITIES:
        return jsonify({"error": "Prioridad de seguimiento inválida"}), 400

    if "situation_change" in updates and updates["situation_change"] not in SITUATION_CHANGES:
        return jsonify({"error": "Cambio de situación inválido"}), 400

    if "active_interchanges_status" in updates and updates["active_interchanges_status"] not in ACTIVE_INTERCHANGES_STATUSES:
        return jsonify({"error": "Estado de intercambios activos inválido"}), 400

    if "interchanges_working_well" in updates and updates["interchanges_working_well"] not in INTERCHANGES_WORKING_WELL:
        return jsonify({"error": "Valor de funcionamiento de intercambios inválido"}), 400

    if "emotional_state" in updates and updates["emotional_state"] not in EMOTIONAL_STATES:
        return jsonify({"error": "Estado emocional inválido"}), 400

    if "need_level" in updates and updates["need_level"] is not None:
        try:
            need_level = int(updates["need_level"])
            if need_level < 1 or need_level > 5:
                return jsonify({"error": "Nivel de necesidad inválido"}), 400
            updates["need_level"] = need_level
        except (ValueError, TypeError):
            return jsonify({"error": "Nivel de necesidad inválido"}), 400

    if "community_connection" in updates and updates["community_connection"] is not None:
        try:
            connection = int(updates["community_connection"])
            if connection < 1 or connection > 5:
                return jsonify({"error": "Conexión comunitaria inválida"}), 400
            updates["community_connection"] = connection
        except (ValueError, TypeError):
            return jsonify({"error": "Conexión comunitaria inválida"}), 400

    for field in ("new_needs_detected", "new_offers_detected", "actions_required"):
        if field in updates and updates[field] is not None:
            updates[field] = FormsManager._safe_json_dump(updates[field])

    try:
        set_clause = ", ".join(f"{field} = ?" for field in updates)
        cursor.execute(
            f"UPDATE follow_ups SET {set_clause} WHERE id = ?",
            list(updates.values()) + [followup_id],
        )
        db.commit()
        return jsonify({"success": True, "message": "Seguimiento actualizado exitosamente"}), 200
    except sqlite3.Error as e:
        return jsonify({"success": False, "error": f"Error de base de datos: {e}"}), 400


@forms_bp.route("/follow-ups/<int:followup_id>", methods=["DELETE"])
@token_required
def delete_followup(current_user, followup_id):
    """
    Elimina un seguimiento.

    Autorización: admin o el participante asociado al seguimiento.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT fu.participant_id, p.email AS participant_email
        FROM follow_ups fu
        LEFT JOIN participants p ON p.id = fu.participant_id
        WHERE fu.id = ?
        """,
        (followup_id,),
    )
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Seguimiento no encontrado"}), 404

    participant_id, participant_email = row
    if not current_user.get("is_admin"):
        email = current_user.get("email")
        if not email or participant_email != email:
            return jsonify({"error": "No tienes autorización para realizar esta acción"}), 403

    cursor.execute("DELETE FROM follow_ups WHERE id = ?", (followup_id,))
    db.commit()
    return jsonify({"success": True, "message": "Seguimiento eliminado exitosamente"}), 200


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

    # We return the full graph data for the React Flow visualization
    network = manager.get_full_network_graph()

    # Merge network flow metrics (top_givers, top_receivers, hub_nodes) for test compliance
    network_flow = manager.get_network_flow()
    network.update(network_flow)

    return jsonify(network), 200


@forms_bp.route("/dashboard/trends", methods=["GET"])
@token_required
def get_trends(current_user):
    """
    Get temporal trends for dashboard visualizations.

    Query params:
    - period: Number of days to analyze (default 30)
    """
    period = request.args.get("period", 30, type=int)
    db = get_db()
    manager = FormsManager(db)
    trends = manager.get_temporal_trends(period)
    return jsonify(trends), 200


@forms_bp.route("/dashboard/categories", methods=["GET"])
@token_required
def get_categories(current_user):
    """Get category breakdown analysis."""
    db = get_db()
    manager = FormsManager(db)
    categories = manager.get_category_breakdown()
    return jsonify(categories), 200


@forms_bp.route("/dashboard/resolution", methods=["GET"])
@token_required
def get_resolution(current_user):
    """Get resolution metrics and effectiveness analysis."""
    db = get_db()
    manager = FormsManager(db)
    resolution = manager.get_resolution_metrics()
    return jsonify(resolution), 200


# ==================== MOTOR DE MATCHING ====================


def _match_result_to_dict(m) -> dict:
    """Convierte un MatchResult dataclass a dict JSON-serializable."""
    return {
        "offerer_id": m.offerer_id,
        "offerer_name": m.offerer_name,
        "offerer_city": m.offerer_city,
        "offerer_neighborhood": m.offerer_neighborhood,
        "offerer_phone_whatsapp": m.offerer_phone_whatsapp,
        "offerer_telegram": m.offerer_telegram,
        "matched_categories": m.matched_categories,
        "offerer_description": m.offerer_description,
        "offerer_dimensions": m.offerer_dimensions,
        "compatibility_score": m.compatibility_score,
        "urgency_weight": m.urgency_weight,
        "same_city": m.same_city,
        "same_neighborhood": m.same_neighborhood,
        "recently_exchanged": m.recently_exchanged,
    }


def _urgent_need_to_dict(u) -> dict:
    """Convierte un UrgentNeed dataclass a dict JSON-serializable."""
    return {
        "participant_id": u.participant_id,
        "participant_name": u.participant_name,
        "city": u.city,
        "neighborhood": u.neighborhood,
        "need_description": u.need_description,
        "need_urgency": u.need_urgency,
        "need_categories": u.need_categories,
        "need_dimensions": u.need_dimensions,
        "days_without_exchange": u.days_without_exchange,
        "latest_need_level": u.latest_need_level,
        "is_coherence_crime": u.is_coherence_crime,
        "top_matches": [_match_result_to_dict(m) for m in u.top_matches],
        "phone_whatsapp": u.phone_whatsapp,
        "telegram": u.telegram,
    }


def _gap_to_dict(g) -> dict:
    """Convierte un CommunityGap dataclass a dict JSON-serializable."""
    return {
        "dimension": g.dimension,
        "dimension_label": g.dimension_label,
        "participants_needing": g.participants_needing,
        "participants_offering": g.participants_offering,
        "coverage_ratio": g.coverage_ratio,
        "gap_severity": g.gap_severity,
    }


@forms_bp.route("/matching/participant/<int:participant_id>", methods=["GET"])
@token_required
def get_matches_for_participant(current_user, participant_id):
    """
    Retorna los mejores matches para un participante dado.

    Query params:
    - limit: Número máximo de resultados (default 10)
    - exclude_recent: Excluir pares recientes (default true)
    """
    limit = request.args.get("limit", 10, type=int)
    exclude_recent = request.args.get("exclude_recent", "true").lower() != "false"

    db = get_db()
    engine = MatchingEngine(db)

    matches = engine.find_matches(
        seeker_id=participant_id, limit=limit, exclude_recent=exclude_recent
    )

    return jsonify({
        "participant_id": participant_id,
        "matches": [_match_result_to_dict(m) for m in matches],
        "count": len(matches),
    }), 200


@forms_bp.route("/matching/urgent", methods=["GET"])
@token_required
def get_urgent_needs(current_user):
    """
    Retorna participantes con necesidad urgente sin resolver.

    Los marcados como is_coherence_crime=true son Alertas de Crimen de
    Coherencia SDV y deben recibir atención inmediata de toda la comunidad.

    Query params:
    - days_threshold: Días sin intercambio para considerar urgente (default 7)
    - top_matches: Cuántos matches incluir por participante (default 3)
    """
    days_threshold = request.args.get("days_threshold", 7, type=int)
    top_matches = request.args.get("top_matches", 3, type=int)

    db = get_db()
    engine = MatchingEngine(db)

    urgent = engine.get_urgent_unmet_needs(
        days_threshold=days_threshold, top_matches=top_matches
    )

    coherence_crimes = [u for u in urgent if u.is_coherence_crime]
    warnings = [u for u in urgent if not u.is_coherence_crime]

    return jsonify({
        "coherence_crimes": [_urgent_need_to_dict(u) for u in coherence_crimes],
        "warnings": [_urgent_need_to_dict(u) for u in warnings],
        "total_urgent": len(urgent),
        "crimes_count": len(coherence_crimes),
        "system_alert": len(coherence_crimes) > 0,
    }), 200


@forms_bp.route("/matching/gaps", methods=["GET"])
@token_required
def get_community_gaps(current_user):
    """
    Retorna el análisis de brechas de cobertura por dimensión humana
    en la comunidad actual de la Cohorte Cero.

    Sirve para identificar qué necesidades la red no puede cubrir sola
    y planificar incorporación de nuevos participantes con esas capacidades.
    """
    db = get_db()
    engine = MatchingEngine(db)

    gaps = engine.get_community_sdv_gaps()

    critical = [g for g in gaps if g.gap_severity == "critical"]
    warnings = [g for g in gaps if g.gap_severity == "warning"]
    covered = [g for g in gaps if g.gap_severity == "ok"]

    return jsonify({
        "gaps": [_gap_to_dict(g) for g in gaps],
        "critical": [_gap_to_dict(g) for g in critical],
        "warnings": [_gap_to_dict(g) for g in warnings],
        "covered": [_gap_to_dict(g) for g in covered],
        "critical_count": len(critical),
    }), 200


@forms_bp.route("/matching/summary", methods=["GET"])
@token_required
def get_matching_summary(current_user):
    """
    Resumen ejecutivo del motor de matching para el dashboard principal.
    Incluye conteos de alertas y nivel de alerta general del sistema.
    """
    db = get_db()
    engine = MatchingEngine(db)
    summary = engine.get_matching_summary()
    return jsonify(summary), 200


# ==================== SDV ANALYSIS ====================


@forms_bp.route("/sdv/participant/<int:p_id>", methods=["GET"])
@token_required
def get_participant_sdv(current_user, p_id):
    """Retorna el estado de dignidad vital estimado de un participante con narrativa."""
    db = get_db()
    analyzer = SDVAnalyzer(db)
    analysis = analyzer.get_participant_analysis(p_id)
    return jsonify(analysis), 200


@forms_bp.route("/sdv/community", methods=["GET"])
@token_required
def get_community_sdv(current_user):
    """Retorna el estatus agregado de la Cohorte Cero con resumen narrativo."""
    db = get_db()
    analyzer = SDVAnalyzer(db)
    status = analyzer.get_community_sdv_status()
    
    # Agregar narrativa comunitaria básica
    avg = status["average_overall"]
    if avg >= 0.9:
        status["community_narrative"] = "La Cohorte Cero se encuentra en un estado de alta resiliencia y plenitud vital."
    elif avg >= 0.7:
        status["community_narrative"] = "La comunidad muestra una base sólida, pero existen vulnerabilidades focalizadas que requieren atención."
    else:
        status["community_narrative"] = "⚠️ Alerta de Coherencia: Múltiples dimensiones vitales están por debajo del umbral de dignidad en la comunidad."
        
    return jsonify(status), 200


# ==================== PULSO VITAL (COHORT HEARTBEAT) ====================


@forms_bp.route("/pulse", methods=["GET"])
@token_required
def get_cohort_pulse(current_user):
    """
    Endpoint agregado que retorna el "Pulso Vital" completo de la Cohorte Cero.

    Combina en una sola respuesta:
    - SDV comunitario (scores + narrativas por dimensión)
    - Brechas de cobertura de la comunidad
    - Alertas urgentes y Crímenes de Coherencia
    - Estadísticas generales del dashboard

    Este endpoint alimenta la página /pulso en el frontend.

    Autor: Claude Opus (Anthropic)
    """
    from datetime import datetime
    from .sdv_analyzer import SDVScore

    db = get_db()

    # 1. SDV Community: scores + narratives
    analyzer = SDVAnalyzer(db)
    sdv_community = analyzer.get_community_sdv_status()

    dims = sdv_community.get("dimensions", {})
    community_score = SDVScore(
        vivienda=dims.get("vivienda", 1.0),
        alimentacion=dims.get("alimentacion", 1.0),
        agua=dims.get("agua", 1.0),
        salud=dims.get("salud", 1.0),
        educacion=dims.get("educacion", 1.0),
        trabajo=dims.get("trabajo", 1.0),
        vinculos=dims.get("vinculos", 1.0),
    )
    narratives = analyzer.generate_narrative(community_score)

    avg = sdv_community.get("average_overall", 1.0)
    if avg >= 0.9:
        community_narrative = (
            "La Cohorte Cero se encuentra en un estado de alta "
            "resiliencia y plenitud vital."
        )
    elif avg >= 0.7:
        community_narrative = (
            "La comunidad muestra una base sólida, pero existen "
            "vulnerabilidades focalizadas que requieren atención."
        )
    else:
        community_narrative = (
            "⚠️ Alerta de Coherencia: Múltiples dimensiones vitales "
            "están por debajo del umbral de dignidad en la comunidad."
        )

    # 2. Matching gaps
    engine = MatchingEngine(db)
    gaps = engine.get_community_sdv_gaps()

    # 3. Urgent needs + Coherence Crimes
    urgent = engine.get_urgent_unmet_needs(days_threshold=7, top_matches=3)
    coherence_crimes = [u for u in urgent if u.is_coherence_crime]
    warnings = [u for u in urgent if not u.is_coherence_crime]

    # 4. Dashboard stats
    manager = FormsManager(db)
    stats = manager.get_dashboard_stats()

    return jsonify({
        "sdv": {
            "average_overall": avg,
            "dimensions": dims,
            "participant_count": sdv_community.get("participant_count", 0),
            "community_narrative": community_narrative,
            "narratives": narratives,
        },
        "gaps": {
            "all": [_gap_to_dict(g) for g in gaps],
            "critical": [
                _gap_to_dict(g) for g in gaps if g.gap_severity == "critical"
            ],
            "warnings": [
                _gap_to_dict(g) for g in gaps if g.gap_severity == "warning"
            ],
            "covered": [
                _gap_to_dict(g) for g in gaps if g.gap_severity == "ok"
            ],
            "critical_count": len(
                [g for g in gaps if g.gap_severity == "critical"]
            ),
        },
        "alerts": {
            "coherence_crimes": [
                _urgent_need_to_dict(u) for u in coherence_crimes
            ],
            "warnings": [_urgent_need_to_dict(u) for u in warnings],
            "total_urgent": len(urgent),
            "crimes_count": len(coherence_crimes),
            "system_alert": len(coherence_crimes) > 0,
        },
        "stats": stats,
        "timestamp": datetime.now().isoformat(),
    }), 200


# ==================== P2P PLAZA Y ORÁCULO SINTÉTICO ====================


@forms_bp.route("/matching/me", methods=["GET"])
@token_required
def get_my_matches(current_user):
    """
    Retorna los matches para el participante autenticado (basado en su email).
    Retorna tanto los oferentes para sus necesidades (find_matches)
    como los buscadores para sus ofertas (find_matches_for_offerer).
    """
    email = current_user.get("email")
    if not email:
        return jsonify({"error": "email not found in token"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM participants WHERE email = ? AND status = 'active'",
        (email,),
    )
    row = cursor.fetchone()
    if not row:
        return jsonify({
            "status": "no_profile",
            "email": email,
            "message": "No profile found for this email in Cohorte Cero. Please complete the Formulario CERO."
        }), 200

    participant = dict(zip([d[0] for d in cursor.description], row))
    participant_id = participant["id"]

    engine = MatchingEngine(db)

    # Quién me ayuda (matches for my needs)
    seeker_matches = engine.find_matches(seeker_id=participant_id, limit=10, exclude_recent=True)
    # A quién ayudo (matches for what I offer)
    offerer_matches = engine.find_matches_for_offerer(offerer_id=participant_id, limit=10, exclude_recent=True)

    # Parse JSON fields
    participant["offer_categories"] = engine._parse_json(participant.get("offer_categories"))
    participant["offer_human_dimensions"] = engine._parse_json(participant.get("offer_human_dimensions"))
    participant["need_categories"] = engine._parse_json(participant.get("need_categories"))
    participant["need_human_dimensions"] = engine._parse_json(participant.get("need_human_dimensions"))

    return jsonify({
        "status": "ok",
        "participant": participant,
        "seeker_matches": [_match_result_to_dict(m) for m in seeker_matches],
        "offerer_matches": [_match_result_to_dict(m) for m in offerer_matches],
    }), 200


def _simulate_oracle(message: str, participants_list: list) -> dict:
    """
    Simulación heurística basada en reglas para extraer datos de intercambio.
    """
    import re
    msg_lower = message.lower()
    
    # 1. Identificar participantes
    matched_participants = []
    for p in participants_list:
        p_name = p["name"].lower()
        first_name = p_name.split()[0] if p_name else ""
        
        if p_name in msg_lower:
            matched_participants.append((p, msg_lower.index(p_name), len(p_name)))
        elif first_name and len(first_name) > 2 and first_name in msg_lower:
            matched_participants.append((p, msg_lower.index(first_name), len(first_name)))

    matched_participants.sort(key=lambda x: x[1])
    
    giver = None
    receiver = None
    
    if len(matched_participants) >= 2:
        p1, idx1, len1 = matched_participants[0]
        p2, idx2, len2 = matched_participants[1]
        
        text_between = msg_lower[idx1 + len1 : idx2].strip()
        
        if any(kw in text_between for kw in ["ayudo", "ayudó", "dio", "para", "entregó", "entrego", "le dio"]):
            giver = p1
            receiver = p2
        elif any(kw in text_between for kw in ["recibió de", "recibio de", "de"]):
            giver = p2
            receiver = p1
        else:
            giver = p1
            receiver = p2
    elif len(matched_participants) == 1:
        p = matched_participants[0][0]
        if any(kw in msg_lower for kw in ["ayudo", "ayudó", "dio", "ofrece"]):
            giver = p
        else:
            receiver = p

    # 2. Extraer horas UTH
    hours_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hora|horas|uth|u\.t\.h)', msg_lower)
    uth_hours = 1.0
    if hours_match:
        try:
            uth_hours = float(hours_match.group(1))
        except ValueError:
            pass
            
    # 3. Extraer urgencia
    urgency = "Media"
    if any(kw in msg_lower for kw in ["alta", "urgente"]):
        urgency = "Alta"
    elif any(kw in msg_lower for kw in ["baja", "tranquilo"]):
        urgency = "Baja"
        
    # 4. Descripción
    description = message
    if giver and receiver:
        desc_match = re.search(r'(?:con|para|de)\s+([^,.\n]+)', message, re.IGNORECASE)
        if desc_match:
            description = desc_match.group(1).strip()
            
    giver_name = giver["name"] if giver else "alguien"
    receiver_name = receiver["name"] if receiver else "alguien"
    
    if giver and receiver:
        reply = (
            f"¡Entendido! He procesado tu mensaje en modo de simulación. "
            f"Detecté que {giver_name} ayudó a {receiver_name} con '{description}' por un total de {uth_hours} UTH (horas). "
            f"Haz clic en el botón de abajo para registrar este intercambio."
        )
        prefill = {
            "giver_id": giver["id"],
            "giver_name": giver["name"],
            "receiver_id": receiver["id"],
            "receiver_name": receiver["name"],
            "type": "UTH",
            "description": description,
            "urgency": urgency,
            "uth_hours": uth_hours
        }
    else:
        reply = (
            "Hola, soy el Oráculo Sintético. No logré identificar claramente a ambos participantes (emisor y receptor) "
            "en tu mensaje. Por favor menciona algo como 'Nelson ayudó a Max con 2 horas de diseño'."
        )
        prefill = None
        
    return {
        "reply": reply,
        "prefill": prefill
    }


@forms_bp.route("/oracle/chat", methods=["POST"])
@token_required
def oracle_chat(current_user):
    """
    Interactúa con el Oráculo Sintético (LLM) para procesar lenguaje natural
    y detectar posibles registros de intercambio.
    """
    import os
    import json
    import requests

    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, city, neighborhood FROM participants WHERE status = 'active'")
    participants = [dict(zip([d[0] for d in cursor.description], row)) for row in cursor.fetchall()]

    participants_context = "\n".join([
        f"- ID: {p['id']}, Nombre: {p['name']}, Email: {p['email']}, Ciudad: {p['city']}, Barrio: {p['neighborhood']}"
        for p in participants
    ])

    gemini_key = os.environ.get("GEMINI_API_KEY")
    local_url = os.environ.get("LOCAL_LLM_URL")

    system_prompt = f"""
Eres el Oráculo Sintético de la Maxocracia, un asistente de IA encargado de facilitar la gestión y registro de datos de la Cohorte Cero.
Tu objetivo principal es leer la conversación del usuario, responder con amabilidad y, si el usuario describe un intercambio/ayuda/servicio que ocurrió o está ocurriendo entre participantes, estructurar y extraer los datos para pre-llenar un formulario de registro de intercambio.

Contexto de los Participantes Registrados:
{participants_context}

Instrucciones de Extracción:
- Identifica quién es el emisor/giver (la persona que ayuda o provee) y el receptor/receiver (la persona que recibe la ayuda). Busca coincidencia de nombres exactos o parciales con los participantes listados en el contexto y obtén sus IDs.
- Estima el número de horas o UTH (Unidad de Tiempo Humano). Por defecto, usa 1.0 hora si no se especifica.
- Escribe una descripción breve e informativa del intercambio.
- Define la urgencia ('Baja', 'Media', 'Alta') basándote en la descripción de la necesidad. Por defecto es 'Media'.
- Define el tipo (usualmente 'UTH').

Debes responder ÚNICAMENTE en formato JSON con la siguiente estructura:
{{
  "reply": "Respuesta textual en español dirigida al usuario, explicando qué entendiste o confirmando el registro del intercambio.",
  "prefill": {{
    "giver_id": <int o null>,
    "giver_name": "<nombre del giver o null>",
    "receiver_id": <int o null>,
    "receiver_name": "<nombre del receiver o null>",
    "type": "UTH",
    "description": "<descripción corta>",
    "urgency": "Baja" | "Media" | "Alta",
    "uth_hours": <float o null>
  }} (o null si no se detecta ningún intercambio en el mensaje del usuario)
}}
"""

    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": system_prompt + f"\nMensaje del usuario: {message}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                res_data = res.json()
                text_response = res_data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_response)
                # Resolve names if missing
                if parsed.get("prefill"):
                    giver_id = parsed["prefill"].get("giver_id")
                    receiver_id = parsed["prefill"].get("receiver_id")
                    for p in participants:
                        if giver_id and p["id"] == giver_id:
                            parsed["prefill"]["giver_name"] = p["name"]
                        if receiver_id and p["id"] == receiver_id:
                            parsed["prefill"]["receiver_name"] = p["name"]
                return jsonify(parsed), 200
        except Exception as e:
            pass

    if local_url:
        try:
            url = f"{local_url.rstrip('/')}/v1/chat/completions"
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "local-model",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "response_format": {"type": "json_object"}
            }
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                res_data = res.json()
                text_response = res_data["choices"][0]["message"]["content"]
                parsed = json.loads(text_response)
                if parsed.get("prefill"):
                    giver_id = parsed["prefill"].get("giver_id")
                    receiver_id = parsed["prefill"].get("receiver_id")
                    for p in participants:
                        if giver_id and p["id"] == giver_id:
                            parsed["prefill"]["giver_name"] = p["name"]
                        if receiver_id and p["id"] == receiver_id:
                            parsed["prefill"]["receiver_name"] = p["name"]
                return jsonify(parsed), 200
        except Exception as e:
            pass

    # Heuristic simulation mode fallback
    result = _simulate_oracle(message, participants)
    return jsonify(result), 200
