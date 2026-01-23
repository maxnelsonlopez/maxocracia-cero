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
    Participant,
    ContractTerm,
    ContractState,
    MaxoAmount,
)
from maxocontracts.core.contract import MaxoContract
from maxocontracts.core.axioms import AxiomValidator
from maxocontracts.oracles import SyntheticOracle

from decimal import Decimal
import json

contracts_bp = Blueprint("contracts", __name__, url_prefix="/contracts")

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
            "ok" # Simplificado por ahora
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
    """Obtiene un participante por su PID (user-ID)."""
    try:
        user_id = int(pid.split("-")[1])
    except (IndexError, ValueError):
        return None
    return _get_or_create_participant(user_id)


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
    
    contract = MaxoContract(
        contract_id=contract_id,
        description=civil_description,
        civil_summary=civil_description
    )
    
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
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    # Preparar VHV para JSON
    vhv = {
        "t": float(contract.total_vhv.T),
        "v": float(contract.total_vhv.V),
        "r": float(contract.total_vhv.R)
    }
    
    return jsonify({
        "contract_id": contract.contract_id,
        "state": contract.state.value,
        "civil_description": contract.civil_summary,
        "participants": [p.id for p in contract.participants],
        "terms_count": len(contract._terms),
        "total_vhv": vhv,
        "events_count": len(contract.get_event_log())
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
    
    if not user_id:
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
        "user_id": 123
    }
    """
    contract = _load_contract(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    term_id = data.get("term_id")
    user_id = data.get("user_id")
    
    if not term_id or not user_id:
        return jsonify({"error": "term_id and user_id are required"}), 400
    
    pid = f"user-{user_id}"
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
    evaluation = oracle.evaluate_retraction_request(
        contract_id=contract_id,
        requester_id=pid,
        reason=reason,
        cause=cause
    )
    
    if evaluation["approved"]:
        success = contract.retract(reason=reason, actor_id=pid)
        _save_contract(contract)
        
        return jsonify({
            "success": success,
            "contract_id": contract_id,
            "state": contract.state.value,
            "oracle_confidence": evaluation["confidence"],
            "oracle_reasoning": evaluation["reasoning"]
        })
    else:
        return jsonify({
            "success": False,
            "error": "retraction not approved by oracle",
            "oracle_confidence": evaluation["confidence"],
            "oracle_reasoning": evaluation["reasoning"]
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


@contracts_bp.route("/", methods=["GET"])
@token_required
def list_contracts(current_user):
    """Listar todos los contratos desde la base de datos."""
    db = get_db()
    rows = db.execute("SELECT contract_id, state FROM maxo_contracts").fetchall()
    
    contracts_list = []
    for row in rows:
        # Podríamos cargar el objeto completo para contar términos/participantes
        # o hacer queries adicionales. Por eficiencia hacemos un resumen rápido.
        c_id = row["contract_id"]
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
        "total": len(contracts_list)
    })
