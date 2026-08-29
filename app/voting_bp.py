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
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

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

# Participación Inteligente (Cap. 14): la voz crece con la vida consciente
# invertida (TVI). Cada voto pesa 1 + TVI_WEIGHT_FACTOR * (horas / max_horas
# de la propuesta); sin TVI registrado todos pesan 1 (retrocompatible).
# El quórum sigue siendo de personas (un voto por persona, T13).
TVI_WEIGHT_FACTOR = 4.0


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
        "result_detail": (
            json.loads(row["result_detail"]) if row["result_detail"] else None
        ),
        "created_by": row["created_by"],
        "reason": row["reason"],
        "deadline": row["deadline"],
        "closed_at": row["closed_at"],
        "created_at": row["created_at"],
        "action": (
            json.loads(row["action_json"])
            if "action_json" in row.keys() and row["action_json"]
            else None
        ),
    }


def _trust_level_guard(db, current_user: dict):
    """Escalera de confianza (Cap. 13, Puente de Llegada): proponer en el
    parlamento es gobernar — la voz se gana caminando el primer acuerdo.
    Un recién llegado (N0) recibe y firma; proponer espera."""
    uid = current_user["user_id"]
    trust = db.execute("SELECT trust_level FROM users WHERE id = ?", (uid,)).fetchone()
    if trust is None or int(trust["trust_level"] or 0) < 1:
        return (
            jsonify(
                {
                    "error": "recién llegado: la voz en la gobernanza llega al caminar tu primer acuerdo",
                    "code": "TRUST_LEVEL_REQUIRED",
                    "hint": "firma y activa tu primer contrato (o pide a la comunidad que te ascienda)",
                }
            ),
            403,
        )
    return None


def _validate_vhv_params(params: dict) -> Optional[str]:
    """Restricciones axiomáticas del Parlamento de Parámetros (Cap. 11):
    α > 0 (no ignorar el tiempo), β > 0 (no ignorar la vida),
    γ ≥ 1 (no premiar el sufrimiento), δ ≥ 0 (no ignorar los recursos).
    Devuelve el mensaje de violación o None si es válido."""
    try:
        alpha = float(params["alpha"])
        beta = float(params["beta"])
        gamma = float(params["gamma"])
        delta = float(params["delta"])
    except (KeyError, ValueError, TypeError):
        return "se requieren alpha, beta, gamma y delta numéricos"
    if any(isinstance(v, bool) for v in (params["alpha"], params["beta"], params["gamma"], params["delta"])):
        return "los parámetros deben ser números, no booleanos"
    if not all(math.isfinite(v) for v in (alpha, beta, gamma, delta)):
        return "los parámetros deben ser números finitos"
    if alpha <= 0:
        return "α debe ser > 0 (axioma: no se puede ignorar el tiempo)"
    if beta <= 0:
        return "β debe ser > 0 (axioma: no se puede ignorar la vida)"
    if gamma < 1:
        return "γ debe ser ≥ 1 (axioma: no se puede premiar el sufrimiento)"
    if delta < 0:
        return "δ debe ser ≥ 0 (axioma: no se pueden ignorar los recursos finitos)"
    return None


# ──────────────────────────────────────────────────────────────────
# PARLAMENTO EDUCATIVO (rama educativa M5/M8): el umbral canónico del
# puente años<->índice se vota; la LEY (INV2-EDU ≥ 12 años) no.
# ──────────────────────────────────────────────────────────────────

# La ley vive en el motor (maxocontracts.core.types.SDV.educacion_anos_minimos)
# y en app/sdv_analyzer.py (EDU_ANIOS_MINIMOS): nunca se vota ni se negocia.
EDU_UMBRAL_MIN = 12.0
# Límite sano de plenitud: 30 años formales es cota razonable de aspiración.
EDU_UMBRAL_MAX = 30.0
# Anti-flip-flop (Cap. 14, la palabra y el poder con fecha de vencimiento):
# entre dos cambios del umbral debe pasar al menos esta ventana de días.
EDU_COOLDOWN_DAYS = 14


def _validate_edu_umbral_params(params: dict) -> Optional[str]:
    """Guardarraíles axiomáticos del Parlamento Educativo:
    - umbral_anios numérico en [12, 30]: nunca por debajo de la ley
      (INV2-EDU: ≥ 12 años de educación formal, SDV-H IV) — el piso
      legal no se vota; y nunca por encima del límite sano de plenitud.
    Devuelve el mensaje de violación o None si es válido."""
    if not isinstance(params, dict):
        return "se requieren umbral_anios numérico"
    value = params.get("umbral_anios")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return "umbral_anios debe ser numérico"
    try:
        umbral = float(value)
    except (ValueError, TypeError):
        return "umbral_anios debe ser numérico"
    if not math.isfinite(umbral):
        return "umbral_anios debe ser un número finito"
    if umbral < EDU_UMBRAL_MIN:
        return "el umbral no puede quedar por debajo de la ley (≥ 12 años: INV2-EDU, SDV-H IV)"
    if umbral > EDU_UMBRAL_MAX:
        return f"el umbral no puede superar {EDU_UMBRAL_MAX:g} años (límite sano de plenitud)"
    return None


def _current_edu_umbral(db) -> tuple:
    """(umbral vigente, procedencia) del Parlamento Educativo (T13).
    Sin resoluciones aún: el canon SDV-H (12 años) — la ley no negociada."""
    row = db.execute(
        "SELECT umbral_anios, notes FROM edu_parameters ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return (float(EDU_UMBRAL_MIN), "canon_sdv_h")
    return (float(row["umbral_anios"]), "comunidad")


def _last_edu_resolution_at(db) -> Optional[datetime]:
    """Fecha de la última resolución vinculante del Parlamento Educativo
    (None si la comunidad aún no ha votado el umbral)."""
    row = db.execute(
        "SELECT applied_at FROM edu_parameter_resolutions ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if row is None or not row["applied_at"]:
        return None
    try:
        dt = datetime.fromisoformat(str(row["applied_at"]).replace(" ", "T"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        # SQLite CURRENT_TIMESTAMP es UTC sin zona: se ancla a UTC (T13).
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _apply_passed_action(db, row) -> bool:
    """Parlamento de parámetros: aplica la acción vinculante de una
    propuesta aprobada (Cap. 11: el Oráculo Dinámico ajusta α, β, γ, δ;
    rama educativa: la comunidad vota el umbral canónico del puente
    años<->índice). Despacha por `type` de la acción.

    Devuelve True si se aplicó una acción; False si no había acción o
    no era aplicable (T13: la inacción también queda documentada).
    """
    action_json = row["action_json"] if "action_json" in row.keys() else None
    if not action_json:
        return False
    try:
        action = json.loads(action_json)
    except (ValueError, TypeError):
        return False
    if not isinstance(action, dict):
        return False
    if action.get("type") == "set_vhv_params":
        return _apply_set_vhv_params(db, row, action)
    if action.get("type") == "set_edu_umbral":
        return _apply_set_edu_umbral(db, row, action)
    return False


def _apply_set_vhv_params(db, row, action: dict) -> bool:
    """Ejecuta la resolución comunitaria sobre α, β, γ, δ (Cap. 11)."""
    params = action.get("params") or {}
    violation = _validate_vhv_params(params)
    if violation:
        return False  # defensa en profundidad: la validación ya ocurrió al crear

    from .maxo import clear_vhv_params_cache

    db.execute(
        """
        INSERT INTO vhv_parameters (alpha, beta, gamma, delta, updated_by, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            float(params["alpha"]),
            float(params["beta"]),
            float(params["gamma"]),
            float(params["delta"]),
            row["created_by"],
            f"decisión comunitaria #{row['id']} (Parlamento de Parámetros, T13)",
        ),
    )
    db.execute(
        """
        INSERT INTO maxo_parameter_resolutions (proposal_id, alpha, beta, gamma, delta, applied_by)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["id"],
            float(params["alpha"]),
            float(params["beta"]),
            float(params["gamma"]),
            float(params["delta"]),
            row["created_by"],
        ),
    )
    db.commit()
    clear_vhv_params_cache()
    return True


def _apply_set_edu_umbral(db, row, action: dict) -> bool:
    """Ejecuta la resolución comunitaria del Parlamento Educativo: actualiza
    el umbral canónico del puente años<->índice (rama educativa, T13)."""
    params = action.get("params") or {}
    violation = _validate_edu_umbral_params(params)
    if violation:
        return False  # defensa en profundidad: la validación ya ocurrió al crear

    umbral = float(params["umbral_anios"])
    db.execute(
        """
        INSERT INTO edu_parameters (umbral_anios, updated_by, notes)
        VALUES (?, ?, ?)
        """,
        (
            umbral,
            row["created_by"],
            f"decisión comunitaria #{row['id']} (Parlamento Educativo, T13)",
        ),
    )
    db.execute(
        """
        INSERT INTO edu_parameter_resolutions (proposal_id, umbral_anios, applied_by)
        VALUES (?, ?, ?)
        """,
        (row["id"], umbral, row["created_by"]),
    )
    db.commit()
    return True


def _vote_payload(row) -> dict:
    return {
        "proposal_id": row["proposal_id"],
        "user_id": row["user_id"],
        "option": row["option"],
        "created_at": row["created_at"],
    }


def _tvi_hours(db, user_id: int) -> float:
    """Horas de vida consciente registrada (TVI) de un usuario."""
    row = db.execute(
        "SELECT COALESCE(SUM(duration_seconds), 0) AS s FROM tvi_entries WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return float(row["s"]) / 3600.0


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
    effective = [(uid, direct[uid]) for uid in direct]
    delegated_extra = 0
    for delegator, delegatee in delegations.items():
        if delegator in direct:
            continue
        if delegatee in direct:
            effective.append((delegatee, direct[delegatee]))
            delegated_extra += 1

    quorum = votes_cast / total_users if total_users else 0.0
    detail = {
        "total_users": total_users,
        "votes_cast": votes_cast,
        "delegated_votes": delegated_extra,
        "effective_votes": len(effective),
        "quorum_ratio": row["quorum_ratio"],
        "quorum_actual": round(quorum, 4),
    }

    # Participación Inteligente (Cap. 14): el peso de cada voto crece con el
    # TVI registrado (vida consciente invertida), normalizado al mayor emisor
    # de la propuesta. Sin TVI, todos pesan 1 (retrocompatible).
    tvi_hours = {uid: _tvi_hours(db, uid) for uid, _ in effective}
    max_h = max(tvi_hours.values()) if tvi_hours else 0.0
    weights = {uid: 1.0 for uid in tvi_hours}
    if max_h > 0:
        for uid in tvi_hours:
            weights[uid] = 1.0 + TVI_WEIGHT_FACTOR * (tvi_hours[uid] / max_h)
    detail["tvi_weighting"] = "participation_intelligence"
    detail["tvi_hours"] = {str(uid): round(h, 2) for uid, h in tvi_hours.items()}

    option_weight: Dict[str, float] = {}
    for uid, option in effective:
        option_weight[option] = option_weight.get(option, 0.0) + weights[uid]

    if quorum < row["quorum_ratio"]:
        result = "quorum_not_met"
    else:
        from collections import Counter

        simple_counts = Counter(o for _, o in effective)
        total_weight = sum(option_weight.values()) if option_weight else 0.0
        winner = max(option_weight, key=lambda o: (option_weight[o], simple_counts[o]))
        weighted_fraction = (
            option_weight[winner] / total_weight if total_weight else 0.0
        )
        detail["winner"] = winner
        detail["winner_fraction"] = (
            round(simple_counts[winner] / len(effective), 4) if effective else 0.0
        )
        detail["weighted_fraction"] = round(weighted_fraction, 4)
        detail["option_weights"] = {k: round(v, 4) for k, v in option_weight.items()}
        if weighted_fraction >= row["majority_ratio"]:
            result = "passed"
        else:
            result = "rejected"

    # Parlamento de Parámetros: la voluntad popular aprobada se ejecuta (T13)
    if result == "passed" and _apply_passed_action(db, row):
        detail["action_applied"] = True

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
        return (
            jsonify(
                {
                    "error": f"categoria invalida: {category}",
                    "validas": sorted(VALID_CATEGORIES),
                }
            ),
            400,
        )
    options = [str(o).strip() for o in options if str(o).strip()]
    if len(options) < 2 or len(options) > MAX_OPTIONS:
        return jsonify({"error": f"se requieren 2-{MAX_OPTIONS} opciones"}), 400
    if len(set(options)) != len(options):
        return jsonify({"error": "las opciones deben ser únicas"}), 400

    defaults = CATEGORY_DEFAULTS[category]
    deadline_hours = max(1, min(int(data.get("deadline_hours", 72)), 24 * 30))
    deadline = (
        datetime.now(timezone.utc) + timedelta(hours=deadline_hours)
    ).isoformat()

    db = get_db()
    cur = db.execute(
        """
        INSERT INTO maxo_community_proposals
            (title, description, category, options_json, quorum_ratio, majority_ratio,
             created_by, reason, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            category,
            json.dumps(options, ensure_ascii=False),
            defaults["quorum"],
            defaults["majority"],
            current_user["user_id"],
            reason,
            deadline,
        ),
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

    # Escalera de confianza (Cap. 13, Puente de Llegada): la voz en la
    # gobernanza no es un derecho de llegada — se gana caminando el primer
    # acuerdo. Un recién llegado (N0) recibe y firma; gobernar espera.
    trust = db.execute("SELECT trust_level FROM users WHERE id = ?", (uid,)).fetchone()
    if trust is None or int(trust["trust_level"] or 0) < 1:
        return (
            jsonify(
                {
                    "error": "recién llegado: la voz en la gobernanza llega al caminar tu primer acuerdo",
                    "code": "TRUST_LEVEL_REQUIRED",
                    "hint": "firma y activa tu primer contrato (o pide a la comunidad que te ascienda)",
                }
            ),
            403,
        )

    cur = db.execute(
        """
        INSERT OR IGNORE INTO maxo_community_votes (proposal_id, user_id, option)
        VALUES (?, ?, ?)
        """,
        (proposal_id, uid, option),
    )
    db.commit()
    if cur.rowcount == 0:
        return (
            jsonify({"error": "ya votaste en esta propuesta (un voto por persona)"}),
            409,
        )

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
        return (
            jsonify(
                {
                    "error": "oracle_disabled",
                    "hint": "configura DEEPSEEK_API_KEY o habilita el oráculo local (LOCAL_ORACLE_ENABLED)",
                }
            ),
            503,
        )

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
        (
            proposal_id,
            json.dumps(analysis, ensure_ascii=False),
            analysis.get("model", ""),
        ),
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
    return jsonify(
        {
            "success": True,
            "delegator_user_id": delegator,
            "delegatee_user_id": delegatee,
        }
    )


@voting_bp.route("/delegations", methods=["GET"])
def list_delegations():
    """Lista pública de delegaciones de voto (T13)."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM maxo_vote_delegations ORDER BY created_at"
    ).fetchall()
    return jsonify(
        [
            {
                "delegator_user_id": r["delegator_user_id"],
                "delegatee_user_id": r["delegatee_user_id"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]
    )


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
    return jsonify(
        {
            "total_proposals": total,
            "open_proposals": open_count,
            "passed_proposals": passed,
            "total_votes": votes_total,
            "audit": hashlib.sha256(
                f"{total}:{open_count}:{passed}:{votes_total}".encode("utf-8")
            ).hexdigest()[:16],
        }
    )


# ──────────────────────────────────────────────────────────────────
# PARLAMENTO DE PARÁMETROS (Cap. 11: el Oráculo Dinámico ajusta
# α, β, γ, δ por votación comunitaria con restricciones axiomáticas)
# ──────────────────────────────────────────────────────────────────

PARAM_LABELS = {
    "alpha": "α (peso del tiempo)",
    "beta": "β (peso de la vida)",
    "gamma": "γ (aversión al sufrimiento, ≥ 1)",
    "delta": "δ (peso de los recursos finitos)",
}


def _current_params(db) -> Optional[dict]:
    row = db.execute(
        "SELECT alpha, beta, gamma, delta FROM vhv_parameters ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return None
    return {
        "alpha": float(row["alpha"]),
        "beta": float(row["beta"]),
        "gamma": float(row["gamma"]),
        "delta": float(row["delta"]),
    }


@voting_bp.route("/parliament/params", methods=["POST"])
@token_required
def propose_params(current_user):
    """
    Parlamento de Parámetros: propone ajustar los pesos axiomáticos
    (α, β, γ, δ) mediante votación comunitaria.

    Body JSON:
    {
        "alpha": float, "beta": float, "gamma": float, "delta": float,
        "reason": str (opcional, T13),
        "deadline_hours": int (opcional, default 72)
    }

    La propuesta es categoría CRITICAL (consenso 75%, Cap. 14): ajustar los
    pesos de la economía de la vida no es una decisión operativa. Si se
    aprueba, los parámetros se actualizan con procedencia auditable.
    """
    data = request.get_json() or {}
    params = {
        "alpha": data.get("alpha"),
        "beta": data.get("beta"),
        "gamma": data.get("gamma"),
        "delta": data.get("delta"),
    }
    violation = _validate_vhv_params(params)
    if violation:
        return (
            jsonify(
                {
                    "error": f"violación axiomática: {violation}",
                    "code": "PARAM_AXIOM_VIOLATION",
                }
            ),
            400,
        )

    db = get_db()
    guard = _trust_level_guard(db, current_user)
    if guard:
        return guard
    current = _current_params(db)
    if current is None:
        return jsonify({"error": "no hay parámetros actuales configurados"}), 500

    # Lenguaje civil: la comunidad entiende qué está decidiendo (T13)
    diffs = []
    for key in ("alpha", "beta", "gamma", "delta"):
        old_v, new_v = current[key], float(params[key])
        direction = (
            "sube" if new_v > old_v else ("baja" if new_v < old_v else "queda igual")
        )
        diffs.append(f"{PARAM_LABELS[key]}: {old_v:g} → {new_v:g} ({direction})")
    title = "Ajuste de los pesos de la economía de la vida (α, β, γ, δ)"
    description = (
        "La comunidad decide los pesos con los que la vida se valora: "
        + ". ".join(diffs)
        + ". Si se aprueba, los nuevos pesos se aplican a todos los cálculos "
        "futuros con registro público. El sufrimiento nunca puede premiarse "
        "(γ ≥ 1), la vida no puede ignorarse (β > 0) ni el tiempo (α > 0)."
    )
    reason = (
        data.get("reason") or ""
    ).strip() or "propuesta del Parlamento de Parámetros"

    deadline_hours = max(1, min(int(data.get("deadline_hours", 72)), 24 * 30))
    deadline = (
        datetime.now(timezone.utc) + timedelta(hours=deadline_hours)
    ).isoformat()

    cur = db.execute(
        """
        INSERT INTO maxo_community_proposals
            (title, description, category, options_json, quorum_ratio, majority_ratio,
             created_by, reason, deadline, action_json)
        VALUES (?, ?, 'critical', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            json.dumps(["Aprobar", "Mantener"], ensure_ascii=False),
            CATEGORY_DEFAULTS["critical"]["quorum"],
            CATEGORY_DEFAULTS["critical"]["majority"],
            current_user["user_id"],
            reason,
            deadline,
            json.dumps(
                {"type": "set_vhv_params", "params": params}, ensure_ascii=False
            ),
        ),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (cur.lastrowid,)
    ).fetchone()
    return jsonify({"success": True, "proposal": _proposal_payload(row)}), 201


@voting_bp.route("/parliament/params", methods=["GET"])
def parliament_params():
    """
    Parlamento de Parámetros (público, T13): pesos actuales de la economía
    de la vida, historial de resoluciones vinculantes y propuestas abiertas.
    """
    db = get_db()
    current = _current_params(db)
    pending = []
    for r in db.execute(
        """
        SELECT * FROM maxo_community_proposals
        WHERE status = 'open' AND action_json IS NOT NULL
        ORDER BY id DESC LIMIT 20
        """
    ).fetchall():
        try:
            action = json.loads(r["action_json"])
        except (ValueError, TypeError):
            continue
        if isinstance(action, dict) and action.get("type") == "set_vhv_params":
            pending.append(_proposal_payload(r))
    history = [
        {
            "proposal_id": r["proposal_id"],
            "alpha": r["alpha"],
            "beta": r["beta"],
            "gamma": r["gamma"],
            "delta": r["delta"],
            "applied_at": r["applied_at"],
        }
        for r in db.execute(
            "SELECT * FROM maxo_parameter_resolutions ORDER BY id DESC LIMIT 50"
        ).fetchall()
    ]
    return jsonify(
        {
            "current": current,
            "pending_proposals": pending,
            "history": history,
            "audit_hash": hashlib.sha256(
                json.dumps(
                    {"current": current, "history": history}, ensure_ascii=False
                ).encode("utf-8")
            ).hexdigest()[:16],
        }
    )


@voting_bp.route("/parliament/educativo", methods=["POST"])
@token_required
def propose_edu_umbral(current_user):
    """
    Parlamento Educativo (rama educativa): propone el umbral canónico del
    puente años<->índice — los años de educación formal que marcan PLENITUD
    (índice 1.0) en la dimensión educativa del SDV-H.

    Body JSON:
    {
        "umbral_anios": float (12.0-30.0; la ley INV2-EDU ≥ 12 NO se vota),
        "reason": str (opcional, T13),
        "deadline_hours": int (opcional, default 72)
    }

    Categoría CRITICAL (consenso 75%, Cap. 14): el umbral define la
    lectura del piso educativo; no es una decisión operativa. Si se aprueba,
    el umbral se aplica al analizador SDV con procedencia auditable. Entre
    dos cambios debe pasar una ventana anti-flip-flop (14 días).
    """
    data = request.get_json() or {}
    params = {"umbral_anios": data.get("umbral_anios")}
    violation = _validate_edu_umbral_params(params)
    if violation:
        return (
            jsonify(
                {
                    "error": f"violación axiomática: {violation}",
                    "code": "PARAM_AXIOM_VIOLATION",
                }
            ),
            400,
        )

    db = get_db()
    guard = _trust_level_guard(db, current_user)
    if guard:
        return guard
    last = _last_edu_resolution_at(db)
    if last is not None:
        elapsed = datetime.now(timezone.utc) - last
        if elapsed < timedelta(days=EDU_COOLDOWN_DAYS):
            return (
                jsonify(
                    {
                        "error": (
                            f"el umbral cambió hace menos de {EDU_COOLDOWN_DAYS} días "
                            "(anti-flip-flop, Cap. 14); espera a la próxima ventana"
                        ),
                        "code": "EDU_COOLDOWN",
                    }
                ),
                409,
            )

    current, provenance = _current_edu_umbral(db)
    umbral = float(params["umbral_anios"])
    direction = "sube" if umbral > current else ("baja" if umbral < current else "queda igual")

    # Lenguaje civil: la comunidad entiende qué decide (T13). La ley no se
    # toca: 12 años (INV2-EDU) siguen siendo el piso de todo cálculo.
    title = "Umbral canónico del puente educativo (años de plenitud)"
    description = (
        "La comunidad decide cuántos años de educación formal marcan la "
        f"PLENITUD (índice 1.0) de la dimensión educativa del SDV-H: {current:g} → "
        f"{umbral:g} años ({direction}). El piso legal NO cambia: la ley "
        "INV2-EDU sigue exigiendo ≥ 12 años (SDV-H IV) y la duda sin dato "
        "sigue sin castigarse. Una plenitud más alta reconoce que el saber "
        "decae (entropía δ) y que la base nunca se gradúa: quien se detuvo "
        "en el piso y no siguió aprendiendo obtiene un índice menor, no una "
        "violación. Si se aprueba, el nuevo umbral se aplica a todos los "
        "análisis con registro público."
    )
    reason = (
        data.get("reason") or ""
    ).strip() or "propuesta del Parlamento Educativo"

    deadline_hours = max(1, min(int(data.get("deadline_hours", 72)), 24 * 30))
    deadline = (
        datetime.now(timezone.utc) + timedelta(hours=deadline_hours)
    ).isoformat()

    cur = db.execute(
        """
        INSERT INTO maxo_community_proposals
            (title, description, category, options_json, quorum_ratio, majority_ratio,
             created_by, reason, deadline, action_json)
        VALUES (?, ?, 'critical', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            json.dumps(["Aprobar", "Mantener"], ensure_ascii=False),
            CATEGORY_DEFAULTS["critical"]["quorum"],
            CATEGORY_DEFAULTS["critical"]["majority"],
            current_user["user_id"],
            reason,
            deadline,
            json.dumps(
                {"type": "set_edu_umbral", "params": {"umbral_anios": umbral}},
                ensure_ascii=False,
            ),
        ),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM maxo_community_proposals WHERE id = ?", (cur.lastrowid,)
    ).fetchone()
    return jsonify({"success": True, "proposal": _proposal_payload(row)}), 201


@voting_bp.route("/parliament/educativo", methods=["GET"])
def parliament_educativo():
    """
    Parlamento Educativo (público, T13): umbral canónico vigente del puente
    años<->índice, propuestas abiertas e historial de resoluciones.
    """
    db = get_db()
    current_value, provenance = _current_edu_umbral(db)
    current = {"umbral_anios": current_value, "provenance": provenance}
    pending = []
    for r in db.execute(
        """
        SELECT * FROM maxo_community_proposals
        WHERE status = 'open' AND action_json IS NOT NULL
        ORDER BY id DESC LIMIT 20
        """
    ).fetchall():
        try:
            action = json.loads(r["action_json"])
        except (ValueError, TypeError):
            continue
        if isinstance(action, dict) and action.get("type") == "set_edu_umbral":
            pending.append(_proposal_payload(r))
    history = [
        {
            "proposal_id": r["proposal_id"],
            "umbral_anios": r["umbral_anios"],
            "applied_by": r["applied_by"],
            "applied_at": r["applied_at"],
        }
        for r in db.execute(
            "SELECT * FROM edu_parameter_resolutions ORDER BY id DESC LIMIT 50"
        ).fetchall()
    ]
    return jsonify(
        {
            "current": current,
            "pending_proposals": pending,
            "history": history,
            "audit_hash": hashlib.sha256(
                json.dumps(
                    {"current": current, "history": history}, ensure_ascii=False
                ).encode("utf-8")
            ).hexdigest()[:16],
        }
    )
