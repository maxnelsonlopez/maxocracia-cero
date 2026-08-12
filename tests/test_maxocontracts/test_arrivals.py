"""
Tests del Puente de Llegada (Sun Tzu + Ternura).

Cubre:
- Invitación firmada: from-need 409 incluye invite_url; GET /invite/<token>
  valida y enmascara el email; token manipulado → 404 sin información.
- Honeypot: un bot que llena el campo invisible entra a cuarentena con éxito
  aparente y tokens inertes; ningún usuario se crea; el flujo queda observado.
- Escalera de confianza (Cap. 13): el recién llegado (N0) no puede votar
  (403 TRUST_LEVEL_REQUIRED); al activar su primer contrato pasa a N1;
  la promoción manual por la comunidad también funciona.
"""

import os
import tempfile

os.environ['SECRET_KEY'] = 'test-secret'

import pytest

from app import create_app
from app.utils import get_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config['TESTING'] = True

    with app.test_client() as test_client:
        with app.app_context():
            db = get_db()
            with open('app/schema.sql', 'r', encoding='utf-8') as f:
                db.executescript(f.read())

            db.execute(
                "INSERT INTO users (id, email, name, password_hash, is_admin, trust_level) "
                "VALUES (1, 'ana@test.com', 'Ana', 'hash', 1, 1)"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash, is_admin, trust_level) "
                "VALUES (2, 'luis@test.com', 'Luis', 'hash', 0, 0)"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash, is_admin, trust_level) "
                "VALUES (3, 'votante@test.com', 'Votante', 'hash', 0, 1)"
            )
            db.execute(
                "INSERT INTO vhv_parameters (alpha, beta, gamma, delta, notes) VALUES (100, 2000, 1, 100, 'x')"
            )
            for pid, name, email, offer, need in (
                (1, 'Ana Pérez', 'ana@test.com',
                 'Cocinar almuerzos y hacer diseño de afiches',
                 'Necesita ayuda con trámites'),
                (2, 'Luis Gómez', 'luis@test.com',
                 'Acompaña en trámites y gestiones',
                 'Necesita comida preparada los martes'),
            ):
                db.execute(
                    """
                    INSERT INTO participants (id, name, email, city, neighborhood,
                        offer_categories, offer_description, offer_human_dimensions,
                        need_categories, need_description, need_urgency, need_human_dimensions)
                    VALUES (?, ?, ?, 'Bogotá', 'Kennedy', ?, ?, ?, ?, ?, 'Media', ?)
                    """,
                    (pid, name, email,
                     '["cocina"]', offer, '["prosperidad_recursos"]',
                     '["seguridad_estabilidad"]', need, '["seguridad_estabilidad"]'),
                )
            db.commit()

        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


def auth(client, uid=1):
    from app.jwt_utils import create_token

    token = create_token({'user_id': uid, 'is_admin': 1 if uid == 1 else 0})
    return {'Authorization': f'Bearer {token}'}


def test_unlinked_participant_gets_invite(client):
    """El muro se vuelve invitación: 409 con invite_url firmado."""
    res = client.post('/contracts/from-need', headers=auth(client, 2), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    # El participante 1 (Ana) está vinculado al user 1; el 2 (Luis) al user 2.
    # Ambos están vinculados: para forzar el 409, probamos con un tercero sin cuenta.
    assert res.status_code == 201

    db = get_db()
    db.execute(
        """
        INSERT INTO participants (id, name, email, city, neighborhood,
            offer_categories, offer_description, offer_human_dimensions,
            need_categories, need_description, need_urgency, need_human_dimensions)
        VALUES (9, 'Rosa Díaz', 'rosa@test.com', 'Bogotá', 'Suba',
            '["conexion_social"]', 'Compañía y escucha', '["conexion_social"]',
            '["salud"]', 'Necesita apoyo en salud', 'Alta', '["salud"]')
        """
    )
    db.commit()

    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 9,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 409
    data = res.get_json()
    assert data['code'] == 'NEED_PARTICIPANT_UNLINKED'
    assert 'invite_urls' in data
    assert data['invite_urls']['9'].startswith('/invite/')


def test_invite_token_valid_and_masked(client):
    """La invitación valida y enmascara el email (Opacidad Sagrada)."""
    from app.arrivals import sign_invite

    token = sign_invite('rosa@test.com')
    res = client.get(f'/invite/{token}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['valid'] is True
    assert data['email_masked'] == 'r***a@test.com'
    assert 'rosa@test.com' not in data['email_masked']
    assert data['already_registered'] is False
    assert data['register_url'] == '/register?email=rosa@test.com'


def test_invite_tampered_token_404(client):
    """Token manipulado → 404 sin información (no confirmamos existencia)."""
    from app.arrivals import sign_invite

    token = sign_invite('rosa@test.com')
    tampered = token[:-2] + ('ab' if token[-2:] != 'ab' else 'cd')
    res = client.get(f'/invite/{tampered}')
    assert res.status_code == 404
    assert res.get_json()['error'] == 'invitación no válida'

    res = client.get('/invite/garbage')
    assert res.status_code == 404


def test_register_honeypot_quarantines_bot(client):
    """Un bot que llena el honeypot entra a cuarentena con éxito aparente."""
    res = client.post('/auth/register', json={
        'email': 'bot@spam.com',
        'password': 'Password1!',
        'name': 'Bot',
        'website': 'http://spam.example',
    })
    # El bot cree haber entrado (Sun Tzu: no despertar al enemigo)
    assert res.status_code == 201
    assert 'access_token' in res.get_json()

    # Pero ningún usuario se creó y su flujo quedó observado
    with client.application.app_context():
        db = get_db()
        user = db.execute("SELECT id FROM users WHERE email = 'bot@spam.com'").fetchone()
        assert user is None
        row = db.execute(
            "SELECT honeypot_hit, status FROM maxo_arrivals WHERE email = 'bot@spam.com'"
        ).fetchone()
        assert row is not None
        assert row['honeypot_hit'] == 1
        assert row['status'] == 'quarantined'

    # Los tokens son inertes: la identidad no existe
    token = res.get_json()['access_token']
    me = client.get('/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert me.status_code in (401, 404)


def test_register_arrival_logged_with_trust0(client):
    """Llegada legítima: registrada y en N0 (recién llegado, sin voz aún)."""
    res = client.post('/auth/register', json={
        'email': 'nuevo@test.com',
        'password': 'Password1!',
        'name': 'Nuevo',
    })
    assert res.status_code == 201

    with client.application.app_context():
        db = get_db()
        row = db.execute(
            "SELECT trust_level FROM users WHERE email = 'nuevo@test.com'"
        ).fetchone()
        assert row is not None and row['trust_level'] == 0
        arrival = db.execute(
            "SELECT status, honeypot_hit FROM maxo_arrivals WHERE email = 'nuevo@test.com'"
        ).fetchone()
        assert arrival is not None
        assert arrival['status'] == 'arrived'
        assert arrival['honeypot_hit'] == 0


def test_voting_gate_trust_level(client):
    """N0 no gobierna: la voz llega al caminar el primer acuerdo (403)."""
    # Votante integrado puede votar
    res = client.post('/voting/proposals', headers=auth(client, 1), json={
        'title': 'Prueba de la sede',
        'description': 'Organizar la sede',
        'category': 'operational',
        'options': ['Sí', 'No'],
    })
    prop_id = res.get_json()['proposal']['id']

    # Luis (N0) no puede votar
    res = client.post(f'/voting/proposals/{prop_id}/vote', headers=auth(client, 2), json={'option': 'Sí'})
    assert res.status_code == 403
    assert res.get_json()['code'] == 'TRUST_LEVEL_REQUIRED'

    # El integrado sí
    res = client.post(f'/voting/proposals/{prop_id}/vote', headers=auth(client, 3), json={'option': 'Sí'})
    assert res.status_code == 200


def test_first_contract_promotes_to_trust(client):
    """Al activar el primer contrato, los participantes pasan a N1."""
    # Luis (N0) crea el borrador con Ana y camina el ciclo completo
    res = client.post('/contracts/from-need', headers=auth(client, 2), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    cid = res.get_json()['contract_id']

    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 2), json={})
    assert res.get_json()['state'] == 'pending'
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 1), json={})
    data = res.get_json()
    assert data['activated'] is True
    assert set(data['promoted_to_trust']) == {'user-2'}  # Ana ya era N1

    with client.application.app_context():
        db = get_db()
        trust = db.execute("SELECT trust_level FROM users WHERE id = 2").fetchone()
        assert trust['trust_level'] == 1
        promoted = db.execute(
            "SELECT status FROM maxo_arrivals WHERE email = 'luis@test.com' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert promoted['status'] == 'promoted'


def test_community_ascension_manual(client):
    """La comunidad puede ascender manualmente a alguien (admin, T13)."""
    res = client.post('/users/2/trust', headers=auth(client, 1))
    assert res.status_code == 200
    assert res.get_json()['trust_level'] == 1

    with client.application.app_context():
        db = get_db()
        row = db.execute(
            "SELECT status FROM maxo_arrivals WHERE email = 'luis@test.com' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert row['status'] == 'promoted'

    # Idempotente
    res = client.post('/users/2/trust', headers=auth(client, 1))
    assert res.status_code == 200


def test_quarantine_list_admin_only(client):
    """La cuarentena es observada por la comunidad (admin), no por curiosos."""
    client.post('/auth/register', json={
        'email': 'bot2@spam.com', 'password': 'Password1!', 'name': 'Bot', 'website': 'x',
    })
    res = client.get('/invite/quarantine', headers=auth(client, 2))
    assert res.status_code == 403
    res = client.get('/invite/quarantine', headers=auth(client, 1))
    assert res.status_code == 200
    data = res.get_json()
    assert any(e['email'] == 'bot2@spam.com' and e['honeypot_hit'] for e in data)
