"""Panel admin de usuarios: fecha de registro y generación de invitaciones.

Cubre RF-G admin:
- GET /subscriptions/admin/users expone created_at, trust_level e is_admin.
- Solo admin (403 para no admin).
- POST /invite/generate crea invitación firmada válida en GET /invite/<token>.
"""

import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db


@pytest.fixture
def client():
    os.environ["SECRET_KEY"] = "test-secret-key-maxocracia-0123456789abcdef"
    os.environ["FLASK_ENV"] = "testing"

    db_fd, db_path = tempfile.mkstemp(prefix="test_admin_users_panel_", suffix=".db")
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
        "INSERT INTO users (email, name, password_hash, is_admin, trust_level) VALUES (?, ?, ?, ?, ?)",
        ("user@example.test", "User", generate_password_hash("Password1"), 0, 0),
    )
    conn.execute(
        "INSERT INTO users (email, name, password_hash, is_admin, trust_level) VALUES (?, ?, ?, ?, ?)",
        ("admin@example.test", "Admin", generate_password_hash("Password1"), 1, 1),
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


def _login(client, email):
    resp = client.post("/auth/login", json={"email": email, "password": "Password1"})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.get_json()['access_token']}"}


def test_admin_users_expone_fecha_y_confianza(client):
    headers = _login(client, "admin@example.test")
    resp = client.get("/subscriptions/admin/users", headers=headers)
    assert resp.status_code == 200
    users = resp.get_json()
    assert len(users) >= 2
    primero = users[0]
    assert "created_at" in primero and primero["created_at"]
    assert "trust_level" in primero
    assert "is_admin" in primero


def test_admin_users_requiere_admin(client):
    headers = _login(client, "user@example.test")
    resp = client.get("/subscriptions/admin/users", headers=headers)
    assert resp.status_code == 403


def test_generate_invite_y_validacion(client):
    headers = _login(client, "admin@example.test")
    resp = client.post(
        "/invite/generate", json={"email": "vecina@example.test"}, headers=headers
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["email"] == "vecina@example.test"
    assert "token" in data and "." in data["token"]
    assert data["invite_url"].startswith("/invite?t=")
    assert data["register_url"].startswith("/register?email=")

    # El token generado abre la puerta pública
    token = data["token"]
    puerta = client.get(f"/invite/{token}")
    assert puerta.status_code == 200
    assert puerta.get_json()["valid"] is True


def test_generate_invite_valida_email_y_permiso(client):
    headers_user = _login(client, "user@example.test")
    resp = client.post(
        "/invite/generate", json={"email": "x@example.test"}, headers=headers_user
    )
    assert resp.status_code == 403

    headers_admin = _login(client, "admin@example.test")
    resp = client.post("/invite/generate", json={"email": "no-es-email"}, headers=headers_admin)
    assert resp.status_code == 400
