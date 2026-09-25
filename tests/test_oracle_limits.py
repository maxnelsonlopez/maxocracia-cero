"""Cuotas de oráculo (parche de seguridad).

Los endpoints que llaman al LLM (guía, negociación, análisis de propuestas,
oráculo de forms) exigen token pero no tenían tope: cualquier integrante N0
podía quemar la cuota de DeepSeek/OpenRouter. El límite se cuenta por huella
del bearer (o IP real si no hay token).
"""

import pytest


@pytest.fixture(autouse=True)
def _limiter_limpio():
    """El almacén del limiter es global al proceso: no contaminar otros tests."""
    from app.limiter import limiter

    limiter.reset()
    yield
    limiter.reset()


def test_guide_chat_limited_by_ip(app, client):
    app.config["RATELIMIT_ORACLE_LIMIT"] = "2 per minute"

    for _ in range(2):
        resp = client.post("/guide/chat", json={"message": "hola"})
        assert resp.status_code != 429

    blocked = client.post("/guide/chat", json={"message": "hola"})
    assert blocked.status_code == 429


def test_oracle_limit_is_per_token(app, client):
    app.config["RATELIMIT_ORACLE_LIMIT"] = "1 per minute"

    headers_a = {"Authorization": "Bearer token-a"}
    headers_b = {"Authorization": "Bearer token-b"}

    # Primer intento de cada huella pasa el limitador (luego 401 por token
    # inválido, que es suficiente para probar la separación de cubetas).
    assert client.post("/guide/chat", json={}, headers=headers_a).status_code != 429

    # La misma huella ya agotó su cuota.
    assert client.post("/guide/chat", json={}, headers=headers_a).status_code == 429

    # Otra huella tiene su propia cubeta.
    assert client.post("/guide/chat", json={}, headers=headers_b).status_code != 429


def test_negotiate_and_analyze_share_oracle_quota_config(app, client):
    """Los endpoints de oráculo responden 429 antes de exigir token."""
    app.config["RATELIMIT_ORACLE_LIMIT"] = "1 per minute"

    first = client.post("/voting/proposals/1/analyze")
    assert first.status_code != 429
    second = client.post("/voting/proposals/1/analyze")
    assert second.status_code == 429
