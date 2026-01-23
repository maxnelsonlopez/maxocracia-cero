"""
MaxoContract - Contrato Inteligente Ético

Clase principal que orquesta bloques, validación axiomática y ciclo de vida.

Referencia: FUNDAMENTOS_CONCEPTUALES.md
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
import uuid
import json

from .types import VHV, Gamma, SDV, Participant, ContractTerm, ContractState
from .axioms import AxiomValidator, ValidationResult


@dataclass
class ContractEvent:
    """Evento registrado en el log del contrato."""
    event_type: str
    timestamp: datetime
    data: Dict[str, Any]
    actor_id: Optional[str] = None


class MaxoContract:
    """
    Contrato Inteligente Ético - MaxoContract.
    
    Un MaxoContract orquesta bloques de condición, acción, protección γ,
    validación SDV y reciprocidad, garantizando coherencia axiomática
    en todo el ciclo de vida.
    
    Ejemplo de uso:
    ```python
    contract = MaxoContract(
        contract_id="loan-001",
        description="Préstamo de 10 Maxos por 7 días",
        participants=[giver, receiver],
        minimum_sdv=SDV()
    )
    
    contract.add_term(ContractTerm(...))
    contract.validate()  # Valida axiomas
    contract.activate()  # Inicia ejecución
    ```
    """
    
    def __init__(
        self,
        contract_id: Optional[str] = None,
        description: str = "",
        participants: Optional[List[Participant]] = None,
        minimum_sdv: Optional[SDV] = None,
        civil_summary: Optional[str] = None
    ):
        """
        Args:
            contract_id: ID único (se genera si no se proporciona)
            description: Descripción del contrato
            participants: Lista de participantes
            minimum_sdv: Estándar SDV a aplicar
            civil_summary: Resumen en lenguaje civil (≤100 palabras)
        """
        self.contract_id = contract_id or str(uuid.uuid4())
        self.description = description
        self.participants = participants or []
        self.minimum_sdv = minimum_sdv or SDV()
        self.civil_summary = civil_summary or description
        
        # Estado
        self._state = ContractState.DRAFT
        self._created_at = datetime.utcnow()
        self._activated_at: Optional[datetime] = None
        self._completed_at: Optional[datetime] = None
        
        # Términos
        self._terms: List[ContractTerm] = []
        
        # VHV acumulado
        self._total_vhv: VHV = VHV.zero()
        
        # Log de eventos (T13: Transparencia)
        self._event_log: List[ContractEvent] = []
        
        # Resultados de validación
        self._validation_results: List[ValidationResult] = []
        
        # Registrar creación
        self._log_event("contract_created", {"description": description})
    
    # --- Propiedades ---
    
    @property
    def state(self) -> ContractState:
        return self._state
    
    @property
    def is_active(self) -> bool:
        return self._state == ContractState.ACTIVE
    
    @property
    def total_vhv(self) -> VHV:
        return self._total_vhv
    
    @property
    def participant_ids(self) -> List[str]:
        return [p.id for p in self.participants]
    
    # --- Gestión de Términos ---
    
    def add_term(self, term: ContractTerm) -> None:
        """Añade un término al contrato."""
        if self._state != ContractState.DRAFT:
            raise ValueError("Solo se pueden añadir términos en estado DRAFT")
        
        self._terms.append(term)
        self._total_vhv = self._total_vhv + term.vhv_cost
        self._log_event("term_added", {"term_id": term.id, "description": term.description})
    
    def accept_term(self, term_id: str, participant_id: str) -> bool:
        """Registra la aceptación de un término por un participante."""
        for term in self._terms:
            if term.id == term_id:
                term.accepted_by[participant_id] = True
                self._log_event("term_accepted", {
                    "term_id": term_id,
                    "participant_id": participant_id
                })
                return True
        return False
    
    def reject_term(self, term_id: str, participant_id: str, reason: str = "") -> bool:
        """Registra el rechazo de un término."""
        for term in self._terms:
            if term.id == term_id:
                term.accepted_by[participant_id] = False
                self._log_event("term_rejected", {
                    "term_id": term_id,
                    "participant_id": participant_id,
                    "reason": reason
                })
                return True
        return False
    
    def all_terms_accepted(self) -> bool:
        """Verifica si todos los términos fueron aceptados por todos."""
        return all(
            term.is_accepted_by_all(self.participant_ids)
            for term in self._terms
        )
    
    # --- Validación Axiomática ---
    
    def validate(self) -> tuple:
        """
        Ejecuta validación axiomática completa.
        
        Returns:
            (is_valid: bool, results: List[ValidationResult])
        """
        is_valid, results = AxiomValidator.validate_all(
            vhv=self._total_vhv,
            participants=self.participants,
            minimum_sdv=self.minimum_sdv
        )
        
        self._validation_results = results
        self._log_event("validation_executed", {
            "is_valid": is_valid,
            "result_count": len(results),
            "failed": [r.axiom_code for r in results if not r.is_valid]
        })
        
        return is_valid, results
    
    # --- Transiciones de Estado ---
    
    def submit_for_acceptance(self) -> bool:
        """
        Transición: DRAFT → PENDING
        
        Requiere que la validación axiomática pase.
        """
        if self._state != ContractState.DRAFT:
            return False
        
        is_valid, _ = self.validate()
        if not is_valid:
            self._log_event("submission_rejected", {"reason": "axiom_validation_failed"})
            return False
        
        self._state = ContractState.PENDING
        self._log_event("state_changed", {"from": "DRAFT", "to": "PENDING"})
        return True
    
    def activate(self) -> bool:
        """
        Transición: PENDING → ACTIVE
        
        Requiere que todos los términos estén aceptados.
        """
        if self._state != ContractState.PENDING:
            return False
        
        if not self.all_terms_accepted():
            self._log_event("activation_rejected", {"reason": "terms_not_accepted"})
            return False
        
        # Re-validar antes de activar
        is_valid, _ = self.validate()
        if not is_valid:
            self._log_event("activation_rejected", {"reason": "axiom_validation_failed"})
            return False
        
        self._state = ContractState.ACTIVE
        self._activated_at = datetime.utcnow()
        self._log_event("state_changed", {"from": "PENDING", "to": "ACTIVE"})
        return True
    
    def complete(self) -> bool:
        """
        Transición: ACTIVE → EXECUTED
        
        Marca el contrato como completado exitosamente.
        """
        if self._state != ContractState.ACTIVE:
            return False
        
        self._state = ContractState.EXECUTED
        self._completed_at = datetime.utcnow()
        self._log_event("state_changed", {"from": "ACTIVE", "to": "EXECUTED"})
        return True
    
    def retract(self, reason: str, actor_id: str) -> bool:
        """
        Transición: ACTIVE/PENDING → RETRACTED
        
        Protocolo de retractación ética (Invariante 4).
        """
        if self._state not in [ContractState.ACTIVE, ContractState.PENDING]:
            return False
        
        previous_state = self._state.value
        self._state = ContractState.RETRACTED
        self._completed_at = datetime.utcnow()
        
        self._log_event("contract_retracted", {
            "reason": reason,
            "actor_id": actor_id,
            "previous_state": previous_state
        })
        
        return True
    
    # --- Logging (T13: Transparencia) ---
    
    def _log_event(self, event_type: str, data: Dict[str, Any], actor_id: Optional[str] = None):
        """Registra un evento en el log."""
        event = ContractEvent(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            data=data,
            actor_id=actor_id
        )
        self._event_log.append(event)
    
    def get_event_log(self) -> List[ContractEvent]:
        """Retorna copia del log de eventos."""
        return self._event_log.copy()
    
    # --- Serialización ---
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el contrato para auditoría o almacenamiento."""
        return {
            "contract_id": self.contract_id,
            "description": self.description,
            "civil_summary": self.civil_summary,
            "state": self._state.value,
            "created_at": self._created_at.isoformat(),
            "activated_at": self._activated_at.isoformat() if self._activated_at else None,
            "completed_at": self._completed_at.isoformat() if self._completed_at else None,
            "participants": [p.id for p in self.participants],
            "terms": [
                {
                    "id": t.id,
                    "description": t.description,
                    "vhv_cost": t.vhv_cost.to_dict(),
                    "accepted_by": t.accepted_by
                }
                for t in self._terms
            ],
            "total_vhv": self._total_vhv.to_dict(),
            "validation_results": [
                {
                    "axiom": r.axiom_code,
                    "is_valid": r.is_valid,
                    "message": r.message
                }
                for r in self._validation_results
            ],
            "event_log_count": len(self._event_log)
        }
    
    def to_civil_language(self) -> str:
        """
        Genera resumen del contrato en lenguaje civil.
        
        Cumple con requisitos de lenguaje civil:
        - Frases ≤20 palabras
        - Vocabulario grado 8vo
        - Sin jerga técnica
        """
        lines = [
            f"📄 **Contrato**: {self.civil_summary}",
            "",
            f"**Estado**: {self._state.value.upper()}",
            f"**Participantes**: {', '.join(self.participant_ids)}",
            "",
            "**Términos acordados**:"
        ]
        
        for i, term in enumerate(self._terms, 1):
            status = "✓" if term.is_accepted_by_all(self.participant_ids) else "⏳"
            lines.append(f"  {i}. {term.description} {status}")
        
        lines.append("")
        lines.append(f"**Costo total estimado**: {self._total_vhv.T:.1f}h de tiempo")
        
        return "\n".join(lines)
