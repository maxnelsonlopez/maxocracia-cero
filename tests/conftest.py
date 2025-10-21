import os
import pytest
from app import create_app
from app.utils import init_db
import tempfile
import sqlite3
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    # Set testing config
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test-secret-key-123',
        'WTF_CSRF_ENABLED': False
    })

    # Create the database and load test data
    with app.app_context():
        init_db()
        
        # Add test user
        db = sqlite3.connect(db_path)
        db.execute(
            'INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
            ('test@example.com', 'Test User', generate_password_hash('test-password'))
        )
        db.commit()
        db.close()

    yield app

    # Clean up the temporary database
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with authentication."""
    # Login first
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'test-password'
    })
    assert response.status_code == 200
    token = response.get_json().get('token')
    
    # Set the token in the client
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client
