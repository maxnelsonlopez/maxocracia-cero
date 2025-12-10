from typing import Tuple

from .utils import get_db


def get_balance(user_id):
    db = get_db()
    cur = db.execute(
        "SELECT SUM(change_amount) as balance FROM maxo_ledger WHERE user_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    return row["balance"] if row and row["balance"] is not None else 0.0


def credit_user(user_id, amount, reason=None):
    db = get_db()
    db.execute(
        "INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)",
        (user_id, amount, reason),
    )
    db.commit()


def get_vhv_parameters() -> Tuple[float, float, float, float]:
    """
    Fetch the latest VHV valuation parameters from the Oracles (DB).
    Returns (alpha, beta, gamma, delta).
    """
    db = get_db()
    try:
        cur = db.execute(
            "SELECT alpha, beta, gamma, delta FROM vhv_parameters ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
        if row:
            return (
                float(row["alpha"]),
                float(row["beta"]),
                float(row["gamma"]),
                float(row["delta"]),
            )
        # Fallbacks based on theoretical axioms if DB is empty
        return 100.0, 2000.0, 1.0, 100.0  # Base values from schema
    except Exception:
        return 100.0, 2000.0, 1.0, 100.0


def calculate_maxo_price(
    t_seconds: float,
    v_lives: float,
    r_resources: float = 0.0,
    frg: float = 1.0,
    cs: float = 1.0,
) -> float:
    """
    Calculate the Maxo Price based on the VHV Vector and Valuation Axioms.

    Formula: Price = α·T + β·V^γ + δ·R·(FRG × CS)

    Args:
        t_seconds (float): Objective Time (T) in seconds.
        v_lives (float): Objective Lives affected (V), weighted by biological complexity [0-1].
        r_resources (float): Objective Resources (R) in base units.
        frg (float): Factor de Rareza Geológica (default 1.0).
        cs (float): Criticidad Sistémica (default 1.0).

    Returns:
        float: The subjective Value in Maxos.
    """
    alpha, beta, gamma, delta = get_vhv_parameters()

    # T: Convert seconds to hours for the valuation formula (standard convention)
    t_hours = t_seconds / 3600.0

    # V: Apply Suffering/Aversion Exponent (Gamma)
    # Axiom: Gamma >= 1 to penalize suffering exponentially
    # Security check: if v_lives is negative (e.g. regenerative/rescue), we handle it carefully
    # For now, simplistic approach: if V > 0, penalize. If V < 0 (rescue), reward linearly?
    # Paper says: V measures "Unidades de Vida Consumidas".
    v_component = 0.0
    if v_lives > 0:
        v_component = v_lives**gamma
    else:
        # Negative lives consumed (saving lives) could be negative impact,
        # but the formula typically measures COST.
        # For simplicity, we keep V^gamma magnitude.
        v_component = -((-v_lives) ** gamma)

    # R: Resources * Modifiers
    r_component = r_resources * frg * cs

    # Final Polynomial Calculation
    price = (alpha * t_hours) + (beta * v_component) + (delta * r_component)

    return float(max(0.0, round(price, 4)))


# Legacy wrapper for backward compatibility
def calculate_credit(uth_hours=0.0, impact_score=0, uvc_score=None, urf_units=None):
    """
    Legacy wrapper.
    Maps old 'uth_hours' to T.
    Maps old 'uvc_score' to V.
    Maps old 'urf_units' to R.
    impact_score is ignored in strict VHV calculation (or could act as modifier).
    """
    t_seconds = uth_hours * 3600.0
    v_lives = float(uvc_score or 0.0)
    r_resources = float(urf_units or 0.0)

    return calculate_maxo_price(t_seconds, v_lives, r_resources)
