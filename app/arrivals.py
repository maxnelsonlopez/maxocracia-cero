"""
Puente de Llegada — la puerta de entrada de la Cohorte (Sun Tzu + Ternura).

Dos artes combinadas en una sola puerta:

1. ENAMORAR CON RESPETO: quien llega invitado no es un cliente, es un futuro
   vecino. La invitación firma el email (HMAC con la SECRET_KEY del servidor)
   y el visitante es recibido sin presión: primero su pulso, luego su
   acuerdo; la voz en la gobernanza llega con el tiempo (Cap. 13, escalera
   de confianza N0-N4).

2. DESARMAR AL ENEMIGO: "la mejor victoria es vencer sin combatir" (Sun Tzu).
   No peleamos contra los bots: los recibimos en una cuarentena donde su
   flujo queda registrado y observado sin dañar a nadie. El honeypot es un
   campo que solo un bot llena; al llenarlo, el sistema responde con éxito
   aparente y tokens inertes — el bot cree haber entrado y su comportamiento
   queda en la bitácora (maxo_arrivals) para entenderlo y reubicarlo.

Referencias: Cap. 13 (niveles de confianza N0-N4), Cap. 15 (Cohorte Cero),
"El arte de la guerra" (Sun Tzu, cap. 3: vencer sin combatir).
"""

import base64
import hashlib
import hmac
import os
from typing import Optional

from flask import Blueprint, current_app, jsonify

from .jwt_utils import admin_required
from .utils import get_db

arrivals_bp = Blueprint("arrivals", __name__, url_prefix="/invite")


def _secret() -> str:
    """Secreto de firma: SECRET_KEY del entorno (run.py la fuerza en
    desarrollo; nunca en producción). current_app como respaldo."""
    env_secret = os.environ.get("SECRET_KEY")
    if env_secret:
        return env_secret
    try:
        return current_app.config.get("SECRET_KEY") or "dev-secret"
    except RuntimeError:
        return "dev-secret"


def sign_invite(email: str) -> str:
    """Firma el email del invitado: base64(email).hmac(secret, email)[:16].

    El token no revela información a quien lo intercepte (base64 no es
    cifrado, pero el HMAC impide forjar invitaciones).
    """
    raw = (
        base64.urlsafe_b64encode(email.lower().encode("utf-8"))
        .decode("ascii")
        .rstrip("=")
    )
    sig = hmac.new(
        _secret().encode("utf-8"), email.lower().encode("utf-8"), hashlib.sha256
    ).hexdigest()[:16]
    return f"{raw}.{sig}"


def verify_invite(token: str) -> Optional[str]:
    """Valida el token y devuelve el email firmado, o None si es inválido."""
    try:
        raw, sig = token.split(".", 1)
        padded = raw + "=" * (-len(raw) % 4)
        email = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8").lower()
    except Exception:
        return None
    expected = hmac.new(
        _secret().encode("utf-8"), email.encode("utf-8"), hashlib.sha256
    ).hexdigest()[:16]
    if not hmac.compare_digest(sig, expected):
        return None
    return email


def mask_email(email: str) -> str:
    """Opacidad Sagrada: el email se muestra enmascarado en la plaza."""
    local, _, domain = email.partition("@")
    if len(local) <= 1:
        return f"{local}***@{domain}"
    return f"{local[0]}***{local[-1]}@{domain}"


@arrivals_bp.route("/<token>", methods=["GET"])
def invite(token: str):
    """
    Puerta de llegada (pública): valida la invitación firmada.

    Devuelve un mensaje de bienvenida sin presión y el email enmascarado.
    Un token inválido responde 404 sin información (no confirmamos existencia).
    """
    email = verify_invite(token)
    if email is None:
        return jsonify({"error": "invitación no válida"}), 404

    db = get_db()
    row = db.execute("SELECT id FROM users WHERE lower(email) = ?", (email,)).fetchone()
    return jsonify(
        {
            "valid": True,
            "email_masked": mask_email(email),
            "already_registered": row is not None,
            "welcome": (
                "Bienvenido a la Cohorte. No hay prisa: primero tu pulso, luego tu acuerdo. "
                "La voz en la gobernanza llega con el tiempo, no con prisa."
            ),
            "register_url": f"/register?email={email}",
        }
    )


@arrivals_bp.route("/quarantine", methods=["GET"])
@admin_required
def quarantine_list(current_user):
    """Cuarentena (admin): el flujo de los bots, observado sin combatirlo."""
    db = get_db()
    rows = db.execute(
        "SELECT id, email, source, honeypot_hit, status, created_at FROM maxo_arrivals ORDER BY id DESC LIMIT 200"
    ).fetchall()
    return jsonify(
        [
            {
                "id": r["id"],
                "email": r["email"],
                "source": r["source"],
                "honeypot_hit": bool(r["honeypot_hit"]),
                "status": r["status"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]
    )
