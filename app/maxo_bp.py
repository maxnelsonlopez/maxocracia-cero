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
    
    # Validar que el token de autenticación sea válido
    if not user or not auth_user_id:
        return jsonify({'error': 'invalid or missing authentication token'}), 401
        
    # Validar que se proporcione un from_user_id
    if from_id is None:
        return jsonify({'error': 'from_user_id is required'}), 400
        
    try:
        # Convertir a entero para asegurar que sea un ID válido
        from_id = int(from_id)
        auth_user_id = int(auth_user_id)
        
        # Verificar que el usuario autenticado sea el mismo que el remitente
        if auth_user_id != from_id:
            return jsonify({'error': 'forbidden: token user mismatch'}), 403
            
    except (ValueError, TypeError):
        return jsonify({'error': 'invalid user id format'}), 400
        
    # Si todo está bien, proceder con la transferencia
    return _transfer_impl()


def _transfer_impl():
    data = request.get_json() or {}
    from_id = data.get('from_user_id')
    to_id = data.get('to_user_id')
    
    # Validar que se proporcione un destinatario
    if to_id is None:
        return jsonify({'error': 'to_user_id is required'}), 400
        
    # Validar el monto
    try:
        amount = float(data.get('amount') or 0)
        if amount <= 0:
            return jsonify({'error': 'amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'invalid amount format'}), 400
        
    reason = data.get('reason', '')
    
    db = get_db()
    # normalize ids
    try:
        from_id = int(from_id)
        to_id = int(to_id)
    except Exception:
        return jsonify({'error': 'invalid user ids'}), 400

    # check users exist
    cur = db.execute('SELECT id FROM users WHERE id = ?', (from_id,))
    if cur.fetchone() is None:
        return jsonify({'error': 'from_user not found'}), 404
    cur = db.execute('SELECT id FROM users WHERE id = ?', (to_id,))
    if cur.fetchone() is None:
        return jsonify({'error': 'to_user not found'}), 404

    # ensure sender has sufficient balance
    sender_balance = get_balance(from_id)
    if sender_balance < amount:
        return jsonify({'error': 'insufficient balance', 'balance': sender_balance, 'required': amount}), 400

    db = get_db()
    try:
        # perform both ledger writes within the same DB connection/transaction
        db.execute('INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)', (from_id, -amount, f'Transfer to {to_id}: {reason}'))
        db.execute('INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)', (to_id, amount, f'Transfer from {from_id}: {reason}'))
        db.commit()
    except Exception as e:
        db.rollback()
        # Don't expose internal error details to prevent information leakage
        return jsonify({'error': 'Transfer failed'}), 500

    return jsonify({'success': True}), 200
