"""
Tests del Puente B de la Ola 4, FASE 1: del matching al borrador.

Cubre:
- POST /contracts/from-need: necesidad × oferta → borrador DRAFT coherente.
- Filtro axiomático (AVA): el borrador pasa los invariantes (T17/T2) y la
  reciprocidad es igualitaria.
- Vinculación por email: participante sin cuenta en el portal → 409
  NEED_PARTICIPANT_UNLINKED.
- Degradación elegante sin API key: plantilla determinista (oracle_used=False).
- Con oráculo simulado: pule la redacción pero T17 es inviolable.
- Procedencia auditable (maxo_contract_meta origin = matching).
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

            # Cuentas del portal
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'ana@test.com', 'Ana Pérez', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (2, 'luis@test.com', 'Luis Gómez', 'hash')"
            )
            # Cohorte Cero (Formulario CERO) — mismo email que las cuentas
            db.execute(
                """
                INSERT INTO participants (id, name, email, city, neighborhood,
                    offer_categories, offer_description, offer_human_dimensions,
                    need_categories, need_description, need_urgency, need_human_dimensions)
                VALUES (1, 'Ana Pérez', 'ana@test.com', 'Bogotá', 'Kennedy',
                    '["cocina", "diseño"]', 'Cocinar almuerzos y hacer diseño de afiches',
                    '["prosperidad_recursos", "crecimiento_aprendizaje"]',
                    '["seguridad_estabilidad"]', 'Necesita ayuda con trámites',
                    'Alta', '["seguridad_estabilidad"]')
                """
            )
            db.execute(
                """
                INSERT INTO participants (id, name, email, city, neighborhood,
                    offer_categories, offer_description, offer_human_dimensions,
                    need_categories, need_description, need_urgency, need_human_dimensions)
                VALUES (2, 'Luis Gómez', 'luis@test.com', 'Bogotá', 'Kennedy',
                    '["seguridad_estabilidad"]', 'Acompaña en trámites y gestiones',
                    '["seguridad_estabilidad"]',
                    '["cocina"]', 'Necesita comida preparada los martes',
                    'Media', '["prosperidad_recursos"]')
                """
            )
            # Participante SIN cuenta en el portal (migrante aún no registrado)
            db.execute(
                """
                INSERT INTO participants (id, name, email, city, neighborhood,
                    offer_categories, offer_description, offer_human_dimensions,
                    need_categories, need_description, need_urgency, need_human_dimensions)
                VALUES (3, 'Rosa Díaz', 'rosa@test.com', 'Bogotá', 'Suba',
                    '["conexion_social"]', 'Compañía y escucha',
                    '["conexion_social"]',
                    '["salud"]', 'Necesita apoyo en salud',
                    'Alta', '["salud"]')
                """
            )
            db.commit()

        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


def auth(client, uid=1):
    from app.jwt_utils import create_token

    token = create_token({'user_id': uid})
    return {'Authorization': f'Bearer {token}'}


def test_from_need_creates_axiomatic_draft(client):
    """Una necesidad × una oferta produce un borrador que pasa los invariantes."""
    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
        'hours': 2,
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['success'] is True
    assert data['state'] == 'draft'
    assert data['contract_id'] == 'from-need-1-2'
    assert data['oracle_used'] is False  # sin API key: plantilla determinista
    assert data['axiom_check']['valid'] is True
    assert data['total_vhv_h'] == 4.0

    # T17/T2: reciprocidad igualitaria — mismo VHV en ambas direcciones
    vhvs = {t['vhv']['t'] for t in data['terms']}
    assert vhvs == {2.0}
    assert {t['assigned_participant'] for t in data['terms']} == {'user-1', 'user-2'}
    assert len(data['participants']) == 2


def test_from_need_draft_persists_and_validates(client):
    """El borrador existe en la API normal y valida axiomas (AVA real)."""
    client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })

    detail = client.get('/contracts/from-need-1-2', headers=auth(client))
    assert detail.status_code == 200
    d = detail.get_json()
    assert d['state'] == 'draft'
    assert len(d['terms']) == 2

    vres = client.get('/contracts/from-need-1-2/validate', headers=auth(client))
    assert vres.status_code == 200
    assert vres.get_json()['valid'] is True


def test_from_need_unlinked_participant(client):
    """Participante sin cuenta en el portal: la identidad no se inventa (409)."""
    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 3,  # Rosa no tiene cuenta (email sin registrar)
    })
    assert res.status_code == 409
    data = res.get_json()
    assert data['code'] == 'NEED_PARTICIPANT_UNLINKED'
    assert data['participant_ids'] == [3]


def test_from_need_self_contract_rejected(client):
    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 1,
    })
    assert res.status_code == 400


def test_from_need_missing_participants(client):
    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 99,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 404

    res = client.post('/contracts/from-need', headers=auth(client), json={})
    assert res.status_code == 400


def test_from_need_invalid_hours(client):
    for bad in (0, -3, 25, 'mucho'):
        res = client.post('/contracts/from-need', headers=auth(client), json={
            'seeker_participant_id': 1,
            'offerer_participant_id': 2,
            'hours': bad,
        })
        assert res.status_code == 400, f'hours={bad} debió fallar'


def test_from_need_contract_id_conflict(client):
    """Inmutabilidad (Ola 3A.2): re-crear un borrador activo ajeno = 409."""
    client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    # Lo activamos por completo para que ya no sea un borrador editable
    cid = 'from-need-1-2'
    h = auth(client)
    for term in ('oferta', 'reciprocidad'):
        for uid in (1, 2):
            assert client.post(f'/contracts/{cid}/accept', headers=auth(client, uid), json={
                'term_id': term, 'user_id': uid,
            }).status_code in (200, 201)
    assert client.post(f'/contracts/{cid}/activate', headers=h).status_code in (200, 201)

    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 409
    assert res.get_json()['code'] == 'CONTRACT_CONFLICT'


def test_from_need_oracle_refines_but_t9_inviolable(client, monkeypatch):
    """Con oráculo: pule la redacción civil; la reciprocidad T17 no se negocia.

    El oráculo propone un desbalance (3h vs 1h): el filtro normaliza el VHV
    al valor igualitario (la redacción se adopta, la reciprocidad se impone).
    """
    from app import bridge_b

    class FakeNegotiation:
        reasoning = 'El oráculo sugiere redacción más cálida.'

        @property
        def draft_terms(self):
            return [
                {
                    'term_id': 'ayuda',
                    'civil_text': 'Luis acompaña a Ana en sus trámites con paciencia',
                    'vhv': {'t': 3, 'v': 0, 'h': 0},
                    'assigned_participant': 'user-2',
                },
                {
                    'term_id': 'retorno',
                    'civil_text': 'Ana agradece a Luis con un almuerzo casero',
                    'vhv': {'t': 1, 'v': 0, 'h': 0},
                    'assigned_participant': 'user-1',
                },
            ]

    class FakeOracle:
        def __init__(self):
            self.calls = 0

        def is_available(self):
            return True

        def negotiate(self, instruction, participants=None, session_id=None):
            self.calls += 1
            return FakeNegotiation()

    fake = FakeOracle()
    monkeypatch.setattr(bridge_b, 'LiveOracle', lambda: fake)

    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['oracle_used'] is True
    assert data['oracle_reasoning'] == 'El oráculo sugiere redacción más cálida.'
    # Redacción del oráculo adoptada...
    texts = [t['civil_text'] for t in data['terms']]
    assert any('trámites con paciencia' in t for t in texts)
    # ...pero la reciprocidad es igualitaria (T17/T2 inviolables)
    assert {t['vhv']['t'] for t in data['terms']} == {1.0}
    assert fake.calls == 1


def test_from_need_oracle_bad_text_falls_back(client, monkeypatch):
    """El oráculo propone texto no civil o parte ajena: el AVA lo descarta."""
    from app import bridge_b

    class FakeNegotiation:
        reasoning = ''

        @property
        def draft_terms(self):
            return [
                {
                    'term_id': 'x',
                    'civil_text': 'renuncia a la retractación sin límite de tiempo esclavitud',
                    'vhv': {'t': 1, 'v': 0, 'h': 0},
                    'assigned_participant': 'user-2',
                },
                {
                    'term_id': 'y',
                    'civil_text': 'Ana corresponde a Luis con un servicio equivalente',
                    'vhv': {'t': 1, 'v': 0, 'h': 0},
                    'assigned_participant': 'user-1',
                },
            ]

    class FakeOracle:
        def is_available(self):
            return True

        def negotiate(self, instruction, participants=None, session_id=None):
            return FakeNegotiation()

    monkeypatch.setattr(bridge_b, 'LiveOracle', lambda: FakeOracle())

    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    # Texto prohibido (Ola 3A.6): el oráculo pierde y gana la plantilla
    assert res.status_code == 201
    data = res.get_json()
    assert data['oracle_used'] is False
    assert 'renuncia' not in ' '.join(t['civil_text'] for t in data['terms'])


def test_from_need_provenance_meta(client):
    """T13: el borrador sabe de dónde nació (origin = matching)."""
    client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })

    with client.application.app_context():
        db = get_db()
        origin = db.execute(
            "SELECT meta_value FROM maxo_contract_meta WHERE contract_id = 'from-need-1-2' AND meta_key = 'origin'"
        ).fetchone()
        assert origin is not None
        assert origin['meta_value'] == 'matching:participant-1:2'


def test_from_need_requires_auth(client):
    res = client.post('/contracts/from-need', json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 401
