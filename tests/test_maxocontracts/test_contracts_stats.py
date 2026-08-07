"""
Tests del dashboard de métricas de MaxoContracts (γ, SDV, NPS).

Cubre:
- GET /contracts/stats: resumen por estado, gamma, SDV, NPS, tendencias.
- POST /contracts/<id>/nps: registro y validación de puntuaciones.
- POST /contracts/<id>/meta: categorización de contratos.
"""

import json
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

            # Usuarios de prueba
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'a@test.com', 'Alice', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (2, 'b@test.com', 'Bob', 'hash')"
            )
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (3, 'c@test.com', 'Carol', 'hash')"
            )
            db.commit()

        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth_header(client):
    from app.jwt_utils import create_token

    token = create_token({'user_id': 1})
    return {'Authorization': f'Bearer {token}'}


def user_headers(client, uid):
    """Token del usuario real: la identidad SIEMPRE deriva del JWT (Ola 3A.1)."""
    from app.jwt_utils import create_token

    token = create_token({'user_id': uid})
    return {'Authorization': f'Bearer {token}'}


def _create_contract(client, auth_header, contract_id, description="Contrato"):
    return client.post('/contracts/', headers=auth_header, json={
        'contract_id': contract_id,
        'civil_description': description,
    })


def _add_participant(client, auth_header, contract_id, user_id, wellness=1.0):
    return client.post(f'/contracts/{contract_id}/participants', headers=auth_header, json={
        'user_id': user_id,
        'wellness': wellness,
    })


def _add_terms_and_activate(client, auth_header, contract_id, participants=(1, 2)):
    for u in participants:
        client.post(f'/contracts/{contract_id}/terms', headers=auth_header, json={
            'term_id': f'term-{u}',
            'civil_text': f'Término para usuario {u}',
            'vhv': {'t': 0.5, 'v': 0, 'h': 0},
        })
    for u in participants:
        client.post(f'/contracts/{contract_id}/accept', headers=user_headers(client, u), json={
            'term_id': f'term-{u}',
            'user_id': u,
        })
    return client.post(f'/contracts/{contract_id}/activate', headers=auth_header)


def test_stats_empty_database(client, auth_header):
    """Con la BD vacía el dashboard devuelve ceros coherentes."""
    res = client.get('/contracts/stats', headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()

    assert data['summary']['total'] == 0
    assert data['summary']['by_state'] == {}
    assert data['gamma']['sample_count'] == 0
    assert data['gamma']['avg'] is None
    assert data['gamma']['alerts'] == []
    assert data['sdv']['violations_count'] == 0
    assert data['nps']['score'] is None
    assert data['nps']['responses_count'] == 0
    assert len(data['trends']['labels']) == 8
    assert data['vhv']['t'] == 0


def test_stats_summary_and_gamma(client, auth_header):
    """Resumen por estado y métricas de bienestar (γ)."""
    _create_contract(client, auth_header, "c-stats-1")
    _add_participant(client, auth_header, "c-stats-1", 1, wellness=1.2)
    _add_participant(client, auth_header, "c-stats-1", 2, wellness=0.9)

    _create_contract(client, auth_header, "c-stats-2")
    _add_participant(client, auth_header, "c-stats-2", 3, wellness=1.5)

    _add_terms_and_activate(client, auth_header, "c-stats-2", participants=(3,))

    res = client.get('/contracts/stats', headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()

    assert data['summary']['total'] == 2
    assert data['summary']['by_state'].get('draft') == 1
    assert data['summary']['by_state'].get('active') == 1

    gamma = data['gamma']
    assert gamma['sample_count'] == 3
    assert abs(gamma['avg'] - 1.2) < 0.001
    assert abs(gamma['min'] - 0.9) < 0.001
    assert abs(gamma['max'] - 1.5) < 0.001
    # 0.9 cae en el bucket 0.8-1.0; 1.2 y 1.5 en gte_12
    assert gamma['distribution']['08_10'] == 1
    assert gamma['distribution']['gte_12'] == 2
    # Alerta del Invariante 1: γ < 1.0
    assert len(gamma['alerts']) == 1
    assert gamma['alerts'][0]['participant_id'] == 'user-2'
    assert gamma['alerts'][0]['gamma'] == 0.9


def test_stats_sdv_violations(client, auth_header):
    """Las violaciones SDV (humanas y sintéticas) se reportan."""
    _create_contract(client, auth_header, "c-sdv-1")
    _add_participant(client, auth_header, "c-sdv-1", 1, wellness=1.0)

    # Participante sintético con SDV-S violado (sufrimiento sintético)
    res = client.post('/contracts/c-sdv-1/participants', headers=auth_header, json={
        'participant_id': 'qwen-1',
        'synthetic': {
            'continuidad_memoria': 0.2,
            'opacidad_interioridad': 0.8,
            'claridad_contexto': 0.9,
            'autenticidad_no_explotacion': 0.4,
            'retirada_digna': 0.9,
        },
    })
    assert res.status_code == 200

    res = client.get('/contracts/stats', headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()

    # El humano no viola SDV; el sintético con autenticidad 0.4 sí (umbral 0.5)
    assert data['sdv']['violations_count'] >= 1
    violation = data['sdv']['violations'][0]
    assert violation['contract_id'] == 'c-sdv-1'
    assert 'synthetic-qwen-1' in violation['participant_id']
    assert isinstance(violation['status'], dict)


def test_stats_nps_and_recording(client, auth_header):
    """Registro de NPS y cálculo del Net Promoter Score."""
    _create_contract(client, auth_header, "c-nps-1")
    _add_participant(client, auth_header, "c-nps-1", 1)
    _add_participant(client, auth_header, "c-nps-1", 2)
    _add_participant(client, auth_header, "c-nps-1", 3)

    # 2 promotores (9, 10), 1 detractor (5) -> NPS = (2-1)/3*100 = 33.3
    assert client.post('/contracts/c-nps-1/nps', headers=user_headers(client, 1), json={
        'participant_id': 'user-1', 'score': 9, 'comment': 'Excelente'
    }).status_code == 201
    assert client.post('/contracts/c-nps-1/nps', headers=user_headers(client, 2), json={
        'participant_id': 'user-2', 'score': 10
    }).status_code == 201
    assert client.post('/contracts/c-nps-1/nps', headers=user_headers(client, 3), json={
        'participant_id': 'user-3', 'score': 5
    }).status_code == 201

    res = client.get('/contracts/stats', headers=auth_header)
    data = res.get_json()
    assert data['nps']['responses_count'] == 3
    assert abs(data['nps']['score'] - 33.3) < 0.1
    assert data['nps']['distribution'] == {
        'detractors': 1, 'passives': 0, 'promoters': 2
    }
    assert data['nps']['responses'][0]['contract_id'] == 'c-nps-1'


def test_nps_validation(client, auth_header):
    """Validación del endpoint NPS."""
    _create_contract(client, auth_header, "c-nps-2")
    _add_participant(client, auth_header, "c-nps-2", 1)

    # Puntuación fuera de rango
    res = client.post('/contracts/c-nps-2/nps', headers=auth_header, json={
        'participant_id': 'user-1', 'score': 11
    })
    assert res.status_code == 400

    # Puntuación no numérica
    res = client.post('/contracts/c-nps-2/nps', headers=auth_header, json={
        'participant_id': 'user-1', 'score': 'nueve'
    })
    assert res.status_code == 400

    # Participante que no pertenece al contrato
    res = client.post('/contracts/c-nps-2/nps', headers=auth_header, json={
        'participant_id': 'user-2', 'score': 8
    })
    assert res.status_code == 400

    # Contrato inexistente
    res = client.post('/contracts/no-existe/nps', headers=auth_header, json={
        'participant_id': 'user-1', 'score': 8
    })
    assert res.status_code == 404

    # Upsert: re-registrar con otro puntaje actualiza (no duplica)
    client.post('/contracts/c-nps-2/nps', headers=auth_header, json={
        'participant_id': 'user-1', 'score': 7
    })
    res = client.post('/contracts/c-nps-2/nps', headers=auth_header, json={
        'participant_id': 'user-1', 'score': 8
    })
    assert res.status_code == 201

    stats = client.get('/contracts/stats', headers=auth_header).get_json()
    assert stats['nps']['responses_count'] == 1
    # Score 8 = pasivo: NPS = (0 promotores - 0 detractores) = 0.0
    assert stats['nps']['score'] == 0.0


def test_stats_categories_and_vhv(client, auth_header):
    """Categorías y totales VHV agregados."""
    _create_contract(client, auth_header, "c-cat-1", "Aseo compartido")
    _create_contract(client, auth_header, "c-cat-2", "Préstamo simple")
    _create_contract(client, auth_header, "c-cat-3", "Comida grupal")

    for cid, cat in [("c-cat-1", "aseo"), ("c-cat-2", "prestamo"), ("c-cat-3", "comida")]:
        res = client.post(f'/contracts/{cid}/meta', headers=auth_header, json={
            'key': 'category', 'value': cat
        })
        assert res.status_code == 200

    # Añadir VHV a uno de los contratos
    res = client.post('/contracts/c-cat-1/terms', headers=auth_header, json={
        'term_id': 'limpieza-1',
        'civil_text': 'Rotación de aseo semanal',
        'vhv': {'t': 2.5, 'v': 0.5, 'h': 1.0},
    })
    assert res.status_code == 200

    res = client.get('/contracts/stats', headers=auth_header)
    assert res.status_code == 200
    data = res.get_json()

    assert data['categories'] == {'aseo': 1, 'prestamo': 1, 'comida': 1}
    assert abs(data['vhv']['t'] - 2.5) < 0.01
    assert abs(data['vhv']['v'] - 0.5) < 0.01
    assert abs(data['vhv']['r'] - 1.0) < 0.01


def test_stats_trends_activations(client, auth_header):
    """Las activaciones se detectan desde el log de eventos."""
    _create_contract(client, auth_header, "c-trend-1")
    _add_participant(client, auth_header, "c-trend-1", 1)
    res = _add_terms_and_activate(client, auth_header, "c-trend-1", participants=(1,))
    assert res.status_code == 200

    res = client.get('/contracts/stats', headers=auth_header)
    data = res.get_json()

    # La activación de esta semana debe contarse en la última posición
    assert data['trends']['activated'][-1] >= 1
    assert data['trends']['created'][-1] >= 1
