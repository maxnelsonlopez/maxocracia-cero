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
    with client.application.app_context():
        db = get_db()
        db.execute('DELETE FROM users WHERE email=?', ('rt@test.local',))
        db.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                   ('rt@test.local', 'RT Test', generate_password_hash('secret')))
        db.commit()

    r = client.post('/auth/login', json={'email': 'rt@test.local', 'password': 'secret'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'refresh_token' in data
    rt = data['refresh_token']
    assert '.' in rt


def test_refresh_rotates_and_rejects_old(client):
    from werkzeug.security import generate_password_hash
    from app.utils import get_db
    with client.application.app_context():
        db = get_db()
        db.execute('DELETE FROM users WHERE email=?', ('rot@test.local',))
        db.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                   ('rot@test.local', 'Rotate Test', generate_password_hash('s3cret')))
        db.commit()

    r = client.post('/auth/login', json={'email': 'rot@test.local', 'password': 's3cret'})
    assert r.status_code == 200
    data = r.get_json()
    old_rt = data['refresh_token']

    # call refresh with old token -> should return new refresh token
    r2 = client.post('/auth/refresh', json={'refresh_token': old_rt})
    assert r2.status_code == 200
    d2 = r2.get_json()
    new_rt = d2['refresh_token']
    assert new_rt != old_rt

    # reuse old token -> should be rejected
    r3 = client.post('/auth/refresh', json={'refresh_token': old_rt})
    assert r3.status_code == 401


def test_expired_refresh_token_rejected(client):
    # create user and manually insert a refresh token with past expires_at
    from werkzeug.security import generate_password_hash
    from app.utils import get_db
    from app.refresh_utils import hash_refresh_token
    with client.application.app_context():
        db = get_db()
        db.execute('DELETE FROM users WHERE email=?', ('exp@test.local',))
        db.execute('INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
                   ('exp@test.local', 'Exp Test', generate_password_hash('pw')))
        db.commit()
        user = db.execute('SELECT * FROM users WHERE email=?', ('exp@test.local',)).fetchone()
        jti = 'expired-jti'
        raw = 'expiredrawtoken'
        token_hash = hash_refresh_token(raw)
        past = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        db.execute('INSERT INTO refresh_tokens (user_id, jti, token_hash, issued_at, expires_at, revoked) VALUES (?, ?, ?, ?, ?, 0)',
                   (user['id'], jti, token_hash, past, past))
        db.commit()

    r = client.post('/auth/refresh', json={'refresh_token': f'{jti}.{raw}'})
    assert r.status_code == 401
