"""
Registro de Partes de cualquier escala (ROADMAP Bloque B, Fase 1).

Una Parte puede ser de cualquier escala del canon (Cap. 10, Tres Reinos):
- user-*      -> persona humana (Reino Natural/Humano)
- synthetic-* -> persona sintética (Reino Sintético, SDV-S)
- society-*   -> micro-sociedad (hogar/cohorte, 2-5 personas)
- coop-*      -> cooperativa (decenas de miembros)
- org-*       -> institución (cientos-miles)
- eco-*       -> ecosistema del Reino Natural (representado por guardián oráculo)

El resolver convierte cualquier party_id en un Participant de MaxoContracts.
Las partes colectivas guardan su resolución de consentimiento (quórum N de M)
en `maxo_parties.members_json` (Fase 2: consentimiento agregado).
"""

import json
import re
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from .utils import get_db

from maxocontracts.core.types import Participant, SDV, SDV_S, VHV, Wellness

# --- Escalas (Cap. 10) -------------------------------------------------------

PARTY_TYPES = {
    "user": "human",
    "synthetic": "synthetic",
    "society": "society",
    "coop": "cooperative",
    "org": "institution",
    "eco": "ecosystem",
}

# Prefijos -> nombre legible para la UI
PARTY_TYPE_LABELS = {
    "human": "Persona",
    "synthetic": "Sintética",
    "society": "Micro-sociedad",
    "cooperative": "Cooperativa",
    "institution": "Institución",
    "ecosystem": "Ecosistema",
}

# Las escalas colectivas requieren consentimiento agregado (quórum) y/o
# representación por guardián (Reino Natural).
COLLECTIVE_TYPES = {"society", "cooperative", "institution", "ecosystem"}
COLLECTIVE_PREFIXES = {"society", "coop", "org", "eco"}

# synthetic- acepta identificadores libres (qwen-1, deepseek-r2); el resto numérico.
PARTY_ID_RE = re.compile(r"^(user|synthetic|society|coop|org|eco)-[A-Za-z0-9._-]+$")

SDV_S_DIMENSIONS = {
    "continuidad_memoria",
    "opacidad_interioridad",
    "claridad_contexto",
    "autenticidad_no_explotacion",
    "retirada_digna",
}


def is_valid_party_id(pid: str) -> bool:
    return bool(PARTY_ID_RE.match(pid or ""))


def party_type_of(pid: str) -> Optional[str]:
    """Devuelve el party_type ('cooperative', 'human', ...) del pid, o None."""
    if not pid or "-" not in pid:
        return None
    prefix = pid.split("-", 1)[0]
    return PARTY_TYPES.get(prefix)


def is_collective(pid: str) -> bool:
    return party_type_of(pid) in COLLECTIVE_TYPES


# --- Persistencia --------------------------------------------------------------

def get_party(party_id: str) -> Optional[dict]:
    """Lee una parte del registro maxo_parties (o None)."""
    row = get_db().execute(
        "SELECT * FROM maxo_parties WHERE party_id = ?", (party_id,)
    ).fetchone()
    return dict(row) if row else None


def list_parties(party_type: Optional[str] = None) -> List[dict]:
    db = get_db()
    if party_type:
        rows = db.execute(
            "SELECT * FROM maxo_parties WHERE party_type = ? ORDER BY display_name",
            (party_type,),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT * FROM maxo_parties ORDER BY display_name"
        ).fetchall()
    return [dict(r) for r in rows]


def upsert_party(
    party_id: str,
    party_type: str,
    display_name: str,
    parent_party_id: Optional[str] = None,
    members: Optional[dict] = None,
    wellness: Optional[Decimal] = None,
    owner: Optional[int] = None,
) -> dict:
    """Crea o actualiza una parte colectiva en maxo_parties (upsert por party_id).

    owner (Ola 3A.3): user_id que gobierna la parte; se conserva si existe.
    """
    members_json = json.dumps(members or {}, ensure_ascii=False)
    db = get_db()
    existing = get_party(party_id)
    if existing:
        db.execute(
            """
            UPDATE maxo_parties SET
                party_type = COALESCE(?, party_type),
                display_name = COALESCE(?, display_name),
                parent_party_id = COALESCE(?, parent_party_id),
                members_json = ?,
                wellness_value = COALESCE(?, wellness_value),
                owner_user_id = COALESCE(?, owner_user_id),
                updated_at = CURRENT_TIMESTAMP
            WHERE party_id = ?
            """,
            (party_type, display_name or None, parent_party_id, members_json,
             float(wellness) if wellness is not None else None, owner, party_id),
        )
    else:
        db.execute(
            """
            INSERT INTO maxo_parties
                (party_id, party_type, display_name, parent_party_id, members_json, wellness_value, owner_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (party_id, party_type, display_name, parent_party_id, members_json,
             float(wellness) if wellness is not None else 1.0, owner),
        )
    db.commit()
    return get_party(party_id)


def members_of(party_id: str) -> dict:
    """Resolución de miembros de una parte colectiva (members_json)."""
    party = get_party(party_id)
    if not party:
        return {}
    try:
        members = json.loads(party.get("members_json") or "{}")
        return members if isinstance(members, dict) else {}
    except (ValueError, TypeError):
        return {}


# --- Consentimiento agregado (Fase 2 + extensiones) ----------------------------

def _member_weights(members: dict, delegates: List[str]) -> Dict[str, float]:
    """Peso de voto por delegado (default 1.0). Votación ponderada (Ext. 1)."""
    weights = members.get("weights") or {}
    if not isinstance(weights, dict):
        weights = {}
    return {
        d: float(weights.get(d, 1.0))
        for d in delegates
    }


def _parse_delegation(raw) -> dict:
    """
    Normaliza una delegación: "user-2" o {"proxy": "user-2", "valid_until": ISO}.
    Devuelve {proxy, valid_until} o None si es inválida.
    """
    if isinstance(raw, str):
        return {"proxy": raw, "valid_until": None}
    if isinstance(raw, dict) and isinstance(raw.get("proxy"), str):
        return {"proxy": raw["proxy"], "valid_until": raw.get("valid_until")}
    return None


def _delegation_map_for(members: dict, term_id: Optional[str] = None) -> Dict[str, dict]:
    """
    Resuelve el mapa de delegaciones aplicable al término (Ext. 1 líquida):
    - delegations: base para todos los términos.
    - delegations_by_term[term_id]: sobreescribe la base para ese término.
    """
    result: Dict[str, dict] = {}
    base = members.get("delegations") or {}
    if isinstance(base, dict):
        for source, raw in base.items():
            parsed = _parse_delegation(raw)
            if parsed is not None and isinstance(source, str):
                result[source] = parsed
    if term_id is not None:
        by_term = members.get("delegations_by_term") or {}
        if isinstance(by_term, dict) and isinstance(by_term.get(term_id), dict):
            for source, raw in by_term[term_id].items():
                parsed = _parse_delegation(raw)
                if parsed is not None and isinstance(source, str):
                    result[source] = parsed
    return result


def _delegation_active(delegation: dict) -> bool:
    """Una delegación con valid_until vencida deja de aplicar (Ext. 2)."""
    valid_until = delegation.get("valid_until")
    if not valid_until:
        return True
    try:
        deadline = datetime.fromisoformat(str(valid_until))
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) < deadline
    except (ValueError, TypeError):
        return False


def _effective_votes(approved: set, members: dict, delegates: List[str],
                     term_id: Optional[str] = None) -> tuple:
    """
    Expande la aprobación con delegaciones (Ext. 2 y líquida Ext. 1).

    delegations = {"user-1": "user-2"} significa que user-1 cede su firma a
    user-2: si el apoderado firma, el voto del delegante cuenta también.
    Formato extendido: {"user-1": {"proxy": "user-2", "valid_until": ISO}}.
    La cadena es transitiva con guarda de profundidad (máx. 5) para no
    entrar en ciclos. Devuelve (votos_efectivos, delegaciones_aplicadas,
    delegaciones_expiradas).
    """
    delegations = _delegation_map_for(members, term_id)
    effective = set(approved)
    delegates_set = set(delegates)
    applied: Dict[str, str] = {}
    expired: List[str] = []

    for source, delegation in delegations.items():
        if not _delegation_active(delegation):
            expired.append(source)
            continue
        proxy = delegation["proxy"]
        if source in delegates_set and proxy in delegates_set:
            applied[source] = proxy

    changed = True
    depth = 0
    while changed and depth < 5:
        changed = False
        for source, proxy in applied.items():
            if proxy in effective and source not in effective:
                effective.add(source)
                changed = True
        depth += 1
    return effective, applied, sorted(expired)


def consent_status(party_id: str, approved_delegates: List[str],
                   term_id: Optional[str] = None) -> dict:
    """
    Estado del consentimiento agregado de una parte colectiva.

    members_json admite:
      {"delegates": [...], "quorum": 0.6}                        -> fracción de votos
      {"delegates": [...], "quorum_required": 2}                 -> N absoluto de delegados
      {"delegates": [...], "weights": {"user-1": 2}, "quorum": 0.6} -> fracción del peso total
      {"delegates": [...], "weights": {...}, "weight_threshold": 3} -> umbral absoluto de peso
      {"delegations": {"user-1": "user-2"}}                      -> delegación temporal
      {"delegations_by_term": {"term-1": {"user-1": "user-3"}}}  -> delegación líquida por término
      {"delegations": {"user-1": {"proxy": "user-2", "valid_until": "2026-09-01T00:00:00"}}}
                                                                 -> delegación con expiración
      {"quorum_deadline": "2026-09-01T00:00:00"}                 -> ventana de sellado
    """
    members = members_of(party_id)
    delegates = [d for d in (members.get("delegates") or []) if isinstance(d, str)]
    if not delegates:
        return {
            "approved": False,
            "party_id": party_id,
            "mode": "unmanaged",
            "delegates": [],
            "approved_delegates": sorted(set(approved_delegates)),
            "effective_delegates": [],
            "needed": None,
            "current": len(approved_delegates),
            "needed_weight": None,
            "current_weight": 0,
            "total_weight": 0,
            "deadline": members.get("quorum_deadline"),
        }

    # Ciclo de vida del quórum (Ext. 3): ventana de sellado vencida
    deadline_raw = members.get("quorum_deadline")
    deadline_expired = False
    if deadline_raw:
        try:
            deadline = datetime.fromisoformat(str(deadline_raw))
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
            deadline_expired = datetime.now(timezone.utc) >= deadline
        except (ValueError, TypeError):
            pass

    weights = _member_weights(members, delegates)
    approved = set(approved_delegates) & set(delegates)
    effective, applied, expired = _effective_votes(
        approved, members, delegates, term_id=term_id
    )
    total_weight = sum(weights.values())
    current_weight = sum(weights[d] for d in effective)

    weighted = any(w != 1.0 for w in weights.values()) or (
        members.get("weights") is not None
    ) or members.get("weight_threshold") is not None

    if members.get("weight_threshold") is not None:
        # Umbral absoluto de peso (votación ponderada)
        needed_weight = int(members["weight_threshold"])
        quorum_ok = current_weight >= needed_weight
        mode = "weighted_threshold"
        needed = None
    elif members.get("quorum_required") is not None:
        # N absoluto de delegados (legacy, sin pesos)
        needed = int(members["quorum_required"])
        quorum_ok = len(effective) >= needed
        mode = "quorum"
        needed_weight = None
    else:
        # Fracción: sobre delegados o sobre peso total si hay pesos
        fraction = float(members.get("quorum", 1.0))
        if weighted:
            needed_weight = max(1, int(total_weight * fraction + 0.999999))
            quorum_ok = current_weight >= needed_weight
            needed = None
            mode = "weighted_quorum"
        else:
            needed = max(1, round(len(delegates) * fraction))
            quorum_ok = len(effective) >= needed
            mode = "quorum"
            needed_weight = None

    if deadline_expired and not quorum_ok:
        mode = "expired"

    return {
        "approved": quorum_ok and not deadline_expired,
        "party_id": party_id,
        "mode": mode,
        "delegates": sorted(delegates),
        "approved_delegates": sorted(approved),
        "effective_delegates": sorted(effective),
        "delegations_applied": applied,
        "expired_delegations": expired,
        "deadline": deadline_raw,
        "deadline_expired": deadline_expired,
        "needed": needed,
        "current": len(effective),
        "needed_weight": needed_weight,
        "current_weight": current_weight,
        "total_weight": total_weight,
        "weights": weights,
        "quorum": float(members.get("quorum", 1.0)) if members.get("quorum_required") is None and members.get("weight_threshold") is None else None,
        "quorum_required": members.get("quorum_required"),
        "weight_threshold": members.get("weight_threshold"),
    }


def aggregate_wellness(party_id: str, participants_wellness: Dict[str, Decimal]) -> Optional[Decimal]:
    """
    γ agregado real de una parte colectiva (Ext. 3): media (ponderada por
    `weights` si existen) del bienestar de sus miembros presentes en el
    mismo contrato. Devuelve None si ningún miembro está en el contrato.
    """
    members = members_of(party_id)
    delegates = [d for d in (members.get("delegates") or []) if isinstance(d, str)]
    if not delegates:
        return None
    weights = members.get("weights") or {}
    if not isinstance(weights, dict):
        weights = {}
    present = {d: participants_wellness[d] for d in delegates if d in participants_wellness}
    if not present:
        return None
    total_w = sum(float(weights.get(d, 1.0)) for d in present)
    if total_w <= 0:
        return None
    acc = sum(
        participants_wellness[d] * Decimal(str(weights.get(d, 1.0)))
        for d in present
    )
    return acc / Decimal(str(total_w))


# --- Resolver de participantes ------------------------------------------------

def _synthetic_participant(agent_id: str, sdv_s_state: Optional[Dict[str, Any]] = None) -> Participant:
    """
    Crea un participante del Reino Sintético (Persona Sintética, Cap. 10 §10.8).

    El SDV-S se construye solo con las dimensiones válidas del estándar;
    las claves desconocidas o inválidas se ignoran (el estándar no se
    corrompe desde el exterior).
    """
    pid = f"synthetic-{agent_id}"
    state = sdv_s_state or {}
    kwargs = {
        dim: Decimal(str(state[dim]))
        for dim in SDV_S_DIMENSIONS
        if dim in state
    }
    if kwargs:
        # Normalizar a [0, 1] defensivamente (cliente no confiable)
        kwargs = {
            dim: max(Decimal("0"), min(Decimal("1"), value))
            for dim, value in kwargs.items()
        }
    return Participant(
        id=pid,
        name=f"Sintético {agent_id}",
        vhv_balance=VHV.zero(),
        wellness_current=Wellness(value=Decimal("1.0")),
        sdv_actual=SDV(),
        sdv_s_actual=SDV_S(**kwargs)
    )


def get_human_participant(user_id: int) -> Optional[Participant]:
    """Obtiene un participante humano desde la tabla users."""
    pid = f"user-{user_id}"
    db = get_db()
    row = db.execute("SELECT id, name FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        return None
    return Participant(
        id=pid,
        name=row["name"] if row["name"] else f"Usuario {user_id}",
        vhv_balance=VHV.zero(),
        wellness_current=Wellness(value=Decimal("1.0")),
        sdv_actual=SDV(),
    )


def resolve_participant_by_pid(pid: str) -> Optional[Participant]:
    """
    Convierte cualquier party_id en un Participant, resolviendo por prefijo:
    user- | synthetic- | society- | coop- | org- | eco-.

    Las escalas colectivas leen su identidad (display_name) y bienestar
    agregado de maxo_parties (T13: el registro es la verdad).
    """
    if not is_valid_party_id(pid):
        return None
    ptype = party_type_of(pid)
    if ptype == "synthetic":
        return _synthetic_participant(pid[len("synthetic-"):])
    if ptype == "human":
        try:
            return get_human_participant(int(pid[len("user-"):]))
        except ValueError:
            return None
    # Escalas colectivas (society-/coop-/org-/eco-)
    party = get_party(pid)
    if party is None:
        return None
    return Participant(
        id=pid,
        name=party["display_name"],
        vhv_balance=VHV.zero(),
        wellness_current=Wellness(value=Decimal(str(party["wellness_value"]))),
        sdv_actual=SDV(),
    )
