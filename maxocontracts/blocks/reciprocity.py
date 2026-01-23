"""
ReciprocityBlock - Bloque de Reciprocidad

Verifica que el intercambio VHV entre partes esté balanceado.

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md):
- SIMÉTRICA: Evalúa el intercambio desde ambas perspectivas
- TOLERANTE: Permite desbalance dentro de un umbral aceptable
- CALCULADORA: Produce métrica cuantitativa de balance

Axiomas vinculados: T9 (Reciprocidad Justa), T2 (Igualdad Temporal)
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

import sys
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
from core.types import VHV


@dataclass
class ReciprocityBalance:
    """Resultado del análisis de reciprocidad."""
    is_balanced: bool
    giver_vhv: VHV
    receiver_vhv: VHV
    imbalance_T: Decimal  # Desbalance en tiempo
    imbalance_V: Decimal  # Desbalance en vidas
    imbalance_R: Decimal  # Desbalance en recursos
    overall_imbalance: Decimal
    tolerance_used: Decimal
    checked_at: datetime = field(default_factory=datetime.utcnow)
    analysis: Optional[str] = None
    
    @property
    def favors(self) -> Optional[str]:
        """Retorna quién está favorecido en el intercambio."""
        giver_total = self.giver_vhv.T + self.giver_vhv.V + self.giver_vhv.R
        receiver_total = self.receiver_vhv.T + self.receiver_vhv.V + self.receiver_vhv.R
        
        if abs(giver_total - receiver_total) <= self.tolerance_used:
            return None  # Balanceado
        elif giver_total > receiver_total:
            return "receiver"  # Receiver da menos
        else:
            return "giver"  # Giver da menos


class ReciprocityBlock:
    """
    Bloque de reciprocidad para MaxoContracts.
    
    Evalúa si un intercambio entre dos partes respeta el axioma T9
    (reciprocidad justa) verificando que los VHV estén balanceados.
    
    Ejemplo de uso:
    ```python
    reciprocity = ReciprocityBlock(tolerance=Decimal("0.15"))
    
    balance = reciprocity.evaluate(vhv_giver, vhv_receiver)
    if not balance.is_balanced:
        # Notificar desbalance, sugerir ajustes
        pass
    ```
    """
    
    def __init__(
        self,
        tolerance: Decimal = Decimal("0.2"),
        weights: Optional[Dict[str, Decimal]] = None,
        strict_on_lives: bool = True
    ):
        """
        Args:
            tolerance: Tolerancia de desbalance permitido (0.2 = 20%)
            weights: Pesos para cada dimensión del VHV (default: iguales)
            strict_on_lives: Si True, aplica tolerancia menor para V (vidas)
        """
        self.tolerance = tolerance
        self.weights = weights or {
            "T": Decimal("1.0"),
            "V": Decimal("1.0"),
            "R": Decimal("1.0")
        }
        self.strict_on_lives = strict_on_lives
        
        # Tolerancia especial para vidas (más estricta)
        self.lives_tolerance = tolerance / 2 if strict_on_lives else tolerance
        
        # Historial
        self._evaluation_log: list = []
    
    def evaluate(self, giver_vhv: VHV, receiver_vhv: VHV) -> ReciprocityBalance:
        """
        Evalúa la reciprocidad entre giver y receiver.
        
        Args:
            giver_vhv: VHV que da el "giver"
            receiver_vhv: VHV que da el "receiver"
            
        Returns:
            ReciprocityBalance con análisis detallado
        """
        # Calcular desbalances por dimensión
        imbalance_T = self._calculate_dimension_imbalance(
            giver_vhv.T, receiver_vhv.T
        )
        imbalance_V = self._calculate_dimension_imbalance(
            giver_vhv.V, receiver_vhv.V
        )
        imbalance_R = self._calculate_dimension_imbalance(
            giver_vhv.R, receiver_vhv.R
        )
        
        # Calcular desbalance general ponderado
        overall = (
            self.weights["T"] * imbalance_T +
            self.weights["V"] * imbalance_V +
            self.weights["R"] * imbalance_R
        ) / sum(self.weights.values())
        
        # Determinar si está balanceado
        is_balanced = (
            overall <= self.tolerance and
            imbalance_V <= self.lives_tolerance  # Estricto en vidas
        )
        
        # Generar análisis
        analysis = self._generate_analysis(
            imbalance_T, imbalance_V, imbalance_R, overall
        )
        
        result = ReciprocityBalance(
            is_balanced=is_balanced,
            giver_vhv=giver_vhv,
            receiver_vhv=receiver_vhv,
            imbalance_T=imbalance_T,
            imbalance_V=imbalance_V,
            imbalance_R=imbalance_R,
            overall_imbalance=overall,
            tolerance_used=self.tolerance,
            analysis=analysis
        )
        
        # Registrar para auditoría
        self._evaluation_log.append(result)
        
        return result
    
    def suggest_adjustment(
        self,
        giver_vhv: VHV,
        receiver_vhv: VHV
    ) -> Tuple[VHV, str]:
        """
        Sugiere un ajuste al VHV del receiver para balancear.
        
        Returns:
            (VHV sugerido para receiver, explicación)
        """
        # Objetivo: igualar totales ponderados
        giver_total = (
            self.weights["T"] * giver_vhv.T +
            self.weights["V"] * giver_vhv.V +
            self.weights["R"] * giver_vhv.R
        )
        
        receiver_total = (
            self.weights["T"] * receiver_vhv.T +
            self.weights["V"] * receiver_vhv.V +
            self.weights["R"] * receiver_vhv.R
        )
        
        if receiver_total >= giver_total:
            return receiver_vhv, "El intercambio ya está balanceado o favorece al giver."
        
        # Calcular déficit
        deficit = giver_total - receiver_total
        
        # Sugerir agregar al componente T (tiempo) del receiver
        # ya que es el más fácil de ajustar
        additional_T = deficit / self.weights["T"]
        
        suggested = VHV(
            T=receiver_vhv.T + additional_T,
            V=receiver_vhv.V,
            R=receiver_vhv.R
        )
        
        explanation = (
            f"Para balancear, el receiver podría aportar "
            f"{additional_T:.2f} horas TVI adicionales."
        )
        
        return suggested, explanation
    
    def _calculate_dimension_imbalance(
        self,
        giver_value: Decimal,
        receiver_value: Decimal
    ) -> Decimal:
        """Calcula el desbalance relativo para una dimensión."""
        total = giver_value + receiver_value
        
        if total == Decimal("0"):
            return Decimal("0")  # Sin valores, sin desbalance
        
        return abs(giver_value - receiver_value) / total
    
    def _generate_analysis(
        self,
        imb_T: Decimal,
        imb_V: Decimal,
        imb_R: Decimal,
        overall: Decimal
    ) -> str:
        """Genera un análisis en lenguaje civil."""
        parts = []
        
        if overall <= Decimal("0.05"):
            return "Intercambio muy bien balanceado. ✓"
        
        if overall <= self.tolerance:
            parts.append("Intercambio aceptablemente balanceado.")
        else:
            parts.append("⚠️ Intercambio desbalanceado:")
        
        if imb_T > Decimal("0.1"):
            parts.append(f"  - Tiempo: desbalance del {imb_T:.0%}")
        
        if imb_V > Decimal("0.1"):
            parts.append(f"  - Vidas: desbalance del {imb_V:.0%}")
        
        if imb_R > Decimal("0.1"):
            parts.append(f"  - Recursos: desbalance del {imb_R:.0%}")
        
        return "\n".join(parts)
    
    def get_evaluation_log(self) -> list:
        """Retorna historial de evaluaciones (T13)."""
        return self._evaluation_log.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "ReciprocityBlock",
            "tolerance": str(self.tolerance),
            "weights": {k: str(v) for k, v in self.weights.items()},
            "strict_on_lives": self.strict_on_lives,
            "evaluation_log_count": len(self._evaluation_log)
        }
