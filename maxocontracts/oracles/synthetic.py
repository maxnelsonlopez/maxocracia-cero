"""
Synthetic Oracle - Oráculo Sintético Simulado

Implementación de oráculo sintético para testing.
Compatible con ORACLE_API_SPEC.md v1.0
"""

from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal
import uuid
import json

from .base import OracleInterface, OracleQuery, OracleResponse, Verdict


class SyntheticOracle(OracleInterface):
    """
    Oráculo Sintético para MaxoContracts.
    """
    
    def __init__(self, mode: str = "simulation"):
        self.mode = mode
        self._query_log: List[OracleQuery] = []
        self._response_log: List[OracleResponse] = []
        self.oracle_id = "synthetic-v1-sim"
    
    def validate_contract(self, contract_data: Dict[str, Any]) -> OracleResponse:
        """
        Valida un contrato usando heurísticas.
        QueryType: contract_validation
        """
        query = OracleQuery(
            query_id=str(uuid.uuid4()),
            query_type="contract_validation",
            context=contract_data,
            submitted_at=datetime.now(),
            requester_id="system"
        )
        self._query_log.append(query)
        
        if self.mode == "simulation":
            return self._simulate_validation(query, contract_data)
        else:
            raise NotImplementedError("API mode not yet implemented")
    
    def evaluate_retraction(
        self,
        contract_id: str,
        reason: str,
        evidence: Dict[str, Any]
    ) -> OracleResponse:
        """
        Evalúa solicitud de retractación.
        QueryType: retraction_evaluation
        """
        query = OracleQuery(
            query_id=str(uuid.uuid4()),
            query_type="retraction_evaluation",
            context={
                "contract_id": contract_id,
                "reason": reason,
                "evidence": evidence
            },
            submitted_at=datetime.now(),
            requester_id=evidence.get("requester_id", "unknown")
        )
        self._query_log.append(query)
        
        if self.mode == "simulation":
            return self._simulate_retraction_eval(query, reason, evidence)
        else:
            raise NotImplementedError("API mode not yet implemented")
    
    def estimate_gamma_impact(
        self,
        action_data: Dict[str, Any],
        participant_data: Dict[str, Any]
    ) -> Decimal:
        """Estima el impacto en γ de una acción."""
        if self.mode == "simulation":
            # Heurística simple
            vhv = action_data.get("vhv_cost", {})
            v_component = Decimal(str(vhv.get("V", "0")))
            
            if v_component > Decimal("0.5"):
                return Decimal("-0.1")
            elif v_component > Decimal("0.1"):
                return Decimal("-0.05")
            else:
                return Decimal("0.02")
        else:
            raise NotImplementedError("API mode not yet implemented")
    
    def get_oracle_type(self) -> str:
        return "synthetic"
    
    # --- Simulaciones ---
    
    def _simulate_validation(
        self,
        query: OracleQuery,
        contract_data: Dict[str, Any]
    ) -> OracleResponse:
        """Simula validación usando heurísticas."""
        issues = []
        confidence = Decimal("0.9")
        
        # 1. Verificar términos
        terms = contract_data.get("terms", [])
        if len(terms) == 0:
            issues.append("No hay términos definidos (T > 0)")
        
        # 2. Verificar participantes
        participants = contract_data.get("participants", [])
        if len(participants) < 2:
            issues.append("Se requieren al menos 2 participantes")
        
        # Decisión
        is_approved = len(issues) == 0
        
        verdict = Verdict(
            approved=is_approved,
            confidence=confidence,
            reasoning="; ".join(issues) if issues else "Contrato válido axiomáticamente"
        )
        
        response = OracleResponse(
            query_id=query.query_id,
            oracle_id=self.oracle_id,
            verdict=verdict,
            metadata={"simulation_engine": "heuristic_v1"},
            signature=f"sim-sig-{uuid.uuid4().hex[:8]}"
        )
        self._response_log.append(response)
        
        return response
    
    def _simulate_retraction_eval(
        self,
        query: OracleQuery,
        reason: str,
        evidence: Dict[str, Any]
    ) -> OracleResponse:
        """Simula evaluación de retractación."""
        
        approved = False
        confidence = Decimal("0.7")
        final_reason = reason
        
        # Lógica de simulación
        if "gamma_crisis" in reason or "wellness" in str(evidence):
             # Simular aprobación si hay crisis de wellness
             approved = True
             confidence = Decimal("0.9")
             final_reason = "Crisis de Wellness detectada (γ < 1.0)"
        
        verdict = Verdict(
            approved=approved,
            confidence=confidence,
            reasoning=final_reason
        )
        
        response = OracleResponse(
            query_id=query.query_id,
            oracle_id=self.oracle_id,
            verdict=verdict,
            metadata={"evidence_points": len(evidence)},
            signature=f"sim-sig-{uuid.uuid4().hex[:8]}"
        )
        self._response_log.append(response)
        
        return response
