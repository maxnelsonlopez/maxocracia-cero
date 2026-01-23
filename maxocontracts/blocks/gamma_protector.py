"""
GammaProtectorBlock - Bloque Protector de Gamma

Monitorea el índice de bienestar γ y activa alertas/retractaciones.

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md):
- VIGILANTE: Monitorea continuamente γ de participantes
- PREVENTIVA: Alerta antes de violación, no solo después
- ACTIVADORA: Puede triggear retractación automática

Axiomas vinculados: T7 (Minimizar Daño), Invariante 1 (γ ≥ 1)
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from enum import Enum

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from core.types import Gamma, Participant


class AlertLevel(Enum):
    """Niveles de alerta para γ."""
    FLOURISHING = "flourishing"   # γ ≥ 1.2
    NEUTRAL = "neutral"           # 1.0 ≤ γ < 1.2
    WARNING = "warning"           # 0.8 ≤ γ < 1.0
    CRITICAL = "critical"         # 0.5 ≤ γ < 0.8
    EMERGENCY = "emergency"       # γ < 0.5


@dataclass
class GammaAlert:
    """Alerta generada por el GammaProtectorBlock."""
    level: AlertLevel
    participant_id: str
    gamma_value: Decimal
    threshold: Decimal
    message: str
    triggered_at: datetime = field(default_factory=datetime.utcnow)
    should_retract: bool = False


@dataclass
class GammaCheckResult:
    """Resultado de un chequeo de gamma."""
    all_ok: bool
    alerts: List[GammaAlert]
    should_trigger_retraction: bool
    checked_at: datetime = field(default_factory=datetime.utcnow)


class GammaProtectorBlock:
    """
    Bloque protector de γ para MaxoContracts.
    
    Monitorea el índice de bienestar de todos los participantes
    y genera alertas cuando cae debajo de umbrales definidos.
    
    Ejemplo de uso:
    ```python
    protector = GammaProtectorBlock(
        threshold=Decimal("1.0"),
        warning_threshold=Decimal("1.1"),
        auto_retract_on_emergency=True
    )
    
    result = protector.check(participants)
    if result.should_trigger_retraction:
        # Activar protocolo de retractación
        pass
    ```
    """
    
    def __init__(
        self,
        threshold: Decimal = Decimal("1.0"),
        warning_threshold: Decimal = Decimal("1.1"),
        critical_threshold: Decimal = Decimal("0.8"),
        emergency_threshold: Decimal = Decimal("0.5"),
        auto_retract_on_emergency: bool = True,
        sustained_suffering_days: int = 14,
        on_alert: Optional[Callable[[GammaAlert], None]] = None
    ):
        """
        Args:
            threshold: Umbral mínimo aceptable (Invariante 1)
            warning_threshold: Umbral para emitir advertencia
            critical_threshold: Umbral para estado crítico
            emergency_threshold: Umbral para emergencia (retractación automática)
            auto_retract_on_emergency: Si True, γ < emergency activa retractación
            sustained_suffering_days: Días de sufrimiento antes de retractación
            on_alert: Callback opcional para procesar alertas
        """
        self.threshold = threshold
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.emergency_threshold = emergency_threshold
        self.auto_retract_on_emergency = auto_retract_on_emergency
        self.sustained_suffering_days = sustained_suffering_days
        self.on_alert = on_alert
        
        # Historial de alertas
        self._alert_history: List[GammaAlert] = []
    
    def check(self, participants: List[Participant]) -> GammaCheckResult:
        """
        Verifica el γ de todos los participantes.
        
        Args:
            participants: Lista de participantes a verificar
            
        Returns:
            GammaCheckResult con alertas y estado
        """
        alerts = []
        should_retract = False
        
        for participant in participants:
            gamma = participant.gamma_current
            alert = self._evaluate_gamma(participant.id, gamma)
            
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
        
        return GammaCheckResult(
            all_ok=all_ok,
            alerts=alerts,
            should_trigger_retraction=should_retract
        )
    
    def check_single(self, participant: Participant) -> Optional[GammaAlert]:
        """Verifica el γ de un solo participante."""
        return self._evaluate_gamma(participant.id, participant.gamma_current)
    
    def _evaluate_gamma(self, participant_id: str, gamma: Gamma) -> Optional[GammaAlert]:
        """Evalúa el γ y genera alerta si corresponde."""
        value = gamma.value
        
        # Determinar nivel de alerta
        if value >= Decimal("1.2"):
            return None  # Floreciendo, no hay alerta
        
        if value >= self.threshold:
            if value < self.warning_threshold:
                return GammaAlert(
                    level=AlertLevel.NEUTRAL,
                    participant_id=participant_id,
                    gamma_value=value,
                    threshold=self.threshold,
                    message=f"γ={value:.2f} - Neutral, monitorear"
                )
            return None  # Sobre threshold y warning, todo bien
        
        # γ debajo del threshold - hay sufrimiento (T7)
        if value >= self.critical_threshold:
            return GammaAlert(
                level=AlertLevel.WARNING,
                participant_id=participant_id,
                gamma_value=value,
                threshold=self.threshold,
                message=f"γ={value:.2f} < {self.threshold} - ADVERTENCIA: Sufrimiento detectado"
            )
        
        if value >= self.emergency_threshold:
            return GammaAlert(
                level=AlertLevel.CRITICAL,
                participant_id=participant_id,
                gamma_value=value,
                threshold=self.threshold,
                message=f"γ={value:.2f} - CRÍTICO: Sufrimiento significativo"
            )
        
        # Emergencia
        return GammaAlert(
            level=AlertLevel.EMERGENCY,
            participant_id=participant_id,
            gamma_value=value,
            threshold=self.threshold,
            message=f"γ={value:.2f} - EMERGENCIA: Retractación recomendada",
            should_retract=self.auto_retract_on_emergency
        )
    
    def get_alert_history(self) -> List[GammaAlert]:
        """Retorna historial de alertas (T13: Transparencia)."""
        return self._alert_history.copy()
    
    def clear_history(self) -> None:
        """Limpia el historial de alertas."""
        self._alert_history = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "GammaProtectorBlock",
            "threshold": str(self.threshold),
            "warning_threshold": str(self.warning_threshold),
            "critical_threshold": str(self.critical_threshold),
            "emergency_threshold": str(self.emergency_threshold),
            "auto_retract_on_emergency": self.auto_retract_on_emergency,
            "alert_history_count": len(self._alert_history)
        }
