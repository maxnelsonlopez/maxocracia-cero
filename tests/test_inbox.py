"""Bandeja interna: relevo cuando el correo no llega.

- Generar invitación deja fila en bandeja (link compartible visible).
- Pedir reset deja fila, pero el link se redacta al propio dueño.
- El outbox es solo admin; marcar leído solo lo propio.
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

    db_fd, db_path = tempfile.mkstemp(prefix="test_inbox_", suffix=".db")
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
        "INSERT INTO users (email, name, password_hash, is_admin) VALUES (?, ?, ?, ?)",
        ("user@example.test", "User", generate_password_hash("Password1"), 0),
    )
    conn.execute(
        "INSERT INTO users (email, name, password_hash, is_admin) VALUES (?, ?, ?, ?)",
        ("admin@example.test", "Admin", generate_password_hash("Password1"), 1),
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


def test_invite_llega_a_bandeja_y_outbox(client):
    admin = _login(client, "admin@example.test")
    resp = client.post(
        "/invite/generate", json={"email": "user@example.test"}, headers=admin
    )
    assert resp.status_code == 201
    url = resp.get_json()["invite_url"]

    # El dueño la ve con su link (las invitaciones son compartibles)
    user = _login(client, "user@example.test")
    bandeja = client.get("/inbox", headers=user)
    assert bandeja.status_code == 200
    mensajes = bandeja.get_json()
    assert len(mensajes) == 1
    assert mensajes[0]["kind"] == "invite"
    assert mensajes[0]["link_url"] == url
    assert mensajes[0]["status"] == "sent"

    # Marcar leído
    mid = mensajes[0]["id"]
    leido = client.post(f"/inbox/{mid}/read", headers=user)
    assert leido.status_code == 200
    assert client.get("/inbox", headers=user).get_json()[0]["status"] == "read"

    # Outbox admin con link completo
    outbox = client.get("/inbox/outbox", headers=admin)
    assert outbox.status_code == 200
    assert any(m["link_url"] == url for m in outbox.get_json())


def test_reset_redacta_link_al_dueno(client, monkeypatch):
    for var in ("SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD", "SMTP_PORT"):
        monkeypatch.delenv(var, raising=False)
    admin = _login(client, "admin@example.test")
    resp = client.post("/auth/forgot", json={"email": "user@example.test"})
    assert resp.status_code == 200

    # El dueño ve el aviso pero SIN el token (el correo autentica)
    user = _login(client, "user@example.test")
    bandeja = client.get("/inbox", headers=user).get_json()
    resets = [m for m in bandeja if m["kind"] == "password_reset"]
    assert len(resets) == 1
    assert resets[0]["link_url"] is None
    assert resets[0]["has_link"] is True
    # Sin SMTP, el estado visible explica por qué no llegó el correo
    assert resets[0]["mail_status"] == "skipped"

    # El facilitador sí ve el link para relevarlo de viva voz
    outbox = client.get("/inbox/outbox?kind=password_reset", headers=admin)
    assert outbox.status_code == 200
    assert len(outbox.get_json()) == 1
    assert "/reset?token=" in outbox.get_json()[0]["link_url"]
    assert outbox.get_json()[0]["mail_status"] == "skipped"


def test_outbox_solo_admin_y_lectura_ajena_404(client):
    user = _login(client, "user@example.test")
    assert client.get("/inbox/outbox", headers=user).status_code == 403
    assert client.get("/inbox/outbox").status_code == 401
    # Leer mensaje inexistente o ajeno
    assert client.post("/inbox/9999/read", headers=user).status_code == 404
