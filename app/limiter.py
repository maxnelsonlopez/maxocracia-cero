from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Configuración del limiter
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.environ.get("REDIS_URL", "memory://"),
    strategy="fixed-window",
    default_limits=["200 per day", "50 per hour"]
)

# Límites específicos para rutas sensibles
AUTH_LIMITS = "5 per minute"
API_GENERAL_LIMITS = "60 per minute"

# Función para manejar excesos de límite
def ratelimit_handler(e):
    """Handler para cuando se excede el límite de peticiones"""
    return jsonify({
        "error": "Demasiadas peticiones",
        "message": str(e.description),
        "retry_after": e.retry_after
    }), 429

def init_limiter(app):
    """Inicializa el limiter con la aplicación Flask"""
    limiter.init_app(app)
    app.errorhandler(429)(ratelimit_handler)
    return limiter