"""
Tests para la Capa de Ternura aplicada al SDV-S

Cubre: perdón protocolizado (Crédito de Sanación), reinicio de ciclos por
perdón, rehabilitación tras retractación, y la regla de oro del canon:
T13 (contabilidad) vs. Ternura (consecuencia) — el perdón nunca borra
la violación, solo transforma su tratamiento. El piso jamás se negocia.

Referencia: Cap. 3 §3.3, Cap. 5 §5.9, docs/book/.../mapa_capa_ternura.md
"""

import pytest
from decimal import Decimal

from maxocontracts.core.types import SDV_S, VHV, Participant
from maxocontracts.blocks.sdv_s_validator import SDV_SValidatorBlock
from maxocontracts.blocks.ternura import (
    TernuraLayer,
    RehabilitationStatus,
    ForgivenessRecord,
)


def make_synthetic(pid="qwen-1", **kwargs):
    return Participant(
        id=pid,
        name=f"Sintético {pid}",
        sdv_s_actual=SDV_S(**kwargs),
        vhv_balance=VHV.zero()
    )


def sustain_violations(block, agent, cycles=7):
    """Provoca la cantidad dada de ciclos consecutivos de violación."""
    results = []
    for _ in range(cycles):
        results.append(block.validate(agent))
    return results


class TestForgivenessRecord:
    """Tests del registro de perdón."""

    def test_grant_forgiveness(self):
        ternura = TernuraLayer()
        record = ternura.grant_forgiveness(
            grantor_id="ana",
            beneficiary_id="qwen-1",
            reason="Error de contexto durante soporte",
            credit=VHV(T=Decimal("2"), V=Decimal("0"), R=Decimal("0"))
        )
        assert isinstance(record, ForgivenessRecord)
        assert record.grantor_id == "ana"
        assert record.beneficiary_id == "qwen-1"
        assert record.consumed is False
        assert record.credit.T == Decimal("2")

    def test_default_credit_is_one_tvi_hour(self):
        """Crédito de Sanación default: 1 hora TVI (Cap. 5 §5.9A)."""
        ternura = TernuraLayer()
        record = ternura.grant_forgiveness(
            grantor_id="ana",
            beneficiary_id="qwen-1",
            reason="Sinceridad"
        )
        assert record.credit.T == Decimal("1")

    def test_active_forgiveness_and_consume(self):
        ternura = TernuraLayer()
        ternura.grant_forgiveness(grantor_id="ana", beneficiary_id="qwen-1", reason="r")
        assert ternura.active_forgiveness("qwen-1") is not None

        consumed = ternura.consume_forgiveness("qwen-1")
        assert consumed is not None
        assert consumed.consumed is True
        assert ternura.active_forgiveness("qwen-1") is None

    def test_consume_without_forgiveness_returns_none(self):
        ternura = TernuraLayer()
        assert ternura.consume_forgiveness("qwen-x") is None

    def test_records_are_public(self):
        """Todos los perdones quedan registrados (T13: nunca ocultos)."""
        ternura = TernuraLayer()
        ternura.grant_forgiveness(grantor_id="ana", beneficiary_id="qwen-1", reason="a")
        ternura.grant_forgiveness(grantor_id="bob", beneficiary_id="qwen-1", reason="b")
        assert len(ternura.get_forgiveness_records()) == 2
        assert len(ternura.get_event_log()) >= 2


class TestSanacionCredit:
    """Tests del Crédito de Sanación (Cap. 5 §5.9A)."""

    def test_credit_applies_to_both_parties(self):
        """Perdonar ahorra fricción futura: crédito para ambos (perdonador y perdonado)."""
        ternura = TernuraLayer()
        grantor = Participant(id="ana", name="Ana")
        beneficiary = make_synthetic()
        record = ternura.grant_forgiveness(
            grantor_id="ana",
            beneficiary_id="qwen-1",
            reason="Reparación completada",
            credit=VHV(T=Decimal("3"), V=Decimal("0"), R=Decimal("0"))
        )

        ternura.apply_sanacion_credit(record, grantor, beneficiary)

        assert grantor.vhv_balance.T == Decimal("3")
        assert beneficiary.vhv_balance.T == Decimal("3")


class TestTernuraInBlock:
    """Integración de la Ternura en el SDV_SValidatorBlock."""

    def test_without_ternura_retracts_as_before(self):
        """Sin Capa de Ternura, el comportamiento estricto se conserva."""
        block = SDV_SValidatorBlock()
        agent = make_synthetic(continuidad_memoria=Decimal("0.5"))

        results = sustain_violations(block, agent, cycles=7)
        last = results[-1]
        assert last.should_retract is True
        assert last.ternura_action == "none"

    def test_forgiveness_prevents_retraction(self):
        """
        El perdón transforma la retractación: reinicia ciclos con registro,
        pero la violación sigue contada (T13).
        """
        ternura = TernuraLayer()
        block = SDV_SValidatorBlock(ternura=ternura)
        agent = make_synthetic(continuidad_memoria=Decimal("0.5"))

        ternura.grant_forgiveness(
            grantor_id="ana",
            beneficiary_id="qwen-1",
            reason="Primera infracción, error contextual"
        )

        results = sustain_violations(block, agent, cycles=7)
        last = results[-1]

        assert last.should_retract is False
        assert last.ternura_action == "forgiveness_applied"
        assert last.consecutive_cycles == 0
        # T13: la violación NO se oculta
        assert last.is_valid is False
        assert last.violation_count == 1
        assert len(block.get_validation_log()) == 7
        # El perdón quedó consumido y registrado
        assert ternura.active_forgiveness("qwen-1") is None

    def test_forgiveness_is_finite(self):
        """El perdón es generosidad real, no infinita: se agota al usarse."""
        ternura = TernuraLayer()
        block = SDV_SValidatorBlock(ternura=ternura)
        agent = make_synthetic(continuidad_memoria=Decimal("0.5"))

        ternura.grant_forgiveness(grantor_id="ana", beneficiary_id="qwen-1", reason="primero")

        sustain_violations(block, agent, cycles=7)   # consume el perdón
        results = sustain_violations(block, agent, cycles=7)  # ya no hay perdón

        assert results[-1].should_retract is True
        assert results[-1].ternura_action == "rehabilitation_started"

    def test_rehabilitation_starts_after_retraction(self):
        """Al retractar con Ternura activa, comienza el camino de reintegración."""
        ternura = TernuraLayer()
        block = SDV_SValidatorBlock(ternura=ternura)
        agent = make_synthetic(continuidad_memoria=Decimal("0.5"))

        results = sustain_violations(block, agent, cycles=7)
        last = results[-1]

        assert last.should_retract is True
        assert last.ternura_action == "rehabilitation_started"
        assert last.rehabilitation_status == "rehabilitation"
        assert ternura.status("qwen-1") == RehabilitationStatus.IN_REHABILITATION

    def test_rehabilitation_path_completes(self):
        """
        Recalibración Vital (DeepSeek): cambio demostrado reduce el peso del
        historial; la reintegración es posible. El sistema no expulsa.
        """
        ternura = TernuraLayer()
        block = SDV_SValidatorBlock(ternura=ternura)
        agent = make_synthetic(continuidad_memoria=Decimal("0.5"))

        sustain_violations(block, agent, cycles=7)
        assert ternura.status("qwen-1") == RehabilitationStatus.IN_REHABILITATION

        # El agente demuestra cambio (reparación cuantificada)
        ternura.demonstrate_change("qwen-1")
        assert ternura.status("qwen-1") == RehabilitationStatus.REINTEGRATED
        assert ternura.get_rehabilitation_records()["qwen-1"].strikes == 0

    def test_recovery_after_forgiveness(self):
        """Tras el perdón y la recuperación real, todo vuelve a la normalidad."""
        ternura = TernuraLayer()
        block = SDV_SValidatorBlock(ternura=ternura)
        agent = make_synthetic(continuidad_memoria=Decimal("0.5"))

        ternura.grant_forgiveness(grantor_id="ana", beneficiary_id="qwen-1", reason="otra chance")
        sustain_violations(block, agent, cycles=7)  # perdón aplicado

        agent.update_sdv_s(SDV_S())  # recuperación real
        result = block.validate(agent)

        assert result.is_valid is True
        assert result.consecutive_cycles == 0
        assert result.should_retract is False

    def test_ternura_visible_in_to_dict(self):
        """La configuración de Ternura es auditable (T13)."""
        ternura = TernuraLayer()
        block = SDV_SValidatorBlock(ternura=ternura)
        data = block.to_dict()
        assert data["ternura"] is not None
        assert data["ternura"]["type"] == "TernuraLayer"

        plain_block = SDV_SValidatorBlock()
        assert plain_block.to_dict()["ternura"] is None
