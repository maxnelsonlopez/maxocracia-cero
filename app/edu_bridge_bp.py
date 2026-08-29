# -*- coding: utf-8 -*-
"""
Blueprint del Puente de Identidad del Organismo Educativo Vital (OEV).

Conecta la plataforma principal de Maxocracia (:5001) con los nodos de
aprendizaje del OEV (:5050).

Permite:
1. Validar el estado de identidad unificada y configuración de federación.
2. Registrar y sincronizar eventos de maestría/mentoría verificados en el
   OEV hacia el Perfil Vital con trazabilidad T13.
3. Impacto en la Escalera de Confianza (N0 -> N1) por transferencia demostrada.
"""

import hashlib
import hmac
import os
from datetime import datetime, timezone
from typing import Any, Dict

from flask import Blueprint, jsonify, request

from .jwt_utils import token_required
from .utils import get_db

edu_bridge_bp = Blueprint("edu_bridge", __name__, url_prefix="/edu-bridge")

_DEFAULT_OEV_NODE_URL = os.environ.get("EDUCATIONAL_PLATFORM_URL", "http://localhost:5050")

# Token de servicio del nodo OEV: la sincronización NO la declara el usuario,
# la reporta el nodo educativo con su propio secreto (procedencia verificable).
# Sin esta variable, el puente queda apagado (fail-closed): nada de eventos.
EDU_BRIDGE_SERVICE_TOKEN = os.environ.get("EDU_BRIDGE_SERVICE_TOKEN")


def init_edu_bridge_tables(app):
    """Crea la tabla de eventos de maestría sincronizados del OEV si no existe."""
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS edu_mastery_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                topic_slug TEXT NOT NULL,
                branch_slug TEXT NOT NULL,
                score REAL,
                mentor_rounds INTEGER NOT NULL DEFAULT 0,
                triada_approved INTEGER NOT NULL DEFAULT 0,
                verified_at TEXT NOT NULL,
                t13_hash TEXT
            )
            """
        )
        db.commit()


@edu_bridge_bp.route("/status", methods=["GET"])
@token_required
def status(current_user: Dict[str, Any]):
    """Devuelve el estado de la identidad unificada y la URL del nodo educativo."""
    user_id = current_user.get("user_id")
    if not user_id:
        return jsonify({"error": "invalid token"}), 401

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return jsonify({"error": "user not found"}), 404

    return (
        jsonify(
            {
                "unified_identity": True,
                "user_id": user["id"],
                "email": user["email"],
                "alias": user["alias"] if "alias" in user.keys() else None,
                "trust_level": user["trust_level"] if "trust_level" in user.keys() else 0,
                "oev_node_url": _DEFAULT_OEV_NODE_URL,
            }
        ),
        200,
    )


@edu_bridge_bp.route("/sync-mastery", methods=["POST"])
def sync_mastery():
    """Sincroniza un hito de maestría o mentoría verificado por el nodo OEV (T13).

    Procedencia: el evento NO lo declara el usuario (eso convertiría la escalera
    de confianza en un ascensor); lo reporta el nodo educativo :5050 con su
    token de servicio (`X-Edu-Bridge-Token`). El token de servicio es SUFICIENTE
    (la sincronización automática es servicio-a-servicio); si además hay un JWT
    humano válido, se acepta su `user_id` como objetivo salvo que el nodo
    reporte uno explícito. Sin token configurado, el puente queda cerrado
    (fail-closed).

    El evento queda como EVIDENCIA en el Perfil Vital; la escalera N0→N1 sigue
    siendo asunto del primer acuerdo (Cap. 13) — la formación que pese en la voz
    es una decisión de parlamento, no un endpoint.
    """
    from .jwt_utils import verify_token

    # El emisor humano (si lo hay): su JWT es opcional gracias al token de servicio.
    bearer = ""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        bearer = auth_header.split(" ", 1)[1].strip()
    emisor = verify_token(bearer) if bearer else None

    data = request.get_json(silent=True) or {}

    # Procedencia del nodo OEV (comparación en tiempo constante, T13).
    presented = request.headers.get("X-Edu-Bridge-Token") or ""
    if not EDU_BRIDGE_SERVICE_TOKEN or not hmac.compare_digest(
        presented, EDU_BRIDGE_SERVICE_TOKEN
    ):
        return (
            jsonify(
                {
                    "error": "el nodo educativo debe reportar con su token de servicio (X-Edu-Bridge-Token)",
                    "code": "BRIDGE_TOKEN_REQUIRED",
                    "hint": "configura EDU_BRIDGE_SERVICE_TOKEN en :5001 y en el nodo OEV",
                }
            ),
            403,
        )

    # Identidad del evento: user_id reportado por el nodo, o el del JWT humano
    # si el emisor es una persona (retrocompatibilidad).
    reported = data.get("user_id")
    if reported is not None:
        try:
            target_user_id = int(reported)
        except (TypeError, ValueError):
            return jsonify({"error": "user_id reportado debe ser un entero"}), 400
    elif emisor and emisor.get("user_id"):
        target_user_id = int(emisor["user_id"])
    else:
        return (
            jsonify(
                {
                    "error": "se requiere user_id reportado o un JWT humano de emisor",
                    "code": "TARGET_USER_REQUIRED",
                }
            ),
            400,
        )
    db = get_db()
    target = db.execute("SELECT id FROM users WHERE id = ?", (target_user_id,)).fetchone()
    if target is None:
        return jsonify({"error": f"user_id {target_user_id} no existe en Maxocracia"}), 404

    topic_slug = (data.get("topic_slug") or "").strip()
    branch_slug = (data.get("branch_slug") or "").strip()
    score = data.get("score")
    if score is not None:
        try:
            score = max(0.0, min(100.0, float(score)))
        except (TypeError, ValueError):
            score = None
    mentor_rounds = int(data.get("mentor_rounds") or 0)
    triada_approved = 1 if data.get("triada_approved") else 0

    if not topic_slug or not branch_slug:
        return jsonify({"error": "topic_slug y branch_slug son requeridos."}), 400

    now = datetime.now(timezone.utc).isoformat()
    # T13 real: hash SHA-256 de los datos del evento (auditable, no una cadena).
    t13_hash = hashlib.sha256(
        "|".join(
            [
                str(target_user_id),
                topic_slug,
                branch_slug,
                str(score),
                str(mentor_rounds),
                str(triada_approved),
                now,
            ]
        ).encode("utf-8")
    ).hexdigest()

    cur = db.execute(
        """
        INSERT INTO edu_mastery_events (
            user_id, topic_slug, branch_slug, score, mentor_rounds, triada_approved, verified_at, t13_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            target_user_id,
            topic_slug,
            branch_slug,
            score,
            mentor_rounds,
            triada_approved,
            now,
            t13_hash,
        ),
    )
    event_id = cur.lastrowid
    db.commit()

    return (
        jsonify(
            {
                "synced": True,
                "event_id": event_id,
                "t13_hash": t13_hash,
                "trust_effect": "none",
                "note": "la escalera de confianza sigue siendo por el primer acuerdo (Cap. 13); el evento queda como evidencia educativa",
            }
        ),
        201,
    )


@edu_bridge_bp.route("/events", methods=["GET"])
@token_required
def get_events(current_user: Dict[str, Any]):
    """Lista el historial de eventos educativos sincronizados para el usuario."""
    user_id = current_user.get("user_id")
    if not user_id:
        return jsonify({"error": "invalid token"}), 401

    db = get_db()
    rows = db.execute(
        "SELECT * FROM edu_mastery_events WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()

    events = [
        {
            "id": r["id"],
            "topic_slug": r["topic_slug"],
            "branch_slug": r["branch_slug"],
            "score": r["score"],
            "mentor_rounds": r["mentor_rounds"],
            "triada_approved": bool(r["triada_approved"]),
            "verified_at": r["verified_at"],
            "t13_hash": r["t13_hash"],
        }
        for r in rows
    ]
    return jsonify({"events": events, "count": len(events)}), 200
