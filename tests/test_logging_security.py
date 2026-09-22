# -*- coding: utf-8 -*-
"""Tests del logging JSON sanitizado y del storage URI (plan seguridad §3.4/§4).

Nunca se usan claves reales: los secretos de prueba son cadenas falsas.
"""

import json
import logging

from app.limiter import get_storage_uri
from app.logging_config import (
    REDACTED,
    JsonFormatter,
    SanitizingFilter,
    redact_text,
    sanitize_value,
    setup_json_logging,
)

FAKE_JWT = (
    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0."
    "dW1jdG9yX2Zha2Utc2lnbmF0dXJlLTEyMzQ1Njc4OTA"
)
FAKE_API_KEY = "nvapi-0123456789abcdef0123456789abcdef"

# --- Redacción de texto ---


def test_redact_text_quita_jwt():
    assert FAKE_JWT not in redact_text(f"token {FAKE_JWT} y mas")
    assert REDACTED in redact_text(f"token {FAKE_JWT}")


def test_redact_text_quita_claves_api_y_bearer():
    out = redact_text(f"Authorization: Bearer {FAKE_API_KEY}")
    assert FAKE_API_KEY not in out
    out2 = redact_text(f"clave nvapi-{FAKE_API_KEY}")
    assert FAKE_API_KEY not in out2


def test_redact_text_respeta_texto_normal():
    texto = "El VHV no se oculta (T13)."
    assert redact_text(texto) == texto


# --- Sanitización estructurada (campos sensibles) ---


def test_sanitize_value_redacta_campos_sensibles():
    data = {
        "gamma_protegido": 0.72,
        "esi": "contenido intimo",
        "t13_hash": "a1b2c3",
        "nested": {"token": "abc", "msg": "ok"},
        "lista": [{"api_key": "sk-xxx"}],
    }
    out = sanitize_value(data)
    assert out["gamma_protegido"] == REDACTED
    assert out["esi"] == REDACTED
    assert out["t13_hash"] == "a1b2c3"  # el hash T13 es evidencia, se conserva
    assert out["nested"]["token"] == REDACTED
    assert out["lista"][0]["api_key"] == REDACTED


# --- Formateador JSON ---


def _record(msg, extra=None):
    record = logging.LogRecord(
        name="app.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=msg,
        args=(),
        exc_info=None,
    )
    if extra:
        record.extra = extra
    return record


def test_json_formatter_produce_linea_json_sanitizada():
    fmt = JsonFormatter()
    record = _record(
        f"proceso con token {FAKE_JWT}",
        extra={"gamma_protegido": 0.65, "t13_hash": "hash-ok"},
    )
    line = fmt.format(record)
    parsed = json.loads(line)
    assert FAKE_JWT not in line
    assert parsed["msg"].startswith("proceso con token")
    assert parsed["gamma_protegido"] == REDACTED
    assert parsed["t13_hash"] == "hash-ok"
    assert parsed["level"] == "INFO"


def test_sanitizing_filter_redacta_args():
    filtro = SanitizingFilter()
    record = logging.LogRecord(
        name="app",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="clave %s",
        args=(FAKE_API_KEY,),
        exc_info=None,
    )
    filtro.filter(record)
    assert FAKE_API_KEY not in record.getMessage()


def test_setup_json_logging_instala_handler_con_filtro():
    handler = setup_json_logging(level=logging.DEBUG)
    assert any(isinstance(f, SanitizingFilter) for f in handler.filters)
    assert isinstance(handler.formatter, JsonFormatter)
    # limpieza: no polucionar loggers globales entre tests
    logging.getLogger("app").removeHandler(handler)


def test_create_app_con_log_json_funciona(monkeypatch):
    monkeypatch.setenv("LOG_JSON", "1")
    from app import create_app

    app = create_app()
    # el logger de la app sigue vivo (no rompe el arranque)
    assert app is not None


# --- Storage URI del limiter ---


def test_storage_uri_prioridad_ratelimit(monkeypatch):
    monkeypatch.setenv("RATELIMIT_STORAGE_URI", "redis://a/0")
    monkeypatch.setenv("REDIS_URL", "redis://b/0")
    assert get_storage_uri() == "redis://a/0"


def test_storage_uri_fallback_redis_url(monkeypatch):
    monkeypatch.delenv("RATELIMIT_STORAGE_URI", raising=False)
    monkeypatch.setenv("REDIS_URL", "redis://b/0")
    assert get_storage_uri() == "redis://b/0"


def test_storage_uri_default_memory(monkeypatch):
    monkeypatch.delenv("RATELIMIT_STORAGE_URI", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)
    assert get_storage_uri() == "memory://"


def test_create_app_sin_log_json_no_rompe(monkeypatch):
    monkeypatch.delenv("LOG_JSON", raising=False)
    from app import create_app

    assert create_app() is not None
