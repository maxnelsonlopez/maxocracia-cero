"""
SDVValidatorBlock - Bloque Validador de SDV

Verifica que el Suelo de Dignidad Vital no sea violado.

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md):
- MULTI-DIMENSIONAL: Valida todas las dimensiones del SDV
- ESTRICTA: Un solo componente bajo mínimo invalida todo
- CONTEXTUAL: El SDV_mínimo puede variar por región/cultura

Axiomas vinculados: Axioma SDV, Invariante 2
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, Optional, List
from datetime import datetime

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from core.types import SDV, Participant


@dataclass
class SDVViolation:
    """Violación detectada en una dimensión del SDV."""
    dimension: str
    actual_value: Decimal
    minimum_required: Decimal
    deficit: Decimal
    severity: str  # "minor", "moderate", "severe"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension,
            "actual": str(self.actual_value),
            "minimum": str(self.minimum_required),
            "deficit": str(self.deficit),
            "severity": self.severity
        }


@dataclass
class SDVValidationResult:
    """Resultado de la validación SDV."""
    is_valid: bool
    participant_id: str
    violations: List[SDVViolation]
    checked_at: datetime = field(default_factory=datetime.utcnow)
    should_block_action: bool = False
    
    @property
    def violation_count(self) -> int:
        return len(self.violations)
    
    @property
    def most_severe(self) -> Optional[SDVViolation]:
        if not self.violations:
            return None
        severity_order = {"minor": 0, "moderate": 1, "severe": 2}
        return max(self.violations, key=lambda v: severity_order.get(v.severity, 0))


class SDVValidatorBlock:
    """
    Bloque validador de SDV para MaxoContracts.
    
    Verifica que ningún participante caiga debajo del Suelo de
    Dignidad Vital como consecuencia de una acción del contrato.
    
    Ejemplo de uso:
    ```python
    validator = SDVValidatorBlock(minimum_sdv=SDV())
    
    result = validator.validate(participant)
    if not result.is_valid:
        # Bloquear acción - viola Invariante 2
        pass
    ```
    """
    
    def __init__(
        self,
        minimum_sdv: SDV,
        block_on_any_violation: bool = True,
        severity_thresholds: Optional[Dict[str, Decimal]] = None
    ):
        """
        Args:
            minimum_sdv: Estándar mínimo de dignidad vital
            block_on_any_violation: Si True, cualquier violación bloquea
            severity_thresholds: Umbrales para clasificar severidad
        """
        self.minimum_sdv = minimum_sdv
        self.block_on_any_violation = block_on_any_violation
        
        # Umbrales para clasificar severidad (deficit relativo)
        self.severity_thresholds = severity_thresholds or {
            "minor": Decimal("0.1"),      # ≤10% déficit
            "moderate": Decimal("0.3"),   # ≤30% déficit
            "severe": Decimal("1.0")      # >30% déficit
        }
        
        # Historial de validaciones
        self._validation_log: List[SDVValidationResult] = []
    
    def validate(self, participant: Participant) -> SDVValidationResult:
        """
        Valida el SDV de un participante.
        
        Args:
            participant: Participante a validar
            
        Returns:
            SDVValidationResult con detalle de violaciones
        """
        violations = self._check_all_dimensions(participant.sdv_actual)
        
        is_valid = len(violations) == 0
        should_block = self.block_on_any_violation and not is_valid
        
        result = SDVValidationResult(
            is_valid=is_valid,
            participant_id=participant.id,
            violations=violations,
            should_block_action=should_block
        )
        
        # Registrar para auditoría
        self._validation_log.append(result)
        
        return result
    
    def validate_all(self, participants: List[Participant]) -> List[SDVValidationResult]:
        """Valida el SDV de todos los participantes."""
        return [self.validate(p) for p in participants]
    
    def would_violate(
        self,
        participant: Participant,
        projected_sdv: SDV
    ) -> SDVValidationResult:
        """
        Verifica si un SDV proyectado violaría el mínimo.
        
        Útil para validar ANTES de ejecutar una acción.
        """
        violations = self._check_all_dimensions(projected_sdv)
        
        is_valid = len(violations) == 0
        should_block = self.block_on_any_violation and not is_valid
        
        return SDVValidationResult(
            is_valid=is_valid,
            participant_id=participant.id,
            violations=violations,
            should_block_action=should_block
        )
    
    def _check_all_dimensions(self, actual_sdv: SDV) -> List[SDVViolation]:
        """Verifica todas las dimensiones del SDV."""
        violations = []
        
        # Vivienda
        if actual_sdv.vivienda_m2 < self.minimum_sdv.vivienda_m2:
            violations.append(self._create_violation(
                "vivienda",
                actual_sdv.vivienda_m2,
                self.minimum_sdv.vivienda_m2
            ))
        
        # Alimentación
        if actual_sdv.alimentacion_kcal < self.minimum_sdv.alimentacion_kcal:
            violations.append(self._create_violation(
                "alimentacion",
                actual_sdv.alimentacion_kcal,
                self.minimum_sdv.alimentacion_kcal
            ))
        
        # Agua
        if actual_sdv.agua_litros_dia < self.minimum_sdv.agua_litros_dia:
            violations.append(self._create_violation(
                "agua",
                actual_sdv.agua_litros_dia,
                self.minimum_sdv.agua_litros_dia
            ))
        
        # Salud (invertido - máximo de horas aceptable)
        if actual_sdv.salud_acceso_horas > self.minimum_sdv.salud_acceso_horas:
            violations.append(self._create_violation(
                "salud_acceso",
                actual_sdv.salud_acceso_horas,
                self.minimum_sdv.salud_acceso_horas,
                is_max_constraint=True
            ))
        
        # Trabajo (invertido - máximo de horas aceptable)
        if actual_sdv.trabajo_horas_semana_max > self.minimum_sdv.trabajo_horas_semana_max:
            violations.append(self._create_violation(
                "trabajo_horas",
                actual_sdv.trabajo_horas_semana_max,
                self.minimum_sdv.trabajo_horas_semana_max,
                is_max_constraint=True
            ))
        
        return violations
    
    def _create_violation(
        self,
        dimension: str,
        actual: Decimal,
        required: Decimal,
        is_max_constraint: bool = False
    ) -> SDVViolation:
        """Crea un objeto de violación con severidad calculada."""
        if is_max_constraint:
            # Para máximos, el déficit es lo que excede
            deficit = actual - required
            relative = deficit / required if required > 0 else Decimal("1")
        else:
            # Para mínimos, el déficit es lo que falta
            deficit = required - actual
            relative = deficit / required if required > 0 else Decimal("1")
        
        # Clasificar severidad
        if relative <= self.severity_thresholds["minor"]:
            severity = "minor"
        elif relative <= self.severity_thresholds["moderate"]:
            severity = "moderate"
        else:
            severity = "severe"
        
        return SDVViolation(
            dimension=dimension,
            actual_value=actual,
            minimum_required=required,
            deficit=deficit,
            severity=severity
        )
    
    def get_validation_log(self) -> List[SDVValidationResult]:
        """Retorna historial de validaciones (T13)."""
        return self._validation_log.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "SDVValidatorBlock",
            "minimum_sdv": {
                "vivienda_m2": str(self.minimum_sdv.vivienda_m2),
                "alimentacion_kcal": str(self.minimum_sdv.alimentacion_kcal),
                "agua_litros_dia": str(self.minimum_sdv.agua_litros_dia)
            },
            "block_on_any_violation": self.block_on_any_violation,
            "validation_log_count": len(self._validation_log)
        }
