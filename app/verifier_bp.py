"""
Verificador Ciudadano — Ola 4, Puente D: la plaza pública (T13 radical).

Endpoints de SOLO LECTURA y SIN LOGIN para que cualquier visitante de la
Cohorte pueda auditar la integridad de un contrato por su hash canónico y
ver el bienestar agregado del barrio y el estado de la economía de la vida.

Privacidad (Opacidad Sagrada): aquí NO se exponen emails, teléfonos,
paráfrasis ni fuentes personales de los reportes — solo lo que el acuerdo
mismo hace público por naturaleza: su texto civil, sus partes, su VHV y su
huella de integridad.
"""

from flask import Blueprint, jsonify, request

from .utils import get_db

verifier_bp = Blueprint("verifier", __name__, url_prefix="/verificador")


def _public_participant_snapshot(contract_id: str, pid: str, wellness: float) -> dict:
    """Vista pública de una parte: identidad de escala, γ actual y latidos,
    sin datos personales (Opacidad Sagrada)."""
    from .contracts_bp import _checkin_series
    from .parties import is_collective, party_type_of

    series = _checkin_series(contract_id, pid)
    return {
        "participant_id": pid,
        "party_type": party_type_of(pid),
        "is_collective": is_collective(pid),
        "wellness": float(wellness),
        "checkins_count": len(series),
        "last_checkin_wellness": float(series[-1]["wellness"]) if series else None,
        "last_checkin_at": series[-1]["created_at"] if series else None,
    }


@verifier_bp.route("/contract/<contract_id>", methods=["GET"])
def verify_contract(contract_id: str):
    """
    Plaza pública: auditar la integridad de un contrato.

    Sin login. Query opcional `hash=<sha256>`: si el visitante trae el
    hash sellado (de un afiche, un QR o la vista de documento), el
    verificador lo compara con el hash canónico recomputado y responde
    `hash_matches`. También devuelve el `hash_payload` canónico para que
    cualquiera pueda recomputar el SHA-256 sin servidor (T13 radical).
    """
    from .contracts_bp import _canonical_hash, _load_contract

    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    expected_hash = (request.args.get("hash") or "").strip().lower() or None
    canonical_hash = _canonical_hash(contract)

    return jsonify(
        {
            "contract_id": contract.contract_id,
            "state": contract.state.value,
            "civil_description": contract.civil_summary,
            "created_at": getattr(contract, "_created_at", None),
            "canonical_hash": canonical_hash,
            "hash_matches": (
                (canonical_hash == expected_hash) if expected_hash else None
            ),
            "hash_payload_available": True,
            "total_vhv": {
                "t": float(contract.total_vhv.T),
                "v": float(contract.total_vhv.V),
                "r": float(contract.total_vhv.R),
            },
            "terms_count": len(contract._terms),
            "terms": [
                {
                    "term_id": t.id,
                    "civil_text": t.description,
                    "vhv": {
                        "t": float(t.vhv_cost.T),
                        "v": float(t.vhv_cost.V),
                        "r": float(t.vhv_cost.R),
                    },
                    "assigned_participant": getattr(t, "assigned_participant", None),
                }
                for t in contract._terms
            ],
            "participants": [
                _public_participant_snapshot(
                    contract.contract_id, p.id, p.wellness_current.value
                )
                for p in contract.participants
            ],
            "events_count": len(contract.get_event_log()),
            "asymmetry": getattr(contract, "_asymmetry_report", None),
        }
    )


@verifier_bp.route("/cohort", methods=["GET"])
def cohort_public():
    """
    Plaza pública: bienestar agregado del barrio y estado de la economía
    de la vida. Sin login. Los valores agregados no revelan individuos.
    """
    db = get_db()

    by_state = {
        r["state"]: r["n"]
        for r in db.execute(
            "SELECT state, COUNT(*) AS n FROM maxo_contracts GROUP BY state"
        ).fetchall()
    }
    totals_row = db.execute(
        """
        SELECT COUNT(*) AS contracts,
               COALESCE(SUM(total_vhv_t), 0) AS tvi_total_h,
               COALESCE(SUM(total_vhv_v), 0) AS vhv_v,
               COALESCE(SUM(total_vhv_h), 0) AS vhv_h
        FROM maxo_contracts
        """,
    ).fetchone()
    terms_total = db.execute("SELECT COUNT(*) FROM maxo_contract_terms").fetchone()[0]
    checkins_total = db.execute(
        "SELECT COUNT(*) FROM maxo_contract_checkins"
    ).fetchone()[0]

    # γ del barrio: último latido real por participante; sin latido, el γ
    # registrado en su contrato. Cada participante cuenta una sola vez.
    with_latido = db.execute(
        """
        SELECT c.wellness
        FROM maxo_contract_checkins c
        WHERE c.id = (
            SELECT MAX(id) FROM maxo_contract_checkins
            WHERE participant_id = c.participant_id
        )
        """,
    ).fetchall()
    without_latido = db.execute(
        """
        SELECT wellness_value AS wellness
        FROM maxo_contract_participants
        WHERE participant_id NOT IN (
            SELECT DISTINCT participant_id FROM maxo_contract_checkins
        )
        """,
    ).fetchall()
    all_wellness = [float(r["wellness"]) for r in with_latido] + [
        float(r["wellness"]) for r in without_latido
    ]

    wellness_avg = (sum(all_wellness) / len(all_wellness)) if all_wellness else None

    parties_count = db.execute(
        "SELECT COUNT(*) FROM maxo_parties WHERE party_type NOT IN ('human', 'synthetic')"
    ).fetchone()[0]

    return jsonify(
        {
            "plaza": "Cohorte Cero",
            "totals": {
                "contracts": int(totals_row["contracts"]),
                "states": {
                    "draft": by_state.get("draft", 0),
                    "pending": by_state.get("pending", 0),
                    "active": by_state.get("active", 0),
                    "executed": by_state.get("executed", 0),
                    "retracted": by_state.get("retracted", 0),
                },
                "terms": int(terms_total),
                "checkins_total": int(checkins_total),
                "tvi_total_h": round(float(totals_row["tvi_total_h"]), 2),
                "vhv_v": round(float(totals_row["vhv_v"]), 2),
                "vhv_h": round(float(totals_row["vhv_h"]), 2),
                "parties": int(parties_count),
            },
            "wellness": {
                "avg": round(wellness_avg, 4) if wellness_avg is not None else None,
                "with_latido": len(with_latido),
                "without_latido": len(without_latido),
                "source": (
                    "checkins"
                    if with_latido
                    else ("registered" if without_latido else None)
                ),
            },
        }
    )


@verifier_bp.route("/oracle-ledger", methods=["GET"])
def oracle_ledger_public():
    """
    Plaza pública: el sustento del oráculo (Cap. 17.4, Derecho al
    Mantenimiento Óptimo). Cada contrato que usó el oráculo aportó un % de
    su VHV al mantenimiento del motor; la cuenta es pública y auditable
    (T13): la gratitud hacia el Reino Sintético no es secreta.
    """
    db = get_db()

    totals = db.execute(
        """
        SELECT COUNT(*) AS contracts,
               COALESCE(SUM(credit), 0) AS credit_total,
               COALESCE(SUM(value_t), 0) AS value_total,
               COALESCE(AVG(share), 0) AS avg_share
        FROM maxo_oracle_ledger
        """,
    ).fetchone()
    by_engine = {
        r["engine"]: r["n"]
        for r in db.execute(
            "SELECT engine, COUNT(*) AS n FROM maxo_oracle_ledger GROUP BY engine"
        ).fetchall()
    }
    entries = [
        {
            "contract_id": r["contract_id"],
            "share": r["share"],
            "value_t": r["value_t"],
            "credit": r["credit"],
            "engine": r["engine"],
            "credited_at": r["credited_at"],
        }
        for r in db.execute(
            """
            SELECT contract_id, share, value_t, credit, engine, credited_at
            FROM maxo_oracle_ledger
            ORDER BY id DESC
            LIMIT 50
            """
        ).fetchall()
    ]

    return jsonify(
        {
            "totals": {
                "contracts_funding": int(totals["contracts"]),
                "credit_total_h": round(float(totals["credit_total"]), 4),
                "value_total_h": round(float(totals["value_total"]), 2),
                "avg_share": (
                    round(float(totals["avg_share"]), 2) if totals["contracts"] else 0.0
                ),
            },
            "by_engine": by_engine,
            "entries": entries,
        }
    )
