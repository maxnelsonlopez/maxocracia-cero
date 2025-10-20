from flask import Blueprint, jsonify, request
from .maxo import get_balance, credit_user
from .utils import get_db
from .jwt_utils import token_required

bp = Blueprint('maxo', __name__, url_prefix='/maxo')


@bp.route('/<int:user_id>/balance', methods=['GET'])
def balance(user_id):
    bal = get_balance(user_id)
    return jsonify({'user_id': user_id, 'balance': bal})
@bp.route('/transfer', methods=['POST'])
@token_required
def transfer():
    # ensure authenticated user is the sender
    user = getattr(request, 'user', {})
    auth_user_id = user.get('user_id')
    data = request.get_json() or {}
    from_id = data.get('from_user_id')
    if auth_user_id is None or int(auth_user_id) != int(from_id):
        return jsonify({'error': 'forbidden: token user mismatch'}), 403
    return _transfer_impl()


def _transfer_impl():
    data = request.get_json() or {}
    from_id = data.get('from_user_id')
    to_id = data.get('to_user_id')
    amount = float(data.get('amount') or 0)
    reason = data.get('reason')

    if amount <= 0:
        return jsonify({'error': 'amount must be positive'}), 400

    db = get_db()
    # check users exist
    cur = db.execute('SELECT id FROM users WHERE id = ?', (from_id,))
    if cur.fetchone() is None:
        return jsonify({'error': 'from_user not found'}), 404
    cur = db.execute('SELECT id FROM users WHERE id = ?', (to_id,))
    if cur.fetchone() is None:
        return jsonify({'error': 'to_user not found'}), 404

    # debit from sender (negative change) and credit receiver
    credit_user(from_id, -amount, f'Transfer to {to_id}: {reason}')
    credit_user(to_id, amount, f'Transfer from {from_id}: {reason}')

    return jsonify({'success': True}), 200
