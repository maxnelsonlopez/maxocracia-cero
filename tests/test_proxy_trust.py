"""ProxyFix condicionado a TRUST_PROXY=1 (parche de seguridad).

Sin confiar en el proxy, el rate limiting ve la IP de cloudflared (127.0.0.1)
para todo el mundo y los límites se vuelven un cuello de botella global.
Con TRUST_PROXY=1 se confía en exactamente un salto (X-Forwarded-For), como
corresponde al túnel de Cloudflare. Si el puerto queda expuesto directo,
dejarlo apagado para que no se pueda falsificar la IP.
"""

from flask import request

from app import create_app


def _make_app(tmp_path, monkeypatch, trust):
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-maxocracia-0123456789abcdef")
    monkeypatch.setenv("FLASK_ENV", "testing")
    if trust:
        monkeypatch.setenv("TRUST_PROXY", "1")
    else:
        monkeypatch.delenv("TRUST_PROXY", raising=False)

    app = create_app(db_path=str(tmp_path / f"proxy_{trust}.db"))
    app.config["TESTING"] = True

    seen = {}

    @app.before_request
    def _capture_remote_addr():
        seen["remote_addr"] = request.remote_addr

    return app, seen


def test_xff_ignored_without_trust_proxy(tmp_path, monkeypatch):
    app, seen = _make_app(tmp_path, monkeypatch, trust=False)
    client = app.test_client()

    client.get("/favicon.ico", environ_base={"HTTP_X_FORWARDED_FOR": "203.0.113.9"})

    assert seen["remote_addr"] == "127.0.0.1"


def test_xff_used_with_trust_proxy(tmp_path, monkeypatch):
    app, seen = _make_app(tmp_path, monkeypatch, trust=True)
    client = app.test_client()

    client.get("/favicon.ico", environ_base={"HTTP_X_FORWARDED_FOR": "203.0.113.9"})

    assert seen["remote_addr"] == "203.0.113.9"


def test_limiter_key_prefers_cf_connecting_ip(tmp_path, monkeypatch):
    from app.limiter import get_client_address

    app, _seen = _make_app(tmp_path, monkeypatch, trust=True)
    with app.test_request_context(
        "/",
        headers={
            "CF-Connecting-IP": "198.51.100.7",
            "X-Forwarded-For": "203.0.113.9",
        },
    ):
        assert get_client_address() == "198.51.100.7"


def test_limiter_key_ignores_cf_header_without_trust(tmp_path, monkeypatch):
    from app.limiter import get_client_address

    app, _seen = _make_app(tmp_path, monkeypatch, trust=False)
    with app.test_request_context("/", headers={"CF-Connecting-IP": "198.51.100.7"}):
        assert get_client_address() != "198.51.100.7"
