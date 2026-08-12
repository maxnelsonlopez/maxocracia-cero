"""
Tests para MaxoContracts Axiom Validators
"""

import pytest
from decimal import Decimal

from maxocontracts.core.types import VHV, Wellness, SDV, Participant
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
        """Wellness ≥ 1 pasa Invariante 1."""
        wellness = Wellness(value=Decimal("1.2"))
        result = AxiomValidator.validate_invariant_gamma(wellness)
        
        assert result.is_valid is True
        assert result.axiom_code == "INV1"
    
    def test_invariant1_gamma_at_threshold(self):
        """Wellness = 1 (exacto) pasa Invariante 1."""
        wellness = Wellness(value=Decimal("1.0"))
        result = AxiomValidator.validate_invariant_gamma(wellness)
        
        assert result.is_valid is True
    
    def test_invariant1_gamma_below_threshold(self):
        """Wellness < 1 falla Invariante 1."""
        wellness = Wellness(value=Decimal("0.8"))
        result = AxiomValidator.validate_invariant_gamma(wellness)
        
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


class TestAxiomValidatorINV3:
    """Tests para Invariante 3: VHV No Ocultable (auditable públicamente)."""

    def _records(self, **overrides):
        record = {
            "vhv": VHV(T=Decimal("1"), V=Decimal("0"), R=Decimal("0")),
            "source": "term:t1",
            "audit_ref": "t1",
        }
        record.update(overrides)
        return [record]

    def test_inv3_records_validos(self):
        """Registros con VHV, source y audit_ref pasan INV3."""
        result = AxiomValidator.validate_invariant_vhv_auditable(self._records())
        assert result.is_valid is True
        assert result.axiom_code == "INV3"
        assert result.details["records"] == 1

    def test_inv3_sin_vhv_falla(self):
        """Registro sin VHV viola INV3."""
        result = AxiomValidator.validate_invariant_vhv_auditable(
            self._records(vhv=None)
        )
        assert result.is_valid is False
        assert result.details["violations"][0]["reason"] == "VHV no registrado"

    def test_inv3_sin_origen_falla(self):
        """Registro sin source (origen) viola INV3."""
        result = AxiomValidator.validate_invariant_vhv_auditable(
            self._records(source="")
        )
        assert result.is_valid is False
        assert "sin origen" in result.details["violations"][0]["reason"]

    def test_inv3_sin_audit_ref_falla(self):
        """Registro sin audit_ref viola INV3."""
        result = AxiomValidator.validate_invariant_vhv_auditable(
            self._records(audit_ref=None)
        )
        assert result.is_valid is False
        assert "auditoría" in result.details["violations"][0]["reason"]

    def test_inv3_ofuscado_falla(self):
        """Registro marcado como obscured viola INV3."""
        result = AxiomValidator.validate_invariant_vhv_auditable(
            self._records(obscured=True)
        )
        assert result.is_valid is False
        assert result.details["violations"][0]["reason"] == "registro ofuscado"

    def test_inv3_vacio_es_valido_por_vacuidad(self):
        """Sin acciones registradas, INV3 es válido por vacuidad."""
        result = AxiomValidator.validate_invariant_vhv_auditable([])
        assert result.is_valid is True

    def test_inv3_multiples_violaciones_se_reportan(self):
        """Dos registros malos reportan ambas violaciones."""
        records = self._records(audit_ref=None) + self._records(vhv=None)
        result = AxiomValidator.validate_invariant_vhv_auditable(records)
        assert result.is_valid is False
        assert len(result.details["violations"]) == 2


class TestValidateAll:
    """Tests para validación completa."""
    
    def test_validate_all_success(self):
        """validate_all pasa con datos válidos."""
        vhv = VHV(T=Decimal("10"), V=Decimal("0.5"), R=Decimal("2"))
        
        participant = Participant(
            id="test",
            name="Test",
            wellness_current=Wellness(value=Decimal("1.2")),
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
            wellness_current=Wellness(value=Decimal("0.7"))
        )
        
        is_valid, results = AxiomValidator.validate_all(
            vhv=vhv,
            participants=[participant],
            minimum_sdv=SDV()
        )
        
        assert is_valid is False
        failed = [r for r in results if not r.is_valid]
        assert any(r.axiom_code == "INV1" for r in failed)

    def test_validate_all_incluye_inv3(self):
        """validate_all incorpora INV3 (por defecto, con el VHV total)."""
        vhv = VHV(T=Decimal("10"), V=Decimal("0.5"), R=Decimal("2"))
        participant = Participant(
            id="test",
            name="Test",
            wellness_current=Wellness(value=Decimal("1.2")),
            sdv_actual=SDV()
        )
        is_valid, results = AxiomValidator.validate_all(
            vhv=vhv,
            participants=[participant],
            minimum_sdv=SDV()
        )
        inv3 = [r for r in results if r.axiom_code == "INV3"]
        assert len(inv3) == 1
        assert inv3[0].is_valid is True

    def test_validate_all_falla_si_registros_ofuscados(self):
        """validate_all falla si se pasan registros VHV sin trazabilidad."""
        vhv = VHV.zero()
        is_valid, results = AxiomValidator.validate_all(
            vhv=vhv,
            participants=[],
            minimum_sdv=SDV(),
            vhv_records=[{"vhv": None, "source": "t1", "audit_ref": "t1"}]
        )
        assert is_valid is False
        inv3 = [r for r in results if r.axiom_code == "INV3"]
        assert len(inv3) == 1
        assert inv3[0].is_valid is False
