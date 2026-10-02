"""Envío de correos transaccionales (SMTP del .env, nunca a Git).

Entiende dos convenciones de nombres (SMTP_* manda si ambas existen):
  SMTP_SERVER  | MAIL_SERVER      (p. ej. smtp.gmail.com)
  SMTP_PORT    | MAIL_PORT        (587 con STARTTLS, 465 con SSL)
  SMTP_USERNAME| MAIL_USERNAME
  SMTP_PASSWORD| MAIL_PASSWORD    (en Gmail: contraseña de aplicación)
  FROM_EMAIL   | MAIL_DEFAULT_SENDER
  FROM_NAME                      (solo SMTP_*)
  MAIL_ENABLED                   (True/False maestro, convención Flask-Mail)
  MAIL_USE_TLS / MAIL_USE_SSL
  FRONTEND_URL                   (arma el enlace de /reset)

Si falta configuración o MAIL_ENABLED=False, el envío se omite con un
Warning en consola (best-effort) y el flujo sigue respondiendo genérico
para no enumerar cuentas. En testing/desarrollo el token puede exponerse
en la respuesta JSON (ver auth.forgot); en producción jamás.
"""

import os
import smtplib
from email.message import EmailMessage


def _get(smtp_name: str, mail_name: str, default: str = "") -> str:
    return (os.environ.get(smtp_name) or os.environ.get(mail_name) or default).strip()


def _flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def mail_enabled() -> bool:
    """Interruptor maestro. Si no está definido, manda la presencia de servidor."""
    raw = os.environ.get("MAIL_ENABLED")
    if raw is not None:
        return raw.strip().lower() in ("1", "true", "yes", "on")
    return True


def smtp_configured() -> bool:
    return bool(_get("SMTP_SERVER", "MAIL_SERVER") and _get("SMTP_USERNAME", "MAIL_USERNAME"))


def _smtp_configured() -> bool:
    return smtp_configured()


def build_reset_url(token: str) -> str:
    base = (os.environ.get("FRONTEND_URL") or "http://localhost:3000").rstrip("/")
    return f"{base}/reset?token={token}"


def send_reset_email(to_email: str, reset_url: str) -> bool:
    """Envía el correo de restablecimiento. True si se envió, False si no.

    Nunca lanza: el llamador no debe romper el flujo por un fallo de correo.
    """
    if not mail_enabled():
        print(
            "Warning: MAIL_ENABLED=False en .env, correo omitido. "
            "El aviso queda en la bandeja interna."
        )
        return False
    if not _smtp_configured():
        print(
            "Warning: SMTP sin configurar (SMTP_SERVER/MAIL_SERVER y "
            "SMTP_USERNAME/MAIL_USERNAME en .env), correo omitido. "
            "El aviso queda en la bandeja interna."
        )
        return False
    try:
        server = _get("SMTP_SERVER", "MAIL_SERVER")
        port = int(_get("SMTP_PORT", "MAIL_PORT", "587"))
        username = _get("SMTP_USERNAME", "MAIL_USERNAME")
        password = _get("SMTP_PASSWORD", "MAIL_PASSWORD")
        from_email = _get("FROM_EMAIL", "MAIL_DEFAULT_SENDER") or username
        from_name = (os.environ.get("FROM_NAME") or "Maxocracia").strip()
        use_ssl = _flag("MAIL_USE_SSL", default=(port == 465))
        use_tls = _flag("MAIL_USE_TLS", default=(port == 587))

        msg = EmailMessage()
        msg["Subject"] = "Restablece tu contraseña — Maxocracia"
        msg["From"] = f"{from_name} <{from_email}>"
        msg["To"] = to_email
        msg.set_content(
            "Hola,\n\n"
            "Pediste restablecer tu contraseña en Maxocracia.\n\n"
            f"Abre este enlace (vale 1 hora, un solo uso):\n{reset_url}\n\n"
            "Si no fuiste tú, ignora este correo: tu contraseña sigue intacta.\n\n"
            "— Primero tu pulso, luego tu acuerdo."
        )

        if use_ssl:
            with smtplib.SMTP_SSL(server, port, timeout=10) as smtp:
                if username:
                    smtp.login(username, password)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(server, port, timeout=10) as smtp:
                if use_tls:
                    smtp.starttls()
                if username:
                    smtp.login(username, password)
                smtp.send_message(msg)
        return True
    except Exception as exc:  # best-effort: no romper el flujo ni filtrar detalles
        print(f"Warning: no se pudo enviar correo de reset: {type(exc).__name__}")
        return False
