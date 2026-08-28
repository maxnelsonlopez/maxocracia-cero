# -*- coding: utf-8 -*-
"""
Regla de oro de la Vacuación y triada de verificación — rama educativa.

La vacuación es la regla de oro del aprendizaje maxocrático (OEV §1.7,
Educación Siamesa §3g): el skill se gana produciendo material de enseñanza
y mentoría a nuevos aprendices — *la validación es la transferencia*.
"Vacua" el skill quien lo enseña.

La validación se hace en tres capas (siamesa §2c): hecho (obra aplicada
verificable) + opinión (peso ganado por precisión) + credencial (doble
libro transicional). Para software, la capa de opinión se materializa en la
**triada**: mentor (facilitador) + par (aprendiz) + oráculo con veto. Todo
verificador es verificable: rotación, veto y disidente (siamesa §3e).

Este módulo es puro (sin Flask, sin BD): las decisiones se calculan aquí y
la capa app solo persiste el resultado con su trazabilidad (T13).
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class VacuacionRequirements:
    """Requisitos mínimos de la regla de oro (canon editable por el parlamento)."""

    obra_requerida: bool = True
    material_requerido: bool = True
    mentoria_min_horas: float = 1.0


DEFAULT_VACUACION_REQUIREMENTS = VacuacionRequirements()


@dataclass(frozen=True)
class VacuacionResult:
    """Veredicto de la regla de oro: vacua (true) si no falta ningún requisito."""

    vacua: bool
    faltantes: List[str] = field(default_factory=list)
    razones: List[str] = field(default_factory=list)


def evaluate_vacuacion(
    obra_aplicada: bool,
    material_publicado: bool,
    mentoria_horas: float,
    requirements: VacuacionRequirements = DEFAULT_VACUACION_REQUIREMENTS,
) -> VacuacionResult:
    """Evalúa la regla de oro (el skill se gana enseñándolo).

    - obra_aplicada: competencia demostrada en obra / enseñanza / proyecto
      real con la comunidad (hecho verificable, no opinión de autoridad).
    - material_publicado: material de enseñanza abierto y forkable.
    - mentoria_horas: mentoría a nuevos aprendices, contada en TVI.
    """
    faltantes: List[str] = []
    razones: List[str] = []

    if requirements.obra_requerida and not obra_aplicada:
        faltantes.append("obra aplicada")
    if requirements.material_requerido and not material_publicado:
        faltantes.append("material de enseñanza publicado")
    if mentoria_horas < requirements.mentoria_min_horas:
        faltantes.append(
            f"mentoría mínima ({requirements.mentoria_min_horas:g} h de TVI)"
        )

    if not faltantes:
        razones.append(
            "obra aplicada + material publicado + mentoría registrada: "
            "la validación es la transferencia"
        )
    return VacuacionResult(vacua=not faltantes, faltantes=faltantes, razones=razones)


@dataclass(frozen=True)
class TriadaVotos:
    """Votos de la triada de verificación (siamesa §2c)."""

    mentor_ok: bool = False
    peer_ok: bool = False
    oracle_veto: bool = False  # el oráculo tiene veto, no voto


@dataclass(frozen=True)
class TriadaResult:
    """Veredicto de la triada: aprobada si mentor y par aprueban y no hay veto.

    El oráculo con veto no sustituye a los humanos: los humanos custodian el
    sentido; el sintético protege los axiomas (Cap. 14.9).
    """

    aprobada: bool
    bloqueos: List[str] = field(default_factory=list)
    razones: List[str] = field(default_factory=list)


def evaluate_triada(votos: TriadaVotos) -> TriadaResult:
    """Aplica la triada: mentor + par + oráculo con veto (rotación y disidente)."""
    bloqueos: List[str] = []
    razones: List[str] = []

    if not votos.mentor_ok:
        bloqueos.append("el mentor (facilitador) no avala")
    if not votos.peer_ok:
        bloqueos.append("el par no avala")
    if votos.oracle_veto:
        bloqueos.append("el oráculo ejerció el veto (axiomas en riesgo)")

    if not bloqueos:
        razones.append("triada completa: mentor + par aprueban, oráculo sin veto")
    return TriadaResult(aprobada=not bloqueos, bloqueos=bloqueos, razones=razones)


def evaluar_concesion(
    obra_aplicada: bool,
    material_publicado: bool,
    mentoria_horas: float,
    votos: TriadaVotos,
    requirements: VacuacionRequirements = DEFAULT_VACUACION_REQUIREMENTS,
) -> dict:
    """Evaluación completa de una concesión de skill (regla de oro + triada).

    Devuelve el veredicto canónico de la capa app (serializable):
    - "awarded": regla de oro cumplida Y triada aprobada -> el skill vacua.
    - "awaiting_triada": regla de oro cumplida, triada incompleta.
    - "rejected": la regla de oro no se cumple (faltantes) o hay veto.
    """
    vacua = evaluate_vacuacion(obra_aplicada, material_publicado, mentoria_horas, requirements)
    triada = evaluate_triada(votos)

    if not vacua.vacua:
        outcome = "rejected"
    elif not triada.aprobada:
        outcome = "awaiting_triada"
    else:
        outcome = "awarded"

    return {
        "outcome": outcome,
        "vacua": {
            "cumplida": vacua.vacua,
            "faltantes": vacua.faltantes,
            "razones": vacua.razones,
        },
        "triada": {
            "aprobada": triada.aprobada,
            "bloqueos": triada.bloqueos,
            "razones": triada.razones,
        },
    }
