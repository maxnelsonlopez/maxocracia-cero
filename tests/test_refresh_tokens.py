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

    r = client.post('/auth/login', json={'email': 'rt@test.local', 'password': 'secret'}, environ_base={'REMOTE_ADDR': '127.0.0.1'})
    assert r.status_code == 200
    # cookie should be set in Set-Cookie header
    setc = r.headers.get('Set-Cookie', '')
    assert 'mc_refresh=' in setc
    rt = setc.split('mc_refresh=')[1].split(';', 1)[0]
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
    # extract cookie from response header
    setc = r.headers.get('Set-Cookie', '')
    assert 'mc_refresh=' in setc
    old_cookie = setc.split('mc_refresh=')[1].split(';', 1)[0]

    # call refresh with cookie provided explicitly
    r2 = client.post('/auth/refresh', headers={'Cookie': f'mc_refresh={old_cookie}'})
    assert r2.status_code == 200
    # server should set a new cookie in response
    setc2 = r2.headers.get('Set-Cookie', '')
    assert 'mc_refresh=' in setc2
    new_cookie = setc2.split('mc_refresh=')[1].split(';', 1)[0]
    assert new_cookie != old_cookie

    # reuse old cookie value -> rejected (use a fresh client without the new cookie stored)
    with client.application.test_client() as c2:
        r3 = c2.post('/auth/refresh', headers={'Cookie': f'mc_refresh={old_cookie}'})
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
                   ('exp@test.local', 'Exp Test', generate_password_hash('Password1')))
        db.commit()
        user = db.execute('SELECT * FROM users WHERE email=?', ('exp@test.local',)).fetchone()
        jti = 'expired-jti'
        raw = 'expiredrawtoken'
        token_hash = hash_refresh_token(raw)
        past = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        db.execute('INSERT INTO refresh_tokens (user_id, jti, token_hash, issued_at, expires_at, revoked) VALUES (?, ?, ?, ?, ?, 0)',
                   (user['id'], jti, token_hash, past, past))
        db.commit()

    # call refresh sending expired cookie
    r = client.post('/auth/refresh', headers={'Cookie': f'mc_refresh={jti}.{raw}'})
    assert r.status_code == 401
