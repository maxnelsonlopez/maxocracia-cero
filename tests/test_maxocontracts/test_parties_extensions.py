"""
Tests de las extensiones de la hackathon (ROADMAP oráculo vivo y escalas, §4).

Cubre:
- Ext. 1: votación ponderada (weights, weight_threshold) en el quórum.
- Ext. 2: delegación temporal (delegations, votos efectivos, guarda de ciclos).
- Ext. 3: γ agregado real por contrato (media ponderada del γ de los miembros).
- Ext. 4: árbol jerárquico (GET /contracts/<id>/tree) y endpoint de sub-contratos.
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
        'civil_description': 'Contrato de extensiones',
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


def accept_delegate(client, auth_header, contract_id, delegate_id):
    return client.post(f'/contracts/{contract_id}/accept', headers=auth_header, json={
        'term_id': 'term-1', 'party_id': 'coop-7', 'delegate_id': delegate_id,
    })


# ---------------------------------------------------------------------------
# Ext. 1 — Votación ponderada
# ---------------------------------------------------------------------------

class TestWeightedVoting:
    def test_weighted_quorum_fraction_of_total_weight(self, client, auth_header):
        """Pesos {u1:2, u2:1, u3:1} + quorum 0.6 -> umbral 3 de 4."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2', 'user-3'],
            'weights': {'user-1': 2, 'user-2': 1, 'user-3': 1},
            'quorum': 0.6,
        })
        create_contract(client, auth_header, 'ctr-peso-1', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])

        res = accept_delegate(client, auth_header, 'ctr-peso-1', 'user-1')
        assert res.status_code == 202
        consent = res.get_json()['consent']
        assert consent['mode'] == 'weighted_quorum'
        assert consent['current_weight'] == 2
        assert consent['needed_weight'] == 3
        assert consent['total_weight'] == 4
        assert consent['approved'] is False

        # u2 aporta 1 -> peso total 3/3: se sella
        res = accept_delegate(client, auth_header, 'ctr-peso-1', 'user-2')
        assert res.status_code == 200
        assert res.get_json()['consent']['approved'] is True
        assert res.get_json()['quorum_reached'] is True

    def test_weight_threshold_absolute(self, client, auth_header):
        """weight_threshold: umbral absoluto de peso (2) — un delegado pesado sella."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'weights': {'user-1': 2, 'user-2': 1},
            'weight_threshold': 2,
        })
        create_contract(client, auth_header, 'ctr-peso-2', [
            {'user_id': 1}, {'user_id': 2},
            {'party_id': 'coop-7'},
        ])

        res = accept_delegate(client, auth_header, 'ctr-peso-2', 'user-1')
        assert res.status_code == 200
        consent = res.get_json()['consent']
        assert consent['mode'] == 'weighted_threshold'
        assert consent['current_weight'] == 2
        assert consent['needed_weight'] == 2

    def test_legacy_quorum_unchanged(self, client, auth_header):
        """Sin pesos, el quórum N de M sigue siendo por delegados."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2', 'user-3'],
            'quorum': 0.6,
        })
        create_contract(client, auth_header, 'ctr-peso-3', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])
        res = accept_delegate(client, auth_header, 'ctr-peso-3', 'user-1')
        assert res.status_code == 202
        consent = res.get_json()['consent']
        assert consent['mode'] == 'quorum'
        assert consent['needed'] == 2
        assert consent['needed_weight'] is None


# ---------------------------------------------------------------------------
# Ext. 2 — Delegación temporal
# ---------------------------------------------------------------------------

class TestDelegation:
    def test_delegated_vote_counts_for_proxy(self, client, auth_header):
        """user-1 delega en user-2: cuando user-2 firma, el voto de user-1 cuenta."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2', 'user-3'],
            'quorum': 1.0,  # se requiere unanimidad (3 de 3)
            'delegations': {'user-1': 'user-2'},
        })
        create_contract(client, auth_header, 'ctr-del-1', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])

        # user-2 firma y arrastra el voto de user-1: 2 votos efectivos de 3
        res = accept_delegate(client, auth_header, 'ctr-del-1', 'user-2')
        assert res.status_code == 202
        consent = res.get_json()['consent']
        assert consent['current'] == 2
        assert 'user-1' in consent['effective_delegates']
        assert 'user-1' not in consent['approved_delegates']

        # user-3 firma -> 3/3: sellado
        res = accept_delegate(client, auth_header, 'ctr-del-1', 'user-3')
        assert res.status_code == 200
        assert res.get_json()['quorum_reached'] is True

    def test_transitive_delegation_chain(self, client, auth_header):
        """Cadena transitiva: u1 -> u2 -> u3; firmar u3 cuenta para los tres."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2', 'user-3'],
            'quorum': 1.0,
            'delegations': {'user-1': 'user-2', 'user-2': 'user-3'},
        })
        create_contract(client, auth_header, 'ctr-del-2', [
            {'user_id': 1}, {'user_id': 2}, {'user_id': 3},
            {'party_id': 'coop-7'},
        ])
        res = accept_delegate(client, auth_header, 'ctr-del-2', 'user-3')
        assert res.status_code == 200
        consent = res.get_json()['consent']
        assert consent['current'] == 3
        assert set(consent['effective_delegates']) == {'user-1', 'user-2', 'user-3'}

    def test_delegation_cycle_does_not_hang(self, client, auth_header):
        """Ciclo A<->B no cuelga ni duplica votos: cada voto cuenta una vez."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
            'delegations': {'user-1': 'user-2', 'user-2': 'user-1'},
        })
        create_contract(client, auth_header, 'ctr-del-3', [
            {'user_id': 1}, {'user_id': 2},
            {'party_id': 'coop-7'},
        ])
        res = accept_delegate(client, auth_header, 'ctr-del-3', 'user-1')
        # user-2 delega en user-1: al firmar user-1, ambos votos se ejercen
        # (cada uno exactamente una vez, sin voto fantasma ni bucle infinito).
        consent = res.get_json()['consent']
        assert consent['current'] == 2
        assert set(consent['effective_delegates']) == {'user-1', 'user-2'}
        assert consent['approved'] is True

    def test_invalid_delegation_ignored(self, client, auth_header):
        """Delegación a alguien que no es miembro se ignora."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'quorum': 1.0,
            'delegations': {'user-1': 'user-99'},
        })
        create_contract(client, auth_header, 'ctr-del-4', [
            {'user_id': 1}, {'user_id': 2},
            {'party_id': 'coop-7'},
        ])
        res = accept_delegate(client, auth_header, 'ctr-del-4', 'user-2')
        assert res.get_json()['consent']['current'] == 1


# ---------------------------------------------------------------------------
# Ext. 3 — γ agregado real por contrato
# ---------------------------------------------------------------------------

class TestAggregateWellness:
    def test_collective_wellness_is_members_mean(self, client, auth_header):
        """El γ de la cooperativa es la media del γ de sus miembros en el contrato."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
        })
        create_contract(client, auth_header, 'ctr-agg-1', [
            {'user_id': 1, 'wellness': 0.9},
            {'user_id': 2, 'wellness': 0.7},
            {'party_id': 'coop-7'},
        ])

        res = client.get('/contracts/ctr-agg-1', headers=auth_header)
        coop = next(d for d in res.get_json()['participants_details'] if d['id'] == 'coop-7')
        assert coop['wellness'] == pytest.approx(0.8)

        # T13: el registro de partes refleja el agregado
        res = client.get('/parties/coop-7', headers=auth_header)
        assert res.get_json()['party']['wellness'] == pytest.approx(0.8)

    def test_weighted_aggregate(self, client, auth_header):
        """Con pesos: (2*0.9 + 1*0.7) / 3 ≈ 0.8333."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
            'weights': {'user-1': 2, 'user-2': 1},
        })
        create_contract(client, auth_header, 'ctr-agg-2', [
            {'user_id': 1, 'wellness': 0.9},
            {'user_id': 2, 'wellness': 0.7},
            {'party_id': 'coop-7'},
        ])

        res = client.get('/contracts/ctr-agg-2', headers=auth_header)
        coop = next(d for d in res.get_json()['participants_details'] if d['id'] == 'coop-7')
        assert coop['wellness'] == pytest.approx((2 * 0.9 + 0.7) / 3)

    def test_no_members_in_contract_keeps_provided_wellness(self, client, auth_header):
        """Sin miembros en el contrato, se conserva el γ provisto."""
        make_party(client, auth_header, 'coop-7', 'cooperative', 'Coop del Barrio', members={
            'delegates': ['user-1', 'user-2'],
        })
        create_contract(client, auth_header, 'ctr-agg-3', [
            {'user_id': 3},  # Luis no es miembro de la coop
            {'party_id': 'coop-7', 'wellness': 0.95},
        ])

        res = client.get('/contracts/ctr-agg-3', headers=auth_header)
        coop = next(d for d in res.get_json()['participants_details'] if d['id'] == 'coop-7')
        assert coop['wellness'] == pytest.approx(0.95)


# ---------------------------------------------------------------------------
# Ext. 4 — Árbol jerárquico y sub-contratos
# ---------------------------------------------------------------------------

class TestHierarchy:
    def test_tree_endpoint_nested(self, client, auth_header):
        create_contract(client, auth_header, 'acuerdo-madre', [
            {'user_id': 1}, {'user_id': 2},
        ])
        create_contract(client, auth_header, 'micro-hijo', [
            {'user_id': 1}, {'user_id': 2},
        ])
        client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'micro-hijo',
            'civil_description': 'Hijo',
            'parent_contract_id': 'acuerdo-madre',
            'participants': [{'user_id': 1}, {'user_id': 2}],
        })
        client.post('/contracts/', headers=auth_header, json={
            'contract_id': 'micro-nieto',
            'civil_description': 'Nieto',
            'parent_contract_id': 'micro-hijo',
            'participants': [{'user_id': 1}, {'user_id': 2}],
        })

        res = client.get('/contracts/acuerdo-madre/tree', headers=auth_header)
        assert res.status_code == 200
        tree = res.get_json()['tree']
        assert tree['contract_id'] == 'acuerdo-madre'
        assert tree['subcontracts'][0]['contract_id'] == 'micro-hijo'
        assert tree['subcontracts'][0]['subcontracts'][0]['contract_id'] == 'micro-nieto'
        assert res.get_json()['ancestors'] == []

        res = client.get('/contracts/micro-nieto/tree', headers=auth_header)
        assert res.get_json()['ancestors'] == ['micro-hijo', 'acuerdo-madre']

    def test_subcontract_endpoint(self, client, auth_header):
        create_contract(client, auth_header, 'madre', [{'user_id': 1}])

        res = client.post('/contracts/madre/subcontracts', headers=auth_header, json={
            'contract_id': 'hijo-api',
            'civil_description': 'Creado por endpoint',
            'participants': [{'user_id': 1}, {'user_id': 2}],
            'terms': [{
                'term_id': 't1',
                'civil_text': 'Cláusula del hijo',
                'vhv': {'t': 1.0, 'v': 0, 'h': 1.0},
            }],
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data['parent_contract_id'] == 'madre'

        res = client.get('/contracts/madre', headers=auth_header)
        assert 'hijo-api' in res.get_json()['subcontracts']

        # 404 si el padre no existe; 400 sin contract_id
        res = client.post('/contracts/no-existe/subcontracts', headers=auth_header,
                          json={'contract_id': 'huerfano'})
        assert res.status_code == 404
        res = client.post('/contracts/madre/subcontracts', headers=auth_header, json={})
        assert res.status_code == 400
