import os
import jwt
from functools import wraps
from flask import request, jsonify, current_app

SECRET = os.environ.get('SECRET_KEY', 'dev-secret')
ALGORITHM = 'HS256'


def create_token(payload):
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    # pyjwt returns bytes in older versions
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def verify_token(token):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return data
    except Exception:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'authorization required'}), 401
        token = auth.split(' ', 1)[1]
        data = verify_token(token)
        if data is None:
            return jsonify({'error': 'invalid token'}), 401
        # attach user info to current_app for simplicity
        request.user = data
        return f(*args, **kwargs)
    return decorated
