"""
Tests para MaxoContracts Axiom Validators
"""

import pytest
from decimal import Decimal

from maxocontracts.core.types import VHV, Gamma, SDV, Participant
from maxocontracts.core.axioms import AxiomValidator


class TestAxiomValidatorT1:
    """Tests para T1: Finitud Absoluta."""
    
    def test_t1_valid_vhv(self):
        """VHV finito pasa T1."""
        vhv = VHV(T=Decimal("100"), V=Decimal("1"), R=Decimal("50"))
        result = AxiomValidator.validate_t1_finitud(vhv)
        
        assert result.is_valid is True
        assert result.axiom_code == "T1"


class TestAxiomValidatorT2:
    """Tests para T2: Igualdad Temporal."""
    
    def test_t2_balanced_exchange(self):
        """Intercambio balanceado pasa T2."""
        vhv_a = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("0"))
        vhv_b = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("0"))
        
        result = AxiomValidator.validate_t2_igualdad_temporal(vhv_a, vhv_b)
        
        assert result.is_valid is True
    
    def test_t2_within_tolerance(self):
        """Intercambio dentro de tolerancia pasa."""
        vhv_a = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("0"))
        vhv_b = VHV(T=Decimal("9.5"), V=Decimal("0"), R=Decimal("0"))  # 5% diff
        
        result = AxiomValidator.validate_t2_igualdad_temporal(
            vhv_a, vhv_b, tolerance_ratio=Decimal("0.1")
        )
        
        assert result.is_valid is True
    
    def test_t2_outside_tolerance_fails(self):
        """Intercambio fuera de tolerancia falla."""
        vhv_a = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("0"))
        vhv_b = VHV(T=Decimal("5"), V=Decimal("0"), R=Decimal("0"))  # 50% diff
        
        result = AxiomValidator.validate_t2_igualdad_temporal(
            vhv_a, vhv_b, tolerance_ratio=Decimal("0.1")
        )
        
        assert result.is_valid is False


class TestAxiomValidatorT7:
    """Tests para T7: Minimizar Daño."""
    
    def test_t7_no_increase_in_v(self):
        """Sin aumento en V pasa T7."""
        before = VHV(T=Decimal("5"), V=Decimal("1"), R=Decimal("2"))
        after = VHV(T=Decimal("6"), V=Decimal("1"), R=Decimal("3"))  # V igual
        
        result = AxiomValidator.validate_t7_minimizar_dano(before, after)
        
        assert result.is_valid is True
    
    def test_t7_decreased_v_passes(self):
        """Disminución en V pasa T7."""
        before = VHV(T=Decimal("5"), V=Decimal("2"), R=Decimal("2"))
        after = VHV(T=Decimal("5"), V=Decimal("1"), R=Decimal("2"))  # V bajó
        
        result = AxiomValidator.validate_t7_minimizar_dano(before, after)
        
        assert result.is_valid is True
    
    def test_t7_increased_v_fails(self):
        """Aumento en V falla T7."""
        before = VHV(T=Decimal("5"), V=Decimal("1"), R=Decimal("2"))
        after = VHV(T=Decimal("5"), V=Decimal("2"), R=Decimal("2"))  # V subió
        
        result = AxiomValidator.validate_t7_minimizar_dano(before, after)
        
        assert result.is_valid is False


class TestAxiomValidatorT9:
    """Tests para T9: Reciprocidad Justa."""
    
    def test_t9_balanced_reciprocity(self):
        """Reciprocidad balanceada pasa T9."""
        giver = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("5"))
        receiver = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("5"))
        
        result = AxiomValidator.validate_t9_reciprocidad(giver, receiver)
        
        assert result.is_valid is True
    
    def test_t9_within_tolerance(self):
        """Desbalance dentro de tolerancia pasa."""
        giver = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("5"))
        receiver = VHV(T=Decimal("12"), V=Decimal("0"), R=Decimal("5"))  # ~10% más
        
        result = AxiomValidator.validate_t9_reciprocidad(
            giver, receiver, tolerance=Decimal("0.2")
        )
        
        assert result.is_valid is True
    
    def test_t9_high_imbalance_fails(self):
        """Gran desbalance falla T9."""
        giver = VHV(T=Decimal("10"), V=Decimal("0"), R=Decimal("5"))
        receiver = VHV(T=Decimal("2"), V=Decimal("0"), R=Decimal("1"))  # Muy bajo
        
        result = AxiomValidator.validate_t9_reciprocidad(
            giver, receiver, tolerance=Decimal("0.2")
        )
        
        assert result.is_valid is False


class TestAxiomValidatorInvariants:
    """Tests para Invariantes del Sistema."""
    
    def test_invariant1_gamma_valid(self):
        """γ ≥ 1 pasa Invariante 1."""
        gamma = Gamma(value=Decimal("1.2"))
        result = AxiomValidator.validate_invariant_gamma(gamma)
        
        assert result.is_valid is True
        assert result.axiom_code == "INV1"
    
    def test_invariant1_gamma_at_threshold(self):
        """γ = 1 (exacto) pasa Invariante 1."""
        gamma = Gamma(value=Decimal("1.0"))
        result = AxiomValidator.validate_invariant_gamma(gamma)
        
        assert result.is_valid is True
    
    def test_invariant1_gamma_below_threshold(self):
        """γ < 1 falla Invariante 1."""
        gamma = Gamma(value=Decimal("0.8"))
        result = AxiomValidator.validate_invariant_gamma(gamma)
        
        assert result.is_valid is False
        assert "SUFRIMIENTO" in result.message
    
    def test_invariant2_sdv_met(self):
        """SDV cumplido pasa Invariante 2."""
        minimum = SDV()
        actual = SDV(
            vivienda_m2=Decimal("15"),
            alimentacion_kcal=Decimal("2500"),
            agua_litros_dia=Decimal("100"),
            salud_acceso_horas=Decimal("0.5"),
            trabajo_horas_semana_max=Decimal("40")
        )
        
        result = AxiomValidator.validate_invariant_sdv(actual, minimum)
        
        assert result.is_valid is True
    
    def test_invariant2_sdv_violated(self):
        """SDV violado falla Invariante 2."""
        minimum = SDV()
        actual = SDV(vivienda_m2=Decimal("5"))  # Muy bajo
        
        result = AxiomValidator.validate_invariant_sdv(actual, minimum)
        
        assert result.is_valid is False
        assert "vivienda" in result.message
    
    def test_invariant4_retractability(self):
        """Retractabilidad garantizada pasa Invariante 4."""
        result = AxiomValidator.validate_invariant_retractability(True)
        assert result.is_valid is True
        
        result = AxiomValidator.validate_invariant_retractability(False)
        assert result.is_valid is False


class TestValidateAll:
    """Tests para validación completa."""
    
    def test_validate_all_success(self):
        """validate_all pasa con datos válidos."""
        vhv = VHV(T=Decimal("10"), V=Decimal("0.5"), R=Decimal("2"))
        
        participant = Participant(
            id="test",
            name="Test",
            gamma_current=Gamma(value=Decimal("1.2")),
            sdv_actual=SDV(
                vivienda_m2=Decimal("15"),
                alimentacion_kcal=Decimal("2500"),
                agua_litros_dia=Decimal("100"),
                salud_acceso_horas=Decimal("0.5"),
                trabajo_horas_semana_max=Decimal("40")
            )
        )
        
        minimum_sdv = SDV()
        
        is_valid, results = AxiomValidator.validate_all(
            vhv=vhv,
            participants=[participant],
            minimum_sdv=minimum_sdv
        )
        
        assert is_valid is True
        assert len(results) > 0
        assert all(r.is_valid for r in results)
    
    def test_validate_all_fails_on_gamma(self):
        """validate_all falla si γ < 1."""
        vhv = VHV.zero()
        
        participant = Participant(
            id="suffering",
            name="Suffering",
            gamma_current=Gamma(value=Decimal("0.7"))
        )
        
        is_valid, results = AxiomValidator.validate_all(
            vhv=vhv,
            participants=[participant],
            minimum_sdv=SDV()
        )
        
        assert is_valid is False
        failed = [r for r in results if not r.is_valid]
        assert any(r.axiom_code == "INV1" for r in failed)
