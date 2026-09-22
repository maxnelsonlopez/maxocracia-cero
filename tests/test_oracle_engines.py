# -*- coding: utf-8 -*-
"""Tests del registro de motores LLM multi-proveedor (Concilio).

Verifica el contrato OpenAI-compatible sin red: los ``requests.post`` se
mockean; la resolución desde el entorno se hace con dicts en memoria.
"""

from types import SimpleNamespace

import pytest

from maxocontracts.oracles.engines import (
    DEFAULT_ORDER,
    ENGINE_DEFAULTS,
    EngineConfig,
    EngineError,
    available_engines,
    call_engine,
    chain_call,
    resolve_engine,
)


def _fake_env(overrides=None):
    """Entorno mínimo con dos motores listos (nvidia + deepseek)."""
    env = {
        "NVIDIA_NIM_API_KEY": "nv-test",
        "NVIDIA_NIM_BASE_URL": "https://integrate.api.nvidia.com/v1",
        "NVIDIA_NIM_MODEL": "deepseek-ai/deepseek-v4-flash-0731",
        "DEEPSEEK_API_KEY": "ds-test",
    }
    env.update(overrides or {})
    return env


def _fake_response(text="respuesta del motor", status=200):
    """Réplica mínima de una Response de requests."""
    body = text if status == 200 else "error"

    def json():
        if status != 200:
            return {}
        return {"choices": [{"message": {"content": body}}]}

    return SimpleNamespace(status_code=status, text=body, json=json)


def test_engine_defaults_registran_los_cuatro_proveedores():
    assert set(ENGINE_DEFAULTS) == {"nvidia", "openrouter", "deepseek", "local"}
    assert "NVIDIA_NIM_API_KEY" == ENGINE_DEFAULTS["nvidia"]["api_key_env"]
    assert ENGINE_DEFAULTS["local"]["json_mode"] is False


def test_resolve_engine_desde_env():
    cfg = resolve_engine("nvidia", env=_fake_env())
    assert cfg.name == "nvidia"
    assert cfg.api_key == "nv-test"
    assert cfg.model == "deepseek-ai/deepseek-v4-flash-0731"
    assert cfg.base_url == "https://integrate.api.nvidia.com/v1"
    assert cfg.json_mode is True


def test_resolve_engine_sin_clave_devuelve_none():
    assert resolve_engine("nvidia", env={}) is None
    assert resolve_engine("openrouter", env=_fake_env()) is None


def test_resolve_engine_desconocido_devuelve_none():
    assert resolve_engine("no-existe", env=_fake_env()) is None


def test_available_engines_filtra_y_respeta_orden():
    engines = available_engines(env=_fake_env(), order=DEFAULT_ORDER)
    assert [e.name for e in engines] == [
        "nvidia",
        "deepseek",
    ]  # OpenRouter principal (15-09, sin ingresos para DeepSeek)
    engines2 = available_engines(env=_fake_env(), order=("deepseek", "nvidia", "local"))
    assert [e.name for e in engines2] == ["deepseek", "nvidia"]


def test_default_order_empieza_en_openrouter():
    """Decisión del custodio (15-09, temporal): OpenRouter principal hasta recargar DeepSeek."""
    assert DEFAULT_ORDER[0] == "openrouter"


def test_openrouter_carga_alternativas_de_modelo():
    """OpenRouter rota sus :free; el motor trae alternativas probables."""
    env = dict(_fake_env(), OPENROUTER_API_KEY="or-test")
    cfg = resolve_engine("openrouter", env=env)
    assert cfg.model.endswith(":free")
    assert len(cfg.model_alternatives) >= 2


def test_call_engine_404_free_cambia_a_alternativa(monkeypatch):
    """Retiro de un :free → la llamada se recupera con la siguiente gratuita."""
    state = {"n": 0}

    def fake_post(url, json=None, headers=None, timeout=None):
        state["n"] += 1
        if state["n"] == 1:
            return SimpleNamespace(
                status_code=404,
                text=(
                    '{"error":{"message":"This model is unavailable for free. '
                    'Use this slug instead: z-ai/glm-4.5-air"}}'
                ),
                json=lambda: {},
            )
        return _fake_response("sobrevivio con la alternativa", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    monkeypatch.setattr("maxocontracts.oracles.engines.time.sleep", lambda *a: None)
    env = dict(_fake_env(), OPENROUTER_API_KEY="or-test")
    cfg = resolve_engine("openrouter", env=env)
    text = call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=0)
    assert text == "sobrevivio con la alternativa"
    # la firma T13 posterior será verdad: el cfg quedó con el modelo que sirvió
    assert cfg.model == cfg.model_alternatives[0]


def test_call_engine_404_sin_alternativas_lanza(monkeypatch):
    monkeypatch.setattr(
        "maxocontracts.oracles.engines.requests.post",
        lambda *a, **k: _fake_response("model not found", 404),
    )
    cfg = resolve_engine("nvidia", env=_fake_env())
    cfg.model_alternatives = ()
    with pytest.raises(EngineError, match="HTTP 404"):
        call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=0)


def test_call_engine_devuelve_contenido(monkeypatch):
    calls = {}

    def fake_post(url, json=None, headers=None, timeout=None):
        calls["url"] = url
        calls["json"] = json
        return _fake_response("texto ok", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    cfg = resolve_engine("nvidia", env=_fake_env())
    text = call_engine(cfg, [{"role": "user", "content": "hola"}], want_json=True)
    assert text == "texto ok"
    assert calls["url"].endswith("/chat/completions")
    assert calls["json"]["response_format"] == {"type": "json_object"}


def test_call_engine_sin_response_format_en_motor_local(monkeypatch):
    calls = {}

    def fake_post(url, json=None, headers=None, timeout=None):
        calls["json"] = json
        return _fake_response("ok", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    cfg = resolve_engine("local", env=_fake_env({"LOCAL_ORACLE_API_KEY": "x"}))
    call_engine(cfg, [{"role": "user", "content": "hola"}], want_json=True)
    assert "response_format" not in calls["json"]


def test_call_engine_http_error_lanza_engineerror(monkeypatch):
    monkeypatch.setattr(
        "maxocontracts.oracles.engines.requests.post",
        lambda *a, **k: _fake_response("", 429),
    )
    cfg = resolve_engine("nvidia", env=_fake_env())
    # El 429 es reintentable: al agotar los reintentos (monkeypatch del sleep
    # a no-op) debe lanzar EngineError.
    monkeypatch.setattr("maxocontracts.oracles.engines.time.sleep", lambda *a: None)
    with pytest.raises(EngineError, match="HTTP 429"):
        call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=2)


def test_call_engine_reintenta_529_y_respondepor_la_segunda(monkeypatch):
    """El 529 observado en NVIDIA (sobrecarga transitoria) se recupera."""
    state = {"n": 0}

    def fake_post(url, json=None, headers=None, timeout=None):
        state["n"] += 1
        if state["n"] == 1:
            return _fake_response("", 529)
        return _fake_response("sobrevivi", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    monkeypatch.setattr("maxocontracts.oracles.engines.time.sleep", lambda *a: None)
    cfg = resolve_engine("nvidia", env=_fake_env())
    text = call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=2)
    assert text == "sobrevivi"
    assert state["n"] == 2


def test_call_engine_respuesta_ilegible_lanza_engineerror(monkeypatch):
    import requests as _requests

    def connection_down(*a, **k):
        raise _requests.exceptions.ConnectionError("red caida")

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", connection_down)
    cfg = resolve_engine("nvidia", env=_fake_env())
    with pytest.raises(EngineError, match="no se pudo contactar"):
        call_engine(cfg, [{"role": "user", "content": "hola"}])


def test_chain_call_falls_back_al_segundo_motor_y_firma_el_que_uso(monkeypatch):
    """El primero falla (cuota/red) y la cadena responde con el segundo.

    Con OpenRouter principal (15-09): si el primero cae, la firma T13 es la
    del motor que realmente respondió.
    """
    attempts = []

    def fake_post(url, json=None, headers=None, timeout=None):
        attempts.append(json["model"])
        if json["model"] == "deepseek-ai/deepseek-v4-flash-0731":
            return _fake_response("", 503)  # nvidia (primero disponible) cae
        return _fake_response("texto del deepseek", 200)  # deepseek responde

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    monkeypatch.setattr("maxocontracts.oracles.engines.time.sleep", lambda *a: None)
    env = _fake_env()
    text, cfg = chain_call("sistema", "usuario", env=env)
    assert text == "texto del deepseek"
    assert cfg.name == "deepseek"
    assert cfg.model == "deepseek-chat"
    # nvidia intentó 3 veces (2 reintentos del 503) y la cadena pasó a deepseek
    assert attempts[:3] == ["deepseek-ai/deepseek-v4-flash-0731"] * 3
    assert attempts[3] == "deepseek-chat"


def test_chain_call_sin_motores_lanza_error():
    with pytest.raises(EngineError, match="Ningún motor"):
        chain_call("s", "u", env={})


def test_chain_call_todos_fallan_lanza_error_agregado(monkeypatch):
    monkeypatch.setattr(
        "maxocontracts.oracles.engines.requests.post",
        lambda *a, **k: _fake_response("", 500),
    )
    env = _fake_env()
    with pytest.raises(EngineError, match="Todos los motores fallaron"):
        chain_call("s", "u", env=env)


def test_engine_config_endpoint_sin_doble_barra():
    cfg = EngineConfig(
        name="nvidia",
        api_key="k",
        base_url="https://x.example/v1/",
        model="m",
    )
    assert cfg.endpoint() == "https://x.example/v1/chat/completions"


def test_openrouter_default_es_modelo_vivo_sept2026():
    """La lista muerta de 09-09 (glm-4.5-air, r1-0528, qwen3.6-plus) ya no es default."""
    muertos = {
        "z-ai/glm-4.5-air:free",
        "deepseek/deepseek-r1-0528:free",
        "qwen/qwen3.6-plus:free",
    }
    default = ENGINE_DEFAULTS["openrouter"]["default_model"]
    assert default not in muertos
    alternativas = set(ENGINE_DEFAULTS["openrouter"]["model_alternatives"])
    assert not (alternativas & muertos)
    assert (
        "nvidia/nemotron-3-super-120b-a12b:free" in alternativas
    )  # verificado vivo el 13-09


def test_call_engine_429_rota_a_siguiente_free(monkeypatch):
    """429 persistente en el modelo principal → rota al siguiente :free.

    Cada 429 fallido consume cuota diaria: insistir en el mismo modelo caído
    quema el presupuesto free (50/día) sin producir.
    """
    state = {"n": 0}

    def fake_post(url, json=None, headers=None, timeout=None):
        state["n"] += 1
        if state["n"] <= 2:
            return SimpleNamespace(
                status_code=429, text="Rate limit exceeded", json=lambda: {}
            )
        return _fake_response("sobrevivio rotando", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    monkeypatch.setattr("maxocontracts.oracles.engines.time.sleep", lambda *a: None)
    env = dict(_fake_env(), OPENROUTER_API_KEY="or-test")
    cfg = resolve_engine("openrouter", env=env)
    primero = cfg.model
    text = call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=1)
    assert text == "sobrevivio rotando"
    assert cfg.model != primero  # rotó: la firma T13 dirá la verdad


def test_call_engine_429_sin_alternativas_lanza(monkeypatch):
    """Sin alternativas (nvidia/deepseek) el 429 persistente sigue lanzando."""
    monkeypatch.setattr(
        "maxocontracts.oracles.engines.requests.post",
        lambda *a, **k: SimpleNamespace(
            status_code=429, text="Rate limit", json=lambda: {}
        ),
    )
    monkeypatch.setattr("maxocontracts.oracles.engines.time.sleep", lambda *a: None)
    cfg = resolve_engine("nvidia", env=_fake_env())
    with pytest.raises(EngineError, match="HTTP 429"):
        call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=1)


def test_retry_after_se_honra(monkeypatch):
    """El 429 con Retry-After duerme lo que pide el proveedor (cap 60s)."""
    dormido = []

    def fake_post(url, json=None, headers=None, timeout=None):
        if len(dormido) == 0:
            return SimpleNamespace(
                status_code=429,
                text="slow down",
                headers={"Retry-After": "7"},
                json=lambda: {},
            )
        return _fake_response("ok tras espera", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    monkeypatch.setattr(
        "maxocontracts.oracles.engines.time.sleep", lambda s: dormido.append(s)
    )
    cfg = resolve_engine("nvidia", env=_fake_env())
    assert (
        call_engine(cfg, [{"role": "user", "content": "hola"}], max_retries=2)
        == "ok tras espera"
    )
    assert any(abs(s - 7.0) < 0.01 for s in dormido)


def test_openrouter_envia_referer_y_titulo(monkeypatch):
    """OpenRouter recomienda HTTP-Referer + X-Title (evita throttle/403)."""
    calls = {}

    def fake_post(url, json=None, headers=None, timeout=None):
        calls["headers"] = headers
        return _fake_response("ok", 200)

    monkeypatch.setattr("maxocontracts.oracles.engines.requests.post", fake_post)
    env = dict(_fake_env(), OPENROUTER_API_KEY="or-test")
    cfg = resolve_engine("openrouter", env=env)
    call_engine(cfg, [{"role": "user", "content": "hola"}])
    assert "HTTP-Referer" in calls["headers"]
    assert "X-Title" in calls["headers"]
