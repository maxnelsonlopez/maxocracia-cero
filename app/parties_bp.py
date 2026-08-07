"""
Registro de Partes de cualquier escala (ROADMAP Bloque B, Fase 1).

Endpoints:
- POST   /parties/            - Crear/actualizar una parte
- GET    /parties/            - Listar partes (filtro opcional party_type)
- GET    /parties/<party_id>  - Detalle de una parte (incluye estado de consentimiento)
- PUT    /parties/<party_id>  - Actualizar una parte
- DELETE /parties/<party_id>  - Eliminar una parte
"""

import hashlib
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
    members_of,
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
        "owner_user_id": row.get("owner_user_id"),
    }


def _token_uid(current_user):
    uid = current_user.get("user_id") or current_user.get("id")
    return int(uid) if uid is not None else None


def _can_govern(row: dict, token_uid) -> bool:
    """Autoridad sobre la parte (Ola 3A.3, R3): el owner, o en partes
    legacy (owner NULL) cualquier delegado actual."""
    if token_uid is None:
        return False
    if row.get("owner_user_id") == token_uid:
        return True
    if row.get("owner_user_id") is None:
        members = _parse_members(row.get("members_json"))
        delegates = members.get("delegates") or []
        return f"user-{token_uid}" in delegates
    return False


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
        owner=_token_uid(current_user),
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
    """
    Actualizar una parte (Ola 3A.3, R3): SOLO el owner (o un delegado en
    partes legacy sin owner). Los delegados de partes con owner usan
    /governance-change para votar el cambio por quórum.
    """
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404

    token_uid = _token_uid(current_user)
    if not _can_govern(row, token_uid):
        return jsonify({
            "error": "sin autoridad sobre esta parte (solo el owner o delegados en partes legacy)",
            "code": "GOVERNANCE_FORBIDDEN",
            "hint": "los delegados de una parte con owner usan POST /parties/<id>/governance-change",
        }), 403

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
        owner=row.get("owner_user_id"),
    )
    return jsonify({"success": True, "party": _party_payload(updated)})


@parties_bp.route("/<party_id>/governance-change", methods=["POST"])
@token_required
def governance_change(current_user, party_id: str):
    """
    Cambio de membresía/gobernanza aprobado por quórum de delegados
    (Ola 3A.3, R3). Cada delegado vota la misma propuesta con su token;
    al alcanzar el quórum de la parte, la propuesta se aplica.

    Body JSON:
    {
        "members": {"delegates": [...], "weights": {...}, "quorum": 0.6},
        "reason": "Renovación del consejo"   # opcional (T13)
    }
    """
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404

    token_uid = _token_uid(current_user)
    if token_uid is None:
        return jsonify({"error": "token sin identidad válida"}), 403

    members = _parse_members(row.get("members_json"))
    delegates = members.get("delegates") or []
    delegate_pid = f"user-{token_uid}"

    data = request.get_json() or {}
    new_members = _parse_members(data.get("members"))
    if not isinstance(new_members, dict) or not new_members.get("delegates"):
        return jsonify({"error": "members.delegates es obligatorio en la propuesta"}), 400

    # El owner aplica directamente; los delegados votan por quórum.
    if row.get("owner_user_id") == token_uid:
        updated = upsert_party(
            party_id=party_id,
            party_type=row["party_type"],
            display_name=row["display_name"],
            parent_party_id=row.get("parent_party_id"),
            members=new_members,
            wellness=Decimal(str(row.get("wellness_value", 1.0) or 1.0)),
            owner=row.get("owner_user_id"),
        )
        return jsonify({
            "success": True,
            "applied": True,
            "mode": "owner",
            "party": _party_payload(updated),
        })

    if delegate_pid not in delegates:
        return jsonify({"error": "solo los delegados de la parte votan el cambio",
                        "code": "GOVERNANCE_FORBIDDEN"}), 403

    from .utils import get_db
    db = get_db()
    proposal_hash = hashlib.sha256(
        json.dumps(new_members, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    db.execute(
        """
        INSERT OR IGNORE INTO maxo_party_governance_votes (party_id, proposal_hash, delegate_id)
        VALUES (?, ?, ?)
        """,
        (party_id, proposal_hash, delegate_pid),
    )
    db.commit()

    votes = db.execute(
        "SELECT COUNT(*) FROM maxo_party_governance_votes WHERE party_id = ? AND proposal_hash = ?",
        (party_id, proposal_hash),
    ).fetchone()[0]
    fraction = float(members.get("quorum", 0.6))
    needed = max(1, round(len(delegates) * fraction))

    if votes >= needed:
        updated = upsert_party(
            party_id=party_id,
            party_type=row["party_type"],
            display_name=row["display_name"],
            parent_party_id=row.get("parent_party_id"),
            members=new_members,
            wellness=Decimal(str(row.get("wellness_value", 1.0) or 1.0)),
            owner=row.get("owner_user_id"),
        )
        db.execute("DELETE FROM maxo_party_governance_votes WHERE party_id = ?", (party_id,))
        db.commit()
        return jsonify({
            "success": True,
            "applied": True,
            "mode": "quorum",
            "votes": votes,
            "needed": needed,
            "party": _party_payload(updated),
        })

    return jsonify({
        "success": True,
        "applied": False,
        "mode": "quorum",
        "votes": votes,
        "needed": needed,
        "reason": data.get("reason", ""),
    }), 202


@parties_bp.route("/<party_id>", methods=["DELETE"])
@token_required
def delete_party(current_user, party_id: str):
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404
    if not _can_govern(row, _token_uid(current_user)):
        return jsonify({"error": "sin autoridad sobre esta parte",
                        "code": "GOVERNANCE_FORBIDDEN"}), 403
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


@parties_bp.route("/<party_id>/quorum-extension", methods=["POST"])
@token_required
def extend_quorum_deadline(current_user, party_id: str):
    """
    Prórroga de la ventana de quórum (Ext. 3, ciclo de vida).

    Body JSON:
    {
        "deadline": "2026-09-01T23:59:59"   # nueva fecha límite (ISO)
    }

    Cuando la ventana vence, la parte no puede sellar (409 QUORUM_EXPIRED
    en /accept); este endpoint reabre la votación.
    """
    row = get_party(party_id)
    if row is None:
        return jsonify({"error": "party not found"}), 404

    # Autoridad (Ola 3A.3): solo owner o delegados
    if not _can_govern(row, _token_uid(current_user)):
        return jsonify({"error": "sin autoridad sobre esta parte",
                        "code": "GOVERNANCE_FORBIDDEN"}), 403

    data = request.get_json() or {}
    deadline = (data.get("deadline") or "").strip()
    if not deadline:
        return jsonify({"error": "deadline is required (ISO 8601)"}), 400

    members = _parse_members(row.get("members_json"))
    members["quorum_deadline"] = deadline
    updated = upsert_party(
        party_id=party_id,
        party_type=row["party_type"],
        display_name=row["display_name"],
        parent_party_id=row.get("parent_party_id"),
        members=members,
        wellness=Decimal(str(row.get("wellness_value", 1.0) or 1.0)),
    )
    return jsonify({
        "success": True,
        "party": _party_payload(updated),
        "quorum_deadline": deadline,
    })
