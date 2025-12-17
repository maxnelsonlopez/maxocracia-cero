"""
Tests for Users API endpoints.

Tests the /users endpoints for listing, getting, and creating users.
"""

import json
import sqlite3
import tempfile

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.utils import init_db


@pytest.fixture
def client():
    """Create test client with temporary database."""
    db_fd, db_path = tempfile.mkstemp(prefix="test_users_", suffix=".db")
    import os

    os.close(db_fd)

    app = create_app(db_path=db_path)
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})

    with app.app_context():
        init_db()

        # Add test users
        db = sqlite3.connect(db_path)
        db.execute(
            "INSERT INTO users (id, email, name, alias, password_hash) VALUES (?, ?, ?, ?, ?)",
            (
                1,
                "user1@example.com",
                "User One",
                "user1",
                generate_password_hash("Password1"),
            ),
        )
        db.execute(
            "INSERT INTO users (id, email, name, alias, password_hash) VALUES (?, ?, ?, ?, ?)",
            (
                2,
                "user2@example.com",
                "User Two",
                "user2",
                generate_password_hash("Password1"),
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


class TestListUsers:
    """Test GET /users endpoint."""

    def test_list_users_success(self, client):
        """Test listing users returns all users."""
        response = client.get("/users")
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
        for i in range(3, 105):
            db.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (
                    f"user{i}@example.com",
                    f"User {i}",
                    generate_password_hash("Password1"),
                ),
            )
        db.commit()
        db.close()

        response = client.get("/users")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data) == 100  # Should be limited to 100


class TestGetUser:
    """Test GET /users/<id> endpoint."""

    def test_get_user_success(self, client):
        """Test getting a user by ID returns correct data."""
        response = client.get("/users/1")
        assert response.status_code == 200

        data = response.get_json()
        assert data["id"] == 1
        assert data["email"] == "user1@example.com"
        assert data["name"] == "User One"
        assert data["alias"] == "user1"
        assert "password_hash" not in data  # Should be excluded

    def test_get_user_not_found(self, client):
        """Test getting non-existent user returns 404."""
        response = client.get("/users/999")
        assert response.status_code == 404

        data = response.get_json()
        assert "error" in data
        assert data["error"] == "not found"

    def test_get_user_includes_values_json(self, client):
        """Test that get_user includes values_json if present."""
        # Add values_json to user
        db_path = client.application.config["DATABASE"]
        db = sqlite3.connect(db_path)
        db.execute(
            "UPDATE users SET values_json = ? WHERE id = ?",
            ('{"key": "value"}', 1),
        )
        db.commit()
        db.close()

        response = client.get("/users/1")
        assert response.status_code == 200

        data = response.get_json()
        assert "values_json" in data


class TestCreateUser:
    """Test POST /users endpoint."""

    def test_create_user_success(self, client):
        """Test creating a user with valid data."""
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "alias": "newuser",
            "password": "Password1",
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
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
        data = {
            "name": "New User",
            "password": "Password1",
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "email" in result["error"]

    def test_create_user_missing_password(self, client):
        """Test creating user without password returns 400."""
        data = {
            "email": "newuser@example.com",
            "name": "New User",
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
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
            "password": "Password1",
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
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
        )

        assert response.status_code == 400

    def test_create_user_no_json(self, client):
        """Test creating user without JSON returns 400."""
        response = client.post(
            "/users", data="not json", content_type="application/json"
        )

        assert response.status_code == 400

    def test_create_user_optional_fields(self, client):
        """Test creating user with optional alias field."""
        data = {
            "email": "optional@example.com",
            "name": "Optional User",
            "alias": "optional_alias",
            "password": "Password1",
        }

        response = client.post(
            "/users",
            data=json.dumps(data),
            content_type="application/json",
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
