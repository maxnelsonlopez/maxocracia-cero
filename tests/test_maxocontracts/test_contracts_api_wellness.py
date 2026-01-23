import pytest
import json
from decimal import Decimal

import os
os.environ['SECRET_KEY'] = 'test-secret'

# Import app creation
from app import create_app
from app.utils import get_db

import tempfile

@pytest.fixture
def client():
    # Create a temporary file to use as the database
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            # Initialize schema
            db = get_db()
            with open('app/schema.sql', 'r') as f:
                db.executescript(f.read())
            
            # Create a test user
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'test@example.com', 'Test User', 'hash')"
            )
            # Create a second user for the participant
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (2, 'bob@example.com', 'Bob', 'hash')"
            )
            db.commit()
            
        yield client

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def auth_header(client):
    # Mock token generation or just bypass if testing logic, 
    # but since app uses @token_required, we need to mock it or generate a valid token.
    # For this specific test, we can mock the jwt_utils or generate a token if the secret is known.
    # Alternatively, we can use the 'login' endpoint if it exists and works in test mode.
    # Given the previous context, let's try to generate a token or mock.
    
    # Simpler: Import create_access_token if available
    from app.jwt_utils import create_token
    token = create_token({'user_id': 1})
    return {'Authorization': f'Bearer {token}'}

def test_add_participant_wellness_parameter(client, auth_header):
    """Test using the new 'wellness' parameter."""
    
    # 1. Create a contract
    res = client.post('/contracts/', headers=auth_header, json={
        'contract_id': 'contract-wellness',
        'civil_description': 'Test Contract'
    })
    assert res.status_code == 201
    
    # 2. Add participant using 'wellness'
    res = client.post('/contracts/contract-wellness/participants', headers=auth_header, json={
        'user_id': 2,
        'wellness': 1.5
    })
    
    # Should succeed
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    # The API returns float, check mostly equal
    assert abs(data['wellness'] - 1.5) < 0.0001


def test_add_participant_gamma_legacy(client, auth_header):
    """Test using the legacy 'gamma' parameter."""
    
    # 1. Create a contract
    res = client.post('/contracts/', headers=auth_header, json={
        'contract_id': 'contract-gamma',
        'civil_description': 'Test Contract Legacy'
    })
    assert res.status_code == 201
    
    # 2. Add participant using 'gamma'
    res = client.post('/contracts/contract-gamma/participants', headers=auth_header, json={
        'user_id': 2,
        'gamma': 1.2
    })
    
    # Should succeed
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert abs(data['wellness'] - 1.2) < 0.0001
