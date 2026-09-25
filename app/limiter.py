import hashlib
import os

from flask import jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def get_client_address() -> str:
    """IP real del cliente detrás del túnel de Cloudflare.

    Con TRUST_PROXY=1 se prefiere CF-Connecting-IP (lo inyecta el borde de
    Cloudflare y no es falsificable a través del túnel); si no está, ProxyFix
    ya dejó X-Forwarded-For en request.remote_addr. Sin TRUST_PROXY no se
    confía en cabeceras (evita spoofing si el puerto queda expuesto).
    """
    if os.environ.get("TRUST_PROXY") == "1":
        cf = request.headers.get("CF-Connecting-IP")
        if cf and cf.strip():
            return cf.strip()
    return get_remote_address()


def get_user_or_ip_key() -> str:
    """Clave para endpoints autenticados costosos (oráculo LLM): huella del
    bearer si existe, IP real en caso contrario. No guarda el token."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.split(" ", 1)[1].strip()
        if token:
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            return "tok:" + digest[:32]
    return get_client_address()


def get_storage_uri() -> str:
    """URI de almacenamiento del limiter (uso en multi-worker).

    Orden: RATELIMIT_STORAGE_URI (plan de seguridad §4) → REDIS_URL
    (compatibilidad histórica) → memory:// (desarrollo, límites por proceso).
    """
    return (
        os.environ.get("RATELIMIT_STORAGE_URI")
        or os.environ.get("REDIS_URL")
        or "memory://"
    )


# Configuración del limiter
limiter = Limiter(
    key_func=get_client_address,
    storage_uri=get_storage_uri(),
    strategy="fixed-window",
    default_limits=["10000 per day", "5000 per hour"],
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


def get_oracle_limits():
    """Cuota de los endpoints que llaman al oráculo (costo real por token).

    Sin cuota, cualquier integrante N0 podía quemar la cuota de DeepSeek/
    OpenRouter. Configurable con RATELIMIT_ORACLE_LIMIT.
    """
    from flask import current_app

    override = current_app.config.get("RATELIMIT_ORACLE_LIMIT") or os.environ.get(
        "RATELIMIT_ORACLE_LIMIT"
    )
    if override:
        return override
    if current_app.config.get("TESTING"):
        return "100 per minute"
    return "30 per hour"


# Usar funciones para obtener límites dinámicamente
AUTH_LIMITS = get_auth_limits
API_GENERAL_LIMITS = get_api_limits
LOGIN_LIMITS = get_login_limits
REGISTER_LIMITS = get_register_limits
REFRESH_LIMITS = get_refresh_limits
ORACLE_LIMITS = get_oracle_limits


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
