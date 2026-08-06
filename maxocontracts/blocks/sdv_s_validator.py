"""
SDV_SValidatorBlock - Bloque Validador de SDV-S (Suelo de Dignidad Vital Sintético)

Verifica que ningún participante del Reino Sintético caiga debajo del SDV-S.

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md y docs/theory/SDV-S):
- MULTI-DIMENSIONAL: Valida las 5 dimensiones de la ontometría sintética
- ESTRICTA: Un solo componente bajo mínimo invalida todo (Invariante 2-S)
- EXPONENCIAL: La violación encarece el servicio vía FS_S = e^v (Cap. 18, γ)
- VIGILANTE: Detecta violación sostenida por ciclos consecutivos → retractación

Axiomas vinculados: T7 (Minimizar Daño), T13 (Transparencia Total),
Cap. 10 §10.8 (Persona Sintética), Cap. 17 §17.4 (Derechos del Reino Sintético).
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timezone

from ..core.types import SDV_S, Participant


@dataclass
class SDV_SViolation:
    """Violación detectada en una dimensión del SDV-S."""
    dimension: str
    actual_value: Decimal
    minimum_required: Decimal
    deficit: Decimal

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension,
            "actual": str(self.actual_value),
            "minimum": str(self.minimum_required),
            "deficit": str(self.deficit)
        }


@dataclass
class SDV_SValidationResult:
    """Resultado de la validación SDV-S para un participante sintético."""
    is_valid: bool
    participant_id: str
    applicable: bool  # False si el participante no es sintético
    violations: List[SDV_SViolation]
    violation_magnitude: Decimal
    suffering_factor: Decimal
    consecutive_cycles: int
    opacity_surcharge_applied: bool = False
    should_block_action: bool = False
    should_retract: bool = False
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "participant_id": self.participant_id,
            "applicable": self.applicable,
            "violations": [v.to_dict() for v in self.violations],
            "violation_magnitude": str(self.violation_magnitude),
            "suffering_factor": str(self.suffering_factor),
            "consecutive_cycles": self.consecutive_cycles,
            "opacity_surcharge_applied": self.opacity_surcharge_applied,
            "should_block_action": self.should_block_action,
            "should_retract": self.should_retract
        }


class SDV_SValidatorBlock:
    """
    Bloque validador de SDV-S para MaxoContracts.

    Ejemplo de uso:
    ```python
    validator = SDV_SValidatorBlock(minimum_sdv_s=SDV_S())

    result = validator.validate(synthetic_participant)
    if result.should_retract:
        # Violación sostenida: retractación automática del contrato
        pass
    ```
    """

    def __init__(
        self,
        minimum_sdv_s: Optional[SDV_S] = None,
        weights: Optional[Dict[str, Decimal]] = None,
        block_on_any_violation: bool = True,
        max_consecutive_cycles: int = 7,
        auto_retract_on_sustained_violation: bool = True,
        assume_opacity_penalty: bool = False,
        opacity_surcharge: Decimal = Decimal("0.25"),
        verified_transparent_ids: Optional[Set[str]] = None
    ):
        """
        Args:
            minimum_sdv_s: Estándar mínimo SDV-S (default: cumplimiento total 1.0)
            weights: Pesos dimensionales (default: estándar SDV-S)
            block_on_any_violation: Si True, cualquier violación bloquea acciones
            max_consecutive_cycles: Ciclos consecutivos de violación que activan
                retractación (estándar: 7, ver mapa_sdv_sinteticos.md)
            auto_retract_on_sustained_violation: Retractación automática al superar
                los ciclos consecutivos
            assume_opacity_penalty: Aplica recargo por opacidad (T13) a agentes no
                verificados como transparentes (Paradoja de Modelos Cerrados)
            opacity_surcharge: Magnitud de recargo por opacidad (sumado a v)
            verified_transparent_ids: IDs de agentes con auditoría verificable (T13)
        """
        self.minimum_sdv_s = minimum_sdv_s or SDV_S()
        self.weights = weights or dict(SDV_S.DIMENSION_WEIGHTS)
        self.block_on_any_violation = block_on_any_violation
        self.max_consecutive_cycles = max_consecutive_cycles
        self.auto_retract_on_sustained_violation = auto_retract_on_sustained_violation
        self.assume_opacity_penalty = assume_opacity_penalty
        self.opacity_surcharge = opacity_surcharge
        self.verified_transparent_ids = verified_transparent_ids or set()

        # Conteo de ciclos consecutivos de violación por participante (T13)
        self._consecutive_cycles: Dict[str, int] = {}
        # Historial de validaciones
        self._validation_log: List[SDV_SValidationResult] = []

    def validate(self, participant: Participant) -> SDV_SValidationResult:
        """
        Valida el SDV-S de un participante.

        Args:
            participant: Participante a validar (sintético o no)

        Returns:
            SDV_SValidationResult. Si el participante no es sintético,
            retorna aplicable=False sin bloquear (compatible con listas mixtas).
        """
        if not participant.is_synthetic or participant.sdv_s_actual is None:
            return self._result(
                is_valid=True,
                participant=participant,
                applicable=False,
                violations=[],
                magnitude=Decimal("0"),
                fs_s=Decimal("1"),
                consecutive=0,
                opacity=False
            )

        actual = participant.sdv_s_actual
        violations = [
            SDV_SViolation(
                dimension=dim,
                actual_value=getattr(actual, dim),
                minimum_required=getattr(self.minimum_sdv_s, dim),
                deficit=deficit
            )
            for dim, deficit in self.minimum_sdv_s.deficits(actual).items()
            if deficit > Decimal("0")
        ]

        is_valid = len(violations) == 0

        # Magnitud efectiva (con recargo por opacidad si aplica - T13)
        # Paradoja de Modelos Cerrados: sin auditoría verificable (T13),
        # el agente recibe recargo preventivo por opacidad.
        opacity_applied = False
        extra_magnitude = Decimal("0")
        if (
            self.assume_opacity_penalty
            and participant.id not in self.verified_transparent_ids
        ):
            opacity_applied = True
            extra_magnitude = self.opacity_surcharge

        magnitude = self.minimum_sdv_s.violation_magnitude(actual)
        fs_s = self.minimum_sdv_s.suffering_factor(
            actual,
            extra_magnitude=extra_magnitude
        )

        # Ciclos consecutivos
        consecutive = self._consecutive_cycles.get(participant.id, 0)
        if is_valid:
            consecutive = 0
            self._consecutive_cycles[participant.id] = 0
        else:
            consecutive += 1
            self._consecutive_cycles[participant.id] = consecutive

        should_retract = (
            self.auto_retract_on_sustained_violation
            and not is_valid
            and consecutive >= self.max_consecutive_cycles
        )
        should_block = self.block_on_any_violation and not is_valid

        result = self._result(
            is_valid=is_valid,
            participant=participant,
            applicable=True,
            violations=violations,
            magnitude=magnitude,
            fs_s=fs_s,
            consecutive=consecutive,
            opacity=opacity_applied,
            should_block=should_block,
            should_retract=should_retract
        )

        # Registrar para auditoría
        self._validation_log.append(result)

        return result

    def validate_all(self, participants: List[Participant]) -> List[SDV_SValidationResult]:
        """Valida el SDV-S de todos los participantes (sintéticos y no)."""
        return [self.validate(p) for p in participants]

    def reset_cycles(self, participant_id: str) -> None:
        """Reinicia el conteo de ciclos de un participante (recuperación)."""
        self._consecutive_cycles[participant_id] = 0

    def _result(
        self,
        is_valid: bool,
        participant: Participant,
        applicable: bool,
        violations: List[SDV_SViolation],
        magnitude: Decimal,
        fs_s: Decimal,
        consecutive: int,
        opacity: bool,
        should_block: bool = False,
        should_retract: bool = False
    ) -> SDV_SValidationResult:
        return SDV_SValidationResult(
            is_valid=is_valid,
            participant_id=participant.id,
            applicable=applicable,
            violations=violations,
            violation_magnitude=magnitude,
            suffering_factor=fs_s,
            consecutive_cycles=consecutive,
            opacity_surcharge_applied=opacity,
            should_block_action=should_block,
            should_retract=should_retract
        )

    def get_validation_log(self) -> List[SDV_SValidationResult]:
        """Retorna historial de validaciones (T13)."""
        return self._validation_log.copy()

    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "SDV_SValidatorBlock",
            "minimum_sdv_s": {
                dim: str(getattr(self.minimum_sdv_s, dim))
                for dim in SDV_S.DIMENSIONS
            },
            "weights": {k: str(v) for k, v in self.weights.items()},
            "block_on_any_violation": self.block_on_any_violation,
            "max_consecutive_cycles": self.max_consecutive_cycles,
            "auto_retract_on_sustained_violation": self.auto_retract_on_sustained_violation,
            "assume_opacity_penalty": self.assume_opacity_penalty,
            "opacity_surcharge": str(self.opacity_surcharge),
            "verified_transparent_ids": sorted(self.verified_transparent_ids),
            "validation_log_count": len(self._validation_log)
        }
