from flask import Blueprint, request, jsonify, session
from .utils import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from .jwt_utils import create_token
from .jwt_utils import token_required
from .jwt_utils import verify_token
from .refresh_utils import (
    generate_refresh_token_raw,
    hash_refresh_token,
    store_refresh_token,
    verify_refresh_token_raw,
    rotate_refresh_token,
    revoke_user_tokens,
)
from uuid import uuid4
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    alias = data.get('alias')
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400
    db = get_db()
    try:
        db.execute('INSERT INTO users (email, name, alias, password_hash) VALUES (?, ?, ?, ?)',
                   (email, name, alias, generate_password_hash(password)))
        db.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'user created'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'invalid credentials'}), 401
    session.clear()
    session['user_id'] = user['id']
    # Access token
    token = create_token({'user_id': user['id'], 'email': user['email']})
    # Refresh token (rotate-on-use pattern): generate raw token and store its hash
    jti = str(uuid4())
    raw_refresh = generate_refresh_token_raw()
    # expires refresh token in 30 days (seconds)
    refresh_expires = 30 * 24 * 3600
    store_refresh_token(user['id'], jti, raw_refresh, expires_in=refresh_expires)
    refresh_token_combined = f"{jti}.{raw_refresh}"
    return jsonify({'message': 'logged in', 'user_id': user['id'], 'token': token, 'refresh_token': refresh_token_combined})


@bp.route('/logout', methods=['POST'])
def logout():
    # Revoke all refresh tokens for this user to fully logout
    uid = session.get('user_id')
    session.clear()
    if uid:
        revoke_user_tokens(uid)
    return jsonify({'message': 'logged out'})


@bp.route('/me', methods=['GET'])
@token_required
def me():
    # request.user is set by token_required
    user_info = getattr(request, 'user', {})
    user_id = user_info.get('user_id')
    if not user_id:
        return jsonify({'error': 'invalid token'}), 401
    db = get_db()
    row = db.execute('SELECT id, email, name, alias, phone, city, neighborhood, created_at FROM users WHERE id = ?', (user_id,)).fetchone()
    if row is None:
        return jsonify({'error': 'user not found'}), 404
    return jsonify(dict(row))



@bp.route('/refresh', methods=['POST'])
def refresh():
    # Support two modes:
    # 1) Legacy: Authorization: Bearer <access_token> -> verify signature allowing expired and return new access token
    # 2) Rotation: JSON body {"refresh_token": "<jti>.<raw>"} -> validate stored hash, rotate, and return new access + refresh
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1]
        data = verify_token(token, allow_expired=True)
        if data is None:
            return jsonify({'error': 'invalid token'}), 401
        payload = {'user_id': data.get('user_id'), 'email': data.get('email')}
        new_token = create_token(payload)
        return jsonify({'token': new_token})

    # Rotation flow: accept refresh token in JSON body as {"refresh_token": "<jti>.<raw>"}
    data = request.get_json(silent=True) or {}
    rt = data.get('refresh_token')
    if not rt or '.' not in rt:
        return jsonify({'error': 'refresh_token required'}), 401
    jti, raw = rt.split('.', 1)
    # verify raw against DB hash and revoked/expiry
    ok = verify_refresh_token_raw(jti, raw)
    if not ok:
        return jsonify({'error': 'invalid or revoked refresh token'}), 401
    # rotate: create new jti and raw, store new and revoke old
    new_jti = str(uuid4())
    new_raw = generate_refresh_token_raw()
    refresh_expires = 30 * 24 * 3600
    rotate_success = rotate_refresh_token(jti, new_jti, new_raw, expires_in=refresh_expires)
    if not rotate_success:
        return jsonify({'error': 'failed to rotate refresh token'}), 500
    # fetch user and issue new access token
    from .refresh_utils import find_refresh_token_record
    rec = find_refresh_token_record(new_jti)
    if not rec:
        return jsonify({'error': 'internal error'}), 500
    user_id = rec['user_id']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({'error': 'user not found'}), 404
    payload = {'user_id': user['id'], 'email': user['email']}
    new_access = create_token(payload)
    new_refresh_combined = f"{new_jti}.{new_raw}"
    return jsonify({'token': new_access, 'refresh_token': new_refresh_combined})
