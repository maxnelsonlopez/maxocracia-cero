"""
Tests de la segunda ola de la hackathon (ROADMAP oráculo vivo y escalas, §4):

- Delegación líquida por término (delegations_by_term).
- Expiración de delegaciones (valid_until).
- Ciclo de vida del quórum (quorum_deadline, prórroga, re-consulta que des-sella).
- Webhooks por parte (filtro party_filter).
- Vista de cohorte consolidada (/contracts/cohort).
"""

import os
import tempfile

os.environ['SECRET_KEY'] = 'test-secret'
os.environ.pop('DEEPSEEK_API_KEY', None)

import pytest

from app import create_app
from app.utils import get_db
from app.webhooks import webhook_matches_party


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
        'civil_description': 'Contrato de gobernanza',
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


def accept_delegate(client, auth_header, contract_id, term_id, delegate_id):
    """Firma delegada: el token ES el delegado (Ola 3A.1, R1)."""
    uid = int(delegate_id.split('-')[1])
    return client.post(f'/contracts/{contract_id}/accept',
                       headers=user_headers(client, uid), json={
        'term_id': term_id, 'party_id': 'coop-7',
    })


# ---------------------------------------------------------------------------
# Delegación líquida por término
# ---------------------------------------------------------------------------

class TestLiquidDelegation:
    TERMS = [
        {'term_id': 'term-a', 'civil_text': 'Cláusula A', 'vhv': {'t': 2.0, 'v': 0, 'h': 2.0}},
        {'term_id': 'term-b', 'civil_text': 'Cláusula B', 'vhv': {'t': 3.0, 'v': 0, 'h': 3.0}},
    ]

    def _contract(self, client, auth_header, members, contract_id):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members=members)
        create_contract(client, auth_header, contract_id, [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ], terms=self.TERMS)

    def test_delegation_scoped_per_term(self, client, auth_header):
        """user-1 delega en user-3 SOLO para term-a; en user-2 para term-b."""
        self._contract(client, auth_header, {
            'delegates': ['user-1', 'user-2', 'user-3'],
            'quorum': 1.0,
            'delegations': {'user-1': 'user-2'},
            'delegations_by_term': {'term-a': {'user-1': 'user-3'}},
        }, 'ctr-lqd-1')

        # term-a: user-3 firma y arrastra a user-1 (2/3)
        res = accept_delegate(client, auth_header, 'ctr-lqd-1', 'term-a', 'user-3')
        consent = res.get_json()['consent']
        assert consent['current'] == 2
        assert consent['delegations_applied'] == {'user-1': 'user-3'}

        # term-b: la delegación base (user-1 -> user-2) sigue vigente
        res = accept_delegate(client, auth_header, 'ctr-lqd-1', 'term-b', 'user-2')
        consent = res.get_json()['consent']
        assert consent['current'] == 2
        assert consent['delegations_applied'] == {'user-1': 'user-2'}

    def test_term_scoped_delegation_not_leaking(self, client, auth_header):
        """La delegación de term-a no afecta a term-b: user-3 no arrastra a user-1 allí."""
        self._contract(client, auth_header, {
            'delegates': ['user-1', 'user-2', 'user-3'],
            'quorum': 1.0,
            'delegations_by_term': {'term-a': {'user-1': 'user-3'}},
        }, 'ctr-lqd-2')

        res = accept_delegate(client, auth_header, 'ctr-lqd-2', 'term-b', 'user-3')
        consent = res.get_json()['consent']
        assert consent['current'] == 1
        assert consent['delegations_applied'] == {}


# ---------------------------------------------------------------------------
# Expiración de delegaciones (valid_until)
# ---------------------------------------------------------------------------

class TestDelegationExpiry:
    def test_expired_delegation_ignored(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
            'delegations': {'user-1': {'proxy': 'user-2', 'valid_until': '2020-01-01T00:00:00'}},
        })
        create_contract(client, auth_header, 'ctr-exp-1', [
            {'user_id': 1}, {'user_id': 2},
            {'party_id': 'coop-7'},
        ])
        res = accept_delegate(client, auth_header, 'ctr-exp-1', 'term-1', 'user-2')
        consent = res.get_json()['consent']
        assert consent['current'] == 1  # user-1 ya no viaja con user-2
        assert 'user-1' in consent['expired_delegations']

    def test_future_delegation_still_active(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
            'delegations': {'user-1': {'proxy': 'user-2', 'valid_until': '2099-01-01T00:00:00'}},
        })
        create_contract(client, auth_header, 'ctr-exp-2', [
            {'user_id': 1}, {'user_id': 2},
            {'party_id': 'coop-7'},
        ])
        res = accept_delegate(client, auth_header, 'ctr-exp-2', 'term-1', 'user-2')
        consent = res.get_json()['consent']
        assert consent['current'] == 2
        assert consent['approved'] is True


# ---------------------------------------------------------------------------
# Ciclo de vida del quórum (deadline, prórroga, re-consulta)
# ---------------------------------------------------------------------------

class TestQuorumLifecycle:
    def test_expired_window_rejects_and_extension_reopens(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
            'quorum_deadline': '2020-01-01T00:00:00',
        })
        create_contract(client, auth_header, 'ctr-win-1', [
            {'user_id': 1}, {'user_id': 2},
            {'party_id': 'coop-7'},
        ])

        res = accept_delegate(client, auth_header, 'ctr-win-1', 'term-1', 'user-1')
        assert res.status_code == 409
        assert res.get_json()['code'] == 'QUORUM_EXPIRED'

        # Prórroga: reabre la ventana
        res = client.post('/parties/coop-7/quorum-extension', headers=auth_header,
                          json={'deadline': '2099-01-01T00:00:00'})
        assert res.status_code == 200
        assert res.get_json()['quorum_deadline'] == '2099-01-01T00:00:00'

        res = accept_delegate(client, auth_header, 'ctr-win-1', 'term-1', 'user-1')
        assert res.status_code == 202
        assert res.get_json()['consent']['deadline_expired'] is False

    def test_membership_change_revokes_seal(self, client, auth_header):
        """Re-consulta: si la configuración de miembros cambia y el quórum ya
        no se cumple, el sello se revoca al recargar (T13: la verdad vigente)."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
        })
        create_contract(client, auth_header, 'ctr-req-1', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])

        # Sellar con unanimidad de 2 (primera firma 202, segunda sella 200)
        res = accept_delegate(client, auth_header, 'ctr-req-1', 'term-1', 'user-1')
        assert res.status_code == 202
        res = accept_delegate(client, auth_header, 'ctr-req-1', 'term-1', 'user-2')
        assert res.status_code == 200

        res = client.get('/contracts/ctr-req-1', headers=auth_header)
        assert res.get_json()['terms'][0]['accepted_by'].get('coop-7') is True

        # Nuevo miembro: el quórum pasa a exigir 3; el sello se revoca solo
        client.put('/parties/coop-7', headers=auth_header, json={
            'members': {
                'delegates': ['user-1', 'user-2', 'user-3'],
                'quorum': 1.0,
            },
        })
        res = client.get('/contracts/ctr-req-1', headers=auth_header)
        assert res.get_json()['terms'][0]['accepted_by'].get('coop-7') is not True

        # Con el tercer delegado se vuelve a sellar
        res = accept_delegate(client, auth_header, 'ctr-req-1', 'term-1', 'user-3')
        assert res.status_code == 200
        assert res.get_json()['quorum_reached'] is True


# ---------------------------------------------------------------------------
# Webhooks por parte (filtro party_filter)
# ---------------------------------------------------------------------------

class TestWebhookPartyFilter:
    def test_no_filter_receives_all(self):
        assert webhook_matches_party(None, ['coop-7']) is True
        assert webhook_matches_party('', ['coop-7']) is True

    def test_matching_filter(self):
        assert webhook_matches_party('["coop-7", "org-9"]', ['coop-7']) is True

    def test_non_matching_filter(self):
        assert webhook_matches_party('["org-9"]', ['coop-7']) is False

    def test_no_parties_no_match(self):
        assert webhook_matches_party('["coop-7"]', None) is False
        assert webhook_matches_party('["coop-7"]', []) is False

    def test_invalid_filter_receives_all(self):
        assert webhook_matches_party('{no-json', ['coop-7']) is True


# ---------------------------------------------------------------------------
# Vista de cohorte consolidada
# ---------------------------------------------------------------------------

class TestCohortOverview:
    def test_cohort_aggregates_collective_parties(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
        })
        make_party(client, auth_header, 'org-9', 'institution', 'Escuela Aurora', members={
            'delegates': ['user-1'],
            'quorum': 1.0,
        })
        create_contract(client, auth_header, 'ctr-coh-1', [
            {'user_id': 1}, {'user_id': 2}, {'party_id': 'coop-7'},
        ])
        create_contract(client, auth_header, 'ctr-coh-2', [
            {'user_id': 1}, {'user_id': 2}, {'party_id': 'coop-7'},
        ])
        # org-9 aún sin contratos: no aparece en la cohorte

        res = client.get('/contracts/cohort', headers=auth_header)
        assert res.status_code == 200
        data = res.get_json()
        assert data['totals']['parties'] == 1
        assert data['totals']['total_contracts'] == 2
        coop = data['parties'][0]
        assert coop['party_id'] == 'coop-7'
        assert coop['contracts_total'] == 2
        assert coop['contracts_pending'] == 2
        assert coop['contracts_active'] == 0

    def test_cohort_counts_sealed_terms(self, client, auth_header):
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
        })
        create_contract(client, auth_header, 'ctr-coh-3', [
            {'user_id': 1}, {'user_id': 2}, {'party_id': 'coop-7'},
        ])
        for d in ('user-1', 'user-2'):
            accept_delegate(client, auth_header, 'ctr-coh-3', 'term-1', d)

        res = client.get('/contracts/cohort', headers=auth_header)
        coop = res.get_json()['parties'][0]
        assert coop['terms_sealed'] == 1
