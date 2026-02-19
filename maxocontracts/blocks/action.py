"""
ActionBlock - Bloque de Acción

Ejecuta una transformación en el contexto y registra el VHV consumido.

Propiedades formales (de FUNDAMENTOS_CONCEPTUALES.md):
- TRANSFORMADORA: Modifica el estado del contexto
- REGISTRABLE: Produce log auditable de cambios
- REVERSIBLE: Puede existir acción inversa (para retractación)

Axiomas vinculados: T4 (Materialización), T10 (Responsabilidad)
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
import copy

from ..core.types import VHV


@dataclass
class ActionResult:
    """Resultado de la ejecución de una acción."""
    success: bool
    action_id: str
    vhv_consumed: VHV
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context_before: Optional[Dict[str, Any]] = None
    context_after: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class ActionBlock:
    """
    Bloque de acción para MaxoContracts.
    
    Una acción transforma el contexto y registra el VHV consumido.
    Toda acción debe tener una acción inversa para soportar retractación.
    
    Ejemplo de uso:
    ```python
    action = ActionBlock(
        action_id="transfer_maxos",
        description="Transfiere Maxos de A a B",
        vhv_cost=VHV(T=Decimal("0.1"), V=Decimal("0"), R=Decimal("0")),
        transformer=lambda ctx: {**ctx, "balance_a": ctx["balance_a"] - 10},
        reverse_transformer=lambda ctx: {**ctx, "balance_a": ctx["balance_a"] + 10}
    )
    
    result = action.execute({"balance_a": 100})
    # result.success = True, result.context_after["balance_a"] = 90
    ```
    """
    
    def __init__(
        self,
        action_id: str,
        description: str,
        vhv_cost: VHV,
        transformer: Callable[[Dict[str, Any]], Dict[str, Any]],
        reverse_transformer: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        civil_language: Optional[str] = None
    ):
        """
        Args:
            action_id: Identificador único
            description: Descripción técnica
            vhv_cost: Costo en VHV de ejecutar esta acción
            transformer: Función que transforma el contexto
            reverse_transformer: Función inversa para retractación
            civil_language: Descripción en lenguaje simple
        """
        self.action_id = action_id
        self.description = description
        self.vhv_cost = vhv_cost
        self.transformer = transformer
        self.reverse_transformer = reverse_transformer
        self.civil_language = civil_language or description
        
        # Historial de ejecuciones para auditoría
        self._execution_log: list = []
    
    def execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Ejecuta la acción sobre el contexto.
        
        Args:
            context: Estado actual
            
        Returns:
            ActionResult con el nuevo estado y VHV consumido
        """
        context_before = copy.deepcopy(context)
        
        try:
            context_after = self.transformer(context)
            
            result = ActionResult(
                success=True,
                action_id=self.action_id,
                vhv_consumed=self.vhv_cost,
                context_before=context_before,
                context_after=context_after
            )
            
            # Registrar para auditoría (T13)
            self._execution_log.append(result)
            
            return result
            
        except Exception as e:
            return ActionResult(
                success=False,
                action_id=self.action_id,
                vhv_consumed=VHV.zero(),  # No se consumió VHV si falló
                context_before=context_before,
                context_after=None,
                error_message=str(e)
            )
    
    def reverse(self, context: Dict[str, Any]) -> ActionResult:
        """
        Ejecuta la acción inversa (para retractación).
        
        Raises:
            ValueError: Si no hay reverse_transformer definido
        """
        if self.reverse_transformer is None:
            raise ValueError(
                f"Acción {self.action_id} no tiene transformer inverso - "
                "viola Invariante 4 (Retractabilidad)"
            )
        
        context_before = copy.deepcopy(context)
        
        try:
            context_after = self.reverse_transformer(context)
            
            return ActionResult(
                success=True,
                action_id=f"{self.action_id}_REVERSE",
                vhv_consumed=VHV.zero(),  # Retractación no consume VHV adicional
                context_before=context_before,
                context_after=context_after
            )
        except Exception as e:
            return ActionResult(
                success=False,
                action_id=f"{self.action_id}_REVERSE",
                vhv_consumed=VHV.zero(),
                context_before=context_before,
                context_after=None,
                error_message=str(e)
            )
    
    def is_reversible(self) -> bool:
        """Retorna True si la acción tiene transformer inverso."""
        return self.reverse_transformer is not None
    
    def get_execution_log(self) -> list:
        """Retorna historial de ejecuciones (T13: Transparencia)."""
        return self._execution_log.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialización para auditoría."""
        return {
            "type": "ActionBlock",
            "action_id": self.action_id,
            "description": self.description,
            "vhv_cost": self.vhv_cost.to_dict(),
            "is_reversible": self.is_reversible(),
            "civil_language": self.civil_language
        }


# --- Acciones Predefinidas ---

class CommonActions:
    """Fábrica de acciones comunes para MaxoContracts."""
    
    @staticmethod
    def transfer_amount(
        from_key: str,
        to_key: str,
        amount_key: str,
        vhv_cost: VHV
    ) -> ActionBlock:
        """Acción: transferir monto de una cuenta a otra."""
        return ActionBlock(
            action_id=f"transfer_{from_key}_to_{to_key}",
            description=f"Transfiere {amount_key} de {from_key} a {to_key}",
            vhv_cost=vhv_cost,
            transformer=lambda ctx: {
                **ctx,
                from_key: ctx[from_key] - ctx[amount_key],
                to_key: ctx[to_key] + ctx[amount_key]
            },
            reverse_transformer=lambda ctx: {
                **ctx,
                from_key: ctx[from_key] + ctx[amount_key],
                to_key: ctx[to_key] - ctx[amount_key]
            },
            civil_language=f"Movemos el monto acordado de {from_key} a {to_key}."
        )
    
    @staticmethod
    def set_flag(
        flag_key: str,
        value: bool = True,
        vhv_cost: VHV = None
    ) -> ActionBlock:
        """Acción: establecer una bandera booleana."""
        return ActionBlock(
            action_id=f"set_flag_{flag_key}",
            description=f"Establece {flag_key} = {value}",
            vhv_cost=vhv_cost or VHV.zero(),
            transformer=lambda ctx: {**ctx, flag_key: value},
            reverse_transformer=lambda ctx: {**ctx, flag_key: not value},
            civil_language=f"Marcamos que {flag_key} está {'activo' if value else 'inactivo'}."
        )
    
    @staticmethod
    def record_timestamp(
        key: str,
        vhv_cost: VHV = None
    ) -> ActionBlock:
        """Acción: registrar timestamp actual."""
        return ActionBlock(
            action_id=f"record_timestamp_{key}",
            description=f"Registra timestamp en {key}",
            vhv_cost=vhv_cost or VHV.zero(),
            transformer=lambda ctx: {**ctx, key: datetime.now(timezone.utc).isoformat()},
            reverse_transformer=lambda ctx: {k: v for k, v in ctx.items() if k != key},
            civil_language=f"Registramos la fecha y hora actual en {key}."
        )
