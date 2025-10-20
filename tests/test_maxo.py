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


def seed_user(db_path, email, name='Test User'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, 'pw'))
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

    # transfer 5 from A to B (should fail, but our system allows negative balances)
    payload = {'from_user_id': a, 'to_user_id': b, 'amount': 5.0, 'reason': 'test transfer'}
    resp = client.post('/maxo/transfer', json=payload)
    assert resp.status_code == 200

    # check ledger sums
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?', (a,))
    row = cur.fetchone()
    assert row[0] == -5.0
    cur.execute('SELECT SUM(change_amount) FROM maxo_ledger WHERE user_id = ?', (b,))
    row = cur.fetchone()
    assert row[0] == 5.0
    conn.close()
