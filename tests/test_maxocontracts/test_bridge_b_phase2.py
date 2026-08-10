"""
Tests del Puente B de la Ola 4, FASE 2: el camino de firma guiado.

Cubre:
- POST /contracts/<id>/cycle: DRAFT → PENDING → firma de términos del actor
  → activación automática cuando todo está firmado y sin bloqueos.
- GET /contracts/<id>/cycle: el camino de firma (estado, firmas, protecciones).
- Identidad (Ola 3A.1): nadie firma el tramo de otro.
- Escalera de equidad (Ola 3B): paráfrasis obligatoria para perfiles
  protegidos; oráculo requerido para assisted/shielded.
- Criterio de salida del puente: necesidad → contrato ACTIVO sin teclear
  el contrato (solo la ruta /from-need + /cycle).
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
                (3, 'testigo@test.com', 'Testigo Díaz'),
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


def _make_draft(client):
    """Crea el borrador desde la necesidad (Fase 1) y lo deja listo."""
    res = client.post('/contracts/from-need', headers=auth(client), json={
        'seeker_participant_id': 1,
        'offerer_participant_id': 2,
    })
    assert res.status_code == 201
    return res.get_json()['contract_id']


def test_full_cycle_need_to_active(client):
    """CRITERIO DE SALIDA: una necesidad registrada produce un contrato
    firmado y ACTIVO sin teclear el contrato."""
    cid = _make_draft(client)

    # Ana (parte 1) camina su tramo: DRAFT → PENDING + firma sus términos
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 1), json={})
    assert res.status_code in (200, 202)  # 202: falta la firma de Luis
    data = res.get_json()
    assert data['state'] == 'pending'
    assert any(a['action'] == 'submitted' for a in data['actions'])
    assert data['signed_terms'] == ['oferta', 'reciprocidad']
    assert data['activated'] is False  # falta la firma de Luis

    # Luis (parte 2) firma su tramo → todo aceptado → activación
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 2), json={})
    assert res.status_code == 200
    data = res.get_json()
    assert data['activated'] is True
    assert data['state'] == 'active'

    # Verificación final: contrato activo
    detail = client.get(f'/contracts/{cid}', headers=auth(client, 1)).get_json()
    assert detail['state'] == 'active'
    assert all(t['accepted_by'].get('user-1') and t['accepted_by'].get('user-2')
               for t in detail['terms'])


def test_cycle_status_roadmap(client):
    """El camino de firma muestra qué falta y quién debe actuar."""
    cid = _make_draft(client)

    res = client.get(f'/contracts/{cid}/cycle', headers=auth(client, 1))
    assert res.status_code == 200
    data = res.get_json()
    assert data['state'] == 'draft'
    assert data['origin'] == 'matching:participant-1:2'
    assert len(data['terms']) == 2
    assert all(not t['signed_by_all'] for t in data['terms'])
    assert data['can_activate'] is False
    assert any(b['code'] == 'DRAFT_NOT_SUBMITTED' for b in data['blockers'])


def test_cycle_identity_not_for_others(client):
    """Ola 3A.1: nadie firma el tramo de otro (solo las partes caminan)."""
    cid = _make_draft(client)

    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 3))
    assert res.status_code == 403
    assert res.get_json()['code'] == 'CYCLE_NOT_PARTICIPANT'


def test_cycle_protected_requires_paraphrase(client, monkeypatch):
    """Escalera de equidad: un perfil asistido firma solo con sus palabras."""
    import app.contracts_bp as cb

    # Oráculo disponible: así la paráfrasis queda aislada como única puerta.
    # El gate de protección vive en contracts_bp: se parchea su namespace.
    class FakeOracle:
        def is_available(self):
            return True

        def critique(self, contract_id, contract_data):
            return type('R', (), {
                'valid': True, 'issues': [], 'recommendations': [],
                'reasoning': 'coherente',
            })()

    monkeypatch.setattr(cb, 'LiveOracle', lambda: FakeOracle())

    cid = _make_draft(client)

    # Luis (id 2) declara perfil assisted
    res = client.post('/protection/profile', headers=auth(client, 2), json={
        'level': 'assisted',
    })
    assert res.status_code == 200

    # Sin paráfrasis → bloqueado (derecho a la comprensión)
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 2), json={})
    assert res.status_code == 400
    assert res.get_json()['code'] == 'PROTECTION_PARAPHRASE_REQUIRED'

    # Con sus propias palabras → su tramo fluye (falta el de Ana)
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 2), json={
        'paraphrase': 'yo prometo acompañar a Ana en sus trámites con calma',
    })
    assert res.status_code in (200, 202)
    assert res.get_json()['activated'] is False

    # Ana (perfil estándar) camina su tramo → activación
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 1), json={})
    assert res.status_code == 200
    assert res.get_json()['activated'] is True

    # La paráfrasis quedó registrada (T13: derecho a la comprensión)
    with client.application.app_context():
        db = get_db()
        row = db.execute(
            "SELECT paraphrase FROM maxo_contract_term_approvals WHERE contract_id = ? AND participant_id = 'user-2' LIMIT 1",
            (cid,),
        ).fetchone()
        assert row is not None and 'acompañar a Ana' in row['paraphrase']


def test_cycle_protected_requires_oracle(client):
    """Assisted + sin oráculo en vivo: la firma se bloquea (sin degradación)."""
    cid = _make_draft(client)

    client.post('/protection/profile', headers=auth(client, 1), json={'level': 'assisted'})

    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 1), json={
        'paraphrase': 'yo prometo ayudar a Luis con lo que necesita',
    })
    assert res.status_code == 503
    assert res.get_json()['code'] == 'PROTECTION_ORACLE_REQUIRED'


def test_cycle_second_party_cannot_activate_alone(client):
    """Sin la firma de la otra parte no hay activación (término por término)."""
    cid = _make_draft(client)

    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 1), json={})
    assert res.get_json()['state'] == 'pending'

    # Ana intenta activar de nuevo: ya firmó todo; falta Luis
    res = client.post(f'/contracts/{cid}/cycle', headers=auth(client, 1), json={})
    data = res.get_json()
    assert data['activated'] is False
    assert data['signed_terms'] == []
    assert data['activation_blocked'] is not None
    assert data['activation_blocked']['code'] == 'TERMS_UNACCEPTED'


def test_cycle_requires_auth(client):
    res = client.post('/contracts/cualquiera/cycle', json={})
    assert res.status_code == 401
