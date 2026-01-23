"""
Oracle Interface - Base para Oráculos

Define la interfaz común para oráculos sintéticos y humanos.
Alineado con docs/specs/ORACLE_API_SPEC.md
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal


@dataclass
class OracleQuery:
    """Consulta a un oráculo."""
    query_id: str
    query_type: str  # "contract_validation", "retraction_evaluation", "impact_estimation"
    context: Dict[str, Any]
    submitted_at: datetime
    requester_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_id": self.query_id,
            "query_type": self.query_type,
            "requester_id": self.requester_id,
            "submitted_at": self.submitted_at.isoformat(),
            "context": self.context
        }


@dataclass
class Verdict:
    """Veredicto del oráculo (nested object)."""
    approved: bool
    confidence: Decimal
    reasoning: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "approved": self.approved,
            "confidence": float(self.confidence),
            "reasoning": self.reasoning
        }


@dataclass
class OracleResponse:
    """Respuesta de un oráculo."""
    query_id: str
    oracle_id: str
    verdict: Verdict
    metadata: Optional[Dict[str, Any]] = None
    signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_id": self.query_id,
            "oracle_id": self.oracle_id,
            "verdict": self.verdict.to_dict(),
            "metadata": self.metadata or {},
            "signature": self.signature
        }
    
    @property
    def approved(self) -> bool:
        """Helper para compatibilidad."""
        return self.verdict.approved


class OracleInterface(ABC):
    """
    Interfaz base para todos los oráculos.
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
