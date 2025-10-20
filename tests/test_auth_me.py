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
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('pw')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def login_and_token(client, email):
    resp = client.post('/auth/login', json={'email': email, 'password': 'pw'})
    assert resp.status_code == 200
    return resp.get_json().get('token')


def test_auth_me_returns_profile(client):
    db_path = client.application.config['DATABASE']
    uid = seed_user(db_path, 'me@example.test', 'Me')
    token = login_and_token(client, 'me@example.test')
    resp = client.get('/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    j = resp.get_json()
    assert j['id'] == uid
    assert j['email'] == 'me@example.test'
