"""
Forms Blueprint - API endpoints for Red de Apoyo forms system.

Provides REST API for:
- Formulario CERO (Participant Registration)
- Formulario A (Exchange Registration)
- Formulario B (Follow-up Reports)
- Dashboard analytics
- Matching Engine (Motor de Emparejamiento SDV)
"""

from flask import Blueprint, jsonify, request

from .auth import token_required
from .forms_manager import FormsManager
from .matching import MatchingEngine
from .sdv_analyzer import SDVAnalyzer
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
