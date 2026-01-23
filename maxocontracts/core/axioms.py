"""
MaxoContracts Axiom Validators

Funciones puras que validan los axiomas temporales y vitales.
Cada función retorna bool y puede ser compuesta.

Referencia: FUNDAMENTOS_CONCEPTUALES.md Sección II.
"""

from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass

from .types import VHV, Gamma, SDV, Participant


@dataclass
class ValidationResult:
    """Resultado de una validación axiomática."""
    is_valid: bool
    axiom_code: str
    axiom_name: str
    message: str
    details: Optional[dict] = None


class AxiomValidator:
    """
    Validador de axiomas para MaxoContracts.
    
    Implementa las verificaciones obligatorias de la Sección II
    del documento de fundamentos conceptuales.
    """
    
    # --- Axiomas Temporales ---
    
    @staticmethod
    def validate_t1_finitud(vhv: VHV) -> ValidationResult:
        """
        T1: Finitud Absoluta
        El TVI consumido debe ser un valor finito positivo.
        """
        is_valid = vhv.T >= Decimal("0") and vhv.T < Decimal("1e12")  # Límite práctico
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="T1",
            axiom_name="Finitud Absoluta",
            message="TVI es finito" if is_valid else "TVI excede límites de finitud",
            details={"T": str(vhv.T)}
        )
    
    @staticmethod
    def validate_t2_igualdad_temporal(
        vhv_participant_a: VHV,
        vhv_participant_b: VHV,
        tolerance_ratio: Decimal = Decimal("0.1")
    ) -> ValidationResult:
        """
        T2: Igualdad Temporal Fundamental
        1 hora TVI tiene igual dignidad para cualquier participante.
        
        Verifica que el intercambio no implique valoración desigual del tiempo.
        """
        if vhv_participant_a.T == Decimal("0") or vhv_participant_b.T == Decimal("0"):
            # Si alguno es cero, no aplica la validación de ratio
            return ValidationResult(
                is_valid=True,
                axiom_code="T2",
                axiom_name="Igualdad Temporal",
                message="No hay intercambio temporal que validar"
            )
        
        # El ratio de tiempo debe estar cerca de 1:1 considerando tolerancia
        ratio = vhv_participant_a.T / vhv_participant_b.T
        is_valid = abs(ratio - Decimal("1.0")) <= tolerance_ratio
        
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="T2",
            axiom_name="Igualdad Temporal",
            message=f"Ratio temporal {ratio:.2f} dentro de tolerancia" if is_valid 
                    else f"Ratio temporal {ratio:.2f} viola igualdad",
            details={"ratio": str(ratio), "tolerance": str(tolerance_ratio)}
        )
    
    @staticmethod
    def validate_t7_minimizar_dano(
        vhv_before: VHV,
        vhv_after: VHV
    ) -> ValidationResult:
        """
        T7: Minimizar Daño
        La acción no debe generar sufrimiento innecesario.
        
        Verifica que V (vidas afectadas) no aumente sin justificación.
        """
        delta_v = vhv_after.V - vhv_before.V
        is_valid = delta_v <= Decimal("0")  # V no debe aumentar
        
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="T7",
            axiom_name="Minimizar Daño",
            message="No hay aumento de vidas afectadas" if is_valid
                    else f"Aumento de {delta_v} UVC detectado",
            details={"delta_V": str(delta_v)}
        )
    
    @staticmethod
    def validate_t9_reciprocidad(
        vhv_giver: VHV,
        vhv_receiver: VHV,
        tolerance: Decimal = Decimal("0.2")
    ) -> ValidationResult:
        """
        T9: Reciprocidad Justa
        El intercambio VHV debe estar balanceado dentro de tolerancia.
        """
        # Calculamos el desbalance relativo en cada dimensión
        total_giver = vhv_giver.T + vhv_giver.V + vhv_giver.R
        total_receiver = vhv_receiver.T + vhv_receiver.V + vhv_receiver.R
        
        if total_giver == Decimal("0") and total_receiver == Decimal("0"):
            return ValidationResult(
                is_valid=True,
                axiom_code="T9",
                axiom_name="Reciprocidad Justa",
                message="Intercambio nulo - recíproco por defecto"
            )
        
        # Evitar división por cero
        max_total = max(total_giver, total_receiver, Decimal("0.001"))
        imbalance = abs(total_giver - total_receiver) / max_total
        
        is_valid = imbalance <= tolerance
        
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="T9",
            axiom_name="Reciprocidad Justa",
            message=f"Desbalance {imbalance:.1%} dentro de tolerancia" if is_valid
                    else f"Desbalance {imbalance:.1%} viola reciprocidad",
            details={
                "imbalance": str(imbalance),
                "tolerance": str(tolerance),
                "giver_total": str(total_giver),
                "receiver_total": str(total_receiver)
            }
        )
    
    @staticmethod
    def validate_t13_transparencia(
        vhv: VHV,
        has_audit_log: bool = True
    ) -> ValidationResult:
        """
        T13: Transparencia Total de Cálculo
        Todo VHV debe ser auditable públicamente.
        """
        is_valid = has_audit_log and vhv.T >= Decimal("0")  # Mínimo: VHV existe
        
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="T13",
            axiom_name="Transparencia",
            message="VHV registrado y auditable" if is_valid
                    else "Falta log de auditoría para VHV"
        )
    
    # --- Invariantes del Sistema ---
    
    @staticmethod
    def validate_invariant_gamma(
        gamma: Gamma,
        threshold: Decimal = Decimal("1.0")
    ) -> ValidationResult:
        """
        Invariante 1: γ ≥ 1 (Bienestar No-Negativo)
        """
        is_valid = gamma.value >= threshold
        
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="INV1",
            axiom_name="Gamma No-Negativo",
            message=f"γ={gamma.value:.2f} ≥ {threshold}" if is_valid
                    else f"γ={gamma.value:.2f} < {threshold} - SUFRIMIENTO",
            details={
                "gamma": str(gamma.value),
                "threshold": str(threshold),
                "severity": gamma.severity()
            }
        )
    
    @staticmethod
    def validate_invariant_sdv(
        participant_sdv: SDV,
        minimum_sdv: SDV
    ) -> ValidationResult:
        """
        Invariante 2: SDV Respetado
        Ningún participante puede caer bajo SDV.
        """
        violations = minimum_sdv.violations(participant_sdv)
        is_valid = len(violations) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            axiom_code="INV2",
            axiom_name="SDV Respetado",
            message="SDV cumplido en todas las dimensiones" if is_valid
                    else f"SDV violado en: {', '.join(violations.keys())}",
            details={"violations": violations} if violations else None
        )
    
    @staticmethod
    def validate_invariant_retractability(
        has_retraction_mechanism: bool = True
    ) -> ValidationResult:
        """
        Invariante 4: Retractabilidad Garantizada
        """
        return ValidationResult(
            is_valid=has_retraction_mechanism,
            axiom_code="INV4",
            axiom_name="Retractabilidad",
            message="Mecanismo de retractación disponible" if has_retraction_mechanism
                    else "CRÍTICO: Sin mecanismo de retractación"
        )
    
    # --- Validación Completa ---
    
    @classmethod
    def validate_all(
        cls,
        vhv: VHV,
        participants: List[Participant],
        minimum_sdv: SDV
    ) -> Tuple[bool, List[ValidationResult]]:
        """
        Ejecuta todas las validaciones obligatorias.
        
        Retorna:
        - bool: True si todas pasan
        - List[ValidationResult]: Resultados detallados
        """
        results = []
        
        # Validar VHV
        results.append(cls.validate_t1_finitud(vhv))
        results.append(cls.validate_t13_transparencia(vhv))
        
        # Validar cada participante
        for participant in participants:
            results.append(cls.validate_invariant_gamma(participant.gamma_current))
            results.append(cls.validate_invariant_sdv(participant.sdv_actual, minimum_sdv))
        
        # Validar retractabilidad
        results.append(cls.validate_invariant_retractability(True))
        
        all_valid = all(r.is_valid for r in results)
        return all_valid, results
    
    @classmethod
    def validate_exchange(
        cls,
        vhv_giver: VHV,
        vhv_receiver: VHV,
        giver: Participant,
        receiver: Participant,
        minimum_sdv: SDV
    ) -> Tuple[bool, List[ValidationResult]]:
        """
        Validación específica para un intercambio entre dos partes.
        """
        results = []
        
        # Axiomas de intercambio
        results.append(cls.validate_t2_igualdad_temporal(vhv_giver, vhv_receiver))
        results.append(cls.validate_t9_reciprocidad(vhv_giver, vhv_receiver))
        
        # Estado de participantes
        results.append(cls.validate_invariant_gamma(giver.gamma_current))
        results.append(cls.validate_invariant_gamma(receiver.gamma_current))
        results.append(cls.validate_invariant_sdv(giver.sdv_actual, minimum_sdv))
        results.append(cls.validate_invariant_sdv(receiver.sdv_actual, minimum_sdv))
        
        all_valid = all(r.is_valid for r in results)
        return all_valid, results
