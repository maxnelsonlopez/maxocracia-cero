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
