"""
Tests for Pulso Vital — Cohort Heartbeat endpoint.

Tests the aggregated /forms/pulse endpoint that combines
SDV community data, matching gaps, urgency alerts, and
dashboard stats into a single response.

Autor: Claude Opus (Anthropic)
"""

import json

import pytest


@pytest.fixture
def auth_headers(app, client):
    """Create authentication headers for testing."""
    register_data = {
        "email": "pulse_test@example.com",
        "password": "TestPassword123!",
        "name": "Pulse Test User",
    }

    client.post(
        "/auth/register",
        data=json.dumps(register_data),
        content_type="application/json",
    )

    login_data = {
        "email": "pulse_test@example.com",
        "password": "TestPassword123!",
    }

    response = client.post(
        "/auth/login",
        data=json.dumps(login_data),
        content_type="application/json",
    )

    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestPulsoVitalEndpoint:
    """Test the /forms/pulse aggregated endpoint."""

    def test_pulse_requires_auth(self, app, client):
        """Pulse endpoint requires authentication."""
        response = client.get("/forms/pulse")
        assert response.status_code == 401

    def test_pulse_returns_complete_structure(self, app, client, auth_headers):
        """Pulse endpoint returns all required sections."""
        response = client.get("/forms/pulse", headers=auth_headers)
        assert response.status_code == 200

        data = response.get_json()

        # Top-level sections
        assert "sdv" in data
        assert "gaps" in data
        assert "alerts" in data
        assert "stats" in data
        assert "timestamp" in data

    def test_pulse_sdv_structure(self, app, client, auth_headers):
        """SDV section has all required fields."""
        response = client.get("/forms/pulse", headers=auth_headers)
        data = response.get_json()
        sdv = data["sdv"]

        assert "average_overall" in sdv
        assert "dimensions" in sdv
        assert "participant_count" in sdv
        assert "community_narrative" in sdv
        assert "narratives" in sdv

        # Verify all 7 dimensions
        dims = sdv["dimensions"]
        for key in [
            "vivienda",
            "alimentacion",
            "agua",
            "salud",
            "educacion",
            "trabajo",
            "vinculos",
        ]:
            assert key in dims
            assert isinstance(dims[key], (int, float))

        # Verify narratives are generated for each dimension
        narratives = sdv["narratives"]
        for key in [
            "vivienda",
            "alimentacion",
            "agua",
            "salud",
            "educacion",
            "trabajo",
            "vinculos",
        ]:
            assert key in narratives
            assert isinstance(narratives[key], str)
            assert len(narratives[key]) > 0

    def test_pulse_gaps_structure(self, app, client, auth_headers):
        """Gaps section has all required fields."""
        response = client.get("/forms/pulse", headers=auth_headers)
        data = response.get_json()
        gaps = data["gaps"]

        assert "all" in gaps
        assert "critical" in gaps
        assert "warnings" in gaps
        assert "covered" in gaps
        assert "critical_count" in gaps
        assert isinstance(gaps["all"], list)
        assert isinstance(gaps["critical_count"], int)

    def test_pulse_alerts_structure(self, app, client, auth_headers):
        """Alerts section has all required fields."""
        response = client.get("/forms/pulse", headers=auth_headers)
        data = response.get_json()
        alerts = data["alerts"]

        assert "coherence_crimes" in alerts
        assert "warnings" in alerts
        assert "total_urgent" in alerts
        assert "crimes_count" in alerts
        assert "system_alert" in alerts
        assert isinstance(alerts["coherence_crimes"], list)
        assert isinstance(alerts["system_alert"], bool)

    def test_pulse_stats_structure(self, app, client, auth_headers):
        """Stats section has basic dashboard metrics."""
        response = client.get("/forms/pulse", headers=auth_headers)
        data = response.get_json()
        stats = data["stats"]

        assert "total_participants" in stats
        assert "total_exchanges" in stats

    def test_pulse_with_participant_data(self, app, client, auth_headers):
        """Pulse returns meaningful data when participants exist."""
        # Register a participant
        participant_data = {
            "name": "Pulso Test Participant",
            "email": "pulso_part@example.com",
            "referred_by": "Max",
            "phone_call": "+57 300 123 4567",
            "phone_whatsapp": "+57 300 123 4567",
            "telegram_handle": "@pulsotest",
            "city": "Bogotá",
            "neighborhood": "Chapinero",
            "personal_values": "Solidaridad, justicia",
            "offer_categories": ["conocimiento", "tiempo"],
            "offer_description": "Enseño programación",
            "offer_human_dimensions": ["crecimiento_aprendizaje"],
            "need_categories": ["alimentacion"],
            "need_description": "Necesito ayuda con mercado semanal",
            "need_urgency": "Alta",
            "need_human_dimensions": ["prosperidad_recursos"],
            "consent_given": 1,
        }

        reg_response = client.post(
            "/forms/participant",
            data=json.dumps(participant_data),
            content_type="application/json",
        )
        assert reg_response.status_code == 201

        # Now fetch pulse
        response = client.get("/forms/pulse", headers=auth_headers)
        assert response.status_code == 200

        data = response.get_json()

        # Should have at least 1 participant
        assert data["sdv"]["participant_count"] >= 1

        # Average should be a valid number
        avg = data["sdv"]["average_overall"]
        assert 0.0 <= avg <= 1.0

        # Community narrative should be non-empty
        assert len(data["sdv"]["community_narrative"]) > 0

    def test_pulse_empty_community(self, app, client, auth_headers):
        """Pulse works correctly with no participants (empty community)."""
        response = client.get("/forms/pulse", headers=auth_headers)
        assert response.status_code == 200

        data = response.get_json()

        # SDV defaults for empty community
        assert data["sdv"]["average_overall"] == 1.0
        assert data["sdv"]["participant_count"] == 0

        # No alerts in empty community
        assert data["alerts"]["system_alert"] is False
        assert data["alerts"]["crimes_count"] == 0
