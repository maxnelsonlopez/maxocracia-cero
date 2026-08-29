# -*- coding: utf-8 -*-
"""Tests del puente años<->índice educativo (M5 — rama educativa).

El motor (INV2-EDU) trabaja en años; SDVScore.educacion es índice 0-1.
educacion_indice() es el puente determinista entre ambos mundos.
"""

from app.sdv_analyzer import EDU_ANIOS_MINIMOS, educacion_indice


class TestPuenteEducacion:
    def test_none_no_castiga(self):
        """Sin dato (None): el SDV educativo no se penaliza (INV2-EDU solo
        se activa cuando hay dato)."""
        assert educacion_indice(None) == 1.0

    def test_piso_pleno_12_anos(self):
        assert educacion_indice(12) == 1.0
        assert educacion_indice(15) == 1.0
        assert educacion_indice(40) == 1.0

    def test_frontera_12(self):
        assert educacion_indice(EDU_ANIOS_MINIMOS) == 1.0

    def test_lineal_0_a_12(self):
        # 0 años -> mínimo vital teórico.
        assert educacion_indice(0) == 0.1
        assert educacion_indice(6) == 0.55  # 0.1 + 0.9*0.5
        assert educacion_indice(3) == 0.325  # 0.1 + 0.9*0.25

    def test_negativo_tratado_como_cero(self):
        assert educacion_indice(-5) == 0.1

    def test_determinista(self):
        assert educacion_indice(7) == educacion_indice(7)
        assert educacion_indice(2.5) == educacion_indice(2.5)

    def test_coherente_con_motor(self):
        """El puente nunca desciende por debajo del piso del analyzer (0.1)."""
        for anos in range(0, 25):
            assert 0.1 <= educacion_indice(float(anos)) <= 1.0


class TestPuenteUmbralParametrizado:
    """El umbral de plenitud es votable (Parlamento Educativo, 12-30);
    la ley (>= 12 años, INV2-EDU) no se vota. El puente es determinista
    para cualquier umbral válido."""

    def test_plenitud_segunda_el_umbral(self):
        # Con umbral comunitario 14: plenitud a partir de 14 años.
        assert educacion_indice(14, umbral_anios=14) == 1.0
        assert educacion_indice(20, umbral_anios=14) == 1.0

    def test_lineal_con_umbral_personalizado(self):
        # 12 años con umbral 14: 0.1 + 0.9 * (12/14) = 0.871 — la ley se
        # cumple (INV2-EDU) pero la plenitud aspiracional no (entropía δ).
        assert educacion_indice(12, umbral_anios=14) == 0.871
        assert educacion_indice(7, umbral_anios=14) == 0.55  # 0.1 + 0.9*0.5

    def test_none_no_castiga_con_cualquier_umbral(self):
        # La duda sin dato jamás castiga, sea cual sea la plenitud votada.
        assert educacion_indice(None, umbral_anios=30) == 1.0

    def test_default_retrocompatible_con_canon(self):
        # Sin umbral explícito, el canon SDV-H (12 años) manda.
        assert educacion_indice(12) == 1.0
        assert educacion_indice(6, umbral_anios=12) == educacion_indice(6)

    def test_umbral_maximo_30_es_lineal(self):
        # 15 años con el techo de plenitud: 0.1 + 0.9 * (15/30) = 0.55.
        assert educacion_indice(15, umbral_anios=30) == 0.55
