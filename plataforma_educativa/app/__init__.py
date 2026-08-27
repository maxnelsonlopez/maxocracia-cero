# -*- coding: utf-8 -*-
"""Fábrica de la aplicación Flask de la Plataforma Educativa.

La plataforma es una aplicación independiente, pero conceptualmente compatible
con Maxocracia. Vive por completo dentro de ``plataforma_educativa/``.
"""

import os

from flask import Flask

from . import db, schema
from .api_routes import api_bp
from .auth_routes import auth_bp
from .frontend_routes import frontend_bp

# Ruta por defecto de la base SQLite (junto a este módulo, en la carpeta raíz
# de la plataforma).
_DEFAULT_DB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plataforma_educativa.db"
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

    db.init_app(app)
    schema.init_db(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(frontend_bp)
    return app
