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


def test_reputation_flow(client):
    db_path = client.application.config["DATABASE"]
    u = seed_user(db_path, "rep@example.test", "Rep")
    seed_user(db_path, "reviewer@example.test", "Reviewer")
    token = _login(client, "reviewer@example.test")

    resp = client.get(f"/reputation/{u}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["score"] == 0.0

    resp = client.post(
        "/reputation/review",
        json={"user_id": u, "score": 4.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    resp = client.get(f"/reputation/{u}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["score"] == 4.0


def test_review_requiere_token_y_no_autoresena(client):
    db_path = client.application.config["DATABASE"]
    u = seed_user(db_path, "auto@example.test", "Auto")
    token = _login(client, "auto@example.test")

    resp = client.post("/reputation/review", json={"user_id": u, "score": 5.0})
    assert resp.status_code == 401

    resp = client.post(
        "/reputation/review",
        json={"user_id": u, "score": 5.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400
    assert "a ti mismo" in resp.get_json()["error"]


def test_resources_flow(client):
    db_path = client.application.config["DATABASE"]
    seed_user(db_path, "res@example.test", "Res")
    token = _login(client, "res@example.test")
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/resources",
        json={
            "title": "Bike",
            "description": "A mountain bike",
            "category": "transport",
        },
        headers=headers,
    )
    assert resp.status_code == 201

    resp = client.get("/resources")
    assert resp.status_code == 200
    items = resp.get_json()
    assert len(items) == 1
    rid = items[0]["id"]

    # claim resource
    resp = client.post(f"/resources/{rid}/claim", json={}, headers=headers)
    assert resp.status_code == 200

    # subsequent claim should fail
    resp = client.post(f"/resources/{rid}/claim", json={}, headers=headers)
    assert resp.status_code == 400


def test_resources_requieren_token(client):
    db_path = client.application.config["DATABASE"]
    seed_user(db_path, "anon@example.test", "Anon")
    resp = client.post("/resources", json={"title": "X"})
    assert resp.status_code == 401
    resp = client.post("/resources/1/claim", json={})
    assert resp.status_code == 401


def _login(client, email, password="Password1"):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]
