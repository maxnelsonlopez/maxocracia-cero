"""Separación de claves JWT (parche de seguridad).

Con JWT_KEY_SEPARATION=1 las firmas usan JWT_SECRET_KEY (dedicada) y no la
SECRET_KEY de sesión/HMAC; una fuga en un uso no compromete el otro. Sin el
flag se mantiene la compatibilidad (SECRET_KEY), para migrar sin cortar la
federación con la escuela.
"""

import jwt as pyjwt
import pytest

from app import jwt_utils


@pytest.fixture
def reset_secret(monkeypatch):
    """La clave se cachea en jwt_utils.SECRET; aislar cada test."""
    monkeypatch.setattr(jwt_utils, "SECRET", None)
    yield
    monkeypatch.setattr(jwt_utils, "SECRET", None)


def test_clave_dedicada_firma_y_verifica(monkeypatch, reset_secret):
    monkeypatch.setenv("SECRET_KEY", "clave-sesion-0123456789abcdef")
    monkeypatch.setenv("JWT_SECRET_KEY", "clave-firma-dedicada-0123456789")
    monkeypatch.setenv("JWT_KEY_SEPARATION", "1")

    token = jwt_utils.create_token({"user_id": 7})
    assert jwt_utils.verify_token(token) is not None

    # La SECRET_KEY de sesión NO valida la firma (claves separadas).
    with pytest.raises(pyjwt.InvalidSignatureError):
        pyjwt.decode(token, "clave-sesion-0123456789abcdef", algorithms=["HS256"])


def test_sin_flag_usa_secret_key(monkeypatch, reset_secret):
    monkeypatch.setenv("SECRET_KEY", "clave-sesion-0123456789abcdef")
    monkeypatch.setenv("JWT_SECRET_KEY", "clave-firma-dedicada-0123456789")
    monkeypatch.delenv("JWT_KEY_SEPARATION", raising=False)

    token = jwt_utils.create_token({"user_id": 7})
    assert jwt_utils.verify_token(token) is not None

    # Compatibilidad: con el flag apagado la firma sigue siendo SECRET_KEY.
    with pytest.raises(pyjwt.InvalidSignatureError):
        pyjwt.decode(token, "clave-firma-dedicada-0123456789", algorithms=["HS256"])
