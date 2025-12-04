"""
Forms Manager - Business logic for Red de Apoyo forms system.

Handles validation, storage, and analysis for:
- Formulario CERO (Participant Registration)
- Formulario A (Exchange Registration)
- Formulario B (Follow-up Reports)
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class FormsManager:
    """Manages the Red de Apoyo forms system."""

    # Category constants
    CATEGORIES = [
        "objeto",
        "alimentacion",
        "habilidad",
        "conocimiento",
        "transporte",
        "tiempo",
        "espacio",
        "apoyo_economico",
    ]

    HUMAN_DIMENSIONS = [
        "crecimiento_aprendizaje",
        "bienestar_descanso",
        "seguridad_estabilidad",
        "autoestima_autonomia",
        "conexion_social",
        "prosperidad_recursos",
        "placer_goce",
        "intimidad_vinculos",
    ]

    def __init__(self, db_connection):
        """Initialize with database connection."""
        self.conn = db_connection

    # ==================== FORMULARIO CERO ====================

    def register_participant(self, data: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Register a new participant (Formulario CERO).

        Args:
            data: Dictionary with participant information

        Returns:
            Tuple of (success, message, participant_id)
        """
        required_fields = [
            "name",
            "email",
            "phone_call",
            "phone_whatsapp",
            "telegram_handle",
            "city",
            "neighborhood",
            "personal_values",
            "offer_description",
            "need_description",
            "need_urgency",
        ]

        # Validate required fields
        for field in required_fields:
            if not data.get(field):
                return False, f"Campo requerido faltante: {field}", None

        # Validate urgency
        if data["need_urgency"] not in ["Alta", "Media", "Baja"]:
            return False, "Urgencia debe ser Alta, Media o Baja", None

        # Validate and serialize JSON fields
        offer_categories = json.dumps(data.get("offer_categories", []))
        offer_dimensions = json.dumps(data.get("offer_human_dimensions", []))
        need_categories = json.dumps(data.get("need_categories", []))
        need_dimensions = json.dumps(data.get("need_human_dimensions", []))

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO participants (
                    name, email, referred_by, phone_call, phone_whatsapp,
                    telegram_handle, city, neighborhood, personal_values,
                    offer_categories, offer_description, offer_human_dimensions,
                    need_categories, need_description, need_urgency, need_human_dimensions,
                    consent_given
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data["name"],
                    data["email"],
                    data.get("referred_by"),
                    data["phone_call"],
                    data["phone_whatsapp"],
                    data["telegram_handle"],
                    data["city"],
                    data["neighborhood"],
                    data["personal_values"],
                    offer_categories,
                    data["offer_description"],
                    offer_dimensions,
                    need_categories,
                    data["need_description"],
                    data["need_urgency"],
                    need_dimensions,
                    data.get("consent_given", 1),
                ),
            )

            self.conn.commit()
            participant_id = cursor.lastrowid

            return True, "Participante registrado exitosamente", participant_id

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: participants.email" in str(e):
                return False, "Este email ya está registrado", None
            return False, f"Error de integridad: {e}", None
        except sqlite3.Error as e:
            return False, f"Error de base de datos: {e}", None

    def get_participants(
        self, limit: int = 50, offset: int = 0, status: Optional[str] = None
    ) -> List[Dict]:
        """Get list of participants with pagination."""
        cursor = self.conn.cursor()

        query = "SELECT * FROM participants"
        params: List[Any] = []

        if status:
            query += " WHERE status = ?"
            params.append(status)

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)

        participants = []
        for row in cursor.fetchall():
            participant = dict(zip([d[0] for d in cursor.description], row))
            # Parse JSON fields
            for field in [
                "offer_categories",
                "offer_human_dimensions",
                "need_categories",
                "need_human_dimensions",
            ]:
                if participant.get(field):
                    participant[field] = json.loads(participant[field])
            participants.append(participant)

        return participants

    def get_participant(self, participant_id: int) -> Optional[Dict]:
        """Get a single participant by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM participants WHERE id = ?", (participant_id,))
        row = cursor.fetchone()

        if not row:
            return None

        participant = dict(zip([d[0] for d in cursor.description], row))
        # Parse JSON fields
        for field in [
            "offer_categories",
            "offer_human_dimensions",
            "need_categories",
            "need_human_dimensions",
        ]:
            if participant.get(field):
                participant[field] = json.loads(participant[field])

        return participant

    # ==================== FORMULARIO A (uses existing interchange table) ====================

    def register_exchange(self, data: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Register an exchange (Formulario A).
        Uses the existing interchange table.

        Args:
            data: Dictionary with exchange information

        Returns:
            Tuple of (success, message, exchange_id)
        """
        required_fields = [
            "date",
            "interchange_id",
            "giver_id",
            "receiver_id",
            "type",
            "description",
            "urgency",
            "impact_resolution_score",
            "reciprocity_status",
        ]

        for field in required_fields:
            if field not in data:
                return False, f"Campo requerido faltante: {field}", None

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO interchange (
                    interchange_id, date, giver_id, receiver_id, type, description,
                    urgency, uth_hours, economic_value_approx, urf_description,
                    impact_resolution_score, reciprocity_status, human_dimension_attended,
                    coordination_method, requires_followup, followup_scheduled_date,
                    facilitator_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data["interchange_id"],
                    data["date"],
                    data["giver_id"],
                    data["receiver_id"],
                    data["type"],
                    data["description"],
                    data["urgency"],
                    data.get("uth_hours"),
                    data.get("economic_value_approx"),
                    data.get("urf_description"),
                    data["impact_resolution_score"],
                    data["reciprocity_status"],
                    data.get("human_dimension_attended"),
                    data.get("coordination_method"),
                    data.get("requires_followup", 0),
                    data.get("followup_scheduled_date"),
                    data.get("facilitator_notes"),
                ),
            )

            self.conn.commit()
            exchange_id = cursor.lastrowid

            return True, "Intercambio registrado exitosamente", exchange_id

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: interchange.interchange_id" in str(e):
                return False, "Este código de intercambio ya existe", None
            return False, f"Error de integridad: {e}", None
        except sqlite3.Error as e:
            return False, f"Error de base de datos: {e}", None

    # ==================== FORMULARIO B ====================

    def register_followup(self, data: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Register a follow-up report (Formulario B).

        Args:
            data: Dictionary with follow-up information

        Returns:
            Tuple of (success, message, followup_id)
        """
        required_fields = [
            "follow_up_date",
            "participant_id",
            "follow_up_type",
            "current_situation",
            "situation_change",
            "active_interchanges_status",
            "follow_up_priority",
        ]

        for field in required_fields:
            if field not in data:
                return False, f"Campo requerido faltante: {field}", None

        # Serialize JSON fields
        new_needs = json.dumps(data.get("new_needs_detected", []))
        new_offers = json.dumps(data.get("new_offers_detected", []))
        actions = json.dumps(data.get("actions_required", []))

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO follow_ups (
                    follow_up_date, participant_id, related_interchange_id,
                    follow_up_type, current_situation, need_level, situation_change,
                    active_interchanges_status, interchanges_working_well,
                    new_needs_detected, new_offers_detected,
                    emotional_state, community_connection,
                    actions_required, follow_up_priority, next_follow_up_date,
                    facilitator_notes, learnings
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data["follow_up_date"],
                    data["participant_id"],
                    data.get("related_interchange_id"),
                    data["follow_up_type"],
                    data["current_situation"],
                    data.get("need_level"),
                    data["situation_change"],
                    data["active_interchanges_status"],
                    data.get("interchanges_working_well"),
                    new_needs,
                    new_offers,
                    data.get("emotional_state"),
                    data.get("community_connection"),
                    actions,
                    data["follow_up_priority"],
                    data.get("next_follow_up_date"),
                    data.get("facilitator_notes"),
                    data.get("learnings"),
                ),
            )

            self.conn.commit()
            followup_id = cursor.lastrowid

            return True, "Seguimiento registrado exitosamente", followup_id

        except sqlite3.Error as e:
            return False, f"Error de base de datos: {e}", None

    # ==================== DASHBOARD & ANALYTICS ====================

    def get_dashboard_stats(self) -> Dict:
        """Calculate aggregate metrics for the dashboard."""
        cursor = self.conn.cursor()

        stats = {}

        # Total participants
        cursor.execute("SELECT COUNT(*) FROM participants WHERE status = 'active'")
        stats["total_participants"] = cursor.fetchone()[0]

        # Total exchanges
        cursor.execute("SELECT COUNT(*) FROM interchange")
        stats["total_exchanges"] = cursor.fetchone()[0]

        # Total UTH mobilized
        cursor.execute("SELECT COALESCE(SUM(uth_hours), 0) FROM interchange")
        stats["total_uth"] = cursor.fetchone()[0]

        # Urgency distribution
        cursor.execute(
            """
            SELECT urgency, COUNT(*)
            FROM interchange
            GROUP BY urgency
        """
        )
        stats["urgency_distribution"] = dict(cursor.fetchall())

        # Resolution rate (average impact_resolution_score)
        cursor.execute(
            """
            SELECT AVG(impact_resolution_score)
            FROM interchange
            WHERE impact_resolution_score IS NOT NULL
        """
        )
        avg_resolution = cursor.fetchone()[0]
        stats["resolution_rate"] = round(avg_resolution, 2) if avg_resolution else 0

        # Follow-up priority distribution
        cursor.execute(
            """
            SELECT follow_up_priority, COUNT(*)
            FROM follow_ups
            GROUP BY follow_up_priority
        """
        )
        stats["followup_priorities"] = dict(cursor.fetchall())

        # Active alerts (high priority follow-ups)
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM follow_ups
            WHERE follow_up_priority = 'high'
        """
        )
        stats["active_alerts"] = cursor.fetchone()[0]

        # Network health (average need_level from recent follow-ups)
        cursor.execute(
            """
            SELECT AVG(need_level)
            FROM follow_ups
            WHERE need_level IS NOT NULL
            AND follow_up_date >= date('now', '-30 days')
        """
        )
        avg_need = cursor.fetchone()[0]
        stats["network_health"] = round(avg_need, 2) if avg_need else 0

        return stats

    def get_active_alerts(self) -> List[Dict]:
        """Get all high-priority follow-ups that need attention."""
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT f.*, p.name, p.email
            FROM follow_ups f
            JOIN participants p ON f.participant_id = p.id
            WHERE f.follow_up_priority = 'high'
            ORDER BY f.follow_up_date DESC
        """
        )

        alerts = []
        for row in cursor.fetchall():
            alert = dict(zip([d[0] for d in cursor.description], row))
            # Parse JSON fields
            for field in [
                "new_needs_detected",
                "new_offers_detected",
                "actions_required",
            ]:
                if alert.get(field):
                    alert[field] = json.loads(alert[field])
            alerts.append(alert)

        return alerts

    def get_network_flow(self) -> Dict:
        """
        Calculate network flow metrics (who gives, who receives).

        Returns:
            Dictionary with givers, receivers, and hub nodes
        """
        cursor = self.conn.cursor()

        # Top givers
        cursor.execute(
            """
            SELECT giver_id, COUNT(*) as give_count
            FROM interchange
            GROUP BY giver_id
            ORDER BY give_count DESC
            LIMIT 10
        """
        )
        top_givers = [{"user_id": row[0], "count": row[1]} for row in cursor.fetchall()]

        # Top receivers
        cursor.execute(
            """
            SELECT receiver_id, COUNT(*) as receive_count
            FROM interchange
            GROUP BY receiver_id
            ORDER BY receive_count DESC
            LIMIT 10
        """
        )
        top_receivers = [
            {"user_id": row[0], "count": row[1]} for row in cursor.fetchall()
        ]

        # Hub nodes (both give and receive a lot)
        cursor.execute(
            """
            SELECT
                COALESCE(g.giver_id, r.receiver_id) as user_id,
                COALESCE(g.give_count, 0) as gives,
                COALESCE(r.receive_count, 0) as receives
            FROM
                (SELECT giver_id, COUNT(*) as give_count FROM interchange GROUP BY giver_id) g
            FULL OUTER JOIN
                (SELECT receiver_id, COUNT(*) as receive_count FROM interchange GROUP BY receiver_id) r
            ON g.giver_id = r.receiver_id
            WHERE COALESCE(g.give_count, 0) > 2 AND COALESCE(r.receive_count, 0) > 2
            ORDER BY (COALESCE(g.give_count, 0) + COALESCE(r.receive_count, 0)) DESC
        """
        )
        hubs = [
            {"user_id": row[0], "gives": row[1], "receives": row[2]}
            for row in cursor.fetchall()
        ]

        return {
            "top_givers": top_givers,
            "top_receivers": top_receivers,
            "hub_nodes": hubs,
        }
