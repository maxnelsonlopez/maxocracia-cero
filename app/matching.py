"""
Matching Engine — Motor de Emparejamiento de la Cohorte Cero.

Cruza las ofertas y necesidades de los participantes para sugerir
intercambios que cubran el Suelo de Dignidad Vital (SDV) de la comunidad.

Principios Maxocracia aplicados:
- Prioridad absoluta a necesidades de urgencia Alta (posible violación SDV).
- Un participante con need_level=5 (crítico) activa Alerta de Coherencia.
- El matching excluye pares recientes para estimular diversidad de red.
- La localidad (barrio/ciudad) se pondera para facilitar el intercambio real.
"""

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


# ──────────────────────────────────────────────────────────────────
# Pesos y configuración del algoritmo
# ──────────────────────────────────────────────────────────────────

URGENCY_WEIGHTS = {
    "Alta": 1.0,
    "Media": 0.5,
    "Baja": 0.2,
}

RECENT_EXCHANGE_DAYS = 7          # Días tras los cuales un par se considera "reciente"
CRITICAL_NEED_LEVEL = 5           # need_level en follow_ups que activa Alerta de Coherencia
UNRESOLVED_DAYS_THRESHOLD = 7     # Días sin intercambio para una urgencia Alta = alerta


# ──────────────────────────────────────────────────────────────────
# Tipos de retorno
# ──────────────────────────────────────────────────────────────────

@dataclass
class MatchResult:
    """Resultado de emparejamiento entre un buscador y un potencial oferente."""
    offerer_id: int
    offerer_name: str
    offerer_city: str
    offerer_neighborhood: str
    offerer_phone_whatsapp: Optional[str]
    offerer_telegram: Optional[str]
    matched_categories: List[str]         # Categorías en común
    offerer_description: str              # Descripción de lo que ofrece
    offerer_dimensions: List[str]         # Dimensiones humanas que cubre
    compatibility_score: float            # 0.0 – 1.0
    urgency_weight: float                 # Peso por urgencia del buscador
    same_city: bool
    same_neighborhood: bool
    recently_exchanged: bool              # True si ya hubo intercambio reciente


@dataclass
class UrgentNeed:
    """Participante con necesidad urgente sin resolver."""
    participant_id: int
    participant_name: str
    city: str
    neighborhood: str
    need_description: str
    need_urgency: str                     # "Alta" siempre en esta lista
    need_categories: List[str]
    need_dimensions: List[str]
    days_without_exchange: int            # Cuántos días lleva sin un intercambio
    latest_need_level: Optional[int]      # Del follow-up más reciente (1-5)
    is_coherence_crime: bool              # True si need_level == 5
    top_matches: List[MatchResult] = field(default_factory=list)


@dataclass
class CommunityGap:
    """Brecha de cobertura de una dimensión humana en la comunidad."""
    dimension: str
    dimension_label: str                  # Nombre legible
    participants_needing: int
    participants_offering: int
    coverage_ratio: float                 # offering / needing (< 1 = déficit)
    gap_severity: str                     # "critical" | "warning" | "ok"


# ──────────────────────────────────────────────────────────────────
# Motor de Matching
# ──────────────────────────────────────────────────────────────────

class MatchingEngine:
    """
    Motor principal de emparejamiento de la Cohorte Cero.

    Uso típico:
        engine = MatchingEngine(db_connection)
        matches = engine.find_matches(seeker_id=3)
        urgent  = engine.get_urgent_unmet_needs()
        gaps    = engine.get_community_sdv_gaps()
    """

    DIMENSION_LABELS: Dict[str, str] = {
        "crecimiento_aprendizaje":  "Educación / Aprendizaje",
        "bienestar_descanso":       "Bienestar y Descanso",
        "seguridad_estabilidad":    "Seguridad y Estabilidad",
        "autoestima_autonomia":     "Autonomía / Autoestima",
        "conexion_social":          "Conexión Social",
        "prosperidad_recursos":     "Recursos / Subsistencia",
        "placer_goce":              "Placer y Goce",
        "intimidad_vinculos":       "Vínculos Íntimos",
    }

    def __init__(self, db_connection: sqlite3.Connection):
        self.conn = db_connection

    # ── Helpers ────────────────────────────────────────────────────

    def _parse_json(self, raw: Optional[str]) -> List[str]:
        """Parsea un campo JSON almacenado como texto; retorna lista vacía si falla."""
        if not raw:
            return []
        try:
            result = json.loads(raw)
            return result if isinstance(result, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def _get_recent_exchange_partners(
        self, participant_id: int, days: int = RECENT_EXCHANGE_DAYS
    ) -> set:
        """
        Retorna IDs de participantes con quienes ya hubo intercambio
        en los últimos `days` días (en cualquier dirección).
        """
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT
                CASE WHEN giver_id = ? THEN receiver_id ELSE giver_id END AS partner
            FROM interchange
            WHERE (giver_id = ? OR receiver_id = ?)
              AND date >= ?
            """,
            (participant_id, participant_id, participant_id, cutoff),
        )
        return {row[0] for row in cursor.fetchall() if row[0] is not None}

    def _get_latest_need_level(self, participant_id: int) -> Optional[int]:
        """Retorna el need_level del follow-up más reciente del participante."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT need_level FROM follow_ups
            WHERE participant_id = ?
              AND need_level IS NOT NULL
            ORDER BY follow_up_date DESC
            LIMIT 1
            """,
            (participant_id,),
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def _days_since_last_exchange(self, participant_id: int) -> int:
        """
        Cuántos días han pasado desde el último intercambio del participante
        (como giver o receiver). Retorna 9999 si nunca hubo intercambio.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT MAX(date) FROM interchange
            WHERE giver_id = ? OR receiver_id = ?
            """,
            (participant_id, participant_id),
        )
        row = cursor.fetchone()
        if not row or not row[0]:
            return 9999
        try:
            last_date = datetime.strptime(row[0][:10], "%Y-%m-%d")
            return (datetime.now() - last_date).days
        except ValueError:
            return 9999

    # ── API pública ────────────────────────────────────────────────

    def find_matches(
        self,
        seeker_id: int,
        limit: int = 10,
        exclude_recent: bool = True,
    ) -> List[MatchResult]:
        """
        Encuentra los mejores oferentes para las necesidades de `seeker_id`.

        Fórmula de score:
            score = overlap_score * 0.6
                  + urgency_weight * 0.3
                  + proximity_score * 0.1

        donde:
            overlap_score   = len(categorías_en_común) / len(categorías_necesitadas)
            urgency_weight  = URGENCY_WEIGHTS[seeker.need_urgency]
            proximity_score = 1.0 si mismo barrio, 0.5 si misma ciudad, 0.0 en otro caso
        """
        cursor = self.conn.cursor()

        # Cargar el buscador
        cursor.execute(
            "SELECT * FROM participants WHERE id = ? AND status = 'active'",
            (seeker_id,),
        )
        row = cursor.fetchone()
        if not row:
            return []

        seeker = dict(zip([d[0] for d in cursor.description], row))
        need_cats = self._parse_json(seeker.get("need_categories"))
        urgency_w = URGENCY_WEIGHTS.get(seeker.get("need_urgency", "Baja"), 0.2)

        if not need_cats:
            return []

        recent_partners = (
            self._get_recent_exchange_partners(seeker_id)
            if exclude_recent
            else set()
        )

        # Candidatos: todos los activos excepto el propio buscador
        cursor.execute(
            """
            SELECT id, name, city, neighborhood, phone_whatsapp, telegram_handle,
                   offer_categories, offer_description, offer_human_dimensions
            FROM participants
            WHERE status = 'active'
              AND id != ?
            """,
            (seeker_id,),
        )

        results: List[MatchResult] = []
        for cand_row in cursor.fetchall():
            cand = dict(zip([d[0] for d in cursor.description], cand_row))
            offer_cats = self._parse_json(cand.get("offer_categories"))

            if not offer_cats:
                continue

            matched = [c for c in need_cats if c in offer_cats]
            if not matched:
                continue

            overlap = len(matched) / max(len(need_cats), 1)

            same_neighborhood = (
                seeker.get("neighborhood", "").lower().strip()
                == cand["neighborhood"].lower().strip()
                and seeker.get("city", "").lower().strip()
                == cand["city"].lower().strip()
            )
            same_city = (
                seeker.get("city", "").lower().strip()
                == cand["city"].lower().strip()
            )
            proximity = 1.0 if same_neighborhood else (0.5 if same_city else 0.0)

            score = overlap * 0.6 + urgency_w * 0.3 + proximity * 0.1

            results.append(
                MatchResult(
                    offerer_id=cand["id"],
                    offerer_name=cand["name"],
                    offerer_city=cand["city"],
                    offerer_neighborhood=cand["neighborhood"],
                    offerer_phone_whatsapp=cand.get("phone_whatsapp"),
                    offerer_telegram=cand.get("telegram_handle"),
                    matched_categories=matched,
                    offerer_description=cand.get("offer_description", ""),
                    offerer_dimensions=self._parse_json(
                        cand.get("offer_human_dimensions")
                    ),
                    compatibility_score=round(score, 4),
                    urgency_weight=urgency_w,
                    same_city=same_city,
                    same_neighborhood=same_neighborhood,
                    recently_exchanged=cand["id"] in recent_partners,
                )
            )

        results.sort(key=lambda r: r.compatibility_score, reverse=True)
        return results[:limit]

    def get_urgent_unmet_needs(
        self, days_threshold: int = UNRESOLVED_DAYS_THRESHOLD, top_matches: int = 3
    ) -> List[UrgentNeed]:
        """
        Retorna todos los participantes con:
          - need_urgency = 'Alta'
          - Sin intercambio reciente (> days_threshold días)

        Para cada uno, incluye sus mejores matches y detecta
        si hay una posible violación SDV (Crimen de Coherencia).

        Orden: need_level crítico primero, luego por días sin intercambio.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, name, city, neighborhood, need_description,
                   need_urgency, need_categories, need_human_dimensions
            FROM participants
            WHERE status = 'active'
              AND need_urgency = 'Alta'
            """,
        )

        urgent_needs: List[UrgentNeed] = []
        for row in cursor.fetchall():
            p = dict(zip([d[0] for d in cursor.description], row))
            days_without = self._days_since_last_exchange(p["id"])

            if days_without < days_threshold:
                continue

            latest_level = self._get_latest_need_level(p["id"])
            is_crime = latest_level is not None and latest_level >= CRITICAL_NEED_LEVEL

            matches = self.find_matches(p["id"], limit=top_matches, exclude_recent=False)

            urgent_needs.append(
                UrgentNeed(
                    participant_id=p["id"],
                    participant_name=p["name"],
                    city=p["city"],
                    neighborhood=p["neighborhood"],
                    need_description=p.get("need_description", ""),
                    need_urgency=p["need_urgency"],
                    need_categories=self._parse_json(p.get("need_categories")),
                    need_dimensions=self._parse_json(p.get("need_human_dimensions")),
                    days_without_exchange=days_without,
                    latest_need_level=latest_level,
                    is_coherence_crime=is_crime,
                    top_matches=matches,
                )
            )

        # Crímenes de Coherencia primero, luego por días sin intercambio
        urgent_needs.sort(
            key=lambda n: (not n.is_coherence_crime, -n.days_without_exchange)
        )
        return urgent_needs

    def get_community_sdv_gaps(self) -> List[CommunityGap]:
        """
        Analiza brechas de cobertura por dimensión humana en toda la comunidad.

        Para cada dimensión calcula:
            coverage_ratio = participantes_que_ofrecen / participantes_que_necesitan

        Un ratio < 0.5 es "critical", < 1.0 es "warning", >= 1.0 es "ok".
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT need_human_dimensions, offer_human_dimensions
            FROM participants
            WHERE status = 'active'
            """
        )

        need_counts: Dict[str, int] = {}
        offer_counts: Dict[str, int] = {}

        for row in cursor.fetchall():
            needs = self._parse_json(row[0])
            offers = self._parse_json(row[1])
            for dim in needs:
                need_counts[dim] = need_counts.get(dim, 0) + 1
            for dim in offers:
                offer_counts[dim] = offer_counts.get(dim, 0) + 1

        all_dims = set(need_counts) | set(offer_counts)
        gaps: List[CommunityGap] = []

        for dim in all_dims:
            needing = need_counts.get(dim, 0)
            offering = offer_counts.get(dim, 0)
            ratio = offering / max(needing, 1)

            if ratio < 0.5:
                severity = "critical"
            elif ratio < 1.0:
                severity = "warning"
            else:
                severity = "ok"

            gaps.append(
                CommunityGap(
                    dimension=dim,
                    dimension_label=self.DIMENSION_LABELS.get(dim, dim.replace("_", " ").title()),
                    participants_needing=needing,
                    participants_offering=offering,
                    coverage_ratio=round(ratio, 3),
                    gap_severity=severity,
                )
            )

        gaps.sort(key=lambda g: g.coverage_ratio)
        return gaps

    def get_matching_summary(self) -> Dict[str, Any]:
        """
        Resumen ejecutivo para el dashboard:
        - Número de necesidades urgentes sin resolver
        - Número de Crímenes de Coherencia detectados
        - Número de brechas críticas en la comunidad
        - Categoría más demandada sin cobertura suficiente
        """
        urgent = self.get_urgent_unmet_needs()
        gaps = self.get_community_sdv_gaps()

        crimes = [u for u in urgent if u.is_coherence_crime]
        critical_gaps = [g for g in gaps if g.gap_severity == "critical"]
        worst_gap = critical_gaps[0] if critical_gaps else None

        return {
            "urgent_unmet_count": len(urgent),
            "coherence_crimes_count": len(crimes),
            "critical_gaps_count": len(critical_gaps),
            "worst_gap_dimension": worst_gap.dimension_label if worst_gap else None,
            "worst_gap_ratio": worst_gap.coverage_ratio if worst_gap else None,
            "system_alert_level": (
                "coherence_crime" if crimes
                else "warning" if urgent
                else "ok"
            ),
        }
