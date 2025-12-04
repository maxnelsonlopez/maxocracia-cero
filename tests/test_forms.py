"""
Tests for Forms System - Backend and API

Tests for:
- FormsManager business logic
- Forms API endpoints
- Database schema
"""

import json
import pytest
from datetime import datetime


class TestFormsManager:
    """Test FormsManager business logic."""

    def test_register_participant_success(self, app, client):
        """Test successful participant registration."""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@testuser",
            "city": "Bogotá",
            "neighborhood": "Chapinero",
            "personal_values": "Honestidad, colaboración",
            "offer_categories": ["conocimiento", "tiempo"],
            "offer_description": "Puedo enseñar programación",
            "offer_human_dimensions": ["crecimiento_aprendizaje"],
            "need_categories": ["alimentacion"],
            "need_description": "Necesito ayuda con mercado",
            "need_urgency": "Media",
            "need_human_dimensions": ["prosperidad_recursos"],
        }

        response = client.post(
            "/forms/participant", data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["success"] is True
        assert "participant_id" in json_data

    def test_register_participant_missing_field(self, app, client):
        """Test participant registration with missing required field."""
        data = {
            "name": "Test User",
            "email": "test2@example.com",
            # Missing many required fields
        }

        response = client.post(
            "/forms/participant", data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["success"] is False
        assert "error" in json_data

    def test_register_participant_duplicate_email(self, app, client):
        """Test participant registration with duplicate email."""
        data = {
            "name": "Test User",
            "email": "duplicate@example.com",
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@testuser",
            "city": "Bogotá",
            "neighborhood": "Chapinero",
            "personal_values": "Honestidad",
            "offer_categories": ["tiempo"],
            "offer_description": "Puedo ayudar",
            "offer_human_dimensions": ["conexion_social"],
            "need_categories": ["alimentacion"],
            "need_description": "Necesito ayuda",
            "need_urgency": "Baja",
            "need_human_dimensions": ["prosperidad_recursos"],
        }

        # First registration
        response1 = client.post(
            "/forms/participant", data=json.dumps(data), content_type="application/json"
        )
        assert response1.status_code == 201

        # Duplicate registration
        response2 = client.post(
            "/forms/participant", data=json.dumps(data), content_type="application/json"
        )
        assert response2.status_code == 400
        json_data = response2.get_json()
        assert "email ya está registrado" in json_data["error"]


class TestFormsAPI:
    """Test Forms API endpoints."""

    def test_get_participants_requires_auth(self, app, client):
        """Test that getting participants requires authentication."""
        response = client.get("/forms/participants")
        assert response.status_code == 401

    def test_get_participants_with_auth(self, app, client, auth_headers):
        """Test getting participants with authentication."""
        response = client.get("/forms/participants", headers=auth_headers)
        assert response.status_code == 200
        json_data = response.get_json()
        assert "participants" in json_data
        assert "count" in json_data

    def test_register_exchange_requires_auth(self, app, client):
        """Test that registering exchange requires authentication."""
        data = {
            "interchange_id": "INT-001",
            "date": "2025-12-03",
            "giver_id": 1,
            "receiver_id": 2,
            "type": "alimentacion",
            "description": "Compartió comida",
            "urgency": "Alta",
            "impact_resolution_score": 5,
            "reciprocity_status": "unidirectional",
        }

        response = client.post(
            "/forms/exchange", data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == 401

    def test_register_exchange_with_auth(self, app, client, auth_headers):
        """Test registering exchange with authentication."""
        data = {
            "interchange_id": "INT-TEST-001",
            "date": "2025-12-03",
            "giver_id": 1,
            "receiver_id": 2,
            "type": "alimentacion",
            "description": "Compartió comida",
            "urgency": "Alta",
            "uth_hours": 2.5,
            "impact_resolution_score": 5,
            "reciprocity_status": "unidirectional",
            "coordination_method": "max_direct",
        }

        response = client.post(
            "/forms/exchange",
            data=json.dumps(data),
            content_type="application/json",
            headers=auth_headers,
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["success"] is True
        assert "exchange_id" in json_data

    def test_register_followup_with_auth(self, app, client, auth_headers):
        """Test registering follow-up with authentication."""
        # First create a participant
        participant_data = {
            "name": "Follow-up Test User",
            "email": "followup@example.com",
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@followuptest",
            "city": "Bogotá",
            "neighborhood": "Usaquén",
            "personal_values": "Solidaridad",
            "offer_categories": ["tiempo"],
            "offer_description": "Puedo escuchar",
            "offer_human_dimensions": ["conexion_social"],
            "need_categories": ["alimentacion"],
            "need_description": "Necesito comida",
            "need_urgency": "Alta",
            "need_human_dimensions": ["prosperidad_recursos"],
        }

        participant_response = client.post(
            "/forms/participant",
            data=json.dumps(participant_data),
            content_type="application/json",
        )
        participant_id = participant_response.get_json()["participant_id"]

        # Now create follow-up
        followup_data = {
            "follow_up_date": "2025-12-03",
            "participant_id": participant_id,
            "follow_up_type": "routine_check",
            "current_situation": "La persona está mejor",
            "situation_change": "improved_slightly",
            "active_interchanges_status": "receiving_help",
            "follow_up_priority": "medium",
            "need_level": 3,
        }

        response = client.post(
            "/forms/follow-up",
            data=json.dumps(followup_data),
            content_type="application/json",
            headers=auth_headers,
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["success"] is True
        assert "followup_id" in json_data

    def test_dashboard_stats(self, app, client, auth_headers):
        """Test dashboard stats endpoint."""
        response = client.get("/forms/dashboard/stats", headers=auth_headers)

        assert response.status_code == 200
        json_data = response.get_json()
        assert "total_participants" in json_data
        assert "total_exchanges" in json_data
        assert "total_uth" in json_data

    def test_dashboard_alerts(self, app, client, auth_headers):
        """Test dashboard alerts endpoint."""
        response = client.get("/forms/dashboard/alerts", headers=auth_headers)

        assert response.status_code == 200
        json_data = response.get_json()
        assert "alerts" in json_data
        assert "count" in json_data

    def test_network_flow(self, app, client, auth_headers):
        """Test network flow endpoint."""
        response = client.get("/forms/dashboard/network", headers=auth_headers)

        assert response.status_code == 200
        json_data = response.get_json()
        assert "top_givers" in json_data
        assert "top_receivers" in json_data
        assert "hub_nodes" in json_data


class TestDatabaseSchema:
    """Test database schema for forms tables."""

    def test_participants_table_exists(self, app):
        """Test that participants table exists with correct schema."""
        from app.utils import get_db

        with app.app_context():
            db = get_db()
            cursor = db.cursor()

            # Check table exists
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='participants'
            """
            )
            assert cursor.fetchone() is not None

            # Check columns
            cursor.execute("PRAGMA table_info(participants)")
            columns = {row[1] for row in cursor.fetchall()}

            required_columns = {
                "id",
                "name",
                "email",
                "city",
                "neighborhood",
                "offer_description",
                "need_description",
                "need_urgency",
                "created_at",
                "status",
            }
            assert required_columns.issubset(columns)

    def test_follow_ups_table_exists(self, app):
        """Test that follow_ups table exists with correct schema."""
        from app.utils import get_db

        with app.app_context():
            db = get_db()
            cursor = db.cursor()

            # Check table exists
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='follow_ups'
            """
            )
            assert cursor.fetchone() is not None

            # Check columns
            cursor.execute("PRAGMA table_info(follow_ups)")
            columns = {row[1] for row in cursor.fetchall()}

            required_columns = {
                "id",
                "follow_up_date",
                "participant_id",
                "follow_up_type",
                "current_situation",
                "follow_up_priority",
                "created_at",
            }
            assert required_columns.issubset(columns)


# Fixtures


@pytest.fixture
def auth_headers(app, client):
    """Create authentication headers for testing."""
    # Register a test user
    register_data = {
        "email": "testauth@example.com",
        "password": "TestPassword123!",
        "name": "Test Auth User",
    }

    client.post(
        "/auth/register",
        data=json.dumps(register_data),
        content_type="application/json",
    )

    # Login
    login_data = {"email": "testauth@example.com", "password": "TestPassword123!"}

    response = client.post(
        "/auth/login", data=json.dumps(login_data), content_type="application/json"
    )

    token = response.get_json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
