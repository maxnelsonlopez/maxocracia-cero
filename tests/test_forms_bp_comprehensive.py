"""
Tests comprehensivos para endpoints de forms_bp.py

Cubre endpoints y casos edge que no están en test_forms.py
"""

import json

import pytest


@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing."""
    # Register test user
    register_data = {
        "email": "testauth_forms@example.com",
        "password": "TestPassword123!",
        "name": "Test Forms User",
    }
    client.post("/auth/register", json=register_data)
    
    # Login and get token
    login_data = {"email": "testauth_forms@example.com", "password": "TestPassword123!"}
    response = client.post("/auth/login", json=login_data)
    token = response.get_json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}



class TestFormsBPEndpoints:
    """Tests para endpoints de forms_bp.py con casos edge."""

    def test_get_participants_with_pagination(self, app, client, auth_headers):
        """Test get_participants con paginación."""
        # Crear múltiples participantes
        for i in range(5):
            data = {
                "name": f"Test User {i}",
                "email": f"test{i}@example.com",
                "referred_by": "Max",
                "phone_call": "+57 123 456 7890",
                "phone_whatsapp": "+57 123 456 7890",
                "telegram_handle": f"@test{i}",
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
            client.post(
                "/forms/participant",
                data=json.dumps(data),
                content_type="application/json",
            )

        # Test con límite
        response = client.get(
            "/forms/participants?limit=2&offset=0", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data["participants"]) <= 2
        assert json_data["limit"] == 2
        assert json_data["offset"] == 0

        # Test con offset
        response = client.get(
            "/forms/participants?limit=2&offset=2", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["offset"] == 2

    def test_get_participants_with_status_filter(self, app, client, auth_headers):
        """Test get_participants con filtro de status."""
        response = client.get(
            "/forms/participants?status=active", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert "participants" in json_data

    def test_get_participants_limit_validation(self, app, client, auth_headers):
        """Test que el límite máximo es 100."""
        response = client.get(
            "/forms/participants?limit=200", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["limit"] == 100  # Debe limitarse a 100

    def test_get_participant_not_found(self, app, client, auth_headers):
        """Test get_participant con ID inexistente."""
        response = client.get("/forms/participants/99999", headers=auth_headers)
        assert response.status_code == 404
        json_data = response.get_json()
        assert "error" in json_data
        assert "no encontrado" in json_data["error"].lower()

    def test_get_exchanges_with_filters(self, app, client, auth_headers):
        """Test get_exchanges con diferentes filtros."""
        # Crear un intercambio primero
        participant_data = {
            "name": "Giver",
            "email": "giver@example.com",
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@giver",
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
        giver_resp = client.post(
            "/forms/participant",
            data=json.dumps(participant_data),
            content_type="application/json",
        )
        giver_id = giver_resp.get_json()["participant_id"]

        participant_data["email"] = "receiver@example.com"
        participant_data["name"] = "Receiver"
        receiver_resp = client.post(
            "/forms/participant",
            data=json.dumps(participant_data),
            content_type="application/json",
        )
        receiver_id = receiver_resp.get_json()["participant_id"]

        exchange_data = {
            "interchange_id": "INT-FILTER-TEST",
            "date": "2025-12-03",
            "giver_id": giver_id,
            "receiver_id": receiver_id,
            "type": "alimentacion",
            "description": "Compartió comida",
            "urgency": "Alta",
            "uth_hours": 2.5,
            "impact_resolution_score": 5,
            "reciprocity_status": "unidirectional",
            "coordination_method": "max_direct",
        }
        client.post(
            "/forms/exchange",
            data=json.dumps(exchange_data),
            content_type="application/json",
            headers=auth_headers,
        )

        # Test con filtro de urgencia
        response = client.get(
            "/forms/exchanges?urgency=Alta", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert "exchanges" in json_data

        # Test con filtro de giver_id
        response = client.get(
            f"/forms/exchanges?giver_id={giver_id}", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert "exchanges" in json_data

    def test_get_exchange_not_found(self, app, client, auth_headers):
        """Test get_exchange con ID inexistente."""
        response = client.get("/forms/exchanges/99999", headers=auth_headers)
        assert response.status_code == 404
        json_data = response.get_json()
        assert "error" in json_data
        assert "no encontrado" in json_data["error"].lower()

    def test_get_followups_with_filters(self, app, client, auth_headers):
        """Test get_followups con filtros."""
        # Crear participante y follow-up
        participant_data = {
            "name": "Follow-up Filter Test",
            "email": "followupfilter@example.com",
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@followupfilter",
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
        participant_resp = client.post(
            "/forms/participant",
            data=json.dumps(participant_data),
            content_type="application/json",
        )
        participant_id = participant_resp.get_json()["participant_id"]

        followup_data = {
            "follow_up_date": "2025-12-03",
            "participant_id": participant_id,
            "follow_up_type": "routine_check",
            "current_situation": "La persona está mejor",
            "situation_change": "improved_slightly",
            "active_interchanges_status": "receiving_help",
            "follow_up_priority": "high",
            "need_level": 3,
        }
        client.post(
            "/forms/follow-up",
            data=json.dumps(followup_data),
            content_type="application/json",
            headers=auth_headers,
        )

        # Test con filtro de priority
        response = client.get(
            "/forms/follow-ups?priority=high", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert "follow_ups" in json_data

        # Test con filtro de participant_id
        response = client.get(
            f"/forms/follow-ups?participant_id={participant_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert "follow_ups" in json_data

    def test_get_participant_followups(self, app, client, auth_headers):
        """Test get_participant_followups con diferentes casos."""
        # Crear participante
        participant_data = {
            "name": "Participant Follow-ups",
            "email": "participantfollowups@example.com",
            "referred_by": "Max",
            "phone_call": "+57 123 456 7890",
            "phone_whatsapp": "+57 123 456 7890",
            "telegram_handle": "@participantfollowups",
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
        participant_resp = client.post(
            "/forms/participant",
            data=json.dumps(participant_data),
            content_type="application/json",
        )
        participant_id = participant_resp.get_json()["participant_id"]

        # Test sin follow-ups
        response = client.get(
            f"/forms/follow-ups/participant/{participant_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["count"] == 0
        assert json_data["participant_id"] == participant_id

        # Crear follow-up
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
        client.post(
            "/forms/follow-up",
            data=json.dumps(followup_data),
            content_type="application/json",
            headers=auth_headers,
        )

        # Test con follow-ups
        response = client.get(
            f"/forms/follow-ups/participant/{participant_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["count"] >= 1

    def test_get_trends_endpoint(self, app, client, auth_headers):
        """Test get_trends endpoint."""
        response = client.get("/forms/dashboard/trends", headers=auth_headers)
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, dict)

        # Test con periodo personalizado
        response = client.get(
            "/forms/dashboard/trends?period=60", headers=auth_headers
        )
        assert response.status_code == 200

    def test_get_categories_endpoint(self, app, client, auth_headers):
        """Test get_categories endpoint."""
        response = client.get("/forms/dashboard/categories", headers=auth_headers)
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, dict)

    def test_get_resolution_endpoint(self, app, client, auth_headers):
        """Test get_resolution endpoint."""
        response = client.get("/forms/dashboard/resolution", headers=auth_headers)
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, dict)

    def test_get_exchanges_limit_validation(self, app, client, auth_headers):
        """Test que el límite máximo es 100 para exchanges."""
        response = client.get(
            "/forms/exchanges?limit=200", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["limit"] == 100

    def test_get_followups_limit_validation(self, app, client, auth_headers):
        """Test que el límite máximo es 100 para follow-ups."""
        response = client.get(
            "/forms/follow-ups?limit=200", headers=auth_headers
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["limit"] == 100
