"""
Escalera de salvaguardas para personas vulnerables (Ola 3B).

Perfiles de protección:
- standard : sin protecciones adicionales.
- assisted : paráfrasis oracular obligatoria, revisión oracular pre-firma,
             enfriamiento 24h, tope de exposición 20h/contrato y 40h/semana.
- shielded : todo lo anterior + co-testigo humano obligatorio, enfriamiento
             72h, topes 8h/contrato y 15h/semana, y bloqueo de creación
             sin oráculo en vivo.

La equidad no se negocia con el presupuesto: la degradación elegante
(oráculo heurístico sin API key) es aceptable para standard pero PROHIBIDA
para assisted/shielded (blindaje_anti_gamificacion_equidad.md §4.2).
"""

from typing import Dict, Optional

from .utils import get_db

LEVELS = {
    "standard": 0,
    "assisted": 1,
    "shielded": 2,
}

# Topes y requisitos por nivel (blindaje_anti_gamificacion_equidad.md §4.2)
CAPS = {
    "standard": {
        "contract_hours": None,  # sin tope
        "weekly_hours": None,
        "reflection_hours": 0,
        "requires_paraphrase": False,
        "requires_oracle_review": False,
        "requires_witness": False,
        "oracle_required_for_creation": False,
    },
    "assisted": {
        "contract_hours": 20,
        "weekly_hours": 40,
        "reflection_hours": 24,
        "requires_paraphrase": True,
        "requires_oracle_review": True,
        "requires_witness": False,
        "oracle_required_for_creation": False,
    },
    "shielded": {
        "contract_hours": 8,
        "weekly_hours": 15,
        "reflection_hours": 72,
        "requires_paraphrase": True,
        "requires_oracle_review": True,
        "requires_witness": True,
        "oracle_required_for_creation": True,
    },
}

PARAPHRASE_MIN_LENGTH = 10


def get_profile(user_id: int) -> dict:
    """Perfil declarado del usuario (o default standard)."""
    row = (
        get_db()
        .execute("SELECT * FROM maxo_user_protection WHERE user_id = ?", (user_id,))
        .fetchone()
    )
    if row is None:
        return {
            "user_id": user_id,
            "level": "standard",
            "companion_user_id": None,
            "declared_age": None,
            "declared_education": None,
        }
    return dict(row)


def set_profile(
    user_id: int,
    level: str,
    companion_user_id: Optional[int] = None,
    declared_age: Optional[int] = None,
    declared_education: Optional[str] = None,
) -> dict:
    """Actualiza el perfil declarado (upsert)."""
    if level not in LEVELS:
        raise ValueError(f"level must be one of: {', '.join(LEVELS)}")
    db = get_db()
    db.execute(
        """
        INSERT INTO maxo_user_protection (user_id, level, companion_user_id, declared_age, declared_education)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            level = excluded.level,
            companion_user_id = excluded.companion_user_id,
            declared_age = excluded.declared_age,
            declared_education = excluded.declared_education,
            updated_at = CURRENT_TIMESTAMP
        """,
        (user_id, level, companion_user_id, declared_age, declared_education),
    )
    db.commit()
    return get_profile(user_id)


def _heuristic_level(user_id: int) -> str:
    """Señales de vulnerabilidad no declaradas (piso de protección):
    necesidad de urgencia Alta registrada en el dominio de formularios.
    (La protección de "primera vez" se entrega mejor con onboarding guiado,
    no con escalada automática que sorprende al usuario.)"""
    db = get_db()
    row = db.execute(
        """
        SELECT 1 FROM participants p
        JOIN participant_needs n ON n.participant_id = p.id
        WHERE p.email = (SELECT email FROM users WHERE id = ?)
          AND n.status = 'active' AND n.urgency = 'Alta'
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()
    if row:
        return "assisted"
    return "standard"


def protection_level(user_id: int) -> str:
    """Nivel efectivo = max(declarado, heurístico)."""
    declared = get_profile(user_id).get("level") or "standard"
    heuristic = _heuristic_level(user_id)
    if LEVELS[heuristic] > LEVELS[declared]:
        return heuristic
    return declared


def caps_for(level: str) -> dict:
    return CAPS.get(level, CAPS["standard"])


def is_protected(level: str) -> bool:
    return LEVELS.get(level, 0) > 0


def assigned_hours(contract_id: str) -> Dict[str, float]:
    """TVI total (T) asignado por parte obligada en un contrato."""
    rows = (
        get_db()
        .execute(
            "SELECT assigned_participant, SUM(vhv_t) AS h FROM maxo_contract_terms "
            "WHERE contract_id = ? AND assigned_participant IS NOT NULL "
            "GROUP BY assigned_participant",
            (contract_id,),
        )
        .fetchall()
    )
    return {r["assigned_participant"]: float(r["h"] or 0) for r in rows}


def weekly_assigned_hours(pid: str) -> float:
    """TVI asignado a la parte en contratos vigentes (pending + active)."""
    row = (
        get_db()
        .execute(
            """
        SELECT COALESCE(SUM(t.vhv_t), 0) AS h
        FROM maxo_contract_terms t
        JOIN maxo_contracts c ON c.contract_id = t.contract_id
        WHERE t.assigned_participant = ? AND c.state IN ('pending', 'active')
        """,
            (pid,),
        )
        .fetchone()
    )
    return float(row["h"] or 0)


def exposure_check(pid: str, new_hours: float = 0.0) -> Optional[str]:
    """
    Topes de exposición (Ola 3B): contrato y semana, según el nivel del
    humano obligado. Devuelve un mensaje de error o None.
    """
    uid = _pid_to_uid(pid)
    if uid is None:
        return None  # las colectivas no se topan aquí
    level = protection_level(uid)
    caps = caps_for(level)
    contract_cap = caps.get("contract_hours")
    if contract_cap is not None and new_hours > contract_cap:
        return (
            f"tu perfil de protección ({level}) limita tu exposición a "
            f"{contract_cap:.0f}h por contrato (tienes {new_hours:.1f}h asignadas)"
        )
    weekly_cap = caps.get("weekly_hours")
    if weekly_cap is not None:
        week = weekly_assigned_hours(pid) + new_hours
        if week > weekly_cap:
            return (
                f"tu perfil de protección ({level}) limita tu exposición semanal "
                f"a {weekly_cap:.0f}h (con este contrato sumarías {week:.1f}h)"
            )
    return None


def _pid_to_uid(pid: str) -> Optional[int]:
    if not pid or not pid.startswith("user-"):
        return None
    try:
        return int(pid[len("user-") :])
    except ValueError:
        return None
