# -*- coding: utf-8 -*-
"""Tests del paquete canónico para oráculos de app (hito 5, 09-10-2026).

Los oráculos de app citaban axiomas que ningún contexto les había servido
(G1 rota por omisión). El anexo C0+C1 los pone a beber del canon vivo sin
tocar sus systems (el enrutamiento por messages[0] queda intacto).
"""

from maxocontracts.concilio.canon import (
    ANEXO_CABECERA,
    con_anexo_canonico,
    paquete_para_oraculo,
)


def test_paquete_acotado_con_manifiesto():
    paq = paquete_para_oraculo()
    assert paq["caracteres"] <= 8_000
    assert isinstance(paq["degradada"], bool)  # honesto: dice si cupo todo
    assert paq["fuente"] == "canon C0+C1"
    assert "validate_invariant_gamma" in paq["texto"]  # catálogo, no corte
    assert "AxiomValidator" in paq["texto"] or "axioms.py" in paq["texto"]
    assert "corpus/registro-pre-ledger-" in paq["texto"]  # ledger con linaje


def test_anexo_tras_el_system_sin_tocarlo():
    system = {"role": "system", "content": "SYSTEM"}
    user = {"role": "user", "content": "PROPUESTA"}
    out = con_anexo_canonico([system, user])
    assert len(out) == 3
    assert out[0] == system
    assert out[1]["role"] == "user"
    assert ANEXO_CABECERA in out[1]["content"]
    assert out[2] == user


def test_opt_out_por_env_deja_los_mensajes_intactos(monkeypatch):
    monkeypatch.setenv("ORACLE_CANON_PACK", "0")
    msgs = [{"role": "system", "content": "S"}, {"role": "user", "content": "U"}]
    assert con_anexo_canonico(msgs) == msgs


def test_analyze_proposal_lleva_anexo_y_conserva_system(monkeypatch):
    from app import voting_oracle

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    visto = {}

    def fake_llm(base_url, api_key, model, messages, temperature=0.2,
                 json_mode=True, timeout=120):
        visto["messages"] = messages
        return {
            "vhv": {"vitalTime": 1, "affectedLives": 2, "finiteResources": 3,
                    "timeFactor": 1.0, "confidence": 0.5},
            "axiomReport": [],
            "oracleOpinions": [],
        }

    monkeypatch.setattr(voting_oracle, "_call_llm", fake_llm)
    monkeypatch.setattr(
        voting_oracle, "_dissident_analysis", lambda *a: None
    )
    voting_oracle.analyze_proposal("Título", "Descripción")
    msgs = visto["messages"]
    assert msgs[0]["content"] == voting_oracle.SYSTEM_PROMPT
    assert any(ANEXO_CABECERA in m["content"] for m in msgs[1:])
    assert any("validate_invariant_gamma" in m["content"] for m in msgs[1:])


def test_live_oracle_negotiate_lleva_anexo(monkeypatch):
    from maxocontracts.oracles import live_oracle as live_module

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-123")
    visto = {}

    def fake_post(url, headers=None, json=None, timeout=120):
        visto["messages"] = json["messages"]
        return _Respuesta(
            {"choices": [{"message": {"content": (
                '{"terms": [{"do": "Max da 10h", "give": "Ana da 10h de cuidado",'
                ' "owner": "Max", "vhv_hours": 10}], "summary": "ok",'
                ' "axiom_notes": "", "open_questions": []}'
            )}}]}
        )

    class _Respuesta:
        def __init__(self, payload):
            self._payload = payload
            self.status_code = 200

        def json(self):
            return self._payload

    monkeypatch.setattr(live_module.requests, "post", fake_post)
    oracle = live_module.LiveOracle()
    oracle.negotiate("Max da 10h, Ana da cuidado")
    msgs = visto["messages"]
    assert msgs[0]["content"] == live_module.SYSTEM_PROMPT
    assert any(ANEXO_CABECERA in m["content"] for m in msgs[1:])
