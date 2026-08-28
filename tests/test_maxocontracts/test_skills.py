# -*- coding: utf-8 -*-
"""Tests del motor de la vacuación (regla de oro + triada) — rama educativa.

maxocontracts/skills.py es lógica pura: los veredictos se verifican sin
Flask, con razones explícitas (T13).
"""

import pytest

from maxocontracts.skills import (
    VacuacionRequirements,
    TriadaVotos,
    evaluate_triada,
    evaluate_vacuacion,
    evaluar_concesion,
)


class TestReglaDeOro:
    def test_vacua_con_requisitos_completos(self):
        resultado = evaluate_vacuacion(
            obra_aplicada=True, material_publicado=True, mentoria_horas=2.0
        )
        assert resultado.vacua is True
        assert resultado.faltantes == []
        assert "transferencia" in resultado.razones[0]

    def test_faltan_los_tres_requisitos(self):
        resultado = evaluate_vacuacion(False, False, 0.0)
        assert resultado.vacua is False
        assert set(resultado.faltantes) == {
            "obra aplicada",
            "material de enseñanza publicado",
            "mentoría mínima (1 h de TVI)",
        }

    def test_frontera_de_mentoria(self):
        # 1.0 h exacta cumple el mínimo por defecto.
        resultado = evaluate_vacuacion(True, True, 1.0)
        assert resultado.vacua is True
        # 0.99 h no cumple.
        resultado = evaluate_vacuacion(True, True, 0.99)
        assert resultado.vacua is False
        assert "mentoría" in resultado.faltantes[0]

    def test_requirements_personalizados(self):
        reqs = VacuacionRequirements(mentoria_min_horas=3.0)
        resultado = evaluate_vacuacion(True, True, 2.0, requirements=reqs)
        assert resultado.vacua is False
        resultado = evaluate_vacuacion(True, True, 3.5, requirements=reqs)
        assert resultado.vacua is True

    def test_sin_obra_pero_con_resto(self):
        resultado = evaluate_vacuacion(False, True, 5.0)
        assert resultado.vacua is False
        assert resultado.faltantes == ["obra aplicada"]


class TestTriada:
    def test_triada_completa_aprueba(self):
        resultado = evaluate_triada(TriadaVotos(mentor_ok=True, peer_ok=True))
        assert resultado.aprobada is True
        assert resultado.bloqueos == []

    def test_mentor_no_avala(self):
        resultado = evaluate_triada(TriadaVotos(mentor_ok=False, peer_ok=True))
        assert resultado.aprobada is False
        assert "el mentor (facilitador) no avala" in resultado.bloqueos

    def test_par_no_avala(self):
        resultado = evaluate_triada(TriadaVotos(mentor_ok=True, peer_ok=False))
        assert resultado.aprobada is False
        assert "el par no avala" in resultado.bloqueos

    def test_oraculo_ejerce_veto(self):
        resultado = evaluate_triada(
            TriadaVotos(mentor_ok=True, peer_ok=True, oracle_veto=True)
        )
        assert resultado.aprobada is False
        assert "el oráculo ejerció el veto (axiomas en riesgo)" in resultado.bloqueos

    def test_triada_con_veto_no_es_usual_aprobacion(self):
        # El veto no se "compensa" con más aprobaciones humanas: guardarraíl.
        resultado = evaluate_triada(
            TriadaVotos(mentor_ok=True, peer_ok=True, oracle_veto=True)
        )
        assert resultado.aprobada is False


class TestConcesion:
    def test_concesion_awarded(self):
        veredicto = evaluar_concesion(True, True, 2.0, TriadaVotos(True, True))
        assert veredicto["outcome"] == "awarded"
        assert veredicto["vacua"]["cumplida"] is True
        assert veredicto["triada"]["aprobada"] is True

    def test_concesion_awaiting_por_triada_incompleta(self):
        veredicto = evaluar_concesion(True, True, 2.0, TriadaVotos(True, False))
        assert veredicto["outcome"] == "awaiting_triada"
        assert veredicto["triada"]["bloqueos"] == ["el par no avala"]

    def test_concesion_rejected_por_regla_de_oro(self):
        veredicto = evaluar_concesion(True, False, 0.0, TriadaVotos(True, True))
        assert veredicto["outcome"] == "rejected"
        assert veredicto["vacua"]["faltantes"]

    def test_concesion_rejected_por_veto(self):
        veredicto = evaluar_concesion(True, True, 2.0, TriadaVotos(True, True, True))
        assert veredicto["outcome"] == "awaiting_triada"

    def test_serializable(self):
        import json

        veredicto = evaluar_concesion(True, True, 1.0, TriadaVotos(True, True))
        json.dumps(veredicto)  # no debe lanzar (T13)
