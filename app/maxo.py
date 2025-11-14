# Minimal Maxo logic utilities
from .utils import get_db


def get_balance(user_id):
    db = get_db()
    cur = db.execute('SELECT SUM(change_amount) as balance FROM maxo_ledger WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    return row['balance'] if row and row['balance'] is not None else 0.0


def credit_user(user_id, amount, reason=None):
    db = get_db()
    db.execute('INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)', (user_id, amount, reason))
    db.commit()


def calculate_credit(uth_hours=0.0, impact_score=0, uvc_score=None, urf_units=None):
    from flask import current_app
    try:
        w_uth = float(current_app.config.get('MAXO_WEIGHT_UTH', 1.0))
        w_imp = float(current_app.config.get('MAXO_WEIGHT_IMPACT', 0.5))
        w_uvc = float(current_app.config.get('MAXO_WEIGHT_UVC', 0.0))
        w_urf = float(current_app.config.get('MAXO_WEIGHT_URF', 0.0))
    except Exception:
        w_uth, w_imp, w_uvc, w_urf = 1.0, 0.5, 0.0, 0.0
    uvc = float(uvc_score or 0.0)
    urf = float(urf_units or 0.0)
    return uth_hours * w_uth + impact_score * w_imp + uvc * w_uvc + urf * w_urf
