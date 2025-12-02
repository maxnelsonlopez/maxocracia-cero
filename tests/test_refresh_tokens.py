def test_login_returns_refresh_token(auth_client, client):
    """Prueba que el login devuelve un token de acceso y un token de refresco."""
    # Usar el cliente no autenticado para el login
    test_password = "ValidPass123!"
    login_response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": test_password}
    )

    # Verificar que el login fue exitoso
    assert login_response.status_code == 200, f"El login falló: {login_response.data}"

    # Verificar que se devuelven los tokens
    data = login_response.get_json()
    assert "access_token" in data, "No se recibió token de acceso"
    assert "refresh_token" in data, "No se recibió token de refresco"
    assert len(data["access_token"]) > 0, "El token de acceso está vacío"
    assert len(data["refresh_token"]) > 0, "El token de refresco está vacío"
    assert "expires_in" in data, "No se recibió el tiempo de expiración"


def test_refresh_rotates_and_rejects_old(client):
    """Prueba que el token de refresco se rota correctamente."""
    # 1. Iniciar sesión para obtener el primer token de refresco
    login_response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "ValidPass123!"}
    )
    assert login_response.status_code == 200, "El login inicial falló"

    # Obtener el token de acceso y el token de refresco
    login_data = login_response.get_json()
    access_token = login_data.get("access_token")
    refresh_token = login_data.get("refresh_token")

    assert access_token, "No se recibió token de acceso"
    assert refresh_token, "No se recibió token de refresco"

    # 2. Usar el token de refresco para obtener un nuevo token de acceso
    refresh_response = client.post(
        "/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200, "El refresco del token falló"

    # Verificar que se devuelve un nuevo token de acceso y un nuevo token de refresco
    refresh_data = refresh_response.get_json()
    new_access_token = refresh_data.get("access_token")
    new_refresh_token = refresh_data.get("refresh_token")

    assert new_access_token, "No se recibió el nuevo token de acceso"
    assert new_refresh_token, "No se recibió el nuevo token de refresco"
    assert new_refresh_token != refresh_token, "El token de refresco no fue rotado"
    assert (
        new_access_token != access_token
    ), "El token de acceso debería ser diferente después del refresco"
    assert (
        new_refresh_token != refresh_token
    ), "El token de refresco debería ser diferente después del refresco"

    # 3. Verificar que el token de refresco anterior ya no funciona
    old_refresh_response = client.post(
        "/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert (
        old_refresh_response.status_code == 401
    ), "El token de refresco anterior debería ser inválido"


def test_expired_refresh_token_rejected(client):
    """Prueba que un token de refresco expirado sea rechazado."""
    import uuid
    from datetime import datetime, timedelta, timezone

    from app.refresh_utils import hash_refresh_token
    from app.utils import get_db

    # 1. Iniciar sesión para obtener un token de refresco
    login_response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "ValidPass123!"}
    )
    assert login_response.status_code == 200, "El login inicial falló"

    # 2. Obtener el ID del usuario
    with client.application.app_context():
        db = get_db()
        user = db.execute(
            "SELECT id FROM users WHERE email = ?", ("test@example.com",)
        ).fetchone()
        user_id = user["id"]

        # 3. Crear manualmente un token de refresco expirado
        jti = str(uuid.uuid4())
        token = f"{jti}.test-expired-token"
        token_hash = hash_refresh_token(token.split(".")[1])

        # Establecer fechas de expiración en el pasado
        issued_at = datetime.now(timezone.utc) - timedelta(days=2)
        expires_at = datetime.now(timezone.utc) - timedelta(days=1)

        # Insertar el token expirado en la base de datos
        db.execute(
            """
            INSERT INTO refresh_tokens (user_id, jti, token_hash, issued_at, expires_at, revoked)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                user_id,
                jti,
                token_hash,
                issued_at.isoformat(),
                expires_at.isoformat(),
                0,
            ),
        )
        db.commit()

    # 4. Intentar usar el token expirado
    response = client.post("/auth/refresh", json={"refresh_token": token})

    # 5. Verificar que se rechaza el token expirado
    assert response.status_code in [
        401,
        403,
    ], f"Se esperaba que el token expirado fuera rechazado, pero se recibió {response.status_code}"

    error_data = response.get_json()
    assert "error" in error_data, "Se esperaba un mensaje de error"

    # Verificar que el mensaje de error sea el esperado
    error_data = response.get_json()
    assert "error" in error_data, "La respuesta de error no contiene el campo 'error'"
    # Aceptamos tanto 'expired' como 'invalid or revoked' como mensajes de error válidos
    # ya que la aplicación actualmente no distingue entre diferentes tipos de errores
    assert any(
        msg in error_data["error"].lower() for msg in ["expired", "invalid", "revoked"]
    ), f"El mensaje de error no es el esperado: {error_data['error']}"
