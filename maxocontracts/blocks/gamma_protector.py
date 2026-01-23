"""
WellnessProtectorBlock - Bloque Protector de Bienestar (Wellness)

Monitorea el índice de bienestar (Wellness) y activa alertas/retractaciones.

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md):
- VIGILANTE: Monitorea continuamente el bienestar de los participantes
- PREVENTIVA: Alerta antes de violación, no solo después
- ACTIVADORA: Puede triggear retractación automática

Axiomas vinculados: T7 (Minimizar Daño), Invariante 1 (Wellness ≥ 1)
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from enum import Enum

from maxocontracts.core.types import Wellness, Participant


class AlertLevel(Enum):
    """Niveles de alerta para el bienestar."""
    FLOURISHING = "flourishing"   # W ≥ 1.2
    NEUTRAL = "neutral"           # 1.0 ≤ W < 1.2
    WARNING = "warning"           # 0.8 ≤ W < 1.0
    CRITICAL = "critical"         # 0.5 ≤ W < 0.8
    EMERGENCY = "emergency"       # W < 0.5


@dataclass
class WellnessAlert:
    """Alerta generada por el WellnessProtectorBlock."""
    level: AlertLevel
    participant_id: str
    wellness_value: Decimal
    threshold: Decimal
    message: str
    triggered_at: datetime = field(default_factory=datetime.utcnow)
    should_retract: bool = False


@dataclass
class WellnessCheckResult:
    """Resultado de un chequeo de bienestar."""
    all_ok: bool
    alerts: List[WellnessAlert]
    should_trigger_retraction: bool
    checked_at: datetime = field(default_factory=datetime.utcnow)


class WellnessProtectorBlock:
    """
    Bloque protector de bienestar (Wellness) para MaxoContracts.
    
    Monitorea el índice de bienestar de todos los participantes
    y genera alertas cuando cae debajo de umbrales definidos.
    """
    
    def __init__(
        self,
        threshold: Decimal = Decimal("1.0"),
        warning_threshold: Decimal = Decimal("1.1"),
        critical_threshold: Decimal = Decimal("0.8"),
        emergency_threshold: Decimal = Decimal("0.5"),
        auto_retract_on_emergency: bool = True,
        sustained_suffering_days: int = 14,
        on_alert: Optional[Callable[[WellnessAlert], None]] = None
    ):
        self.threshold = threshold
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.emergency_threshold = emergency_threshold
        self.auto_retract_on_emergency = auto_retract_on_emergency
        self.sustained_suffering_days = sustained_suffering_days
        self.on_alert = on_alert
        
        # Historial de alertas
        self._alert_history: List[WellnessAlert] = []
    
    def check(self, participants: List[Participant]) -> WellnessCheckResult:
        """
        Verifica el bienestar de todos los participantes.
        """
        alerts = []
        should_retract = False
        
        for participant in participants:
            wellness = participant.wellness_current
            alert = self._evaluate_wellness(participant.id, wellness)
            
            if alert:
                alerts.append(alert)
                
                # Invocar callback si existe
                if self.on_alert:
                    self.on_alert(alert)
                
                # Registrar en historial
                self._alert_history.append(alert)
                
                # Determinar si debe retractar
                if alert.should_retract:
                    should_retract = True
        
        all_ok = len(alerts) == 0 or all(
            a.level in [AlertLevel.FLOURISHING, AlertLevel.NEUTRAL]
            for a in alerts
        )
        
        return WellnessCheckResult(
            all_ok=all_ok,
            alerts=alerts,
            should_trigger_retraction=should_retract
        )
    
    def check_single(self, participant: Participant) -> Optional[WellnessAlert]:
        """Verifica el bienestar de un solo participante."""
        return self._evaluate_wellness(participant.id, participant.wellness_current)
    
    def _evaluate_wellness(self, participant_id: str, wellness: Wellness) -> Optional[WellnessAlert]:
        """Evalúa el bienestar y genera alerta si corresponde."""
        value = wellness.value
        
        # Determinar nivel de alerta
        if value >= Decimal("1.2"):
            return None  # Floreciendo, no hay alerta
        
        if value >= self.threshold:
            if value < self.warning_threshold:
                return WellnessAlert(
                    level=AlertLevel.NEUTRAL,
                    participant_id=participant_id,
                    wellness_value=value,
                    threshold=self.threshold,
                    message=f"W={value:.2f} - Neutral, monitorear"
                )
            return None  # Sobre threshold y warning, todo bien
        
        # Bienestar debajo del threshold - hay sufrimiento (T7)
        if value >= self.critical_threshold:
            return WellnessAlert(
                level=AlertLevel.WARNING,
                participant_id=participant_id,
                wellness_value=value,
                threshold=self.threshold,
                message=f"W={value:.2f} < {self.threshold} - ADVERTENCIA: Sufrimiento detectado"
            )
        
        if value >= self.emergency_threshold:
            return WellnessAlert(
                level=AlertLevel.CRITICAL,
                participant_id=participant_id,
                wellness_value=value,
                threshold=self.threshold,
                message=f"W={value:.2f} - CRÍTICO: Sufrimiento significativo"
            )
        
        # Emergencia
        return WellnessAlert(
            level=AlertLevel.EMERGENCY,
            participant_id=participant_id,
            wellness_value=value,
            threshold=self.threshold,
            message=f"W={value:.2f} - EMERGENCIA: Retractación recomendada",
            should_retract=self.auto_retract_on_emergency
        )
    
    def get_alert_history(self) -> List[WellnessAlert]:
        """Retorna historial de alertas (T13: Transparencia)."""
        return self._alert_history.copy()
    
    def clear_history(self) -> None:
        """Limpia el historial de alertas."""
        self._alert_history = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "WellnessProtectorBlock",
            "threshold": str(self.threshold),
            "warning_threshold": str(self.warning_threshold),
            "critical_threshold": str(self.critical_threshold),
            "emergency_threshold": str(self.emergency_threshold),
            "auto_retract_on_emergency": self.auto_retract_on_emergency,
            "alert_history_count": len(self._alert_history)
        }


# ---------------------------------------------------------------------------
# Backward-compatibility alias
# ---------------------------------------------------------------------------
# Muchos docs y ejemplos aún hablan de `GammaProtectorBlock`. El bloque real
# en el código es WellnessProtectorBlock (γ como símbolo se mantiene).
GammaProtectorBlock = WellnessProtectorBlock
