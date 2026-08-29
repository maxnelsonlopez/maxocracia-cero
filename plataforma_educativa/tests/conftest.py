# -*- coding: utf-8 -*-
"""Configuración de pytest para la Plataforma Educativa.

Asegura que ``import app`` resuelva a ESTA plataforma (``plataforma_educativa/app``)
y no al backend de Maxocracia, que también se llama ``app``. Para eso se mete la
raíz de la plataforma al principio de ``sys.path`` antes de importar nada.
"""

import os
import sys

# Raíz de la plataforma = directorio padre de ``tests``.
_PLATFORM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _PLATFORM_ROOT)

# Clave compartida de prueba para la federación JWT (los tests de Gemini y los
# locales la usan; sin ella la federación queda fail-closed por diseño).
os.environ.setdefault("SECRET_KEY", "test-platform-secret")

import pytest  # noqa: E402

from app import create_app  # noqa: E402


@pytest.fixture
def app(tmp_path):
    """Crea una instancia con una base de datos temporal (no se queda en disco)."""
    db_path = str(tmp_path / "test_plataforma.db")
    application = create_app(db_path=db_path)
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    """Cliente de pruebas de Flask."""
    return app.test_client()
