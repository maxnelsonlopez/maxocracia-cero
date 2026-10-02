"""Restablecimiento de contraseña: token de un solo uso, anti-enumeración.

- POST /auth/forgot siempre 200 genérico; en TESTING expone reset_token.
- POST /auth/reset fija la clave, invalida la anterior y quema el token.
- Tokens vencidos, reusados o débiles se rechazan sin filtrar existencia.
"""

import hashlib
import os
import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db


@pytest.fixture
def client():
    os.environ["SECRET_KEY"] = "test-secret-key-maxocracia-0123456789abcdef"
    os.environ["FLASK_ENV"] = "testing"

    db_fd, db_path = tempfile.mkstemp(prefix="test_pwd_reset_", suffix=".db")
    os.close(db_fd)

    app = create_app(db_path)
    app.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key-maxocracia-0123456789abcdef",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        init_db()

    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        ("vecina@example.test", "Vecina", generate_password_hash("Antigua11")),
    )
    conn.commit()
    conn.close()

    with app.test_client() as test_client:
        test_client.application.config["DATABASE"] = db_path
        yield test_client

    try:
        os.unlink(db_path)
    except OSError:
        pass


def _forgot(client, email):
    return client.post("/auth/forgot", json={"email": email})


def test_flujo_completo_y_quema_token(client):
    resp = _forgot(client, "vecina@example.test")
    assert resp.status_code == 200
    token = resp.get_json().get("reset_token")
    assert token

    # Contraseña débil se rechaza
    debil = client.post("/auth/reset", json={"token": token, "password": "corta"})
    assert debil.status_code == 400

    # Reset válido
    ok = client.post(
        "/auth/reset", json={"token": token, "password": "NuevaClave22"}
    )
    assert ok.status_code == 200

    # Reuso del mismo token se rechaza
    reuso = client.post(
        "/auth/reset", json={"token": token, "password": "OtraClave33"}
    )
    assert reuso.status_code == 400

    # La antigua ya no entra, la nueva sí
    vieja = client.post(
        "/auth/login",
        json={"email": "vecina@example.test", "password": "Antigua11"},
    )
    assert vieja.status_code == 401
    nueva = client.post(
        "/auth/login",
        json={"email": "vecina@example.test", "password": "NuevaClave22"},
    )
    assert nueva.status_code == 200


def test_no_enumera_cuentas(client):
    resp = _forgot(client, "nadie@example.test")
    assert resp.status_code == 200
    body = resp.get_json()
    assert "message" in body
    assert "reset_token" not in body

    resp = _forgot(client, "no-es-email")
    assert resp.status_code == 200
    assert "reset_token" not in resp.get_json()


def test_token_invalido_y_expirado(client):
    malo = client.post(
        "/auth/reset", json={"token": "invento", "password": "NuevaClave22"}
    )
    assert malo.status_code == 400

    # Token expirado insertado a mano
    raw = "expirado-0123456789"
    thash = hashlib.sha256(raw.encode()).hexdigest()
    db_path = client.application.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    uid = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("vecina@example.test",)
    ).fetchone()[0]
    pasado = (datetime.now(timezone.utc) - timedelta(hours=2)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    conn.execute(
        "INSERT INTO password_resets (user_id, token_hash, expires_at) VALUES (?, ?, ?)",
        (uid, thash, pasado),
    )
    conn.commit()
    conn.close()

    resp = client.post(
        "/auth/reset", json={"token": raw, "password": "NuevaClave22"}
    )
    assert resp.status_code == 400
