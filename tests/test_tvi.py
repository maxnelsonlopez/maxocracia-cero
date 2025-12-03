import sqlite3

import pytest

from app import create_app
from app.tvi import TVIManager


@pytest.fixture
def app(db_path):
    app = create_app(db_path=db_path)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def tvi_manager(app):
    # Initialize DB with schema
    with app.app_context():
        db = sqlite3.connect(":memory:")
        with open("app/schema.sql") as f:
            db.executescript(f.read())
        # We need to use a persistent DB for the manager in tests if not using the app's db connection handling
        # But TVIManager creates its own connection.
        # For testing, we can subclass or mock, or just use a file db.
        # Let's use a temporary file db for the manager tests.
        pass
    return TVIManager(
        db_path=":memory:"
    )  # This won't work well because each connection is new DB


@pytest.fixture
def db_path(tmp_path):
    d = tmp_path / "test_tvi.db"
    # Init schema
    conn = sqlite3.connect(str(d))
    with open("app/schema.sql") as f:
        conn.executescript(f.read())
    # Create a user
    conn.execute(
        "INSERT INTO users (email, password_hash, name) VALUES ('test@test.com', 'pass', 'Test User')"
    )
    conn.commit()
    conn.close()
    return str(d)


def test_tvi_log_and_overlap(db_path):
    manager = TVIManager(db_path=db_path)
    user_id = 1

    # Log first entry
    start1 = "2025-01-01T10:00:00"
    end1 = "2025-01-01T11:00:00"
    entry1 = manager.log_tvi(user_id, start1, end1, "WORK", "First block")
    assert entry1["id"] is not None

    # Log non-overlapping entry
    start2 = "2025-01-01T11:00:00"  # Starts exactly when previous ends
    end2 = "2025-01-01T12:00:00"
    entry2 = manager.log_tvi(user_id, start2, end2, "LEISURE", "Second block")
    assert entry2["id"] is not None

    # Log overlapping entry (partial overlap start)
    start3 = "2025-01-01T10:30:00"
    end3 = "2025-01-01T11:30:00"
    with pytest.raises(ValueError, match="TVI Overlap Detected"):
        manager.log_tvi(user_id, start3, end3, "WASTE", "Overlap")

    # Log overlapping entry (contained)
    start4 = "2025-01-01T10:15:00"
    end4 = "2025-01-01T10:45:00"
    with pytest.raises(ValueError, match="TVI Overlap Detected"):
        manager.log_tvi(user_id, start4, end4, "WASTE", "Overlap Contained")

    # Log overlapping entry (enveloping)
    start5 = "2025-01-01T09:00:00"
    end5 = "2025-01-01T13:00:00"
    with pytest.raises(ValueError, match="TVI Overlap Detected"):
        manager.log_tvi(user_id, start5, end5, "WASTE", "Overlap Enveloping")


def test_ccp_calculation(db_path):
    manager = TVIManager(db_path=db_path)
    user_id = 1

    # 8 hours Maintenance (Sleep)
    manager.log_tvi(
        user_id, "2025-01-01T00:00:00", "2025-01-01T08:00:00", "MAINTENANCE"
    )

    # 8 hours Work (Investment)
    manager.log_tvi(user_id, "2025-01-01T09:00:00", "2025-01-01T17:00:00", "INVESTMENT")

    # 4 hours Leisure
    manager.log_tvi(user_id, "2025-01-01T18:00:00", "2025-01-01T22:00:00", "LEISURE")

    # 2 hours Waste
    manager.log_tvi(user_id, "2025-01-01T22:00:00", "2025-01-02T00:00:00", "WASTE")

    # Total: 24h (gaps are not counted in total_seconds of entries, but formula uses total entries duration)
    # Wait, the formula is: (Investment + Leisure) / (Total - Maintenance)
    # Total here refers to the total time *recorded* or total time *available*?
    # The implementation uses total time *recorded*.

    stats = manager.calculate_ccp(user_id)

    # Total recorded: 8+8+4+2 = 22 hours (there was a 1h gap 08-09 and 1h gap 17-18)
    # Maintenance: 8h
    # Discretionary: 22 - 8 = 14h
    # Coherent (Inv + Lei): 8 + 4 = 12h
    # CCP = 12 / 14 = 0.8571

    assert stats["total_seconds"] == 22 * 3600
    assert stats["ccp"] == pytest.approx(0.8571, 0.0001)


def test_api_endpoints(client, db_path, monkeypatch):
    # Patch the TVIManager instance in the blueprint to use the test db
    from app.tvi_bp import tvi_manager

    tvi_manager.db_path = db_path

    # Login
    # We need to register first or insert user (already inserted in fixture)
    # We need to generate a token.
    # Let's just mock g.user_id for simplicity if we can, but login_required decorator checks token.
    # So we need a valid token.

    # Register a user via API to get token
    auth_resp = client.post(
        "/auth/register",
        json={
            "email": "api_test@test.com",
            "password": "Password123",
            "name": "API User",
        },
    )
    assert auth_resp.status_code == 201, f"Register failed: {auth_resp.json}"
    token = auth_resp.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Post TVI
    resp = client.post(
        "/tvi",
        json={
            "start_time": "2025-01-02T10:00:00",
            "end_time": "2025-01-02T11:00:00",
            "category": "WORK",
        },
        headers=headers,
    )
    assert resp.status_code == 201

    # Get TVI
    resp = client.get("/tvi", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]["category"] == "WORK"

    # Get Stats
    resp = client.get("/tvi/stats", headers=headers)
    assert resp.status_code == 200
    assert "ccp" in resp.json
