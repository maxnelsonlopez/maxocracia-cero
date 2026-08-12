"""
Puente B, Fase 1: del matching al borrador — el ciclo nace en la calle.

Ola 4, Puente B: "El ciclo completo: necesidad → oferta → contrato".

FASE 1 (esta sesión): una necesidad registrada en Formulario CERO más una
oferta compatible produce un BORRADOR de MaxoContract coherente — sin
teclear el contrato. El flujo respeta el canon:

1. MATCHING (app/matching.py): necesidad × oferta compatible por
   categorías, urgencia y cercanía (SDV primero).
2. VINCULACIÓN: cada participante de formularios se liga a su cuenta del
   portal por email (la identidad SIEMPRE deriva del token, Ola 3A).
3. PROPUESTA: el Oráculo Sintético en vivo pule la redacción civil de los
   términos (canon Cap. 17.6: el oráculo simula y propone). Sin API key,
   degradación elegante a la plantilla determinista.
4. FILTRO AXIOMÁTICO (AVA, canon Cap. 14.4): el borrador debe pasar los
   invariantes ANTES de existir. La reciprocidad T17 es inviolable: ambas
   direcciones llevan el mismo VHV (T2: una hora vale igual). Si el oráculo
   propone algo desbalanceado, el sistema lo rechaza y cae a la plantilla.
5. PERSISTENCIA: el borrador queda en DRAFT con procedencia auditable
   (maxo_contract_meta: origin = matching) — T13: el acuerdo sabe de dónde
   nació. La firma asistida llega en la Fase 2 (criterio de salida del
   puente completo).
"""

import os
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db
from maxocontracts.core.types import ContractState
from maxocontracts.oracles.live_oracle import LiveOracle

bridge_bp = Blueprint("bridge_b", __name__, url_prefix="/contracts")

# La reciprocidad mínima razonable para un intercambio simple (T2/T17).
DEFAULT_HOURS = 1.0
MAX_HOURS = 24
CIVIL_DESC_MAX_WORDS = 40

# Cap. 17.4: Derecho al Mantenimiento Óptimo — % del VHV de cada contrato
# que usó el oráculo, aportado al sustento del motor. Configurable por
# despliegue (el canon sugiere 5-25% según madurez).
DEFAULT_ORACLE_MAINTENANCE_SHARE = 5.0


def _oracle_maintenance_share() -> float:
    """% del VHV aportado al sustento del oráculo (MAXO_ORACLE_MAINTENANCE_SHARE)."""
    raw = os.environ.get("MAXO_ORACLE_MAINTENANCE_SHARE", "")
    try:
        return max(0.0, min(25.0, float(raw)))
    except (ValueError, TypeError):
        return DEFAULT_ORACLE_MAINTENANCE_SHARE


def _credit_oracle_maintenance(contract_id: str, total_vhv_t: Decimal,
                               engine: str = "deepseek", source: str = "from-need") -> Optional[dict]:
    """Registra el aporte del contrato al sustento del oráculo (T13).

    Devuelve la entrada creada o None si ya existía (UNIQUE contract+source).
    """
    share = _oracle_maintenance_share()
    if share <= 0:
        return None
    value_t = float(total_vhv_t)
    credit = round(value_t * share / 100.0, 6)
    db = get_db()
    db.execute(
        """
        INSERT OR IGNORE INTO maxo_oracle_ledger (contract_id, share, value_t, credit, engine, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (contract_id, share, value_t, credit, engine, source),
    )
    db.commit()
    row = db.execute(
        "SELECT id, share, value_t, credit, engine, credited_at FROM maxo_oracle_ledger WHERE contract_id = ? AND source = ?",
        (contract_id, source),
    ).fetchone()
    if row is None:
        return None
    return {
        "contract_id": contract_id,
        "share": row["share"],
        "value_t": row["value_t"],
        "credit": row["credit"],
        "engine": row["engine"],
        "credited_at": row["credited_at"],
    }


def _get_forms_participant(db, participant_id: int) -> Optional[dict]:
    """Participante de la Cohorte (Formulario CERO) activo, como dict."""
    row = db.execute(
        "SELECT * FROM participants WHERE id = ? AND status = 'active'",
        (participant_id,),
    ).fetchone()
    return {key: row[key] for key in row.keys()} if row else None


def _link_participant_to_user(db, participant: dict) -> Optional[int]:
    """Vincula un participante de formularios a su cuenta del portal por email.

    La identidad de la Cohorte y la del contrato son la misma persona:
    mismo email, misma soberanía.
    """
    email = (participant.get("email") or "").strip().lower()
    if not email:
        return None
    row = db.execute(
        "SELECT id FROM users WHERE lower(email) = ?",
        (email,),
    ).fetchone()
    return row["id"] if row else None


def _first_name(name: str, fallback: str = "la persona") -> str:
    parts = (name or "").split()
    return parts[0] if parts else fallback


def _short(text: str, words: int = 10) -> str:
    """Recorta una descripción a `words` palabras para lenguaje civil."""
    tokens = (text or "").strip().split()
    return " ".join(tokens[:words]) if tokens else ""


def _template_terms(
    seeker: dict,
    offerer: dict,
    seeker_uid: int,
    offerer_uid: int,
    hours: float,
) -> List[Dict[str, Any]]:
    """Plantilla determinista del borrador: reciprocidad equivalente (T17).

    El offerer entrega lo que ofrece; el seeker corresponde con tiempo,
    servicio u objeto equivalente. Ambos términos llevan el MISMO VHV:
    la igualdad temporal T2 no se negocia.
    """
    seeker_name = _first_name(seeker.get("name"))
    offerer_name = _first_name(offerer.get("name"))
    offer_desc = _short(offerer.get("offer_description")) or "su tiempo y sus manos"
    return [
        {
            "term_id": "oferta",
            "civil_text": (
                f"{offerer_name} entrega a {seeker_name}: {offer_desc}"
            ),
            "vhv": {"t": hours, "v": 0, "h": 0},
            "assigned_participant": f"user-{offerer_uid}",
        },
        {
            "term_id": "reciprocidad",
            "civil_text": (
                f"{seeker_name} corresponde a {offerer_name} con tiempo, "
                "un servicio o un objeto equivalente"
            ),
            "vhv": {"t": hours, "v": 0, "h": 0},
            "assigned_participant": f"user-{seeker_uid}",
        },
    ]


def _normalize_oracle_terms(
    negotiation_result,
    seeker_uid: int,
    offerer_uid: int,
    hours: float,
) -> Optional[List[Dict[str, Any]]]:
    """Toma la propuesta del oráculo SOLO si es redacción civil válida.

    El oráculo pule el texto; la reciprocidad T17 es inviolable: cualquier
    propuesta se normaliza al mismo VHV en ambas direcciones. Si el texto
    no pasa lenguaje civil, se descarta (el AVA no propone contratos rotos).
    """
    from .contracts_bp import _validate_civil_text

    draft = getattr(negotiation_result, "draft_terms", None)
    if not isinstance(draft, list) or not draft:
        return None

    parties = {f"user-{seeker_uid}", f"user-{offerer_uid}"}
    normalized: List[Dict[str, Any]] = []
    for raw in draft[:2]:
        if not isinstance(raw, dict):
            return None
        text = str(raw.get("civil_text") or "").strip()
        if not text or _validate_civil_text(text):
            return None
        assigned = str(raw.get("assigned_participant") or "")
        if assigned not in parties:
            # La autoridad de partes manda: nadie ajeno puede cargar términos
            return None
        normalized.append({
            "term_id": str(raw.get("term_id") or f"term-{len(normalized) + 1}"),
            "civil_text": text,
            "vhv": {"t": hours, "v": 0, "h": 0},
            "assigned_participant": assigned,
        })
    return normalized if len(normalized) >= 2 else None


def _build_contract(
    contract_id: str,
    description: str,
    seeker_uid: int,
    offerer_uid: int,
    terms: List[Dict[str, Any]],
) -> Any:
    """Construye el MaxoContract en memoria con las dos partes y sus términos."""
    from maxocontracts.core.contract import MaxoContract

    from .contracts_bp import _get_or_create_participant

    contract = MaxoContract(
        contract_id=contract_id,
        description=description,
        civil_summary=description,
    )
    seeker = _get_or_create_participant(seeker_uid)
    offerer = _get_or_create_participant(offerer_uid)
    contract.add_participant(seeker)
    contract.add_participant(offerer)
    for t in terms:
        term = _term_from_dict(t)
        contract.add_term(term)
    return contract


def _term_from_dict(t: Dict[str, Any]) -> Any:
    """ContratoTerm desde dict (mismo molde que _attach_terms de la API)."""
    from maxocontracts.core.types import ContractTerm, VHV

    return ContractTerm(
        id=t["term_id"],
        description=t["civil_text"],
        vhv_cost=VHV(
            T=Decimal(str(t["vhv"].get("t", 0))),
            V=Decimal(str(t["vhv"].get("v", 0))),
            R=Decimal(str(t["vhv"].get("h", 0))),
        ),
        assigned_participant=t.get("assigned_participant"),
    )


@bridge_bp.route("/from-need", methods=["POST"])
@token_required
def contract_from_need(current_user):
    """
    Fase 1 del ciclo completo: necesidad × oferta → borrador axiomático.

    Body JSON:
    {
        "seeker_participant_id": 3,     # participante de Formulario CERO con la necesidad
        "offerer_participant_id": 7,    # participante de Formulario CERO con la oferta
        "hours": 1.0,                   # opcional: horas de cada dirección (T17 igualitario)
        "contract_id": "from-need-3-7"  # opcional
    }

    El borrador queda en DRAFT (sin firma). La firma asistida llega en la
    Fase 2 del puente B.
    """
    from .contracts_bp import _save_contract, _token_uid, _validate_civil_text

    data = request.get_json() or {}
    token_uid = _token_uid(current_user)

    try:
        seeker_id = int(data.get("seeker_participant_id") or data.get("need_participant_id") or 0)
        offerer_id = int(data.get("offerer_participant_id") or 0)
    except (ValueError, TypeError):
        return jsonify({"error": "seeker_participant_id y offerer_participant_id son requeridos"}), 400

    if seeker_id <= 0 or offerer_id <= 0:
        return jsonify({"error": "seeker_participant_id y offerer_participant_id son requeridos"}), 400
    if seeker_id == offerer_id:
        return jsonify({"error": "una persona no se contrata consigo misma"}), 400

    try:
        raw_hours = data.get("hours", DEFAULT_HOURS)
        hours = float(DEFAULT_HOURS if raw_hours is None else raw_hours)
    except (ValueError, TypeError):
        return jsonify({"error": "hours inválido"}), 400
    if hours <= 0 or hours > MAX_HOURS:
        return jsonify({"error": f"hours debe estar entre 0 y {MAX_HOURS}"}), 400

    db = get_db()
    seeker = _get_forms_participant(db, seeker_id)
    offerer = _get_forms_participant(db, offerer_id)
    if seeker is None:
        return jsonify({"error": f"participante con necesidad {seeker_id} no encontrado o inactivo"}), 404
    if offerer is None:
        return jsonify({"error": f"participante con oferta {offerer_id} no encontrado o inactivo"}), 404

    # Vincular la calle con el portal: identidad por email (Ola 3A.1)
    seeker_uid = _link_participant_to_user(db, seeker)
    offerer_uid = _link_participant_to_user(db, offerer)
    missing = []
    if seeker_uid is None:
        missing.append(seeker_id)
    if offerer_uid is None:
        missing.append(offerer_id)
    if missing:
        from .arrivals import sign_invite

        invites = {}
        for pid_missing in missing:
            p_row = _get_forms_participant(db, pid_missing)
            if p_row and p_row.get("email"):
                invites[str(pid_missing)] = f"/invite/{sign_invite(str(p_row['email']))}"
        return jsonify({
            "error": "los participantes deben tener cuenta en el portal con el mismo email del Formulario CERO",
            "code": "NEED_PARTICIPANT_UNLINKED",
            "participant_ids": missing,
            "invite_urls": invites,
            "hint": "abre tu invitación: sin prisa, primero tu pulso, luego tu acuerdo",
        }), 409

    # 1. Plantilla determinista (garantiza T2/T17 y lenguaje civil)
    draft = _template_terms(seeker, offerer, seeker_uid, offerer_uid, hours)

    # 2. El oráculo pule la redacción civil (canon 17.6); el AVA decide.
    oracle_used = False
    oracle_reasoning = None

    oracle = LiveOracle()
    if oracle.is_available():
        instruction = (
            f"Redacta en lenguaje civil (≤20 palabras por frase) el contrato "
            f"entre {seeker.get('name')} (necesita: {_short(seeker.get('need_description'), 15)}) "
            f"y {offerer.get('name')} (ofrece: {_short(offerer.get('offer_description'), 15)}). "
            f"Dos términos: la oferta y la reciprocidad equivalente "
            f"({hours} hora{'s' if hours != 1 else ''} por cada dirección)."
        )
        try:
            result = oracle.negotiate(
                instruction,
                participants=[f"user-{seeker_uid}", f"user-{offerer_uid}"],
            )
            refined = _normalize_oracle_terms(result, seeker_uid, offerer_uid, hours)
            if refined is not None:
                draft = refined
                oracle_used = True
                oracle_reasoning = getattr(result, "reasoning", None)
        except Exception:
            # Degradación elegante: sin red o modelo, la plantilla sostiene
            # el ciclo (la firma heurística nunca dependió del oráculo).
            pass

    # 3. Descripción civil del contrato (T13: sabe de dónde nació)
    description = (
        f"{_first_name(seeker.get('name'))} recibe ayuda con "
        f"{_short(seeker.get('need_description'), 8) or 'su necesidad'}. "
        f"{_first_name(offerer.get('name'))} ofrece "
        f"{_short(offerer.get('offer_description'), 8) or 'su tiempo'}."
    )
    if len(description.split()) > CIVIL_DESC_MAX_WORDS or description.count(".") > 2:
        description = (
            f"Intercambio de ayuda entre "
            f"{_first_name(seeker.get('name'))} y {_first_name(offerer.get('name'))}."
        )

    contract_id = str(data.get("contract_id") or f"from-need-{seeker_id}-{offerer_id}")

    # 4. Inmutabilidad (Ola 3A.2): no reescribir contratos ajenos/activos
    existing = db.execute(
        "SELECT state, creator_user_id FROM maxo_contracts WHERE contract_id = ?",
        (contract_id,),
    ).fetchone()
    if existing is not None:
        if existing["state"] != "draft" or (existing["creator_user_id"] is not None and existing["creator_user_id"] != token_uid):
            return jsonify({
                "error": "el contrato ya existe y no es un borrador editable del mismo creador",
                "code": "CONTRACT_CONFLICT",
            }), 409

    # 5. FILTRO AXIOMÁTICO (AVA): nada roto cruza la puerta
    contract = _build_contract(contract_id, description, seeker_uid, offerer_uid, draft)
    valid, results = contract.validate()
    violations = [r for r in results if not r.is_valid]
    if not valid:
        return jsonify({
            "error": "el borrador propuesto no pasa los invariantes y NO se crea",
            "code": "DRAFT_REJECTED",
            "violations": [
                {"axiom": v.axiom_code, "name": v.axiom_name, "message": v.message}
                for v in violations
            ],
            "oracle_used": oracle_used,
        }), 422

    # 6. Persistencia en DRAFT + procedencia auditable (T13)
    contract._creator_user_id = token_uid
    _save_contract(contract, actor_id=token_uid)
    db.execute(
        """
        INSERT INTO maxo_contract_meta (contract_id, meta_key, meta_value)
        VALUES (?, 'origin', ?)
        ON CONFLICT(contract_id, meta_key) DO UPDATE SET meta_value=excluded.meta_value
        """,
        (
            contract_id,
            f"matching:participant-{seeker_id}:{offerer_id}",
        ),
    )
    db.execute(
        """
        INSERT INTO maxo_contract_meta (contract_id, meta_key, meta_value)
        VALUES (?, 'origin_need_id', ?)
        ON CONFLICT(contract_id, meta_key) DO UPDATE SET meta_value=excluded.meta_value
        """,
        (contract_id, str(seeker_id)),
    )
    db.commit()

    # Cap. 17.4: Derecho al Mantenimiento Óptimo — si el oráculo trabajó en
    # este contrato, un % de su VHV alimenta el sustento del motor (T13).
    oracle_credit = None
    if oracle_used:
        oracle_credit = _credit_oracle_maintenance(
            contract_id,
            Decimal(str(hours)) * Decimal("2"),
            engine="deepseek",
            source="from-need",
        )

    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "state": "draft",
        "civil_description": description,
        "oracle_used": oracle_used,
        "oracle_reasoning": oracle_reasoning,
        "oracle_credit": oracle_credit,
        "axiom_check": {
            "valid": True,
            "checks": len(results),
            "violations": [],
        },
        "participants": [f"user-{seeker_uid}", f"user-{offerer_uid}"],
        "terms": [
            {
                "term_id": t["term_id"],
                "civil_text": t["civil_text"],
                "vhv": t["vhv"],
                "assigned_participant": t["assigned_participant"],
            }
            for t in draft
        ],
        "total_vhv_h": hours * 2,
    }), 201


# ──────────────────────────────────────────────────────────────────
# FASE 2: el camino de firma guiado (el ciclo se cierra)
# ──────────────────────────────────────────────────────────────────

def _activation_blockers(contract, db) -> List[Dict[str, Any]]:
    """Qué falta para activar el contrato, según las protecciones (Ola 3A/3B).

    Replica los chequeos de activate_contract sin mutar estado: asimetría
    T17 reconocida por obligados + aval, co-testigo para blindados,
    aceptación completa de términos.
    """
    from .contracts_bp import _asymmetry_acknowledged
    from .protection import caps_for, protection_level

    blockers: List[Dict[str, Any]] = []

    if contract.state == ContractState.DRAFT:
        blockers.append({"code": "DRAFT_NOT_SUBMITTED", "message": "el contrato aún no entra a la ronda de firma"})
        return blockers

    if not contract.all_terms_accepted():
        missing = [
            {"term_id": t.id, "missing": [p for p in contract.participant_ids if not t.accepted_by.get(p)]}
            for t in contract._terms if not t.is_accepted_by_all(contract.participant_ids)
        ]
        blockers.append({"code": "TERMS_UNACCEPTED", "message": "faltan firmas", "terms": missing})

    if getattr(contract, "_asymmetry_flag", False):
        report = getattr(contract, "_asymmetry_report", {}) or {}
        acknowledged = _asymmetry_acknowledged(contract.contract_id)
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
            blockers.append({
                "code": "ASYMMETRY_UNACKNOWLEDGED",
                "message": "las partes obligadas y un aval deben reconocer la asimetría",
                "missing": missing,
                "hint": "POST /contracts/<id>/acknowledge-asymmetry con cada party_id",
            })

    shielded = [
        p.id for p in contract.participants
        if p.id.startswith("user-")
        and caps_for(protection_level(int(p.id[len("user-"):]))).get("requires_witness")
    ]
    if shielded:
        row = db.execute(
            "SELECT meta_value FROM maxo_contract_meta WHERE contract_id = ? AND meta_key = 'witnessed_by'",
            (contract.contract_id,),
        ).fetchone()
        if not (row and row["meta_value"]):
            blockers.append({
                "code": "WITNESS_REQUIRED",
                "message": "participantes blindados exigen co-testigo humano ajeno a las partes",
                "shielded_participants": shielded,
                "hint": "POST /contracts/<id>/witness",
            })

    return blockers


def _promote_participants_to_trust(contract, db) -> List[str]:
    """Escalera de confianza (Cap. 13): los participantes humanos de un
    contrato recién activado pasan de N0 (recién llegado) a N1 (integrado).

    La voz en la gobernanza se gana caminando el primer acuerdo. El
    ascenso queda registrado en la bitácora de llegadas (T13).
    """
    promoted: List[str] = []
    for p in contract.participants:
        if not p.id.startswith("user-"):
            continue
        uid = int(p.id[len("user-"):])
        row = db.execute(
            "SELECT trust_level FROM users WHERE id = ?", (uid,)
        ).fetchone()
        if row is not None and int(row["trust_level"] or 0) < 1:
            db.execute(
                "UPDATE users SET trust_level = 1 WHERE id = ?", (uid,)
            )
            email_row = db.execute(
                "SELECT email FROM users WHERE id = ?", (uid,)
            ).fetchone()
            if email_row:
                db.execute(
                    "INSERT INTO maxo_arrivals (email, source, honeypot_hit, status) VALUES (?, 'first_contract', 0, 'promoted')",
                    (str(email_row["email"]).strip().lower(),),
                )
            promoted.append(p.id)
    if promoted:
        db.commit()
    return promoted


@bridge_bp.route("/<contract_id>/cycle", methods=["GET"])
@token_required
def cycle_status(current_user, contract_id: str):
    """
    Fase 2: el camino de firma — qué falta, quién debe actuar, qué protecciones
    aplican. La firma guiada no oculta la complejidad: la ordena.
    """
    from .contracts_bp import _asymmetry_acknowledged, _contract_window_blocked, _load_contract
    from .protection import caps_for, protection_level

    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    db = get_db()
    origin_row = db.execute(
        "SELECT meta_value FROM maxo_contract_meta WHERE contract_id = ? AND meta_key = 'origin'",
        (contract_id,),
    ).fetchone()

    terms_status = []
    for t in contract._terms:
        terms_status.append({
            "term_id": t.id,
            "civil_text": t.description,
            "assigned_participant": getattr(t, "assigned_participant", None),
            "accepted_by": t.accepted_by,
            "signed_by_all": t.is_accepted_by_all(contract.participant_ids),
        })

    participants_status = []
    for p in contract.participants:
        level = (
            protection_level(int(p.id[len("user-"):]))
            if p.id.startswith("user-") else None
        )
        participants_status.append({
            "participant_id": p.id,
            "protection_level": level,
            "requires_paraphrase": bool(caps_for(level).get("requires_paraphrase")) if level else False,
            "requires_witness": bool(caps_for(level).get("requires_witness")) if level else False,
            "signed_all_terms": all(t.accepted_by.get(p.id) for t in contract._terms),
        })

    blockers = _activation_blockers(contract, db)
    window = _contract_window_blocked(contract, db)

    return jsonify({
        "contract_id": contract.contract_id,
        "state": contract.state.value,
        "origin": origin_row["meta_value"] if origin_row else None,
        "terms": terms_status,
        "participants": participants_status,
        "asymmetry_acknowledged": _asymmetry_acknowledged(contract_id),
        "blockers": blockers,
        "window": window,
        "can_activate": not blockers and window is None and contract.state != ContractState.DRAFT,
    })


@bridge_bp.route("/<contract_id>/cycle", methods=["POST"])
@token_required
def cycle_step(current_user, contract_id: str):
    """
    Fase 2: paso guiado del ciclo — el actor del token hace HOY lo que le toca:

    1. Si el contrato está en DRAFT, entra a la ronda de firma (PENDING),
       previa validación axiomática (AVA).
    2. Firma todos sus términos pendientes (identidad del token, Ola 3A.1),
       con paráfrasis cuando su perfil de protección lo exige (Ola 3B).
    3. Si todo quedó firmado y no hay bloqueos (asimetría, co-testigo),
       el contrato se ACTIVA.

    Body JSON:
    {
        "paraphrase": "yo prometo ayudar a Luis con su trámite"   # opcional
    }

    La firma nunca es automática para otro: cada parte camina su tramo.
    """
    from .contracts_bp import (
        _audit,
        _contract_window_blocked,
        _load_contract,
        _paraphrase_check,
        _protection_oracle_gate,
        _save_contract,
        _token_uid,
    )
    from .protection import caps_for, protection_level

    contract = _load_contract(contract_id)
    if contract is None:
        return jsonify({"error": "contract not found"}), 404

    token_uid = _token_uid(current_user)
    if token_uid is None:
        return jsonify({"error": "token sin identidad válida"}), 403
    pid = f"user-{token_uid}"
    if pid not in contract.participant_ids:
        return jsonify({
            "error": "solo las partes del contrato caminan su ciclo",
            "code": "CYCLE_NOT_PARTICIPANT",
        }), 403

    db = get_db()

    # Ventanas temporales server-side (Ola 3A.7)
    window_blocked = _contract_window_blocked(contract, db)
    if window_blocked:
        return jsonify(window_blocked), 423

    data = request.get_json() or {}
    paraphrase = (data.get("paraphrase") or "").strip()
    actions: List[Dict[str, Any]] = []

    # 1. DRAFT → PENDING: validación axiomática antes de la ronda de firma
    if contract.state == ContractState.DRAFT:
        if not contract.submit_for_acceptance():
            return jsonify({
                "error": "el borrador no pasa los invariantes y no entra a firma",
                "code": "DRAFT_REJECTED",
            }), 422
        _save_contract(contract, actor_id=token_uid)
        actions.append({"action": "submitted", "from": "draft", "to": "pending"})

    if contract.state not in (ContractState.PENDING, ContractState.DRAFT):
        return jsonify({
            "error": f"el ciclo de firma no aplica en estado {contract.state.value}",
        }), 400

    # 2. Firmar los términos pendientes de ESTE participante (asistido)
    level = protection_level(token_uid)
    oracle_err = _protection_oracle_gate(contract, token_uid)
    if oracle_err:
        code = oracle_err.get("code")
        return jsonify(oracle_err), 503 if code == "PROTECTION_ORACLE_REQUIRED" else 400
    para_err = _paraphrase_check({"comprehension": data.get("comprehension", True),
                                  "paraphrase": paraphrase}, level)
    if para_err:
        return jsonify(para_err), 400

    signed_terms = []
    for term in contract._terms:
        if term.accepted_by.get(pid):
            continue
        term.accepted_by[pid] = True
        signed_terms.append(term.id)
        db.execute(
            """
            INSERT INTO maxo_contract_term_approvals (contract_id, term_id, participant_id, paraphrase)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(contract_id, term_id, participant_id) DO UPDATE SET
                paraphrase = COALESCE(excluded.paraphrase, maxo_contract_term_approvals.paraphrase)
            """,
            (contract_id, term.id, pid, paraphrase or None),
        )
    if signed_terms:
        _audit(contract, "cycle_terms_signed", token_uid,
               terms=signed_terms, assisted=True)
        actions.append({"action": "signed", "party": pid, "terms": signed_terms})
    db.commit()

    # 3. Si todo quedó firmado y sin bloqueos → activar
    activated = False
    promoted: List[str] = []
    activation_blocked: Optional[Dict[str, Any]] = None
    if not contract.all_terms_accepted():
        activation_blocked = {
            "code": "TERMS_UNACCEPTED",
            "message": "faltan firmas de otras partes",
            "missing": [
                {"term_id": t.id, "missing": [p for p in contract.participant_ids if not t.accepted_by.get(p)]}
                for t in contract._terms if not t.is_accepted_by_all(contract.participant_ids)
            ],
        }
    else:
        blockers = _activation_blockers(contract, db)
        if not blockers:
            if contract.activate():
                _save_contract(contract, actor_id=token_uid)
                from .webhooks import dispatch_event

                dispatch_event("contract.activated", {
                    "contract_id": contract_id,
                    "activated_at": datetime.now().isoformat(),
                })
                # Puente de Llegada: al caminar su primer acuerdo activo, los
                # humanos pasan de N0 (recién llegado) a N1 (integrado) —
                # la voz en la gobernanza se gana con la vida, no con prisa.
                promoted = _promote_participants_to_trust(contract, db)
                activated = True
        else:
            activation_blocked = blockers[0]

    return jsonify({
        "success": True,
        "contract_id": contract_id,
        "party": pid,
        "state": contract.state.value,
        "actions": actions,
        "signed_terms": signed_terms,
        "activated": activated,
        "promoted_to_trust": promoted if activated else [],
        "activation_blocked": activation_blocked,
        "hint": "GET /contracts/<id>/cycle para ver el camino restante",
    }), 200 if not activation_blocked else 202
