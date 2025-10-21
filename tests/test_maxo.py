import os
import tempfile
import sqlite3

import pytest
from app import create_app
from app.utils import init_db


@pytest.fixture
def client():
    # Configurar variables de entorno para pruebas
    os.environ['SECRET_KEY'] = 'test-secret-key-123'
    os.environ['FLASK_ENV'] = 'testing'
    
    # Crear base de datos temporal
    db_fd, db_path = tempfile.mkstemp(prefix='test_comun_', suffix='.db')
    os.close(db_fd)

    # Crear y configurar la aplicación
    app = create_app(db_path)
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key-123',
        'WTF_CSRF_ENABLED': False
    })

    # Inicializar la base de datos
    with app.app_context():
        init_db()

    # Crear un cliente de prueba
    with app.test_client() as client:
        # Pasar la ruta de la base de datos al cliente para usarla en las pruebas
        client.application.config['DATABASE'] = db_path
        yield client

    # Limpieza: eliminar el archivo de la base de datos después de la prueba
    try:
        os.unlink(db_path)
    except OSError:
        pass


from werkzeug.security import generate_password_hash


def seed_user(db_path, email, name='Tester'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)', (email, name, generate_password_hash('Password1')))
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
    resp = client.post('/auth/login', json={'email': 'a@example.test', 'password': 'Password1'})
    assert resp.status_code == 200
    data = resp.get_json()
    token = data.get('access_token')
    assert token is not None, f"No se recibió access_token en la respuesta: {data}"

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
