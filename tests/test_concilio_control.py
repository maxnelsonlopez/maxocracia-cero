# -*- coding: utf-8 -*-
"""Tests del control remoto del Concilio (pausar/reanudar/mensajes + resumen)."""

import json
from pathlib import Path

import pytest

from maxocontracts.concilio import ACTIVE, PAUSED, Control
from maxocontracts.concilio import cycle as cycle_mod
from maxocontracts.concilio.control import STOPPED
from maxocontracts.concilio.cycle import ORACLE_ROLES, run_cycle


def _make_env():
    return {
        "NVIDIA_NIM_API_KEY": "nv-test",
        "DEEPSEEK_API_KEY": "ds-test",
        "OPENROUTER_API_KEY": "or-test",
    }


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    (root / "docs" / "architecture").mkdir(parents=True)
    (root / "docs" / "SESION_NEXT_PROMPT.md").write_text(
        "# SESION\n## 4. Pendientes priorizados\n\n0. Tarea A\n\n## 5. Historia\n",
        encoding="utf-8",
    )
    (root / "docs" / "architecture" / "administracion_humano_sintetica.md").write_text(
        "INV1 gamma >= 1.\n", encoding="utf-8"
    )
    return str(root)


@pytest.fixture
def fake_engine(monkeypatch):
    def install(seen=None):
        seen = seen if seen is not None else []

        def _fake_call(engine_cfg, system, user, want_json=True, max_tokens=2000, **kwargs):
            seen.append((system, user))
            role = next((r for r in ORACLE_ROLES if r in system), "Economic")
            if "CANON (léelo" in user:
                return (
                    json.dumps(
                        {"firma": {"summary": role, "axiom_quotes": ["INV1"],
                                   "critical_question": "?", "confidence": 0.9}}
                    ),
                    engine_cfg,
                    False,
                )
            return (
                json.dumps(
                    {
                        "axioms": {"ok": True, "reasoning": "ok"},
                        "proposals": [
                            {"title": f"Tarea {role}", "source": "agenda §0", "why": "w",
                             "risks": "r", "tests": "t", "axioms": ["INV1"],
                             "vote": "approve", "confidence": 0.8}
                        ],
                        "veto": None,
                    }
                ),
                engine_cfg,
                False,
            )

        monkeypatch.setattr(cycle_mod, "_call", _fake_call)
        return seen

    return install


# --- Control básico ---


def test_control_default_activo_y_nonce(tmp_path):
    control = Control(str(tmp_path))
    assert control.estado() == ACTIVE
    data = control.pausar()
    assert data["estado"] == PAUSED and data["nonce"] == 1
    data2 = control.reanudar()
    assert data2["estado"] == ACTIVE and data2["nonce"] == 2


def test_control_mensaje_cola_y_limite(tmp_path):
    control = Control(str(tmp_path))
    for i in range(25):
        control.mensaje(f"directiva {i}")
    inst = control.instrucciones()
    assert len(inst) == 20  # cola acotada
    assert inst[-1] == "directiva 24"


# --- Ciclo obedece el control ---


def test_ciclo_pausado_no_llama_a_motores(repo, tmp_path, monkeypatch):
    ws = str(tmp_path / "ws")
    Control(ws).pausar()

    def boom(*a, **k):
        raise AssertionError("un ciclo pausado no debe llamar motores")

    monkeypatch.setattr(cycle_mod, "_call", boom)
    manifest = run_cycle(repo, workspace=ws, env=_make_env())
    assert manifest["pausado"] is True
    assert manifest["estado"] == PAUSED
    # el lock se liberó: se puede reanudar y correr
    Control(ws).reanudar()

    def _mock_call(engine_cfg, system, user, want_json=True, max_tokens=2000, **kwargs):
        cfg = type("C", (), {"name": "nv", "model": "m"})()
        if "CANON (léelo" in user:
            return (
                json.dumps({"firma": {"summary": "s", "axiom_quotes": [],
                                      "critical_question": "", "confidence": 0.5}}),
                cfg,
                False,
            )
        return (
            json.dumps({"axioms": {"ok": True, "reasoning": "ok"}, "proposals": [
                {"title": "p", "source": "s", "why": "w", "risks": "r", "tests": "t",
                 "axioms": ["INV1"], "vote": "approve", "confidence": 0.8}], "veto": None}),
            cfg,
            False,
        )

    monkeypatch.setattr(cycle_mod, "_call", _mock_call)
    manifest2 = run_cycle(repo, workspace=ws, env=_make_env(), max_oracles=3)
    assert manifest2.get("pausado") is not True


def test_mensaje_llega_a_oraculos_y_resumen_se_escribe(repo, tmp_path, fake_engine):
    seen = fake_engine()
    ws = str(tmp_path / "ws")
    Control(ws).mensaje("Prioriza lo que amplíe la plaza hablable (T13).")
    manifest = run_cycle(repo, workspace=ws, env=_make_env(), max_oracles=3)
    # la directiva llegó al prompt de F2 (no al de F1)
    f2_users = [u for s, u in seen if "DIRECTIVAS DEL CUSTODIO" in u]
    assert f2_users and "plaza hablable" in f2_users[0]
    # resumen.md existe y menciona motores y oráculos
    resumen = Path(manifest["artefactos"]["resumen"])
    texto = resumen.read_text(encoding="utf-8")
    assert "Economic" in texto and "nv-test" not in texto
    assert "Directivas del custodio: 1" in texto


def test_control_detener_y_reanudar_estados(tmp_path):
    control = Control(str(tmp_path))
    assert control.estado() == ACTIVE
    control.detener()
    assert control.estado() == STOPPED
    control.reanudar()
    assert control.estado() == ACTIVE
