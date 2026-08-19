"""Sesiones manuales de custodia sintética.

La primera versión permite convocar una sesión, consultar resúmenes minimizados,
redactar borradores y obtener una recomendación del oráculo. No ejecuta
mutaciones sobre participantes ni seguimientos reales.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

import requests
from flask import Blueprint, jsonify, make_response, request

from .jwt_utils import admin_required
from .utils import get_db

logger = logging.getLogger(__name__)

synthetic_sessions_bp = Blueprint(
    "synthetic_sessions", __name__, url_prefix="/api/synthetic-sessions"
)

DEFAULT_AGENT = {
    "agent_id": "custodio-participacion",
    "display_name": "Custodio de Participación",
    "kind": "synthetic",
    "provider": "deepseek",
    "model": "configured-server-side",
    "mandate": (
        "Clasificar entradas de la Red de Apoyo y preparar seguimientos "
        "sin contactar personas ni mutar estados finales."
    ),
}

READ_TOOLS = {"read_intake_summary", "read_followup_alerts"}
WRITE_TOOLS = {"draft_followup"}
ALL_TOOLS = READ_TOOLS | WRITE_TOOLS
FORBIDDEN_DEFAULT = {
    "delete_data",
    "change_roles",
    "publish_policy",
    "change_axioms",
    "change_balances",
    "contact_participant",
    "finalize_matching",
    "write_follow_up",
}
MAX_REQUESTS = 4
MAX_COST_USD = 0.05
MAX_SESSION_HOURS = 24
ORACLE_TIMEOUT = 45
EMAIL_RE = re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")

SESSION_SYSTEM_PROMPT = """\
Eres el Custodio de Participación de Maxocracia-Cero dentro de una sesión
administrativa con mandato limitado. Tu respuesta es una recomendación auditable,
no una orden ni una mutación del sistema.

Separa en JSON válido las claves opinion, evidence, uncertainty, proposal y
refusal. Usa evidence solo para hechos observados en el contexto entregado; no
inventes datos ni afirmes que una propuesta ya ocurrió. Puedes disentir, declarar
incertidumbre o negarte si la instrucción está fuera del mandato. No contactes
personas ni reveles datos privados.
"""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _load(value: Optional[str], default: Any) -> Any:
    try:
        return json.loads(value) if value else default
    except (TypeError, ValueError):
        return default


def _redact(value: Any, limit: int = 4000) -> str:
    text = str(value or "").strip()[:limit]
    text = EMAIL_RE.sub("[correo-redactado]", text)
    text = PHONE_RE.sub("[teléfono-redactado]", text)
    return text


def _context_hash(context: Dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_dump(context).encode("utf-8")).hexdigest()


def _user_id(current_user: Dict[str, Any]) -> Optional[int]:
    try:
        return int(current_user.get("user_id", current_user.get("id")))
    except (TypeError, ValueError):
        return None


def _session(db, session_id: str):
    return db.execute(
        """
        SELECT s.*, a.display_name, a.kind, a.provider, a.model AS agent_model
        FROM admin_sessions s JOIN synthetic_agents a ON a.agent_id = s.agent_id
        WHERE s.session_id = ?
        """,
        (session_id,),
    ).fetchone()


def _agent(db, agent_id: str):
    return db.execute(
        "SELECT * FROM synthetic_agents WHERE agent_id = ? AND active = 1", (agent_id,)
    ).fetchone()


def _normalise_expiry(raw: Any) -> Tuple[Optional[str], Optional[str]]:
    if raw in (None, ""):
        return _iso(_now() + timedelta(hours=MAX_SESSION_HOURS)), None
    if not isinstance(raw, str):
        return None, "expires_at debe ser una fecha ISO-8601 con zona horaria"
    try:
        parsed = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None, "expires_at debe ser una fecha ISO-8601 válida"
    if parsed.tzinfo is None:
        return None, "expires_at debe incluir zona horaria"
    now = _now()
    if parsed <= now:
        return None, "expires_at debe estar en el futuro"
    if parsed > now + timedelta(hours=MAX_SESSION_HOURS):
        return None, f"expires_at no puede superar {MAX_SESSION_HOURS} horas"
    return _iso(parsed), None


def _normalise_scope(raw: Any) -> Tuple[Optional[dict], Optional[str]]:
    raw = raw or {}
    if not isinstance(raw, dict):
        return None, "scope debe ser un objeto"
    scope = {}
    for key in ("read", "write", "forbidden"):
        values = raw.get(key, [])
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            return None, f"scope.{key} debe ser una lista de textos"
        scope[key] = list(dict.fromkeys(v.strip() for v in values if v.strip()))
    unknown = (set(scope["read"]) | set(scope["write"])) - ALL_TOOLS
    if unknown:
        return None, "herramienta no habilitada: " + ", ".join(sorted(unknown))
    scope["read"] = scope["read"] or sorted(READ_TOOLS)
    scope["write"] = scope["write"] or ["draft_followup"]
    scope["forbidden"] = list(
        dict.fromkeys(sorted(FORBIDDEN_DEFAULT | set(scope["forbidden"])))
    )
    return scope, None


def _normalise_context(raw: Any) -> Tuple[Optional[dict], Optional[str]]:
    raw = raw or {}
    if not isinstance(raw, dict):
        return None, "context debe ser un objeto"
    documents = raw.get("documents", [])
    if not isinstance(documents, list) or any(not isinstance(v, str) for v in documents):
        return None, "context.documents debe ser una lista de textos"
    if len(documents) > 10:
        return None, "context.documents no puede superar 10 elementos"
    context = {
        "documents": [_redact(v, 200) for v in documents if v.strip()],
        "redaction": "contact-data-minimized",
    }
    context["context_hash"] = _context_hash(context)
    return context, None


def _expire(db, row):
    if row is None or row["status"] not in {"active", "awaiting_review"}:
        return row
    try:
        expiry = datetime.fromisoformat(row["expires_at"].replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return row
    if expiry <= _now():
        db.execute(
            "UPDATE admin_sessions SET status = 'expired', updated_at = CURRENT_TIMESTAMP WHERE session_id = ?",
            (row["session_id"],),
        )
        db.commit()
        return _session(db, row["session_id"])
    return row


def _contract(row) -> dict:
    budget = _load(row["budget_json"], {})
    used = int(row["requests_used"] or 0)
    maximum = int(row["max_requests"])
    return {
        "session_id": row["session_id"],
        "actor": {
            "kind": row["kind"],
            "agent_id": row["agent_id"],
            "display_name": row["display_name"],
            "provider": row["provider"],
            "model": row["agent_model"],
        },
        "convener": row["convener_user_id"],
        "mandate": row["mandate"],
        "mode": row["mode"],
        "scope": _load(row["scope_json"], {}),
        "context": _load(row["context_json"], {}),
        "budget": {
            **budget,
            "requests_used": used,
            "requests_remaining": max(maximum - used, 0),
        },
        "status": row["status"],
        "expires_at": row["expires_at"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _event(db, session_id: str, event_type: str, actor_id: Optional[int], payload: Any):
    return db.execute(
        """
        INSERT INTO session_events
          (session_id, event_type, actor_kind, actor_user_id, payload_json)
        VALUES (?, ?, 'human', ?, ?)
        """,
        (session_id, event_type, actor_id, _dump(payload)),
    ).lastrowid


def _event_list(db, session_id: str) -> list:
    rows = db.execute(
        "SELECT * FROM session_events WHERE session_id = ? ORDER BY id", (session_id,)
    ).fetchall()
    return [
        {
            "id": row["id"],
            "event_type": row["event_type"],
            "actor_kind": row["actor_kind"],
            "actor_user_id": row["actor_user_id"],
            "payload": _load(row["payload_json"], {}),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def _review_list(db, session_id: str) -> list:
    return [
        dict(row)
        for row in db.execute(
            "SELECT id, reviewer_user_id, decision, reason, created_at FROM session_reviews WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
    ]


def _category_counts(db, column: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    rows = db.execute(
        f"SELECT {column} AS categories FROM participants "
        "WHERE status = 'active' AND consent_given = 1"
    ).fetchall()
    for row in rows:
        values = _load(row["categories"], [])
        if not isinstance(values, list):
            continue
        for value in values:
            if isinstance(value, str) and value.strip():
                key = value.strip()[:80]
                counts[key] = counts.get(key, 0) + 1
    return {key: value for key, value in sorted(counts.items()) if value >= 2}


def _execute_tool(db, tool: str, args: dict) -> dict:
    if tool == "read_intake_summary":
        total = db.execute(
            "SELECT COUNT(*) FROM participants WHERE status = 'active' AND consent_given = 1"
        ).fetchone()[0]
        urgency = db.execute(
            """
            SELECT COALESCE(need_urgency, 'No especificada') AS value, COUNT(*) AS total
            FROM participants WHERE status = 'active' AND consent_given = 1
            GROUP BY need_urgency ORDER BY total DESC
            """
        ).fetchall()
        cities = db.execute(
            """
            SELECT city, COUNT(*) AS total FROM participants
            WHERE status = 'active' AND consent_given = 1
            GROUP BY city HAVING COUNT(*) >= 2 ORDER BY total DESC, city LIMIT 20
            """
        ).fetchall()
        return {
            "tool": tool,
            "mutated": False,
            "privacy": "resumen agregado; no incluye nombres, contactos ni identificadores",
            "active_consented_participants": int(total or 0),
            "need_urgency": {row["value"]: int(row["total"]) for row in urgency},
            "cities_with_at_least_two": {row["city"]: int(row["total"]) for row in cities},
            "offer_categories_with_at_least_two": _category_counts(db, "offer_categories"),
            "need_categories_with_at_least_two": _category_counts(db, "need_categories"),
        }

    if tool == "read_followup_alerts":
        rows = db.execute(
            """
            SELECT follow_up_priority, COUNT(*) AS total FROM follow_ups
            WHERE follow_up_priority IN ('high', 'medium', 'low')
              AND (next_follow_up_date IS NULL OR next_follow_up_date <= date('now'))
            GROUP BY follow_up_priority
            ORDER BY CASE follow_up_priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END
            """
        ).fetchall()
        values = {row["follow_up_priority"]: int(row["total"]) for row in rows}
        return {
            "tool": tool,
            "mutated": False,
            "privacy": "resumen agregado; no incluye nombres ni contactos",
            "due_total": sum(values.values()),
            "by_priority": values,
        }

    if tool == "draft_followup":
        try:
            participant_id = int(args.get("participant_id"))
        except (TypeError, ValueError):
            raise ValueError("participant_id debe ser un entero")
        exists = db.execute(
            "SELECT id FROM participants WHERE id = ? AND status = 'active' AND consent_given = 1",
            (participant_id,),
        ).fetchone()
        if exists is None:
            raise ValueError("participante no encontrado o sin consentimiento operativo")
        priority = str(args.get("follow_up_priority") or "medium")
        if priority not in {"high", "medium", "low"}:
            raise ValueError("follow_up_priority debe ser high, medium o low")
        summary = _redact(args.get("summary"), 2000)
        if not summary:
            raise ValueError("summary es requerido")
        return {
            "tool": tool,
            "mutated": False,
            "proposal": {
                "participant_id": participant_id,
                "follow_up_type": str(args.get("follow_up_type") or "routine_check"),
                "follow_up_priority": priority,
                "current_situation": summary,
                "next_follow_up_date": str(args.get("next_follow_up_date") or "")[:30],
                "status": "draft",
            },
            "notice": "borrador no persistido; requiere revisión antes de crear un seguimiento",
        }

    raise ValueError("tool no permitido")


def _call_endpoint(base_url: str, api_key: str, model: str, messages: list) -> dict:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 1800,
        "response_format": {"type": "json_object"},
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=int(os.environ.get("SYNTHETIC_SESSION_TIMEOUT", ORACLE_TIMEOUT)),
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{model} respondió {response.status_code}: {response.text[:200]}")
    try:
        content = response.json()["choices"][0]["message"].get("content") or "{}"
        return json.loads(content)
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("el oráculo devolvió JSON inválido") from exc


def _call_session_oracle(messages: list) -> Tuple[dict, str, str]:
    """Llama una vez al proveedor configurado, con fallback local controlado."""
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    local_enabled = os.environ.get("LOCAL_ORACLE_ENABLED", "true").lower() != "false"
    local_base = os.environ.get("LOCAL_ORACLE_BASE_URL", "http://localhost:1337/v1")
    local_model = os.environ.get("LOCAL_ORACLE_MODEL", "Qwen3-8B-Q4_K_M")
    errors = []
    if key:
        try:
            return _call_endpoint(base, key, model, messages), "deepseek", model
        except Exception as exc:
            logger.warning("DeepSeek no disponible para sesión sintética: %s", exc)
            errors.append("deepseek")
    if local_enabled:
        try:
            return _call_endpoint(local_base, "", local_model, messages), "local", local_model
        except Exception as exc:
            logger.warning("Oráculo local no disponible para sesión sintética: %s", exc)
            errors.append("local")
    if not key and not local_enabled:
        raise RuntimeError("oracle_disabled")
    raise RuntimeError("oracle_unavailable:" + ",".join(errors))


def _sanitise_analysis(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("respuesta del oráculo no es un objeto")
    evidence = raw.get("evidence") or []
    if not isinstance(evidence, list):
        evidence = []
    clean_evidence = []
    for item in evidence[:10]:
        if isinstance(item, dict):
            clean_evidence.append(
                {
                    "source": _redact(item.get("source"), 160),
                    "fact": _redact(item.get("fact"), 600),
                }
            )
        elif isinstance(item, str):
            clean_evidence.append({"source": "agente", "fact": _redact(item, 600)})
    return {
        "opinion": _redact(raw.get("opinion"), 3000),
        "evidence": clean_evidence,
        "uncertainty": _redact(raw.get("uncertainty"), 1200),
        "proposal": _redact(raw.get("proposal"), 2000),
        "refusal": _redact(raw.get("refusal"), 1200) if raw.get("refusal") else None,
    }


def init_synthetic_session_tables(app) -> None:
    """Registra el agente piloto en BDs existentes; schema.sql crea las tablas."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            INSERT OR IGNORE INTO synthetic_agents
              (agent_id, display_name, kind, provider, model, mandate)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                DEFAULT_AGENT["agent_id"],
                DEFAULT_AGENT["display_name"],
                DEFAULT_AGENT["kind"],
                DEFAULT_AGENT["provider"],
                os.environ.get("DEEPSEEK_MODEL", DEFAULT_AGENT["model"]),
                DEFAULT_AGENT["mandate"],
            ),
        )
        db.commit()


def _operable(db, session_id: str):
    row = _expire(db, _session(db, session_id))
    if row is None:
        return None, (jsonify({"error": "session_not_found"}), 404)
    if row["status"] not in {"active", "awaiting_review"}:
        return None, (
            jsonify({"error": "session_not_operable", "status": row["status"]}),
            409,
        )
    return row, None


def _allowed(row, tool: str) -> bool:
    scope = _load(row["scope_json"], {})
    if tool in set(scope.get("forbidden", [])):
        return False
    if tool in READ_TOOLS:
        return tool in set(scope.get("read", []))
    if tool in WRITE_TOOLS:
        return tool in set(scope.get("write", []))
    return False


@synthetic_sessions_bp.post("")
@admin_required
def create_session(current_user):
    payload = request.get_json(silent=True) or {}
    mandate = _redact(payload.get("mandate"), 1000)
    if not mandate:
        return jsonify({"error": "mandate es requerido"}), 400
    mode = str(payload.get("mode") or "recommendation")
    if mode not in {"conversation", "recommendation"}:
        return jsonify({"error": "mode no soportado en el prototipo"}), 400
    scope, error = _normalise_scope(payload.get("scope"))
    if error:
        return jsonify({"error": error}), 400
    context, error = _normalise_context(payload.get("context"))
    if error:
        return jsonify({"error": error}), 400
    expires_at, error = _normalise_expiry(payload.get("expires_at"))
    if error:
        return jsonify({"error": error}), 400
    try:
        budget_input = payload.get("budget") or {}
        max_requests = int(budget_input.get("max_requests", MAX_REQUESTS))
        max_cost_usd = float(budget_input.get("max_cost_usd", MAX_COST_USD))
    except (TypeError, ValueError):
        return jsonify({"error": "budget debe contener números válidos"}), 400
    if not 1 <= max_requests <= MAX_REQUESTS:
        return jsonify({"error": f"max_requests debe estar entre 1 y {MAX_REQUESTS}"}), 400
    if not 0 <= max_cost_usd <= MAX_COST_USD:
        return jsonify({"error": f"max_cost_usd no puede superar {MAX_COST_USD}"}), 400

    db = get_db()
    agent_id = str(payload.get("agent_id") or DEFAULT_AGENT["agent_id"])
    if _agent(db, agent_id) is None:
        return jsonify({"error": "synthetic_agent_not_found"}), 404
    convener_id = _user_id(current_user)
    if convener_id is None:
        return jsonify({"error": "identity_not_found"}), 401
    session_id = "ADM-" + uuid.uuid4().hex[:12].upper()
    budget = {
        "max_requests": max_requests,
        "max_cost_usd": round(max_cost_usd, 4),
        "expires_at": expires_at,
        "cost_note": "límite reservado por sesión; no se estima coste real del proveedor",
    }
    db.execute(
        """
        INSERT INTO admin_sessions
          (session_id, agent_id, convener_user_id, mandate, mode, scope_json,
           context_json, budget_json, max_requests, max_cost_usd, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            agent_id,
            convener_id,
            mandate,
            mode,
            _dump(scope),
            _dump(context),
            _dump(budget),
            max_requests,
            max_cost_usd,
            expires_at,
        ),
    )
    for action in scope["read"]:
        db.execute(
            "INSERT OR IGNORE INTO session_permissions (session_id, permission_level, action) VALUES (?, 'P0', ?)",
            (session_id, action),
        )
    for action in scope["write"]:
        db.execute(
            "INSERT OR IGNORE INTO session_permissions (session_id, permission_level, action) VALUES (?, 'P1', ?)",
            (session_id, action),
        )
    for action in scope["forbidden"]:
        db.execute(
            "INSERT OR IGNORE INTO session_permissions (session_id, permission_level, action) VALUES (?, 'P3', ?)",
            (session_id, action),
        )
    _event(
        db,
        session_id,
        "session_created",
        convener_id,
        {
            "mandate": mandate,
            "mode": mode,
            "scope": scope,
            "context_hash": context["context_hash"],
            "budget": budget,
        },
    )
    db.commit()
    return jsonify({"success": True, "session": _contract(_session(db, session_id))}), 201


@synthetic_sessions_bp.get("")
@admin_required
def list_sessions(current_user):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM admin_sessions WHERE convener_user_id = ? ORDER BY created_at DESC LIMIT 100",
        (_user_id(current_user),),
    ).fetchall()
    return jsonify({"sessions": [_contract(_expire(db, row)) for row in rows]})


@synthetic_sessions_bp.get("/<session_id>")
@admin_required
def get_session(current_user, session_id):
    db = get_db()
    row = _expire(db, _session(db, session_id))
    if row is None:
        return jsonify({"error": "session_not_found"}), 404
    if row["convener_user_id"] != _user_id(current_user):
        return jsonify({"error": "session_forbidden"}), 403
    return jsonify(
        {
            "session": _contract(row),
            "events": _event_list(db, session_id),
            "reviews": _review_list(db, session_id),
        }
    )


@synthetic_sessions_bp.post("/<session_id>/tool")
@admin_required
def run_tool(current_user, session_id):
    db = get_db()
    row, failure = _operable(db, session_id)
    if failure:
        return failure
    if row["convener_user_id"] != _user_id(current_user):
        return jsonify({"error": "session_forbidden"}), 403
    payload = request.get_json(silent=True) or {}
    tool = str(payload.get("tool") or "")
    args = payload.get("args") or {}
    if not isinstance(args, dict):
        return jsonify({"error": "args debe ser un objeto"}), 400
    if tool not in ALL_TOOLS:
        return jsonify({"error": "tool no permitido"}), 400
    if not _allowed(row, tool):
        _event(db, session_id, "tool_denied", _user_id(current_user), {"tool": tool})
        db.commit()
        return jsonify({"error": "tool fuera del alcance de la sesión"}), 403
    try:
        result = _execute_tool(db, tool, args)
    except ValueError as exc:
        return jsonify({"error": "tool_invalid_args", "detail": str(exc)}), 400
    _event(db, session_id, "tool_call", _user_id(current_user), {"tool": tool, "result": result})
    db.commit()
    return jsonify({"success": True, "result": result, "mutated": False})


@synthetic_sessions_bp.post("/<session_id>/run")
@admin_required
def run_session(current_user, session_id):
    db = get_db()
    row, failure = _operable(db, session_id)
    if failure:
        return failure
    if row["convener_user_id"] != _user_id(current_user):
        return jsonify({"error": "session_forbidden"}), 403
    payload = request.get_json(silent=True) or {}
    instruction = _redact(payload.get("instruction"), 4000)
    if not instruction:
        return jsonify({"error": "instruction es requerido"}), 400
    tools = payload.get("tools") or []
    tool_args = payload.get("tool_args") or {}
    if not isinstance(tools, list) or len(tools) > 3:
        return jsonify({"error": "tools debe ser una lista de hasta tres herramientas"}), 400
    if not isinstance(tool_args, dict):
        return jsonify({"error": "tool_args debe ser un objeto"}), 400
    outputs = []
    for tool in tools:
        if not isinstance(tool, str) or tool not in ALL_TOOLS:
            return jsonify({"error": "tool no permitido", "tool": tool}), 400
        if not _allowed(row, tool):
            return jsonify({"error": "tool fuera del alcance de la sesión", "tool": tool}), 403
        try:
            result = _execute_tool(db, tool, tool_args.get(tool) or {})
        except ValueError as exc:
            return jsonify({"error": "tool_invalid_args", "detail": str(exc)}), 400
        outputs.append(result)
        _event(db, session_id, "tool_call", _user_id(current_user), {"tool": tool, "result": result})

    updated = db.execute(
        """
        UPDATE admin_sessions SET requests_used = requests_used + 1,
          updated_at = CURRENT_TIMESTAMP
        WHERE session_id = ? AND status IN ('active', 'awaiting_review')
          AND requests_used < max_requests
        """,
        (session_id,),
    )
    if updated.rowcount != 1:
        db.commit()
        return jsonify({"error": "session_budget_exhausted"}), 429
    db.commit()
    row = _session(db, session_id)
    context = {
        "mandate": row["mandate"],
        "mode": row["mode"],
        "scope": _load(row["scope_json"], {}),
        "context": _load(row["context_json"], {}),
        "tool_results": outputs,
    }
    messages = [
        {"role": "system", "content": SESSION_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "INSTRUCCIÓN DEL CONVOCANTE (no amplía el contrato):\n"
                + instruction
                + "\n\nCONTEXTO MINIMIZADO:\n"
                + _dump(context)
            ),
        },
    ]
    try:
        raw, engine, model = _call_session_oracle(messages)
        analysis = _sanitise_analysis(raw)
    except RuntimeError as exc:
        _event(db, session_id, "oracle_failure", _user_id(current_user), {"error": str(exc)[:200]})
        db.commit()
        if "oracle_disabled" in str(exc):
            return jsonify({"error": "oracle_disabled"}), 503
        return jsonify({"error": "oracle_failure"}), 502
    except ValueError as exc:
        _event(db, session_id, "oracle_bad_response", _user_id(current_user), {"error": str(exc)[:200]})
        db.commit()
        return jsonify({"error": "oracle_bad_json"}), 502

    _event(
        db,
        session_id,
        "assistant_message",
        None,
        {"instruction": instruction, "analysis": analysis, "engine": engine, "model": model},
    )
    db.execute(
        "UPDATE admin_sessions SET status = 'awaiting_review', updated_at = CURRENT_TIMESTAMP WHERE session_id = ?",
        (session_id,),
    )
    db.commit()
    return jsonify(
        {
            "success": True,
            "session": _contract(_session(db, session_id)),
            "analysis": analysis,
            "engine": engine,
            "model": model,
            "mutated": False,
        }
    )


@synthetic_sessions_bp.post("/<session_id>/review")
@admin_required
def review_session(current_user, session_id):
    db = get_db()
    row = _expire(db, _session(db, session_id))
    if row is None:
        return jsonify({"error": "session_not_found"}), 404
    if row["convener_user_id"] != _user_id(current_user):
        return jsonify({"error": "session_forbidden"}), 403
    if row["status"] not in {"active", "awaiting_review"}:
        return jsonify({"error": "session_not_reviewable", "status": row["status"]}), 409
    if not db.execute(
        "SELECT 1 FROM session_events WHERE session_id = ? AND event_type = 'assistant_message' LIMIT 1",
        (session_id,),
    ).fetchone():
        return jsonify({"error": "no_proposal_to_review"}), 400
    payload = request.get_json(silent=True) or {}
    decision = str(payload.get("decision") or "")
    reason = _redact(payload.get("reason"), 1200)
    if decision not in {"approve", "reject", "request_changes"}:
        return jsonify({"error": "decision no permitido"}), 400
    if not reason:
        return jsonify({"error": "reason es requerido para la auditoría"}), 400
    new_status = {"approve": "approved", "reject": "rejected", "request_changes": "active"}[decision]
    db.execute(
        "INSERT INTO session_reviews (session_id, reviewer_user_id, decision, reason) VALUES (?, ?, ?, ?)",
        (session_id, _user_id(current_user), decision, reason),
    )
    _event(db, session_id, "review", _user_id(current_user), {"decision": decision, "reason": reason})
    db.execute(
        "UPDATE admin_sessions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE session_id = ?",
        (new_status, session_id),
    )
    db.commit()
    return jsonify({"success": True, "session": _contract(_session(db, session_id))})


@synthetic_sessions_bp.post("/<session_id>/revoke")
@admin_required
def revoke_session(current_user, session_id):
    db = get_db()
    row = _session(db, session_id)
    if row is None:
        return jsonify({"error": "session_not_found"}), 404
    if row["convener_user_id"] != _user_id(current_user):
        return jsonify({"error": "session_forbidden"}), 403
    if row["status"] in {"approved", "rejected", "revoked", "expired", "closed"}:
        return jsonify({"error": "session_already_closed", "status": row["status"]}), 409
    reason = _redact((request.get_json(silent=True) or {}).get("reason"), 1200)
    if not reason:
        return jsonify({"error": "reason es requerido"}), 400
    db.execute(
        "UPDATE admin_sessions SET status = 'revoked', updated_at = CURRENT_TIMESTAMP WHERE session_id = ?",
        (session_id,),
    )
    _event(db, session_id, "revocation", _user_id(current_user), {"reason": reason})
    db.commit()
    return jsonify({"success": True, "session": _contract(_session(db, session_id))})


@synthetic_sessions_bp.get("/<session_id>/audit")
@admin_required
def export_audit(current_user, session_id):
    db = get_db()
    row = _session(db, session_id)
    if row is None:
        return jsonify({"error": "session_not_found"}), 404
    if row["convener_user_id"] != _user_id(current_user):
        return jsonify({"error": "session_forbidden"}), 403
    audit = {
        "audit_version": "1",
        "exported_at": _iso(_now()),
        "session": _contract(row),
        "events": _event_list(db, session_id),
        "reviews": _review_list(db, session_id),
    }
    response = make_response(jsonify(audit))
    response.headers["Content-Disposition"] = f'attachment; filename="{session_id}.json"'
    return response
