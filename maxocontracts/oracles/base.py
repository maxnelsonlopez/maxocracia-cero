"""
Oracle Interface - Base para Oráculos

Define la interfaz común para oráculos sintéticos y humanos.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal


@dataclass
class OracleQuery:
    """Consulta a un oráculo."""
    query_id: str
    query_type: str  # "validation", "retraction", "mediation", "estimation"
    context: Dict[str, Any]
    submitted_at: datetime
    requester_id: str


@dataclass
class OracleResponse:
    """Respuesta de un oráculo."""
    query_id: str
    approved: bool
    confidence: Decimal  # 0.0 a 1.0
    reasoning: str
    responded_at: datetime
    oracle_type: str  # "synthetic" o "human"
    metadata: Optional[Dict[str, Any]] = None


class OracleInterface(ABC):
    """
    Interfaz base para todos los oráculos.
    
    Los oráculos tienen dos roles principales:
    1. Validación: Verificar coherencia axiomática
    2. Mediación: Resolver disputas y retractaciones
    """
    
    @abstractmethod
    def validate_contract(
        self,
        contract_data: Dict[str, Any]
    ) -> OracleResponse:
        """Valida un contrato antes de activación."""
        pass
    
    @abstractmethod
    def evaluate_retraction(
        self,
        contract_id: str,
        reason: str,
        evidence: Dict[str, Any]
    ) -> OracleResponse:
        """Evalúa una solicitud de retractación."""
        pass
    
    @abstractmethod
    def estimate_gamma_impact(
        self,
        action_data: Dict[str, Any],
        participant_data: Dict[str, Any]
    ) -> Decimal:
        """Estima el impacto en γ de una acción."""
        pass
    
    @abstractmethod
    def get_oracle_type(self) -> str:
        """Retorna el tipo de oráculo."""
        pass
