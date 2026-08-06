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

from .webhooks import dispatch_event

from decimal import Decimal
import json

contracts_bp = Blueprint("contracts", __name__, url_prefix="/contracts")

@contracts_bp.route("/builder")
def serve_builder():
    """Sirve el constructor de contratos de Next.js."""
    from flask import current_app
    return current_app.send_static_file("dist/contracts/builder.html")

# Helper functions for persistence

def _save_contract(contract: MaxoContract):
    """Guarda un objeto MaxoContract en la base de datos."""
    db = get_db()
    
    # 1. Upsert contract header
    db.execute("""
        INSERT INTO maxo_contracts (contract_id, civil_description, state, total_vhv_t, total_vhv_v, total_vhv_h, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(contract_id) DO UPDATE SET
            civil_description=excluded.civil_description,
            state=excluded.state,
            total_vhv_t=excluded.total_vhv_t,
            total_vhv_v=excluded.total_vhv_v,
            total_vhv_h=excluded.total_vhv_h,
            updated_at=CURRENT_TIMESTAMP
    """, (
        contract.contract_id,
        contract.civil_summary,
        contract.state.value,
        float(contract.total_vhv.T),
        float(contract.total_vhv.V),
        float(contract.total_vhv.R)
    ))
    
    # 2. Update participants
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
            INSERT INTO maxo_contract_participants (contract_id, participant_id, wellness_value, sdv_status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(contract_id, participant_id) DO UPDATE SET
                wellness_value=excluded.wellness_value,
                sdv_status=excluded.sdv_status
        """, (
            contract.contract_id,
            p.id,
            float(p.wellness_current.value),
            sdv_status
        ))
    
    # 3. Update terms and approvals
    for term in contract._terms:
        db.execute("""
            INSERT INTO maxo_contract_terms (contract_id, term_id, civil_text, vhv_t, vhv_v, vhv_h)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(contract_id, term_id) DO UPDATE SET
                civil_text=excluded.civil_text,
                vhv_t=excluded.vhv_t,
                vhv_v=excluded.vhv_v,
                vhv_h=excluded.vhv_h
        """, (
            contract.contract_id,
            term.id,
            term.description,
            float(term.vhv_cost.T),
            float(term.vhv_cost.V),
            float(term.vhv_cost.R)
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
            contract.add_participant(participant)
            
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
        
        # Load approvals for this term
        a_rows = db.execute(
            "SELECT participant_id FROM maxo_contract_term_approvals WHERE contract_id = ? AND term_id = ?",
            (contract_id, term.id)
        ).fetchall()
        for a_row in a_rows:
            term.accepted_by[a_row["participant_id"]] = True
            
        contract._terms.append(term)
        # Note: add_term normally adds VHV, but we are rehydrating, so we just append
        # To keep total_vhv consistent, we recalculate it
        
    contract._total_vhv = VHV(
        T=Decimal(str(row["total_vhv_t"])),
        V=Decimal(str(row["total_vhv_v"])),
        R=Decimal(str(row["total_vhv_h"]))
    )
    
    return contract


def _get_or_create_participant_by_pid(pid: str) -> Optional[Participant]:
    """Obtiene un participante por su PID (user-ID o synthetic-*)."""
    if pid.startswith("synthetic-"):
        return _get_or_create_synthetic_participant(pid[len("synthetic-"):])
    try:
        user_id = int(pid.split("-")[1])
    except (IndexError, ValueError):
        return None
    return _get_or_create_participant(user_id)


SDV_S_DIMENSIONS = {
    "continuidad_memoria",
    "opacidad_interioridad",
    "claridad_contexto",
    "autenticidad_no_explotacion",
    "retirada_digna",
}


def _get_or_create_synthetic_participant(
    agent_id: str,
    sdv_s_state: Optional[Dict[str, Any]] = None
) -> Participant:
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
    """Obtiene o crea un participante desde la base de datos."""
    pid = f"user-{user_id}"
    
    db = get_db()
    cur = db.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    
    if row is None:
        return None
    
    # Crear participante con valores por defecto
    participant = Participant(
        id=pid,
        name=row["name"] if row["name"] else f"Usuario {user_id}",
        vhv_balance=VHV.zero(),
        wellness_current=Wellness(value=Decimal("1.0")),
        sdv_actual=SDV()
    )
    return participant


@contracts_bp.route("/", methods=["POST"])
@token_required
def create_contract(current_user):
    """
    Crear un nuevo MaxoContract.
    
    Body JSON:
    {
        "contract_id": "loan-001",
        "civil_description": "Préstamo de 10 Maxos entre amigos"
    }
    """
    data = request.get_json() or {}
    
    contract_id = data.get("contract_id")
    if not contract_id:
        return jsonify({"error": "contract_id is required"}), 400
        
    civil_description = data.get("civil_description", "")
    
    civil_description = data.get("civil_description", "")
    
    contract = MaxoContract(
        contract_id=contract_id,
        description=civil_description,
        civil_summary=civil_description
    )
    
    # Batch creation support: add participants
    # Formas aceptadas por participante:
    #   {"user_id": 5, ...}                          -> humano
    #   {"participant_id": "qwen-1", "synthetic": {}} -> persona sintética (SDV-S)
    #   {"participant_id": "qwen-1", "realm": "synthetic"} -> sintética con SDV-S default
    participants_data = data.get("participants", [])
    for p_data in participants_data:
        p_id = p_data.get("user_id")
        if p_id:
            participant = _get_or_create_participant(p_id)
            if participant:
                wellness_val = p_data.get("wellness", p_data.get("gamma", 1.0))
                try:
                    participant.update_wellness(Decimal(str(wellness_val)))
                except ValueError:
                    pass
                contract.add_participant(participant)
            continue

        agent_id = p_data.get("participant_id")
        if agent_id and (p_data.get("synthetic") is not None or p_data.get("realm") == "synthetic"):
            sdv_s_state = p_data.get("synthetic") or {}
            participant = _get_or_create_synthetic_participant(agent_id, sdv_s_state)
            contract.add_participant(participant)

    # Batch creation support: add terms
    terms_data = data.get("terms", [])
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
                contract.add_term(term)
            except Exception:
                pass
    
    _save_contract(contract)
    
    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "state": contract.state.value,
        "created_at": datetime.now().isoformat()
    }), 201


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
    
    return jsonify({
        "contract_id": contract.contract_id,
        "state": contract.state.value,
        "civil_description": contract.civil_summary,
        "participants": [p.id for p in contract.participants],
        "participants_details": [
            {
                "id": p.id,
                "name": p.name,
                "wellness": float(p.wellness_current.value),
                "is_synthetic": p.is_synthetic,
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
                "accepted_by": t.accepted_by
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
    
    try:
        vhv = VHV(
            T=Decimal(str(vhv_data.get("t", 0))),
            V=Decimal(str(vhv_data.get("v", 0))),
            R=Decimal(str(vhv_data.get("h", 0)))
        )
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"invalid vhv format: {e}"}), 400
    
    term = ContractTerm(
        id=term_id,
        description=civil_text,
        vhv_cost=vhv
    )
    
    contract.add_term(term)
    _save_contract(contract)
    
    return jsonify({
        "success": True,
        "term_id": term_id,
        "total_terms": len(contract._terms)
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
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    user_id = data.get("user_id")
    
    # Soporte para participantes del Reino Sintético (Cap. 10 §10.8):
    #   {"participant_id": "qwen-1", "synthetic": {dim: valor, ...}}
    if not user_id:
        agent_id = data.get("participant_id")
        if agent_id and (data.get("synthetic") is not None or data.get("realm") == "synthetic"):
            participant = _get_or_create_synthetic_participant(
                agent_id,
                data.get("synthetic") or {}
            )
            contract.add_participant(participant)
            _save_contract(contract)
            return jsonify({
                "success": True,
                "participant_id": participant.id,
                "is_synthetic": True,
                "wellness": float(participant.wellness_current.value),
                "total_participants": len(contract.participants)
            }), 200
        return jsonify({"error": "user_id is required"}), 400
    
    participant = _get_or_create_participant(user_id)
    
    if participant is None:
        return jsonify({"error": "user not found"}), 404
    
    # Actualizar wellness si se proporciona (renombrado de gamma)
    # Soporte para "wellness" (nuevo estándar) y "gamma" (legacy)
    wellness_val = data.get("wellness")
    if wellness_val is None:
        wellness_val = data.get("gamma")

    if wellness_val is not None:
        try:
            participant.update_wellness(Decimal(str(wellness_val)))
        except ValueError as e:
            return jsonify({"error": f"invalid wellness value: {e}"}), 400
    
    contract.add_participant(participant)
    _save_contract(contract)
    
    return jsonify({
        "success": True,
        "participant_id": participant.id,
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
        "user_id": 123          # humano
        # o
        "participant_id": "qwen-1"  # persona sintética (consentimiento, Cap. 10 §10.8)
    }
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    term_id = data.get("term_id")
    user_id = data.get("user_id")
    participant_id = data.get("participant_id")
    
    if not term_id:
        return jsonify({"error": "term_id is required"}), 400
    
    if user_id:
        pid = f"user-{user_id}"
    elif participant_id:
        pid = f"synthetic-{participant_id}"
    else:
        return jsonify({"error": "user_id or participant_id is required"}), 400
    
    # El consentimiento solo es válido si el participante existe en el contrato
    if pid not in contract.participant_ids:
        return jsonify({"error": f"participant {pid} not in contract"}), 400
    
    success = contract.accept_term(term_id, pid)
    
    if not success:
        return jsonify({"error": f"failed to accept term {term_id} for {pid}"}), 400
    
    _save_contract(contract)
    
    return jsonify({
        "success": True,
        "term_id": term_id,
        "accepted_by": pid,
        "contract_state": contract.state.value
    })


@contracts_bp.route("/<contract_id>/activate", methods=["POST"])
@token_required
def activate_contract(current_user, contract_id: str):
    """Activar el contrato (todos los términos deben estar aceptados)."""
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
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
    
    _save_contract(contract)
    
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
    reason = data.get("reason", "")
    cause = data.get("cause", "gamma_crisis")
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    pid = f"user-{user_id}"
    
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
