# -*- coding: utf-8 -*-
"""Endurecimiento de seguridad (jornada hardening, sep 2026).

Cubre la cadena de secretos y el HTTPS forzado:
- SECRET_KEY fail-closed en producción (run.py guarda por CLI, create_app
  por factory — despliegues WSGI sin run.py también quedan protegidos).
- FORCE_HTTPS=1 redirige 308 http→https según X-Forwarded-Proto.
- El CSP de producción no anuncia WebSocket de localhost (solo dev).
- El fallback de desarrollo ya no usa claves < 32 bytes (PyJWT 2.13
  advierte claves HMAC cortas, RFC 7518 §3.2).
"""

import io
import os
import re

import pytest

from app import create_app

BASE_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def restore_env():
    """Guarda y restaura las variables de entorno que tocan los tests."""
    keys = ["SECRET_KEY", "FLASK_ENV", "FORCE_HTTPS"]
    saved = {k: os.environ.get(k) for k in keys}
    yield
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def test_produccion_sin_secret_key_rechaza_arranque(restore_env):
    """create_app con FLASK_ENV=production y sin SECRET_KEY debe fallar."""
    os.environ.pop("SECRET_KEY", None)
    os.environ["FLASK_ENV"] = "production"
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(db_path=":memory:")


def test_desarrollo_sin_secret_key_mantiene_fallback(restore_env):
    """Fuera de producción el fallback de desarrollo sigue desbloqueando."""
    import tempfile

    fd, db_path = tempfile.mkstemp(prefix="test_sec_", suffix=".db")
    os.close(fd)
    try:
        os.environ.pop("SECRET_KEY", None)
        os.environ["FLASK_ENV"] = "development"
        app = create_app(db_path=db_path)
        assert app.config["SECRET_KEY"] == "dev-secret"
    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass


def test_fallback_desarrollo_supera_32_bytes():
    """La clave de desarrollo forzada por run.py ya no es corta (PyJWT 2.13)."""
    with io.open(os.path.join(BASE_REPO, "run.py"), "r", encoding="utf-8") as fh:
        contenido = fh.read()
    match = re.search(r'SECRET_KEY"\] = "([^"]+)"', contenido)
    assert match, "no se encontró el fallback de SECRET_KEY en run.py"
    assert len(match.group(1)) >= 32


def test_force_https_redirige_http_a_https(restore_env, app):
    """Con FORCE_HTTPS=1, una petición http se redirige 308 a https."""
    os.environ["FORCE_HTTPS"] = "1"
    client = app.test_client()
    resp = client.get("/favicon.ico", headers={"X-Forwarded-Proto": "http"})
    assert resp.status_code == 308
    assert resp.headers["Location"].startswith("https://")


def test_force_https_no_afecta_https_entrante(restore_env, app):
    """El tráfico que ya llegó por https (según el proxy) no se toca."""
    os.environ["FORCE_HTTPS"] = "1"
    client = app.test_client()
    resp = client.get("/favicon.ico", headers={"X-Forwarded-Proto": "https"})
    assert resp.status_code == 204


def test_force_https_apagado_por_defecto(restore_env, app):
    """Sin FORCE_HTTPS, http pasa tal cual (compatibilidad desarrollo)."""
    os.environ.pop("FORCE_HTTPS", None)
    client = app.test_client()
    resp = client.get("/favicon.ico", headers={"X-Forwarded-Proto": "http"})
    assert resp.status_code == 204


def test_csp_produccion_sin_websocket_localhost(restore_env, app):
    """En producción el CSP no anuncia ws://localhost:* (solo dev)."""
    os.environ["FLASK_ENV"] = "production"
    client = app.test_client()
    resp = client.get("/favicon.ico")
    csp = resp.headers["Content-Security-Policy"]
    assert "ws://localhost" not in csp
    assert "https://api.stripe.com" in csp


def test_csp_desarrollo_mantiene_websocket_localhost(restore_env, app):
    """En desarrollo el HMR de Next.js sigue permitido."""
    os.environ["FLASK_ENV"] = "development"
    client = app.test_client()
    resp = client.get("/favicon.ico")
    csp = resp.headers["Content-Security-Policy"]
    assert "ws://localhost:*" in csp


def test_hsts_presente_con_testing(restore_env, app):
    """La cabecera HSTS se emite cuando el esquema es seguro (o testing)."""
    app.config["TESTING"] = True
    client = app.test_client()
    resp = client.get("/favicon.ico")
    assert "max-age=31536000" in resp.headers.get("Strict-Transport-Security", "")
