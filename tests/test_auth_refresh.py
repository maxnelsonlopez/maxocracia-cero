import sqlite3
import tempfile
import os
import pytest
from app import create_app
from app.utils import init_db
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(prefix='test_comun_', suffix='.db')
    os.close(db_fd)
    
    # Configurar SECRET_KEY para pruebas
    os.environ['SECRET_KEY'] = 'clave_secreta_para_pruebas'
    
    app = create_app(db_path)
    app.config['TESTING'] = True
    with app.app_context():
        init_db(app)
    with app.test_client() as client:
        yield client
    try:
        os.remove(db_path)
    except OSError:
        pass


def seed_user(db_path, email, name='Tester'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('Password1')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def login_and_token(client, email):
    resp = client.post('/auth/login', json={'email': email, 'password': 'Password1'})
    assert resp.status_code == 200
    return resp.get_json().get('token')


def test_refresh_returns_new_token(client):
    db_path = client.application.config['DATABASE']
    seed_user(db_path, 'r1@example.test', 'R1')
    token = login_and_token(client, 'r1@example.test')
    resp = client.post('/auth/refresh', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    j = resp.get_json()
    assert 'token' in j and isinstance(j['token'], str) and len(j['token']) > 10


def test_refresh_requires_token(client):
    resp = client.post('/auth/refresh')
    assert resp.status_code == 401


def test_refresh_allows_expired_token(client):
    db_path = client.application.config['DATABASE']
    uid = seed_user(db_path, 'r2@example.test', 'R2')
    # create a token that expires immediately using jwt_utils.create_token
    from app.jwt_utils import create_token
    tok = create_token({'user_id': uid, 'email': 'r2@example.test'}, expires_in=1)
    import time
    time.sleep(2)
    resp = client.post('/auth/refresh', headers={'Authorization': f'Bearer {tok}'})
    assert resp.status_code == 200
    j = resp.get_json()
    assert 'token' in j
