
import base64
import hashlib
import pytest
from app.refresh_utils import (
    generate_refresh_token_raw,
    hash_refresh_token,
    verify_refresh_token_hash,
    PBKDF2_ITERATIONS,
)


def test_token_generation():
    """Prueba que la generación de tokens produce resultados únicos y del tamaño correcto."""
    token1 = generate_refresh_token_raw()
    token2 = generate_refresh_token_raw()

    # Verificar que los tokens son diferentes
    assert token1 != token2

    # Verificar el tamaño del token (64 caracteres hexadecimales = 32 bytes)
    assert len(token1) == 64
    assert len(token2) == 64


def test_token_hashing():
    """Prueba que el hashing de tokens produce hashes diferentes para tokens diferentes."""
    token1 = generate_refresh_token_raw()
    token2 = generate_refresh_token_raw()

    hash1 = hash_refresh_token(token1)
    hash2 = hash_refresh_token(token2)

    # Verificar que los hashes son diferentes
    assert hash1 != hash2

    # Verificar que los hashes están en formato base64
    try:
        base64.b64decode(hash1)
        base64.b64decode(hash2)
    except Exception:
        pytest.fail("Los hashes no están en formato base64 válido")


def test_token_verification():
    """Prueba que la verificación de tokens funciona correctamente."""
    token = generate_refresh_token_raw()
    token_hash = hash_refresh_token(token)

    # Verificar que el token original se verifica correctamente
    assert verify_refresh_token_hash(token, token_hash) is True

    # Verificar que un token diferente no se verifica
    assert verify_refresh_token_hash(generate_refresh_token_raw(), token_hash) is False

    # Verificar que un token modificado no se verifica
    modified_token = token[:-1] + ("1" if token[-1] != "1" else "2")
    assert verify_refresh_token_hash(modified_token, token_hash) is False


def test_hash_structure():
    """Prueba que la estructura del hash contiene salt y clave."""
    token = generate_refresh_token_raw()
    token_hash = hash_refresh_token(token)

    # Decodificar el hash
    decoded = base64.b64decode(token_hash.encode("utf-8"))

    # Verificar que el hash decodificado tiene el tamaño correcto
    # 16 bytes de salt + 32 bytes de hash SHA-256
    assert len(decoded) == 16 + 32

    # Extraer salt y verificar que funciona para recrear el hash
    salt = decoded[:16]
    stored_key = decoded[16:]

    # Recrear el hash manualmente
    key = hashlib.pbkdf2_hmac("sha256", token.encode("utf-8"), salt, PBKDF2_ITERATIONS)

    # Verificar que el hash recreado coincide con el almacenado
    assert key == stored_key


def test_pbkdf2_iterations():
    """Prueba que el número de iteraciones de PBKDF2 es suficientemente alto."""
    # Según las recomendaciones de seguridad actuales, PBKDF2 debería usar
    # al menos 10,000 iteraciones, idealmente 100,000+
    assert (
        PBKDF2_ITERATIONS >= 10000
    ), "El número de iteraciones de PBKDF2 es demasiado bajo"
