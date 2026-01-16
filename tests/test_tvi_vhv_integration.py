"""
Tests for TVI-VHV integration functionality.

Tests the integration between Tiempo Vital Indexado (TVI) and
Vector de Huella Vital (VHV) calculations.
"""

import sqlite3
from datetime import datetime, timedelta

import pytest

from app import create_app
from app.tvi import TVIManager


@pytest.fixture
def app(db_path):
    app = create_app(db_path=db_path)
    app.config.update({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")  # Create fresh DB for each test
def db_path(tmp_path):
    d = tmp_path / "test_tvi_vhv.db"
    conn = sqlite3.connect(str(d))
    with open("app/schema.sql") as f:
        conn.executescript(f.read())

    # Create a user
    from werkzeug.security import generate_password_hash

    conn.execute(
        "INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, ?)",
        (1, "test@example.com", "Test User", generate_password_hash("Password1")),
    )

    # Create VHV parameters
    conn.execute(
        """
        INSERT INTO vhv_parameters (alpha, beta, gamma, delta, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (100.0, 2000.0, 1.0, 100.0, "Test parameters"),
    )

    conn.commit()
    conn.close()
    return str(d)


@pytest.fixture
def auth_token(client):
    """Get authentication token for test user."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "Password1"},
    )
    assert response.status_code == 200
    data = response.get_json()
    return data["access_token"]  # Use 'access_token' not 'token'


def test_calculate_ttvi_from_tvis_empty(app, db_path):
    """Test calculating TTVI when user has no TVI entries."""
    with app.app_context():
        manager = TVIManager()
        result = manager.calculate_ttvi_from_tvis(user_id=1)

    assert result["direct_hours"] == 0.0
    assert result["inherited_hours"] == 0.0
    assert result["future_hours"] == 0.0
    assert result["total_hours"] == 0.0
    assert result["breakdown_by_category"] == {}


def test_calculate_ttvi_from_tvis_with_work(app, db_path):
    """Test calculating TTVI with WORK category entries."""
    with app.app_context():
        manager = TVIManager()

        # Add WORK entries
        now = datetime.now()
        manager.log_tvi(
            user_id=1,
            start_time=(now - timedelta(hours=2)).isoformat(),
            end_time=(now - timedelta(hours=1)).isoformat(),
            category="WORK",
            description="Test work",
        )
        manager.log_tvi(
            user_id=1,
            start_time=(now - timedelta(hours=1)).isoformat(),
            end_time=now.isoformat(),
            category="WORK",
            description="More work",
        )

        result = manager.calculate_ttvi_from_tvis(user_id=1)

    assert result["direct_hours"] == 2.0  # 2 hours of WORK
    assert result["inherited_hours"] == 0.0
    assert result["future_hours"] == 0.0
    assert result["total_hours"] == 2.0
    assert result["breakdown_by_category"]["WORK"] == 2.0


def test_calculate_ttvi_from_tvis_with_investment(app, db_path):
    """Test calculating TTVI with INVESTMENT category entries."""
    with app.app_context():
        manager = TVIManager()

        now = datetime.now()
        manager.log_tvi(
            user_id=1,
            start_time=(now - timedelta(hours=3)).isoformat(),
            end_time=(now - timedelta(hours=1)).isoformat(),
            category="INVESTMENT",
            description="Learning",
        )

        result = manager.calculate_ttvi_from_tvis(user_id=1)

    assert result["direct_hours"] == 2.0  # INVESTMENT counts as direct
    assert result["breakdown_by_category"]["INVESTMENT"] == 2.0


def test_calculate_ttvi_from_tvis_with_date_filter(app, db_path):
    """Test calculating TTVI with date range filter."""
    with app.app_context():
        manager = TVIManager()

        now = datetime.now()
        yesterday = now - timedelta(days=1)

        # Add entry from yesterday
        manager.log_tvi(
            user_id=1,
            start_time=(yesterday - timedelta(hours=1)).isoformat(),
            end_time=yesterday.isoformat(),
            category="WORK",
            description="Old work",
        )

        # Add entry from today
        manager.log_tvi(
            user_id=1,
            start_time=(now - timedelta(hours=1)).isoformat(),
            end_time=now.isoformat(),
            category="WORK",
            description="Today work",
        )

        # Filter only today
        result = manager.calculate_ttvi_from_tvis(
            user_id=1, start_date=now.date().isoformat()
        )

    assert result["direct_hours"] == 1.0  # Only today's entry


def test_calculate_ttvi_from_tvis_with_category_filter(app, db_path):
    """Test calculating TTVI with category filter."""
    with app.app_context():
        manager = TVIManager()

        now = datetime.now()
        manager.log_tvi(
            user_id=1,
            start_time=(now - timedelta(hours=2)).isoformat(),
            end_time=(now - timedelta(hours=1)).isoformat(),
            category="WORK",
            description="Work",
        )
        manager.log_tvi(
            user_id=1,
            start_time=(now - timedelta(hours=1)).isoformat(),
            end_time=now.isoformat(),
            category="LEISURE",
            description="Leisure",
        )

        # Filter only WORK
        result = manager.calculate_ttvi_from_tvis(user_id=1, category_filter="WORK")

    assert result["direct_hours"] == 1.0  # Only WORK counts as direct
    assert "LEISURE" not in result["breakdown_by_category"]


def test_vhv_calculate_from_tvi_endpoint(client, auth_token, db_path):
    """Test the /vhv/calculate-from-tvi endpoint."""
    # First, add some TVI entries
    now = datetime.now()
    tvi_data = {
        "start_time": (now - timedelta(hours=2)).isoformat(),
        "end_time": (now - timedelta(hours=1)).isoformat(),
        "category": "WORK",
        "description": "Test work for VHV",
    }

    response = client.post(
        "/tvi",
        json=tvi_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201

    # Now calculate VHV from TVI
    vhv_data = {
        "v_organisms_affected": 0.001,
        "v_consciousness_factor": 0.9,
        "v_suffering_factor": 1.1,
        "v_abundance_factor": 0.0006,
        "v_rarity_factor": 1.0,
        "r_minerals_kg": 0.1,
        "r_water_m3": 0.05,
        "r_petroleum_l": 0.0,
        "r_land_hectares": 0.0,
        "r_frg_factor": 1.0,
        "r_cs_factor": 1.0,
    }

    response = client.post(
        "/vhv/calculate-from-tvi",
        json=vhv_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "vhv" in data
    assert "maxo_price" in data
    assert "breakdown" in data
    assert "ttvi_breakdown" in data

    # Check TTVI breakdown
    ttvi = data["ttvi_breakdown"]
    assert ttvi["direct_hours"] == 1.0  # 1 hour of WORK
    assert "breakdown_by_category" in ttvi
    assert ttvi["breakdown_by_category"]["WORK"] == 1.0


def test_vhv_calculate_from_tvi_with_overrides(client, auth_token, db_path):
    """Test /vhv/calculate-from-tvi with inherited/future hours overrides."""
    # Add TVI entry
    now = datetime.now()
    tvi_data = {
        "start_time": (now - timedelta(hours=1)).isoformat(),
        "end_time": now.isoformat(),
        "category": "WORK",
    }

    client.post(
        "/tvi",
        json=tvi_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Calculate with overrides
    vhv_data = {
        "v_organisms_affected": 0.001,
        "v_consciousness_factor": 0.9,
        "v_suffering_factor": 1.1,
        "v_abundance_factor": 0.0006,
        "v_rarity_factor": 1.0,
        "r_minerals_kg": 0.1,
        "r_water_m3": 0.05,
        "r_petroleum_l": 0.0,
        "r_land_hectares": 0.0,
        "r_frg_factor": 1.0,
        "r_cs_factor": 1.0,
        "inherited_hours_override": 0.5,
        "future_hours_override": 0.2,
    }

    response = client.post(
        "/vhv/calculate-from-tvi",
        json=vhv_data,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.get_json()

    # Check that overrides were used
    ttvi = data["ttvi_breakdown"]
    assert ttvi["inherited_hours"] == 0.5
    assert ttvi["future_hours"] == 0.2


def test_vhv_calculate_from_tvi_requires_auth(client, db_path):
    """Test that /vhv/calculate-from-tvi requires authentication."""
    vhv_data = {
        "v_organisms_affected": 0.001,
        "v_consciousness_factor": 0.9,
        "v_suffering_factor": 1.1,
        "v_abundance_factor": 0.0006,
        "v_rarity_factor": 1.0,
        "r_minerals_kg": 0.1,
        "r_water_m3": 0.05,
        "r_petroleum_l": 0.0,
        "r_land_hectares": 0.0,
        "r_frg_factor": 1.0,
        "r_cs_factor": 1.0,
    }

    response = client.post("/vhv/calculate-from-tvi", json=vhv_data)
    assert response.status_code == 401


def test_vhv_calculate_from_tvi_missing_fields(client, auth_token, db_path):
    """Test /vhv/calculate-from-tvi with missing required fields."""
    response = client.post(
        "/vhv/calculate-from-tvi",
        json={"v_organisms_affected": 0.001},  # Missing other fields
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field" in data["error"]
