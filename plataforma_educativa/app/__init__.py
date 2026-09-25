# -*- coding: utf-8 -*-
"""Fábrica de la aplicación Flask de la Plataforma Educativa.

La plataforma es una aplicación independiente, pero conceptualmente compatible
con Maxocracia. Vive por completo dentro de ``plataforma_educativa/``.
"""

import os

from flask import Flask, request

from . import actividad, buscador as buscador_engine, db, schema
from .api_routes import api_bp
from .auth_routes import auth_bp
from .buscador_routes import buscador_bp
from .frontend_routes import frontend_bp

# Ruta por defecto de la base SQLite (junto a este módulo, en la carpeta raíz
# de la plataforma).
_DEFAULT_DB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "plataforma_educativa.db",
)


def create_app(db_path=None):
    """Crea una instancia de la aplicación.

    Args:
        db_path: ruta a la base de datos SQLite. Si se omite, se usa
            ``plataforma_educativa.db`` en la raíz de la plataforma.
    """
    # ``../templates`` y ``../static`` son relativos a la carpeta del paquete
    # ``app``, que vive en ``plataforma_educativa/app``.
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    )
    app.config["DATABASE"] = db_path or _DEFAULT_DB
    # Respuestas JSON en UTF-8 legible (sin \uXXXX).
    try:
        app.json.ensure_ascii = False
    except AttributeError:
        pass

    # Almacén de tokens en memoria, por instancia (aislado entre tests).
    app.extensions["auth_tokens"] = {}

    # Cabeceras de seguridad (la escuela se sirve tras el túnel TLS de
    # Cloudflare): sin scripts inline, sin enmarcado y con HSTS cuando el
    # proxy confirma HTTPS.
    @app.after_request
    def _security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Referrer-Policy", "strict-origin-when-cross-origin"
        )
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; font-src 'self'; "
            "object-src 'none'; base-uri 'self'; frame-ancestors 'none'",
        )
        proto = request.headers.get("X-Forwarded-Proto", request.scheme)
        if proto == "https" or request.headers.get("CF-Connecting-IP"):
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response

    # Narrador humano de la actividad (terminal; silenciable con LOG_HUMANO=0)
    actividad.init_actividad(app)

    db.init_app(app)
    schema.init_db(app)

    # Buscador educativo (B1): parámetros canon y semillas canónicas
    # (seeds/maxocracia.json), ambos idempotentes. Fail-open (P2): si la
    # siembra falla, la plataforma arranca igual — el buscador se degrada
    # con honestidad, nunca rompe la casa.
    try:
        buscador_engine.sync_parametros_db(app.config["DATABASE"])
        buscador_engine.sync_seeds_file(app.config["DATABASE"])
    except Exception:
        app.logger.warning("Buscador (B1): siembra canónica falló (fail-open).")

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(buscador_bp)
    app.register_blueprint(frontend_bp)
    return app
