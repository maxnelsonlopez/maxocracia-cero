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
    Gamma,
    SDV,
    Participant,
    ContractTerm,
    ContractState,
    MaxoAmount,
)
from maxocontracts.core.contract import MaxoContract
from maxocontracts.core.axioms import AxiomValidator
from maxocontracts.oracles import SyntheticOracle

contracts_bp = Blueprint("contracts", __name__, url_prefix="/contracts")

# Almacenamiento en memoria para MVP (después: persistir en DB)
_contracts_store: Dict[str, MaxoContract] = {}
_participants_store: Dict[str, Participant] = {}


def _get_or_create_participant(user_id: int) -> Participant:
    """Obtiene o crea un participante desde la base de datos."""
    pid = f"user-{user_id}"
    if pid in _participants_store:
        return _participants_store[pid]
    
    db = get_db()
    cur = db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    
    if row is None:
        return None
    
    # Crear participante con valores por defecto (pueden actualizarse después)
    participant = Participant(
        id=pid,
        name=row["username"] if row else f"Usuario {user_id}",
        vhv=VHV(t=0, v=0, h=0),
        gamma=Gamma(value=1.0),  # Valor neutro por defecto
        sdv=SDV()
    )
    _participants_store[pid] = participant
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
    
    if contract_id in _contracts_store:
        return jsonify({"error": "contract already exists"}), 400
    
    civil_description = data.get("civil_description", "")
    
    contract = MaxoContract(
        contract_id=contract_id,
        civil_description=civil_description
    )
    
    _contracts_store[contract_id] = contract
    
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
    contract = _contracts_store.get(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    return jsonify({
        "contract_id": contract.contract_id,
        "state": contract.state.value,
        "civil_description": contract.civil_description,
        "participants": [p.id for p in contract.participants],
        "terms_count": len(contract.terms),
        "total_vhv": {
            "t": contract.total_vhv.t,
            "v": contract.total_vhv.v,
            "h": contract.total_vhv.h
        },
        "events_count": len(contract.event_log)
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
    contract = _contracts_store.get(contract_id)
    
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
            t=float(vhv_data.get("t", 0)),
            v=int(vhv_data.get("v", 0)),
            h=float(vhv_data.get("h", 0))
        )
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"invalid vhv format: {e}"}), 400
    
    term = ContractTerm(
        term_id=term_id,
        civil_text=civil_text,
        vhv_cost=vhv
    )
    
    contract.add_term(term)
    
    return jsonify({
        "success": True,
        "term_id": term_id,
        "total_terms": len(contract.terms)
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
    contract = _contracts_store.get(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    participant = _get_or_create_participant(user_id)
    
    if participant is None:
        return jsonify({"error": "user not found"}), 404
    
    # Actualizar gamma si se proporciona
    gamma_value = data.get("gamma")
    if gamma_value is not None:
        try:
            participant.update_gamma(Gamma(value=float(gamma_value)))
        except ValueError as e:
            return jsonify({"error": f"invalid gamma: {e}"}), 400
    
    contract.add_participant(participant)
    
    return jsonify({
        "success": True,
        "participant_id": participant.id,
        "gamma": participant.gamma.value,
        "total_participants": len(contract.participants)
    })


@contracts_bp.route("/<contract_id>/validate", methods=["GET"])
@token_required
def validate_contract(current_user, contract_id: str):
    """Validar axiomas del contrato."""
    contract = _contracts_store.get(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    results = contract.validate_axioms()
    
    return jsonify({
        "contract_id": contract_id,
        "valid": all(r.is_valid for r in results),
        "validations": [
            {
                "axiom": r.axiom_id,
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
    contract = _contracts_store.get(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    term_id = data.get("term_id")
    user_id = data.get("user_id")
    
    if not term_id or not user_id:
        return jsonify({"error": "term_id and user_id are required"}), 400
    
    participant = _get_or_create_participant(user_id)
    
    if participant is None:
        return jsonify({"error": "user not found"}), 404
    
    success = contract.accept_term(participant.id, term_id)
    
    if not success:
        return jsonify({"error": "failed to accept term"}), 400
    
    return jsonify({
        "success": True,
        "term_id": term_id,
        "accepted_by": participant.id,
        "contract_state": contract.state.value
    })


@contracts_bp.route("/<contract_id>/activate", methods=["POST"])
@token_required
def activate_contract(current_user, contract_id: str):
    """Activar el contrato (todos los términos deben estar aceptados)."""
    contract = _contracts_store.get(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    success = contract.activate()
    
    if not success:
        return jsonify({
            "error": "activation failed",
            "state": contract.state.value,
            "hint": "ensure all terms are accepted by all participants"
        }), 400
    
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
    contract = _contracts_store.get(contract_id)
    
    if contract is None:
        return jsonify({"error": "contract not found"}), 404
    
    data = request.get_json() or {}
    user_id = data.get("user_id")
    reason = data.get("reason", "")
    cause = data.get("cause", "gamma_crisis")
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    participant = _get_or_create_participant(user_id)
    
    if participant is None:
        return jsonify({"error": "user not found"}), 404
    
    # Usar oráculo sintético para evaluar
    oracle = SyntheticOracle()
    evaluation = oracle.evaluate_retraction_request(
        contract_id=contract_id,
        requester_id=participant.id,
        reason=reason,
        cause=cause
    )
    
    if evaluation["approved"]:
        success = contract.retract(requester_id=participant.id, reason=reason)
        
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
    contract = _contracts_store.get(contract_id)
    
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
    """Listar todos los contratos (para admin o desarrollo)."""
    contracts_list = [
        {
            "contract_id": c.contract_id,
            "state": c.state.value,
            "participants": len(c.participants),
            "terms": len(c.terms)
        }
        for c in _contracts_store.values()
    ]
    
    return jsonify({
        "contracts": contracts_list,
        "total": len(contracts_list)
    })
