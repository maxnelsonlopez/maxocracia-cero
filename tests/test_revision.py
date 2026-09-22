# -*- coding: utf-8 -*-
"""Tests de la revisión multi-modelo (F4 conceptual, Aster §4)."""

import json

from maxocontracts.concilio import revision as rev_mod
from maxocontracts.concilio.revision import revisar_candidato

ENV = {
    "NVIDIA_NIM_API_KEY": "nv-test",
    "DEEPSEEK_API_KEY": "ds-test",
    "OPENROUTER_API_KEY": "or-test",
}


def _respuesta(role, verdict="approve", changed=None):
    return json.dumps(
        {
            "verdict": verdict,
            "criticisms": ["una crítica"],
            "uncertainties": ["una incertidumbre"],
            "changed_mind": changed,
            "confidence": 0.8,
            "reasoning": "razonamiento corto",
        }
    )


def test_revision_multimodelo_diversidad_y_firma(monkeypatch):
    """Revisor A (motor 1), Revisor B (motor 2) y Disidente (motor 3)."""
    llamadas = []

    def _fake_call(engine_cfg, system, user, want_json=True):
        llamadas.append(engine_cfg.name)
        role = (
            "Dissident"
            if "Disidente" in system
            else ("Revisor A" if llamadas[-1] == "nv" else "Revisor B")
        )
        return _respuesta(role), engine_cfg, False

    monkeypatch.setattr(rev_mod, "_call_revision", _fake_call)
    revisiones = revisar_candidato(
        "propuesta", "diff: 3 files", "evidencia: 968 passed", env=ENV
    )
    assert len(revisiones) == 3
    motores = [r["engine"] for r in revisiones]
    assert len(set(motores)) == len(motores)  # diversidad real (3 motores, 3 roles)
    assert all("engine" in r and "model" in r for r in revisiones)
    assert revisiones[0]["verdict"] == "approve"


def test_revision_captura_changed_mind(monkeypatch):
    """changed_mind es la señal de aprendizaje (nunca un objetivo)."""

    def _fake_call(engine_cfg, system, user, want_json=True):
        return (
            _respuesta(
                "Dissident",
                verdict="modify",
                changed={"desde": "approve", "hacia": "modify: evidencia nueva"},
            ),
            engine_cfg,
            False,
        )

    monkeypatch.setattr(rev_mod, "_call_revision", _fake_call)
    revisiones = revisar_candidato("p", "d", "e", env=ENV)
    assert revisiones[0]["changed_mind"]["desde"] == "approve"


def test_revision_sin_consulta_registra_infra(monkeypatch):
    """Si el motor falla, el revisor queda registrado con rechazo y sin mentira."""

    def _fake_call(engine_cfg, system, user, want_json=True):
        raise rev_mod.engines.EngineError("motor caído")

    monkeypatch.setattr(rev_mod, "_call_revision", _fake_call)
    revisiones = revisar_candidato("p", "d", "e", env=ENV)
    assert len(revisiones) == 3
    assert all(r["verdict"] == "reject" for r in revisiones)
    assert all(r.get("fallback") for r in revisiones)


def test_prompt_disidente_no_se_filtra_a_los_demas():
    s_dis, _ = rev_mod._prompt_revisor("Dissident", "p", "d", "e")
    s_a, _ = rev_mod._prompt_revisor("Revisor A", "p", "d", "e")
    assert "Disidente Permanente" in s_dis
    assert "Disidente Permanente" not in s_a
