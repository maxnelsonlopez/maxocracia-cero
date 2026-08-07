"""
Tests de la Ola 3C — Ejecución mínima (los dientes).

Cubre (blindaje_anti_gamificacion_equidad.md §5):
- Bitácora de cumplimiento por término (fulfilled/partial/violated/appealed).
- Penalización γ ejecutable con actor 'oracle' y evento contract.violation.
- INV1: γ < 0.8 -> retractación AUTOMÁTICA.
- Cierre ACTIVE -> EXECUTED (finalize) con bloqueo de pendientes.
- Apelación: restaura el γ y marca la bitácora.
- Identidad: solo la parte obligada reporta su cumplimiento; cualquier
  participante reporta violaciones; nadie externo.
"""

import os
import tempfile

os.environ['SECRET_KEY'] = 'test-secret'
os.environ.pop('DEEPSEEK_API_KEY', None)

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
            for uid, name in [(1, 'Max'), (2, 'Ana'), (3, 'Luis'), (4, 'Sara')]:
                db.execute(
                    "INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, 'hash')",
                    (uid, f"{name.lower()}@test.com", name),
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
    from app.jwt_utils import create_token

    token = create_token({'user_id': uid})
    return {'Authorization': f'Bearer {token}'}


TERMS = [
    {'term_id': 'do', 'civil_text': 'Max ofrece dos horas',
     'vhv': {'t': 2.0, 'v': 0, 'h': 2.0}, 'assigned_participant_id': 'user-1',
     'penalty_gamma': 0.2},
    {'term_id': 'give', 'civil_text': 'Ana ofrece dos horas',
     'vhv': {'t': 2.0, 'v': 0, 'h': 2.0}, 'assigned_participant_id': 'user-2',
     'penalty_gamma': 0.2},
]


def create_active_contract(client, auth_header, contract_id, wellness_1=1.0):
    res = client.post('/contracts/', headers=auth_header, json={
        'contract_id': contract_id,
        'civil_description': 'Contrato de ejecución',
        'min_reflection_hours': 0,
        'participants': [{'user_id': 1, 'wellness': wellness_1}, {'user_id': 2}],
        'terms': TERMS,
    })
    assert res.status_code == 201, res.get_json()
    for uid in (1, 2):
        for term in ('do', 'give'):
            res = client.post(f'/contracts/{contract_id}/accept',
                              headers=user_headers(client, uid),
                              json={'term_id': term, 'user_id': uid})
            assert res.status_code == 200, res.get_json()
    res = client.post(f'/contracts/{contract_id}/activate', headers=auth_header)
    assert res.status_code == 200, res.get_json()
    return res


def report(client, contract_id, term_id, status, uid, evidence='Evidencia de prueba'):
    return client.post(f'/contracts/{contract_id}/terms/{term_id}/fulfillment',
                       headers=user_headers(client, uid),
                       json={'status': status, 'evidence': evidence})


# ---------------------------------------------------------------------------
# Penalización γ ejecutable
# ---------------------------------------------------------------------------

class TestPenalty:
    def test_penalty_gamma_validation(self, client, auth_header):
        res = client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'ctr-pen-0', 'civil_description': 'x',
            'participants': [{'user_id': 1}],
            'terms': [{'term_id': 't1', 'civil_text': 'Hora de trabajo',
                       'vhv': {'t': 1.0, 'v': 0, 'h': 0},
                       'assigned_participant_id': 'user-1', 'penalty_gamma': 1.5}],
        })
        assert res.status_code == 400
        assert 'penalty_gamma' in res.get_json()['error']

    def test_violation_applies_penalty(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-pen-1')

        # user-2 (participante) reporta la violación del término de user-1
        res = report(client, 'ctr-pen-1', 'do', 'violated', 2)
        assert res.status_code == 200
        assert res.get_json()['wellness_delta'] == pytest.approx(-0.2)

        # El γ de user-1 bajó y persiste; la fuente es 'oracle'
        res = client.get('/contracts/ctr-pen-1', headers=auth_header)
        data = res.get_json()
        max_p = next(p for p in data['participants_details'] if p['id'] == 'user-1')
        assert max_p['wellness'] == pytest.approx(0.8)
        assert data['terms'][0]['fulfillments'][0]['status'] == 'violated'
        assert data['terms'][0]['fulfillments'][0]['reported_by'] == 'user-2'
        with client.application.app_context():
            row = get_db().execute(
                "SELECT reported_by FROM maxo_contract_participants "
                "WHERE contract_id = 'ctr-pen-1' AND participant_id = 'user-1'"
            ).fetchone()
            assert row['reported_by'] == 'oracle'

    def test_fulfilled_no_penalty(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-pen-2')
        res = report(client, 'ctr-pen-2', 'do', 'fulfilled', 1)
        assert res.status_code == 200
        assert res.get_json()['wellness_delta'] == 0
        res = client.get('/contracts/ctr-pen-2', headers=auth_header)
        max_p = next(p for p in res.get_json()['participants_details'] if p['id'] == 'user-1')
        assert max_p['wellness'] == pytest.approx(1.0)

    def test_only_obligated_reports_own_fulfillment(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-pen-3')
        # user-2 intenta reportar como cumplido el término de user-1
        res = report(client, 'ctr-pen-3', 'do', 'fulfilled', 2)
        assert res.status_code == 403

    def test_external_cannot_report_violation(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-pen-4')
        res = report(client, 'ctr-pen-4', 'do', 'violated', 3)  # user-3 no participa
        assert res.status_code == 403


# ---------------------------------------------------------------------------
# INV1: retractación automática
# ---------------------------------------------------------------------------

class TestInv1Teeth:
    def test_gamma_below_threshold_auto_retracts(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-inv1-1')
        report(client, 'ctr-inv1-1', 'do', 'violated', 2)  # γ: 1.0 -> 0.8
        report(client, 'ctr-inv1-1', 'do', 'violated', 2)  # γ: 0.8 -> 0.6

        res = client.post('/contracts/ctr-inv1-1/retract', headers=user_headers(client, 1),
                          json={'user_id': 1, 'reason': 'Mi bienestar colapsó'})
        assert res.status_code == 200
        data = res.get_json()
        assert data['automatic'] is True
        assert data['invariant'] == 'INV1'
        assert data['state'] == 'retracted'

    def test_healthy_gamma_uses_oracle_flow(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-inv1-2')
        res = client.post('/contracts/ctr-inv1-2/retract', headers=user_headers(client, 1),
                          json={'user_id': 1, 'reason': 'Cambio de planes'})
        # No es automático: pasa por el veredicto del oráculo (200 o 400)
        assert res.status_code in (200, 400)
        assert res.get_json().get('automatic') is not True


# ---------------------------------------------------------------------------
# Cierre de ejecución (finalize)
# ---------------------------------------------------------------------------

class TestFinalize:
    def test_pending_terms_block_finalize(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-fin-1')
        report(client, 'ctr-fin-1', 'do', 'fulfilled', 1)
        res = client.post('/contracts/ctr-fin-1/finalize', headers=auth_header)
        assert res.status_code == 400
        assert res.get_json()['code'] == 'EXECUTION_INCOMPLETE'
        assert res.get_json()['pending_terms'] == ['give']

    def test_full_execution_reaches_executed(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-fin-2')
        report(client, 'ctr-fin-2', 'do', 'fulfilled', 1)
        report(client, 'ctr-fin-2', 'give', 'fulfilled', 2)
        res = client.post('/contracts/ctr-fin-2/finalize', headers=auth_header)
        assert res.status_code == 200
        assert res.get_json()['state'] == 'executed'

        res = client.get('/contracts/ctr-fin-2', headers=auth_header)
        assert res.get_json()['state'] == 'executed'

    def test_draft_cannot_finalize(self, client, auth_header):
        client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'ctr-fin-3', 'civil_description': 'x',
            'participants': [{'user_id': 1}],
        })
        res = client.post('/contracts/ctr-fin-3/finalize', headers=auth_header)
        assert res.status_code == 400


# ---------------------------------------------------------------------------
# Apelación
# ---------------------------------------------------------------------------

class TestAppeal:
    def test_appeal_restores_gamma(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-app-1')
        report(client, 'ctr-app-1', 'do', 'violated', 2)  # γ: 1.0 -> 0.8

        # Apela la parte obligada
        res = client.post('/contracts/ctr-app-1/terms/do/appeal',
                          headers=user_headers(client, 1),
                          json={'reason': 'La entrega se hizo al día siguiente'})
        assert res.status_code == 200
        assert res.get_json()['restored_gamma'] == pytest.approx(0.2)

        res = client.get('/contracts/ctr-app-1', headers=auth_header)
        max_p = next(p for p in res.get_json()['participants_details'] if p['id'] == 'user-1')
        assert max_p['wellness'] == pytest.approx(1.0)
        assert res.get_json()['terms'][0]['fulfillments'][0]['status'] == 'appealed'

    def test_appeal_by_third_party_forbidden(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-app-2')
        report(client, 'ctr-app-2', 'do', 'violated', 2)
        res = client.post('/contracts/ctr-app-2/terms/do/appeal',
                          headers=user_headers(client, 2),
                          json={'reason': 'Yo no debería apelar esto'})
        assert res.status_code == 403

    def test_appeal_without_penalty_rejected(self, client, auth_header):
        create_active_contract(client, auth_header, 'ctr-app-3')
        report(client, 'ctr-app-3', 'do', 'fulfilled', 1)
        res = client.post('/contracts/ctr-app-3/terms/do/appeal',
                          headers=user_headers(client, 1),
                          json={'reason': 'Apelo algo que no fue penalizado'})
        assert res.status_code == 400
