"""
Tests para MaxoContracts Core Types
"""

import pytest
from decimal import Decimal

from maxocontracts.core.types import VHV, Gamma, SDV, Participant, ContractTerm


class TestVHV:
    """Tests para Vector de Huella Vital."""
    
    def test_vhv_creation_valid(self):
        """VHV se crea correctamente con valores válidos."""
        vhv = VHV(T=Decimal("10"), V=Decimal("0.5"), R=Decimal("2"))
        assert vhv.T == Decimal("10")
        assert vhv.V == Decimal("0.5")
        assert vhv.R == Decimal("2")
    
    def test_vhv_negative_t_raises(self):
        """VHV con T negativo lanza error (viola T1 Finitud)."""
        with pytest.raises(ValueError, match="T.*negativo"):
            VHV(T=Decimal("-1"), V=Decimal("0"), R=Decimal("0"))
    
    def test_vhv_zero(self):
        """VHV.zero() crea vector nulo."""
        vhv = VHV.zero()
        assert vhv.T == Decimal("0")
        assert vhv.V == Decimal("0")
        assert vhv.R == Decimal("0")
    
    def test_vhv_addition(self):
        """VHVs se suman correctamente."""
        vhv1 = VHV(T=Decimal("1"), V=Decimal("0.1"), R=Decimal("0.5"))
        vhv2 = VHV(T=Decimal("2"), V=Decimal("0.2"), R=Decimal("1"))
        
        result = vhv1 + vhv2
        
        assert result.T == Decimal("3")
        assert result.V == Decimal("0.3")
        assert result.R == Decimal("1.5")
    
    def test_vhv_to_dict(self):
        """VHV se serializa correctamente."""
        vhv = VHV(T=Decimal("5"), V=Decimal("1"), R=Decimal("2"))
        d = vhv.to_dict()
        
        assert d["T"] == "5"
        assert d["V"] == "1"
        assert d["R"] == "2"


class TestGamma:
    """Tests para índice de bienestar γ."""
    
    def test_gamma_creation(self):
        """Gamma se crea correctamente."""
        g = Gamma(value=Decimal("1.2"))
        assert g.value == Decimal("1.2")
    
    def test_gamma_negative_raises(self):
        """Gamma negativo lanza error."""
        with pytest.raises(ValueError, match="negativo"):
            Gamma(value=Decimal("-0.5"))
    
    def test_gamma_is_suffering(self):
        """is_suffering detecta γ < threshold."""
        g = Gamma(value=Decimal("0.8"))
        assert g.is_suffering() is True
        assert g.is_suffering(threshold=Decimal("0.7")) is False
    
    def test_gamma_is_flourishing(self):
        """is_flourishing detecta γ > 1."""
        flourishing = Gamma(value=Decimal("1.3"))
        neutral = Gamma(value=Decimal("1.0"))
        suffering = Gamma(value=Decimal("0.9"))
        
        assert flourishing.is_flourishing() is True
        assert neutral.is_flourishing() is False
        assert suffering.is_flourishing() is False
    
    def test_gamma_severity_levels(self):
        """severity() clasifica correctamente."""
        assert Gamma(value=Decimal("1.5")).severity() == "flourishing"
        assert Gamma(value=Decimal("1.0")).severity() == "neutral"
        assert Gamma(value=Decimal("0.9")).severity() == "warning"
        assert Gamma(value=Decimal("0.6")).severity() == "critical"
        assert Gamma(value=Decimal("0.3")).severity() == "emergency"


class TestSDV:
    """Tests para Suelo de Dignidad Vital."""
    
    def test_sdv_defaults(self):
        """SDV tiene valores por defecto razonables."""
        sdv = SDV()
        assert sdv.vivienda_m2 == Decimal("9.0")
        assert sdv.alimentacion_kcal == Decimal("2000")
    
    def test_sdv_meets_minimum(self):
        """meets_minimum verifica correctamente."""
        minimum = SDV(vivienda_m2=Decimal("9"), alimentacion_kcal=Decimal("2000"))
        
        # Cumple
        actual_good = SDV(vivienda_m2=Decimal("12"), alimentacion_kcal=Decimal("2200"))
        assert minimum.meets_minimum(actual_good) is True
        
        # No cumple (vivienda bajo mínimo)
        actual_bad = SDV(vivienda_m2=Decimal("6"), alimentacion_kcal=Decimal("2200"))
        assert minimum.meets_minimum(actual_bad) is False
    
    def test_sdv_violations_empty_when_met(self):
        """violations() retorna dict vacío si SDV se cumple."""
        minimum = SDV()
        actual = SDV(
            vivienda_m2=Decimal("15"),
            alimentacion_kcal=Decimal("2500"),
            agua_litros_dia=Decimal("100")
        )
        
        violations = minimum.violations(actual)
        assert len(violations) == 0
    
    def test_sdv_violations_detected(self):
        """violations() detecta y reporta violaciones."""
        minimum = SDV(vivienda_m2=Decimal("9"), alimentacion_kcal=Decimal("2000"))
        actual = SDV(vivienda_m2=Decimal("5"), alimentacion_kcal=Decimal("1500"))
        
        violations = minimum.violations(actual)
        
        assert "vivienda" in violations
        assert "alimentacion" in violations


class TestParticipant:
    """Tests para Participante."""
    
    def test_participant_creation(self):
        """Participante se crea correctamente."""
        p = Participant(id="test-001", name="Test User")
        
        assert p.id == "test-001"
        assert p.name == "Test User"
        assert p.gamma_current.value == Decimal("1.0")  # Default neutral
    
    def test_participant_update_gamma(self):
        """update_gamma actualiza γ con timestamp."""
        p = Participant(id="test-001", name="Test")
        p.update_gamma(Decimal("0.8"))
        
        assert p.gamma_current.value == Decimal("0.8")
        assert p.gamma_current.participant_id == "test-001"
    
    def test_participant_is_in_good_standing(self):
        """is_in_good_standing verifica γ y SDV."""
        sdv_min = SDV()
        
        # Good standing
        good = Participant(
            id="good",
            name="Good",
            gamma_current=Gamma(value=Decimal("1.2")),
            sdv_actual=SDV(vivienda_m2=Decimal("15"))
        )
        assert good.is_in_good_standing(sdv_min) is True
        
        # Bad γ
        bad_gamma = Participant(
            id="bad",
            name="Bad",
            gamma_current=Gamma(value=Decimal("0.8")),
            sdv_actual=SDV(vivienda_m2=Decimal("15"))
        )
        assert bad_gamma.is_in_good_standing(sdv_min) is False


class TestContractTerm:
    """Tests para ContractTerm."""
    
    def test_term_creation(self):
        """Término se crea correctamente."""
        term = ContractTerm(
            id="term-1",
            description="Transferir 10 Maxos",
            vhv_cost=VHV(T=Decimal("0.5"), V=Decimal("0"), R=Decimal("0"))
        )
        
        assert term.id == "term-1"
        assert term.description == "Transferir 10 Maxos"
    
    def test_term_acceptance_tracking(self):
        """is_accepted_by_all verifica aceptaciones."""
        term = ContractTerm(
            id="term-1",
            description="Test term",
            vhv_cost=VHV.zero()
        )
        
        participants = ["alice", "bob"]
        
        # Sin aceptaciones
        assert term.is_accepted_by_all(participants) is False
        
        # Solo Alice acepta
        term.accepted_by["alice"] = True
        assert term.is_accepted_by_all(participants) is False
        
        # Ambos aceptan
        term.accepted_by["bob"] = True
        assert term.is_accepted_by_all(participants) is True
