"""
Tests para las mutaciones CRUD de admin (RF-G4 fase 2).

Cubre PUT/DELETE de intercambios (forms), seguimientos (forms) y
productos VHV (vhv): autenticación, autorización (admin/propietario),
404 y casos exitosos.
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
    """Aplicación con base de datos temporal, usuario normal, otro usuario y admin."""
    os.environ["SECRET_KEY"] = "test-secret-key-123"
    os.environ["FLASK_ENV"] = "testing"

    db_fd, db_path = tempfile.mkstemp(prefix="test_admin_crud_", suffix=".db")
    os.close(db_fd)

    app = create_app(db_path)
    app.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key-123",
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
        ("other@example.test", "Other", generate_password_hash("Password1"), 0),
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


def _db(client):
    return sqlite3.connect(client.application.config["DATABASE"])


def _user_id(db_path, email):
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row[0]


def _seed_exchange(db_path, giver, receiver):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO interchange (
            interchange_id, date, giver_id, receiver_id, type, description,
            urgency, uth_hours, impact_resolution_score, reciprocity_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "CRUD-INT-001",
            "2026-08-01",
            giver,
            receiver,
            "UTH",
            "Ayuda de prueba",
            "Media",
            2.0,
            5,
            "unidirectional",
        ),
    )
    exchange_id = cur.lastrowid
    conn.commit()
    conn.close()
    return exchange_id


def _seed_followup(db_path, participant_email="participante@example.test"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, need_urgency)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Participante CRUD",
            participant_email,
            "Bogotá",
            "Chapinero",
            "Puedo ayudar",
            "Necesito ayuda",
            "Baja",
        ),
    )
    participant_id = cur.lastrowid
    cur.execute(
        """
        INSERT INTO follow_ups (
            follow_up_date, participant_id, follow_up_type, current_situation,
            situation_change, active_interchanges_status, follow_up_priority
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "2026-08-01",
            participant_id,
            "routine_check",
            "Situación estable",
            "same",
            "none",
            "low",
        ),
    )
    followup_id = cur.lastrowid
    conn.commit()
    conn.close()
    return followup_id


def _seed_product(db_path, created_by=None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO vhv_products (name, category, description, created_by) VALUES (?, ?, ?, ?)",
        ("Producto CRUD", "food", "Producto de prueba", created_by),
    )
    product_id = cur.lastrowid
    conn.commit()
    conn.close()
    return product_id


# ==================== INTERCAMBIOS (forms) ====================


def test_put_exchange_requires_auth(client):
    resp = client.put("/forms/exchanges/1", json={"description": "x"})
    assert resp.status_code == 401


def test_delete_exchange_requires_auth(client):
    resp = client.delete("/forms/exchanges/1")
    assert resp.status_code == 401


def test_put_exchange_forbidden_for_outsider(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, other_id, other_id)
    token = _login(client, "user@example.test")
    resp = client.put(
        f"/forms/exchanges/{exchange_id}",
        json={"description": "cambio"},
        headers=token,
    )
    assert resp.status_code == 403


def test_delete_exchange_forbidden_for_outsider(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, other_id, other_id)
    token = _login(client, "user@example.test")
    resp = client.delete(f"/forms/exchanges/{exchange_id}", headers=token)
    assert resp.status_code == 403


def test_put_exchange_success_as_owner(client):
    db_path = client.application.config["DATABASE"]
    user_id = _user_id(db_path, "user@example.test")
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, user_id, other_id)
    token = _login(client, "user@example.test")
    resp = client.put(
        f"/forms/exchanges/{exchange_id}",
        json={"description": "Cambio del propietario"},
        headers=token,
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    conn = _db(client)
    desc = conn.execute(
        "SELECT description FROM interchange WHERE id = ?", (exchange_id,)
    ).fetchone()[0]
    conn.close()
    assert desc == "Cambio del propietario"


def test_put_exchange_success_as_admin(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, other_id, other_id)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/forms/exchanges/{exchange_id}",
        json={"urgency": "Alta", "uth_hours": 5.0, "facilitator_notes": "Revisado"},
        headers=token,
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    conn = _db(client)
    row = conn.execute(
        "SELECT urgency, uth_hours FROM interchange WHERE id = ?", (exchange_id,)
    ).fetchone()
    conn.close()
    assert row[0] == "Alta"
    assert row[1] == 5.0


def test_put_exchange_invalid_urgency(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, other_id, other_id)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/forms/exchanges/{exchange_id}",
        json={"urgency": "Urgentísima"},
        headers=token,
    )
    assert resp.status_code == 400


def test_put_exchange_not_found(client):
    token = _login(client, "admin@example.test")
    resp = client.put(
        "/forms/exchanges/99999", json={"description": "x"}, headers=token
    )
    assert resp.status_code == 404


def test_delete_exchange_success_as_owner(client):
    db_path = client.application.config["DATABASE"]
    user_id = _user_id(db_path, "user@example.test")
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, user_id, other_id)
    token = _login(client, "user@example.test")
    resp = client.delete(f"/forms/exchanges/{exchange_id}", headers=token)
    assert resp.status_code == 200

    conn = _db(client)
    count = conn.execute(
        "SELECT COUNT(*) FROM interchange WHERE id = ?", (exchange_id,)
    ).fetchone()[0]
    conn.close()
    assert count == 0


def test_delete_exchange_success_as_admin(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    exchange_id = _seed_exchange(db_path, other_id, other_id)
    token = _login(client, "admin@example.test")
    resp = client.delete(f"/forms/exchanges/{exchange_id}", headers=token)
    assert resp.status_code == 200

    conn = _db(client)
    count = conn.execute(
        "SELECT COUNT(*) FROM interchange WHERE id = ?", (exchange_id,)
    ).fetchone()[0]
    conn.close()
    assert count == 0


def test_delete_exchange_not_found(client):
    token = _login(client, "admin@example.test")
    resp = client.delete("/forms/exchanges/99999", headers=token)
    assert resp.status_code == 404


# ==================== SEGUIMIENTOS (forms) ====================


def test_put_followup_requires_auth(client):
    resp = client.put("/forms/follow-ups/1", json={"current_situation": "x"})
    assert resp.status_code == 401


def test_delete_followup_requires_auth(client):
    resp = client.delete("/forms/follow-ups/1")
    assert resp.status_code == 401


def test_put_followup_forbidden_for_outsider(client):
    db_path = client.application.config["DATABASE"]
    followup_id = _seed_followup(db_path, participant_email="other@example.test")
    token = _login(client, "user@example.test")
    resp = client.put(
        f"/forms/follow-ups/{followup_id}",
        json={"current_situation": "cambio"},
        headers=token,
    )
    assert resp.status_code == 403


def test_put_followup_success_as_owner(client):
    db_path = client.application.config["DATABASE"]
    followup_id = _seed_followup(db_path, participant_email="user@example.test")
    token = _login(client, "user@example.test")
    resp = client.put(
        f"/forms/follow-ups/{followup_id}",
        json={"current_situation": "Mejoró notablemente", "follow_up_priority": "high"},
        headers=token,
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    conn = _db(client)
    row = conn.execute(
        "SELECT current_situation, follow_up_priority FROM follow_ups WHERE id = ?",
        (followup_id,),
    ).fetchone()
    conn.close()
    assert row[0] == "Mejoró notablemente"
    assert row[1] == "high"


def test_put_followup_success_as_admin(client):
    db_path = client.application.config["DATABASE"]
    followup_id = _seed_followup(db_path)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/forms/follow-ups/{followup_id}",
        json={
            "current_situation": "Mejoró notablemente",
            "follow_up_priority": "high",
            "need_level": 2,
            "actions_required": ["seguimiento_social"],
        },
        headers=token,
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    conn = _db(client)
    row = conn.execute(
        "SELECT current_situation, follow_up_priority, actions_required FROM follow_ups WHERE id = ?",
        (followup_id,),
    ).fetchone()
    conn.close()
    assert row[0] == "Mejoró notablemente"
    assert row[1] == "high"
    assert '"seguimiento_social"' in row[2]


def test_put_followup_invalid_priority(client):
    db_path = client.application.config["DATABASE"]
    followup_id = _seed_followup(db_path)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/forms/follow-ups/{followup_id}",
        json={"follow_up_priority": "urgent"},
        headers=token,
    )
    assert resp.status_code == 400


def test_put_followup_invalid_need_level(client):
    db_path = client.application.config["DATABASE"]
    followup_id = _seed_followup(db_path)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/forms/follow-ups/{followup_id}",
        json={"need_level": 9},
        headers=token,
    )
    assert resp.status_code == 400


def test_put_followup_not_found(client):
    token = _login(client, "admin@example.test")
    resp = client.put(
        "/forms/follow-ups/99999", json={"current_situation": "x"}, headers=token
    )
    assert resp.status_code == 404


def test_delete_followup_success_as_admin(client):
    db_path = client.application.config["DATABASE"]
    followup_id = _seed_followup(db_path)
    token = _login(client, "admin@example.test")
    resp = client.delete(f"/forms/follow-ups/{followup_id}", headers=token)
    assert resp.status_code == 200

    conn = _db(client)
    count = conn.execute(
        "SELECT COUNT(*) FROM follow_ups WHERE id = ?", (followup_id,)
    ).fetchone()[0]
    conn.close()
    assert count == 0


def test_delete_followup_not_found(client):
    token = _login(client, "admin@example.test")
    resp = client.delete("/forms/follow-ups/99999", headers=token)
    assert resp.status_code == 404


# ==================== PRODUCTOS VHV ====================


def test_put_product_requires_auth(client):
    resp = client.put("/vhv/products/1", json={"name": "x"})
    assert resp.status_code == 401


def test_delete_product_requires_auth(client):
    resp = client.delete("/vhv/products/1")
    assert resp.status_code == 401


def test_put_product_forbidden_for_non_admin_and_non_owner(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    product_id = _seed_product(db_path, created_by=other_id)
    token = _login(client, "user@example.test")
    resp = client.put(
        f"/vhv/products/{product_id}",
        json={"name": "Hackeado"},
        headers=token,
    )
    assert resp.status_code == 403


def test_delete_product_forbidden_for_non_admin_and_non_owner(client):
    db_path = client.application.config["DATABASE"]
    other_id = _user_id(db_path, "other@example.test")
    product_id = _seed_product(db_path, created_by=other_id)
    token = _login(client, "user@example.test")
    resp = client.delete(f"/vhv/products/{product_id}", headers=token)
    assert resp.status_code == 403


def test_put_product_success_as_owner(client):
    db_path = client.application.config["DATABASE"]
    user_id = _user_id(db_path, "user@example.test")
    product_id = _seed_product(db_path, created_by=user_id)
    token = _login(client, "user@example.test")
    resp = client.put(
        f"/vhv/products/{product_id}",
        json={"name": "Producto del Propietario"},
        headers=token,
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    conn = _db(client)
    name = conn.execute(
        "SELECT name FROM vhv_products WHERE id = ?", (product_id,)
    ).fetchone()[0]
    conn.close()
    assert name == "Producto del Propietario"


def test_put_product_success_as_admin(client):
    db_path = client.application.config["DATABASE"]
    product_id = _seed_product(db_path)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/vhv/products/{product_id}",
        json={
            "name": "Producto Actualizado",
            "category": "electronics",
            "description": "Descripción nueva",
            "t_direct_hours": 2.0,
        },
        headers=token,
    )
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

    conn = _db(client)
    row = conn.execute(
        "SELECT name, maxo_price, vhv_json FROM vhv_products WHERE id = ?",
        (product_id,),
    ).fetchone()
    conn.close()
    assert row[0] == "Producto Actualizado"
    assert row[1] is not None
    assert row[2] is not None


def test_put_product_invalid_consciousness_factor(client):
    db_path = client.application.config["DATABASE"]
    product_id = _seed_product(db_path)
    token = _login(client, "admin@example.test")
    resp = client.put(
        f"/vhv/products/{product_id}",
        json={"v_consciousness_factor": 1.5},
        headers=token,
    )
    assert resp.status_code == 400


def test_put_product_not_found(client):
    token = _login(client, "admin@example.test")
    resp = client.put("/vhv/products/99999", json={"name": "x"}, headers=token)
    assert resp.status_code == 404


def test_delete_product_success_as_admin(client):
    db_path = client.application.config["DATABASE"]
    product_id = _seed_product(db_path)
    token = _login(client, "admin@example.test")
    resp = client.delete(f"/vhv/products/{product_id}", headers=token)
    assert resp.status_code == 200

    conn = _db(client)
    count = conn.execute(
        "SELECT COUNT(*) FROM vhv_products WHERE id = ?", (product_id,)
    ).fetchone()[0]
    conn.close()
    assert count == 0


def test_delete_product_not_found(client):
    token = _login(client, "admin@example.test")
    resp = client.delete("/vhv/products/99999", headers=token)
    assert resp.status_code == 404
