"""Revocación real de access tokens vía token_version (parche de seguridad).

Antes: el logout solo borraba refresh tokens; un access token robado seguía
valiendo hasta expirar (y el flujo legacy /auth/refresh lo renovaba para
siempre). Ahora el logout sube `users.token_version` y token_required exige
coincidencia, así que el token emitido deja de servir de inmediato (T13).
"""

import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db

PASSWORD = "ValidPass123!"
EMAIL = "rev@example.com"


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(prefix="test_revoke_", suffix=".db")
    os.close(db_fd)

    app = create_app(db_path=db_path)
    app.config.update({"TESTING": True})

    with app.app_context():
        init_db()
        db = sqlite3.connect(db_path)
        db.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (EMAIL, "Rev", generate_password_hash(PASSWORD)),
        )
        db.commit()
        db.close()

    with app.test_client() as test_client:
        yield test_client

    try:
        os.unlink(db_path)
    except OSError:
        pass


def _login(client):
    resp = client.post("/auth/login", json={"email": EMAIL, "password": PASSWORD})
    assert resp.status_code == 200, resp.data
    return resp.get_json()["access_token"]


def test_logout_revokes_access_token(client):
    token = _login(client)
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/auth/me", headers=headers).status_code == 200

    assert client.post("/auth/logout", headers=headers).status_code == 200

    # El access token ya no sirve, aunque no haya expirado.
    assert client.get("/auth/me", headers=headers).status_code == 401


def test_login_again_after_logout_works(client):
    token = _login(client)
    client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})

    token2 = _login(client)
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 200


def test_token_version_mismatch_invalidates_token(client):
    token = _login(client)
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/auth/me", headers=headers).status_code == 200

    db = sqlite3.connect(client.application.config["DATABASE"])
    db.execute(
        "UPDATE users SET token_version = token_version + 1 WHERE email = ?",
        (EMAIL,),
    )
    db.commit()
    db.close()

    assert client.get("/auth/me", headers=headers).status_code == 401


def test_token_for_unknown_user_rejected(client):
    from app.jwt_utils import create_token

    token = create_token({"user_id": 99999, "email": "ghost@example.com"})
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401
