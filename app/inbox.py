"""Bandeja interna — el relevo cuando el correo no llega.

Mínimo viable del Puente de Llegada: cada invitación de admin y cada
solicitud de reset deja una fila en `maxo_inbox` dirigida al email.
El dueño la lee en /bandeja; el facilitador la releva desde el outbox
admin (T13: quién creó qué, cuándo).

Regla de seguridad: el link de `password_reset` se guarda para relevo
admin pero se redacta en la bandeja del propio dueño (si una sesión
comprometida pudiera leer el token, el correo dejaría de autenticar
la recuperación). Los links de invitación sí son compartibles por diseño.
"""

from flask import Blueprint, jsonify, request

from .jwt_utils import admin_required, token_required
from .utils import get_db

inbox_bp = Blueprint("inbox", __name__, url_prefix="/inbox")


def deliver(
    to_email, kind, subject="", body="", link_url=None, created_by=None,
    mail_status="unknown",
):
    """Guarda un mensaje en la bandeja. Best-effort: nunca lanza.

    mail_status: 'sent' (el correo salió), 'failed' (SMTP lo rechazó),
    'skipped' (sin SMTP configurado) o 'unknown' (no aplica, p. ej. invite).
    """
    try:
        db = get_db()
        db.execute(
            "INSERT INTO maxo_inbox (to_email, kind, subject, body, link_url,"
            " mail_status, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(to_email).strip().lower(),
                kind,
                subject,
                body,
                link_url,
                mail_status,
                created_by,
            ),
        )
        db.commit()
        return True
    except Exception as exc:
        print(f"Warning: no se pudo guardar en bandeja: {type(exc).__name__}")
        return False


def _own_email(db, current_user):
    row = db.execute(
        "SELECT email FROM users WHERE id = ?", (current_user.get("user_id"),)
    ).fetchone()
    if row is None:
        return None
    return str(row["email"]).strip().lower()


def _public_row(r):
    d = dict(r)
    if d.get("kind") == "password_reset":
        d["has_link"] = bool(d.get("link_url"))
        d["link_url"] = None  # redactado al dueño: el correo autentica
    return d


@inbox_bp.route("", methods=["GET"])
@token_required
def my_inbox(current_user):
    """Bandeja propia: mensajes dirigidos al email del token."""
    db = get_db()
    email = _own_email(db, current_user)
    if email is None:
        return jsonify({"error": "user not found"}), 404
    rows = db.execute(
        "SELECT id, to_email, kind, subject, body, link_url, status,"
        " mail_status, created_at"
        " FROM maxo_inbox WHERE lower(to_email) = ? ORDER BY id DESC LIMIT 100",
        (email,),
    ).fetchall()
    return jsonify([_public_row(r) for r in rows])


@inbox_bp.route("/<int:msg_id>/read", methods=["POST"])
@token_required
def mark_read(current_user, msg_id):
    """Marca un mensaje propio como leído."""
    db = get_db()
    email = _own_email(db, current_user)
    if email is None:
        return jsonify({"error": "user not found"}), 404
    row = db.execute(
        "SELECT id FROM maxo_inbox WHERE id = ? AND lower(to_email) = ?",
        (msg_id, email),
    ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    db.execute("UPDATE maxo_inbox SET status = 'read' WHERE id = ?", (msg_id,))
    db.commit()
    return jsonify({"success": True, "id": msg_id})


@inbox_bp.route("/outbox", methods=["GET"])
@admin_required
def outbox(current_user):
    """Outbox del facilitador: relevo manual con links completos."""
    kind = (request.args.get("kind") or "").strip()
    db = get_db()
    if kind in ("invite", "password_reset", "notice"):
        rows = db.execute(
            "SELECT id, to_email, kind, subject, body, link_url, status,"
            " mail_status, created_by, created_at FROM maxo_inbox"
            " WHERE kind = ? ORDER BY id DESC LIMIT 200",
            (kind,),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT id, to_email, kind, subject, body, link_url, status,"
            " mail_status, created_by, created_at FROM maxo_inbox"
            " ORDER BY id DESC LIMIT 200"
        ).fetchall()
    return jsonify([dict(r) for r in rows])
