"""
MaxoContracts API Blueprint
===========================
REST API para contratos inteligentes éticos de la Maxocracia.

Endpoints:
- POST   /contracts/             - Crear nuevo contrato
- GET    /contracts/<id>         - Obtener contrato
- POST   /contracts/<id>/terms   - Añadir término
- POST   /contracts/<id>/accept  - Aceptar término
- POST   /contracts/<id>/activate - Activar contrato
- POST   /contracts/<id>/retract  - Solicitar retractación
- GET    /contracts/<id>/civil    - Resumen en lenguaje civil
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import sqlite3

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db

# Importar MaxoContracts core
import sys
import os

# Agregar ruta del proyecto para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maxocontracts.core.types import (
    VHV,
    Wellness,
    SDV,
    SDV_S,
    Participant,
    ContractTerm,
    ContractState,
    MaxoAmount,
)
from maxocontracts.core.contract import MaxoContract
from maxocontracts.blocks.sdv_s_validator import SDV_SValidatorBlock
from maxocontracts.core.axioms import AxiomValidator, ValidationResult
from maxocontracts.oracles import SyntheticOracle
from maxocontracts.oracles.live_oracle import (
    LiveOracle,
    OracleUnavailableError,
    OracleAPIError,
)

from .webhooks import dispatch_event
from .parties import (
    aggregate_wellness,
    consent_status,
    get_party,
    get_human_participant,
    is_collective,
    is_valid_party_id,
    members_of,
    party_type_of,
    resolve_participant_by_pid,
    _synthetic_participant,
)

from decimal import Decimal
import hashlib
import json
import unicodedata

# --- Blindaje anti-gamificación (Ola 3A) --------------------------------------
# Límites y umbrales configurables del sistema (diseño: blindaje_anti_gamificacion_equidad.md)

CIVIL_MAX_WORDS = 40
CIVIL_MAX_SENTENCES = 2
WELLNESS_MIN = Decimal("0.5")
WELLNESS_MAX = Decimal("1.5")
ASYMMETRY_MAX_SHARE = 0.7
ASYMMETRY_MIN_TOTAL_H = 8.0
ASSIGNED_REQUIRED_MIN_TOTAL = Decimal("10")

PROHIBITED_PATTERNS = [
    "sin derecho a retractarse",
    "sin derecho a retractacion",
    "renuncia a la retractacion",
    "no podra retractarse",
    "renuncia a retractarse",
    "exclusividad",
    "renovacion automatica",
    "penalizacion por retractarse",
    "retractacion penalizada",
    "renuncia a la dignidad",
    "renuncia a mi sdv",
    "esclavitud",
    "sin limite de tiempo",
]


def _token_uid(current_user) -> Optional[int]:
    """El actor SIEMPRE deriva del token (Ola 3A.1, R1)."""
    uid = current_user.get("user_id") or current_user.get("id")
    return int(uid) if uid is not None else None


def _normalize_civil(text: str) -> str:
    """Minúsculas y sin acentos para comparación de patrones."""
    text = (text or "").lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def _validate_civil_text(text: str) -> Optional[str]:
    """Lenguaje civil enforceable (Ola 3A.6, R8): palabras, oraciones y
    patrones explotativos prohibidos (R7)."""
    t = text or ""
    if len(t.split()) > CIVIL_MAX_WORDS:
        return f"civil_text excede {CIVIL_MAX_WORDS} palabras (lenguaje civil, grado 8º)"
    if t.count(".") > CIVIL_MAX_SENTENCES:
        return f"civil_text excede {CIVIL_MAX_SENTENCES} oraciones (lenguaje civil)"
    norm = _normalize_civil(t)
    for pattern in PROHIBITED_PATTERNS:
        if pattern in norm:
            return f"cláusula prohibida detectada: '{pattern}' (viola T11/T12)"
    return None


def _reciprocity_imbalance(contract) -> tuple:
    """
    T9 ejecutable con tolerancia declarada (Ola 3A.4, R6).

    Devuelve (flag, report): flag True si una sola parte carga más del 70%
    del TVI total asignado, con ≥ 2 partes obligadas y total ≥ 8h.
    La asimetría NO bloquea la creación: bloquea la ACTIVACIÓN hasta que
    todas las partes obligadas (y un aval) la reconozcan explícitamente.
    """
    by_party = {}
    for t in contract._terms:
        pid = getattr(t, "assigned_participant", None)
        if pid and float(t.vhv_cost.T) > 0:
            by_party[pid] = by_party.get(pid, 0.0) + float(t.vhv_cost.T)
    total = sum(by_party.values())
    if not by_party or total < ASYMMETRY_MIN_TOTAL_H or len(by_party) < 2:
        return False, {"obligations": by_party, "total": round(total, 2)}
    max_party = max(by_party, key=by_party.get)
    max_share = by_party[max_party] / total
    return max_share > ASYMMETRY_MAX_SHARE, {
        "obligations": by_party,
        "total": round(total, 2),
        "max_party": max_party,
        "max_share": round(max_share, 3),
        "threshold": ASYMMETRY_MAX_SHARE,
    }


def _audit(contract: MaxoContract, action: str, actor_id: Optional[int], **extra) -> None:
    """Registro auditable de acciones de la API (Ola 3A.2, T13)."""
    data = {"actor_id": f"user-{actor_id}" if actor_id else None}
    data.update(extra)
    contract._log_event(action, data)


def _can_act_for(pid: str, token_uid: Optional[int], contract=None) -> bool:
    """¿Puede el actor del token actuar por el pid? (Ola 3A.1, R1/R4)"""
    if token_uid is None:
        return False
    if pid == f"user-{token_uid}":
        return True
    if party_type_of(pid) == "ecosystem":
        # El guardián del Reino Natural es invocado por un participante
        # humano del contrato (el actor queda registrado).
        return contract is not None and f"user-{token_uid}" in contract.participant_ids
    if is_collective(pid):
        return f"user-{token_uid}" in (members_of(pid).get("delegates") or [])
    if party_type_of(pid) == "synthetic":
        # Operación asistida: cualquier participante humano del contrato
        # puede operar la firma sintética (el actor queda registrado).
        return contract is not None and f"user-{token_uid}" in contract.participant_ids
    return False


def _contract_window_blocked(contract, db) -> Optional[dict]:
    """
    Ventanas temporales server-side (Ola 3A.7, R10/R11): deadline de firma
    y enfriamiento mínimo entre creación y primera firma.
    Devuelve un payload de error (423) o None.
    """
    from datetime import timedelta
    created_at = getattr(contract, "_created_at", None)
    if created_at:
        try:
            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            created_dt = None
    else:
        created_dt = None

    deadline = getattr(contract, "_signature_deadline", None)
    if deadline:
        try:
            dl = datetime.fromisoformat(str(deadline).replace("Z", "+00:00"))
            if datetime.now() > dl:
                return {"error": "la ventana de firma del contrato venció",
                        "code": "SIGNATURE_DEADLINE_EXPIRED"}
        except (ValueError, TypeError):
            pass

    hours = float(getattr(contract, "_min_reflection_hours", 0) or 0)
    if hours > 0 and created_dt:
        ready_at = created_dt + timedelta(hours=hours)
        now = datetime.now()
        if now < ready_at:
            remaining = (ready_at - now).total_seconds() / 3600
            return {"error": f"periodo de reflexión obligatorio en curso "
                             f"({hours:.0f}h desde la creación)",
                    "code": "REFLECTION_PENDING",
                    "remaining_hours": round(remaining, 1)}
    return None

contracts_bp = Blueprint("contracts", __name__, url_prefix="/contracts")


def _serve_first(*rel_paths):
    """Sirve el primer asset estático existente (relativo a app/static/dist)."""
    from flask import current_app, send_from_directory

    dist_dir = os.path.join(current_app.root_path, "static", "dist")
    for rel in rel_paths:
        if os.path.exists(os.path.join(dist_dir, rel)):
            return send_from_directory(dist_dir, rel)
    return None


def _alias_dynamic_segments(rel: str) -> str:
    """Reemplaza el id dinámico de /contracts/<id> por el segmento estático
    'placeholder' (página SSG de la ruta dinámica exportada por Next.js).

    El componente de esa página lee el id real del URL (useParams), así que
    el payload RSC es reutilizable para cualquier contrato.
    """
    parts = rel.split("/")
    if (
        len(parts) >= 2
        and parts[0] == "contracts"
        and parts[1]
        and not parts[1].startswith("builder")
        and not parts[1].startswith("negotiate")
        and not parts[1].startswith("__next")
    ):
        original = parts[1]
        pure_id = original
        for ext in (".txt", ".html"):
            if pure_id.endswith(ext):
                pure_id = pure_id[: -len(ext)]
                parts[1] = "placeholder" + ext
                break
        else:
            parts[1] = "placeholder"
        # Los archivos de segmento (__next.contracts.<id>.txt) también
        # llevan el id dinámico en el nombre; se reescribe igual.
        if pure_id and pure_id != "placeholder":
            parts[2:] = [seg.replace(pure_id, "placeholder") for seg in parts[2:]]
    return "/".join(parts)


@contracts_bp.before_request
def _serve_frontend_collisions():
    """Despacha al frontend estático las peticiones que colisionan con las
    rutas API de /contracts/:

    1. Payloads RSC (.txt) que el router de Next solicita para navegar.
    2. Navegaciones completas de navegador (Accept: text/html) que deben
       recibir la página HTML en lugar del JSON 401 de la API.

    Las peticiones API normales (fetch con Accept */* o application/json)
    no se ven afectadas y siguen su flujo con autenticación.
    """
    if request.method != "GET":
        return None

    path = request.path.lstrip("/")

    # 1. Payloads RSC de la navegación cliente (Next.js static export)
    if path.endswith(".txt"):
        asset = _serve_first(_alias_dynamic_segments(path))
        if asset is not None:
            return asset
        return jsonify({"error": "RSC payload not found"}), 404

    # 2. Carga completa de página en el navegador
    if "text/html" in request.headers.get("Accept", ""):
        base = path.rstrip("/")
        asset = _serve_first(_alias_dynamic_segments(base + ".html"))
        if asset is None:
            asset = _serve_first("index.html")
        if asset is not None:
            return asset

    return None


def init_contracts_metrics_tables(app):
    """Crea las tablas de métricas (NPS, metadatos, partes, quórum) si no existen.

    Sigue el patrón de init_subscription_tables / init_micromax_tables:
    permite que bases de datos ya existentes reciban las tablas nuevas
    sin re-ejecutar todo el schema.sql.
    """
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS maxo_contract_nps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                participant_id TEXT NOT NULL,
                score INTEGER NOT NULL CHECK(score >= 0 AND score <= 10),
                comment TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
                UNIQUE(contract_id, participant_id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS maxo_contract_meta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                meta_key TEXT NOT NULL,
                meta_value TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
                UNIQUE(contract_id, meta_key)
            )
        """)
        # Registro de Partes de cualquier escala (ROADMAP Bloque B, Fase 1):
        # persona, micro-sociedad, cooperativa, institución, sintética, ecosistema.
        cur.execute("""
            CREATE TABLE IF NOT EXISTS maxo_parties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_id TEXT UNIQUE NOT NULL,
                party_type TEXT NOT NULL,
                display_name TEXT NOT NULL,
                parent_party_id TEXT,
                members_json TEXT DEFAULT '{}',
                wellness_value REAL DEFAULT 1.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Firmas delegadas para consentimiento agregado con quórum (Fase 2).
        cur.execute("""
            CREATE TABLE IF NOT EXISTS maxo_contract_delegate_approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id TEXT NOT NULL,
                term_id TEXT NOT NULL,
                party_id TEXT NOT NULL,
                delegate_id TEXT NOT NULL,
                approved_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
                UNIQUE(contract_id, term_id, party_id, delegate_id)
            )
        """)
        # Migración: cada término puede quedar vinculado a la parte obligada
        # (ej. 'user-1' o 'synthetic-qwen-1'). Permite "bloques vinculados
        # a usuarios" y la vista de documento legal. Solo aplica si la tabla
        # ya existe (en BD nuevas el schema.sql la crea con la columna).
        tables = [
            r[0] for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        ]
        if "maxo_contract_terms" in tables:
            cols = [r[1] for r in cur.execute("PRAGMA table_info(maxo_contract_terms)").fetchall()]
            if "assigned_participant" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contract_terms ADD COLUMN assigned_participant TEXT"
                )
        # Migración: contratos interescala anidados (Fase 5).
        if "maxo_contracts" in tables:
            cols = [r[1] for r in cur.execute("PRAGMA table_info(maxo_contracts)").fetchall()]
            if "parent_contract_id" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contracts ADD COLUMN parent_contract_id TEXT"
                )
            # Ola 3A: inmutabilidad (creador) y ventanas temporales
            if "creator_user_id" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contracts ADD COLUMN creator_user_id INTEGER"
                )
            if "signature_deadline" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contracts ADD COLUMN signature_deadline TEXT"
                )
            if "min_reflection_hours" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contracts ADD COLUMN min_reflection_hours REAL DEFAULT 0"
                )
        # Ola 3A.3: autoridad sobre las partes + votos de gobernanza
        if "maxo_parties" in tables:
            cols = [r[1] for r in cur.execute("PRAGMA table_info(maxo_parties)").fetchall()]
            if "owner_user_id" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_parties ADD COLUMN owner_user_id INTEGER"
                )
        cur.execute("""
            CREATE TABLE IF NOT EXISTS maxo_party_governance_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_id TEXT NOT NULL,
                proposal_hash TEXT NOT NULL,
                delegate_id TEXT NOT NULL,
                approved INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(party_id, proposal_hash, delegate_id)
            )
        """)
        # Ola 3A.5: γ con fuente (actor y timestamp del reporte)
        if "maxo_contract_participants" in tables:
            cols = [r[1] for r in cur.execute("PRAGMA table_info(maxo_contract_participants)").fetchall()]
            if "reported_by" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contract_participants ADD COLUMN reported_by TEXT"
                )
            if "reported_at" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_contract_participants ADD COLUMN reported_at TEXT"
                )
        # Migración: webhooks filtrados por parte (Ext. 4).
        if "maxo_webhooks" in tables:
            cols = [r[1] for r in cur.execute("PRAGMA table_info(maxo_webhooks)").fetchall()]
            if "party_filter" not in cols:
                cur.execute(
                    "ALTER TABLE maxo_webhooks ADD COLUMN party_filter TEXT"
                )
        conn.commit()
    finally:
        conn.close()


@contracts_bp.route("/builder")
def serve_builder():
    """Sirve el constructor de contratos de Next.js."""
    from flask import current_app
    return current_app.send_static_file("dist/contracts/builder.html")

# Helper functions for persistence

def _save_contract(contract: MaxoContract, actor_id: Optional[int] = None):
    """Guarda un objeto MaxoContract en la base de datos.

    actor_id (Ola 3A.5): quién reporta el γ al escribir participantes.
    """
    db = get_db()
    
    # 1. Upsert contract header
    parent_id = getattr(contract, "_parent_contract_id", None)
    creator_id = getattr(contract, "_creator_user_id", None)
    deadline = getattr(contract, "_signature_deadline", None)
    reflection = float(getattr(contract, "_min_reflection_hours", 0) or 0)
    db.execute("""
        INSERT INTO maxo_contracts (contract_id, civil_description, state, total_vhv_t, total_vhv_v, total_vhv_h, parent_contract_id, creator_user_id, signature_deadline, min_reflection_hours, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(contract_id) DO UPDATE SET
            civil_description=excluded.civil_description,
            state=excluded.state,
            total_vhv_t=excluded.total_vhv_t,
            total_vhv_v=excluded.total_vhv_v,
            total_vhv_h=excluded.total_vhv_h,
            parent_contract_id=COALESCE(excluded.parent_contract_id, parent_contract_id),
            creator_user_id=COALESCE(excluded.creator_user_id, creator_user_id),
            signature_deadline=COALESCE(excluded.signature_deadline, signature_deadline),
            min_reflection_hours=COALESCE(excluded.min_reflection_hours, min_reflection_hours),
            updated_at=CURRENT_TIMESTAMP
    """, (
        contract.contract_id,
        contract.civil_summary,
        contract.state.value,
        float(contract.total_vhv.T),
        float(contract.total_vhv.V),
        float(contract.total_vhv.R),
        parent_id,
        creator_id,
        deadline,
        reflection
    ))
    
    # 2. Update participants
    # Primero: γ agregado real de las partes colectivas (Ext. 3) — media
    # ponderada del bienestar de sus miembros presentes en este contrato.
    wellness_map = {
        p.id: p.wellness_current.value for p in contract.participants
    }
    for p in contract.participants:
        if p.id.startswith(("society-", "coop-", "org-", "eco-")):
            agg = aggregate_wellness(p.id, wellness_map)
            if agg is not None:
                p.update_wellness(agg)
    for p in contract.participants:
        # sdv_status: "ok" para humanos; JSON completo del estado SDV-S
        # para participantes sintéticos (T13: auditable en la base).
        if p.is_synthetic and p.sdv_s_actual is not None:
            sdv_status = json.dumps({
                dim: str(getattr(p.sdv_s_actual, dim))
                for dim in SDV_S.DIMENSIONS
            })
        else:
            sdv_status = "ok"
        db.execute("""
            INSERT INTO maxo_contract_participants (contract_id, participant_id, wellness_value, sdv_status, reported_by, reported_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(contract_id, participant_id) DO UPDATE SET
                wellness_value=excluded.wellness_value,
                sdv_status=excluded.sdv_status,
                reported_by=COALESCE(maxo_contract_participants.reported_by, excluded.reported_by),
                reported_at=COALESCE(maxo_contract_participants.reported_at, excluded.reported_at)
        """, (
            contract.contract_id,
            p.id,
            float(p.wellness_current.value),
            sdv_status,
            f"user-{actor_id}" if actor_id is not None else None,
            datetime.now().isoformat()
        ))
        # Sincronizar γ agregado de partes colectivas al registro (T13)
        if p.id.startswith(("society-", "coop-", "org-", "eco-")):
            party = get_party(p.id)
            if party is not None:
                from .parties import upsert_party
                upsert_party(
                    party_id=p.id,
                    party_type=party["party_type"],
                    display_name=party["display_name"],
                    parent_party_id=party.get("parent_party_id"),
                    members=members_of(p.id),
                    wellness=p.wellness_current.value,
                )
    
    # 3. Update terms and approvals
    for term in contract._terms:
        db.execute("""
            INSERT INTO maxo_contract_terms (contract_id, term_id, civil_text, vhv_t, vhv_v, vhv_h, assigned_participant)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(contract_id, term_id) DO UPDATE SET
                civil_text=excluded.civil_text,
                vhv_t=excluded.vhv_t,
                vhv_v=excluded.vhv_v,
                vhv_h=excluded.vhv_h,
                assigned_participant=excluded.assigned_participant
        """, (
            contract.contract_id,
            term.id,
            term.description,
            float(term.vhv_cost.T),
            float(term.vhv_cost.V),
            float(term.vhv_cost.R),
            getattr(term, "assigned_participant", None)
        ))
        
        for p_id, accepted in term.accepted_by.items():
            if accepted:
                db.execute("""
                    INSERT OR IGNORE INTO maxo_contract_term_approvals (contract_id, term_id, participant_id)
                    VALUES (?, ?, ?)
                """, (contract.contract_id, term.id, p_id))
    
    # 4. Sync events (only new ones)
    existing_events_count = db.execute("SELECT COUNT(*) FROM maxo_contract_events WHERE contract_id = ?", (contract.contract_id,)).fetchone()[0]
    for i, event in enumerate(contract.get_event_log()):
        if i >= existing_events_count:
            db.execute("""
                INSERT INTO maxo_contract_events (contract_id, event_type, description, metadata_json)
                VALUES (?, ?, ?, ?)
            """, (
                contract.contract_id,
                event.event_type,
                event.data.get("description", ""),
                json.dumps(event.data)
            ))
            
    db.commit()


def _load_contract(contract_id: str) -> Optional[MaxoContract]:
    """Reconstruye un objeto MaxoContract desde la base de datos."""
    db = get_db()
    
    # 1. Load header
    row = db.execute("SELECT * FROM maxo_contracts WHERE contract_id = ?", (contract_id,)).fetchone()
    if not row:
        return None
    
    contract = MaxoContract(
        contract_id=row["contract_id"],
        description=row["civil_description"],
        civil_summary=row["civil_description"]
    )
    contract._state = ContractState(row["state"])
    if row["parent_contract_id"]:
        contract._parent_contract_id = row["parent_contract_id"]
    if row["creator_user_id"]:
        contract._creator_user_id = row["creator_user_id"]
    if row["signature_deadline"]:
        contract._signature_deadline = row["signature_deadline"]
    if row["min_reflection_hours"]:
        contract._min_reflection_hours = row["min_reflection_hours"]
    if row["created_at"]:
        contract._created_at = row["created_at"]
    
    # 2. Load participants
    p_rows = db.execute("SELECT * FROM maxo_contract_participants WHERE contract_id = ?", (contract_id,)).fetchall()
    for p_row in p_rows:
        participant = _get_or_create_participant_by_pid(p_row["participant_id"])
        if participant:
            participant.update_wellness(Decimal(str(p_row["wellness_value"])))
            # Restaurar estado SDV-S persistido (T13: el registro es la verdad)
            if participant.is_synthetic and p_row["sdv_status"] and p_row["sdv_status"] != "ok":
                try:
                    state = json.loads(p_row["sdv_status"])
                    kwargs = {
                        dim: Decimal(str(state[dim]))
                        for dim in SDV_S.DIMENSIONS
                        if dim in state
                    }
                    participant.update_sdv_s(SDV_S(**kwargs))
                except (ValueError, TypeError, json.JSONDecodeError):
                    pass  # estado corrupto: mantener SDV-S por defecto
            # Rehidratación: append directo al participante. NO usar
            # add_participant() (el core exige estado DRAFT) — reconstruir
            # desde la BD no es una mutación de diseño y el estado ya fue
            # restaurado (un contrato ACTIVE debe volver a cargarse igual).
            contract.participants.append(participant)

    # Auto-curación del γ agregado (Ext. 3): si los miembros están en el
    # contrato, el bienestar de la parte colectiva es su media ponderada,
    # aunque la fila se haya escrito antes de esta extensión.
    wellness_map = {p.id: p.wellness_current.value for p in contract.participants}
    for p in contract.participants:
        if p.id.startswith(("society-", "coop-", "org-", "eco-")):
            agg = aggregate_wellness(p.id, wellness_map)
            if agg is not None:
                p.update_wellness(agg)

    # 3. Load terms
    t_rows = db.execute("SELECT * FROM maxo_contract_terms WHERE contract_id = ?", (contract_id,)).fetchall()
    for t_row in t_rows:
        term = ContractTerm(
            id=t_row["term_id"],
            description=t_row["civil_text"],
            vhv_cost=VHV(
                T=Decimal(str(t_row["vhv_t"])),
                V=Decimal(str(t_row["vhv_v"])),
                R=Decimal(str(t_row["vhv_h"]))
            )
        )
        term.assigned_participant = t_row["assigned_participant"]
        
        # Load approvals for this term
        a_rows = db.execute(
            "SELECT participant_id FROM maxo_contract_term_approvals WHERE contract_id = ? AND term_id = ?",
            (contract_id, term.id)
        ).fetchall()
        for a_row in a_rows:
            term.accepted_by[a_row["participant_id"]] = True

        # Rehidratar consentimiento agregado (Fase 2 + Ext. 3): si el quórum
        # de una parte colectiva se cumplió, su aceptación sigue vigente;
        # si la configuración cambió (miembros/pesos/deadline), el sello se
        # revisa y se revoca automáticamente (re-consulta).
        d_rows = db.execute(
            """
            SELECT party_id, delegate_id FROM maxo_contract_delegate_approvals
            WHERE contract_id = ? AND term_id = ?
            """,
            (contract_id, term.id)
        ).fetchall()
        delegated = {}
        for d_row in d_rows:
            delegated.setdefault(d_row["party_id"], []).append(d_row["delegate_id"])
        for party_pid, delegates in delegated.items():
            status = consent_status(party_pid, delegates, term_id=term.id)
            term.accepted_by[party_pid] = bool(status.get("approved"))
            
        contract._terms.append(term)
        # Note: add_term normally adds VHV, but we are rehydrating, so we just append
        # To keep total_vhv consistent, we recalculate it
        
    contract._total_vhv = VHV(
        T=Decimal(str(row["total_vhv_t"])),
        V=Decimal(str(row["total_vhv_v"])),
        R=Decimal(str(row["total_vhv_h"]))
    )

    # T9 ejecutable (Ola 3A.4): el flag de asimetría condiciona la activación.
    flag, report = _reciprocity_imbalance(contract)
    contract._asymmetry_flag = flag
    contract._asymmetry_report = report
    
    return contract


def _get_or_create_participant_by_pid(pid: str) -> Optional[Participant]:
    """Obtiene un participante por su party_id (user-, synthetic-, society-,
    coop-, org-, eco-). Delega en el registro de escalas (app/parties.py)."""
    return resolve_participant_by_pid(pid)


def _sdv_s_summary(participant: Participant) -> Dict[str, Any]:
    """
    Resumen SDV-S de un participante sintético para la API (T13).

    Incluye: estado por dimensión, magnitud de violación ponderada y el
    Factor de Sufrimiento Sintético FS_S = e^v (base neutra 1.0) que
    multiplica el costo en Maxos de los servicios que lo usan.
    """
    if not participant.is_synthetic or participant.sdv_s_actual is None:
        return {}
    validator = SDV_SValidatorBlock()
    result = validator.validate(participant)
    return {
        "sdv_s": {
            dim: float(getattr(participant.sdv_s_actual, dim))
            for dim in SDV_S.DIMENSIONS
        },
        "sdv_s_violations": [
            v.to_dict() for v in result.violations
        ],
        "sdv_s_magnitude": float(result.violation_magnitude),
        "fs_s": float(result.suffering_factor),
        "sdv_s_status": "ok" if result.is_valid else "violated"
    }


def _get_or_create_participant(user_id: int) -> Participant:
    """Obtiene o crea un participante humano desde la base de datos."""
    return get_human_participant(user_id)


def _resolve_party_from_payload(p_data: Dict[str, Any], owner: Optional[int] = None) -> Optional[Participant]:
    """
    Resuelve una parte desde el payload de un participante, soportando
    todas las escalas (ROADMAP Bloque B):

      {"user_id": 5, ...}                            -> humano (legacy)
      {"participant_id": "qwen-1", "synthetic": {}}  -> sintética (legacy)
      {"party_id": "coop-7", ...}                    -> cualquier escala

    Si la parte colectiva no existe aún en maxo_parties y el payload trae
    party_type/display_name, se auto-crea (upsert) en el registro con el
    actor del token como owner (Ola 3A.3).
    """
    if p_data.get("party_id"):
        pid = str(p_data["party_id"])
        if not is_valid_party_id(pid):
            return None
        if is_collective(pid):
            party = get_party(pid)
            if party is None:
                ptype = party_type_of(pid)
                display_name = (p_data.get("display_name") or "").strip() or pid
                from .parties import upsert_party
                upsert_party(
                    party_id=pid,
                    party_type=ptype,
                    display_name=display_name,
                    parent_party_id=p_data.get("parent_party_id"),
                    members=p_data.get("members") if isinstance(p_data.get("members"), dict) else None,
                    owner=owner,
                )
        return resolve_participant_by_pid(pid)

    p_id = p_data.get("user_id")
    if p_id:
        return _get_or_create_participant(p_id)

    agent_id = p_data.get("participant_id")
    if agent_id and (p_data.get("synthetic") is not None or p_data.get("realm") == "synthetic"):
        return _synthetic_participant(agent_id, p_data.get("synthetic") or {})
    return None


def _apply_wellness(participant: Participant, p_data: Dict[str, Any]) -> Optional[str]:
    """Aplica wellness/gamma al participante con tope defensivo (Ola 3A.5).

    γ ∈ [0.5, 1.5]; fuera de rango -> mensaje de error (400 en la API).
    """
    wellness_val = p_data.get("wellness", p_data.get("gamma"))
    if wellness_val is None:
        return None
    try:
        value = Decimal(str(wellness_val))
    except (ValueError, TypeError):
        return "invalid wellness value"
    if value < WELLNESS_MIN or value > WELLNESS_MAX:
        return f"wellness fuera de rango [{WELLNESS_MIN}, {WELLNESS_MAX}]"
    participant.update_wellness(value)
    return None


@contracts_bp.route("/", methods=["POST"])
@token_required
def create_contract(current_user):
    """
    Crear un nuevo MaxoContract.

    Body JSON:
    {
        "contract_id": "loan-001",
        "civil_description": "Préstamo de 10 Maxos entre amigos",
        "signature_deadline": "2026-09-01T23:59:59",   # opcional (Ola 3A.7)
        "min_reflection_hours": 24                      # opcional (Ola 3A.7)
    }

    Blindaje (Ola 3A): el creador queda registrado (3A.2) y un contract_id
    existente fuera de DRAFT del mismo creador se rechaza con 409 (R2).
    """
    data = request.get_json() or {}
    token_uid = _token_uid(current_user)

    contract_id = data.get("contract_id")
    if not contract_id:
        return jsonify({"error": "contract_id is required"}), 400

    civil_description = data.get("civil_description", "")

    # Inmutabilidad (Ola 3A.2, R2): re-crear un contrato ajeno/activo = 409
    db = get_db()
    existing = db.execute(
        "SELECT state, creator_user_id FROM maxo_contracts WHERE contract_id = ?",
        (contract_id,),
    ).fetchone()
    if existing is not None:
        creator = existing["creator_user_id"]
        if existing["state"] != "draft" or (creator is not None and creator != token_uid):
            return jsonify({
                "error": "el contrato ya existe y no es un borrador editable del mismo creador",
                "code": "CONTRACT_CONFLICT",
            }), 409

    contract = MaxoContract(
        contract_id=contract_id,
        description=civil_description,
        civil_summary=civil_description
    )
    contract._creator_user_id = token_uid

    # Batch creation support: add participants
    # Formas aceptadas por participante:
    #   {"user_id": 5, ...}                          -> humano
    #   {"participant_id": "qwen-1", "synthetic": {}} -> persona sintética (SDV-S)
    #   {"participant_id": "qwen-1", "realm": "synthetic"} -> sintética con SDV-S default
    #   {"party_id": "coop-7", "party_type": "cooperative", "display_name": ...} -> cualquier escala (Bloque B)
    participants_data = data.get("participants", [])
    for p_data in participants_data:
        participant = _resolve_party_from_payload(p_data, owner=token_uid)
        if participant:
            err = _apply_wellness(participant, p_data)
            if err:
                return jsonify({"error": err}), 400
            contract.add_participant(participant)
            continue

    # Batch creation support: add terms
    _attach_terms(contract, data.get("terms", []))

    # Lenguaje civil enforceable (Ola 3A.6, R8)
    desc_err = _validate_civil_text(civil_description)
    if desc_err:
        return jsonify({"error": f"civil_description: {desc_err}"}), 400
    for term in contract._terms:
        term_err = _validate_civil_text(term.description)
        if term_err:
            return jsonify({"error": f"término {term.id}: {term_err}"}), 400

    # Obligaciones sin parte responsable (Ola 3A.6, R9): si el contrato pesa
    # ≥ 10h, cada término con costo T > 0 debe tener parte obligada.
    if contract.total_vhv.T >= ASSIGNED_REQUIRED_MIN_TOTAL:
        for term in contract._terms:
            if term.vhv_cost.T > 0 and not getattr(term, "assigned_participant", None):
                return jsonify({
                    "error": f"término {term.id} sin parte obligada (assigned_participant_id) "
                             f"en contrato de ≥ {ASSIGNED_REQUIRED_MIN_TOTAL}h",
                    "code": "UNASSIGNED_OBLIGATION",
                }), 400

    # T9: flag de asimetría (Ola 3A.4) + ventana de reflexión por defecto
    flag, report = _reciprocity_imbalance(contract)
    contract._asymmetry_flag = flag
    contract._asymmetry_report = report
    contract._signature_deadline = data.get("signature_deadline")
    reflection = data.get("min_reflection_hours")
    if reflection is None:
        # La asimetría declarada exige reflexión por defecto (24h)
        contract._min_reflection_hours = 24 if flag else 0
    else:
        try:
            contract._min_reflection_hours = max(0.0, float(reflection))
        except (ValueError, TypeError):
            return jsonify({"error": "invalid min_reflection_hours"}), 400

    # Contratos interescala anidados (Fase 5): un contrato puede declararse
    # sub-contrato de un contrato madre existente.
    parent_id = data.get("parent_contract_id")
    if parent_id:
        err = _attach_parent(contract, parent_id)
        if err:
            return err

    _audit(contract, "contract_created", token_uid, asymmetry=report)
    _save_contract(contract, actor_id=token_uid)
    
    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "state": contract.state.value,
        "created_at": datetime.now().isoformat(),
        "asymmetry": report,
        "requires_asymmetry_acknowledgment": flag,
        "min_reflection_hours": contract._min_reflection_hours,
    }), 201


def _attach_terms(contract: MaxoContract, terms_data: List[Dict[str, Any]]) -> None:
    """Añade los términos del payload a un contrato (creación batch)."""
    for t_data in terms_data:
        t_id = t_data.get("term_id")
        t_civil = t_data.get("civil_text", "")
        t_vhv = t_data.get("vhv", {})
        if t_id:
            try:
                vhv = VHV(
                    T=Decimal(str(t_vhv.get("t", 0))),
                    V=Decimal(str(t_vhv.get("v", 0))),
                    R=Decimal(str(t_vhv.get("h", 0)))
                )
                term = ContractTerm(id=t_id, description=t_civil, vhv_cost=vhv)
                term.assigned_participant = t_data.get("assigned_participant_id")
                contract.add_term(term)
            except Exception:
                pass


def _attach_parent(contract: MaxoContract, parent_id: str):
    """
    Vincula un contrato a su contrato madre (Fase 5 / Ext. 4).
    Devuelve un jsonify de error (para retornar) o None si todo va bien.
    """
    db = get_db()
    parent = db.execute(
        "SELECT contract_id FROM maxo_contracts WHERE contract_id = ?", (parent_id,)
    ).fetchone()
    if parent is None:
        return jsonify({"error": f"parent contract {parent_id} not found"}), 400
    # Protección de ciclos: el padre no puede ser descendiente del nuevo.
    node = parent_id
    while node:
        if node == contract.contract_id:
            return jsonify({"error": "parent_contract_id crearía un ciclo de contratos"}), 400
        node = db.execute(
            "SELECT parent_contract_id FROM maxo_contracts WHERE contract_id = ?", (node,)
        ).fetchone()
        node = node["parent_contract_id"] if node else None
    contract._parent_contract_id = parent_id
    contract._log_event("subcontract_created", {
        "parent_contract_id": parent_id,
        "child_contract_id": contract.contract_id,
    })
    return None


def _build_contract_tree(cid: str, db, depth: int = 0) -> Dict[str, Any]:
    """Árbol recursivo de sub-contratos (Ext. 4), con guarda de profundidad."""
    if depth > 10:
        return {"contract_id": cid, "truncated": True, "subcontracts": []}
    children = [
        r["contract_id"]
        for r in db.execute(
            "SELECT contract_id FROM maxo_contracts WHERE parent_contract_id = ? ORDER BY created_at",
            (cid,),
        ).fetchall()
    ]
    return {
        "contract_id": cid,
        "subcontracts": [_build_contract_tree(c, db, depth + 1) for c in children],
    }


def _asymmetry_acknowledged(contract_id: str) -> List[str]:
    """Reconocimientos de asimetría registrados del contrato (Ola 3A.4)."""
    try:
        row = get_db().execute(
            "SELECT meta_value FROM maxo_contract_meta WHERE contract_id = ? AND meta_key = 'asymmetry_acknowledged'",
            (contract_id,),
        ).fetchone()
    except Exception:
        return []
    if not row or not row["meta_value"]:
        return []
    try:
        parsed = json.loads(row["meta_value"])
        return parsed if isinstance(parsed, list) else []
    except (ValueError, TypeError):
        return []


@contracts_bp.route("/<contract_id>/subcontracts", methods=["POST"])
@token_required
def create_subcontract(current_user, contract_id: str):
    """
    Crear un sub-contrato bajo un contrato madre existente (Fase 5 / Ext. 4).

    Body JSON: igual que POST /contracts/ pero sin parent_contract_id
    (el padre es la URL). Conveniente para la vista jerárquica.
    """
    parent = _load_contract(contract_id)
    if parent is None:
        return jsonify({"error": "contract not found"}), 404

    token_uid = _token_uid(current_user)
    data = request.get_json() or {}
    child_id = data.get("contract_id")
    if not child_id:
        return jsonify({"error": "contract_id is required"}), 400

    contract = MaxoContract(
        contract_id=child_id,
        description=data.get("civil_description", ""),
        civil_summary=data.get("civil_description", "")
    )
    contract._creator_user_id = token_uid
    for p_data in data.get("participants", []):
        participant = _resolve_party_from_payload(p_data, owner=token_uid)
        if participant:
            err = _apply_wellness(participant, p_data)
            if err:
                return jsonify({"error": err}), 400
            contract.add_participant(participant)
    _attach_terms(contract, data.get("terms", []))
    desc_err = _validate_civil_text(contract.civil_summary)
    if desc_err:
        return jsonify({"error": f"civil_description: {desc_err}"}), 400
    for term in contract._terms:
        term_err = _validate_civil_text(term.description)
        if term_err:
            return jsonify({"error": f"término {term.id}: {term_err}"}), 400
    if contract.total_vhv.T >= ASSIGNED_REQUIRED_MIN_TOTAL:
        for term in contract._terms:
            if term.vhv_cost.T > 0 and not getattr(term, "assigned_participant", None):
                return jsonify({"error": f"término {term.id} sin parte obligada",
                                "code": "UNASSIGNED_OBLIGATION"}), 400
    flag, report = _reciprocity_imbalance(contract)
    contract._asymmetry_flag = flag
    contract._asymmetry_report = report
    contract._min_reflection_hours = 24 if flag else 0
    err = _attach_parent(contract, contract_id)
    if err:
        return err
    _audit(contract, "contract_created", token_uid, parent=contract_id, asymmetry=report)
    _save_contract(contract, actor_id=token_uid)
    return jsonify({
        "success": True,
        "contract_id": child_id,
        "parent_contract_id": contract_id,
        "state": contract.state.value,
    }), 201


@contracts_bp.route("/<contract_id>/tree", methods=["GET"])
@token_required
def get_contract_tree(current_user, contract_id: str):
    """
    Vista jerárquica del contrato (Ext. 4): ancestros (camino al tronco)
    y árbol completo de sub-contratos (madre -> hijos -> nietos...).
    """
    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    db = get_db()
    ancestors = []
    node = getattr(contract, "_parent_contract_id", None)
    while node:
        ancestors.append(node)
        row = db.execute(
            "SELECT parent_contract_id FROM maxo_contracts WHERE contract_id = ?", (node,)
        ).fetchone()
        node = row["parent_contract_id"] if row else None
        if len(ancestors) > 20:
            break

    return jsonify({
        "contract_id": contract_id,
        "ancestors": ancestors,
        "tree": _build_contract_tree(contract_id, db),
    })


def _live_oracle_or_503():
    """Instancia el oráculo en vivo; si no está disponible responde 503
    con degradación elegante (el resto de la API sigue funcionando)."""
    oracle = LiveOracle()
    if not oracle.is_available():
        return None, jsonify({
            "error": "La negociación asistida por oráculo no está disponible.",
            "code": "ORACLE_UNAVAILABLE",
            "hint": "Configura DEEPSEEK_API_KEY en el .env para activarla.",
        }), 503
    return oracle, None, None


@contracts_bp.route("/negotiate", methods=["POST"])
@token_required
def negotiate_with_oracle(current_user):
    """
    Negociación Asistida por Oráculo (ROADMAP Bloque A).
    El oráculo en vivo (DeepSeek, protocolo OpenAI-compatible) genera un
    borrador de MaxoContract desde una instrucción en lenguaje natural.

    Body JSON:
    {
        "instruction": "Max ofrece 10 horas y quiere que Ana dé un objeto, un servicio o sus horas",
        "participants": ["user-1", "user-2"],   # opcional
        "session_id": "abc123"                   # opcional (para iterar)
    }
    """
    oracle, error_response, status = _live_oracle_or_503()
    if oracle is None:
        return error_response, status

    data = request.get_json() or {}
    instruction = (data.get("instruction") or "").strip()
    if not instruction:
        return jsonify({"error": "instruction is required"}), 400

    participants = data.get("participants") or []
    session_id = data.get("session_id")

    try:
        result = oracle.negotiate(
            instruction=instruction,
            participants=[str(p) for p in participants],
            session_id=session_id,
        )
    except OracleAPIError as e:
        return jsonify({"error": f"El oráculo falló: {e}"}), 502
    except OracleUnavailableError as e:
        return jsonify({"error": str(e), "code": "ORACLE_UNAVAILABLE"}), 503

    return jsonify(result.to_dict()), 200


@contracts_bp.route("/negotiate/feedback", methods=["POST"])
@token_required
def negotiate_oracle_feedback(current_user):
    """
    Iteración de la negociación: la contraparte responde al borrador y el
    oráculo produce una nueva versión (sesiones en memoria, TTL 30 min).

    Body JSON:
    {
        "session_id": "abc123",
        "feedback": "Ana no puede dar más de 5 horas; sugiere un servicio de diseño"
    }
    """
    oracle, error_response, status = _live_oracle_or_503()
    if oracle is None:
        return error_response, status

    data = request.get_json() or {}
    session_id = (data.get("session_id") or "").strip()
    feedback = (data.get("feedback") or "").strip()

    if not session_id:
        return jsonify({"error": "session_id is required"}), 400
    if not feedback:
        return jsonify({"error": "feedback is required"}), 400

    try:
        result = oracle.feedback(session_id, feedback)
    except KeyError:
        return jsonify({"error": f"session {session_id} not found"}), 404
    except OracleAPIError as e:
        return jsonify({"error": f"El oráculo falló: {e}"}), 502
    except OracleUnavailableError as e:
        return jsonify({"error": str(e), "code": "ORACLE_UNAVAILABLE"}), 503

    return jsonify(result.to_dict()), 200


def _contract_snapshot(contract: MaxoContract) -> Dict[str, Any]:
    """Snapshot JSON de un contrato para auditorías del oráculo."""
    return {
        "contract_id": contract.contract_id,
        "state": contract.state.value,
        "civil_description": contract.civil_summary,
        "participants": [
            {
                "id": p.id,
                "name": p.name,
                "wellness": float(p.wellness_current.value),
                "is_synthetic": p.is_synthetic,
            }
            for p in contract.participants
        ],
        "terms": [
            {
                "term_id": t.id,
                "civil_text": t.description,
                "vhv": {
                    "t": float(t.vhv_cost.T),
                    "v": float(t.vhv_cost.V),
                    "r": float(t.vhv_cost.R),
                },
                "assigned_participant": t.assigned_participant,
            }
            for t in contract._terms
        ],
        "total_vhv": {
            "t": float(contract.total_vhv.T),
            "v": float(contract.total_vhv.V),
            "r": float(contract.total_vhv.R),
        },
    }


def _guardian_approve_ecosystem(contract: MaxoContract) -> tuple:
    """
    Guardián del Reino Natural (ROADMAP Bloque B, Fase 4).

    El ecosistema (eco-*) es representado por un guardián oráculo que
    audita el contrato contra los invariantes (γ, SDV, T9) antes de dar
    su consentimiento. Si el oráculo en vivo está configurado, su auditoría
    es la fuente de verdad; si no, degradación elegante al oráculo
    heurístico (validación axiomática dura).
    """
    is_valid, results = contract.validate()
    if not is_valid:
        failed = ", ".join(r.axiom_code for r in results if not r.is_valid)
        return False, f"Invariantes axiomáticos fallan: {failed}"

    oracle = LiveOracle()
    if oracle.is_available():
        try:
            critique = oracle.critique(contract.contract_id, _contract_snapshot(contract))
            if critique.valid:
                return True, f"Oráculo en vivo: {critique.reasoning}"
            return False, f"Oráculo en vivo rechaza la representación: {critique.reasoning}"
        except (OracleAPIError, OracleUnavailableError):
            pass  # degradación elegante: continuar con el heurístico

    return True, "Oráculo heurístico: invariantes axiomáticos en orden (γ, SDV, T9)."


@contracts_bp.route("/<contract_id>/critique", methods=["POST"])
@token_required
def critique_contract(current_user, contract_id: str):
    """
    Auditoría del oráculo: revisa un contrato existente contra T13, INV2/
    INV2-S, T9, γ ≥ 1 y la Capa de Ternura, y propone mejoras.
    """
    oracle, error_response, status = _live_oracle_or_503()
    if oracle is None:
        return error_response, status

    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    contract_data = _contract_snapshot(contract)

    try:
        result = oracle.critique(contract_id, contract_data)
    except OracleAPIError as e:
        return jsonify({"error": f"El oráculo falló: {e}"}), 502
    except OracleUnavailableError as e:
        return jsonify({"error": str(e), "code": "ORACLE_UNAVAILABLE"}), 503

    return jsonify(result.to_dict()), 200


@contracts_bp.route("/stats", methods=["GET"])
@token_required
def contract_stats(current_user):
    """
    Métricas agregadas de MaxoContracts para el dashboard de la Cohorte Cero.

    Devuelve:
    - summary: totales y conteo por estado
    - gamma: promedio/mínimo de bienestar (γ) y distribución de participantes
    - sdv: violaciones del Suelo de Dignidad Vital (humanos y sintéticos)
    - nps: Net Promoter Score y distribución de respuestas
    - trends: contratos creados y activados por semana (últimas 8 semanas)
    - categories: desglose por categoría (aseo, prestamo, comida, otros)
    - vhv: totales agregados de T, V, R
    """
    db = get_db()

    # --- Summary por estado ---
    state_rows = db.execute(
        "SELECT state, COUNT(*) AS n FROM maxo_contracts GROUP BY state"
    ).fetchall()
    by_state = {row["state"]: row["n"] for row in state_rows}
    total = sum(by_state.values())

    # --- Gamma (bienestar) de participantes ---
    gamma_rows = db.execute(
        """
        SELECT cp.participant_id, cp.wellness_value, cp.contract_id, c.state
        FROM maxo_contract_participants cp
        JOIN maxo_contracts c ON c.contract_id = cp.contract_id
        """
    ).fetchall()

    wellness_values = [row["wellness_value"] for row in gamma_rows]
    gamma_distribution = {
        "lt_05": sum(1 for v in wellness_values if v < 0.5),
        "05_08": sum(1 for v in wellness_values if 0.5 <= v < 0.8),
        "08_10": sum(1 for v in wellness_values if 0.8 <= v < 1.0),
        "10_12": sum(1 for v in wellness_values if 1.0 <= v < 1.2),
        "gte_12": sum(1 for v in wellness_values if v >= 1.2),
    }

    gamma_alerts = []
    seen_alerts = set()
    for row in gamma_rows:
        if row["wellness_value"] < 1.0:
            key = (row["contract_id"], row["participant_id"])
            if key not in seen_alerts:
                seen_alerts.add(key)
                gamma_alerts.append({
                    "contract_id": row["contract_id"],
                    "contract_state": row["state"],
                    "participant_id": row["participant_id"],
                    "gamma": row["wellness_value"],
                })
    gamma_alerts.sort(key=lambda a: a["gamma"])

    # --- SDV: violaciones ---
    sdv_rows = db.execute(
        """
        SELECT cp.contract_id, cp.participant_id, cp.sdv_status, c.state
        FROM maxo_contract_participants cp
        JOIN maxo_contracts c ON c.contract_id = cp.contract_id
        WHERE cp.sdv_status IS NOT NULL AND cp.sdv_status != 'ok'
        """
    ).fetchall()

    sdv_violations = []
    for row in sdv_rows:
        status = row["sdv_status"]
        detail = None
        try:
            parsed = json.loads(status)
            detail = parsed
        except (ValueError, TypeError):
            pass
        sdv_violations.append({
            "contract_id": row["contract_id"],
            "contract_state": row["state"],
            "participant_id": row["participant_id"],
            "status": detail if detail is not None else status,
        })

    # --- NPS ---
    nps_rows = db.execute(
        "SELECT score, comment, contract_id, participant_id FROM maxo_contract_nps"
    ).fetchall()
    nps_scores = [row["score"] for row in nps_rows]
    nps = None
    nps_distribution = {"detractors": 0, "passives": 0, "promoters": 0}
    if nps_scores:
        n_detractors = sum(1 for s in nps_scores if s <= 6)
        n_passives = sum(1 for s in nps_scores if s in (7, 8))
        n_promoters = sum(1 for s in nps_scores if s >= 9)
        nps_distribution = {
            "detractors": n_detractors,
            "passives": n_passives,
            "promoters": n_promoters,
        }
        nps = round(
            ((n_promoters - n_detractors) / len(nps_scores)) * 100.0, 1
        )

    nps_responses = [
        {
            "contract_id": row["contract_id"],
            "participant_id": row["participant_id"],
            "score": row["score"],
            "comment": row["comment"],
        }
        for row in nps_rows
    ]

    # --- Tendencias: últimas 8 semanas ---
    from datetime import timedelta

    weeks_created = []
    weeks_activated = []
    week_labels = []
    for w in range(7, -1, -1):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = today - timedelta(days=w * 7)
        end = start + timedelta(days=7)
        label = start.strftime("%d/%m")
        week_labels.append(label)

        created = db.execute(
            "SELECT COUNT(*) FROM maxo_contracts WHERE created_at >= ? AND created_at < ?",
            (start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")),
        ).fetchone()[0]

        # Activaciones: eventos state_changed con metadata 'to': 'ACTIVE'
        events = db.execute(
            """
            SELECT metadata_json FROM maxo_contract_events
            WHERE event_type = 'state_changed'
              AND created_at >= ? AND created_at < ?
            """,
            (start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")),
        ).fetchall()
        activated = sum(
            1
            for e in events
            if e["metadata_json"]
            and json.loads(e["metadata_json"]).get("to") == "ACTIVE"
        )

        weeks_created.append(created)
        weeks_activated.append(activated)

    # --- Categorías (meta) ---
    cat_rows = db.execute(
        "SELECT meta_value, COUNT(*) AS n FROM maxo_contract_meta WHERE meta_key = 'category' GROUP BY meta_value"
    ).fetchall()
    categories = {row["meta_value"]: row["n"] for row in cat_rows}

    # --- VHV totales ---
    vhv_row = db.execute(
        """
        SELECT
            COALESCE(SUM(total_vhv_t), 0) AS t,
            COALESCE(SUM(total_vhv_v), 0) AS v,
            COALESCE(SUM(total_vhv_h), 0) AS r
        FROM maxo_contracts
        """
    ).fetchone()

    return jsonify({
        "summary": {
            "total": total,
            "by_state": by_state,
        },
        "gamma": {
            "sample_count": len(wellness_values),
            "avg": round(sum(wellness_values) / len(wellness_values), 3) if wellness_values else None,
            "min": round(min(wellness_values), 3) if wellness_values else None,
            "max": round(max(wellness_values), 3) if wellness_values else None,
            "distribution": gamma_distribution,
            "alerts": gamma_alerts,
        },
        "sdv": {
            "violations_count": len(sdv_violations),
            "violations": sdv_violations,
        },
        "nps": {
            "score": nps,
            "responses_count": len(nps_scores),
            "distribution": nps_distribution,
            "responses": nps_responses,
        },
        "trends": {
            "labels": week_labels,
            "created": weeks_created,
            "activated": weeks_activated,
        },
        "categories": categories,
        "vhv": {
            "t": round(float(vhv_row["t"]), 2),
            "v": round(float(vhv_row["v"]), 2),
            "r": round(float(vhv_row["r"]), 2),
        },
    })


@contracts_bp.route("/<contract_id>/nps", methods=["POST"])
@token_required
def record_nps(current_user, contract_id: str):
    """
    Registrar la puntuación NPS (0-10) de un participante sobre un contrato.

    Body JSON:
    {
        "participant_id": "user-3",   # obligatorio
        "score": 9,                    # 0-10, obligatorio
        "comment": "Resolvimos todo sin fricción"  # opcional
    }

    El participante debe existir en el contrato (T13: el registro es la verdad).
    """
    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    data = request.get_json() or {}
    participant_id = data.get("participant_id")
    score = data.get("score")

    if not participant_id:
        return jsonify({"error": "participant_id is required"}), 400

    if participant_id not in contract.participant_ids:
        return jsonify({"error": f"participant {participant_id} not in contract"}), 400

    # Identidad vinculada (Ola 3A.1): el NPS solo se reporta por sí mismo,
    # como delegado de su colectiva o como operador de una sintética.
    if not _can_act_for(participant_id, _token_uid(current_user), contract):
        return jsonify({"error": "no puedes reportar NPS por esta parte",
                        "code": "IDENTITY_MISMATCH"}), 403

    try:
        score_int = int(score)
    except (TypeError, ValueError):
        return jsonify({"error": "score must be an integer between 0 and 10"}), 400

    if score_int < 0 or score_int > 10:
        return jsonify({"error": "score must be an integer between 0 and 10"}), 400

    comment = (data.get("comment") or "").strip()

    db = get_db()
    db.execute(
        """
        INSERT INTO maxo_contract_nps (contract_id, participant_id, score, comment)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(contract_id, participant_id) DO UPDATE SET
            score = excluded.score,
            comment = excluded.comment,
            created_at = CURRENT_TIMESTAMP
        """,
        (contract_id, participant_id, score_int, comment),
    )
    db.commit()

    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "participant_id": participant_id,
        "score": score_int,
    }), 201


@contracts_bp.route("/<contract_id>/meta", methods=["POST"])
@token_required
def set_contract_meta(current_user, contract_id: str):
    """
    Guardar un metadato del contrato (ej. categoria: aseo | prestamo | comida).

    Body JSON:
    {
        "key": "category",
        "value": "aseo"
    }
    """
    db = get_db()
    exists = db.execute(
        "SELECT 1 FROM maxo_contracts WHERE contract_id = ?", (contract_id,)
    ).fetchone()
    if not exists:
        return jsonify({"error": "contract not found"}), 404

    data = request.get_json() or {}
    key = (data.get("key") or "").strip()
    value = (data.get("value") or "").strip()

    if not key or not value:
        return jsonify({"error": "key and value are required"}), 400

    db.execute(
        """
        INSERT INTO maxo_contract_meta (contract_id, meta_key, meta_value)
        VALUES (?, ?, ?)
        ON CONFLICT(contract_id, meta_key) DO UPDATE SET
            meta_value = excluded.meta_value
        """,
        (contract_id, key, value),
    )
    db.commit()

    return jsonify({"success": True, "contract_id": contract_id, "key": key, "value": value})


@contracts_bp.route("/<contract_id>", methods=["GET"])
@token_required
def get_contract(current_user, contract_id: str):
    """Obtener detalles de un contrato."""
    if contract_id == "builder":
        # Evitar conflicto con la ruta del frontend
        return jsonify({"error": "This is a frontend route"}), 404
        
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    # Preparar VHV para JSON
    vhv = {
        "t": float(contract.total_vhv.T),
        "v": float(contract.total_vhv.V),
        "r": float(contract.total_vhv.R)
    }
    
    import hashlib
    # Generar un hash simplificado para inmutabilidad local
    hash_payload = f"{contract.contract_id}:{contract.state.value}:{contract.total_vhv.T}:{contract.total_vhv.V}:{contract.total_vhv.R}:{len(contract._terms)}".encode('utf-8')
    contract_hash = hashlib.sha256(hash_payload).hexdigest()

    db = get_db()
    parent_contract_id = getattr(contract, "_parent_contract_id", None)
    subcontract_rows = db.execute(
        "SELECT contract_id FROM maxo_contracts WHERE parent_contract_id = ? ORDER BY created_at",
        (contract.contract_id,),
    ).fetchall() if db is not None else []
    
    return jsonify({
        "contract_id": contract.contract_id,
        "state": contract.state.value,
        "civil_description": contract.civil_summary,
        "parent_contract_id": parent_contract_id,
        "subcontracts": [r["contract_id"] for r in subcontract_rows],
        "creator_user_id": getattr(contract, "_creator_user_id", None),
        "signature_deadline": getattr(contract, "_signature_deadline", None),
        "min_reflection_hours": getattr(contract, "_min_reflection_hours", 0),
        "asymmetry": getattr(contract, "_asymmetry_report", None),
        "requires_asymmetry_acknowledgment": bool(getattr(contract, "_asymmetry_flag", False)),
        "asymmetry_acknowledged": _asymmetry_acknowledged(contract_id),
        "participants": [p.id for p in contract.participants],
        "participants_details": [
            {
                "id": p.id,
                "name": p.name,
                "party_type": party_type_of(p.id),
                "is_collective": is_collective(p.id),
                "wellness": float(p.wellness_current.value),
                "is_synthetic": p.is_synthetic,
                **(
                    {"members": members_of(p.id)}
                    if is_collective(p.id) else {}
                ),
                **(
                    _sdv_s_summary(p)
                    if p.is_synthetic and p.sdv_s_actual is not None
                    else {}
                )
            }
            for p in contract.participants
        ],
        "terms": [
            {
                "term_id": t.id,
                "civil_text": t.description,
                "vhv": {
                    "t": float(t.vhv_cost.T),
                    "v": float(t.vhv_cost.V),
                    "r": float(t.vhv_cost.R)
                },
                "accepted_by": t.accepted_by,
                "assigned_participant": t.assigned_participant
            }
            for t in contract._terms
        ],
        "terms_count": len(contract._terms),
        "total_vhv": vhv,
        "events_count": len(contract.get_event_log()),
        "hash": contract_hash
    })


@contracts_bp.route("/<contract_id>/terms", methods=["POST"])
@token_required
def add_term(current_user, contract_id: str):
    """
    Añadir un término al contrato.
    
    Body JSON:
    {
        "term_id": "term-1",
        "civil_text": "Alice transfiere 10 Maxos a Bob",
        "vhv": {"t": 0.5, "v": 0, "h": 0}
    }
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    if contract.state != ContractState.DRAFT:
        return jsonify({"error": "contract not in draft state"}), 400
    
    data = request.get_json() or {}
    
    term_id = data.get("term_id")
    if not term_id:
        return jsonify({"error": "term_id is required"}), 400
    
    civil_text = data.get("civil_text", "")
    vhv_data = data.get("vhv", {})
    assigned_participant = data.get("assigned_participant_id")

    # Lenguaje civil enforceable (Ola 3A.6)
    text_err = _validate_civil_text(civil_text)
    if text_err:
        return jsonify({"error": f"civil_text: {text_err}"}), 400

    try:
        vhv = VHV(
            T=Decimal(str(vhv_data.get("t", 0))),
            V=Decimal(str(vhv_data.get("v", 0))),
            R=Decimal(str(vhv_data.get("h", 0)))
        )
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"invalid vhv format: {e}"}), 400

    # Obligaciones sin parte responsable (Ola 3A.6, R9)
    if (
        vhv.T > 0
        and contract.total_vhv.T + vhv.T >= ASSIGNED_REQUIRED_MIN_TOTAL
        and not assigned_participant
    ):
        return jsonify({
            "error": "término sin parte obligada (assigned_participant_id) en contrato de ≥ "
                     f"{ASSIGNED_REQUIRED_MIN_TOTAL}h",
            "code": "UNASSIGNED_OBLIGATION",
        }), 400

    term = ContractTerm(
        id=term_id,
        description=civil_text,
        vhv_cost=vhv
    )
    term.assigned_participant = assigned_participant

    contract.add_term(term)
    # Recalcular flag de asimetría (Ola 3A.4)
    flag, report = _reciprocity_imbalance(contract)
    contract._asymmetry_flag = flag
    contract._asymmetry_report = report
    _audit(contract, "term_added", _token_uid(current_user), term_id=term_id)
    _save_contract(contract, actor_id=_token_uid(current_user))
    
    return jsonify({
        "success": True,
        "term_id": term_id,
        "total_terms": len(contract._terms),
        "assigned_participant": assigned_participant
    })


@contracts_bp.route("/<contract_id>/participants", methods=["POST"])
@token_required
def add_participant(current_user, contract_id: str):
    """
    Añadir un participante al contrato.

    Body JSON:
    {
        "user_id": 123,
        "gamma": 1.2  (opcional, default 1.0)
    }

    Escalas (Bloque B): también acepta
    {"participant_id": "qwen-1", "synthetic": {}}  -> sintética
    {"party_id": "coop-7", "party_type": "cooperative", "display_name": ...}
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    if contract.state != ContractState.DRAFT:
        return jsonify({"error": "contract not in draft state"}), 400
    
    data = request.get_json() or {}
    token_uid = _token_uid(current_user)

    participant = _resolve_party_from_payload(data, owner=token_uid)
    if participant is None:
        return jsonify({
            "error": "user_id, participant_id (synthetic) or party_id is required"
        }), 400
    
    # Actualizar wellness si se proporciona (renombrado de gamma)
    # Soporte para "wellness" (nuevo estándar) y "gamma" (legacy)
    wellness_val = data.get("wellness")
    if wellness_val is None:
        wellness_val = data.get("gamma")

    if wellness_val is not None:
        err = _apply_wellness(participant, {"wellness": wellness_val})
        if err:
            return jsonify({"error": err}), 400
    
    contract.add_participant(participant)
    _audit(contract, "participant_added", token_uid, participant_id=participant.id)
    _save_contract(contract, actor_id=token_uid)
    # Fuente del γ (Ola 3A.5): el reporte queda atribuido al actor
    if wellness_val is not None:
        db = get_db()
        db.execute(
            """
            UPDATE maxo_contract_participants
            SET reported_by = ?, reported_at = ?
            WHERE contract_id = ? AND participant_id = ?
            """,
            (f"user-{token_uid}", datetime.now().isoformat(),
             contract_id, participant.id),
        )
        db.commit()
    
    return jsonify({
        "success": True,
        "participant_id": participant.id,
        "party_type": party_type_of(participant.id),
        "is_synthetic": participant.is_synthetic,
        "wellness": float(participant.wellness_current.value),
        "total_participants": len(contract.participants)
    })


@contracts_bp.route("/<contract_id>/validate", methods=["GET"])
@token_required
def validate_contract(current_user, contract_id: str):
    """Validar axiomas del contrato."""
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    valid, results = contract.validate()
    
    return jsonify({
        "contract_id": contract_id,
        "valid": valid,
        "validations": [
            {
                "axiom": r.axiom_code,
                "valid": r.is_valid,
                "message": r.message
            }
            for r in results
        ]
    })


@contracts_bp.route("/<contract_id>/accept", methods=["POST"])
@token_required
def accept_term(current_user, contract_id: str):
    """
    Aceptar un término del contrato.

    Body JSON:
    {
        "term_id": "term-1",
        "user_id": 123          # humano (legacy)
        # o
        "participant_id": "qwen-1"  # persona sintética (consentimiento, Cap. 10 §10.8)
        # o
        "party_id": "coop-7",       # cualquier escala (Bloque B)
        "delegate_id": "user-2"     # firma delegada (colectivas, Fase 2)
    }

    Partes colectivas (society-/coop-/org-): la firma es delegada; el quórum
    configurado en members_json decide el consentimiento agregado.
    Ecosistemas (eco-*): consentimiento otorgado por el guardián oráculo (Fase 4).
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    token_uid = _token_uid(current_user)
    if token_uid is None:
        return jsonify({"error": "token sin identidad válida"}), 403
    
    # Ventanas temporales server-side (Ola 3A.7, R10/R11)
    window_blocked = _contract_window_blocked(contract, get_db())
    if window_blocked:
        return jsonify(window_blocked), 423
    
    data = request.get_json() or {}
    term_id = data.get("term_id")
    user_id = data.get("user_id")
    participant_id = data.get("participant_id")
    party_id = data.get("party_id")
    delegate_id = data.get("delegate_id")
    
    if not term_id:
        return jsonify({"error": "term_id is required"}), 400
    
    if party_id:
        pid = str(party_id)
        if not is_valid_party_id(pid):
            return jsonify({"error": f"invalid party_id format: {party_id}"}), 400
    elif user_id:
        pid = f"user-{user_id}"
    elif participant_id:
        pid = f"synthetic-{participant_id}"
    else:
        return jsonify({"error": "user_id, participant_id or party_id is required"}), 400
    
    # El consentimiento solo es válido si el participante existe en el contrato
    if pid not in contract.participant_ids:
        return jsonify({"error": f"participant {pid} not in contract"}), 400

    # --- Identidad vinculada al token (Ola 3A.1, R1): el actor nunca se
    #     toma del cuerpo de la petición; solo puede firmar por sí mismo,
    #     como delegado de su colectiva, o como operador asistido de una
    #     sintética/ecosistema del que es participante. ---
    if party_type_of(pid) == "human" and pid != f"user-{token_uid}":
        return jsonify({"error": "solo puedes firmar por ti mismo", "code": "IDENTITY_MISMATCH"}), 403
    if is_collective(pid) and party_type_of(pid) != "ecosystem" and not members_of(pid).get("delegates"):
        return jsonify({
            "error": f"la parte {pid} no tiene delegados configurados en members_json"
        }), 409
    if not _can_act_for(pid, token_uid, contract):
        return jsonify({
            "error": "no puedes actuar por esta parte",
            "code": "IDENTITY_MISMATCH",
        }), 403

    # --- Ecosistema del Reino Natural: guardián oráculo (Fase 4) ---
    if party_type_of(pid) == "ecosystem":
        approved, reasoning = _guardian_approve_ecosystem(contract)
        if not approved:
            return jsonify({
                "error": "el guardián del Reino Natural no otorga consentimiento",
                "guardian_reasoning": reasoning,
            }), 400
        success = contract.accept_term(term_id, pid)
        _audit(contract, "term_accept_guardian", token_uid, term_id=term_id, party_id=pid)
        _save_contract(contract, actor_id=token_uid)
        return jsonify({
            "success": success,
            "term_id": term_id,
            "accepted_by": pid,
            "guardian": {"mode": "oracle_guardian", "reasoning": reasoning},
            "contract_state": contract.state.value
        })

    # --- Parte colectiva: consentimiento agregado por quórum (Fase 2) ---
    if is_collective(pid):
        members = members_of(pid)
        delegates = members.get("delegates") or []
        if not delegates:
            return jsonify({
                "error": f"la parte {pid} no tiene delegados configurados en members_json"
            }), 409
        # El delegado que firma es SIEMPRE el actor del token (Ola 3A.1)
        delegate_pid = f"user-{token_uid}"
        if delegate_pid not in delegates:
            return jsonify({
                "error": f"delegate {delegate_pid} no es delegado de {pid}"
            }), 403

        db = get_db()
        db.execute(
            """
            INSERT OR IGNORE INTO maxo_contract_delegate_approvals
                (contract_id, term_id, party_id, delegate_id)
            VALUES (?, ?, ?, ?)
            """,
            (contract_id, term_id, pid, delegate_pid),
        )
        db.commit()

        approved_rows = db.execute(
            """
            SELECT delegate_id FROM maxo_contract_delegate_approvals
            WHERE contract_id = ? AND term_id = ? AND party_id = ?
            """,
            (contract_id, term_id, pid),
        ).fetchall()
        consent = consent_status(pid, [r["delegate_id"] for r in approved_rows], term_id=term_id)

        # Ciclo de vida del quórum (Ext. 3): ventana de sellado vencida
        if consent.get("deadline_expired"):
            return jsonify({
                "error": "la ventana de quórum de esta parte venció; solicita una prórroga",
                "code": "QUORUM_EXPIRED",
                "consent": consent,
            }), 409

        if consent.get("approved"):
            success = contract.accept_term(term_id, pid)
            _save_contract(contract)
            # Evento de consentimiento agregado sellado: las partes
            # colectivas pueden vigilarse vía webhooks (filtrados por parte).
            dispatch_event("contract.quorum_sealed", {
                "contract_id": contract_id,
                "term_id": term_id,
                "party_id": pid,
                "delegates": consent.get("approved_delegates", []),
                "effective_delegates": consent.get("effective_delegates", []),
                "delegations_applied": consent.get("delegations_applied", {}),
                "current_weight": consent.get("current_weight"),
                "needed_weight": consent.get("needed_weight"),
                "sealed_at": datetime.now().isoformat(),
            }, party_ids=[pid])
        else:
            success = False

        return jsonify({
            "success": success,
            "term_id": term_id,
            "accepted_by": pid,
            "delegate_id": delegate_pid,
            "consent": consent,
            "quorum_reached": bool(consent.get("approved")),
            "contract_state": contract.state.value
        }), 200 if consent.get("approved") else 202

    # --- Parte individual (humana o sintética): flujo estándar ---
    success = contract.accept_term(term_id, pid)
    
    if not success:
        return jsonify({"error": f"failed to accept term {term_id} for {pid}"}), 400
    
    _audit(contract, "term_accept_signed", token_uid, term_id=term_id, party_id=pid)
    _save_contract(contract, actor_id=token_uid)
    
    return jsonify({
        "success": True,
        "term_id": term_id,
        "accepted_by": pid,
        "contract_state": contract.state.value
    })


@contracts_bp.route("/<contract_id>/acknowledge-asymmetry", methods=["POST"])
@token_required
def acknowledge_asymmetry(current_user, contract_id: str):
    """
    T9 ejecutable (Ola 3A.4, R6): reconocimiento explícito de la asimetría
    del contrato. Solo las partes obligadas y un aval pueden reconocer, y
    cada reconocimiento es firma vinculada al token.

    Body JSON:
    {
        "party_id": "user-2"
    }

    La activación de un contrato asimétrico exige el reconocimiento de TODAS
    las partes obligadas (+ un aval de los participantes no obligados).
    """
    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    token_uid = _token_uid(current_user)
    if token_uid is None:
        return jsonify({"error": "token sin identidad válida"}), 403

    if not getattr(contract, "_asymmetry_flag", False):
        return jsonify({"error": "este contrato no tiene asimetría declarada"}), 400

    data = request.get_json() or {}
    pid = str(data.get("party_id") or "")
    if pid not in contract.participant_ids:
        return jsonify({"error": f"participant {pid} not in contract"}), 400
    if not _can_act_for(pid, token_uid, contract):
        return jsonify({"error": "no puedes reconocer por esta parte",
                        "code": "IDENTITY_MISMATCH"}), 403

    db = get_db()
    row = db.execute(
        "SELECT meta_value FROM maxo_contract_meta WHERE contract_id = ? AND meta_key = 'asymmetry_acknowledged'",
        (contract_id,),
    ).fetchone()
    acknowledged = []
    if row and row["meta_value"]:
        try:
            acknowledged = json.loads(row["meta_value"])
        except (ValueError, TypeError):
            acknowledged = []
    if pid not in acknowledged:
        acknowledged.append(pid)
    db.execute(
        """
        INSERT INTO maxo_contract_meta (contract_id, meta_key, meta_value)
        VALUES (?, 'asymmetry_acknowledged', ?)
        ON CONFLICT(contract_id, meta_key) DO UPDATE SET meta_value = excluded.meta_value
        """,
        (contract_id, json.dumps(acknowledged)),
    )
    _audit(contract, "asymmetry_acknowledged", token_uid, party_id=pid)
    db.commit()

    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "party_id": pid,
        "acknowledged": acknowledged,
    })


@contracts_bp.route("/<contract_id>/activate", methods=["POST"])
@token_required
def activate_contract(current_user, contract_id: str):
    """Activar el contrato (todos los términos deben estar aceptados)."""
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    token_uid = _token_uid(current_user)

    # T9 ejecutable (Ola 3A.4): la asimetría debe reconocerse explícitamente
    # por todas las partes obligadas + un aval antes de activar.
    if getattr(contract, "_asymmetry_flag", False):
        report = getattr(contract, "_asymmetry_report", {}) or {}
        db = get_db()
        row = db.execute(
            "SELECT meta_value FROM maxo_contract_meta WHERE contract_id = ? AND meta_key = 'asymmetry_acknowledged'",
            (contract_id,),
        ).fetchone()
        acknowledged = []
        if row and row["meta_value"]:
            try:
                acknowledged = json.loads(row["meta_value"])
            except (ValueError, TypeError):
                acknowledged = []
        obligated = [pid for pid in report.get("obligations", {})]
        aval = next(
            (pid for pid in contract.participant_ids if pid not in obligated),
            None,
        )
        needed = set(obligated)
        if aval:
            needed.add(aval)
        missing = sorted(needed - set(acknowledged))
        if missing:
            return jsonify({
                "error": "asimetría no reconocida: faltan partes que acepten la asimetría",
                "code": "ASYMMETRY_UNACKNOWLEDGED",
                "missing": missing,
                "acknowledged": acknowledged,
                "asymmetry": report,
                "hint": "POST /contracts/<id>/acknowledge-asymmetry con cada party_id",
            }), 400
    
    if contract.state == ContractState.DRAFT:
        # Intentar pasar a PENDING primero (validación axiomática)
        if not contract.submit_for_acceptance():
            return jsonify({"error": "axiom validation failed for submission"}), 400
            
    success = contract.activate()
    
    if not success:
        return jsonify({
            "error": "activation failed",
            "state": contract.state.value,
            "hint": "ensure all terms are accepted and contract is in PENDING state"
        }), 400
    
    _audit(contract, "contract_activated", token_uid)
    _save_contract(contract, actor_id=token_uid)
    
    # Despachar evento
    dispatch_event("contract.activated", {
        "contract_id": contract_id,
        "activated_at": datetime.now().isoformat()
    })
    
    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "state": contract.state.value,
        "activated_at": datetime.now().isoformat()
    })


@contracts_bp.route("/<contract_id>/retract", methods=["POST"])
@token_required
def request_retraction(current_user, contract_id: str):
    """
    Solicitar retractación ética del contrato.
    
    Body JSON:
    {
        "user_id": 123,
        "reason": "Emergencia médica",
        "cause": "gamma_crisis"  # gamma_crisis, sdv_violation, mutual_consent, force_majeure
    }
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    user_id = data.get("user_id")
    party_id = data.get("party_id")
    reason = data.get("reason", "")
    cause = data.get("cause", "gamma_crisis")
    
    if not user_id and not party_id:
        return jsonify({"error": "user_id or party_id is required"}), 400
    
    token_uid = _token_uid(current_user)
    pid = f"user-{user_id}" if user_id else str(party_id)
    # Identidad vinculada (Ola 3A.1): solo por ti mismo o como delegado/operador
    if not _can_act_for(pid, token_uid, contract):
        return jsonify({"error": "no puedes solicitar retractación por esta parte",
                        "code": "IDENTITY_MISMATCH"}), 403
    
    # Usar oráculo sintético para evaluar
    oracle = SyntheticOracle()
    # Nota: evaluate_retraction devuelve un objeto OracleResponse
    response = oracle.evaluate_retraction(
        contract_id=contract_id,
        reason=reason,
        evidence={
            "requester_id": pid,
            "cause": cause
        }
    )
    
    # OracleResponse ahora tiene un objeto Verdict
    if response.verdict.approved:
        success = contract.retract(reason=reason, actor_id=pid)
        _save_contract(contract)
        
        # Despachar evento
        dispatch_event("contract.retracted", {
            "contract_id": contract_id,
            "reason": reason,
            "cause": cause,
            "oracle_confidence": float(response.verdict.confidence)
        })
        
        return jsonify({
            "success": success,
            "contract_id": contract_id,
            "state": contract.state.value,
            "oracle_confidence": float(response.verdict.confidence),
            "oracle_reasoning": response.verdict.reasoning
        })
    else:
        return jsonify({
            "success": False,
            "error": "retraction not approved by oracle",
            "oracle_confidence": float(response.verdict.confidence),
            "oracle_reasoning": response.verdict.reasoning
        }), 400


@contracts_bp.route("/<contract_id>/civil", methods=["GET"])
@token_required
def get_civil_summary(current_user, contract_id: str):
    """Obtener resumen del contrato en lenguaje civil."""
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    summary = contract.to_civil_language()
    
    return jsonify({
        "contract_id": contract_id,
        "civil_summary": summary
    })


@contracts_bp.route("/validate_graph", methods=["POST"])
@token_required
def validate_graph(current_user):
    """
    Valida un grafo proveniente del Constructor Visual (React Flow).
    """
    data = request.get_json() or {}
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    duration = float(data.get("duration", 30.0))
    
    if not nodes:
        return jsonify({"error": "no nodes found in graph"}), 400
        
    # Crear un contrato temporal para validación
    temp_contract = MaxoContract(
        contract_id="visual-temp",
        description="Validación Visual de Grafo"
    )
    
    # Mapear nodos a términos del contrato
    vhv_total_t = Decimal("0")
    n_cond = 0
    
    for node in nodes:
        node_type = node.get("type")
        node_id = node.get("id")
        label = node.get("data", {}).get("label", "Sin etiqueta")
        
        if node_type == "action":
            # Extraer costo VHV si existe en la data
            vhv_cost_val = node.get("data", {}).get("vhvCost", 0.5)
            try:
                t_val = Decimal(str(vhv_cost_val))
            except:
                t_val = Decimal("0.5")
                
            vhv_total_t += t_val
            vhv_cost = VHV(T=t_val, V=Decimal("0"), R=Decimal("0"))
            term = ContractTerm(id=node_id, description=f"Acción: {label}", vhv_cost=vhv_cost)
            temp_contract.add_term(term)
            
        elif node_type == "condition":
            n_cond += 1
            
        elif node_type == "sdv":
            # El bloque SDV asegura que el contrato respeta el suelo de dignidad
            temp_contract.minimum_sdv = SDV() # En el futuro, cargar parámetros específicos
            
    # Calcular Peso del Contrato (Complejidad)
    # Peso = (Nº_Condiciones * 2) + (VHV_total_T * 5) + (Duración / 30)
    weight = (n_cond * 2) + float(vhv_total_t * 5) + (duration / 30.0)
    
    if weight < 10:
        ux_signature_type = "simple"
    elif weight <= 50:
        ux_signature_type = "medium"
    else:
        ux_signature_type = "rigorous"
        
    # Inyectar participantes de simulación para evaluaciones de INV1 e INV2
    user_id = current_user.get("user_id") or current_user.get("id") or 1
    db = get_db()
    user_row = db.execute("SELECT id, name FROM users WHERE id = ?", (user_id,)).fetchone()
    user_name = user_row["name"] if user_row else f"Usuario {user_id}"
    
    p1 = Participant(
        id=f"user-{user_id}",
        name=user_name,
        wellness_current=Wellness(value=Decimal("1.0")),
        sdv_actual=SDV()
    )
    p2 = Participant(
        id="user-counterparty",
        name="Bob",
        wellness_current=Wellness(value=Decimal("1.0")),
        sdv_actual=SDV()
    )
    
    temp_contract.add_participant(p1)
    temp_contract.add_participant(p2)
            
    # Ejecutar validación axiomática de core
    valid, results = temp_contract.validate()
    
    # Construir mapa de conexiones para validación de reciprocidad
    connections = {}
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source and target:
            connections.setdefault(source, []).append(target)
            connections.setdefault(target, []).append(source)
            
    def has_path_to_type(start_id, target_type):
        visited = set()
        queue = [start_id]
        node_types = {n.get("id"): n.get("type") for n in nodes}
        
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            
            if node_types.get(curr) == target_type:
                return True
                
            for neighbor in connections.get(curr, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        return False
        
    # Validar que cada nodo de acción tenga una reciprocidad conectada (Axioma T9)
    connections_valid = True
    for node in nodes:
        if node.get("type") == "action":
            node_id = node.get("id")
            label = node.get("data", {}).get("label", "Acción")
            if not has_path_to_type(node_id, "reciprocity"):
                connections_valid = False
                results.append(ValidationResult(
                    is_valid=False,
                    axiom_code="T9",
                    axiom_name="Reciprocidad Justa",
                    message=f"La acción '{label}' ({node_id}) no está conectada a ningún bloque de Reciprocidad."
                ))
                
    if not connections_valid:
        valid = False
        
    return jsonify({
        "valid": valid,
        "results": [
            {
                "axiom": r.axiom_code,
                "is_valid": r.is_valid,
                "message": r.message
            }
            for r in results
        ],
        "weight": weight,
        "ux_signature_type": ux_signature_type,
        "total_vhv": {
            "t": float(temp_contract.total_vhv.T),
            "v": float(temp_contract.total_vhv.V),
            "r": float(temp_contract.total_vhv.R)
        }
    })


@contracts_bp.route("/cohort", methods=["GET"])
@token_required
def cohort_overview(current_user):
    """
    Vista de cohorte consolidada (Ext. 5): acuerdos de todas las partes
    colectivas del registro — contratos por estado, términos sellados y γ.

    Útil para el panel de la Cohorte Cero y para monitorear la vida
    económica agregada de las cooperativas/instituciones.
    """
    db = get_db()
    parties = [
        dict(r) for r in db.execute(
            "SELECT * FROM maxo_parties WHERE party_type NOT IN ('human', 'synthetic') ORDER BY display_name"
        ).fetchall()
    ]
    rows = []
    for party in parties:
        contracts = [dict(r) for r in db.execute(
            """
            SELECT c.contract_id, c.state FROM maxo_contracts c
            JOIN maxo_contract_participants cp ON cp.contract_id = c.contract_id
            WHERE cp.participant_id = ? ORDER BY c.created_at DESC
            """,
            (party["party_id"],),
        ).fetchall()]
        if not contracts:
            continue
        terms_sealed = db.execute(
            """
            SELECT COUNT(*) FROM maxo_contract_term_approvals
            WHERE participant_id = ?
            """,
            (party["party_id"],),
        ).fetchone()[0]
        rows.append({
            "party_id": party["party_id"],
            "party_type": party["party_type"],
            "display_name": party["display_name"],
            "wellness": float(party["wellness_value"] or 1.0),
            "contracts_total": len(contracts),
            "contracts_active": sum(1 for c in contracts if c["state"] == "active"),
            "contracts_pending": sum(1 for c in contracts if c["state"] in ("draft", "pending")),
            "terms_sealed": terms_sealed,
        })

    return jsonify({
        "parties": rows,
        "totals": {
            "parties": len(rows),
            "total_contracts": sum(r["contracts_total"] for r in rows),
            "active": sum(r["contracts_active"] for r in rows),
            "pending": sum(r["contracts_pending"] for r in rows),
            "terms_sealed": sum(r["terms_sealed"] for r in rows),
        },
    })


@contracts_bp.route("/", methods=["GET"])
@token_required
def list_contracts(current_user):
    """Listar todos los contratos desde la base de datos con paginación y filtros."""
    db = get_db()
    
    # Parámetros de paginación
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    # Filtros
    state_filter = request.args.get('state')
    participant_filter = request.args.get('participant_id')
    
    query = "SELECT contract_id, state FROM maxo_contracts WHERE 1=1"
    params = []
    
    if state_filter:
        query += " AND state = ?"
        params.append(state_filter)
        
    if participant_filter:
        query += " AND contract_id IN (SELECT contract_id FROM maxo_contract_participants WHERE participant_id = ?)"
        params.append(participant_filter)
        
    # Total sin límite
    total = db.execute(f"SELECT COUNT(*) FROM ({query})", params).fetchone()[0]
    
    # Añadir paginación
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    rows = db.execute(query, params).fetchall()
    
    contracts_list = []
    for row in rows:
        c_id = row["contract_id"]
        # Por eficiencia hacemos un resumen rápido
        p_count = db.execute("SELECT COUNT(*) FROM maxo_contract_participants WHERE contract_id = ?", (c_id,)).fetchone()[0]
        t_count = db.execute("SELECT COUNT(*) FROM maxo_contract_terms WHERE contract_id = ?", (c_id,)).fetchone()[0]
        
        contracts_list.append({
            "contract_id": c_id,
            "state": row["state"],
            "participants": p_count,
            "terms": t_count
        })
    
    return jsonify({
        "contracts": contracts_list,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total
    })
