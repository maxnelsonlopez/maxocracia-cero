import time
from datetime import datetime, timedelta, timezone
import pytest

from app import create_app
from app.utils import init_db


@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config['TESTING'] = True
    # use a temp DB file
    db_path = tmp_path / 'test.db'
    app.config['DATABASE'] = str(db_path)
    with app.app_context():
        init_db(app)
        # create a test user
        from app.utils import get_db
        db = get_db()
        db.execute("INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                   ("rt@test.local", "RT Test", "pbkdf2:sha256:150000$xyz$abc"))
        db.commit()
    with app.test_client() as c:
        yield c


def test_login_returns_refresh_token(client):
    # Create user with known password inside app context, then login
    from werkzeug.security import generate_password_hash
    from app.utils import get_db
    
    # Usar una contraseña que cumpla con los requisitos de validación
    test_password = 'Password1!'
    
    with client.application.app_context():
        db = get_db()
        db.execute('DELETE FROM users WHERE email=?', ('rt@test.local',))
        db.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                   ('rt@test.local', 'RT Test', generate_password_hash(test_password)))
        db.commit()

    # Realizar login con credenciales válidas
    r = client.post('/auth/login', 
                   json={'email': 'rt@test.local', 'password': test_password}, 
                   environ_base={'REMOTE_ADDR': '127.0.0.1'})
    
    # Verificar que el login fue exitoso
    assert r.status_code == 200, f"El login falló con: {r.data}"
    
    # Verificar que se devuelve un token de acceso
    data = r.get_json()
    assert 'token' in data, "No se recibió token de acceso"
    assert len(data['token']) > 0, "El token de acceso está vacío"
    
    # Verificar que se devuelve un token de refresco
    assert 'refresh_token' in data, "No se recibió token de refresco"
    assert len(data['refresh_token']) > 0, "El token de refresco está vacío"


def test_refresh_rotates_and_rejects_old(client):
    """Prueba que el token de refresco se rota correctamente."""
    from werkzeug.security import generate_password_hash
    from app.utils import get_db
    
    # Usar una contraseña que cumpla con los requisitos de validación
    test_password = 'Password1!'
    
    with client.application.app_context():
        db = get_db()
        db.execute('DELETE FROM users WHERE email=?', ('rot@test.local',))
        db.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                   ('rot@test.local', 'Rotate Test', generate_password_hash(test_password)))
        db.commit()

    # 1. Iniciar sesión para obtener el primer token de refresco
    login_response = client.post('/auth/login', 
                               json={'email': 'rot@test.local', 'password': test_password})
    assert login_response.status_code == 200, "El login inicial falló"
    
    # Obtener el token de acceso y el token de refresco
    login_data = login_response.get_json()
    access_token = login_data.get('token')
    refresh_token = login_data.get('refresh_token')
    
    assert access_token, "No se recibió token de acceso"
    assert refresh_token, "No se recibió token de refresco"
    
    # 2. Usar el token de refresco para obtener un nuevo token de acceso
    refresh_response = client.post('/auth/refresh', 
                                 headers={'Authorization': f'Bearer {refresh_token}'})
    assert refresh_response.status_code == 200, "El refresco del token falló"
    
    # Verificar que se devuelve un nuevo token de acceso y un nuevo token de refresco
    refresh_data = refresh_response.get_json()
    new_access_token = refresh_data.get('token')
    new_refresh_token = refresh_data.get('refresh_token')
    
    assert new_access_token, "No se recibió el nuevo token de acceso"
    assert new_refresh_token, "No se recibió el nuevo token de refresco"
    assert new_access_token != access_token, "El token de acceso debería ser diferente después del refresco"
    assert new_refresh_token != refresh_token, "El token de refresco debería ser diferente después del refresco"
    
    # 3. Verificar que el token de refresco anterior ya no funciona
    old_refresh_response = client.post('/auth/refresh',
                                     headers={'Authorization': f'Bearer {refresh_token}'})
    assert old_refresh_response.status_code == 401, "El token de refresco anterior debería ser inválido"


def test_expired_refresh_token_rejected(client):
    """Prueba que un token de refresco expirado sea rechazado."""
    from werkzeug.security import generate_password_hash
    from app.utils import get_db
    from app.refresh_utils import hash_refresh_token
    import sqlite3
    from datetime import datetime, timedelta
    
    # Usar una contraseña que cumpla con los requisitos de validación
    test_password = 'Password1!'
    
    with client.application.app_context():
        db = get_db()
        # Crear un usuario de prueba
        db.execute('DELETE FROM users WHERE email=?', ('exp@test.local',))
        db.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                   ('exp@test.local', 'Expired Test', generate_password_hash(test_password)))
        
        # Obtener el ID del usuario recién creado
        user_id = db.execute('SELECT id FROM users WHERE email = ?', ('exp@test.local',)).fetchone()[0]
        
        # Crear un token de refresco expirado manualmente
        expired_token = 'expired-token-123'
        token_hash = hash_refresh_token(expired_token)
        expires_at = (datetime.utcnow() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        created_at = (datetime.utcnow() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Insertar el token expirado en la base de datos
        db.execute('''
            INSERT INTO refresh_tokens (user_id, token_hash, expires_at, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, token_hash, expires_at, created_at))
        
        db.commit()

    # Intentar usar el token expirado
    response = client.post('/auth/refresh', 
                          headers={'Authorization': f'Bearer {expired_token}'})
    
    # Verificar que el token expirado sea rechazado
    assert response.status_code == 401, "Se esperaba un error 401 para un token expirado"
    
    # Verificar que el mensaje de error sea el esperado
    error_data = response.get_json()
    assert 'error' in error_data, "La respuesta de error no contiene el campo 'error'"
    assert 'expired' in error_data['error'].lower(), "El mensaje de error no indica que el token ha expirado"
