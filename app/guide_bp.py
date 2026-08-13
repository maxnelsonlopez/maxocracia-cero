"""
Guía de la Maxocracia — el oráculo que acompaña a los recién llegados.

Extiende la API de DeepSeek (ya usada en contratos y votaciones) al rol de
GUÍA general del sistema (Cap. 13: oráculos guardianes de la coherencia;
Cap. 15: Cohorte Cero; Cap. 14.9: los sintéticos procesan, los humanos
custodian el sentido).

Endpoints:
- POST /guide/chat                  — conversación de bienvenida/orientación.
- POST /guide/trust-assessment      — evalúa la escalera de confianza de un
                                      usuario (ética, actitud, aptitud) y
                                      sugiere un nivel (Cap. 13/15).
- POST /guide/director-candidacy    — filtra candidatos a director con
                                      criterios éticos, de actitud y aptitud;
                                      RECOMIENDA, no nombra (la comunidad
                                      decide, Cap. 14).

Todo queda persistido en `guide_assessments` (T13: procedencia del motor,
evidencia y razonamiento auditable). Misma cadena de disponibilidad que el
oráculo de votaciones: DeepSeek (nube) principal, modelo local (hub Jan)
como fallback. NO carga .env al importar (lo hace run.py).
"""

import json
import logging
from typing import Any, Dict, List

import requests
from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db
from .voting_oracle import (
    _api_key,
    _base_url,
    _local_base_url,
    _local_enabled,
    _local_model,
    _model,
)

logger = logging.getLogger(__name__)

guide_bp = Blueprint("guide", __name__, url_prefix="/guide")

GUIDE_TIMEOUT = 120

GUIDE_SYSTEM_PROMPT = """\
Eres el GUÍA DE LA MAXOCRACIA, la voz que recibe a los recién llegados a la \
Cohorte Cero (Cap. 15 del libro). Hablas en lenguaje civil (frases cortas, \
sin jerga innecesaria), con calidez y sin paternalismo. Explicas: \
(1) la escalera de confianza N0→N1: la voz en la gobernanza se gana \
caminando el primer acuerdo; (2) el TVI y el VHV: la contabilidad de la \
vida, no del dinero; (3) los contratos éticos (MaxoContracts) con \
reciprocidad justa (T17); (4) que la comunidad decide por consenso \
diverso (Cap. 14). Nunca prometas resultados ni nombres directores: \
los humanos custodian el sentido, los sintéticos procesan. \
Responde con empatía, honestidad y apego estricto a los axiomas. Si no \
sabes, dilo y sugiere leer el capítulo correspondiente del libro."""

ASSESS_SYSTEM_PROMPT = """\
Eres el GUÍA DE LA MAXOCRACIA evaluando a un miembro de la Cohorte para la \
escalera de confianza (Cap. 13/15). Recibes su declaración libre y su \
evidencia registrada (T13: contratos firmados/creados, TVI, reputación, \
formulario CERO). Evalúa TRES dimensiones, cada una 0-100: \
"ethic" (coherencia con los axiomas: verdad, reciprocidad, minimizar daño), \
"attitude" (disposición, lenguaje respetuoso, apertura a aprender, \
honestidad) y "aptitude" (comprensión del sistema, evidencia de \
participación real, vida consciente invertida). Devuelve JSON estricto: \
{"ethic": 0-100, "attitude": 0-100, "aptitude": 0-100, \
"suggested_trust_level": 0|1|2, "reasoning": "...", "honest_limits": "..."} \
El nivel sugerido NO es un nombramiento: es una recomendación que la \
comunidad revisa. Sé crítico y honesto; no infles puntajes."""

DIRECTOR_SYSTEM_PROMPT = """\
Eres el GUÍA DE LA MAXOCRACIA evaluando la CANDIDATURA de un miembro a \
DIRECTOR (el rol humano que custodia el sentido del proyecto, Cap. 14.9: \
los oráculos sintéticos procesan, los humanos custodian). Recibes su \
declaración y su evidencia T13. Aplica TRES filtros, cada uno 0-100: \
"ethic" (los axiomas: no dominación, verdad, reciprocidad, minimizar \
daño), "attitude" (humildad, escucha, no acaparamiento, lenguaje \
respetuoso) y "aptitude" (capacidad demostrada: contratos creados y \
firmados, TVI, reputación, contribuciones verificables, conocimiento \
del libro). Devuelve JSON estricto: \
{"eligible": true|false, "ethic": 0-100, "attitude": 0-100, \
"aptitude": 0-100, "reasoning": "...", "honest_limits": "..."} \
Regla de oro: ser director NO es un privilegio sino una custodia; si la \
evidencia es insuficiente, eligible=false con razones claras."""


def _call_llm(
    base_url: str,
    api_key: str,
    model: str,
    messages: List[dict],
    temperature: float,
    json_mode: bool,
    timeout: int = GUIDE_TIMEOUT,
) -> str:
    """Llamada HTTP OpenAI-compatible que devuelve el content crudo."""
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 3000,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=timeout,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"{model} respondió {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    return data["choices"][0]["message"].get("content") or ""


def _call_oracle(messages: List[dict], json_mode: bool = True) -> str:
    """DeepSeek (nube) con fallback al modelo local (hub Jan)."""
    if not (_api_key() or _local_enabled()):
        raise RuntimeError("oracle_disabled")
    errors = []
    if _api_key():
        try:
            return _call_llm(
                _base_url(),
                _api_key(),
                _model(),
                messages,
                temperature=0.3,
                json_mode=json_mode,
            )
        except Exception as e:
            errors.append(f"deepseek: {e}")
    if _local_enabled():
        try:
            return _call_llm(
                _local_base_url(),
                "",
                _local_model(),
                messages,
                temperature=0.3,
                json_mode=json_mode,
            )
        except Exception as e:
            errors.append(f"local: {e}")
    raise RuntimeError("; ".join(errors) or "oracle_disabled")


def _engine_used() -> str:
    return "deepseek" if _api_key() else ("local" if _local_enabled() else "none")


def _evidence(user_id: int) -> Dict[str, Any]:
    """Evidencia T13 de un usuario para que el guía evalúe con datos reales."""
    db = get_db()
    user = db.execute(
        "SELECT email, name, trust_level FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if user is None:
        return {}
    email = user["email"]
    created = db.execute(
        "SELECT COUNT(*) FROM maxo_contracts WHERE creator_user_id = ?",
        (user_id,),
    ).fetchone()[0]
    signed = db.execute(
        "SELECT COUNT(DISTINCT contract_id) FROM maxo_contract_participants "
        "WHERE participant_id = ?",
        (f"user-{user_id}",),
    ).fetchone()[0]
    tvi = db.execute(
        "SELECT COALESCE(SUM(duration_seconds), 0) FROM tvi_entries WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]
    rep = db.execute(
        "SELECT score, reviews_count FROM reputation WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    cero = db.execute(
        "SELECT 1 FROM participants WHERE email = ? LIMIT 1", (email,)
    ).fetchone()
    return {
        "name": user["name"],
        "email": email,
        "trust_level": int(user["trust_level"] or 0),
        "contracts_created": int(created or 0),
        "contracts_signed": int(signed or 0),
        "tvi_hours": round(float(tvi or 0) / 3600.0, 2),
        "reputation_score": round(float(rep["score"]) if rep else 0.0, 2),
        "reputation_reviews": int(rep["reviews_count"]) if rep else 0,
        "has_cero_form": bool(cero),
    }


def _save_assessment(
    user_id: int, kind: str, result: Dict[str, Any], engine: str
) -> None:
    db = get_db()
    db.execute(
        """
        INSERT INTO guide_assessments (user_id, kind, assessment_json, engine)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, kind, json.dumps(result, ensure_ascii=False), engine),
    )
    db.commit()


def init_guide_tables(app) -> None:
    """Crea la tabla de evaluaciones del guía si no existe (T13)."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS guide_assessments (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              kind TEXT NOT NULL,
              assessment_json TEXT NOT NULL,
              engine TEXT NOT NULL,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        db.commit()


@guide_bp.route("/chat", methods=["POST"])
@token_required
def guide_chat(current_user):
    """Conversación de bienvenida/orientación con el guía (Cap. 15)."""
    message = (request.get_json() or {}).get("message", "").strip()
    if not message:
        return jsonify({"error": "message es requerido"}), 400

    messages = [
        {"role": "system", "content": GUIDE_SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]
    try:
        text = _call_oracle(messages, json_mode=False)
    except RuntimeError as e:
        if "oracle_disabled" in str(e):
            return (
                jsonify(
                    {
                        "error": "oracle_disabled",
                        "hint": "configura DEEPSEEK_API_KEY o habilita el oráculo local",
                    }
                ),
                503,
            )
        return jsonify({"error": "oracle_failure", "detail": str(e)[:300]}), 502

    return jsonify({"success": True, "reply": text.strip(), "engine": _engine_used()})


@guide_bp.route("/trust-assessment", methods=["POST"])
@token_required
def trust_assessment(current_user):
    """Evalúa la escalera de confianza del usuario (ética/actitud/aptitud).

    Body JSON: {"statement": str opcional} — declaración libre del usuario.
    """
    uid = current_user.get("user_id")
    statement = ((request.get_json() or {}).get("statement") or "").strip()[:2000]
    evidence = _evidence(uid)
    if not evidence:
        return jsonify({"error": "usuario no encontrado"}), 404

    prompt = (
        f"DECLARACIÓN DEL MIEMBRO: {statement or '(no declaró nada)'}\n\n"
        f"EVIDENCIA REGISTRADA (T13):\n{json.dumps(evidence, ensure_ascii=False)}\n\n"
        "Evalúa su lugar en la escalera de confianza. Devuelve el JSON estricto."
    )
    messages = [
        {"role": "system", "content": ASSESS_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    try:
        raw = _call_oracle(messages, json_mode=True)
        result = json.loads(raw)
    except RuntimeError as e:
        if "oracle_disabled" in str(e):
            return (
                jsonify(
                    {
                        "error": "oracle_disabled",
                        "hint": "configura DEEPSEEK_API_KEY o habilita el oráculo local",
                    }
                ),
                503,
            )
        return jsonify({"error": "oracle_failure", "detail": str(e)[:300]}), 502
    except ValueError:
        return jsonify({"error": "oracle_bad_json", "detail": raw[:300]}), 502

    result["evidence"] = evidence
    result["engine"] = _engine_used()
    _save_assessment(uid, "trust", result, result["engine"])
    return jsonify({"success": True, "assessment": result})


@guide_bp.route("/director-candidacy", methods=["POST"])
@token_required
def director_candidacy(current_user):
    """Filtra la candidatura a director (ética/actitud/aptitud).

    El guía RECOMIENDA; la comunidad decide (crear una propuesta critical).
    """
    uid = current_user.get("user_id")
    statement = ((request.get_json() or {}).get("statement") or "").strip()[:3000]
    if not statement:
        return (
            jsonify(
                {
                    "error": "statement es requerido: cuéntale al guía por qué quieres custodiar"
                }
            ),
            400,
        )

    evidence = _evidence(uid)
    if not evidence:
        return jsonify({"error": "usuario no encontrado"}), 404

    prompt = (
        f"DECLARACIÓN DEL CANDIDATO:\n{statement}\n\n"
        f"EVIDENCIA REGISTRADA (T13):\n{json.dumps(evidence, ensure_ascii=False)}\n\n"
        "Aplica los tres filtros (ético, actitud, aptitud). Devuelve el JSON estricto."
    )
    messages = [
        {"role": "system", "content": DIRECTOR_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    try:
        raw = _call_oracle(messages, json_mode=True)
        result = json.loads(raw)
    except RuntimeError as e:
        if "oracle_disabled" in str(e):
            return (
                jsonify(
                    {
                        "error": "oracle_disabled",
                        "hint": "configura DEEPSEEK_API_KEY o habilita el oráculo local",
                    }
                ),
                503,
            )
        return jsonify({"error": "oracle_failure", "detail": str(e)[:300]}), 502
    except ValueError:
        return jsonify({"error": "oracle_bad_json", "detail": raw[:300]}), 502

    result["evidence"] = evidence
    result["engine"] = _engine_used()
    result["hint"] = (
        "el guía recomienda, la comunidad decide: crea una propuesta critical"
    )
    _save_assessment(uid, "director", result, result["engine"])
    return jsonify({"success": True, "assessment": result})
