# -*- coding: utf-8 -*-
"""
Tests para el blueprint de Puente Educativo (edu_bridge_bp) y síntesis de identidad.

Contrato de gobernanza (29-08-2026):
- El nodo OEV reporta con su token de servicio (X-Edu-Bridge-Token); sin él o sin
  configurar, el puente cierra (fail-closed) — la escalera no se compra con un POST.
- El evento queda como evidencia T13 (SHA-256); la escalera N0->N1 sigue siendo
  asunto del primer acuerdo (Cap. 13).
"""

import os

import pytest
from app.jwt_utils import create_token

BRIDGE_TOKEN = "test-bridge-secret"


@pytest.fixture
def bridge_token(monkeypatch):
    monkeypatch.setenv("EDU_BRIDGE_SERVICE_TOKEN", BRIDGE_TOKEN)
    # Reimportar el módulo para que lea la variable (módulo ya cargado).
    from importlib import import_module

    import app.edu_bridge_bp as bridge_mod

    import_module("app.edu_bridge_bp")
    bridge_mod.EDU_BRIDGE_SERVICE_TOKEN = BRIDGE_TOKEN
    yield BRIDGE_TOKEN


@pytest.fixture
def auth_header(app, client):
    """Crea un usuario en el sistema principal y devuelve cabecera Bearer con su token."""
    with app.app_context():
        from app.utils import get_db
        db = get_db()
        cur = db.execute(
            "INSERT INTO users (email, name, alias, password_hash, trust_level) VALUES (?, ?, ?, ?, ?)",
            ("viajero@maxocracia.org", "Viajero Vital", "viajero", "hash123", 0),
        )
        db.commit()
        user_id = cur.lastrowid

    token = create_token({"user_id": user_id, "email": "viajero@maxocracia.org", "is_admin": 0})
    return {"Authorization": f"Bearer {token}"}, user_id


def _sync(client, headers, bridge_token=None, **payload):
    extra = {}
    if bridge_token:
        extra["X-Edu-Bridge-Token"] = bridge_token
    return client.post("/edu-bridge/sync-mastery", headers={**headers, **extra}, json=payload)


def test_edu_bridge_status_unauthorized_returns_401(client):
    """Acceder a /edu-bridge/status sin token responde 401."""
    resp = client.get("/edu-bridge/status")
    assert resp.status_code == 401


def test_edu_bridge_status_authorized(client, auth_header):
    """Acceder a /edu-bridge/status con token devuelve estado de identidad unificada."""
    headers, user_id = auth_header
    resp = client.get("/edu-bridge/status", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["unified_identity"] is True
    assert data["user_id"] == user_id
    assert data["email"] == "viajero@maxocracia.org"
    assert "oev_node_url" in data


def test_sync_without_bridge_token_rejected_403(client, auth_header):
    """El usuario NO puede declarar su propia maestría: sin token de servicio,
    el puente cierra (fail-closed)."""
    headers, _ = auth_header
    resp = _sync(
        client,
        headers,
        topic_slug="aritmetica_vital",
        branch_slug="matematicas",
        mentor_rounds=2,
        triada_approved=True,
    )
    assert resp.status_code == 403
    assert resp.get_json()["code"] == "BRIDGE_TOKEN_REQUIRED"


def test_sync_mastery_requires_fields(client, auth_header, bridge_token):
    """Sincronizar maestría sin topic_slug o branch_slug responde 400."""
    headers, _ = auth_header
    resp = _sync(client, headers, bridge_token, score=88)
    assert resp.status_code == 400


def test_sync_mastery_recorded_and_no_auto_promotion(client, auth_header, bridge_token):
    """El nodo OEV reporta (T13 SHA-256); el evento queda como evidencia y la
    escalera NO se toca: quien tiene la voz la camina, no la declara (Cap. 13)."""
    headers, user_id = auth_header
    payload = {
        "topic_slug": "aritmetica_vital",
        "branch_slug": "matematicas",
        "score": 88.5,
        "mentor_rounds": 2,
        "triada_approved": True,
    }
    resp = _sync(client, headers, bridge_token, **payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["synced"] is True
    assert data["trust_effect"] == "none"
    # T13 real: SHA-256 hexadecimal (no una cadena legible de conveniencia).
    assert len(data["t13_hash"]) == 64
    assert set(data["t13_hash"]) <= set("0123456789abcdef")
    assert not data["t13_hash"].startswith("t13-edu-")

    # La escalera NO promueve por autodeclaración del nodo…
    status_resp = client.get("/edu-bridge/status", headers=headers)
    assert status_resp.get_json()["trust_level"] == 0

    # …pero el evento sí quedó como evidencia (T13).
    events_resp = client.get("/edu-bridge/events", headers=headers)
    events_data = events_resp.get_json()
    assert events_data["count"] == 1
    assert events_data["events"][0]["topic_slug"] == "aritmetica_vital"
    assert events_data["events"][0]["triada_approved"] is True
    assert events_data["events"][0]["t13_hash"] == data["t13_hash"]


def test_sync_node_report_on_behalf_without_user_jwt(client, auth_header, bridge_token):
    """Sincronización automática (servicio-a-servicio): el nodo OEV reporta en
    nombre del usuario con su token de servicio, sin el JWT de esa persona."""
    _, user_id = auth_header
    resp = client.post(
        "/edu-bridge/sync-mastery",
        headers={"X-Edu-Bridge-Token": bridge_token},
        json={
            "user_id": user_id,
            "topic_slug": "cuidado_vital",
            "branch_slug": "relaciones",
            "score": 95,
            "mentor_rounds": 2,
            "triada_approved": True,
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["trust_effect"] == "none"
    assert len(data["t13_hash"]) == 64

    # El usuario ve su evidencia (con su JWT humano, consulta normal).
    headers, _ = auth_header
    events = client.get("/edu-bridge/events", headers=headers).get_json()
    assert events["count"] == 1
    assert events["events"][0]["branch_slug"] == "relaciones"


def test_sync_node_unknown_user_404(client, bridge_token):
    """El nodo reporta un user_id que no existe en Maxocracia -> 404."""
    resp = client.post(
        "/edu-bridge/sync-mastery",
        headers={"X-Edu-Bridge-Token": bridge_token},
        json={"user_id": 999999, "topic_slug": "x", "branch_slug": "y"},
    )
    assert resp.status_code == 404


def test_sync_without_any_identity_400(client, bridge_token):
    """Sin user_id reportado y sin JWT humano no hay identidad de evento."""
    resp = client.post(
        "/edu-bridge/sync-mastery",
        headers={"X-Edu-Bridge-Token": bridge_token},
        json={"topic_slug": "x", "branch_slug": "y"},
    )
    assert resp.status_code == 400
    assert resp.get_json()["code"] == "TARGET_USER_REQUIRED"
