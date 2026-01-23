"""
MaxoContracts Core Types

Tipos fundamentales con validación axiomática integrada.
Basado en: FUNDAMENTOS_CONCEPTUALES.md y matematicas_maxocracia_compiladas.md

Los tipos aquí definidos representan HECHOS OBJETIVOS (no valoraciones subjetivas).
La valoración en Maxos ocurre en una capa superior usando f(VHV).
"""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class ContractState(Enum):
    """
    Estados válidos de un MaxoContract.
    Ver FUNDAMENTOS_CONCEPTUALES.md Sección IV.
    """
    DRAFT = "draft"           # Creación inicial, no validado
    PENDING = "pending"       # Validado, esperando aceptaciones
    ACTIVE = "active"         # En ejecución
    EXECUTED = "executed"     # Todas las acciones completadas
    PARTIAL = "partial"       # Algunas acciones completadas
    RETRACTED = "retracted"   # Retractado por causa ética


@dataclass(frozen=True)
class VHV:
    """
    Vector de Huella Vital - HECHO OBJETIVO
    
    Representa el costo real de una acción en las tres dimensiones fundamentales.
    Es inmutable una vez calculado (frozen=True).
    
    VHV = [T, V, R] donde:
    - T: Tiempo Vital Indexado (horas TVI)
    - V: Vidas afectadas (UVC ponderadas)
    - R: Recursos finitos consumidos (unidades normalizadas)
    
    Axiomas vinculados:
    - T4: Materialización Temporal (todo es TVI cristalizado)
    - Invariante 3: VHV No Ocultable
    """
    T: Decimal  # Tiempo en horas TVI
    V: Decimal  # Vidas (UVC ponderadas, puede ser fraccional)
    R: Decimal  # Recursos normalizados
    
    def __post_init__(self):
        """Validación de límites físicos."""
        if self.T < 0:
            raise ValueError("T (tiempo) no puede ser negativo - viola T1 (Finitud)")
        if self.V < 0:
            raise ValueError("V (vidas) no puede ser negativo")
        if self.R < 0:
            raise ValueError("R (recursos) no puede ser negativo")
    
    def __add__(self, other: "VHV") -> "VHV":
        """Suma de VHVs (para calcular totales de contratos)."""
        return VHV(
            T=self.T + other.T,
            V=self.V + other.V,
            R=self.R + other.R
        )
    
    def magnitude(self) -> Decimal:
        """Magnitud euclidiana del vector (para comparaciones rápidas)."""
        return (self.T**2 + self.V**2 + self.R**2).sqrt()
    
    def to_dict(self) -> Dict[str, str]:
        """Serialización para logs y auditoría (T13: Transparencia)."""
        return {
            "T": str(self.T),
            "V": str(self.V),
            "R": str(self.R)
        }
    
    @classmethod
    def zero(cls) -> "VHV":
        """VHV nulo para inicialización."""
        return cls(T=Decimal("0"), V=Decimal("0"), R=Decimal("0"))


@dataclass
class Wellness:
    """
    Índice de Bienestar (Wellness)
    
    Escala:
    - Wellness = 0: Sufrimiento máximo
    - Wellness = 1: Neutral (punto de equilibrio)
    - Wellness > 1: Florecimiento
    
    Invariante 1: Wellness ≥ 1 para todos los participantes siempre.
    Si Wellness < 1 sostenido > 14 días, se activa retractación automática.
    
    Axiomas vinculados:
    - T7: Minimizar Daño (Wellness < 1 es daño)
    """
    value: Decimal
    measured_at: datetime = field(default_factory=datetime.utcnow)
    participant_id: Optional[str] = None
    
    def __post_init__(self):
        if self.value < Decimal("0"):
            raise ValueError("Wellness no puede ser negativo")
    
    def is_suffering(self, threshold: Decimal = Decimal("1.0")) -> bool:
        """Retorna True si Wellness está debajo del umbral (sufrimiento)."""
        return self.value < threshold
    
    def is_flourishing(self) -> bool:
        """Retorna True si Wellness > 1 (florecimiento)."""
        return self.value > Decimal("1.0")
    
    def severity(self) -> str:
        """Categoría de severidad para alertas."""
        if self.value >= Decimal("1.2"):
            return "flourishing"
        elif self.value >= Decimal("1.0"):
            return "neutral"
        elif self.value >= Decimal("0.8"):
            return "warning"
        elif self.value >= Decimal("0.5"):
            return "critical"
        else:
            return "emergency"


@dataclass
class SDV:
    """
    Suelo de Dignidad Vital - Estándar Técnico Cuantificable
    
    Define el umbral mínimo por debajo del cual la vida humana
    pierde su integridad biológica y psicológica.
    
    Basado en SDV-H_Suelo_Dignidad_Vital_Humanos.txt
    
    Invariante 2: SDV siempre respetado para todos los participantes.
    """
    # Vivienda
    vivienda_m2: Decimal = Decimal("9.0")  # mínimo m² por persona
    
    # Alimentación
    alimentacion_kcal: Decimal = Decimal("2000")  # kcal/día mínimo
    grupos_alimentarios: int = 5  # grupos distintos/día
    
    # Agua
    agua_litros_dia: Decimal = Decimal("50")  # litros/día mínimo
    agua_distancia_minutos: Decimal = Decimal("30")  # máximo minutos a fuente
    
    # Salud
    salud_acceso_horas: Decimal = Decimal("1.0")  # máximo horas a centro
    gasto_catastrofico_pct: Decimal = Decimal("0")  # meta: 0%
    
    # Educación
    educacion_anos_minimos: int = 12
    
    # Trabajo
    trabajo_horas_semana_max: Decimal = Decimal("48")
    
    # Conexión social
    vinculos_intimos_minimos: int = 2
    
    def meets_minimum(self, actual: "SDV") -> bool:
        """
        Verifica si un SDV actual cumple con este mínimo.
        Retorna False si CUALQUIER dimensión está violada.
        """
        return (
            actual.vivienda_m2 >= self.vivienda_m2 and
            actual.alimentacion_kcal >= self.alimentacion_kcal and
            actual.agua_litros_dia >= self.agua_litros_dia and
            actual.salud_acceso_horas <= self.salud_acceso_horas and
            actual.trabajo_horas_semana_max <= self.trabajo_horas_semana_max
        )
    
    def violations(self, actual: "SDV") -> Dict[str, str]:
        """
        Retorna diccionario de violaciones detectadas.
        Útil para diagnóstico y logs.
        """
        violations = {}
        
        if actual.vivienda_m2 < self.vivienda_m2:
            violations["vivienda"] = f"{actual.vivienda_m2}m² < {self.vivienda_m2}m² mínimo"
        
        if actual.alimentacion_kcal < self.alimentacion_kcal:
            violations["alimentacion"] = f"{actual.alimentacion_kcal}kcal < {self.alimentacion_kcal}kcal mínimo"
        
        if actual.agua_litros_dia < self.agua_litros_dia:
            violations["agua"] = f"{actual.agua_litros_dia}L < {self.agua_litros_dia}L mínimo"
        
        if actual.salud_acceso_horas > self.salud_acceso_horas:
            violations["salud"] = f"{actual.salud_acceso_horas}h > {self.salud_acceso_horas}h máximo"
        
        if actual.trabajo_horas_semana_max > self.trabajo_horas_semana_max:
            violations["trabajo"] = f"{actual.trabajo_horas_semana_max}h > {self.trabajo_horas_semana_max}h máximo"
        
        return violations


@dataclass
class MaxoAmount:
    """
    Cantidad en Maxos - VALOR SOCIAL (no hecho objetivo)
    
    A diferencia del VHV (hecho), el Maxo es la valoración social
    del VHV según la fórmula configurable:
    
    Precio_Maxos = α·T + β·V^γ + δ·R·(FRG × CS)
    
    Este tipo es para representar montos ya calculados.
    """
    amount: Decimal
    calculated_from_vhv: Optional[VHV] = None
    parameters_used: Optional[Dict[str, Decimal]] = None
    
    def __post_init__(self):
        if self.amount < Decimal("0"):
            raise ValueError("Cantidad de Maxos no puede ser negativa")
    
    def __add__(self, other: "MaxoAmount") -> "MaxoAmount":
        return MaxoAmount(amount=self.amount + other.amount)
    
    def __sub__(self, other: "MaxoAmount") -> "MaxoAmount":
        result = self.amount - other.amount
        if result < Decimal("0"):
            raise ValueError("Resultado negativo en sustracción de Maxos")
        return MaxoAmount(amount=result)


@dataclass
class Participant:
    """
    Participante en un MaxoContract.
    
    Cada participante tiene:
    - Identidad única
    - Estado actual de SDV
    - Historial de Wellness
    - Balance VHV
    """
    id: str
    name: str
    sdv_actual: SDV = field(default_factory=SDV)
    wellness_current: Wellness = field(default_factory=lambda: Wellness(value=Decimal("1.0")))
    vhv_balance: VHV = field(default_factory=VHV.zero)
    
    def update_wellness(self, new_value: Decimal) -> None:
        """Actualiza Wellness con timestamp."""
        self.wellness_current = Wellness(
            value=new_value,
            participant_id=self.id
        )
    
    def is_in_good_standing(self, sdv_minimum: SDV) -> bool:
        """Verifica que el participante está en buen estado (Wellness ≥ 1, SDV met)."""
        return (
            not self.wellness_current.is_suffering() and
            sdv_minimum.meets_minimum(self.sdv_actual)
        )


@dataclass
class ContractTerm:
    """
    Término individual de un MaxoContract.
    
    Los términos son aceptados/rechazados individualmente
    (Aceptación Término-a-Término, no "todo o nada").
    """
    id: str
    description: str  # Lenguaje civil, ≤20 palabras
    vhv_cost: VHV
    accepted_by: Dict[str, bool] = field(default_factory=dict)
    
    def is_accepted_by_all(self, participant_ids: list) -> bool:
        """Verifica si todos los participantes aceptaron este término."""
        return all(
            self.accepted_by.get(pid, False)
            for pid in participant_ids
        )
    
    def acceptance_status(self, participant_ids: list) -> Dict[str, str]:
        """Retorna estado de aceptación por participante."""
        return {
            pid: "accepted" if self.accepted_by.get(pid, False) else "pending"
            for pid in participant_ids
        }
