"""
ConditionBlock - Bloque de Condición

Bloque fundamental: Si [condición] entonces [permitir siguiente bloque]

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md):
- DETERMINISTA: f(x) siempre retorna el mismo resultado para x
- TRANSPARENTE: La lógica de evaluación es visible (T13)
- DESCRIPTIBLE: Tiene representación en lenguaje civil

Axiomas vinculados: T13 (Transparencia), V6 (Verbo Justo)
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional, List
from datetime import datetime, timezone
from abc import ABC, abstractmethod


@dataclass
class ConditionResult:
    """Resultado de la evaluación de una condición."""
    passed: bool
    condition_id: str
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context_snapshot: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None


class ConditionBlock:
    """
    Bloque de condición para MaxoContracts.
    
    Ejemplo de uso:
    ```python
    cond = ConditionBlock(
        condition_id="has_balance",
        description="El usuario tiene saldo suficiente",
        predicate=lambda ctx: ctx.get("balance", 0) >= ctx.get("required", 0)
    )
    
    result = cond.evaluate({"balance": 100, "required": 50})
    # result.passed = True
    ```
    """
    
    def __init__(
        self,
        condition_id: str,
        description: str,
        predicate: Callable[[Dict[str, Any]], bool],
        civil_language: Optional[str] = None
    ):
        """
        Args:
            condition_id: Identificador único
            description: Descripción técnica
            predicate: Función que evalúa la condición
            civil_language: Descripción en lenguaje civil (≤20 palabras)
        """
        self.condition_id = condition_id
        self.description = description
        self.predicate = predicate
        
        # Validar lenguaje civil
        self.civil_language = civil_language or description
        if len(self.civil_language.split()) > 25:  # Margen sobre el límite de 20
            raise ValueError(
                f"Descripción civil excede límite de palabras: "
                f"{len(self.civil_language.split())} > 20"
            )
    
    def evaluate(self, context: Dict[str, Any]) -> ConditionResult:
        """
        Evalúa la condición contra el contexto actual.
        
        Args:
            context: Diccionario con el estado actual
            
        Returns:
            ConditionResult con el resultado de la evaluación
        """
        try:
            passed = self.predicate(context)
            return ConditionResult(
                passed=passed,
                condition_id=self.condition_id,
                context_snapshot=context.copy(),
                reason="Condición satisfecha" if passed else "Condición no satisfecha"
            )
        except Exception as e:
            # Si hay error en la evaluación, la condición falla
            return ConditionResult(
                passed=False,
                condition_id=self.condition_id,
                context_snapshot=context.copy(),
                reason=f"Error en evaluación: {str(e)}"
            )
    
    def to_civil_language(self) -> str:
        """Retorna descripción en lenguaje civil (grado 8vo)."""
        return self.civil_language
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría (T13)."""
        return {
            "type": "ConditionBlock",
            "condition_id": self.condition_id,
            "description": self.description,
            "civil_language": self.civil_language
        }


# --- Condiciones Predefinidas ---

class CommonConditions:
    """Fábrica de condiciones comunes para MaxoContracts."""
    
    @staticmethod
    def has_minimum_balance(key: str = "balance", minimum: float = 0) -> ConditionBlock:
        """Condición: el saldo es mayor o igual al mínimo."""
        return ConditionBlock(
            condition_id=f"has_minimum_balance_{key}",
            description=f"Verifica que {key} >= {minimum}",
            predicate=lambda ctx: ctx.get(key, 0) >= minimum,
            civil_language=f"Tienes al menos {minimum} en tu cuenta."
        )
    
    @staticmethod
    def all_parties_accepted(key: str = "acceptances") -> ConditionBlock:
        """Condición: todas las partes aceptaron."""
        return ConditionBlock(
            condition_id="all_parties_accepted",
            description="Verifica que todos los participantes hayan aceptado",
            predicate=lambda ctx: all(ctx.get(key, {}).values()),
            civil_language="Todos los participantes han aceptado."
        )
    
    @staticmethod
    def within_time_limit(deadline_key: str = "deadline") -> ConditionBlock:
        """Condición: estamos dentro del límite de tiempo."""
        return ConditionBlock(
            condition_id="within_time_limit",
            description=f"Verifica que fecha actual <= {deadline_key}",
            predicate=lambda ctx: datetime.now(timezone.utc) <= ctx.get(deadline_key, datetime.max.replace(tzinfo=timezone.utc)),
            civil_language="Estamos dentro del plazo acordado."
        )
    
    @staticmethod
    def custom(
        condition_id: str,
        civil_language: str,
        predicate: Callable[[Dict[str, Any]], bool]
    ) -> ConditionBlock:
        """Crea una condición personalizada."""
        return ConditionBlock(
            condition_id=condition_id,
            description=civil_language,
            predicate=predicate,
            civil_language=civil_language
        )
