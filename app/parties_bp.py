"""
Registro de Partes de cualquier escala (ROADMAP Bloque B, Fase 1).

Endpoints:
- POST   /parties/            - Crear/actualizar una parte
- GET    /parties/            - Listar partes (filtro opcional party_type)
- GET    /parties/<party_id>  - Detalle de una parte (incluye estado de consentimiento)
- PUT    /parties/<party_id>  - Actualizar una parte
- DELETE /parties/<party_id>  - Eliminar una parte
"""

import json
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .parties import (
    PARTY_TYPE_LABELS,
    consent_status,
    get_party,
    is_valid_party_id,
    list_parties,
    party_type_of,
    upsert_party,
)

parties_bp = Blueprint("parties", __name__, url_prefix="/parties")


def _parse_members(raw) -> dict:
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except (ValueError, TypeError):
        return {}


def _party_payload(row: dict) -> dict:
    members = {}
    try:
        members = json.loads(row.get("members_json") or "{}")
    except (ValueError, TypeError):
        pass
    return {
        "party_id": row["party_id"],
        "party_type": row["party_type"],
        "party_type_label": PARTY_TYPE_LABELS.get(row["party_type"], row["party_type"]),
        "display_name": row["display_name"],
        "parent_party_id": row.get("parent_party_id"),
        "members": members,
        "wellness": float(row.get("wellness_value", 1.0) or 1.0),
    }


@parties_bp.route("/", methods=["POST"])
@token_required
def create_party(current_user):
    """
    Crear (o actualizar) una parte de cualquier escala.

    Body JSON:
    {
        "party_id": "coop-7",          # si se omite, se auto-genera del tipo
        "party_type": "cooperative",   # human|society|cooperative|institution|synthetic|ecosystem
        "display_name": "Coop del Barrio",
        "parent_party_id": null,
        "members": {"delegates": ["user-1", "user-2", "user-3"], "quorum": 0.6},
        "wellness": 1.0
    }
    """
    data = request.get_json() or {}
    party_type = data.get("party_type")
    display_name = (data.get("display_name") or "").strip()
    if party_type not in PARTY_TYPE_LABELS:
        return jsonify({"error": "party_type must be one of: human, society, cooperative, institution, synthetic, ecosystem"}), 400
    if not display_name:
        return jsonify({"error": "display_name is required"}), 400

    party_id = (data.get("party_id") or "").strip()
    if not party_id:
        # Auto-generar: prefix-<id> con el autoincremento del registro
        prefix = {
            "human": "user", "synthetic": "synthetic", "society": "society",
            "cooperative": "coop", "institution": "org", "ecosystem": "eco",
        }[party_type]
        from .utils import get_db
        row = get_db().execute(
            "INSERT INTO maxo_parties (party_id, party_type, display_name, members_json) "
            "VALUES (?, ?, ?, ?)",
            (f"{prefix}-pending", party_type, display_name, "{}"),
        )
        generated_id = f"{prefix}-{row.lastrowid}"
        get_db().execute("UPDATE maxo_parties SET party_id = ? WHERE id = ?",
                         (generated_id, row.lastrowid))
        get_db().commit()
        party_id = generated_id
    elif party_type_of(party_id) != party_type:
        return jsonify({
            "error": f"party_id '{party_id}' no coincide con party_type '{party_type}'"
        }), 400
    elif not is_valid_party_id(party_id):
        return jsonify({"error": f"invalid party_id format: {party_id}"}), 400

    wellness = None
    if data.get("wellness") is not None:
        try:
            wellness = Decimal(str(data["wellness"]))
        except (InvalidOperation, ValueError):
            return jsonify({"error": "invalid wellness value"}), 400

    row = upsert_party(
        party_id=party_id,
        party_type=party_type,
        display_name=display_name,
        parent_party_id=data.get("parent_party_id"),
        members=_parse_members(data.get("members")),
        wellness=wellness,
    )
    return jsonify({"success": True, "party": _party_payload(row)}), 201


@parties_bp.route("/", methods=["GET"])
@token_required
def list_all_parties(current_user):
    party_type = request.args.get("party_type")
    rows = list_parties(party_type=party_type)
    return jsonify({
        "parties": [_party_payload(r) for r in rows],
        "total": len(rows),
    })


@parties_bp.route("/<party_id>", methods=["GET"])
@token_required
def get_party_detail(current_user, party_id: str):
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404
    payload = _party_payload(row)
    payload["consent"] = consent_status(party_id, [])
    return jsonify({"party": payload})


@parties_bp.route("/<party_id>", methods=["PUT"])
@token_required
def update_party(current_user, party_id: str):
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404
    data = request.get_json() or {}
    display_name = (data.get("display_name") or row["display_name"]).strip()
    members = _parse_members(data.get("members"))
    wellness = None
    if data.get("wellness") is not None:
        try:
            wellness = Decimal(str(data["wellness"]))
        except (InvalidOperation, ValueError):
            return jsonify({"error": "invalid wellness value"}), 400
    updated = upsert_party(
        party_id=party_id,
        party_type=row["party_type"],
        display_name=display_name,
        parent_party_id=data.get("parent_party_id", row.get("parent_party_id")),
        members=members if data.get("members") is not None else None,
        wellness=wellness,
    )
    return jsonify({"success": True, "party": _party_payload(updated)})


@parties_bp.route("/<party_id>", methods=["DELETE"])
@token_required
def delete_party(current_user, party_id: str):
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404
    from .utils import get_db
    db = get_db()
    # T13: no borrar partes con contratos activos (el registro es la verdad)
    active = db.execute(
        """
        SELECT COUNT(*) FROM maxo_contract_participants cp
        JOIN maxo_contracts c ON c.contract_id = cp.contract_id
        WHERE cp.participant_id = ? AND c.state IN ('pending', 'active')
        """,
        (party_id,),
    ).fetchone()[0]
    if active:
        return jsonify({"error": "party has active contracts; retract them first"}), 409
    db.execute("DELETE FROM maxo_parties WHERE party_id = ?", (party_id,))
    db.commit()
    return jsonify({"success": True, "party_id": party_id})
