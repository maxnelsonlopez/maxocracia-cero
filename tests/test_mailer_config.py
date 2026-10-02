"""Mailer bilingüe: entiende SMTP_* y MAIL_* (convención Flask-Mail).

- MAIL_SERVER/PORT/USERNAME/PASSWORD se usan para conectar y autenticar.
- MAIL_ENABLED=False omite el envío sin intentar conectar.
- SMTP_* tiene precedencia si ambas convenciones existen.
- MAIL_USE_SSL=True usa SMTP_SSL; por defecto (587) usa STARTTLS.
"""

from unittest.mock import patch

from app import mailer


class _FakeSMTP:
    instances = []

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.starttls_called = False
        self.login_args = None
        self.sent = []
        _FakeSMTP.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self):
        self.starttls_called = True

    def login(self, user, password):
        self.login_args = (user, password)

    def send_message(self, msg):
        self.sent.append(msg)


class _FakeSMTP_SSL(_FakeSMTP):
    pass


def _clean_env(monkeypatch):
    for var in (
        "SMTP_SERVER", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD",
        "MAIL_SERVER", "MAIL_PORT", "MAIL_USERNAME", "MAIL_PASSWORD",
        "MAIL_ENABLED", "MAIL_USE_TLS", "MAIL_USE_SSL",
        "FROM_EMAIL", "MAIL_DEFAULT_SENDER", "FROM_NAME",
    ):
        monkeypatch.delenv(var, raising=False)
    _FakeSMTP.instances.clear()


def test_mail_vars_envian_por_gmail_587(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setenv("MAIL_SERVER", "smtp.gmail.com")
    monkeypatch.setenv("MAIL_PORT", "587")
    monkeypatch.setenv("MAIL_USERNAME", "maxocracia@gmail.com")
    monkeypatch.setenv("MAIL_PASSWORD", "abcdefghijklmnop")
    monkeypatch.setenv("MAIL_USE_TLS", "True")
    monkeypatch.setenv("MAIL_ENABLED", "True")

    assert mailer.smtp_configured() is True
    assert mailer.mail_enabled() is True

    with patch.object(mailer.smtplib, "SMTP", _FakeSMTP):
        assert mailer.send_reset_email("x@y.test", "http://x/reset?token=t") is True

    conn = _FakeSMTP.instances[-1]
    assert (conn.host, conn.port) == ("smtp.gmail.com", 587)
    assert conn.starttls_called is True
    assert conn.login_args == ("maxocracia@gmail.com", "abcdefghijklmnop")
    assert len(conn.sent) == 1


def test_mail_enabled_false_omite_sin_conectar(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setenv("MAIL_SERVER", "smtp.gmail.com")
    monkeypatch.setenv("MAIL_USERNAME", "maxocracia@gmail.com")
    monkeypatch.setenv("MAIL_ENABLED", "False")

    assert mailer.mail_enabled() is False
    with patch.object(mailer.smtplib, "SMTP", _FakeSMTP):
        assert mailer.send_reset_email("x@y.test", "http://x/reset?token=t") is False
    assert _FakeSMTP.instances == []


def test_smtp_tiene_precedencia_y_ssl(monkeypatch):
    _clean_env(monkeypatch)
    monkeypatch.setenv("SMTP_SERVER", "smtp.propio.test")
    monkeypatch.setenv("MAIL_SERVER", "smtp.gmail.com")
    monkeypatch.setenv("SMTP_USERNAME", "a@propio.test")
    monkeypatch.setenv("MAIL_USERNAME", "maxocracia@gmail.com")
    monkeypatch.setenv("MAIL_USE_SSL", "True")
    monkeypatch.setenv("MAIL_PORT", "465")

    with patch.object(mailer.smtplib, "SMTP_SSL", _FakeSMTP_SSL):
        assert mailer.send_reset_email("x@y.test", "http://x/reset?token=t") is True

    conn = _FakeSMTP_SSL.instances[-1]
    assert (conn.host, conn.port) == ("smtp.propio.test", 465)
    assert conn.login_args == ("a@propio.test", "")
