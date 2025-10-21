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

    # initialize db
    with app.app_context():
        init_db(app)

    with app.test_client() as client:
        yield client

    # cleanup
    try:
        os.remove(db_path)
    except OSError:
        pass


def seed_user(db_path, email, name='Test User'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('Password1')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def test_reputation_flow(client):
    db_path = client.application.config['DATABASE']
    u = seed_user(db_path, 'rep@example.test', 'Rep')

    resp = client.get(f'/reputation/{u}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['score'] == 0.0

    resp = client.post('/reputation/review', json={'user_id': u, 'score': 4.0})
    assert resp.status_code == 201
    resp = client.get(f'/reputation/{u}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['score'] == 4.0


def test_resources_flow(client):
    db_path = client.application.config['DATABASE']
    u = seed_user(db_path, 'res@example.test', 'Res')

    resp = client.post('/resources', json={'user_id': u, 'title': 'Bike', 'description': 'A mountain bike', 'category': 'transport'})
    assert resp.status_code == 201

    resp = client.get('/resources')
    assert resp.status_code == 200
    items = resp.get_json()
    assert len(items) == 1
    rid = items[0]['id']

    # claim resource
    resp = client.post(f'/resources/{rid}/claim', json={'user_id': u})
    assert resp.status_code == 200

    # subsequent claim should fail
    resp = client.post(f'/resources/{rid}/claim', json={'user_id': u})
    assert resp.status_code == 400
