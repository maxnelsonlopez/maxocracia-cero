"""
Tests del Bloque B — Escalas e interescala (ROADMAP oráculo vivo y escalas).

Cubre:
- Fase 1: party_id genérico, registro maxo_parties, resolvers por prefijo
  (user-, synthetic-, society-, coop-, org-, eco-), API /parties.
- Fase 2: consentimiento agregado con quórum (firma delegada N de M).
- Fase 4: Reino Natural (eco-) con guardián oráculo (degradación heurística).
- Fase 5: contratos interescala anidados (padre/hijos) con protección de ciclos.
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
    """Token del usuario real: la identidad SIEMPRE deriva del JWT (Ola 3A.1)."""
    from app.jwt_utils import create_token

    token = create_token({'user_id': uid})
    return {'Authorization': f'Bearer {token}'}


def make_party(client, auth_header, party_id, party_type, name, members=None):
    res = client.post('/parties/', headers=auth_header, json={
        'party_id': party_id,
        'party_type': party_type,
        'display_name': name,
        'members': members or {},
    })
    assert res.status_code == 201, res.get_json()
    return res.get_json()['party']


def create_contract(client, auth_header, contract_id, participants, terms=None):
    res = client.post('/contracts/', headers=auth_header, json={
        'contract_id': contract_id,
        'civil_description': 'Contrato de escalas',
        'participants': participants,
        'terms': terms or [
            {
                'term_id': 'term-1',
                'civil_text': 'Acción y reciprocidad balanceadas',
                'vhv': {'t': 5.0, 'v': 0, 'h': 5.0},
            },
        ],
    })
    assert res.status_code == 201, res.get_json()
    return res


# ---------------------------------------------------------------------------
# Fase 1 — party_id genérico y registro de escalas
# ---------------------------------------------------------------------------

class TestPartiesRegistry:
    def test_create_and_list_parties(self, client, auth_header):
        coop = make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio',
                          members={'delegates': ['user-1', 'user-2'], 'quorum': 0.5})
        assert coop['party_type'] == 'cooperative'
        assert coop['party_type_label'] == 'Cooperativa'

        res = client.get('/parties/', headers=auth_header)
        data = res.get_json()
        assert data['total'] == 1
        assert data['parties'][0]['party_id'] == 'coop-7'

        res = client.get('/parties/coop-7', headers=auth_header)
        detail = res.get_json()['party']
        assert detail['display_name'] == 'Coop del Barrio'
        assert detail['consent']['mode'] == 'quorum'

    def test_auto_generated_party_id(self, client, auth_header):
        res = client.post('/parties/', headers=auth_header, json={
            'party_type': 'society',
            'display_name': 'Hogar Norte',
        })
        assert res.status_code == 201
        party_id = res.get_json()['party']['party_id']
        assert party_id.startswith('society-')

    def test_party_type_mismatch_rejected(self, client, auth_header):
        res = client.post('/parties/', headers=auth_header, json={
            'party_id': 'coop-7',
            'party_type': 'institution',
            'display_name': 'Mal tipada',
        })
        assert res.status_code == 400

    def test_invalid_party_id_format_rejected(self, client, auth_header):
        res = client.post('/parties/', headers=auth_header, json={
            'party_id': 'banana-1',
            'party_type': 'institution',
            'display_name': 'Institucion',
        })
        assert res.status_code == 400


class TestCollectivePartyInContracts:
    def test_create_contract_with_collective_parties(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio',
                   members={'delegates': ['user-1', 'user-2', 'user-3'], 'quorum': 0.6})
        make_party(client, auth_header, 'org-9', 'institution', 'Escuela Aurora')

        create_contract(client, auth_header, 'ctr-escalas-1', [
            {'user_id': 1, 'wellness': 1.0},
            {'party_id': 'coop-7'},
            {'party_id': 'org-9'},
        ])

        res = client.get('/contracts/ctr-escalas-1', headers=auth_header)
        data = res.get_json()
        assert set(data['participants']) == {'user-1', 'coop-7', 'org-9'}
        by_id = {d['id']: d for d in data['participants_details']}
        assert by_id['coop-7']['party_type'] == 'cooperative'
        assert by_id['coop-7']['is_collective'] is True
        assert by_id['coop-7']['name'] == 'Coop del Barrio'
        assert by_id['coop-7']['members']['delegates'] == ['user-1', 'user-2', 'user-3']
        assert by_id['org-9']['party_type'] == 'institution'
        assert by_id['user-1']['party_type'] == 'human'

    def test_batch_auto_creates_collective_party(self, client, auth_header):
        """Un party_id colectivo desconocido se auto-registra con display_name."""
        create_contract(client, auth_header, 'ctr-escalas-2', [
            {'user_id': 1},
            {'party_id': 'coop-42', 'display_name': 'Coop Semilla',
             'members': {'delegates': ['user-1'], 'quorum': 1.0}},
        ])
        res = client.get('/contracts/ctr-escalas-2', headers=auth_header)
        by_id = {d['id']: d for d in res.get_json()['participants_details']}
        assert by_id['coop-42']['name'] == 'Coop Semilla'

        res = client.get('/parties/coop-42', headers=auth_header)
        assert res.get_json()['party']['display_name'] == 'Coop Semilla'

    def test_add_participant_with_party_id(self, client, auth_header):
        make_party(client, auth_header, 'society-3', 'society', 'Hogar Norte')
        create_contract(client, auth_header, 'ctr-escalas-3', [{'user_id': 1}])

        res = client.post('/contracts/ctr-escalas-3/participants',
                          headers=auth_header, json={'party_id': 'society-3'})
        assert res.status_code == 200
        data = res.get_json()
        assert data['participant_id'] == 'society-3'
        assert data['party_type'] == 'society'

    def test_invalid_party_id_rejected(self, client, auth_header):
        create_contract(client, auth_header, 'ctr-escalas-4', [{'user_id': 1}])
        res = client.post('/contracts/ctr-escalas-4/participants',
                          headers=auth_header, json={'party_id': 'banana-1'})
        assert res.status_code == 400

    def test_collective_wellness_syncs_to_registry(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio')
        create_contract(client, auth_header, 'ctr-escalas-5', [{'user_id': 1}])
        res = client.post('/contracts/ctr-escalas-5/participants',
                          headers=auth_header, json={'party_id': 'coop-7', 'wellness': 0.8})
        assert res.status_code == 200

        # T13: el registro refleja el γ agregado observado
        res = client.get('/parties/coop-7', headers=auth_header)
        assert res.get_json()['party']['wellness'] == pytest.approx(0.8)


# ---------------------------------------------------------------------------
# Fase 2 — consentimiento agregado con quórum
# ---------------------------------------------------------------------------

class TestQuorumConsent:
    DELEGATES = ['user-1', 'user-2', 'user-3']

    def _make_coop(self, client, auth_header, party_id='coop-7', quorum=0.6):
        return make_party(client, auth_header, party_id, 'cooperative',
                          'Coop del Barrio',
                          members={'delegates': self.DELEGATES, 'quorum': quorum})

    def _create_contract_with_coop(self, client, auth_header):
        self._make_coop(client, auth_header)
        create_contract(client, auth_header, 'ctr-quorum-1', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])

    def test_quorum_flow_delegate_by_delegate(self, client, auth_header):
        """N de M: con quorum 0.6 (2 de 3), la segunda firma sella el término."""
        self._create_contract_with_coop(client, auth_header)

        res = client.post('/contracts/ctr-quorum-1/accept', headers=user_headers(client, 1),
                          json={'term_id': 'term-1', 'party_id': 'coop-7'})
        assert res.status_code == 202
        data = res.get_json()
        assert data['success'] is False
        assert data['quorum_reached'] is False
        assert data['consent']['current'] == 1
        assert data['consent']['needed'] == 2

        res = client.post('/contracts/ctr-quorum-1/accept', headers=user_headers(client, 2),
                          json={'term_id': 'term-1', 'party_id': 'coop-7'})
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert data['quorum_reached'] is True
        assert data['consent']['approved_delegates'] == ['user-1', 'user-2']

        # Los demás participantes humanos aceptan el término
        for uid in (1, 2, 3):
            res = client.post('/contracts/ctr-quorum-1/accept', headers=user_headers(client, uid),
                              json={'term_id': 'term-1', 'user_id': uid})
            assert res.status_code == 200

        # El contrato puede activarse: todos aceptaron el único término
        res = client.post('/contracts/ctr-quorum-1/activate', headers=auth_header)
        assert res.status_code == 200
        assert res.get_json()['state'] == 'active'

    def test_non_delegate_rejected(self, client, auth_header):
        self._create_contract_with_coop(client, auth_header)
        res = client.post('/contracts/ctr-quorum-1/accept', headers=user_headers(client, 4),
                          json={'term_id': 'term-1', 'party_id': 'coop-7'})
        assert res.status_code == 403

    def test_collective_without_delegates_conflict(self, client, auth_header):
        make_party(client, auth_header, 'society-2', 'society', 'Hogar Sin Quorum')
        create_contract(client, auth_header, 'ctr-quorum-2', [
            {'user_id': 1}, {'party_id': 'society-2'},
        ])
        res = client.post('/contracts/ctr-quorum-2/accept', headers=user_headers(client, 1),
                          json={'term_id': 'term-1', 'party_id': 'society-2'})
        assert res.status_code == 409

    def test_quorum_survives_reload(self, client, auth_header):
        """Firmas delegadas parciales persisten; el sello llega al cumplirse N."""
        self._make_coop(client, auth_header, quorum=1.0)  # 3 de 3
        create_contract(client, auth_header, 'ctr-quorum-3', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])

        for delegate in ['user-1', 'user-2']:
            res = client.post('/contracts/ctr-quorum-3/accept',
                              headers=user_headers(client, int(delegate.split('-')[1])),
                              json={'term_id': 'term-1', 'party_id': 'coop-7'})
            assert res.status_code == 202

        # Recarga: 2/3, aún sin sello
        res = client.get('/contracts/ctr-quorum-3', headers=auth_header)
        term = res.get_json()['terms'][0]
        assert term['accepted_by'].get('coop-7') is not True

        # Tercera firma: quórum cumplido y persistido
        res = client.post('/contracts/ctr-quorum-3/accept', headers=user_headers(client, 3),
                          json={'term_id': 'term-1', 'party_id': 'coop-7'})
        assert res.status_code == 200
        assert res.get_json()['quorum_reached'] is True

        res = client.get('/contracts/ctr-quorum-3', headers=auth_header)
        term = res.get_json()['terms'][0]
        assert term['accepted_by'].get('coop-7') is True


# ---------------------------------------------------------------------------
# Fase 4 — Reino Natural (eco-) con guardián oráculo
# ---------------------------------------------------------------------------

class TestEcosystemGuardian:
    def test_guardian_accepts_axiom_valid_contract(self, client, auth_header):
        make_party(client, auth_header, 'eco-1', 'ecosystem', 'Humedal del Valle')
        create_contract(client, auth_header, 'ctr-eco-1', [
            {'user_id': 1},
            {'party_id': 'eco-1'},
        ])

        res = client.post('/contracts/ctr-eco-1/accept', headers=auth_header,
                          json={'term_id': 'term-1', 'party_id': 'eco-1'})
        assert res.status_code == 200
        data = res.get_json()
        assert data['success'] is True
        assert data['guardian']['mode'] == 'oracle_guardian'
        assert 'heurístico' in data['guardian']['reasoning']

        res = client.post('/contracts/ctr-eco-1/accept', headers=auth_header,
                          json={'term_id': 'term-1', 'user_id': 1})
        assert res.status_code == 200

        res = client.post('/contracts/ctr-eco-1/activate', headers=auth_header)
        assert res.status_code == 200

    def test_guardian_denies_axiom_violating_contract(self, client, auth_header):
        make_party(client, auth_header, 'eco-1', 'ecosystem', 'Humedal del Valle')
        # γ < 1 (dentro del rango permitido [0.5, 1.5]) viola el invariante
        # de bienestar: el ecosistema no puede contratar en sufrimiento.
        create_contract(client, auth_header, 'ctr-eco-2', [
            {'user_id': 1},
            {'party_id': 'eco-1', 'wellness': 0.6},
        ])

        res = client.post('/contracts/ctr-eco-2/accept', headers=auth_header,
                          json={'term_id': 'term-1', 'party_id': 'eco-1'})
        assert res.status_code == 400
        data = res.get_json()
        assert 'guardian_reasoning' in data
        assert 'INV' in data['guardian_reasoning']


# ---------------------------------------------------------------------------
# Fase 5 — contratos interescala anidados
# ---------------------------------------------------------------------------class TestNestedContracts:
    def test_parent_and_subcontracts(self, client, auth_header):
        create_contract(client, auth_header, 'acuerdo-madre', [
            {'user_id': 1}, {'user_id': 2},
        ])
        create_contract(client, auth_header, 'micro-hijo-1', [
            {'user_id': 1}, {'user_id': 2},
        ])
        res = client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'micro-hijo-1',
            'civil_description': 'Sub-contrato interno',
            'parent_contract_id': 'acuerdo-madre',
            'participants': [{'user_id': 1}, {'user_id': 2}],
            'terms': [{
                'term_id': 'term-hijo',
                'civil_text': 'Cuidado compartido dentro del acuerdo madre',
                'vhv': {'t': 2.0, 'v': 0, 'h': 2.0},
            }],
        })
        assert res.status_code == 201

        res = client.get('/contracts/acuerdo-madre', headers=auth_header)
        assert res.get_json()['subcontracts'] == ['micro-hijo-1']

        res = client.get('/contracts/micro-hijo-1', headers=auth_header)
        assert res.get_json()['parent_contract_id'] == 'acuerdo-madre'

    def test_missing_parent_rejected(self, client, auth_header):
        res = client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'ctr-huerfano',
            'civil_description': 'Sin padre',
            'parent_contract_id': 'no-existe',
            'participants': [{'user_id': 1}],
        })
        assert res.status_code == 400

    def test_cycle_rejected(self, client, auth_header):
        create_contract(client, auth_header, 'ctr-a', [{'user_id': 1}])
        res = client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'ctr-b',
            'civil_description': 'Hijo de A',
            'parent_contract_id': 'ctr-a',
            'participants': [{'user_id': 1}],
        })
        assert res.status_code == 201

        # Intentar re-crear A como hijo de B formaría el ciclo A <-> B
        res = client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'ctr-a',
            'civil_description': 'A (hijo de B)',
            'parent_contract_id': 'ctr-b',
            'participants': [{'user_id': 1}],
        })
        assert res.status_code == 400
        assert 'ciclo' in res.get_json()['error']


# ---------------------------------------------------------------------------
# Regresión: rehidratación de contratos fuera de DRAFT
# ---------------------------------------------------------------------------

class TestContractReload:
    def test_activated_contract_reloads(self, client, auth_header):
        """Un contrato ACTIVO debe cargarse por API (regresión: add_participant
        exigía DRAFT y rompía la rehidratación de participantes)."""
        create_contract(client, auth_header, 'ctr-reload-1', [
            {'user_id': 1}, {'user_id': 2},
        ])
        for uid in (1, 2):
            res = client.post('/contracts/ctr-reload-1/accept', headers=user_headers(client, uid),
                              json={'term_id': 'term-1', 'user_id': uid})
            assert res.status_code == 200
        res = client.post('/contracts/ctr-reload-1/activate', headers=auth_header)
        assert res.status_code == 200

        res = client.get('/contracts/ctr-reload-1', headers=auth_header)
        assert res.status_code == 200
        data = res.get_json()
        assert data['state'] == 'active'
        assert len(data['participants_details']) == 2
        assert data['participants'] == ['user-1', 'user-2']
        assert data['terms'][0]['accepted_by'] == {'user-1': True, 'user-2': True}

    def test_add_participant_to_pending_contract_rejected(self, client, auth_header):
        create_contract(client, auth_header, 'ctr-reload-2', [
            {'user_id': 1}, {'user_id': 2},
        ])
        for uid in (1, 2):
            client.post('/contracts/ctr-reload-2/accept', headers=user_headers(client, uid),
                        json={'term_id': 'term-1', 'user_id': uid})
        res = client.post('/contracts/ctr-reload-2/activate', headers=auth_header)
        assert res.status_code == 200

        # En PENDING/ACTIVE ya no se añaden partes (misma política que add_term)
        res = client.post('/contracts/ctr-reload-2/participants', headers=auth_header,
                          json={'user_id': 3})
        assert res.status_code == 400
