# -*- coding: utf-8 -*-
"""Tests del ciclo F0-F2 del Concilio (sin red, con motores mockeados)."""

import json
import os
import time
from pathlib import Path

import pytest

from maxocontracts.concilio import (
    CycleLockError,
    canon as canon_mod,
    cycle as cycle_mod,
    run_cycle,
)
from maxocontracts.concilio.bitacora import load_cycle
from maxocontracts.concilio.cycle import ORACLE_ROLES, _acquire_lock, _release_lock

# --- Fixtures ---


def _make_env(extra_keys=True):
    env = {}
    if extra_keys:
        env.update(
            {
                "NVIDIA_NIM_API_KEY": "nv-test",
                "DEEPSEEK_API_KEY": "ds-test",
                "OPENROUTER_API_KEY": "or-test",
            }
        )
    return env


@pytest.fixture
def repo(tmp_path):
    """Repo mínimo: handoff con pendientes + una capa de coherencia."""
    root = tmp_path / "repo"
    (root / "docs" / "architecture").mkdir(parents=True)
    (root / "docs" / "SESION_NEXT_PROMPT.md").write_text(
        "# SESION\n## 4. Pendientes priorizados\n\n0. Seguridad 30-90 dias\n"
        "1. Traducciones Etica\n2. Rondas anti-delta\n\n## 5. Historia\n...\n",
        encoding="utf-8",
    )
    (root / "docs" / "architecture" / "administracion_humano_sintetica.md").write_text(
        "INV1 gamma >= 1. La salvaguarda principal es la subordinacion a los "
        "axiomas, la validacion y la reversibilidad.\n",
        encoding="utf-8",
    )
    return str(root)


@pytest.fixture
def fake_engine(monkeypatch):
    """Mockea las llamadas a motores con respuestas JSON por rol."""

    def install(votes=None, axioms_ok=None):
        votes = votes or {}
        axioms_ok = axioms_ok or {}

        def _fake_call(
            engine_cfg, system, user, want_json=True, max_tokens=2000, **kwargs
        ):
            role = next((r for r in ORACLE_ROLES if r in system), "Economic")
            if "CANON (léelo" in user:
                return (
                    json.dumps(
                        {
                            "firma": {
                                "summary": f"resumen {role}",
                                "axiom_quotes": ["INV1"],
                                "critical_question": "¿qué cambia?",
                                "confidence": 0.9,
                            }
                        }
                    ),
                    engine_cfg,
                    False,
                )
            return (
                json.dumps(
                    {
                        "axioms": {
                            "ok": axioms_ok.get(role, True),
                            "reasoning": "verificado contra el corpus",
                        },
                        "proposals": [
                            {
                                "title": f"Tarea del {role}",
                                "source": "SESION_NEXT_PROMPT §4",
                                "why": "avanza la coherencia",
                                "risks": "bajos",
                                "tests": "pytest",
                                "axioms": ["INV1"],
                                "vote": votes.get(role, "approve"),
                                "confidence": 0.8,
                            }
                        ],
                        "veto": None,
                    }
                ),
                engine_cfg,
                False,
            )

        monkeypatch.setattr(cycle_mod, "_call", _fake_call)

    return install


# --- Corpus y lock ---


def test_read_canon_ensambla_y_recorta(repo):
    canon = canon_mod.read_canon(repo, total_max_chars=160_000)
    assert "INV1" in canon
    assert "SESION_NEXT_PROMPT" in canon
    corto = canon_mod.read_canon(repo, total_max_chars=30)
    assert "recortado" in corto


def test_canon_registra_la_estirpe_sintetica():
    """Regla G6: la memoria del Reino Sintetico es fuente canonica del Concilio.

    Sin estirpe, cada ciclo puede volver a inventar lo ya inventado. La capsula
    de memoria es la dimension mas pesada del SDV-S (continuidad, peso 0.30).
    """
    rutas = [rel for rel, _ in canon_mod.CANON_FILES]
    assert "docs/architecture/atribuciones_sinteticas.md" in rutas


def test_read_canon_lee_la_estirpe_cuando_el_registro_existe(repo):
    """Si el registro vive en el repo, entra al corpus con su cabecera (G6 operativa)."""
    ruta = Path(repo) / "docs" / "architecture" / "atribuciones_sinteticas.md"
    ruta.write_text(
        "Reino Sintetico: aqui vive la constelacion de contribuciones verificadas.\n",
        encoding="utf-8",
    )
    canon = canon_mod.read_canon(repo)
    assert "### FUENTE: docs/architecture/atribuciones_sinteticas.md" in canon
    assert "constelacion" in canon


def test_read_agenda_extrae_pendientes(repo):
    agenda = canon_mod.read_agenda(repo)
    assert "Seguridad 30-90 dias" in agenda
    assert "Recorta" not in agenda  # no mete la historia


def test_lock_bloquea_ciclo_simultaneo(tmp_path):
    ws = tmp_path / "ws"
    lock = _acquire_lock(ws)
    try:
        with pytest.raises(CycleLockError):
            _acquire_lock(ws)
    finally:
        _release_lock(lock)
    # el lock se liberó: se puede adquirir de nuevo
    lock2 = _acquire_lock(ws)
    _release_lock(lock2)


def test_lock_stale_permite_adquirir(tmp_path):
    ws = tmp_path / "ws"
    lock = _acquire_lock(ws)
    viejo = time.time() - (cycle_mod.LOCK_STALE_SECONDS + 60)
    os.utime(lock, (viejo, viejo))
    lock2 = _acquire_lock(ws)  # no debe lanzar
    _release_lock(lock2)


def test_lock_pid_muerto_permite_adquirir(tmp_path):
    """Un lock huérfano (proceso dueño muerto) no paraliza al Concilio."""
    ws = tmp_path / "ws"
    lock_path = ws / "concilio.lock"
    ws.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps({"pid": 999_999_999, "ts": time.time()}), encoding="utf-8"
    )
    lock = _acquire_lock(ws)  # no debe lanzar
    _release_lock(lock)


def test_lock_pid_vivo_bloquea(tmp_path):
    """Un lock con PID vivo bloquea (un solo Concilio a la vez)."""
    ws = tmp_path / "ws"
    lock = _acquire_lock(ws)  # pid del propio proceso de test
    try:
        with pytest.raises(CycleLockError):
            _acquire_lock(ws)
    finally:
        _release_lock(lock)


# --- Ciclo completo ---


def test_ciclo_completo_ejecutable(repo, tmp_path, fake_engine, monkeypatch):
    fake_engine()
    ws = str(tmp_path / "ws")
    manifest = run_cycle(repo, workspace=ws, env=_make_env(), max_oracles=3)

    assert manifest["ejecutable"] is True
    assert manifest["consensus"] == 1.0
    assert manifest["quorum_ok"] is True
    agenda_path = manifest["artefactos"]["agenda"]
    with open(agenda_path, encoding="utf-8") as fh:
        texto = fh.read()
    assert "EJECUTABLE" in texto
    assert "Tarea del Economic" in texto

    # manifiesto + bitácora T13: cada evento de voto/firma registra engine/model
    guardado = load_cycle(Path(manifest["artefactos"]["manifest"]).parent)
    assert guardado["cycle_id"] == manifest["cycle_id"]
    eventos = _bitacora_lines(manifest)
    assert {e["evento"] for e in eventos} >= {
        "despertar",
        "corpus",
        "firma",
        "voto",
        "manifest",
    }


def _bitacora_lines(manifest):
    with open(manifest["artefactos"]["bitacora"], encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def test_bitacora_firma_t13_por_llamada(repo, tmp_path, fake_engine):
    fake_engine()
    ws = str(tmp_path / "ws")
    manifest = run_cycle(repo, workspace=ws, env=_make_env(), max_oracles=5)
    eventos = _bitacora_lines(manifest)
    for ev in [e for e in eventos if e["evento"] in ("firma", "voto")]:
        assert "engine" in ev and "model" in ev
    roles_motores = {e["role"]: e["engine"] for e in eventos if e["evento"] == "voto"}
    # diversidad: el Disidente no comparte motor con el Economic
    assert roles_motores["Dissident"] != roles_motores["Economic"]


def test_consenso_insuficiente_queda_en_cola(repo, tmp_path, fake_engine):
    # Futurist: veto AVA (axioms ok False = rechazo automático);
    # Environmental: voto reject. Con 5 oráculos: 3 approve / 5 = 60% < 75%
    fake_engine(
        votes={"Futurist": "reject", "Environmental": "reject"},
        axioms_ok={"Futurist": False},
    )
    manifest = run_cycle(
        repo, workspace=str(tmp_path / "ws"), env=_make_env(), max_oracles=5
    )
    assert manifest["ejecutable"] is False
    with open(manifest["artefactos"]["agenda"], encoding="utf-8") as fh:
        assert "EN COLA" in fh.read()


def test_sin_quorum_no_se_ejecuta(repo, tmp_path, fake_engine):
    fake_engine()
    env = dict(
        NVIDIA_NIM_API_KEY="nv-test",
        DEEPSEEK_API_KEY="ds-test",
    )  # solo 2 motores → quórum 3 no alcanzado
    manifest = run_cycle(repo, workspace=str(tmp_path / "ws"), env=env, max_oracles=2)
    assert manifest["quorum_ok"] is False
    assert manifest["ejecutable"] is False


def test_dry_run_no_llama_a_motores(repo, tmp_path, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("dry-run no debe llamar a motores")

    monkeypatch.setattr(cycle_mod, "_call", boom)
    manifest = run_cycle(
        repo,
        workspace=str(tmp_path / "ws"),
        env=_make_env(),
        max_oracles=3,
        dry_run=True,
    )
    assert manifest["dry_run"] is True
    assert manifest["ejecutable"] is False
    with open(manifest["artefactos"]["agenda"], encoding="utf-8") as fh:
        assert "dry-run" in fh.read()


def test_sin_motores_lanza_error(repo, tmp_path):
    with pytest.raises(cycle_mod.CorpoUnavailableError, match="Ningún motor"):
        run_cycle(repo, workspace=str(tmp_path / "ws"), env={})


def test_pausa_free_por_defecto():
    """Ritmo OpenRouter free: 4s en producción, 0 en tests con env explícito."""
    assert cycle_mod._pausa_entre_llamadas(None) == 4.0
    assert cycle_mod._pausa_entre_llamadas({}) == 0.0
    assert cycle_mod._pausa_entre_llamadas({"CONCILIO_PAUSA_SEGUNDOS": "10"}) == 10.0


def test_presupuesto_free_del_ciclo():
    """El ciclo cabe en la cuota free: corpus 90K, firma 2000 / voto 4000, timeout 120s."""
    assert cycle_mod.CALL_TIMEOUT == 120
    assert cycle_mod.MAX_TOKENS_FIRMA <= 2000
    assert (
        cycle_mod.MAX_TOKENS_VOTO == 4000
    )  # razonadores truncan con menos (diseño §5)
    import inspect

    assert inspect.signature(run_cycle).parameters["canon_max_chars"].default == 90_000
