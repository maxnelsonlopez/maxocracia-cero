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
from typing import Optional

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
    vote_rows = db.execute(
        "SELECT user_id, option FROM maxo_community_votes WHERE proposal_id = ?",
        (proposal_id,),
    ).fetchall()
    direct = {v["user_id"]: v["option"] for v in vote_rows}
    votes_cast = len(direct)

    # Democracia líquida (profundidad 1): el voto del delegatario arrastra
    # a quienes le delegaron y NO votaron directamente.
    delegations = {
        d["delegator_user_id"]: d["delegatee_user_id"]
        for d in db.execute("SELECT * FROM maxo_vote_delegations").fetchall()
    }
    effective_options = list(direct.values())
    delegated_extra = 0
    for delegator, delegatee in delegations.items():
        if delegator in direct:
            continue
        if delegatee in direct:
            effective_options.append(direct[delegatee])
            delegated_extra += 1

    quorum = votes_cast / total_users if total_users else 0.0
    detail = {"total_users": total_users, "votes_cast": votes_cast,
              "delegated_votes": delegated_extra,
              "effective_votes": len(effective_options),
              "quorum_ratio": row["quorum_ratio"], "quorum_actual": round(quorum, 4)}

    if quorum < row["quorum_ratio"]:
        result = "quorum_not_met"
    else:
        from collections import Counter
        counts = Counter(effective_options)
        winner, winner_n = counts.most_common(1)[0]
        fraction = winner_n / len(effective_options) if effective_options else 0.0
        detail["winner"] = winner
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


def _analysis_payload(row) -> Optional[dict]:
    if row is None:
        return None
    return {
        "analysis": json.loads(row["analysis_json"]),
        "model": row["model"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


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
    analysis = db.execute(
        "SELECT * FROM maxo_community_analysis WHERE proposal_id = ?", (proposal_id,)
    ).fetchone()
    payload["oracle_analysis"] = _analysis_payload(analysis)
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


@voting_bp.route("/proposals/<int:proposal_id>/analyze", methods=["POST"])
@token_required
def analyze_proposal(current_user, proposal_id: int):
    """
    Analiza la propuesta con el Oráculo Sintético (DeepSeek): estima el VHV,
    valida axiomas (TRUTH/TIME/LIFE) y recoge opiniones de 4 oráculos.
    El resultado se persiste (T13) y se expone en el detalle público.

    Sin API key configurada, devuelve 503 (oráculo deshabilitado).
    """
    from . import voting_oracle

    db = get_db()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (proposal_id,)
    ).fetchone()
    if row is None:
        return jsonify({"error": "proposal not found"}), 404

    if not voting_oracle.is_available():
        return jsonify({"error": "oracle_disabled",
                        "hint": "configura DEEPSEEK_API_KEY o habilita el oráculo local (LOCAL_ORACLE_ENABLED)"}), 503

    try:
        analysis = voting_oracle.analyze_proposal(row["title"], row["description"])
    except Exception as e:
        return jsonify({"error": "oracle_failure", "detail": str(e)[:300]}), 502

    db.execute(
        """
        INSERT INTO maxo_community_analysis (proposal_id, analysis_json, model, updated_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(proposal_id) DO UPDATE SET
            analysis_json = excluded.analysis_json,
            model = excluded.model,
            updated_at = datetime('now')
        """,
        (proposal_id, json.dumps(analysis, ensure_ascii=False), analysis.get("model", "")),
    )
    db.commit()

    stored = db.execute(
        "SELECT * FROM maxo_community_analysis WHERE proposal_id = ?", (proposal_id,)
    ).fetchone()
    return jsonify({"success": True, "oracle_analysis": _analysis_payload(stored)})


@voting_bp.route("/delegations", methods=["POST"])
@token_required
def set_delegation(current_user):
    """
    Delega el voto comunitario a otro usuario (democracia líquida, profundidad 1).

    Body JSON: {"delegatee_user_id": int}
    El delegatario debe existir y no puede ser uno mismo. El voto directo
    siempre manda sobre la delegación. Registro público (T13).
    """
    delegatee = (request.get_json() or {}).get("delegatee_user_id")
    if not isinstance(delegatee, int) or delegatee <= 0:
        return jsonify({"error": "delegatee_user_id (int) obligatorio"}), 400
    delegator = current_user["user_id"]
    if delegatee == delegator:
        return jsonify({"error": "no puedes delegar tu voto a ti mismo"}), 400

    db = get_db()
    exists = db.execute("SELECT id FROM users WHERE id = ?", (delegatee,)).fetchone()
    if exists is None:
        return jsonify({"error": "el delegatario no existe"}), 404

    db.execute(
        """
        INSERT INTO maxo_vote_delegations (delegator_user_id, delegatee_user_id)
        VALUES (?, ?)
        ON CONFLICT(delegator_user_id) DO UPDATE SET
            delegatee_user_id = excluded.delegatee_user_id,
            created_at = datetime('now')
        """,
        (delegator, delegatee),
    )
    db.commit()
    return jsonify({"success": True, "delegator_user_id": delegator, "delegatee_user_id": delegatee})


@voting_bp.route("/delegations", methods=["GET"])
def list_delegations():
    """Lista pública de delegaciones de voto (T13)."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM maxo_vote_delegations ORDER BY created_at"
    ).fetchall()
    return jsonify([
        {"delegator_user_id": r["delegator_user_id"],
         "delegatee_user_id": r["delegatee_user_id"],
         "created_at": r["created_at"]}
        for r in rows
    ])


@voting_bp.route("/delegations", methods=["DELETE"])
@token_required
def revoke_delegation(current_user):
    """Revoca la delegación de voto propia."""
    db = get_db()
    cur = db.execute(
        "DELETE FROM maxo_vote_delegations WHERE delegator_user_id = ?",
        (current_user["user_id"],),
    )
    db.commit()
    return jsonify({"success": True, "revoked": cur.rowcount > 0})


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
