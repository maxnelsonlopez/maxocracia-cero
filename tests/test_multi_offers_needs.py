import json
import sqlite3

from app.forms_manager import FormsManager
from app.matching import MatchingEngine


def register_test_participant(
    client,
    email="test@example.com",
    name="Test User",
    offer_cat="tiempo",
    need_cat="alimentacion",
):
    data = {
        "name": name,
        "email": email,
        "referred_by": "Max",
        "phone_call": "+57 123 456 7890",
        "phone_whatsapp": "+57 123 456 7890",
        "telegram_handle": "@testuser",
        "city": "Bogotá",
        "neighborhood": "Chapinero",
        "personal_values": "Honestidad, colaboración",
        "offer_categories": [offer_cat],
        "offer_description": "Ofrezco ayuda",
        "offer_human_dimensions": ["conexion_social"],
        "need_categories": [need_cat],
        "need_description": "Necesito ayuda",
        "need_urgency": "Media",
        "need_human_dimensions": ["prosperidad_recursos"],
    }
    response = client.post(
        "/forms/participant", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    return response.get_json()["participant_id"]


def test_secondary_offers_crud(app, client, auth_client, admin_client, auth):
    # 1. Register a participant
    pid = register_test_participant(client, email="test@example.com")

    # 2. Add secondary offer (POST)
    offer_data = {
        "description": "Clases de matemáticas de refuerzo",
        "categories": ["conocimiento", "habilidad"],
        "human_dimensions": ["crecimiento_aprendizaje"],
        "status": "active",
    }

    # Try adding without token (unauthenticated) - should return 401
    token = client.environ_base.pop("HTTP_AUTHORIZATION", None)
    res = client.post(f"/forms/participants/{pid}/offers", json=offer_data)
    assert res.status_code == 401
    if token:
        client.environ_base["HTTP_AUTHORIZATION"] = token

    # Add as owner (auth_client)
    res = auth_client.post(f"/forms/participants/{pid}/offers", json=offer_data)
    assert res.status_code == 201
    offer_id = res.get_json()["offer_id"]
    assert offer_id is not None

    # 3. Get secondary offers (GET)
    res = auth_client.get(f"/forms/participants/{pid}/offers")
    assert res.status_code == 200
    offers = res.get_json()["offers"]
    assert len(offers) == 1
    assert offers[0]["description"] == "Clases de matemáticas de refuerzo"
    assert "conocimiento" in offers[0]["categories"]
    assert "crecimiento_aprendizaje" in offers[0]["human_dimensions"]

    # 4. Update secondary offer (PUT)
    update_data = {"description": "Clases de física y matemáticas", "status": "paused"}

    # Try updating as non-owner (test2)
    # Login as test2
    login_res = auth.login(email="test2@example.com", password="ValidPass123!")
    assert login_res.status_code == 200
    token2 = login_res.get_json().get("access_token")

    headers = {"Authorization": f"Bearer {token2}"}
    res = client.put(f"/forms/offers/{offer_id}", json=update_data, headers=headers)
    assert res.status_code == 403

    # Update as owner
    res = auth_client.put(f"/forms/offers/{offer_id}", json=update_data)
    assert res.status_code == 200

    # Verify update
    res = auth_client.get(f"/forms/participants/{pid}/offers")
    assert (
        res.get_json()["offers"][0]["description"] == "Clases de física y matemáticas"
    )
    assert res.get_json()["offers"][0]["status"] == "paused"

    # Update as admin (should succeed)
    res = admin_client.put(f"/forms/offers/{offer_id}", json={"status": "active"})
    assert res.status_code == 200

    # 5. Delete secondary offer (DELETE)
    # Try deleting as non-owner
    res = client.delete(f"/forms/offers/{offer_id}", headers=headers)
    assert res.status_code == 403

    # Delete as owner
    res = auth_client.delete(f"/forms/offers/{offer_id}")
    assert res.status_code == 200

    # Verify deleted
    res = auth_client.get(f"/forms/participants/{pid}/offers")
    assert len(res.get_json()["offers"]) == 0


def test_secondary_needs_crud(app, client, auth_client, admin_client, auth):
    pid = register_test_participant(client, email="test@example.com")

    need_data = {
        "description": "Reparar fuga de agua en cocina",
        "categories": ["habilidad", "objeto"],
        "urgency": "Alta",
        "human_dimensions": ["seguridad_estabilidad"],
        "status": "active",
    }

    # Add as owner
    res = auth_client.post(f"/forms/participants/{pid}/needs", json=need_data)
    assert res.status_code == 201
    need_id = res.get_json()["need_id"]

    # Get
    res = auth_client.get(f"/forms/participants/{pid}/needs")
    assert res.status_code == 200
    needs = res.get_json()["needs"]
    assert len(needs) == 1
    assert needs[0]["description"] == "Reparar fuga de agua en cocina"
    assert needs[0]["urgency"] == "Alta"

    # Update as non-owner
    login_res = auth.login(email="test2@example.com", password="ValidPass123!")
    token2 = login_res.get_json().get("access_token")
    headers = {"Authorization": f"Bearer {token2}"}
    res = client.put(
        f"/forms/needs/{need_id}", json={"urgency": "Media"}, headers=headers
    )
    assert res.status_code == 403

    # Update as owner
    res = auth_client.put(f"/forms/needs/{need_id}", json={"urgency": "Media"})
    assert res.status_code == 200

    # Verify update
    res = auth_client.get(f"/forms/participants/{pid}/needs")
    assert res.get_json()["needs"][0]["urgency"] == "Media"

    # Delete as owner
    res = auth_client.delete(f"/forms/needs/{need_id}")
    assert res.status_code == 200


def test_matching_engine_consolidation(app, client, auth_client):
    # Register two participants
    # pid1 is seeker. Primary need: "alimentacion"
    pid1 = register_test_participant(
        client,
        email="test@example.com",
        name="Seeker",
        offer_cat="tiempo",
        need_cat="alimentacion",
    )
    # pid2 is offerer. Primary offer: "tiempo"
    pid2 = register_test_participant(
        client,
        email="test2@example.com",
        name="Offerer",
        offer_cat="tiempo",
        need_cat="alimentacion",
    )

    # Initially, pid2 doesn't offer "alimentacion" (only "tiempo"). So pid2 is NOT a match for pid1.
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    engine = MatchingEngine(conn)

    matches = engine.find_matches(seeker_id=pid1)
    # No matches on need categories because pid2 offers "tiempo" and pid1 needs "alimentacion"
    assert len(matches) == 0

    # Add secondary offer to pid2 that matches pid1's need
    manager = FormsManager(conn)
    success, msg, offer_id = manager.add_participant_offer(
        pid2,
        {
            "description": "Entrega de mercados gratis",
            "categories": ["alimentacion"],
            "human_dimensions": ["prosperidad_recursos"],
            "status": "active",
        },
    )
    assert success is True

    # Re-evaluate matching. Now pid2 should match pid1 because of secondary offer
    matches = engine.find_matches(seeker_id=pid1)
    assert len(matches) == 1
    assert matches[0].offerer_id == pid2
    assert "alimentacion" in matches[0].matched_categories
    assert "Entrega de mercados gratis" in matches[0].offerer_description
    assert "prosperidad_recursos" in matches[0].offerer_dimensions

    # Let's test find_matches_for_offerer
    # Seeker (pid1) has primary need "alimentacion". Offerer (pid2) has primary offer "tiempo", secondary "alimentacion".
    # If we find matches for offerer pid2, we should find seeker pid1.
    matches_offerer = engine.find_matches_for_offerer(offerer_id=pid2)
    assert len(matches_offerer) == 1
    assert matches_offerer[0].offerer_id == pid1
    assert "alimentacion" in matches_offerer[0].matched_categories

    conn.close()


def test_urgent_unmet_needs_with_contact(app, client):
    pid = register_test_participant(
        client, email="test@example.com", name="Urgent Seeker"
    )

    # Initially need urgency is "Media", so it shouldn't show in urgent unmet needs
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    engine = MatchingEngine(conn)

    assert len(engine.get_urgent_unmet_needs()) == 0

    # Add a secondary urgent need (urgency = 'Alta')
    manager = FormsManager(conn)
    success, msg, need_id = manager.add_participant_need(
        pid,
        {
            "description": "Necesidad médica urgente",
            "categories": ["alimentacion"],
            "urgency": "Alta",
            "human_dimensions": ["bienestar_descanso"],
            "status": "active",
        },
    )
    assert success is True

    # Now it should show in urgent unmet needs
    urgent = engine.get_urgent_unmet_needs(days_threshold=0)
    assert len(urgent) == 1
    assert urgent[0].participant_id == pid
    assert urgent[0].need_description == "Necesidad médica urgente"
    assert urgent[0].phone_whatsapp == "+57 123 456 7890"
    assert urgent[0].telegram == "@testuser"

    conn.close()


def test_community_sdv_gaps_incorporates_secondary(app, client):
    # Create two participants
    pid1 = register_test_participant(
        client, email="test@example.com", name="P1", offer_cat="tiempo"
    )
    register_test_participant(
        client, email="test2@example.com", name="P2", offer_cat="habilidad"
    )

    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)

    # Check default coverage gaps
    engine = MatchingEngine(conn)

    # Add secondary need with a new dimension "autoestima_autonomia" to pid1
    manager = FormsManager(conn)
    success, msg, need_id = manager.add_participant_need(
        pid1,
        {
            "description": "Ayuda con emprendimiento",
            "categories": ["tiempo"],
            "urgency": "Media",
            "human_dimensions": ["autoestima_autonomia"],
            "status": "active",
        },
    )
    assert success is True

    # Check updated gaps
    gaps_after = {g.dimension: g for g in engine.get_community_sdv_gaps()}

    # Seeker needing autoestima_autonomia should be 1 now
    assert gaps_after["autoestima_autonomia"].participants_needing == 1

    conn.close()


def test_cascade_delete_participant(app, client):
    pid = register_test_participant(client, email="test@example.com")

    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    manager = FormsManager(conn)

    # Add secondary offer and need
    manager.add_participant_offer(
        pid,
        {
            "description": "Trabajo secundario",
            "categories": ["tiempo"],
            "human_dimensions": ["conexion_social"],
        },
    )
    manager.add_participant_need(
        pid,
        {
            "description": "Ayuda secundaria",
            "categories": ["tiempo"],
            "human_dimensions": ["conexion_social"],
        },
    )

    # Verify count in DB
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM participant_offers WHERE participant_id = ?", (pid,)
    )
    assert cursor.fetchone()[0] == 1
    cursor.execute(
        "SELECT COUNT(*) FROM participant_needs WHERE participant_id = ?", (pid,)
    )
    assert cursor.fetchone()[0] == 1

    # Delete participant
    success, msg = manager.delete_participant(pid)
    assert success is True

    # Verify cascade deletion
    cursor.execute(
        "SELECT COUNT(*) FROM participant_offers WHERE participant_id = ?", (pid,)
    )
    assert cursor.fetchone()[0] == 0
    cursor.execute(
        "SELECT COUNT(*) FROM participant_needs WHERE participant_id = ?", (pid,)
    )
    assert cursor.fetchone()[0] == 0

    conn.close()
