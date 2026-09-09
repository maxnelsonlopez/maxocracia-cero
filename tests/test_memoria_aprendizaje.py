# -*- coding: utf-8 -*-
"""Tests de la memoria causal y la verificación determinista (Aster, v0.2).

La conversión de autonomía en aprendizaje verificable: hipótesis →
evidencia → decisión (ratify|revoke|queue) → memoria que alimenta el
siguiente F2.
"""

from types import SimpleNamespace

import pytest

from maxocontracts.concilio import (
    VALID_DECISIONS,
    evidencia_determinista,
    leer_aprendizajes,
    leer_desacuerdos,
    metricas_aprendizaje,
    registrar_aprendizaje,
    registrar_desacuerdo,
)
from maxocontracts.concilio import RegistroAprendizajeError
from maxocontracts.concilio import canon as canon_mod
from maxocontracts.concilio import verificacion as verif_mod
from maxocontracts.concilio.memoria import FICHA, FICHA_DESACUERDOS


def _registro(workspace, decision="ratify", outcome="mejoró el flujo"):
    return registrar_aprendizaje(
        workspace,
        {
            "cycle_id": "ciclo-test",
            "candidate_id": "cand-1",
            "hypothesis": "Creemos que A mejorará B bajo condiciones C",
            "expected_signal": "suite verde y menos llamadas",
            "decision": decision,
            "outcome": outcome,
            "next_hypothesis": "probar A+B",
            "changed_mind": ["Economic cambió de opinión con la evidencia"],
        },
    )


def test_memoria_roundtrip_y_orden(tmp_path):
    ws = str(tmp_path)
    _registro(ws, outcome="primero")
    _registro(ws, decision="queue", outcome="segundo")
    registros = leer_aprendizajes(ws, n=2)
    assert len(registros) == 2
    assert registros[-1]["decision"] == "queue"
    assert registros[0]["hypothesis"].startswith("Creemos")
    # n limita
    assert len(leer_aprendizajes(ws, n=1)) == 1
    assert (tmp_path / FICHA).exists()


def test_memoria_rechaza_decision_invalida(tmp_path):
    with pytest.raises(RegistroAprendizajeError, match="decision inválida"):
        _registro(str(tmp_path), decision="quizás")


def test_memoria_rechaza_registro_incompleto(tmp_path):
    with pytest.raises(RegistroAprendizajeError, match="campo obligatorio"):
        registrar_aprendizaje(str(tmp_path), {"cycle_id": "x"})


def test_agenda_incluye_aprendizajes_previos(tmp_path):
    """El siguiente F2 ve la memoria: el bucle causal queda cerrado."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "SESION_NEXT_PROMPT.md").write_text(
        "## 4. Pendientes priorizados\n\n0. Tarea A\n", encoding="utf-8"
    )
    ws = tmp_path / "ws"
    ws.mkdir()
    _registro(str(ws), outcome="A no produjo mejora medible")
    agenda = canon_mod.read_agenda(str(repo), workspace=str(ws))
    assert "Memoria del Concilio" in agenda
    assert "A no produjo mejora medible" in agenda


def test_memoria_de_desacuerdos_anti_amnesia(tmp_path):
    """Aster §4ª dimensión: la objeción histórica se conserva y se recupera."""
    ws = str(tmp_path)
    registrar_desacuerdo(
        ws,
        {
            "cycle_id": "ciclo-1",
            "question": "¿Optimizar A o B?",
            "discarded_alternative": "Optimizar A",
            "defended_by": "Aster",
            "reason": "A no produjo mejora medible",
            "evidence": "suite 968/968 sin cambio de rendimiento",
        },
    )
    with pytest.raises(RegistroAprendizajeError):
        registrar_desacuerdo(ws, {"question": "incompleto"})
    objs = leer_desacuerdos(ws)
    assert len(objs) == 1
    assert objs[0]["discarded_alternative"] == "Optimizar A"
    assert (tmp_path / FICHA_DESACUERDOS).exists()

    # la agenda del siguiente ciclo la ve ("esto ya se intentó")
    repo = tmp_path / "repo2"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "SESION_NEXT_PROMPT.md").write_text(
        "## 4. Pendientes priorizados\n\n0. Tarea A\n", encoding="utf-8"
    )
    agenda = canon_mod.read_agenda(str(repo), workspace=ws)
    assert "Objeciones históricas" in agenda
    assert "no re-proponer" in agenda.lower()


def test_metricas_aprendizaje_son_observacion_no_meta(tmp_path):
    ws = str(tmp_path)
    _registro(ws, decision="ratify", outcome="mejoró el flujo")
    _registro(ws, decision="revoke", outcome="no funcionó")
    _registro(ws, decision="queue")
    m = metricas_aprendizaje(ws)
    assert m["total"] == 3
    assert m["por_decision"]["ratify"] == 1
    assert m["reversal_rate"] == pytest.approx(0.333, abs=0.001)
    assert m["valid_learnings_per_cycle_provisional"] == 1  # ratify + hipótesis + outcome
    assert "latencia epistemológica" in m["advertencia"]
    # señales, no objetivos: la métrica lo dice explícitamente
    assert "no objetivos" in m["advertencia"]


# --- Verificación determinista (F4) ---


def _fake_run(captured):
    def run(cmd, cwd="", timeout=0):
        captured.append((cmd, cwd))
        if cmd[0] == "git":
            out = "3 files changed, 42 insertions(+), 7 deletions(-)\n"
            return SimpleNamespace(stdout=out, returncode=0)
        out = "968 passed in 100.0s\n"
        return SimpleNamespace(stdout=out, stderr="", returncode=0)

    return run


def test_evidencia_determinista_pytest_y_diff(monkeypatch, tmp_path):
    captured = []
    monkeypatch.setattr(verif_mod, "_run", _fake_run(captured))
    ev = evidencia_determinista(str(tmp_path), base_commit="abc1234")
    assert ev["tests"] == {
        "ran": True,
        "status": "pass",
        "total": 968,
        "failed": 0,
        "duration_s": pytest.approx(0.0, abs=2),
    }
    assert ev["diff"] == {"files_changed": 3, "insertions": 42, "deletions": 7}
    # la suite se ejecuta con el python del venv del repo
    assert captured[0][0][-1] == "-q"


def test_evidencia_determinista_suite_roja(monkeypatch, tmp_path):
    def run(cmd, cwd="", timeout=0):
        if cmd[0] == "git":
            return SimpleNamespace(stdout="", returncode=0)
        return SimpleNamespace(stdout="1 failed, 5 passed", stderr="", returncode=1)

    monkeypatch.setattr(verif_mod, "_run", run)
    ev = evidencia_determinista(str(tmp_path))
    assert ev["tests"]["status"] == "fail"
    assert ev["tests"]["failed"] == 1


def test_evidencia_determinista_sobrevive_a_errores(monkeypatch, tmp_path):
    def boom(cmd, cwd="", timeout=0):
        raise OSError("venv roto")

    monkeypatch.setattr(verif_mod, "_run", boom)
    ev = evidencia_determinista(str(tmp_path))
    assert ev["tests"]["ran"] is False
    assert ev["tests"]["status"] == "fail"


def test_validador_de_decisiones_tiene_tres_estados():
    assert VALID_DECISIONS == {"ratify", "revoke", "queue"}
