"""
Tests del Derecho al Mantenimiento Óptimo (Cap. 17.4) — el ledger del oráculo.

Cubre:
- from-need CON oráculo: crédito automático de % del VHV al sustento del motor.
- from-need SIN oráculo (plantilla): sin crédito (el motor no trabajó).
- Share configurable por entorno (MAXO_ORACLE_MAINTENANCE_SHARE).
- No duplicación (UNIQUE contract+source).
- Plaza pública: GET /verificador/oracle-ledger sin login, sanitizado.
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

            for uid, email, name in (
                (1, 'ana@test.com', 'Ana Pérez'),
                (2, 'luis@test.com', 'Luis Gómez'),
            ):
                db.execute(
                    "INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, 'hash')",
                    (uid, email, name),
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

    token = create_token({'user_id': uid})
    return {'Authorization': f'Bearer {token}'}


def _fake_oracle(available=True):
    """Oráculo disponible que pule la redacción (terms válidos)."""
    class FakeNegotiation:
        reasoning = 'el oráculo pule la redacción'

        @property
        def draft_terms(self):
            return [
                {
                    'term_id': 'ayuda',
                    'civil_text': 'Luis acompaña a Ana en sus trámites con paciencia',
                    'vhv': {'t': 1, 'v': 0, 'h': 0},
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
            self.available = available

        def is_available(self):
            return self.available

        def negotiate(self, instruction, participants=None, session_id=None):
            if not self.available:
                raise RuntimeError('no disponible')
            return FakeNegotiation()

    return FakeOracle


def test_from_need_with_oracle_credits_ledger(client, monkeypatch):
    """El contrato que usó el oráculo alimenta su sustento (5% por defecto)."""
    from app import bridge_b

    monkeypatch.setattr(bridge_b, 'LiveOracle', _fake_oracle(True))

    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['oracle_used'] is True
    assert data['oracle_credit'] is not None
    assert data['oracle_credit']['share'] == 5.0
    # VHV total 2h × 5% = 0.1h de crédito
    assert abs(data['oracle_credit']['credit'] - 0.1) < 1e-6
    assert data['oracle_credit']['engine'] == 'deepseek'


def test_from_need_without_oracle_no_credit(client):
    """Sin oráculo (plantilla determinista): el motor no trabajó, no cobra."""
    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['oracle_used'] is False
    assert data['oracle_credit'] is None


def test_credit_not_duplicated(client, monkeypatch):
    """UNIQUE(contract_id, source): re-crear no duplica el aporte."""
    from app import bridge_b

    monkeypatch.setattr(bridge_b, 'LiveOracle', _fake_oracle(True))

    for _ in range(2):
        res = client.post('/contracts/from-need', headers=auth(client), json={
            'seeker_participant_id': 1,
            'offerer_participant_id': 2,
        })
        assert res.status_code == 201

    with client.application.app_context():
        db = get_db()
        rows = db.execute(
            "SELECT COUNT(*) AS n FROM maxo_oracle_ledger WHERE contract_id = 'from-need-1-2'"
        ).fetchone()
        assert rows['n'] == 1


def test_share_configurable(client, monkeypatch):
    """MAXO_ORACLE_MAINTENANCE_SHARE ajusta el % del aporte (migración)."""
    from app import bridge_b

    os.environ['MAXO_ORACLE_MAINTENANCE_SHARE'] = '10'
    try:
        monkeypatch.setattr(bridge_b, 'LiveOracle', _fake_oracle(True))
        res = client.post('/contracts/from-need', headers=auth(client), json={
            'seeker_participant_id': 1,
            'offerer_participant_id': 2,
        })
        assert res.status_code == 201
        credit = res.get_json()['oracle_credit']
        assert credit['share'] == 10.0
        assert abs(credit['credit'] - 0.2) < 1e-6  # 2h × 10%
    finally:
        del os.environ['MAXO_ORACLE_MAINTENANCE_SHARE']


def test_ledger_public_and_sanitized(client, monkeypatch):
    """La plaza muestra el sustento del oráculo sin login y sin datos personales."""
    from app import bridge_b

    monkeypatch.setattr(bridge_b, 'LiveOracle', _fake_oracle(True))
    client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })

    res = client.get('/verificador/oracle-ledger')
    assert res.status_code == 200
    data = res.get_json()
    assert data['totals']['contracts_funding'] == 1
    assert abs(data['totals']['credit_total_h'] - 0.1) < 1e-6
    assert data['totals']['avg_share'] == 5.0
    assert data['by_engine'].get('deepseek') == 1
    assert len(data['entries']) == 1
    assert data['entries'][0]['contract_id'] == 'from-need-1-2'

    # Sanitización: sin emails ni datos personales (Opacidad Sagrada)
    raw = client.get('/verificador/oracle-ledger').get_data(as_text=True)
    assert 'ana@test.com' not in raw
    assert 'luis@test.com' not in raw


def test_ledger_empty(client):
    """Ledger vacío: estructura sin romperse."""
    res = client.get('/verificador/oracle-ledger')
    assert res.status_code == 200
    data = res.get_json()
    assert data['totals']['contracts_funding'] == 0
    assert data['entries'] == []
