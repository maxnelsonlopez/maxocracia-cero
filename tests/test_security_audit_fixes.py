import json
import pytest
from datetime import datetime, timedelta, timezone


def test_admin_interface_protection(client):
    """Verify that /admin is protected and redirects unauthenticated users."""
    response = client.get("/admin/")
    # Flask-Admin usually redirects to main or login if is_accessible returns False
    assert response.status_code in [302, 403]


def test_vhv_range_validation_hours(admin_client):
    """Verify that negative hours are rejected in VHV calculation."""
    data = {
        "name": "Invalid Product",
        "t_direct_hours": -1.0,
        "t_inherited_hours": 0,
        "t_future_hours": 0,
        "v_organisms_affected": 0,
        "v_consciousness_factor": 0,
        "v_suffering_factor": 1,
        "v_abundance_factor": 1,
        "v_rarity_factor": 1,
        "r_minerals_kg": 0,
        "r_water_m3": 0,
        "r_petroleum_l": 0,
        "r_land_hectares": 0,
        "r_frg_factor": 1,
        "r_cs_factor": 1,
    }
    response = admin_client.post("/vhv/calculate", json=data)
    assert response.status_code == 400
    assert "cannot be negative" in response.get_json()["error"]


def test_vhv_range_validation_suffering(admin_client):
    """Verify that suffering factor < 1 is rejected (Axiom violation)."""
    data = {
        "name": "Evil Product",
        "t_direct_hours": 1.0,
        "t_inherited_hours": 0,
        "t_future_hours": 0,
        "v_organisms_affected": 1,
        "v_consciousness_factor": 1,
        "v_suffering_factor": 0.5,  # INVALID: must be >= 1
        "v_abundance_factor": 1,
        "v_rarity_factor": 1,
        "r_minerals_kg": 0,
        "r_water_m3": 0,
        "r_petroleum_l": 0,
        "r_land_hectares": 0,
        "r_frg_factor": 1,
        "r_cs_factor": 1,
    }
    response = admin_client.post("/vhv/calculate", json=data)
    assert response.status_code == 400
    assert "suffering" in response.get_json()["error"].lower()


def test_balance_privacy(client, auth_client):
    """Verify that a user cannot see another user's balance."""
    # User 1 is logged in via auth_client (test@example.com, id=1 usually)
    # Let's try to query balance for user 2 (test2@example.com, id=2)
    response = auth_client.get("/maxo/2/balance")
    assert response.status_code == 403
    assert "forbidden" in response.get_json()["error"]


def test_admin_can_see_any_balance(admin_client):
    """Verify that admin can see any user's balance."""
    response = admin_client.get("/maxo/1/balance")
    assert response.status_code == 200
    assert "balance" in response.get_json()


def test_tvi_future_time_rejection(auth_client):
    """Verify that logging time in the future is rejected."""
    future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    now_time = datetime.now(timezone.utc).isoformat()

    data = {
        "start_time": now_time,
        "end_time": future_time,
        "category": "WORK",
        "description": "Playing with time machine",
    }
    response = auth_client.post("/tvi", json=data)
    assert response.status_code == 400
    assert "future" in response.get_json()["error"].lower()


def test_tvi_duration_limit(auth_client):
    """Verify that a single TVI entry cannot exceed 24 hours."""
    start = datetime.now(timezone.utc) - timedelta(days=2)
    end = start + timedelta(hours=25)

    data = {
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "category": "WORK",
        "description": "Super long shift",
    }
    response = auth_client.post("/tvi", json=data)
    assert response.status_code == 400
    assert "24 hours" in response.get_json()["error"]
