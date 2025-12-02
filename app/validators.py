import os
import re
from functools import wraps
from flask import request, jsonify

# Patrones de validación
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PASSWORD_MIN_LENGTH = 8
NAME_MAX_LENGTH = 100
ALIAS_MAX_LENGTH = 50


def validate_email(email):
    """Valida que el email tenga un formato correcto"""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.match(email))


def validate_password(password):
    """Valida que la contraseña cumpla con requisitos mínimos de seguridad

    La contraseña debe tener al menos 8 caracteres, incluyendo al menos
    una letra mayúscula, una minúscula y un número.
    """
    if not password or not isinstance(password, str):
        return False

    # Verificar longitud mínima
    if len(password) < PASSWORD_MIN_LENGTH:
        return False

    # Verificar que tenga al menos una mayúscula, una minúscula y un número
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit


def validate_name(name):
    """Valida que el nombre no exceda la longitud máxima"""
    if not name or not isinstance(name, str):
        return False
    return len(name) <= NAME_MAX_LENGTH


def validate_alias(alias):
    """Valida que el alias no exceda la longitud máxima"""
    if not alias or not isinstance(alias, str):
        return False
    return len(alias) <= ALIAS_MAX_LENGTH


def validate_amount(amount):
    """Valida que el monto sea un número positivo"""
    try:
        amount_float = float(amount)
        return amount_float > 0
    except (ValueError, TypeError):
        return False


def validate_user_id(user_id):
    """Valida que el ID de usuario sea un entero positivo"""
    try:
        user_id_int = int(user_id)
        return user_id_int > 0
    except (ValueError, TypeError):
        return False


def validate_json_request(schema):
    """Decorador para validar solicitudes JSON según un esquema definido"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            errors = {}

            for field, validator in schema.items():
                if field in data:
                    if not validator(data[field]):
                        errors[field] = "valor inválido"
                elif field.endswith("?"):  # Campo opcional
                    continue
                else:  # Campo requerido
                    errors[field] = "campo requerido"

            if errors:
                # Usar mensajes genéricos sin detalles técnicos
                return (
                    jsonify(
                        {
                            "error": "entrada inválida",
                            "details": {"campo": "valor inválido"},
                        }
                    ),
                    400,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator
