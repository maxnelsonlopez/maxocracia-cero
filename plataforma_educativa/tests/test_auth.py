# -*- coding: utf-8 -*-
"""Test 1 y 2: registro (email opcional), login y /api/me con token."""


def _register(client, username, password, email=None):
    payload = {"username": username, "password": password}
    if email is not None:
        payload["email"] = email
    return client.post("/api/auth/register", json=payload)


def _login(client, username, password):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_register_without_email_works(client):
    """Registrarse sin email es válido (la columna email es nullable)."""
    resp = _register(client, "ana", "secreto")
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["token"]
    assert body["user"]["username"] == "ana"
    assert body["user"]["email"] is None


def test_register_with_email_works(client):
    """Registrarse con email también es válido."""
    resp = _register(client, "luis", "secreto", email="luis@ejemplo.com")
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["user"]["email"] == "luis@ejemplo.com"


def test_register_duplicate_username_returns_409(client):
    """Un username ya usado responde 409."""
    _register(client, "ana", "secreto")
    resp = _register(client, "ana", "otra")
    assert resp.status_code == 409
    assert "error" in resp.get_json()


def test_register_missing_fields_returns_400(client):
    """Faltan username o password -> 400."""
    resp = client.post("/api/auth/register", json={"username": "solo"})
    assert resp.status_code == 400


def test_login_and_me_with_token(client):
    """Login devuelve token y /api/me lo acepta con X-Auth-Token."""
    _register(client, "ana", "secreto")
    resp = _login(client, "ana", "secreto")
    assert resp.status_code == 200
    token = resp.get_json()["token"]

    headers = {"X-Auth-Token": token}
    me = client.get("/api/me", headers=headers)
    assert me.status_code == 200
    body = me.get_json()
    assert body["user"]["username"] == "ana"
    assert len(body["branches"]) == 9


def test_me_without_token_returns_401(client):
    """Sin token, /api/me responde 401."""
    resp = client.get("/api/me")
    assert resp.status_code == 401


def test_login_bad_credentials_returns_401(client):
    """Credenciales inválidas -> 401."""
    _register(client, "ana", "secreto")
    resp = _login(client, "ana", "incorrecta")
    assert resp.status_code == 401
