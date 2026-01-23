"""
Synthetic Oracle - Oráculo Sintético Simulado

Implementación de oráculo sintético para testing.
En producción, se conectaría a Claude API u otro LLM.
"""

from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal
import uuid

from .base import OracleInterface, OracleQuery, OracleResponse


class SyntheticOracle(OracleInterface):
    """
    Oráculo Sintético para MaxoContracts.
    
    En modo simulación (default), usa heurísticas simples.
    Para producción, conectar a Claude API.
    
    Ejemplo de uso:
    ```python
    oracle = SyntheticOracle(mode="simulation")
    
    response = oracle.validate_contract(contract.to_dict())
    if response.approved:
        contract.activate()
    ```
    """
    
    def __init__(self, mode: str = "simulation"):
        """
        Args:
            mode: "simulation" para testing, "api" para producción
        """
        self.mode = mode
        self._query_log: List[OracleQuery] = []
        self._response_log: List[OracleResponse] = []
    
    def validate_contract(self, contract_data: Dict[str, Any]) -> OracleResponse:
        """
        Valida un contrato usando heurísticas o LLM.
        
        Verificaciones:
        1. Todos los términos tienen VHV registrado
        2. No hay violaciones axiomáticas conocidas
        3. El lenguaje es civil (no ofuscado)
        """
        query = OracleQuery(
            query_id=str(uuid.uuid4()),
            query_type="validation",
            context=contract_data,
            submitted_at=datetime.utcnow(),
            requester_id="system"
        )
        self._query_log.append(query)
        
        if self.mode == "simulation":
            return self._simulate_validation(query, contract_data)
        else:
            # Placeholder para integración con API real
            raise NotImplementedError("API mode not yet implemented")
    
    def evaluate_retraction(
        self,
        contract_id: str,
        reason: str,
        evidence: Dict[str, Any]
    ) -> OracleResponse:
        """
        Evalúa solicitud de retractación.
        
        Criterios de aprobación:
        - γ < 1.0 sostenido (sufrimiento)
        - SDV violado como consecuencia
        - Evidencia de manipulación
        """
        query = OracleQuery(
            query_id=str(uuid.uuid4()),
            query_type="retraction",
            context={
                "contract_id": contract_id,
                "reason": reason,
                "evidence": evidence
            },
            submitted_at=datetime.utcnow(),
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
        """
        Estima el impacto en γ de una acción.
        
        Retorna delta_gamma estimado (puede ser negativo).
        """
        if self.mode == "simulation":
            # Heurística simple: acciones con alto VHV.V tienen impacto negativo
            vhv = action_data.get("vhv_cost", {})
            v_component = Decimal(str(vhv.get("V", "0")))
            
            # V alto → impacto negativo en γ
            if v_component > Decimal("0.5"):
                return Decimal("-0.1")
            elif v_component > Decimal("0.1"):
                return Decimal("-0.05")
            else:
                return Decimal("0.02")  # Acciones ligeras pueden mejorar γ
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
        
        # Verificar que hay términos
        terms = contract_data.get("terms", [])
        if len(terms) == 0:
            issues.append("No hay términos definidos")
        
        # Verificar VHV en cada término
        for term in terms:
            if not term.get("vhv_cost"):
                issues.append(f"Término {term.get('id')} sin VHV")
        
        # Verificar participantes
        participants = contract_data.get("participants", [])
        if len(participants) < 2:
            issues.append("Se requieren al menos 2 participantes")
        
        # Verificar resultados de validación previos
        validation_results = contract_data.get("validation_results", [])
        failed_axioms = [r for r in validation_results if not r.get("is_valid")]
        if failed_axioms:
            issues.append(f"Axiomas fallidos: {[r['axiom'] for r in failed_axioms]}")
            confidence = Decimal("0.5")
        
        approved = len(issues) == 0
        
        response = OracleResponse(
            query_id=query.query_id,
            approved=approved,
            confidence=confidence,
            reasoning="; ".join(issues) if issues else "Contrato válido axiomáticamente",
            responded_at=datetime.utcnow(),
            oracle_type="synthetic"
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
        
        # Criterios de aprobación automática
        auto_approve_reasons = [
            "gamma_below_threshold",
            "sdv_violated",
            "manipulation_detected",
            "new_vital_facts"
        ]
        
        # Verificar γ en evidencia
        gamma_value = evidence.get("current_gamma", Decimal("1.0"))
        if isinstance(gamma_value, str):
            gamma_value = Decimal(gamma_value)
        
        # Decisión
        approved = False
        confidence = Decimal("0.7")
        
        if reason in auto_approve_reasons:
            approved = True
            confidence = Decimal("0.85")
        elif gamma_value < Decimal("0.8"):
            approved = True
            confidence = Decimal("0.9")
            reason = f"γ={gamma_value} < 0.8 (sufrimiento crítico)"
        elif gamma_value < Decimal("1.0"):
            approved = True  # γ < 1 siempre aprueba retractación
            confidence = Decimal("0.8")
        
        response = OracleResponse(
            query_id=query.query_id,
            approved=approved,
            confidence=confidence,
            reasoning=f"Retractación {'aprobada' if approved else 'rechazada'}: {reason}",
            responded_at=datetime.utcnow(),
            oracle_type="synthetic",
            metadata={"gamma_evaluated": str(gamma_value)}
        )
        self._response_log.append(response)
        
        return response
    
    def get_query_log(self) -> List[OracleQuery]:
        """Retorna historial de consultas (T13)."""
        return self._query_log.copy()
    
    def get_response_log(self) -> List[OracleResponse]:
        """Retorna historial de respuestas (T13)."""
        return self._response_log.copy()
