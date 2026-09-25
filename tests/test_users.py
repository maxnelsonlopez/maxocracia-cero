"""
Tests for Users API endpoints.

Endurecimiento: el directorio exige sesión; el alta pública vive en
/auth/register y la alta administrativa exige admin (parche de seguridad).
"""

import json
import os
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db

PASSWORD = "Password1"


@pytest.fixture
def client():
    """Create test client with temporary database."""
    db_fd, db_path = tempfile.mkstemp(prefix="test_users_", suffix=".db")
    os.close(db_fd)

    app = create_app(db_path=db_path)
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})

    with app.app_context():
        init_db()

        # Add test users
        db = sqlite3.connect(db_path)
        db.execute(
            "INSERT INTO users (id, email, name, alias, is_admin, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (
                1,
                "user1@example.com",
                "User One",
                "user1",
                0,
                generate_password_hash(PASSWORD),
            ),
        )
        db.execute(
            "INSERT INTO users (id, email, name, alias, is_admin, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (
                2,
                "user2@example.com",
                "User Two",
                "user2",
                0,
                generate_password_hash(PASSWORD),
            ),
        )
        db.execute(
            "INSERT INTO users (id, email, name, alias, is_admin, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (
                3,
                "admin@example.com",
                "Admin User",
                "admin",
                1,
                generate_password_hash(PASSWORD),
            ),
        )
        db.commit()
        db.close()

    with app.test_client() as client:
        yield client

    # Cleanup
    try:
        os.unlink(db_path)
    except OSError:
        pass


def _login(client, email, password=PASSWORD):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.data
    return resp.get_json()["access_token"]


def _headers(client, email):
    return {"Authorization": f"Bearer {_login(client, email)}"}


class TestListUsers:
    """Test GET /users endpoint."""

    def test_list_users_requires_auth(self, client):
        """Sin token, el directorio no se expone (antes filtraba PII)."""
        response = client.get("/users")
        assert response.status_code == 401

    def test_list_users_success(self, client):
        """Test listing users returns all users for authenticated members."""
        response = client.get("/users", headers=_headers(client, "user1@example.com"))
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 2

        # Check structure
        user = data[0]
        assert "id" in user
        assert "email" in user
        assert "name" in user
        assert "password_hash" not in user  # Should be excluded

    def test_list_users_limit(self, client):
        """Test that list_users respects the 100 limit."""
        # Add more than 100 users
        db_path = client.application.config["DATABASE"]
        db = sqlite3.connect(db_path)
        for i in range(4, 106):
            db.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (
                    f"user{i}@example.com",
                    f"User {i}",
                    generate_password_hash(PASSWORD),
                ),
            )
        db.commit()
        db.close()

        response = client.get("/users", headers=_headers(client, "user1@example.com"))
        assert response.status_code == 200

        data = response.get_json()
        assert len(data) == 100  # Should be limited to 100


class TestGetUser:
    """Test GET /users/<id> endpoint."""

    def test_get_user_requires_auth(self, client):
        response = client.get("/users/1")
        assert response.status_code == 401

    def test_get_user_success(self, client):
        """Test getting a user by ID returns correct data."""
        response = client.get("/users/1", headers=_headers(client, "user1@example.com"))
        assert response.status_code == 200

        data = response.get_json()
        assert data["id"] == 1
        assert data["email"] == "user1@example.com"
        assert data["name"] == "User One"
        assert data["alias"] == "user1"
        assert "password_hash" not in data  # Should be excluded

    def test_get_user_not_found(self, client):
        """Test getting non-existent user returns 404."""
        response = client.get(
            "/users/999", headers=_headers(client, "user1@example.com")
        )
        assert response.status_code == 404

        data = response.get_json()
        assert "error" in data
        assert data["error"] == "not found"

    def test_get_own_user_includes_values_json(self, client):
        """El propio usuario sí ve sus valores personales."""
        # Add values_json to user
        db_path = client.application.config["DATABASE"]
        db = sqlite3.connect(db_path)
        db.execute(
            "UPDATE users SET values_json = ? WHERE id = ?",
            ('{"key": "value"}', 1),
        )
        db.commit()
        db.close()

        response = client.get("/users/1", headers=_headers(client, "user1@example.com"))
        assert response.status_code == 200

        data = response.get_json()
        assert "values_json" in data

    def test_get_other_user_hides_values_json(self, client):
        """Los valores personales de terceros no se exponen."""
        db_path = client.application.config["DATABASE"]
        db = sqlite3.connect(db_path)
        db.execute(
            "UPDATE users SET values_json = ? WHERE id = ?",
            ('{"key": "privado"}', 1),
        )
        db.commit()
        db.close()

        response = client.get("/users/1", headers=_headers(client, "user2@example.com"))
        assert response.status_code == 200
        assert "values_json" not in response.get_json()

    def test_admin_can_see_values_json(self, client):
        response = client.get("/users/1", headers=_headers(client, "admin@example.com"))
        assert response.status_code == 200
        assert "values_json" in response.get_json()


class TestCreateUser:
    """Test POST /users endpoint (solo admin)."""

    def test_create_user_requires_auth(self, client):
        response = client.post(
            "/users",
            data=json.dumps({"email": "x@example.com", "password": PASSWORD}),
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_create_user_forbidden_for_member(self, client):
        response = client.post(
            "/users",
            data=json.dumps({"email": "x@example.com", "password": PASSWORD}),
            content_type="application/json",
            headers=_headers(client, "user1@example.com"),
        )
        assert response.status_code == 403

    def test_create_user_success(self, client):
        """Test creating a user with valid data as admin."""
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "alias": "newuser",
            "password": PASSWORD,
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 201
        result = response.get_json()
        assert result["message"] == "user created"

        # Verify user was created
        db_path = client.application.config["DATABASE"]
        db = sqlite3.connect(db_path)
        cursor = db.execute(
            "SELECT * FROM users WHERE email = ?", ("newuser@example.com",)
        )
        user = cursor.fetchone()
        assert user is not None
        db.close()

    def test_create_user_missing_email(self, client):
        """Test creating user without email returns 400."""
        data = {"name": "New User", "password": PASSWORD}

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "email" in result["error"]

    def test_create_user_missing_password(self, client):
        """Test creating user without password returns 400."""
        data = {"email": "newuser@example.com", "name": "New User"}

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "password" in result["error"]

    def test_create_user_duplicate_email(self, client):
        """Test creating user with duplicate email returns 500."""
        data = {
            "email": "user1@example.com",  # Already exists
            "name": "Duplicate User",
            "password": PASSWORD,
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 500
        result = response.get_json()
        assert "error" in result
        assert "Failed to create user" in result["error"]

    def test_create_user_empty_json(self, client):
        """Test creating user with empty JSON returns 400."""
        response = client.post(
            "/users",
            data=json.dumps({}),
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 400

    def test_create_user_no_json(self, client):
        """Test creating user without JSON returns 400."""
        response = client.post(
            "/users",
            data="not json",
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 400

    def test_create_user_optional_fields(self, client):
        """Test creating user with optional alias field."""
        data = {
            "email": "optional@example.com",
            "name": "Optional User",
            "alias": "optional_alias",
            "password": PASSWORD,
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
            headers=_headers(client, "admin@example.com"),
        )

        assert response.status_code == 201

        # Verify alias was saved
        db_path = client.application.config["DATABASE"]
        db = sqlite3.connect(db_path)
        cursor = db.execute(
            "SELECT alias FROM users WHERE email = ?", ("optional@example.com",)
        )
        row = cursor.fetchone()
        assert row[0] == "optional_alias"
        db.close()
