import pytest
import json
import os
from decimal import Decimal

os.environ['SECRET_KEY'] = 'test-secret'

from app import create_app
from app.utils import get_db
import tempfile

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db = get_db()
            with open('app/schema.sql', 'r') as f:
                db.executescript(f.read())
            
            # Crear usuarios de prueba
            db.execute("INSERT INTO users (id, email, name, password_hash) VALUES (1, 'test@example.com', 'Test User', 'hash')")
            db.execute("INSERT INTO users (id, email, name, password_hash) VALUES (2, 'bob@example.com', 'Bob', 'hash')")
            db.commit()
            
        yield client

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def auth_header(client):
    from app.jwt_utils import create_token
    token = create_token({'user_id': 1})
    return {'Authorization': f'Bearer {token}'}

def test_validate_graph_valid_simple(client, auth_header):
    """Test validador de grafo con conexiones válidas y complejidad simple."""
    payload = {
        "nodes": [
            {"id": "start", "type": "input", "data": {"label": "Start"}},
            {"id": "action-1", "type": "action", "data": {"label": "Lavar platos", "vhvCost": 1.5}},
            {"id": "recip-1", "type": "reciprocity", "data": {"label": "Pagar 1.5"}}
        ],
        "edges": [
            {"source": "start", "target": "action-1"},
            {"source": "action-1", "target": "recip-1"}
        ],
        "duration": 60
    }
    
    res = client.post('/contracts/validate_graph', headers=auth_header, json=payload)
    assert res.status_code == 200
    data = res.get_json()
    
    assert data["valid"] is True
    # Peso = (0 * 2) + (1.5 * 5) + (60 / 30) = 9.5
    assert abs(data["weight"] - 9.5) < 0.0001
    assert data["ux_signature_type"] == "simple"
    assert data["total_vhv"]["t"] == 1.5

def test_validate_graph_invalid_axiom_t9(client, auth_header):
    """Test validador de grafo violando el axioma T9 de Reciprocidad Justa."""
    payload = {
        "nodes": [
            {"id": "start", "type": "input", "data": {"label": "Start"}},
            {"id": "action-1", "type": "action", "data": {"label": "Lavar platos", "vhvCost": 1.5}}
        ],
        "edges": [
            {"source": "start", "target": "action-1"}
        ],
        "duration": 30
    }
    
    res = client.post('/contracts/validate_graph', headers=auth_header, json=payload)
    assert res.status_code == 200
    data = res.get_json()
    
    assert data["valid"] is False
    # Debería contener un resultado que indique el fallo en T9
    t9_failures = [r for r in data["results"] if r["axiom"] == "T9" and not r["is_valid"]]
    assert len(t9_failures) == 1
    assert "no está conectada a ningún bloque de Reciprocidad" in t9_failures[0]["message"]

def test_validate_graph_rigorous_complexity(client, auth_header):
    """Test validador de grafo con peso alto que requiere firma rigurosa."""
    payload = {
        "nodes": [
            {"id": "start", "type": "input", "data": {"label": "Start"}},
            {"id": "cond-1", "type": "condition", "data": {"label": "Cond 1"}},
            {"id": "cond-2", "type": "condition", "data": {"label": "Cond 2"}},
            {"id": "cond-3", "type": "condition", "data": {"label": "Cond 3"}},
            {"id": "action-1", "type": "action", "data": {"label": "Super Acción", "vhvCost": 10.0}},
            {"id": "recip-1", "type": "reciprocity", "data": {"label": "Súper Reciprocidad"}}
        ],
        "edges": [
            {"source": "start", "target": "cond-1"},
            {"source": "cond-1", "target": "cond-2"},
            {"source": "cond-2", "target": "cond-3"},
            {"source": "cond-3", "target": "action-1"},
            {"source": "action-1", "target": "recip-1"}
        ],
        "duration": 180
    }
    
    res = client.post('/contracts/validate_graph', headers=auth_header, json=payload)
    assert res.status_code == 200
    data = res.get_json()
    
    assert data["valid"] is True
    # Peso = (3 * 2) + (10 * 5) + (180 / 30) = 6 + 50 + 6 = 62.0
    assert abs(data["weight"] - 62.0) < 0.0001
    assert data["ux_signature_type"] == "rigorous"
