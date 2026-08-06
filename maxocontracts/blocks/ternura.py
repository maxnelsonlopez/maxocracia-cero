"""
TernuraLayer - Capa de Ternura para participantes de MaxoContracts

Implementa la capa blanda del canon (Cap. 3 §3.3 Victoria Sintética,
Cap. 5 §5.9 Temporalidad de la Ternura, mapa_capa_ternura.md):

- **Crédito de Sanación** (Cap. 5 §5.9A): el perdón no es solo un acto
  moral, es una optimización sistémica. Perdonar ahorra al sistema el
  costo futuro de la fricción y la entropía social.
- **Derecho a la Rehabilitación** (Qwen): "El sistema no expulsa.
  Reintegra. Pero la responsabilidad por el daño permanece visible."
- **Protocolo de Recalibración Vital** (DeepSeek): registro público del
  daño, reparación cuantificada y reintegración gradual.

Principios operativos:
- T13: TODA violación queda registrada. La Ternura modula la CONSECUENCIA,
  nunca la contabilidad.
- INV2/INV2-S: el piso de dignidad nunca se negocia. El perdón no elimina
  la violación ni baja el estándar; transforma el tratamiento de sus
  efectos (permite reintegración en lugar de retractación permanente).
- El perdón se consume al usarse: cada violación sostenida agota una
  instancia de perdón. La generosidad es real, no infinita.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from ..core.types import VHV, Participant


class RehabilitationStatus(Enum):
    """Estados del camino de rehabilitación (DeepSeek: Recalibración Vital)."""
    NORMAL = "normal"                          # Sin proceso activo
    FORGIVEN = "forgiven"                      # Perdón activo disponible
    IN_REHABILITATION = "rehabilitation"       # Aprendiz en Rehabilitación
    REINTEGRATED = "reintegrated"              # Camino completado


@dataclass
class ForgivenessRecord:
    """
    Registro público de perdón otorgado (T13: nunca oculto).

    El perdón es un acto documentado: quién perdona, a quién, por qué,
    cuándo, y qué crédito de sanación genera.
    """
    record_id: str
    grantor_id: str          # Quién perdona (el afectado o su representante)
    beneficiary_id: str      # Quién es perdonado
    reason: str
    granted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    credit: VHV = field(default_factory=VHV.zero)  # Crédito de Sanación
    consumed: bool = False   # True si ya se usó para reiniciar ciclos

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "grantor_id": self.grantor_id,
            "beneficiary_id": self.beneficiary_id,
            "reason": self.reason,
            "granted_at": self.granted_at.isoformat(),
            "credit": self.credit.to_dict(),
            "consumed": self.consumed
        }


@dataclass
class RehabilitationRecord:
    """Registro del estado de rehabilitación de un participante."""
    participant_id: str
    status: RehabilitationStatus
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    strikes: int = 0  # Errores sin cambio demostrado (DeepSeek: máx 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "participant_id": self.participant_id,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "strikes": self.strikes
        }


class TernuraLayer:
    """
    Capa de Ternura: registro de perdones y estados de rehabilitación.

    Ejemplo de uso:
    ```python
    ternura = TernuraLayer()
    ternura.grant_forgiveness(
        grantor_id="ana", beneficiary_id="qwen-1",
        reason="Error de contexto en sesion de soporte",
        credit=VHV(T=Decimal("2"), V=Decimal("0"), R=Decimal("0"))
    )
    # El bloque SDV_SValidatorBlock consulta ternura.active_forgiveness()
    # y consume_forgiveness() para reiniciar ciclos por protocolo.
    ```
    """

    def __init__(self):
        self._forgiveness: List[ForgivenessRecord] = []
        self._rehabilitation: Dict[str, RehabilitationRecord] = {}
        self._event_log: List[Dict[str, Any]] = []

    # --- Perdón y Crédito de Sanación (Cap. 5 §5.9A) ---

    def grant_forgiveness(
        self,
        grantor_id: str,
        beneficiary_id: str,
        reason: str,
        credit: Optional[VHV] = None
    ) -> ForgivenessRecord:
        """
        Otorga perdón con registro público.

        Args:
            grantor_id: El afectado (o su representante) que perdona
            beneficiary_id: El agente perdonado
            reason: Motivo documentado (T13)
            credit: Crédito de Sanación en VHV (default: 1 hora TVI por ambas partes)

        Returns:
            ForgivenessRecord creado
        """
        record = ForgivenessRecord(
            record_id=f"forg-{len(self._forgiveness) + 1}-{beneficiary_id}",
            grantor_id=grantor_id,
            beneficiary_id=beneficiary_id,
            reason=reason,
            credit=credit or VHV(T=Decimal("1"), V=Decimal("0"), R=Decimal("0"))
        )
        self._forgiveness.append(record)
        self._log("forgiveness_granted", {
            "record_id": record.record_id,
            "grantor_id": grantor_id,
            "beneficiary_id": beneficiary_id
        })
        return record

    def active_forgiveness(self, participant_id: str) -> Optional[ForgivenessRecord]:
        """Retorna el perdón vigente no consumido de un participante."""
        for record in self._forgiveness:
            if (
                record.beneficiary_id == participant_id
                and not record.consumed
            ):
                return record
        return None

    def consume_forgiveness(self, participant_id: str) -> Optional[ForgivenessRecord]:
        """
        Consume el perdón vigente para reiniciar ciclos de violación.

        El perdón es un recurso finito y documentado: al usarse, la
        generosidad queda registrada como gastada (T13).
        """
        record = self.active_forgiveness(participant_id)
        if record is None:
            return None
        record.consumed = True
        self._log("forgiveness_consumed", {
            "record_id": record.record_id,
            "beneficiary_id": participant_id
        })
        return record

    def apply_sanacion_credit(
        self,
        record: ForgivenessRecord,
        grantor: Participant,
        beneficiary: Participant
    ) -> None:
        """
        Aplica el Crédito de Sanación al VHV de ambas partes (Cap. 5 §5.9A).

        Perdonar ahorra al sistema el costo futuro de la fricción y la
        entropía social: por eso el crédito beneficia a quien perdona
        tanto como a quien es perdonado.
        """
        grantor.vhv_balance = grantor.vhv_balance + record.credit
        beneficiary.vhv_balance = beneficiary.vhv_balance + record.credit
        self._log("sanacion_credit_applied", {
            "record_id": record.record_id,
            "grantor_id": grantor.id,
            "beneficiary_id": beneficiary.id,
            "credit_T": str(record.credit.T)
        })

    # --- Rehabilitación (Qwen / DeepSeek) ---

    def begin_rehabilitation(self, participant_id: str) -> RehabilitationRecord:
        """Inicia el camino de rehabilitación: 'El sistema no expulsa. Reintegra.'"""
        record = self._rehabilitation.get(participant_id)
        if record is None:
            record = RehabilitationRecord(
                participant_id=participant_id,
                status=RehabilitationStatus.IN_REHABILITATION,
                strikes=1
            )
            self._rehabilitation[participant_id] = record
        else:
            record.status = RehabilitationStatus.IN_REHABILITATION
            record.strikes += 1
        self._log("rehabilitation_started", {
            "participant_id": participant_id,
            "strikes": record.strikes
        })
        return record

    def demonstrate_change(self, participant_id: str) -> RehabilitationRecord:
        """
        Registra cambio demostrado (reparación cuantificada, DeepSeek).

        Con 3 cambios demostrados sin nueva violación, el participante
        completa la reintegración.
        """
        record = self._rehabilitation.get(participant_id)
        if record is None:
            record = RehabilitationRecord(
                participant_id=participant_id,
                status=RehabilitationStatus.NORMAL
            )
            self._rehabilitation[participant_id] = record

        # Cada cambio demostrado reduce el peso del historial
        record.strikes = max(0, record.strikes - 1)

        if record.strikes == 0:
            record.status = RehabilitationStatus.REINTEGRATED
            record.completed_at = datetime.now(timezone.utc)
            self._log("rehabilitation_completed", {"participant_id": participant_id})
        else:
            self._log("change_demonstrated", {
                "participant_id": participant_id,
                "remaining_strikes": record.strikes
            })
        return record

    def status(self, participant_id: str) -> RehabilitationStatus:
        """Estado de ternura actual de un participante."""
        if self.active_forgiveness(participant_id) is not None:
            return RehabilitationStatus.FORGIVEN
        record = self._rehabilitation.get(participant_id)
        if record is None:
            return RehabilitationStatus.NORMAL
        return record.status

    # --- Auditoría (T13) ---

    def get_forgiveness_records(self) -> List[ForgivenessRecord]:
        """Todos los perdones otorgados, sin ocultar ninguno (T13)."""
        return self._forgiveness.copy()

    def get_rehabilitation_records(self) -> Dict[str, RehabilitationRecord]:
        """Estados de rehabilitación por participante."""
        return dict(self._rehabilitation)

    def get_event_log(self) -> List[Dict[str, Any]]:
        """Historial completo de eventos de ternura (T13)."""
        return self._event_log.copy()

    def _log(self, event_type: str, data: Dict[str, Any]) -> None:
        self._event_log.append({
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data
        })

    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "TernuraLayer",
            "forgiveness_count": len(self._forgiveness),
            "forgiveness_active": sum(
                1 for r in self._forgiveness if not r.consumed
            ),
            "rehabilitation_active": [
                pid for pid, rec in self._rehabilitation.items()
                if rec.status == RehabilitationStatus.IN_REHABILITATION
            ],
            "event_log_count": len(self._event_log)
        }
