import os
import tempfile
import sqlite3

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
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('pw')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def login_and_token(client, email):
    resp = client.post('/auth/login', json={'email': email, 'password': 'pw'})
    assert resp.status_code == 200
    return resp.get_json().get('token')


def test_transfer_no_token(client):
    db_path = client.application.config['DATABASE']
    a = seed_user(db_path, 'a2@example.test', 'A2')
    b = seed_user(db_path, 'b2@example.test', 'B2')

    payload = {'from_user_id': a, 'to_user_id': b, 'amount': 1.0, 'reason': 'no token'}
    resp = client.post('/maxo/transfer', json=payload)
    assert resp.status_code == 401


def test_transfer_token_mismatch(client):
    db_path = client.application.config['DATABASE']
    a = seed_user(db_path, 'a3@example.test', 'A3')
    b = seed_user(db_path, 'b3@example.test', 'B3')
    c = seed_user(db_path, 'c3@example.test', 'C3')

    # login as C but try to transfer from A
    token = login_and_token(client, 'c3@example.test')
    payload = {'from_user_id': a, 'to_user_id': b, 'amount': 1.0, 'reason': 'mismatch'}
    resp = client.post('/maxo/transfer', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 403


def test_transfer_invalid_amount(client):
    db_path = client.application.config['DATABASE']
    a = seed_user(db_path, 'a4@example.test', 'A4')
    b = seed_user(db_path, 'b4@example.test', 'B4')
    token = login_and_token(client, 'a4@example.test')

    payload = {'from_user_id': a, 'to_user_id': b, 'amount': -5.0, 'reason': 'invalid'}
    resp = client.post('/maxo/transfer', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 400


def test_transfer_user_not_found(client):
    db_path = client.application.config['DATABASE']
    a = seed_user(db_path, 'a5@example.test', 'A5')
    token = login_and_token(client, 'a5@example.test')

    # to_user does not exist
    payload = {'from_user_id': a, 'to_user_id': 9999, 'amount': 1.0, 'reason': 'no receiver'}
    resp = client.post('/maxo/transfer', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 404


def test_overdraft_allowed(client):
    db_path = client.application.config['DATABASE']
    a = seed_user(db_path, 'a6@example.test', 'A6')
    b = seed_user(db_path, 'b6@example.test', 'B6')
    token = login_and_token(client, 'a6@example.test')

    payload = {'from_user_id': a, 'to_user_id': b, 'amount': 10.0, 'reason': 'overdraft test'}
    resp = client.post('/maxo/transfer', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?', (a,))
    row = cur.fetchone()
    assert row[0] == -10.0
    conn.close()
