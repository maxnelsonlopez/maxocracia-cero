import pytest
from app.validators import (
    validate_email,
    validate_password,
    validate_name,
    validate_alias,
    validate_amount,
    validate_user_id
)


def test_email_validation():
    """Prueba la validación de correos electrónicos."""
    # Correos válidos
    assert validate_email("usuario@dominio.com") is True
    assert validate_email("usuario.nombre@dominio.co") is True
    assert validate_email("usuario+etiqueta@dominio.com.mx") is True
    
    # Correos inválidos
    assert validate_email("") is False
    assert validate_email(None) is False
    assert validate_email("usuario@") is False
    assert validate_email("usuario@dominio") is False
    assert validate_email("@dominio.com") is False
    assert validate_email("usuario dominio.com") is False
    assert validate_email(123) is False


def test_password_validation():
    """Prueba la validación de contraseñas."""
    # Contraseñas válidas
    assert validate_password("Password123") is True
    assert validate_password("Segura2023!") is True
    assert validate_password("aB1!cD2@eF3#") is True
    
    # Contraseñas inválidas
    assert validate_password("") is False
    assert validate_password(None) is False
    assert validate_password("corta1A") is False  # Muy corta
    assert validate_password("sinmayuscula123") is False  # Sin mayúscula
    assert validate_password("SINMINUSCULA123") is False  # Sin minúscula
    assert validate_password("SinNumeros") is False  # Sin números
    assert validate_password(12345678) is False  # No es string


def test_name_validation():
    """Prueba la validación de nombres."""
    # Nombres válidos
    assert validate_name("Juan Pérez") is True
    assert validate_name("A") is True  # Nombre corto pero válido
    
    # Nombres inválidos
    assert validate_name("") is False
    assert validate_name(None) is False
    assert validate_name("X" * 101) is False  # Excede longitud máxima
    assert validate_name(12345) is False  # No es string


def test_alias_validation():
    """Prueba la validación de alias."""
    # Alias válidos
    assert validate_alias("juanp") is True
    assert validate_alias("usuario_123") is True
    
    # Alias inválidos
    assert validate_alias("") is False
    assert validate_alias(None) is False
    assert validate_alias("X" * 51) is False  # Excede longitud máxima
    assert validate_alias(12345) is False  # No es string


def test_amount_validation():
    """Prueba la validación de montos."""
    # Montos válidos
    assert validate_amount(100) is True
    assert validate_amount(0.5) is True
    assert validate_amount("10.5") is True
    
    # Montos inválidos
    assert validate_amount(0) is False
    assert validate_amount(-10) is False
    assert validate_amount("abc") is False
    assert validate_amount("") is False
    assert validate_amount(None) is False


def test_user_id_validation():
    """Prueba la validación de IDs de usuario."""
    # IDs válidos
    assert validate_user_id(1) is True
    assert validate_user_id("1") is True
    
    # IDs inválidos
    assert validate_user_id(0) is False
    assert validate_user_id(-1) is False
    assert validate_user_id("abc") is False
    assert validate_user_id("") is False
    assert validate_user_id(None) is False