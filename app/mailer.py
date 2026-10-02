"""Envío de correos transaccionales (SMTP del .env, nunca a Git).

Variables leídas del entorno (ver config.example.env):
  SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
  FROM_EMAIL, FROM_NAME, FRONTEND_URL.

Si falta configuración, el envío se omite en silencio (best-effort) y
el flujo de restablecimiento sigue respondiendo genérico para no
enumerar cuentas. En testing/desarrollo el token puede exponerse en la
respuesta JSON (ver auth.forgot); en producción jamás.
"""

import os
import smtplib
from email.message import EmailMessage


def smtp_configured() -> bool:
    return bool(os.environ.get("SMTP_SERVER") and os.environ.get("SMTP_USERNAME"))


def _smtp_configured() -> bool:
    return smtp_configured()


def build_reset_url(token: str) -> str:
    base = (os.environ.get("FRONTEND_URL") or "http://localhost:3000").rstrip("/")
    return f"{base}/reset?token={token}"


def send_reset_email(to_email: str, reset_url: str) -> bool:
    """Envía el correo de restablecimiento. True si se envió, False si no.

    Nunca lanza: el llamador no debe romper el flujo por un fallo de correo.
    """
    if not _smtp_configured():
        print(
            "Warning: SMTP sin configurar (SMTP_SERVER/SMTP_USERNAME en .env),"
            " correo omitido. El aviso queda en la bandeja interna."
        )
        return False
    try:
        server = os.environ.get("SMTP_SERVER", "")
        port = int(os.environ.get("SMTP_PORT") or "587")
        username = os.environ.get("SMTP_USERNAME", "")
        password = os.environ.get("SMTP_PASSWORD", "")
        from_email = os.environ.get("FROM_EMAIL") or username
        from_name = os.environ.get("FROM_NAME") or "Maxocracia"

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

        with smtplib.SMTP(server, port, timeout=10) as smtp:
            smtp.starttls()
            if username:
                smtp.login(username, password)
            smtp.send_message(msg)
        return True
    except Exception as exc:  # best-effort: no romper el flujo ni filtrar detalles
        print(f"Warning: no se pudo enviar correo de reset: {type(exc).__name__}")
        return False
