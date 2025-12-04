import os
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Optional

import jwt
from flask import current_app, jsonify, request


# Generar una clave secreta fuerte si no está definida en el entorno
def get_secure_key():
    env_key = os.environ.get("SECRET_KEY")
    if env_key:
        return env_key

    # En modo desarrollo, generar una clave aleatoria pero advertir
    if current_app and current_app.config.get("ENV") == "development":
        print(
            "ADVERTENCIA: Usando clave secreta generada automáticamente. En producción, define SECRET_KEY en variables de entorno."
        )
        return secrets.token_hex(32)

    # En producción, forzar el uso de una clave definida en el entorno
    raise RuntimeError(
        "ERROR DE SEGURIDAD: No se ha definido SECRET_KEY en las variables de entorno. "
        "Esto es obligatorio en entornos de producción."
    )


# La clave se obtendrá cuando se inicialice la aplicación
SECRET = None
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES = int(os.environ.get("ACCESS_TOKEN_EXPIRES", 15 * 60))  # seconds


def create_token(payload, expires_in: Optional[int] = None):
    """Create a JWT with an `exp` claim. expires_in in seconds (default ACCESS_TOKEN_EXPIRES).
    The `exp` claim is stored as an integer UTC epoch (seconds).
    """
    global SECRET
    # Asegurar que SECRET esté inicializado
    if SECRET is None:
        # Inicializar SECRET si aún no se ha hecho
        SECRET = get_secure_key()

    now = datetime.now(timezone.utc)
    exp_dt = now + timedelta(
        seconds=(expires_in if expires_in is not None else ACCESS_TOKEN_EXPIRES)
    )
    exp = int(exp_dt.timestamp())

    # Añadir claims de seguridad estándar
    to_encode = payload.copy()
    to_encode.update(
        {
            "iat": int(now.timestamp()),  # Issued At
            "nbf": int(now.timestamp()),  # Not Before
            "jti": secrets.token_hex(8),  # JWT ID único
        }
    )

    # only set exp if not present to allow tests to override
    if "exp" not in to_encode:
        to_encode.update({"exp": exp})

    token = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def verify_token(token, allow_expired: bool = False):
    """Verify token signature and expiration. If allow_expired is True, signature is still verified
    but expiration is ignored and payload is returned (useful for refresh flows).
    Returns payload dict or None on failure.
    """
    # Asegurar que SECRET esté inicializado
    global SECRET
    if SECRET is None:
        # Inicializar SECRET si aún no se ha hecho
        SECRET = get_secure_key()

    try:
        options = {}
        if allow_expired:
            options["verify_exp"] = False

        data = jwt.decode(token, SECRET, algorithms=[ALGORITHM], options=options)
        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "authorization required"}), 401
        token = auth.split(" ", 1)[1]
        data = verify_token(token)
        if data is None:
            return jsonify({"error": "invalid token"}), 401
        # attach user info to request
        request.user = data
        # pass current_user as first argument to the decorated function
        return f(data, *args, **kwargs)

    return decorated
