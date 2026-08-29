# -*- coding: utf-8 -*-
"""Tests para la síntesis de identidad: autenticación híbrida con JWT de Maxocracia."""

import os
import time
import jwt


def _generate_maxo_jwt(
    user_id=42,
    email="viajero@maxocracia.org",
    alias="viajero",
    name="Viajero Vital",
    is_admin=0,
    secret=None,
    expired=False,
):
    if secret is None:
        secret = os.environ.get("SECRET_KEY", "test-secret-key-123")
    now = int(time.time())
    payload = {
        "user_id": user_id,
        "email": email,
        "alias": alias,
        "name": name,
        "is_admin": is_admin,
        "iat": now - 100 if expired else now,
        "exp": now - 10 if expired else now + 3600,
    }
    return jwt.encode(payload, secret, algorithm="HS256")



def test_jwt_auth_bearer_header_and_jit_provisioning(client):
    """Un usuario con JWT de Maxocracia es autenticado y aprovisionado JIT."""
    token = _generate_maxo_jwt(user_id=101, email="alicia@vital.org", alias="alicia", is_admin=0)

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 200

    body = resp.get_json()
    assert body["user"]["username"] == "alicia"
    assert body["user"]["email"] == "alicia@vital.org"
    assert body["user"]["maxo_user_id"] == 101
    assert body["user"]["is_federated"] is True
    assert body["user"]["is_coordinator"] is False
    assert len(body["branches"]) == 8


def test_jwt_auth_with_x_auth_token_header(client):
    """El JWT de Maxocracia también es aceptado en la cabecera X-Auth-Token."""
    token = _generate_maxo_jwt(user_id=102, email="beto@vital.org", alias="beto")

    headers = {"X-Auth-Token": token}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["user"]["maxo_user_id"] == 102
    assert body["user"]["is_federated"] is True


def test_jwt_admin_becomes_coordinator(client):
    """Un administrador de Maxocracia es reconocido como coordinador en el OEV."""
    token = _generate_maxo_jwt(user_id=1, email="admin@vital.org", alias="director", is_admin=1)

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["user"]["is_coordinator"] is True
    assert body["user"]["maxo_user_id"] == 1


def test_jwt_links_to_existing_email_user(client):
    """Si ya existe un usuario local con el mismo email, se vincula sin duplicar."""
    # 1. Registrar usuario local clásico
    reg_resp = client.post(
        "/api/auth/register",
        json={"username": "carlos_local", "password": "mipassword123", "email": "carlos@vital.org"},
    )
    assert reg_resp.status_code == 201
    local_id = reg_resp.get_json()["user"]["id"]

    # 2. Entrar con JWT de Maxocracia que tiene el mismo email
    token = _generate_maxo_jwt(user_id=77, email="carlos@vital.org", alias="carlos_maxo")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["user"]["id"] == local_id
    assert body["user"]["maxo_user_id"] == 77
    assert body["user"]["username"] == "carlos_local"


def test_jwt_expired_returns_401(client):
    """Un JWT expirado es rechazado con 401."""
    expired_token = _generate_maxo_jwt(user_id=99, expired=True)
    headers = {"Authorization": f"Bearer {expired_token}"}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 401


def test_jwt_invalid_signature_returns_401(client):
    """Un JWT con firma inválida (secreto incorrecto) es rechazado con 401."""
    bad_token = _generate_maxo_jwt(user_id=99, secret="wrong-secret-key")
    headers = {"Authorization": f"Bearer {bad_token}"}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 401


def test_local_memory_token_and_jwt_coexist(client):
    """Los tokens locales en memoria siguen funcionando en paralelo con los JWT federados."""
    # Usuario local 1
    reg_resp = client.post(
        "/api/auth/register",
        json={"username": "local_user", "password": "pass"},
    )
    assert reg_resp.status_code == 201
    local_token = reg_resp.get_json()["token"]

    # Acceso con token local
    resp_local = client.get("/api/me", headers={"X-Auth-Token": local_token})
    assert resp_local.status_code == 200
    assert resp_local.get_json()["user"]["is_federated"] is False
    assert resp_local.get_json()["user"]["maxo_user_id"] is None

    # Usuario federado 2
    jwt_token = _generate_maxo_jwt(user_id=200, alias="federated_user")
    resp_jwt = client.get("/api/me", headers={"Authorization": f"Bearer {jwt_token}"})
    assert resp_jwt.status_code == 200
    assert resp_jwt.get_json()["user"]["is_federated"] is True
    assert resp_jwt.get_json()["user"]["maxo_user_id"] == 200


def test_jwt_without_secret_fails_closed(client, monkeypatch):
    """Sin SECRET_KEY configurada la federación NO abre con una constante pública:
    el JWT falla con 503 FEDERATION_NOT_CONFIGURED (fail-closed, no inseguro)."""
    monkeypatch.delenv("SECRET_KEY", raising=False)
    # El modo autónomo local sigue vivo sin clave.
    reg_resp = client.post(
        "/api/auth/register",
        json={"username": "autonomo", "password": "pass"},
    )
    assert reg_resp.status_code == 201
    local_token = reg_resp.get_json()["token"]
    assert client.get("/api/me", headers={"X-Auth-Token": local_token}).status_code == 200

    # El JWT federado, en cambio, se rechaza de forma explícita.
    token = _generate_maxo_jwt(user_id=999, alias="forjado")
    resp = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 503
    assert resp.get_json()["code"] == "FEDERATION_NOT_CONFIGURED"
