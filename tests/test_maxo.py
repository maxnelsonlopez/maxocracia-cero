import os
import tempfile
import sqlite3

import pytest
from app import create_app
from app.utils import init_db


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


from werkzeug.security import generate_password_hash


def seed_user(db_path, email, name='Test User'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('pw')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def test_balance_and_transfer(client):
    db_path = client.application.config['DATABASE']
    a = seed_user(db_path, 'a@example.test', 'A')
    b = seed_user(db_path, 'b@example.test', 'B')

    # initial balances 0
    resp = client.get(f'/maxo/{a}/balance')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['balance'] == 0

    # login as A to get token
    resp = client.post('/auth/login', json={'email': 'a@example.test', 'password': 'pw'})
    assert resp.status_code == 200
    token = resp.get_json().get('token')
    assert token

    # credit A with 10 to allow the transfer
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO maxo_ledger (user_id, change_amount, reason) VALUES (?, ?, ?)', (a, 10.0, 'seed credit'))
    conn.commit()
    conn.close()

    # transfer 5 from A to B
    payload = {'from_user_id': a, 'to_user_id': b, 'amount': 5.0, 'reason': 'test transfer'}
    resp = client.post('/maxo/transfer', json=payload, headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200

    # check ledger sums
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?', (a,))
    row = cur.fetchone()
    assert row[0] == 5.0
    cur.execute('SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?', (b,))
    row = cur.fetchone()
    assert row[0] == 5.0
    conn.close()
