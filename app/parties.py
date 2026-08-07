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
) -> dict:
    """Crea o actualiza una parte colectiva en maxo_parties (upsert por party_id)."""
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
                updated_at = CURRENT_TIMESTAMP
            WHERE party_id = ?
            """,
            (party_type, display_name or None, parent_party_id, members_json,
             float(wellness) if wellness is not None else None, party_id),
        )
    else:
        db.execute(
            """
            INSERT INTO maxo_parties
                (party_id, party_type, display_name, parent_party_id, members_json, wellness_value)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (party_id, party_type, display_name, parent_party_id, members_json,
             float(wellness) if wellness is not None else 1.0),
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


# --- Consentimiento agregado (Fase 2) -----------------------------------------

def consent_status(party_id: str, approved_delegates: List[str]) -> dict:
    """
    Estado del consentimiento agregado de una parte colectiva.

    members_json admite dos formas de quórum:
      {"delegates": ["user-1", "user-2", "user-3"], "quorum": 0.6}  -> fracción
      {"delegates": [...], "quorum_required": 2}                    -> N absoluto
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
            "needed": None,
            "current": len(approved_delegates),
        }

    approved = set(approved_delegates) & set(delegates)
    if members.get("quorum_required") is not None:
        needed = int(members["quorum_required"])
    else:
        fraction = float(members.get("quorum", 1.0))
        needed = max(1, round(len(delegates) * fraction))
    quorum_ok = len(approved) >= needed
    return {
        "approved": quorum_ok,
        "party_id": party_id,
        "mode": "quorum",
        "delegates": sorted(delegates),
        "approved_delegates": sorted(approved),
        "needed": needed,
        "current": len(approved),
        "quorum": float(members.get("quorum", 1.0)) if members.get("quorum_required") is None else None,
        "quorum_required": members.get("quorum_required"),
    }


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
