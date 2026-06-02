"""
Tests for participant CRUD actions (update and delete) in Forms system.
"""

import json
import pytest
from app.utils import get_db
from app.forms_manager import FormsManager


@pytest.fixture
def create_participant_helper(client):
    """Helper fixture to create a test participant."""
    def _create(email="test@example.com", name="Test Participant"):
        data = {
            "name": name,
            "email": email,
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@testparticipant",
            "city": "Bogotá",
            "neighborhood": "Chapinero",
            "personal_values": "Honestidad",
            "offer_categories": ["tiempo"],
            "offer_description": "Puedo ayudar en lo que sea",
            "offer_human_dimensions": ["conexion_social"],
            "need_categories": ["alimentacion"],
            "need_description": "Necesito comida",
            "need_urgency": "Media",
            "need_human_dimensions": ["prosperidad_recursos"],
        }
        response = client.post(
            "/forms/participant",
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == 201
        return response.get_json()["participant_id"]
    return _create


def test_update_participant_owner(app, client, auth_client, create_participant_helper):
    """Test updating a participant by the owner user."""
    # Participant created with test@example.com (matching auth_client)
    participant_id = create_participant_helper(email="test@example.com")

    update_data = {
        "need_urgency": "Alta",
        "need_description": "Necesito comida urgentemente",
        "offer_description": "Puedo ayudar con programación",
        "offer_categories": ["tiempo", "conocimiento"],
    }

    response = auth_client.put(
        f"/forms/participants/{participant_id}",
        data=json.dumps(update_data),
        content_type="application/json"
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True

    # Verify updates in database
    with app.app_context():
        manager = FormsManager(get_db())
        p = manager.get_participant(participant_id)
        assert p["need_urgency"] == "Alta"
        assert p["need_description"] == "Necesito comida urgentemente"
        assert p["offer_description"] == "Puedo ayudar con programación"
        assert p["offer_categories"] == ["tiempo", "conocimiento"]


def test_update_participant_non_owner_forbidden(app, client, auth, create_participant_helper):
    """Test that updating another user's participant record is forbidden."""
    # Participant created with admin's email or other email
    participant_id = create_participant_helper(email="other@example.com")

    # Login as standard user (test@example.com)
    response_login = auth.login()
    token = response_login.get_json()["access_token"]
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    update_data = {
        "need_urgency": "Alta"
    }

    # standard user test@example.com attempts to edit other@example.com's participant
    response = client.put(
        f"/forms/participants/{participant_id}",
        data=json.dumps(update_data),
        content_type="application/json"
    )

    assert response.status_code == 403
    assert "No tienes autorización" in response.get_json()["error"]


def test_update_participant_admin(app, admin_client, create_participant_helper):
    """Test that an administrator can update any participant."""
    participant_id = create_participant_helper(email="test@example.com")

    update_data = {
        "need_urgency": "Baja",
        "status": "paused"
    }

    response = admin_client.put(
        f"/forms/participants/{participant_id}",
        data=json.dumps(update_data),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.get_json()["success"] is True

    # Verify changes in DB
    with app.app_context():
        manager = FormsManager(get_db())
        p = manager.get_participant(participant_id)
        assert p["need_urgency"] == "Baja"
        assert p["status"] == "paused"


def test_update_participant_validation(app, auth_client, create_participant_helper):
    """Test validation constraints on update."""
    participant_id = create_participant_helper(email="test@example.com")

    # Invalid urgency
    response = auth_client.put(
        f"/forms/participants/{participant_id}",
        data=json.dumps({"need_urgency": "Inmediata"}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "Urgencia debe ser Alta, Media o Baja" in response.get_json()["error"]

    # Invalid status
    response = auth_client.put(
        f"/forms/participants/{participant_id}",
        data=json.dumps({"status": "deleted"}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "Estado debe ser active, inactive o paused" in response.get_json()["error"]


def test_delete_participant_non_owner_forbidden(app, client, auth, create_participant_helper):
    """Test that deleting another user's participant record is forbidden."""
    participant_id = create_participant_helper(email="other@example.com")

    # Login as standard user (test@example.com)
    response_login = auth.login()
    token = response_login.get_json()["access_token"]
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    response = client.delete(f"/forms/participants/{participant_id}")
    assert response.status_code == 403
    assert "No tienes autorización" in response.get_json()["error"]


def test_delete_participant_owner(app, auth_client, create_participant_helper):
    """Test that a participant owner can delete their own record."""
    participant_id = create_participant_helper(email="test@example.com")

    response = auth_client.delete(f"/forms/participants/{participant_id}")
    assert response.status_code == 200
    assert response.get_json()["success"] is True

    # Check that participant is gone from DB
    response_get = auth_client.get(f"/forms/participants/{participant_id}")
    assert response_get.status_code == 404


def test_delete_participant_admin(app, admin_client, create_participant_helper):
    """Test that an admin can delete any participant."""
    participant_id = create_participant_helper(email="test@example.com")

    response = admin_client.delete(f"/forms/participants/{participant_id}")
    assert response.status_code == 200
    assert response.get_json()["success"] is True

    # Check that participant is gone from DB
    response_get = admin_client.get(f"/forms/participants/{participant_id}")
    assert response_get.status_code == 404


def test_delete_participant_cascades(app, admin_client, create_participant_helper):
    """Test that deleting a participant deletes their follow-up records."""
    participant_id = create_participant_helper(email="test@example.com")

    # Create a follow-up for this participant
    followup_data = {
        "follow_up_date": "2026-05-22",
        "participant_id": participant_id,
        "follow_up_type": "routine_check",
        "current_situation": "Estable",
        "situation_change": "same",
        "active_interchanges_status": "none",
        "follow_up_priority": "low",
        "need_level": 1,
    }
    response_f = admin_client.post(
        "/forms/follow-up",
        data=json.dumps(followup_data),
        content_type="application/json"
    )
    assert response_f.status_code == 201
    followup_id = response_f.get_json()["followup_id"]

    # Verify follow-up exists
    response_get_f = admin_client.get(f"/forms/follow-ups")
    assert response_get_f.status_code == 200
    followups = response_get_f.get_json()["follow_ups"]
    assert any(f["id"] == followup_id for f in followups)

    # Delete participant
    response_del = admin_client.delete(f"/forms/participants/{participant_id}")
    assert response_del.status_code == 200

    # Verify follow-up is cascadingly deleted
    response_get_f2 = admin_client.get(f"/forms/follow-ups")
    assert response_get_f2.status_code == 200
    followups2 = response_get_f2.get_json()["follow_ups"]
    assert not any(f["id"] == followup_id for f in followups2)
