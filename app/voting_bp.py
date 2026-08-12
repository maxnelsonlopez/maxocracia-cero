"""
Votación Comunitaria — Gobernanza Operativa de la Cohorte Cero.

Implementa la "Arquitectura del Consenso Diverso" (Cap. 14 del libro):
la comunidad decide los aspectos operativos de la Maxocracia mediante
votación abierta, con quórum y mayorías por categoría:

- operational: aspectos operativos cotidianos   -> quórum 50%, mayoría 50%+1
- critical   : decisiones críticas (valor del Maxo, invariantes, parámetros
               VHV, gobernanza)                  -> quórum 60%, consenso 75% (Cap 14)
- emergency  : veto vital / crimen de coherencia (Cap 9.5 §9.5.10, FS_S -> ∞)
                                                 -> quórum 40%, mayoría 60%

Transparencia (T13): toda propuesta y todo voto quedan registrados y son
legibles públicamente (GET públicos). Un voto por persona por propuesta
(registro inmutable).

Referencias: docs/book/edicion_3_dinamica/capitulo_14_gobernanza_260126.md,
app/parties_bp.py (patrón de quórum de gobernanza de Partes, Ola 3A.3).
"""

import hashlib
import json
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from .jwt_utils import admin_required, token_required
from .utils import get_db

voting_bp = Blueprint("voting", __name__, url_prefix="/voting")

CATEGORY_DEFAULTS = {
    "operational": {"quorum": 0.50, "majority": 0.50},
    "critical": {"quorum": 0.60, "majority": 0.75},
    "emergency": {"quorum": 0.40, "majority": 0.60},
}
VALID_CATEGORIES = set(CATEGORY_DEFAULTS.keys())
MAX_OPTIONS = 8
MAX_TITLE = 200
MAX_DESCRIPTION = 4000


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _proposal_payload(row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "category": row["category"],
        "options": json.loads(row["options_json"]),
        "quorum_ratio": row["quorum_ratio"],
        "majority_ratio": row["majority_ratio"],
        "status": row["status"],
        "result": row["result"],
        "result_detail": json.loads(row["result_detail"]) if row["result_detail"] else None,
        "created_by": row["created_by"],
        "reason": row["reason"],
        "deadline": row["deadline"],
        "closed_at": row["closed_at"],
        "created_at": row["created_at"],
    }


def _vote_payload(row) -> dict:
    return {
        "proposal_id": row["proposal_id"],
        "user_id": row["user_id"],
        "option": row["option"],
        "created_at": row["created_at"],
    }


def _close_proposal(db, proposal_id: int) -> dict:
    """Cierra la propuesta si el plazo venció o es invocada manualmente."""
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
    ).fetchone()
    if row is None or row["status"] != "open":
        return _proposal_payload(row) if row else {}

    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    votes = db.execute(
        "SELECT option, COUNT(*) as n FROM maxo_community_votes WHERE proposal_id = ? GROUP BY option",
        (proposal_id,),
    ).fetchall()
    votes_cast = sum(v["n"] for v in votes)

    quorum = votes_cast / total_users if total_users else 0.0
    detail = {"total_users": total_users, "votes_cast": votes_cast,
              "quorum_ratio": row["quorum_ratio"], "quorum_actual": round(quorum, 4)}

    if quorum < row["quorum_ratio"]:
        result = "quorum_not_met"
    else:
        winner = max(votes, key=lambda v: v["n"], default=None)
        if winner is None:
            result = "quorum_not_met"
        else:
            fraction = winner["n"] / votes_cast if votes_cast else 0.0
            detail["winner"] = winner["option"]
            detail["winner_fraction"] = round(fraction, 4)
            if fraction >= row["majority_ratio"]:
                result = "passed"
            else:
                result = "rejected"

    db.execute(
        "UPDATE maxo_community_proposals SET status='closed', result=?, result_detail=?, closed_at=? WHERE id=?",
        (result, json.dumps(detail, ensure_ascii=False), _now_iso(), proposal_id),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
    ).fetchone()
    return _proposal_payload(row)


@voting_bp.route("/proposals", methods=["POST"])
@token_required
def create_proposal(current_user):
    """
    Crea una propuesta comunitaria.

    Body JSON:
    {
        "title": str (obligatorio),
        "description": str (obligatorio),
        "category": "operational" | "critical" | "emergency" (default operational),
        "options": [str, ...] (2-8 opciones, obligatorio),
        "reason": str (opcional, T13),
        "deadline_hours": int (opcional, default 72)
    }
    """
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    category = (data.get("category") or "operational").strip().lower()
    options = data.get("options") or []
    reason = (data.get("reason") or "").strip()

    if not title or len(title) > MAX_TITLE:
        return jsonify({"error": f"title obligatorio (max {MAX_TITLE} chars)"}), 400
    if not description or len(description) > MAX_DESCRIPTION:
        return jsonify({"error": "description obligatoria"}), 400
    if category not in VALID_CATEGORIES:
        return jsonify({"error": f"categoria invalida: {category}", "validas": sorted(VALID_CATEGORIES)}), 400
    options = [str(o).strip() for o in options if str(o).strip()]
    if len(options) < 2 or len(options) > MAX_OPTIONS:
        return jsonify({"error": f"se requieren 2-{MAX_OPTIONS} opciones"}), 400
    if len(set(options)) != len(options):
        return jsonify({"error": "las opciones deben ser únicas"}), 400

    defaults = CATEGORY_DEFAULTS[category]
    deadline_hours = max(1, min(int(data.get("deadline_hours", 72)), 24 * 30))
    deadline = (datetime.now(timezone.utc) + timedelta(hours=deadline_hours)).isoformat()

    db = get_db()
    cur = db.execute(
        """
        INSERT INTO maxo_community_proposals
            (title, description, category, options_json, quorum_ratio, majority_ratio,
             created_by, reason, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (title, description, category, json.dumps(options, ensure_ascii=False),
         defaults["quorum"], defaults["majority"], current_user["user_id"], reason, deadline),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (cur.lastrowid,)
    ).fetchone()
    return jsonify({"success": True, "proposal": _proposal_payload(row)}), 201


@voting_bp.route("/proposals", methods=["GET"])
def list_proposals():
    """Lista pública de propuestas (T13: legibles por cualquiera)."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM maxo_community_proposals ORDER BY id DESC LIMIT 100"
    ).fetchall()
    return jsonify([_proposal_payload(r) for r in rows])


@voting_bp.route("/proposals/<int:proposal_id>", methods=["GET"])
def get_proposal(proposal_id: int):
    """Detalle público: propuesta + votos + resultado (T13)."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "proposal not found"}), 404

    if row["status"] == "open" and row["deadline"] and row["deadline"] < _now_iso():
        _close_proposal(db, proposal_id)
        row = db.execute(
            "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
        ).fetchone()

    votes = db.execute(
        "SELECT * FROM maxo_community_votes WHERE proposal_id = ? ORDER BY created_at",
        (proposal_id,),
    ).fetchall()
    payload = _proposal_payload(row)
    payload["votes"] = [_vote_payload(v) for v in votes]
    return jsonify(payload)


@voting_bp.route("/proposals/<int:proposal_id>/vote", methods=["POST"])
@token_required
def cast_vote(current_user, proposal_id: int):
    """
    Registra el voto del usuario (uno por persona, inmutable).

    Body JSON: {"option": str}
    """
    db = get_db()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "proposal not found"}), 404
    if row["status"] != "open":
        return jsonify({"error": "propuesta cerrada", "result": row["result"]}), 409

    option = (request.get_json() or {}).get("option")
    options = json.loads(row["options_json"])
    if option not in options:
        return jsonify({"error": f"opcion invalida; opciones: {options}"}), 400

    uid = current_user["user_id"]
    cur = db.execute(
        """
        INSERT OR IGNORE INTO maxo_community_votes (proposal_id, user_id, option)
        VALUES (?, ?, ?)
        """,
        (proposal_id, uid, option),
    )
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "ya votaste en esta propuesta (un voto por persona)"}), 409

    if row["deadline"] and row["deadline"] < _now_iso():
        payload = _close_proposal(db, proposal_id)
        return jsonify({"success": True, "proposal": payload})

    return jsonify({"success": True, "voted": option, "proposal_id": proposal_id})


@voting_bp.route("/proposals/<int:proposal_id>/close", methods=["POST"])
@admin_required
def close_proposal(current_user, proposal_id: int):
    """Cierre manual de una propuesta (admin) y cálculo del resultado."""
    db = get_db()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "proposal not found"}), 404
    payload = _close_proposal(db, proposal_id)
    return jsonify({"success": True, "proposal": payload})


@voting_bp.route("/stats", methods=["GET"])
def voting_stats():
    """Estadísticas públicas de gobernanza (T13)."""
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM maxo_community_proposals").fetchone()[0]
    open_count = db.execute(
        "SELECT COUNT(*) FROM maxo_community_proposals WHERE status='open'"
    ).fetchone()[0]
    passed = db.execute(
        "SELECT COUNT(*) FROM maxo_community_proposals WHERE result='passed'"
    ).fetchone()[0]
    votes_total = db.execute("SELECT COUNT(*) FROM maxo_community_votes").fetchone()[0]
    return jsonify({
        "total_proposals": total,
        "open_proposals": open_count,
        "passed_proposals": passed,
        "total_votes": votes_total,
        "audit": hashlib.sha256(
            f"{total}:{open_count}:{passed}:{votes_total}".encode("utf-8")
        ).hexdigest()[:16],
    })
