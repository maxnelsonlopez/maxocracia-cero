"""
SDV Analyzer — Estimación cualitativa del Suelo de Dignidad Vital.

Analiza los registros de participantes (Formulario CERO) y sus seguimientos
(Formulario B) para estimar el cumplimiento de las 7 dimensiones del SDV.

Este analizador traduce datos cualitativos en una métrica de 0.0 a 1.0:
- 1.0: Plenamente cubierto (Dignidad)
- 0.7: Alerta / Vulnerabilidad
- < 0.5: Violación probable del SDV
"""

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class SDVScore:
    """Puntuación estimada para las 7 dimensiones del SDV."""

    vivienda: float = 1.0
    alimentacion: float = 1.0
    agua: float = 1.0
    salud: float = 1.0
    educacion: float = 1.0
    trabajo: float = 1.0
    vinculos: float = 1.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "vivienda": self.vivienda,
            "alimentacion": self.alimentacion,
            "agua": self.agua,
            "salud": self.salud,
            "educacion": self.educacion,
            "trabajo": self.trabajo,
            "vinculos": self.vinculos,
        }

    def average(self) -> float:
        scores = [
            self.vivienda,
            self.alimentacion,
            self.agua,
            self.salud,
            self.educacion,
            self.trabajo,
            self.vinculos,
        ]
        return sum(scores) / len(scores)


class SDVAnalyzer:
    """
    Analizador de Suelo de Dignidad Vital para la Cohorte Cero.
    """

    # Mapeo de Dimensiones Humanas (Forms) a Dimensiones SDV (Teoría)
    DIMENSION_MAPPING = {
        "crecimiento_aprendizaje": ["educacion"],
        "bienestar_descanso": ["salud", "vivienda"],
        "seguridad_estabilidad": ["vivienda", "trabajo"],
        "autoestima_autonomia": ["salud"],
        "conexion_social": ["vinculos"],
        "prosperidad_recursos": ["alimentacion", "agua", "trabajo"],
        "placer_goce": ["salud"],
        "intimidad_vinculos": ["vinculos"],
    }

    URGENCY_PENALTY = {
        "Alta": 0.3,
        "Media": 0.15,
        "Baja": 0.05,
    }

    NARRATIVE_TEMPLATES = {
        "vivienda": {
            "plenitud": "Condiciones de habitabilidad estables y seguras. El entorno protege la vida.",
            "riesgo": "Vulnerabilidad detectada en la estabilidad del hogar o calidad del entorno habitacional.",
            "violacion": "⚠️ Emergencia habitacional. El espacio actual compromete la dignidad o seguridad.",
        },
        "alimentacion": {
            "plenitud": "Seguridad alimentaria garantizada. Nutrición suficiente y estable.",
            "riesgo": "Inestabilidad en el acceso a alimentos de calidad o frecuencia nutricional.",
            "violacion": "⚠️ Alerta nutricional. Insuficiencia alimentaria que requiere intervención inmediata.",
        },
        "agua": {
            "plenitud": "Acceso pleno a agua potable y saneamiento básico.",
            "riesgo": "Limitaciones en la calidad o regularidad del suministro de agua.",
            "violacion": "⚠️ Privación de agua potable. Riesgo sanitario crítico detectado.",
        },
        "salud": {
            "plenitud": "Bienestar físico y mental preservado. Acceso efectivo a cuidados.",
            "riesgo": "Barreras en el acceso a salud o signos de fragilidad en el bienestar.",
            "violacion": "⚠️ Quebranto vital. Situación de salud sin atención que impide la vida plena.",
        },
        "educacion": {
            "plenitud": "Crecimiento continuo. Acceso a herramientas de conocimiento y desarrollo.",
            "riesgo": "Estancamiento en el desarrollo de capacidades o acceso limitado a formación.",
            "violacion": "⚠️ Exclusión cognitiva. Falta de herramientas básicas para la autonomía social.",
        },
        "trabajo": {
            "plenitud": "Labor digna y equilibrada. Reciprocidad justa por el tiempo vital.",
            "riesgo": "Precarización o desequilibrio entre esfuerzo vital y retorno obtenido.",
            "violacion": "⚠️ Explotación o desempleo crítico. El tiempo vital se consume sin retorno digno.",
        },
        "vinculos": {
            "plenitud": "Red de afectos y apoyo comunitario sólida. Conexión social activa.",
            "riesgo": "Aislamiento relativo o fragilidad en los lazos de apoyo mutuo.",
            "violacion": "⚠️ Soledad sistémica. Ausencia de red de soporte en momentos de necesidad.",
        },
    }

    def __init__(self, db_connection: sqlite3.Connection):
        self.conn = db_connection

    def _parse_json(self, raw: Optional[str]) -> List[str]:
        if not raw:
            return []
        try:
            result = json.loads(raw)
            return result if isinstance(result, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def generate_narrative(self, scores: SDVScore) -> Dict[str, str]:
        """Genera frases humanas basadas en los puntajes SDV."""
        narratives = {}
        for dim, templates in self.NARRATIVE_TEMPLATES.items():
            score = getattr(scores, dim)
            if score >= 0.9:
                narratives[dim] = templates["plenitud"]
            elif score >= 0.5:
                narratives[dim] = templates["riesgo"]
            else:
                narratives[dim] = templates["violacion"]
        return narratives

    def get_participant_analysis(self, participant_id: int) -> Dict[str, Any]:
        """Retorna el análisis completo (scores + narrativa) de un participante."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM participants WHERE id = ?", (participant_id,))
        row = cursor.fetchone()
        name = row[0] if row else "Participante Desconocido"

        scores = self.estimate_participant_sdv(participant_id)
        narratives = self.generate_narrative(scores)

        return {
            "participant_id": participant_id,
            "participant_name": name,
            "sdv_scores": scores.to_dict(),
            "average_score": scores.average(),
            "narratives": narratives,
            "timestamp": datetime.now().isoformat(),
        }

    def estimate_participant_sdv(self, participant_id: int) -> SDVScore:
        """
        Calcula la estimación SDV actual de un participante.

        Lógica:
        1. Parte de 1.0 en todas las dimensiones.
        2. Resta penalizaciones según necesidades registradas en Form Cero.
        3. Ajusta según el historial de Seguimientos (Form B).
        4. (Opcional futuro) Mejora según intercambios exitosos recibidos.
        """
        cursor = self.conn.cursor()

        # 1. Obtener datos del participante
        cursor.execute(
            "SELECT need_human_dimensions, need_urgency FROM participants WHERE id = ?",
            (participant_id,),
        )
        p_row = cursor.fetchone()
        if not p_row:
            return SDVScore()

        need_dims = self._parse_json(p_row[0])
        urgency = p_row[1]

        score = SDVScore()

        # 2. Penalizar según necesidades iniciales
        penalty = self.URGENCY_PENALTY.get(urgency, 0.05)
        for dim in need_dims:
            sdv_targets = self.DIMENSION_MAPPING.get(dim, [])
            for target in sdv_targets:
                current_val = getattr(score, target)
                setattr(score, target, max(0.0, current_val - penalty))

        # 3. Analizar Seguimientos (Form B) - El más reciente pesa más
        cursor.execute(
            """
            SELECT need_level, current_situation FROM follow_ups 
            WHERE participant_id = ? 
            ORDER BY follow_up_date DESC LIMIT 3
            """,
            (participant_id,),
        )
        followups = cursor.fetchall()

        if followups:
            # Solo usamos el más reciente para la estimación de "estado actual"
            latest_level = followups[0][0]  # 1-5
            if latest_level:
                # Si el nivel de necesidad es alto (4-5), aplicamos penalización extra global
                # a las dimensiones afectadas inicialmente
                extra_penalty = (latest_level - 1) * 0.15  # 1=0, 5=0.6
                for dim in need_dims:
                    sdv_targets = self.DIMENSION_MAPPING.get(dim, [])
                    for target in sdv_targets:
                        current_val = getattr(score, target)
                        # Sobrescribimos o profundizamos la penalización
                        setattr(score, target, max(0.1, 1.0 - extra_penalty))

        # 4. Normalizar: no dejar que suba de 1.0 ni baje de 0.1 (mínimo vital teórico)
        for target in [
            "vivienda",
            "alimentacion",
            "agua",
            "salud",
            "educacion",
            "trabajo",
            "vinculos",
        ]:
            val = getattr(score, target)
            setattr(score, target, round(min(1.0, max(0.1, val)), 2))

        return score

    def get_community_sdv_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado promedio de SDV de toda la comunidad activa.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM participants WHERE status = 'active'")
        participant_ids = [row[0] for row in cursor.fetchall()]

        if not participant_ids:
            return {
                "average_score": 1.0,
                "dimensions": SDVScore().to_dict(),
                "count": 0,
            }

        total_scores = {
            "vivienda": 0.0,
            "alimentacion": 0.0,
            "agua": 0.0,
            "salud": 0.0,
            "educacion": 0.0,
            "trabajo": 0.0,
            "vinculos": 0.0,
        }

        for p_id in participant_ids:
            p_score = self.estimate_participant_sdv(p_id)
            for k in total_scores:
                total_scores[k] += getattr(p_score, k)

        count = len(participant_ids)
        avg_dimensions = {k: round(v / count, 2) for k, v in total_scores.items()}

        return {
            "average_overall": round(sum(avg_dimensions.values()) / 7, 2),
            "dimensions": avg_dimensions,
            "participant_count": count,
        }
