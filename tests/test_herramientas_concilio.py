# -*- coding: utf-8 -*-
"""Tests de las herramientas del Concilio (misión del ciclo 114428, LOW)."""

from types import SimpleNamespace
from pathlib import Path

from scripts import canon_index as ci
from scripts import verificar_coherencia as vc


def test_canon_index_enumera_areas_y_encabezados(tmp_path):
    root = tmp_path / "repo"
    (root / "docs" / "theory").mkdir(parents=True)
    (root / "docs" / "theory" / "idea.md").write_text(
        "# La idea del tiempo\n\nEl TVI es el recurso más escaso.\n", encoding="utf-8"
    )
    (root / "maxocontracts" / "core").mkdir(parents=True)
    (root / "maxocontracts" / "core" / "axioms.py").write_text(
        "# Axiomas\nINV1: gamma >= 1\n", encoding="utf-8"
    )
    indice = ci.build_index(root)
    assert "La idea del tiempo" in indice  # encabezado capturado
    assert "axioms.py" in indice
    assert "docs/theory" in indice
    assert "Teoría" in indice  # área declarada y presente


def test_verificar_coherencia_informa_comprobaciones(monkeypatch):
    llamadas = []

    def fake_run(cmd, timeout=0):
        llamadas.append(cmd[-1])
        return SimpleNamespace(returncode=0, stdout="1 passed in 0.1s", stderr="")

    monkeypatch.setattr(vc, "_run", fake_run)
    assert vc.ejecutar(con_suite=False) == 0
    # corpus + validador + sus tests (la suite va con --suite)
    assert len(llamadas) == 3
    # la integridad del corpus va primero: si el Concilio lee recortado, nada
    # de lo que venga después importa
    assert "auditar_canon" in llamadas[0]
    assert "validador_conceptual" in llamadas[1]


def test_verificar_coherencia_detecta_rojo(monkeypatch):
    def fake_run(cmd, timeout=0):
        return SimpleNamespace(returncode=1, stdout="", stderr="fallo")

    monkeypatch.setattr(vc, "_run", fake_run)
    assert vc.ejecutar(con_suite=False) == 1


def test_verificar_coherencia_suite_opcional(monkeypatch):
    llamadas = []

    def fake_run(cmd, timeout=0):
        llamadas.append(cmd[-2:])
        return SimpleNamespace(returncode=0, stdout="982 passed", stderr="")

    monkeypatch.setattr(vc, "_run", fake_run)
    assert vc.ejecutar(con_suite=True) == 0
    assert len(llamadas) == 4  # corpus + validador + tests + suite completa
