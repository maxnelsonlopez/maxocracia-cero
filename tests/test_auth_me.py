import pytest
from werkzeug.security import generate_password_hash


def test_auth_me_returns_profile(auth_client):
    """Test that the /auth/me endpoint returns the user's profile."""
    # Usar el cliente autenticado del fixture auth_client
    resp = auth_client.get("/auth/me")
    assert resp.status_code == 200

    data = resp.get_json()
    assert "id" in data
    assert "email" in data
    assert (
        data["email"] == "test@example.com"
    )  # El email del usuario de prueba en el fixture
