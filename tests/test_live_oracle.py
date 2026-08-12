"""
Pruebas del Oráculo Sintético en Vivo (ROADMAP Bloque A)
========================================================
Cubren el comportamiento con mocks sin red:
- Sin DEEPSEEK_API_KEY → is_available() False y endpoint 503.
- Cliente HTTP simulado (requests.post) → borrador parseado, validado
  contra AxiomValidator y expuesto por la API.

Referencia: docs/architecture/ROADMAP_oraculo_vivo_y_escalas.md §2.4
"""

import json

import pytest

from maxocontracts.oracles.live_oracle import (
    LiveOracle,
    OracleUnavailableError,
    OracleAPIError,
    _extract_json,
)


DEMO_DRAFT = {
    "terms": [
        {
            "term_id": "trabajo-10h",
            "civil_text": "Max ofrece 10 horas de trabajo",
            "vhv": {"t": 10.0, "v": 0.0, "h": 0.0},
            "assigned_participant": "user-1",
        },
        {
            "term_id": "reciprocidad",
            "civil_text": "Ana ofrece a cambio un objeto, un servicio o sus horas",
            "vhv": {"t": 10.0, "v": 0.0, "h": 0.0},
            "assigned_participant": "user-2",
        },
    ],
    "proposed_parties": ["user-1", "user-2"],
    "reasoning": "Intercambio simétrico: 10h por 10h, respeta T17 y SDV.",
}


class FakeChatResponse:
    """Respuesta HTTP simulada del proveedor (protocolo OpenAI-compatible)."""

    status_code = 200

    def __init__(self, content: str):
        self.content = content
        self.text = content

    def json(self):
        return {"choices": [{"message": {"content": self.content}}]}


class FakeErrorResponse:
    status_code = 502
    text = "upstream error"


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """Aisla el entorno: ninguna prueba depende de un .env real."""
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_BASE_URL", raising=False)
    monkeypatch.delenv("DEEPSEEK_MODEL", raising=False)
    monkeypatch.delenv("DEEPSEEK_ORACLE_ENABLED", raising=False)
    monkeypatch.delenv("DEEPSEEK_TIMEOUT", raising=False)


@pytest.fixture
def fake_post(monkeypatch):
    """Mockea requests.post devolviendo el borrador DEMO_DRAFT."""
    import maxocontracts.oracles.live_oracle as live_module

    def _fake_post(*args, **kwargs):
        return FakeChatResponse(json.dumps(DEMO_DRAFT))

    monkeypatch.setattr(live_module.requests, "post", _fake_post)
    return _fake_post


# --- Disponibilidad ---


def test_is_available_false_without_key(monkeypatch):
    assert LiveOracle().is_available() is False


def test_is_available_true_with_key(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    assert LiveOracle().is_available() is True


def test_is_available_false_when_disabled(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    monkeypatch.setenv("DEEPSEEK_ORACLE_ENABLED", "false")
    assert LiveOracle().is_available() is False


# --- Parsing tolerante ---


def test_extract_json_from_fenced_block():
    raw = "Aquí va mi análisis.\n```json\n{\"terms\": [1, 2]}\n```\nFin."
    assert _extract_json(raw) == {"terms": [1, 2]}


def test_extract_json_plain_object():
    assert _extract_json('{"a": 1, "b": [true]}') == {"a": 1, "b": [True]}


def test_extract_json_raises_on_garbage():
    with pytest.raises(OracleAPIError):
        _extract_json("no hay json aquí")


# --- Negociación (mocks sin red) ---


def test_negotiate_raises_when_unavailable():
    oracle = LiveOracle()
    with pytest.raises(OracleUnavailableError):
        oracle.negotiate("10 horas por un servicio")


def test_negotiate_parses_draft_and_validates(monkeypatch, fake_post):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    oracle = LiveOracle()
    result = oracle.negotiate(
        "Max ofrece 10 horas y quiere que Ana dé un objeto o sus horas",
        participants=["user-1", "user-2"],
    )
    assert result.version == 1
    assert len(result.draft_terms) == 2
    assert result.draft_terms[0]["term_id"] == "trabajo-10h"
    assert result.draft_terms[0]["vhv"]["t"] == 10.0
    assert result.proposed_parties == ["user-1", "user-2"]
    assert result.axiom_check["valid"] is True
    assert result.axiom_check["violations"] == []
    assert result.suggested_contract_id.startswith("oracle-")
    assert "reciprocidad" in result.reasoning.lower() or result.reasoning


def test_negotiate_flags_t9_violation(monkeypatch):
    import maxocontracts.oracles.live_oracle as live_module

    unbalanced = json.loads(json.dumps(DEMO_DRAFT))
    unbalanced["terms"][1]["vhv"]["t"] = 1.0  # 10h vs 1h → desbalance ~90%

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    monkeypatch.setattr(
        live_module.requests,
        "post",
        lambda *a, **k: FakeChatResponse(json.dumps(unbalanced)),
    )
    result = LiveOracle().negotiate("Max da 10h, Ana da poco")
    assert result.axiom_check["valid"] is False
    codes = [v["axiom"] for v in result.axiom_check["violations"]]
    assert "T17" in codes


def test_feedback_iterates_same_session(monkeypatch):
    import maxocontracts.oracles.live_oracle as live_module

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    calls = {"n": 0}

    def _fake_post(*args, **kwargs):
        calls["n"] += 1
        draft = json.loads(json.dumps(DEMO_DRAFT))
        if calls["n"] == 2:
            draft["terms"].append({
                "term_id": "aval-luis",
                "civil_text": "Luis avala la simetría del intercambio",
                "vhv": {"t": 0.5, "v": 0.0, "h": 0.0},
                "assigned_participant": "user-3",
            })
        return FakeChatResponse(json.dumps(draft))

    monkeypatch.setattr(live_module.requests, "post", _fake_post)

    oracle = LiveOracle()
    first = oracle.negotiate("Max da 10 horas a Ana")
    second = oracle.feedback(first.session_id, "Ana sugiere que Luis avale la simetría")

    assert first.session_id == second.session_id
    assert second.version == 2
    assert len(second.draft_terms) == 3
    assert calls["n"] == 2


def test_feedback_unknown_session_raises(monkeypatch, fake_post):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    oracle = LiveOracle()
    with pytest.raises(KeyError):
        oracle.feedback("no-existe", "comentario")


def test_negotiate_http_error_raises(monkeypatch):
    import maxocontracts.oracles.live_oracle as live_module

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    monkeypatch.setattr(
        live_module.requests,
        "post",
        lambda *a, **k: FakeErrorResponse(),
    )
    with pytest.raises(OracleAPIError) as exc_info:
        LiveOracle().negotiate("prueba")
    assert "502" in str(exc_info.value)


# --- Endpoints de la API ---


def test_negotiate_endpoint_503_without_key(client, auth_client):
    res = auth_client.post("/contracts/negotiate", json={"instruction": "10h por objeto"})
    assert res.status_code == 503
    body = res.get_json()
    assert body["code"] == "ORACLE_UNAVAILABLE"


def test_negotiate_endpoint_requires_instruction(monkeypatch, client, auth_client):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    res = auth_client.post("/contracts/negotiate", json={})
    assert res.status_code == 400


def test_negotiate_endpoint_ok_with_mocked_client(monkeypatch, client, auth_client, fake_post):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    res = auth_client.post(
        "/contracts/negotiate",
        json={
            "instruction": "Max ofrece 10 horas y quiere un objeto o servicio de Ana",
            "participants": ["user-1", "user-2"],
        },
    )
    assert res.status_code == 200
    body = res.get_json()
    assert body["axiom_check"]["valid"] is True
    assert len(body["draft_terms"]) == 2
    assert body["suggested_contract_id"].startswith("oracle-")
    assert body["session_id"]


def test_negotiate_endpoint_http_error_returns_502(monkeypatch, client, auth_client):
    import maxocontracts.oracles.live_oracle as live_module

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    monkeypatch.setattr(
        live_module.requests,
        "post",
        lambda *a, **k: FakeErrorResponse(),
    )
    res = auth_client.post("/contracts/negotiate", json={"instruction": "prueba"})
    assert res.status_code == 502


def test_feedback_endpoint_unknown_session_404(monkeypatch, client, auth_client, fake_post):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    res = auth_client.post(
        "/contracts/negotiate/feedback",
        json={"session_id": "no-existe", "feedback": "cambiemos las horas"},
    )
    assert res.status_code == 404


def test_feedback_endpoint_ok(monkeypatch, client, auth_client, fake_post):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    first = auth_client.post("/contracts/negotiate", json={"instruction": "10h por servicio"})
    session_id = first.get_json()["session_id"]

    res = auth_client.post(
        "/contracts/negotiate/feedback",
        json={"session_id": session_id, "feedback": "Ana propone 5 horas"},
    )
    assert res.status_code == 200
    assert res.get_json()["version"] == 2
    assert res.get_json()["session_id"] == session_id


def test_critique_endpoint_ok(monkeypatch, client, auth_client, fake_post):
    import maxocontracts.oracles.live_oracle as live_module

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")

    # 1. Crear contrato real vía API
    created = auth_client.post(
        "/contracts/",
        json={
            "contract_id": "critique-test-1",
            "civil_description": "Préstamo de 10 Maxos",
            "participants": [{"user_id": 1}, {"user_id": 2}],
            "terms": [{
                "term_id": "t1",
                "civil_text": "Alice presta 10 Maxos a Bob",
                "vhv": {"t": 1.0, "v": 0, "h": 0},
                "assigned_participant_id": "user-1",
            }],
        },
    )
    assert created.status_code == 201

    # 2. El oráculo audita (mock): issues y recomendaciones
    audit = {
        "valid": False,
        "issues": [{"axiom": "T17", "severity": "alta", "message": "Falta contraprestación"}],
        "recommendations": ["Añadir término de reciprocidad para Bob"],
        "reasoning": "El préstamo no tiene contraprestación clara.",
    }

    def _fake_post(*args, **kwargs):
        return FakeChatResponse(json.dumps(audit))

    monkeypatch.setattr(live_module.requests, "post", _fake_post)

    res = auth_client.post("/contracts/critique-test-1/critique")
    assert res.status_code == 200
    body = res.get_json()
    assert body["contract_id"] == "critique-test-1"
    assert body["valid"] is False
    assert body["issues"][0]["axiom"] == "T17"
    assert "reciprocidad" in body["recommendations"][0]


def test_critique_endpoint_unknown_contract_404(monkeypatch, client, auth_client, fake_post):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    res = auth_client.post("/contracts/no-existe-xyz/critique")
    assert res.status_code == 404
