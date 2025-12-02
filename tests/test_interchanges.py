import os
import sqlite3
import tempfile

import pytest

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


from werkzeug.security import generate_password_hash


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

    payload = {
        "interchange_id": "TEST-INT-001",
        "giver_id": giver_id,
        "receiver_id": receiver_id,
        "description": "Helping with gardening",
        "uth_hours": 2.0,
        "impact_resolution_score": 4,
    }

    # POST interchange
    resp = client.post("/interchanges", json=payload)
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
