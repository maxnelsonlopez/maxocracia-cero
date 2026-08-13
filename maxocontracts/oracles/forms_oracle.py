"""
Forms Oracle - Oráculo de Formularios
=====================================

Este oráculo conecta MaxoContracts con la "realidad" reportada a través
de los formularios de Cohorte Cero (tabla `follow_ups`).

Permite que los contratos reaccionen a eventos como:
- "verification_completed": Verificación de un intercambio
- "need_resolved": Resolución de una necesidad
- "high_priority_alert": Detección de urgencia en seguimiento
"""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, List

from app.utils import get_db

from .base import OracleInterface, OracleQuery, OracleResponse, Verdict


class FormsOracle(OracleInterface):
    """
    Oráculo que lee la base de datos de formularios (follow_ups).
    """

    def __init__(self):
        self._query_log: List[OracleQuery] = []

    def validate_contract(self, contract_data: Dict[str, Any]) -> OracleResponse:
        """FormsOracle no valida contratos, solo eventos."""
        return OracleResponse(
            query_id=str(uuid.uuid4()),
            oracle_id="forms",
            verdict=Verdict(
                approved=True,
                confidence=Decimal("1.0"),
                reasoning="FormsOracle does not validate contract structure",
            ),
            metadata={
                "responded_at": datetime.now(timezone.utc),
                "oracle_type": "forms",
            },
        )

    def evaluate_retraction(
        self, contract_id: str, reason: str, evidence: Dict[str, Any]
    ) -> OracleResponse:
        """FormsOracle no evalúa retractaciones complejas."""
        return OracleResponse(
            query_id=str(uuid.uuid4()),
            oracle_id="forms",
            verdict=Verdict(
                approved=False,
                confidence=Decimal("0.0"),
                reasoning="FormsOracle cannot evaluate retractions",
            ),
            metadata={
                "responded_at": datetime.now(timezone.utc),
                "oracle_type": "forms",
            },
        )

    def estimate_gamma_impact(
        self, action_data: Dict[str, Any], participant_data: Dict[str, Any]
    ) -> Decimal:
        """FormsOracle no estima gamma."""
        return Decimal("0.0")

    def get_oracle_type(self) -> str:
        return "forms"

    def check_condition(
        self, condition_id: str, context: Dict[str, Any]
    ) -> OracleResponse:
        """
        Verifica condiciones basadas en formularios.

        Args:
            condition_id: Identificador de lo que buscamos (ej. "verify_interchange")
            context: Debe contener 'participant_id' y opcionalmente 'interchange_id'
                     o 'time_window_hours'.
        """
        query_uuid = str(uuid.uuid4())
        participant_id_str = context.get("participant_id")  # format: "user-123"

        if not participant_id_str:
            return OracleResponse(
                query_id=query_uuid,
                oracle_id="forms",
                verdict=Verdict(
                    approved=False,
                    confidence=Decimal("1.0"),
                    reasoning="participant_id required in context",
                ),
                metadata={
                    "responded_at": datetime.now(timezone.utc),
                    "oracle_type": "forms",
                },
            )

        # Parse user_id
        try:
            user_id = int(participant_id_str.split("-")[1])
        except (IndexError, ValueError):
            return OracleResponse(
                query_id=query_uuid,
                oracle_id="forms",
                verdict=Verdict(
                    approved=False,
                    confidence=Decimal("1.0"),
                    reasoning=f"Invalid participant_id format: {participant_id_str}",
                ),
                metadata={
                    "responded_at": datetime.now(timezone.utc),
                    "oracle_type": "forms",
                },
            )

        # Dispatch based on condition type
        if condition_id == "has_completed_verification":
            return self._check_verification(query_uuid, user_id, context)
        elif condition_id == "has_high_priority_alert":
            return self._check_alert(query_uuid, user_id, context)
        elif condition_id == "needs_resolved":
            return self._check_needs_resolved(query_uuid, user_id, context)
        else:
            return OracleResponse(
                query_id=query_uuid,
                oracle_id="forms",
                verdict=Verdict(
                    approved=False,
                    confidence=Decimal("1.0"),
                    reasoning=f"Unknown condition_id: {condition_id}",
                ),
                metadata={
                    "responded_at": datetime.now(timezone.utc),
                    "oracle_type": "forms",
                },
            )

    def _check_verification(
        self, query_id: str, user_id: int, context: Dict[str, Any]
    ) -> OracleResponse:
        """Verifica si existe un follow_up de tipo 'verification_completed' reciente."""
        db = get_db()

        # Opcional: filtrar por intercambio específico
        interchange_id = context.get("interchange_id")

        # Opcional: ventana de tiempo (por defecto 7 días atrás)
        hours = context.get("time_window_hours", 24 * 7)
        since_date = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()

        # Buscar participant_id correspondiente al user_id
        # Nota: La tabla follow_ups usa participant_id, que es ID de la tabla participants,
        # NO el user_id de la tabla users directamente.
        # Aquí asumimos que hay una relación o que participant_id = user_id en la práctica
        # o necesitamos buscar el participant_id asociado al email del user.
        # POR AHORA: Asumiremos que tenemos el participant_id correcto en la tabla participants
        # que coincida con el email del user.

        user_row = db.execute(
            "SELECT email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user_row:
            return OracleResponse(
                query_id=query_id,
                oracle_id="forms",
                verdict=Verdict(
                    approved=False,
                    confidence=Decimal("1.0"),
                    reasoning="User not found",
                ),
                metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
            )

        participant_row = db.execute(
            "SELECT id FROM participants WHERE email = ?", (user_row["email"],)
        ).fetchone()
        if not participant_row:
            return OracleResponse(
                query_id=query_id,
                oracle_id="forms",
                verdict=Verdict(
                    approved=False,
                    confidence=Decimal("1.0"),
                    reasoning="Participant profile not found for user",
                ),
                metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
            )

        p_id_db = participant_row["id"]

        query = """
            SELECT id, follow_up_date, facilitator_notes 
            FROM follow_ups 
            WHERE participant_id = ? 
            AND follow_up_type = 'verification_completed'
            AND follow_up_date >= ?
        """
        params = [p_id_db, since_date]

        if interchange_id:
            # Aquí necesitaríamos unir con la tabla interchange o usar related_interchange_id
            # si estuviera poblado correctamente.
            query += " AND related_interchange_id = ?"
            params.append(interchange_id)

        row = db.execute(query, params).fetchone()

        if row:
            return OracleResponse(
                query_id=query_id,
                oracle_id="forms",
                verdict=Verdict(
                    approved=True,
                    confidence=Decimal("1.0"),
                    reasoning=f"Verification found: ID {row['id']} on {row['follow_up_date']}",
                ),
                metadata={
                    "responded_at": datetime.now(timezone.utc),
                    "oracle_type": "forms",
                    "follow_up_id": row["id"],
                    "notes": row["facilitator_notes"],
                },
            )
        else:
            return OracleResponse(
                query_id=query_id,
                oracle_id="forms",
                verdict=Verdict(
                    approved=False,
                    confidence=Decimal("0.9"),
                    reasoning="No verification found in time window",
                ),  # Alta confianza de que NO existe
                metadata={
                    "responded_at": datetime.now(timezone.utc),
                    "oracle_type": "forms",
                },
            )

    def _check_alert(
        self, query_id: str, user_id: int, context: Dict[str, Any]
    ) -> OracleResponse:
        """Verifica si hay alertas de prioridad alta."""
        db = get_db()
        # ... Similar logic to fetch user -> participant ...
        user_row = db.execute(
            "SELECT email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return OracleResponse(
            query_id=query_id,
            oracle_id="forms",
            verdict=Verdict(
                approved=False,
                confidence=Decimal("1.0"),
                reasoning="User/Participant not found",
            ),
            metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
        )
        participant_row = db.execute(
            "SELECT id FROM participants WHERE email = ?", (user_row["email"],)
        ).fetchone()
        return OracleResponse(
            query_id=query_id,
            oracle_id="forms",
            verdict=Verdict(
                approved=False,
                confidence=Decimal("1.0"),
                reasoning="Participant not found",
            ),
            metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
        )
        p_id_db = participant_row["id"]

        row = db.execute(
            """
            SELECT id, follow_up_priority, facilitator_notes
            FROM follow_ups
            WHERE participant_id = ?
            AND follow_up_priority = 'high'
            AND status != 'closed' 
            ORDER BY follow_up_date DESC LIMIT 1
        """,
            (p_id_db,),
        ).fetchone()
        # Nota: 'status' no existe en follow_ups, se infiere de priority='closed' o lógica similar.
        # Ajuste: priority != 'closed'

        # Corregimos query:
        row = db.execute(
            """
            SELECT id, follow_up_priority, facilitator_notes
            FROM follow_ups
            WHERE participant_id = ?
            AND follow_up_priority = 'high'
            ORDER BY follow_up_date DESC LIMIT 1
        """,
            (p_id_db,),
        ).fetchone()

        if row:
            return OracleResponse(
                query_id=query_id,
                oracle_id="forms",
                verdict=Verdict(
                    approved=True,
                    confidence=Decimal("1.0"),
                    reasoning="High priority alert found",
                ),
                metadata={
                    "responded_at": datetime.now(timezone.utc),
                    "oracle_type": "forms",
                    "follow_up_id": row["id"],
                },
            )
        return OracleResponse(
            query_id=query_id,
            oracle_id="forms",
            verdict=Verdict(
                approved=False, confidence=Decimal("1.0"), reasoning="No high alerts"
            ),
            metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
        )

    def _check_needs_resolved(
        self, query_id: str, user_id: int, context: Dict[str, Any]
    ) -> OracleResponse:
        """Verifica si se reportó necesidad resuelta (need_level = 1)."""
        db = get_db()
        # ... User resolution ...
        user_row = db.execute(
            "SELECT email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return OracleResponse(
            query_id=query_id,
            oracle_id="forms",
            verdict=Verdict(
                approved=False, confidence=Decimal("1.0"), reasoning="User not found"
            ),
            metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
        )
        participant_row = db.execute(
            "SELECT id FROM participants WHERE email = ?", (user_row["email"],)
        ).fetchone()
        return OracleResponse(
            query_id=query_id,
            oracle_id="forms",
            verdict=Verdict(
                approved=False,
                confidence=Decimal("1.0"),
                reasoning="Participant not found",
            ),
            metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
        )
        p_id_db = participant_row["id"]

        row = db.execute(
            """
            SELECT id
            FROM follow_ups
            WHERE participant_id = ?
            AND need_level = 1
            ORDER BY follow_up_date DESC LIMIT 1
        """,
            (p_id_db,),
        ).fetchone()

        if row:
            return OracleResponse(
                query_id=query_id,
                oracle_id="forms",
                verdict=Verdict(
                    approved=True,
                    confidence=Decimal("1.0"),
                    reasoning="Need resolved reported",
                ),
                metadata={
                    "responded_at": datetime.utcnow(),
                    "oracle_type": "forms",
                    "follow_up_id": row["id"],
                },
            )

        return OracleResponse(
            query_id=query_id,
            oracle_id="forms",
            verdict=Verdict(
                approved=False,
                confidence=Decimal("1.0"),
                reasoning="No resolution reported",
            ),
            metadata={"responded_at": datetime.utcnow(), "oracle_type": "forms"},
        )
