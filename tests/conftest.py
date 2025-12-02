import os
import pytest
import json
import tempfile
import sqlite3
from werkzeug.security import generate_password_hash
from app import create_app
from app.utils import init_db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp(prefix="test_db_", suffix=".db")

    # Configurar las variables de entorno para pruebas
    os.environ["SECRET_KEY"] = "test-secret-key-123"
    os.environ["FLASK_ENV"] = "testing"

    # Crear la aplicación con la ruta de la base de datos temporal
    app = create_app(db_path=db_path)

    # Configuración adicional para pruebas
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})

    # Create the database and load test data
    with app.app_context():
        init_db()

        # Add test user with valid password that meets requirements
        db = sqlite3.connect(db_path)
        test_password = "ValidPass123!"
        db.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            ("test@example.com", "Test User", generate_password_hash(test_password)),
        )
        # Add a second test user for specific tests
        db.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            ("test2@example.com", "Test User 2", generate_password_hash(test_password)),
        )
        db.commit()
        db.close()

    yield app

    # Clean up the temporary database
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email="test@example.com", password="ValidPass123!"):
        return self._client.post(
            "/auth/login", json={"email": email, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """Fixture to handle authentication in tests."""
    return AuthActions(client)


@pytest.fixture
def auth_client(client, auth):
    """A test client with authentication."""
    # Login first
    response = auth.login()
    assert response.status_code == 200
    token = response.get_json().get("access_token")

    # Set the token in the client
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client
