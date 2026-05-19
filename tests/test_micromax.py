import json
import sqlite3
import tempfile
import os
import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.utils import init_db
from app.jwt_utils import create_token
from app.micromax import init_micromax_tables

@pytest.fixture
def client():
    """Create test client with temporary database."""
    db_fd, db_path = tempfile.mkstemp(prefix="test_micromax_", suffix=".db")
    os.close(db_fd)

    app = create_app(db_path=db_path)
    app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})

    with app.app_context():
        init_db()
        init_micromax_tables(app)

        # Add test users
        db = sqlite3.connect(db_path)
        db.execute(
            "INSERT INTO users (id, email, name, alias, password_hash) VALUES (?, ?, ?, ?, ?)",
            (1, "alice@example.com", "Alice", "alice", generate_password_hash("Password1"))
        )
        db.execute(
            "INSERT INTO users (id, email, name, alias, password_hash) VALUES (?, ?, ?, ?, ?)",
            (2, "bob@example.com", "Bob", "bob", generate_password_hash("Password1"))
        )
        db.commit()
        db.close()

    with app.test_client() as client:
        yield client

    try:
        os.unlink(db_path)
    except OSError:
        pass

@pytest.fixture
def auth_headers():
    def _headers(user_id, email, is_admin=0):
        token = create_token({"user_id": user_id, "email": email, "is_admin": is_admin})
        return {"Authorization": f"Bearer {token}"}
    return _headers

def test_micromax_flow(client, auth_headers):
    # 1. Get household (should return None/empty)
    res = client.get("/api/micromax/household", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    data = res.get_json()
    assert data["household"] is None

    # 2. Create household
    res = client.post(
        "/api/micromax/household",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({"name": "Casa de Alice"}),
        content_type="application/json"
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["household"]["name"] == "Casa de Alice"
    invite_code = data["household"]["invite_code"]
    assert invite_code is not None

    # 3. Bob joins household
    res = client.post(
        "/api/micromax/household/join",
        headers=auth_headers(2, "bob@example.com"),
        data=json.dumps({"invite_code": invite_code}),
        content_type="application/json"
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["household"]["name"] == "Casa de Alice"
    assert data["member"]["name"] == "Bob"

    # 4. Get household (should now show both)
    res = client.get("/api/micromax/household", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["members"]) == 2

    # 5. Save config for Alice
    res = client.post(
        "/api/micromax/member/config",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({
            "monthly_income": 1000,
            "work_hours": 40,
            "travel_hours": 5,
            "sleep_hours": 56
        }),
        content_type="application/json"
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["monthly_income"] == 1000

    # 6. Save safety survey for Alice (all false = score 0)
    res = client.post(
        "/api/micromax/safety-survey",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({
            "answers": {
                "q1": False,
                "q2": False,
                "q3": False,
                "q4": False,
                "q5": False,
                "q6": False
            }
        }),
        content_type="application/json"
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["score"] == 0
    assert not data["blocked"]

    # 7. Log CDD task for Alice
    res = client.post(
        "/api/micromax/cdd",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({
            "task_name": "Lavar platos",
            "duration_hours": 1.5,
            "effort_factor": 1.2,
            "mental_factor": 1.1,
            "scope_factor": 1.0,
            "attention_factor": 1.0,
            "fragmentation_factor": 1.0,
            "loneliness_factor": 1.0
        }),
        content_type="application/json"
    )
    assert res.status_code == 201
    data = res.get_json()
    # 1.5 * (1.2 * 1.1 * 1.0) * (1.0 * 1.0 * 1.0) = 1.5 * 1.32 = 1.98 VHV
    assert data["calculated_vhv"] == 1.98

    # 8. Get CDD logs for Alice
    res = client.get("/api/micromax/cdd", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["task_name"] == "Lavar platos"

    # 9. Get dashboard
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    data = res.get_json()
    assert "three_accounts" in data
    assert "toxicity" in data
    assert "safety_survey" in data

    # 10. Log an audit
    res = client.post(
        "/api/micromax/audit",
        headers=auth_headers(1, "alice@example.com"),
        data=json.dumps({
            "audit_date": "2026-05-19",
            "conflicts_count": 1,
            "weapon_count": 0,
            "accusations_count": 0,
            "threats_count": 0,
            "s1_hours": 0.0,
            "s2_score": 1.0,
            "s3_score": 1.0,
            "s4_score": 1.0,
            "s5_score": 1.0,
            "duration_weeks": 4
        }),
        content_type="application/json"
    )
    assert res.status_code == 201

    # 11. Verify toxicity calculation on dashboard
    res = client.get("/api/micromax/dashboard", headers=auth_headers(1, "alice@example.com"))
    assert res.status_code == 200
    data = res.get_json()
    # Conflicts = 1, baseline = 2. ICE = 1/2 * (1 + 0) = 0.5
    assert data["toxicity"]["ice"] == 0.5
