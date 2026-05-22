import json
import pytest
from app.matching import MatchingEngine
from app.utils import get_db

class TestOracleAndOffererMatching:
    """Tests for the find_matches_for_offerer logic and the Oracle synthetic chat."""

    @pytest.fixture
    def db_conn(self, app):
        """Yields database connection within the app context."""
        with app.app_context():
            db = get_db()
            yield db

    def test_find_matches_for_offerer(self, db_conn):
        """Test finding seekers that match what an offerer can provide."""
        cursor = db_conn.cursor()

        # Insert Offerer
        cursor.execute(
            """
            INSERT INTO participants (
                name, email, city, neighborhood, offer_description, need_description,
                need_urgency, offer_categories, offer_human_dimensions,
                need_categories, need_human_dimensions, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Max Giver", "max@example.com", "Bogotá", "Chapinero", "Ofrece diseño web", "Needs nothing",
                "Baja", '["tecnologia", "diseño"]', '["crecimiento_aprendizaje"]', "[]", "[]", "active"
            )
        )
        offerer_id = cursor.lastrowid

        # Insert Seeker
        cursor.execute(
            """
            INSERT INTO participants (
                name, email, city, neighborhood, offer_description, need_description,
                need_urgency, offer_categories, offer_human_dimensions,
                need_categories, need_human_dimensions, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Nelson Seeker", "nelson@example.com", "Bogotá", "Chapinero", "Offers nothing", "Necesita diseño de logo",
                "Alta", "[]", "[]", '["diseño"]', '["crecimiento_aprendizaje"]', "active"
            )
        )
        seeker_id = cursor.lastrowid
        db_conn.commit()

        engine = MatchingEngine(db_conn)
        matches = engine.find_matches_for_offerer(offerer_id, exclude_recent=False)

        assert len(matches) > 0
        match = matches[0]
        # Candidates in find_matches_for_offerer represent seekers, so match.offerer_id contains the seeker's ID
        assert match.offerer_id == seeker_id
        assert "diseño" in match.matched_categories
        assert match.same_city is True
        assert match.same_neighborhood is True
        assert match.compatibility_score > 0.5

    def test_api_matching_me_no_profile(self, auth_client):
        """Test GET /forms/matching/me when user has no participant profile."""
        response = auth_client.get("/forms/matching/me")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "no_profile"
        assert data["email"] == "test@example.com"

    def test_api_matching_me_success(self, app, auth_client):
        """Test GET /forms/matching/me with active participant profile."""
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                """
                INSERT INTO participants (
                    name, email, city, neighborhood, offer_description, need_description,
                    need_urgency, offer_categories, offer_human_dimensions,
                    need_categories, need_human_dimensions, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "Test User", "test@example.com", "Bogotá", "Chapinero", "Ofrece tutorías", "Necesita comida",
                    "Media", '["educacion"]', '["crecimiento_aprendizaje"]', '["alimentacion"]', '["prosperidad_recursos"]', "active"
                )
            )
            db.commit()

        response = auth_client.get("/forms/matching/me")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert data["participant"]["email"] == "test@example.com"
        assert "seeker_matches" in data
        assert "offerer_matches" in data

    def test_api_oracle_chat_simulation(self, app, auth_client):
        """Test POST /forms/oracle/chat parsing in simulation fallback mode."""
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM participants") # Clean up to ensure exact names mapping
            
            # Insert Max Giver
            cursor.execute(
                "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("Max Nelson", "maxnelson@example.com", "Bogotá", "Chapinero", "Programacion", "Nada", "active")
            )
            max_id = cursor.lastrowid
            
            # Insert Nelson Seeker
            cursor.execute(
                "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("Nelson Lopez", "nelsonlopez@example.com", "Bogotá", "Chapinero", "Nada", "Programacion", "active")
            )
            nelson_id = cursor.lastrowid
            db.commit()

        # Send message where Max Nelson helps Nelson Lopez
        message = "Max Nelson ayudó a Nelson Lopez con 3 horas de clases de programacion y la urgencia fue alta"
        response = auth_client.post("/forms/oracle/chat", json={"message": message})
        assert response.status_code == 200
        data = response.get_json()
        
        assert "reply" in data
        assert data["prefill"] is not None
        assert data["prefill"]["giver_id"] == max_id
        assert data["prefill"]["receiver_id"] == nelson_id
        assert data["prefill"]["uth_hours"] == 3.0
        assert data["prefill"]["urgency"] == "Alta"
        assert "programacion" in data["prefill"]["description"].lower()
