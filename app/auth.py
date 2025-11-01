import sqlite3
from flask import Blueprint, request, jsonify, session, make_response, current_app
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
from .limiter import limiter, AUTH_LIMITS
from .validators import validate_json_request, validate_email, validate_password, validate_name, validate_alias
from uuid import uuid4
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
@limiter.limit(AUTH_LIMITS)
@validate_json_request({
    'email': validate_email,
    'password': validate_password,
    'name': validate_name,
    'alias?': validate_alias  # Campo opcional
})
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    alias = data.get('alias')
    
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users (email, name, alias, password_hash) VALUES (?, ?, ?, ?)',
            (email, name, alias, generate_password_hash(password))
        )
        user_id = cursor.lastrowid
        db.commit()
        
        # Crear tokens para el nuevo usuario
        access_token = create_token({'user_id': user_id, 'email': email})
        
        # Generar refresh token
        jti = str(uuid4())
        raw_refresh = generate_refresh_token_raw()
        refresh_expires = 30 * 24 * 3600  # 30 días
        store_refresh_token(user_id, jti, raw_refresh, expires_in=refresh_expires)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': f"{jti}.{raw_refresh}",
            'expires_in': 3600  # 1 hora
        }), 201
        
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Email already registered'}), 400
    except Exception as e:
        # Don't expose internal error details to prevent information leakage
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/login', methods=['POST'])
@limiter.limit(AUTH_LIMITS)
@validate_json_request({
    'email': validate_email,
    'password': validate_password
})
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'invalid credentials'}), 401
    
    # Clear any existing session
    session.clear()
    session['user_id'] = user['id']
    
    # Create access token (expires in 1 hour)
    access_token = create_token({'user_id': user['id'], 'email': user['email']})
    
    # Generate refresh token (expires in 30 days)
    jti = str(uuid4())
    raw_refresh = generate_refresh_token_raw()
    refresh_expires = 30 * 24 * 3600  # 30 days in seconds
    store_refresh_token(user['id'], jti, raw_refresh, expires_in=refresh_expires)
    
    # Combine jti and raw token for the client
    refresh_token = f"{jti}.{raw_refresh}"
    
    # Prepare response
    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': 3600  # 1 hour in seconds
    }
    
    # In testing mode, return the tokens in the response body
    if current_app.config.get('TESTING', False):
        return jsonify(response_data), 200
    
    # In production/development, set the refresh token as an HttpOnly cookie
    resp = make_response(jsonify(response_data))
    secure = current_app.config.get('ENV') != 'development'
    resp.set_cookie(
        'mc_refresh', 
        refresh_token,
        httponly=True, 
        samesite='Lax', 
        secure=secure, 
        max_age=refresh_expires
    )
    
    return resp


@bp.route('/logout', methods=['POST'])
def logout():
    # Support multiple logout methods for JWT systems:
    # 1. Via refresh token (most secure)
    # 2. Via access token (fallback)
    # 3. Via session (legacy compatibility)

    # Try to get refresh token from request (JSON body or cookie)
    data = request.get_json(silent=True) or {}
    refresh_token = data.get('refresh_token') or request.cookies.get('mc_refresh')

    # Clear session regardless
    session.clear()

    # If we have a refresh token, revoke it specifically
    if refresh_token and '.' in refresh_token:
        try:
            jti, raw = refresh_token.split('.', 1)
            # Find the token record to get user_id
            from .refresh_utils import find_refresh_token_record
            rec = find_refresh_token_record(jti)
            if rec:
                # Revoke all tokens for this user
                revoke_user_tokens(rec['user_id'])
        except Exception as e:
            # Log error but don't expose it - logout should still succeed
            print(f'Warning: Failed to revoke refresh token: {e}')

    # Fallback: try to get user_id from access token in Authorization header
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        try:
            token = auth.split(' ', 1)[1]
            from .jwt_utils import verify_token
            data = verify_token(token)
            if data and 'user_id' in data:
                revoke_user_tokens(data['user_id'])
        except Exception as e:
            print(f'Warning: Failed to revoke via access token: {e}')

    # Final fallback: try to revoke based on session (for backward compatibility)
    uid = session.get('user_id')
    if uid:
        try:
            revoke_user_tokens(uid)
        except Exception as e:
            print(f'Warning: Failed to revoke tokens for user {uid}: {e}')

    resp = make_response(jsonify({'message': 'logged out'}))
    # clear cookie
    resp.set_cookie('mc_refresh', '', httponly=True, samesite='Lax', secure=False, expires=0)
    return resp


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
@limiter.limit(AUTH_LIMITS)
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

    # Rotation flow: accept refresh token from JSON body OR HttpOnly cookie
    data = request.get_json(silent=True) or {}
    rt = data.get('refresh_token')
    if not rt:
        rt = request.cookies.get('mc_refresh')
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
    
    # Create new access token
    access_token = create_token({'user_id': user['id'], 'email': user['email']})
    
    # Prepare response data
    response_data = {
        'access_token': access_token,
        'refresh_token': f"{new_jti}.{new_raw}",
        'expires_in': 3600  # 1 hour in seconds
    }
    
    # In testing mode, return the tokens in the response body
    if current_app.config.get('TESTING', False):
        return jsonify(response_data), 200
    
    # In production/development, set the refresh token as an HttpOnly cookie
    resp = make_response(jsonify(response_data))
    secure = current_app.config.get('ENV') != 'development'
    resp.set_cookie(
        'mc_refresh', 
        response_data['refresh_token'],
        httponly=True, 
        samesite='Lax', 
        secure=secure, 
        max_age=refresh_expires
    )
    
    return resp
