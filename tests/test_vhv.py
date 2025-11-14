import os
import tempfile
import sqlite3
import json
import pytest
from app import create_app
from app.utils import init_db


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
    import sqlite3
    from werkzeug.security import generate_password_hash
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('Password1')))
    uid = cur.lastrowid
    conn.commit()
    conn.close()
    return uid


def test_interchange_vhv_fields(client):
    db_path = client.application.config['DATABASE']
    giver_id = seed_user(db_path, 'a@example.test')
    receiver_id = seed_user(db_path, 'b@example.test')

    payload = {
        'interchange_id': 'VHV-TEST-001',
        'giver_id': giver_id,
        'receiver_id': receiver_id,
        'description': 'ethical egg production',
        'uth_hours': 1.5,
        'impact_resolution_score': 3,
        'uvc_score': 0.0,
        'urf_units': 2.2,
        'vhv_time_seconds': 5400,
        'vhv_lives': 0.0,
        'vhv_resources': {
            'energia_kwh': 1.8,
            'agua_l': 0.12,
            'co2_kg': 0.9
        }
    }

    resp = client.post('/interchanges', json=payload)
    assert resp.status_code == 201, resp.data

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT interchange_id, vhv_time_seconds, vhv_lives, vhv_resources_json FROM interchange WHERE interchange_id=?', ('VHV-TEST-001',))
    row = cur.fetchone()
    conn.close()
    assert row is not None
    assert row[1] == pytest.approx(5400)
    assert row[2] == pytest.approx(0.0)
    data = json.loads(row[3])
    assert data['energia_kwh'] == 1.8
    assert data['agua_l'] == 0.12
    assert data['co2_kg'] == 0.9