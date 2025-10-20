import os
import tempfile
import pytest
import sqlite3
from werkzeug.security import generate_password_hash
from app import create_app
from app.utils import init_db
from app.limiter import init_limiter

@pytest.fixture
def client():
    """Configura un cliente de prueba con una base de datos temporal y límites estrictos"""
    db_fd, db_path = tempfile.mkstemp(prefix='test_comun_', suffix='.db')
    os.close(db_fd)
    
    # Configurar SECRET_KEY para pruebas
    os.environ['SECRET_KEY'] = 'clave_secreta_para_pruebas'
    
    app = create_app(db_path)
    
    # Configurar límites estrictos para pruebas
    app.config['TESTING'] = True
    app.config['RATELIMIT_ENABLED'] = True
    app.config['RATELIMIT_STORAGE_URL'] = 'memory://'
    app.config['RATELIMIT_STRATEGY'] = 'fixed-window'
    app.config['RATELIMIT_DEFAULT'] = "2 per minute"
    app.config['RATELIMIT_AUTH_LIMIT'] = "3 per minute"
    
    with app.app_context():
        init_db(app)
    
    with app.test_client() as client:
        yield client
    
    # Limpiar después de las pruebas
    try:
        os.unlink(db_path)
    except OSError:
        pass


def seed_user(db_path, email, name='Tester'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', 
                (email, name, generate_password_hash('pw')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def test_login_rate_limit(client):
    """Prueba que el rate limiting funciona en la ruta de login."""
    db_path = client.application.config['DATABASE']
    seed_user(db_path, 'rate_test@example.com', 'Rate Test')
    
    # Las primeras 3 solicitudes deberían tener éxito (según la configuración de prueba)
    for i in range(3):
        resp = client.post('/auth/login', json={'email': 'rate_test@example.com', 'password': 'pw'})
        assert resp.status_code == 200, f"Solicitud {i+1} debería tener éxito"
    
    # La cuarta solicitud debería ser limitada
    resp = client.post('/auth/login', json={'email': 'rate_test@example.com', 'password': 'pw'})
    assert resp.status_code == 429, "La solicitud debería ser limitada por rate limiting"
    assert b"Too Many Requests" in resp.data


def test_register_rate_limit(client):
    """Prueba que el rate limiting funciona en la ruta de registro."""
    # Las primeras 3 solicitudes deberían tener éxito
    for i in range(3):
        email = f'new_user_{i}@example.com'
        resp = client.post('/auth/register', json={
            'email': email,
            'password': 'Password123!',
            'name': 'New User',
            'alias': f'user_{i}'
        })
        assert resp.status_code == 201, f"Solicitud {i+1} debería tener éxito"
    
    # La cuarta solicitud debería ser limitada
    resp = client.post('/auth/register', json={
        'email': 'another_user@example.com',
        'password': 'Password123!',
        'name': 'Another User',
        'alias': 'another_user'
    })
    assert resp.status_code == 429, "La solicitud debería ser limitada por rate limiting"
    assert b"Too Many Requests" in resp.data


def test_refresh_rate_limit(client):
    """Prueba que el rate limiting funciona en la ruta de refresh."""
    db_path = client.application.config['DATABASE']
    seed_user(db_path, 'refresh_test@example.com', 'Refresh Test')
    
    # Obtener token
    login_resp = client.post('/auth/login', json={'email': 'refresh_test@example.com', 'password': 'pw'})
    token = login_resp.get_json().get('token')
    
    # Las primeras 3 solicitudes deberían tener éxito
    for i in range(3):
        resp = client.post('/auth/refresh', headers={'Authorization': f'Bearer {token}'})
        assert resp.status_code == 200, f"Solicitud {i+1} debería tener éxito"
        # Actualizar token para la siguiente solicitud
        token = resp.get_json().get('token')
    
    # La cuarta solicitud debería ser limitada
    resp = client.post('/auth/refresh', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 429, "La solicitud debería ser limitada por rate limiting"
    assert b"Too Many Requests" in resp.data