# -*- coding: utf-8 -*-
"""Endurecimiento de la Plataforma Educativa (parche de seguridad).

Cubre:
- Cabeceras de seguridad y CSP sin scripts inline.
- HSTS solo cuando el proxy confirma HTTPS.
- Rate limit de login/registro (ventana por IP y por usuario).
"""


def test_security_headers_present(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"

    csp = resp.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self'" in csp
    assert "'unsafe-inline'" not in csp
    assert "frame-ancestors 'none'" in csp


def test_hsts_only_with_https_proxy_o_cloudflare(client):
    """HSTS con proxy TLS o con petición venida del borde de Cloudflare
    (CF-Connecting-IP solo lo inyecta el túnel)."""
    resp = client.get("/")
    assert "Strict-Transport-Security" not in resp.headers

    resp = client.get("/", headers={"X-Forwarded-Proto": "https"})
    assert "Strict-Transport-Security" in resp.headers

    resp = client.get("/", headers={"CF-Connecting-IP": "203.0.113.5"})
    assert "Strict-Transport-Security" in resp.headers


def test_token_local_expira(client, monkeypatch):
    """El token local ya no vive para siempre: TTL configurable."""
    monkeypatch.setenv("PLATAFORMA_EDUCATIVA_TOKEN_TTL", "0")
    resp = client.post("/api/auth/register", json={"username": "ttl", "password": "x"})
    assert resp.status_code == 201
    token = resp.get_json()["token"]

    me = client.get("/api/me", headers={"X-Auth-Token": token})
    assert me.status_code == 401


def test_login_rate_limited_by_ip(client, app):
    app.config["AUTH_RATE_LIMIT_ATTEMPTS"] = 3
    app.config["AUTH_RATE_LIMIT_WINDOW"] = 60

    for _ in range(3):
        resp = client.post(
            "/api/auth/login", json={"username": "nadie", "password": "x"}
        )
        assert resp.status_code == 401

    blocked = client.post(
        "/api/auth/login", json={"username": "nadie", "password": "x"}
    )
    assert blocked.status_code == 429
    assert "Retry-After" in blocked.headers


def test_login_rate_limited_by_username_across_ips(client, app):
    app.config["AUTH_RATE_LIMIT_ATTEMPTS"] = 2
    app.config["AUTH_RATE_LIMIT_WINDOW"] = 60

    first = client.post(
        "/api/auth/login",
        json={"username": "ana", "password": "x"},
        headers={"CF-Connecting-IP": "203.0.113.1"},
    )
    assert first.status_code == 401

    second = client.post(
        "/api/auth/login",
        json={"username": "ana", "password": "x"},
        headers={"CF-Connecting-IP": "203.0.113.2"},
    )
    assert second.status_code == 401

    third = client.post(
        "/api/auth/login",
        json={"username": "ana", "password": "x"},
        headers={"CF-Connecting-IP": "203.0.113.3"},
    )
    assert third.status_code == 429


def test_register_rate_limited(client, app):
    app.config["AUTH_RATE_LIMIT_ATTEMPTS"] = 2
    app.config["AUTH_RATE_LIMIT_WINDOW"] = 60

    assert (
        client.post(
            "/api/auth/register", json={"username": "n1", "password": "x"}
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/auth/register", json={"username": "n2", "password": "x"}
        ).status_code
        == 201
    )
    blocked = client.post(
        "/api/auth/register", json={"username": "n3", "password": "x"}
    )
    assert blocked.status_code == 429
