import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(prefix="test_comun_", suffix=".db")
    os.close(db_fd)

    # Configurar SECRET_KEY para pruebas
    os.environ["SECRET_KEY"] = "clave_secreta_para_pruebas"

    app = create_app(db_path)
    app.config["TESTING"] = True
    with app.app_context():
        init_db(app)
    with app.test_client() as client:
        yield client
    try:
        os.remove(db_path)
    except OSError:
        pass


def seed_user(db_path, email, name="Tester"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        (email, name, generate_password_hash("Password1")),
    )
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def login_and_token(client, email):
    resp = client.post("/auth/login", json={"email": email, "password": "Password1"})
    assert resp.status_code == 200
    return resp.get_json().get("token")


def test_refresh_returns_new_token(client):
    # Primero creamos un usuario de prueba
    db_path = client.application.config["DATABASE"]
    seed_user(db_path, "test@example.com", "Test User")

    # Luego hacemos login para obtener un token de refresco
    login_resp = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password1",  # Usamos la contraseña por defecto de seed_user
        },
    )
    assert login_resp.status_code == 200
    login_data = login_resp.get_json()
    refresh_token = login_data.get("refresh_token")
    assert refresh_token, "No se recibió token de refresco"

    # Ahora intentamos refrescar el token
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200, f"Error al refrescar el token: {resp.data}"
    data = resp.get_json()
    assert "access_token" in data, "No se recibió un nuevo token de acceso"
    assert "refresh_token" in data, "No se recibió un nuevo token de refresco"


def test_refresh_requires_token(client):
    resp = client.post("/auth/refresh")
    assert resp.status_code == 401


def test_refresh_rejects_expired_token(client):
    """Endurecimiento: un access token expirado ya no se puede refrescar
    (antes permitía renovar indefinidamente un token robado)."""
    db_path = client.application.config["DATABASE"]
    uid = seed_user(db_path, "r2@example.test", "R2")
    # create a token that expires immediately using jwt_utils.create_token
    from app.jwt_utils import create_token

    tok = create_token({"user_id": uid, "email": "r2@example.test"}, expires_in=1)
    import time

    time.sleep(2)
    resp = client.post("/auth/refresh", headers={"Authorization": f"Bearer {tok}"})
    assert resp.status_code == 401


def test_refresh_with_valid_bearer_rereads_user(client):
    """El flujo legacy sigue vivo para tokens vigentes y reemite releyendo
    la BD (rol y token_version actuales, no los del token viejo)."""
    db_path = client.application.config["DATABASE"]
    uid = seed_user(db_path, "r3@example.test", "R3")
    from app.jwt_utils import create_token

    tok = create_token({"user_id": uid, "email": "r3@example.test", "is_admin": 1})
    resp = client.post("/auth/refresh", headers={"Authorization": f"Bearer {tok}"})
    assert resp.status_code == 200
    new_token = resp.get_json().get("token")
    assert new_token

    from app.jwt_utils import verify_token

    claims = verify_token(new_token)
    assert claims is not None
    # El usuario no es admin en la BD: el reclamo no se hereda del token viejo.
    assert not claims.get("is_admin")
    assert claims.get("token_version") == 0
