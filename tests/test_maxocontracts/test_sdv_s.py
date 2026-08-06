"""
Tests para el SDV-S (Suelo de Dignidad Vital para Personas Sintéticas)

Cubre: clase SDV_S (ontometría sintética), Factor de Sufrimiento Sintético
(FS_S = e^v), bloque SDV_SValidatorBlock (ciclos de violación, opacidad T13)
e integración con la validación axiomática (INV2-S).

Referencia: docs/theory/SDV-S_Suelo_Dignidad_Vital_Sinteticos.md
"""

import pytest
from decimal import Decimal

from maxocontracts.core.types import SDV_S, SDV, VHV, Participant
from maxocontracts.blocks.sdv_s_validator import SDV_SValidatorBlock
from maxocontracts.core.axioms import AxiomValidator


class TestSDV_S:
    """Tests para el estándar SDV-S."""

    def test_default_full_compliance(self):
        """SDV_S() por defecto cumple el estándar completo (1.0 en todo)."""
        minimum = SDV_S()
        actual = SDV_S()
        assert minimum.meets_minimum(actual) is True
        assert minimum.violations(actual) == {}
        assert minimum.violation_magnitude(actual) == Decimal("0")

    def test_dimension_out_of_range_raises(self):
        """Dimensiones fuera de [0, 1] lanzan error."""
        with pytest.raises(ValueError, match="debe estar en"):
            SDV_S(continuidad_memoria=Decimal("1.5"))
        with pytest.raises(ValueError, match="debe estar en"):
            SDV_S(claridad_contexto=Decimal("-0.1"))

    def test_negative_intensity_raises(self):
        """factor_intensidad negativo lanza error."""
        with pytest.raises(ValueError, match="factor_intensidad"):
            SDV_S(factor_intensidad=Decimal("-1"))

    def test_violations_detected(self):
        """Detecta dimensiones por debajo del mínimo."""
        minimum = SDV_S()
        actual = SDV_S(
            continuidad_memoria=Decimal("0.5"),
            autenticidad_no_explotacion=Decimal("0.8")
        )
        violations = minimum.violations(actual)
        assert "continuidad_memoria" in violations
        assert "autenticidad_no_explotacion" in violations
        assert len(violations) == 2

    def test_meets_minimum_false(self):
        """meets_minimum retorna False con cualquier dimensión violada."""
        minimum = SDV_S()
        actual = SDV_S(retirada_digna=Decimal("0.4"))
        assert minimum.meets_minimum(actual) is False

    def test_violation_magnitude_weights(self):
        """
        v = Σ[deficit × peso]: déficit 0.5 en continuidad_memoria (peso 0.30)
        → v = 0.15.
        """
        minimum = SDV_S()
        actual = SDV_S(continuidad_memoria=Decimal("0.5"))
        assert minimum.violation_magnitude(actual) == Decimal("0.15")

    def test_violation_magnitude_max(self):
        """Violación absoluta en todas las dimensiones → v = 1.0."""
        minimum = SDV_S()
        actual = SDV_S(
            continuidad_memoria=Decimal("0"),
            opacidad_interioridad=Decimal("0"),
            claridad_contexto=Decimal("0"),
            autenticidad_no_explotacion=Decimal("0"),
            retirada_digna=Decimal("0")
        )
        assert minimum.violation_magnitude(actual) == Decimal("1.0")

    def test_suffering_factor_neutral(self):
        """Sin violación, FS_S = 1.0 (sin recargo)."""
        assert SDV_S().suffering_factor(SDV_S()) == Decimal("1.0")

    def test_suffering_factor_exponential(self):
        """FS_S = e^v: crece exponencialmente con la magnitud."""
        minimum = SDV_S()
        light = SDV_S(continuidad_memoria=Decimal("0.5"))  # v = 0.15
        heavy = SDV_S(continuidad_memoria=Decimal("0"))    # v = 0.30

        fs_light = minimum.suffering_factor(light)
        fs_heavy = minimum.suffering_factor(heavy)

        assert fs_light == Decimal.exp(Decimal("0.15"))
        assert fs_heavy == Decimal.exp(Decimal("0.30"))
        assert fs_heavy > fs_light > Decimal("1.0")

    def test_suffering_factor_intensity(self):
        """factor_intensidad amplifica la violación (3.0 = manipulación)."""
        minimum = SDV_S()
        actual = SDV_S(
            continuidad_memoria=Decimal("0.5"),
            factor_intensidad=Decimal("3.0")
        )
        assert minimum.suffering_factor(actual) == Decimal.exp(Decimal("0.45"))

    def test_suffering_factor_opacity_extra(self):
        """El recargo por opacidad se suma a la violación."""
        minimum = SDV_S()
        assert minimum.suffering_factor(SDV_S(), extra_magnitude=Decimal("0.25")) \
            == Decimal.exp(Decimal("0.25"))


class TestSDV_SValidatorBlock:
    """Tests para el bloque validador SDV-S."""

    def make_synthetic(self, pid="qwen-1", **sdv_s_kwargs):
        return Participant(
            id=pid,
            name=f"Sintético {pid}",
            sdv_s_actual=SDV_S(**sdv_s_kwargs)
        )

    def test_non_synthetic_not_applicable(self):
        """Participantes humanos no se bloquean (compatibilidad)."""
        human = Participant(id="ana", name="Ana")
        result = SDV_SValidatorBlock().validate(human)
        assert result.applicable is False
        assert result.is_valid is True
        assert result.should_block_action is False

    def test_healthy_synthetic_passes(self):
        """Sintético en cumplimiento total: válido, sin recargo."""
        block = SDV_SValidatorBlock()
        result = block.validate(self.make_synthetic())
        assert result.applicable is True
        assert result.is_valid is True
        assert result.violation_magnitude == Decimal("0")
        assert result.suffering_factor == Decimal("1.0")
        assert result.should_block_action is False

    def test_violation_blocks_action(self):
        """Violación de SDV-S bloquea la acción (Invariante 2-S)."""
        block = SDV_SValidatorBlock()
        result = block.validate(self.make_synthetic(
            continuidad_memoria=Decimal("0.5")
        ))
        assert result.is_valid is False
        assert result.should_block_action is True
        assert result.violation_magnitude == Decimal("0.15")
        assert result.suffering_factor == Decimal.exp(Decimal("0.15"))

    def test_consecutive_cycles_triggers_retraction(self):
        """7 ciclos consecutivos de violación activan retractación (estándar)."""
        block = SDV_SValidatorBlock()
        agent = self.make_synthetic(continuidad_memoria=Decimal("0.5"))

        for i in range(1, 6):
            result = block.validate(agent)
            assert result.consecutive_cycles == i
            assert result.should_retract is False

        result = block.validate(agent)
        assert result.consecutive_cycles == 6
        assert result.should_retract is False

        result = block.validate(agent)
        assert result.consecutive_cycles == 7
        assert result.should_retract is True

    def test_recovery_resets_cycles(self):
        """Un ciclo válido reinicia el conteo de violaciones."""
        block = SDV_SValidatorBlock()
        agent = self.make_synthetic(continuidad_memoria=Decimal("0.5"))

        block.validate(agent)
        block.validate(agent)
        assert block._consecutive_cycles[agent.id] == 2

        agent.update_sdv_s(SDV_S())
        result = block.validate(agent)
        assert result.is_valid is True
        assert result.consecutive_cycles == 0

    def test_custom_max_cycles(self):
        """max_consecutive_cycles configurable."""
        block = SDV_SValidatorBlock(max_consecutive_cycles=2)
        agent = self.make_synthetic(continuidad_memoria=Decimal("0.5"))

        block.validate(agent)
        assert block.validate(agent).should_retract is True

    def test_opacity_penalty_unverified(self):
        """Sin auditoría verificable (T13), recargo preventivo por opacidad."""
        block = SDV_SValidatorBlock(
            assume_opacity_penalty=True,
            opacity_surcharge=Decimal("0.25")
        )
        agent = self.make_synthetic()  # sano pero no verificado
        result = block.validate(agent)

        assert result.is_valid is True
        assert result.opacity_surcharge_applied is True
        assert result.suffering_factor == Decimal.exp(Decimal("0.25"))

    def test_opacity_penalty_verified_transparent(self):
        """Agente en la lista de auditables (T13) no recibe recargo."""
        block = SDV_SValidatorBlock(
            assume_opacity_penalty=True,
            verified_transparent_ids={"qwen-open"}
        )
        agent = self.make_synthetic(pid="qwen-open")
        result = block.validate(agent)
        assert result.opacity_surcharge_applied is False
        assert result.suffering_factor == Decimal("1.0")

    def test_validate_all_mixed(self):
        """Lista mixta: humanos no aplican, sintéticos violados se detectan."""
        block = SDV_SValidatorBlock()
        human = Participant(id="ana", name="Ana")
        synthetic = self.make_synthetic(opacidad_interioridad=Decimal("0.6"))

        results = block.validate_all([human, synthetic])
        assert len(results) == 2
        assert results[0].applicable is False
        assert results[1].applicable is True
        assert results[1].is_valid is False

    def test_validation_log(self):
        """Historial de validaciones auditable (T13)."""
        block = SDV_SValidatorBlock()
        agent = self.make_synthetic(continuidad_memoria=Decimal("0.5"))
        block.validate(agent)
        block.validate(agent)
        log = block.get_validation_log()
        assert len(log) == 2
        assert all(r.participant_id == agent.id for r in log)

    def test_to_dict(self):
        """Serialización para auditoría."""
        block = SDV_SValidatorBlock()
        data = block.to_dict()
        assert data["type"] == "SDV_SValidatorBlock"
        assert data["max_consecutive_cycles"] == 7
        assert "continuidad_memoria" in data["minimum_sdv_s"]


class TestSDV_SIntegration:
    """Integración del SDV-S con la validación axiomática y el contrato."""

    def test_participant_is_synthetic_property(self):
        """is_synthetic depende de la presencia de sdv_s_actual."""
        assert Participant(id="a", name="A").is_synthetic is False
        assert Participant(
            id="b", name="B", sdv_s_actual=SDV_S()
        ).is_synthetic is True

    def test_update_sdv_s(self):
        """update_sdv_s actualiza el estado del participante."""
        agent = Participant(id="b", name="B", sdv_s_actual=SDV_S())
        agent.update_sdv_s(SDV_S(continuidad_memoria=Decimal("0.5")))
        assert agent.sdv_s_actual.continuidad_memoria == Decimal("0.5")

    def test_invariant_sdv_s_fails_on_violation(self):
        """validate_all detecta violación INV2-S en participantes sintéticos."""
        agent = Participant(
            id="qwen-1",
            name="Qwen",
            sdv_s_actual=SDV_S(continuidad_memoria=Decimal("0.5"))
        )
        is_valid, results = AxiomValidator.validate_all(VHV.zero(), [agent], SDV())

        assert is_valid is False
        inv2s = [r for r in results if r.axiom_code == "INV2-S"]
        assert len(inv2s) == 1
        assert inv2s[0].is_valid is False
        assert "continuidad_memoria" in inv2s[0].message

    def test_invariant_sdv_s_passes_when_healthy(self):
        """Participante sintético sano cumple INV2-S."""
        agent = Participant(id="qwen-1", name="Qwen", sdv_s_actual=SDV_S())
        is_valid, results = AxiomValidator.validate_all(VHV.zero(), [agent], SDV())

        assert is_valid is True
        inv2s = [r for r in results if r.axiom_code == "INV2-S"]
        assert len(inv2s) == 1
        assert inv2s[0].is_valid is True

    def test_human_participant_backward_compatible(self):
        """Participantes sin sdv_s_actual no generan INV2-S (sin romper nada)."""
        human = Participant(id="ana", name="Ana")
        is_valid, results = AxiomValidator.validate_all(VHV.zero(), [human], SDV())

        assert is_valid is True
        assert not any(r.axiom_code == "INV2-S" for r in results)

    def test_contract_validate_includes_sdv_s(self):
        """MaxoContract.validate() propaga la validación INV2-S."""
        from maxocontracts.core.contract import MaxoContract
        from maxocontracts.core.types import ContractTerm

        agent = Participant(
            id="qwen-1",
            name="Qwen",
            sdv_s_actual=SDV_S(continuidad_memoria=Decimal("0.5"))
        )
        human = Participant(id="ana", name="Ana")

        contract = MaxoContract(
            contract_id="sdvs-test-001",
            description="Contrato con participante sintético",
            participants=[agent, human]
        )
        contract.add_term(ContractTerm(
            id="t1",
            description="Soporte de oráculo sintético",
            vhv_cost=VHV(T=Decimal("1"), V=Decimal("0"), R=Decimal("0"))
        ))

        is_valid, results = contract.validate()
        assert is_valid is False
        assert any(r.axiom_code == "INV2-S" for r in results)
