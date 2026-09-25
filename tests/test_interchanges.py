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

    app = create_app(db_path)
    app.config["TESTING"] = True

    # initialize db
    with app.app_context():
        init_db(app)

    with app.test_client() as client:
        yield client

    # cleanup
    try:
        os.remove(db_path)
    except OSError:
        pass


def seed_user(db_path, email, name="Test User"):
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


def test_create_interchange_and_credit(client):
    # create two users in the test DB
    db_path = client.application.config["DATABASE"]
    giver_id = seed_user(db_path, "giver@example.test", "Giver")
    receiver_id = seed_user(db_path, "receiver@example.test", "Receiver")
    token = _login(client, "giver@example.test")

    payload = {
        "interchange_id": "TEST-INT-001",
        "receiver_id": receiver_id,
        "description": "Helping with gardening",
        "uth_hours": 2.0,
        "impact_resolution_score": 4,
    }

    # POST interchange (el giver sale del token)
    resp = client.post(
        "/interchanges", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "credit" in data
    credit_amount = data["credit"]

    # check ledger for giver
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?", (giver_id,)
    )
    row = cur.fetchone()
    conn.close()
    assert row is not None
    assert row[0] == pytest.approx(credit_amount)


def test_list_interchanges_requires_token(client):
    """El historial de intercambios ya no es público."""
    resp = client.get("/interchanges")
    assert resp.status_code == 401


def test_list_interchanges_only_own(client):
    """Cada integrante ve solo sus intercambios (admin vería todo)."""
    db_path = client.application.config["DATABASE"]
    giver_id = seed_user(db_path, "giver2@example.test", "Giver2")
    receiver_id = seed_user(db_path, "receiver2@example.test", "Receiver2")
    seed_user(db_path, "outsider@example.test", "Outsider")

    token = _login(client, "giver2@example.test")
    resp = client.post(
        "/interchanges",
        json={
            "interchange_id": "TEST-INT-OWN",
            "receiver_id": receiver_id,
            "description": "Clase de matemáticas",
            "uth_hours": 1.0,
            "impact_resolution_score": 2,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201

    own = client.get("/interchanges", headers={"Authorization": f"Bearer {token}"})
    assert own.status_code == 200
    rows = own.get_json()
    assert rows
    assert all(
        r["giver_id"] in (giver_id, receiver_id)
        or r["receiver_id"] in (giver_id, receiver_id)
        for r in rows
    )

    outsider_token = _login(client, "outsider@example.test")
    other = client.get(
        "/interchanges", headers={"Authorization": f"Bearer {outsider_token}"}
    )
    assert other.status_code == 200
    assert other.get_json() == []


def test_create_interchange_requiere_token(client):
    db_path = client.application.config["DATABASE"]
    giver_id = seed_user(db_path, "anon_giver@example.test", "Anon")
    receiver_id = seed_user(db_path, "anon_receiver@example.test", "AnonR")
    resp = client.post(
        "/interchanges",
        json={
            "interchange_id": "TEST-INT-002",
            "giver_id": giver_id,
            "receiver_id": receiver_id,
            "description": "x",
        },
    )
    assert resp.status_code == 401


def _login(client, email, password="Password1"):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]
