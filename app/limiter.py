from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Configuración del limiter
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.environ.get("REDIS_URL", "memory://"),
    strategy="fixed-window",
    default_limits=["200 per day", "50 per hour"],
)


# Límites específicos para rutas sensibles
def get_auth_limits():
    from flask import current_app

    override = current_app.config.get("RATELIMIT_AUTH_LIMIT")
    if override:
        return override
    if current_app.config.get("TESTING"):
        return "100 per minute"
    return "3 per minute"


def get_api_limits():
    from flask import current_app

    override = current_app.config.get("RATELIMIT_API_LIMIT")
    if override:
        return override
    if current_app.config.get("TESTING"):
        return "200 per minute"
    return "60 per minute"


# Límites por endpoint con compatibilidad hacia atrás
def get_login_limits():
    from flask import current_app

    override = current_app.config.get(
        "RATELIMIT_LOGIN_LIMIT"
    ) or current_app.config.get("RATELIMIT_AUTH_LIMIT")
    if override:
        return override
    if current_app.config.get("TESTING"):
        return "100 per minute"
    return "3 per minute"


def get_register_limits():
    from flask import current_app

    override = current_app.config.get(
        "RATELIMIT_REGISTER_LIMIT"
    ) or current_app.config.get("RATELIMIT_AUTH_LIMIT")
    if override:
        return override
    if current_app.config.get("TESTING"):
        return "100 per minute"
    return "10 per hour"


def get_refresh_limits():
    from flask import current_app

    override = current_app.config.get(
        "RATELIMIT_REFRESH_LIMIT"
    ) or current_app.config.get("RATELIMIT_AUTH_LIMIT")
    if override:
        return override
    if current_app.config.get("TESTING"):
        return "200 per minute"
    return "20 per hour"


# Usar funciones para obtener límites dinámicamente
AUTH_LIMITS = get_auth_limits
API_GENERAL_LIMITS = get_api_limits
LOGIN_LIMITS = get_login_limits
REGISTER_LIMITS = get_register_limits
REFRESH_LIMITS = get_refresh_limits


# Función para manejar excesos de límite
def ratelimit_handler(e):
    """Handler para cuando se excede el límite de peticiones"""
    return (
        jsonify(
            {
                "error": "Demasiadas peticiones",
                "message": str(e.description),
                "retry_after": e.retry_after,
            }
        ),
        429,
    )


def init_limiter(app):
    """Inicializa el limiter con la aplicación Flask"""
    limiter.init_app(app)
    app.errorhandler(429)(ratelimit_handler)
    return limiter
