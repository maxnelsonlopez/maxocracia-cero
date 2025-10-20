import os
import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta, timezone

SECRET = os.environ.get('SECRET_KEY', 'dev-secret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES = int(os.environ.get('ACCESS_TOKEN_EXPIRES', 15 * 60))  # seconds


def create_token(payload, expires_in: int = None):
    """Create a JWT with an `exp` claim. expires_in in seconds (default ACCESS_TOKEN_EXPIRES).
    The `exp` claim is stored as an integer UTC epoch (seconds).
    """
    now = datetime.now(timezone.utc)
    exp_dt = now + timedelta(seconds=(expires_in if expires_in is not None else ACCESS_TOKEN_EXPIRES))
    exp = int(exp_dt.timestamp())
    to_encode = payload.copy()
    # only set exp if not present to allow tests to override
    if 'exp' not in to_encode:
        to_encode.update({'exp': exp})
    token = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def verify_token(token, allow_expired: bool = False):
    """Verify token signature and expiration. If allow_expired is True, signature is still verified
    but expiration is ignored and payload is returned (useful for refresh flows).
    Returns payload dict or None on failure.
    """
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        if allow_expired:
            try:
                # decode without verifying exp but still verify signature
                data = jwt.decode(token, SECRET, algorithms=[ALGORITHM], options={"verify_exp": False})
                return data
            except Exception:
                return None
        return None
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
        # attach user info to request
        request.user = data
        return f(*args, **kwargs)
    return decorated
