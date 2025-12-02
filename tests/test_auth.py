import json



def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "ValidPass123!",
            "name": "New User",
        },
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_user(client, auth):
    """Test user login"""
    # Register a test user first
    client.post(
        "/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "ValidPass123!",
            "name": "Login Test User",
        },
    )

    # Test login
    response = auth.login("login_test@example.com", "ValidPass123!")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token(client, auth):
    """Test token refresh"""
    # Login first
    login_response = auth.login("test@example.com", "ValidPass123!")
    refresh_token = json.loads(login_response.data)["refresh_token"]

    # Test refresh
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["refresh_token"] != refresh_token  # Should be a new refresh token


def test_protected_route(client, auth):
    """Test accessing a protected route with valid token"""
    # Login first
    login_response = auth.login("test@example.com", "ValidPass123!")
    access_token = json.loads(login_response.data)["access_token"]

    # Access protected route
    response = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "email" in data
    assert data["email"] == "test@example.com"
