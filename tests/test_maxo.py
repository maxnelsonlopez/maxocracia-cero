import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db


@pytest.fixture
def client():
    # Configurar variables de entorno para pruebas
    os.environ["SECRET_KEY"] = "test-secret-key-123"
    os.environ["FLASK_ENV"] = "testing"

    # Crear base de datos temporal
    db_fd, db_path = tempfile.mkstemp(prefix="test_comun_", suffix=".db")
    os.close(db_fd)

    # Crear y configurar la aplicación
    app = create_app(db_path)
    app.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key-123",
            "WTF_CSRF_ENABLED": False,
        }
    )

    # Inicializar la base de datos
    with app.app_context():
        init_db()

    # Crear un cliente de prueba
    with app.test_client() as client:
        # Pasar la ruta de la base de datos al cliente para usarla en las pruebas
        client.application.config["DATABASE"] = db_path
        yield client

    # Limpieza: eliminar el archivo de la base de datos después de la prueba
    try:
        os.unlink(db_path)
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


def test_balance_and_transfer(client):
    db_path = client.application.config["DATABASE"]
    a = seed_user(db_path, "a@example.test", "A")
    b = seed_user(db_path, "b@example.test", "B")

    # login as A to get token
    resp = client.post(
        "/auth/login", json={"email": "a@example.test", "password": "Password1"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    token = data.get("access_token")
    assert token is not None, f"No se recibió access_token en la respuesta: {data}"

    # initial balances 0 (requires auth)
    resp = client.get(
        f"/maxo/{a}/balance", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["balance"] == 0

    # credit A with 10 to allow the transfer
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)",
        (a, 10.0, "seed credit"),
    )
    conn.commit()
    conn.close()

    # transfer 5 from A to B
    payload = {
        "from_user_id": a,
        "to_user_id": b,
        "amount": 5.0,
        "reason": "test transfer",
    }
    resp = client.post(
        "/maxo/transfer", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200

    # check ledger sums
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?", (a,))
    row = cur.fetchone()
    assert row[0] == 5.0
    cur.execute("SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?", (b,))
    row = cur.fetchone()
    assert row[0] == 5.0
    conn.close()


def _login(client, email, password="Password1"):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]


def test_ledger_propio(client):
    db_path = client.application.config["DATABASE"]
    a = seed_user(db_path, "ledger_a@example.test", "LedgerA")
    token = _login(client, "ledger_a@example.test")

    # sin movimientos: ledger vacío
    resp = client.get(f"/maxo/{a}/ledger", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["user_id"] == a
    assert data["count"] == 0
    assert data["entries"] == []

    # crédito + transferencia para generar movimientos
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)",
        (a, 10.0, "seed credit"),
    )
    conn.commit()
    conn.close()

    resp = client.get(f"/maxo/{a}/ledger", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] == 1
    entry = data["entries"][0]
    assert entry["change_amount"] == 10.0
    assert entry["reason"] == "seed credit"
    assert "created_at" in entry
    assert "id" in entry

    # el orden es de más reciente a más antiguo
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)",
        (a, -3.0, "otro movimiento"),
    )
    conn.commit()
    conn.close()
    resp = client.get(f"/maxo/{a}/ledger", headers={"Authorization": f"Bearer {token}"})
    data = resp.get_json()
    assert data["count"] == 2
    assert data["entries"][0]["change_amount"] == -3.0
    assert data["entries"][1]["change_amount"] == 10.0


def test_ledger_ajeno_forbidden(client):
    db_path = client.application.config["DATABASE"]
    a = seed_user(db_path, "ledger_owner@example.test", "Owner")
    seed_user(db_path, "ledger_intruder@example.test", "Intruder")
    token_b = _login(client, "ledger_intruder@example.test")

    resp = client.get(
        f"/maxo/{a}/ledger", headers={"Authorization": f"Bearer {token_b}"}
    )
    assert resp.status_code == 403
    assert resp.get_json()["error"].startswith("forbidden")


def test_ledger_admin_ve_ajeno(client):
    db_path = client.application.config["DATABASE"]
    a = seed_user(db_path, "ledger_victim@example.test", "Victim")
    admin_id = seed_user(db_path, "ledger_admin@example.test", "Admin")
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (admin_id,))
    conn.commit()
    conn.close()
    token_admin = _login(client, "ledger_admin@example.test")

    resp = client.get(
        f"/maxo/{a}/ledger", headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert resp.status_code == 200
    assert resp.get_json()["user_id"] == a


def test_ledger_sin_auth(client):
    db_path = client.application.config["DATABASE"]
    a = seed_user(db_path, "ledger_anon@example.test", "Anon")
    resp = client.get(f"/maxo/{a}/ledger")
    assert resp.status_code == 401
