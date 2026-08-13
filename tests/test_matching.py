import pytest

from app.matching import MatchingEngine
from app.utils import get_db


class TestMatchingEngineUnit:
    """Unit tests for MatchingEngine business logic using an in-memory/direct DB connection."""

    @pytest.fixture
    def db_conn(self, app):
        """Yields database connection within the app context."""
        with app.app_context():
            db = get_db()
            yield db

    def test_find_matches_basic(self, db_conn):
        """Test basic matching with categories overlap and scoring."""
        cursor = db_conn.cursor()

        # Insert seeker
        cursor.execute(
            """
            INSERT INTO participants (
                name, email, city, neighborhood, offer_description, need_description,
                need_urgency, offer_categories, offer_human_dimensions,
                need_categories, need_human_dimensions, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Seeker",
                "seeker@example.com",
                "Bogotá",
                "Chapinero",
                "Offers nothing",
                "Needs food and help",
                "Alta",
                "[]",
                "[]",
                '["alimentacion", "habilidad"]',
                '["prosperidad_recursos"]',
                "active",
            ),
        )
        seeker_id = cursor.lastrowid

        # Insert candidate that matches
        cursor.execute(
            """
            INSERT INTO participants (
                name, email, city, neighborhood, offer_description, need_description,
                need_urgency, offer_categories, offer_human_dimensions,
                need_categories, need_human_dimensions, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Candidate",
                "cand@example.com",
                "Bogotá",
                "Chapinero",
                "Provides food",
                "Needs nothing",
                "Baja",
                '["alimentacion", "habilidad"]',
                '["prosperidad_recursos"]',
                "[]",
                "[]",
                "active",
            ),
        )
        cand_id = cursor.lastrowid

        engine = MatchingEngine(db_conn)
        matches = engine.find_matches(seeker_id, exclude_recent=False)

        assert len(matches) > 0
        match = matches[0]
        assert match.offerer_id == cand_id
        assert "alimentacion" in match.matched_categories
        assert "habilidad" in match.matched_categories
        assert match.same_city is True
        assert match.same_neighborhood is True
        assert match.compatibility_score > 0.5

    def test_find_matches_exclude_recent(self, db_conn):
        """Test that recent exchange partners are excluded when exclude_recent=True."""
        cursor = db_conn.cursor()

        # Insert Seeker
        cursor.execute(
            "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, need_urgency, offer_categories, need_categories, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Seeker Rec",
                "seeker_rec@example.com",
                "Bogotá",
                "Chapinero",
                "Desc",
                "Desc",
                "Alta",
                "[]",
                '["objeto"]',
                "active",
            ),
        )
        seeker_id = cursor.lastrowid

        # Insert Partner (matching)
        cursor.execute(
            "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, need_urgency, offer_categories, need_categories, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Partner Rec",
                "partner_rec@example.com",
                "Bogotá",
                "Chapinero",
                "Desc",
                "Desc",
                "Baja",
                '["objeto"]',
                "[]",
                "active",
            ),
        )
        partner_id = cursor.lastrowid

        # Create recent exchange
        # Note: in schema, interchange has date, giver_id, receiver_id, etc.
        import datetime

        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO interchange (interchange_id, date, giver_id, receiver_id, type, description, urgency, impact_resolution_score, reciprocity_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "INT-REC-1",
                today_str,
                partner_id,
                seeker_id,
                "objeto",
                "Swap",
                "Baja",
                5,
                "unidirectional",
            ),
        )
        db_conn.commit()

        engine = MatchingEngine(db_conn)

        # With exclude_recent=True (default), partner should be excluded!
        matches_ex = engine.find_matches(seeker_id, exclude_recent=True)
        assert not any(m.offerer_id == partner_id for m in matches_ex)

        # With exclude_recent=False, partner should be included with recently_exchanged=True
        matches_inc = engine.find_matches(seeker_id, exclude_recent=False)
        partner_match = next(
            (m for m in matches_inc if m.offerer_id == partner_id), None
        )
        assert partner_match is not None
        assert partner_match.recently_exchanged is True

    def test_find_matches_empty_proximity_protection(self, db_conn):
        """Test that empty neighborhood/city values do not count as proximity matches."""
        cursor = db_conn.cursor()

        # Seeker and candidate with empty neighborhood and city
        cursor.execute(
            "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, need_urgency, offer_categories, need_categories, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Seeker Empty",
                "seeker_empty@example.com",
                "",
                "",
                "Desc",
                "Desc",
                "Alta",
                "[]",
                '["objeto"]',
                "active",
            ),
        )
        seeker_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, need_urgency, offer_categories, need_categories, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Partner Empty",
                "partner_empty@example.com",
                "",
                "",
                "Desc",
                "Desc",
                "Baja",
                '["objeto"]',
                "[]",
                "active",
            ),
        )
        partner_id = cursor.lastrowid
        db_conn.commit()

        engine = MatchingEngine(db_conn)
        matches = engine.find_matches(seeker_id, exclude_recent=False)

        assert len(matches) > 0
        match = matches[0]
        assert match.offerer_id == partner_id
        # proximity score must be 0.0 because city/neighborhood are empty
        assert match.same_city is False
        assert match.same_neighborhood is False

    def test_get_urgent_unmet_needs_skips_resolved(self, db_conn):
        """Test that get_urgent_unmet_needs excludes participants with need_level = 1 (resolved)."""
        cursor = db_conn.cursor()

        # Insert active participant with urgent need
        cursor.execute(
            "INSERT INTO participants (name, email, city, neighborhood, offer_description, need_description, need_urgency, offer_categories, need_categories, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Urgent User",
                "urgent_user@example.com",
                "Bogotá",
                "Chapinero",
                "Desc",
                "Desc",
                "Alta",
                "[]",
                '["objeto"]',
                "active",
            ),
        )
        p_id = cursor.lastrowid
        db_conn.commit()

        engine = MatchingEngine(db_conn)

        # 1. Unresolved: should show up
        urgent_list = engine.get_urgent_unmet_needs(days_threshold=0)
        assert any(u.participant_id == p_id for u in urgent_list)

        # 2. Resolved (need_level = 1 in follow-up): should NOT show up
        import datetime

        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO follow_ups (follow_up_date, participant_id, follow_up_type, current_situation, situation_change, active_interchanges_status, follow_up_priority, need_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                today_str,
                p_id,
                "need_resolved",
                "La situación está resuelta",
                "improved_significantly",
                "none",
                "closed",
                1,
            ),
        )
        db_conn.commit()

        urgent_list_resolved = engine.get_urgent_unmet_needs(days_threshold=0)
        assert not any(u.participant_id == p_id for u in urgent_list_resolved)

    def test_get_community_sdv_gaps(self, db_conn):
        """Test sdv gaps analysis returns all 8 dimensions and handles needing=0 correctly."""
        cursor = db_conn.cursor()

        # Clean database active participants first
        cursor.execute("UPDATE participants SET status = 'inactive'")
        db_conn.commit()

        engine = MatchingEngine(db_conn)
        gaps = engine.get_community_sdv_gaps()

        # Must return exactly 8 dimensions
        assert len(gaps) == 8
        # Because we cleaned up participants, needing=0 and offering=0 for all
        for gap in gaps:
            assert gap.participants_needing == 0
            assert gap.participants_offering == 0
            assert gap.coverage_ratio == 1.0  # Safe ratio for no demand/supply
            assert gap.gap_severity == "ok"


class TestMatchingAPI:
    """Integration tests for forms matching blueprints endpoints."""

    @pytest.fixture
    def test_data(self, app):
        """Insert test participants for matching API routes."""
        with app.app_context():
            db = get_db()
            cursor = db.cursor()

            # Insert seeker
            cursor.execute(
                """
                INSERT INTO participants (
                    name, email, city, neighborhood, offer_description, need_description,
                    need_urgency, offer_categories, offer_human_dimensions,
                    need_categories, need_human_dimensions, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "API Seeker",
                    "apiseeker@example.com",
                    "Bogotá",
                    "Chapinero",
                    "Desc",
                    "Need food",
                    "Alta",
                    "[]",
                    "[]",
                    '["alimentacion"]',
                    '["prosperidad_recursos"]',
                    "active",
                ),
            )
            seeker_id = cursor.lastrowid

            # Insert candidate
            cursor.execute(
                """
                INSERT INTO participants (
                    name, email, city, neighborhood, offer_description, need_description,
                    need_urgency, offer_categories, offer_human_dimensions,
                    need_categories, need_human_dimensions, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "API Cand",
                    "apicand@example.com",
                    "Bogotá",
                    "Chapinero",
                    "Offer food",
                    "Need nothing",
                    "Baja",
                    '["alimentacion"]',
                    '["prosperidad_recursos"]',
                    "[]",
                    "[]",
                    "active",
                ),
            )
            cand_id = cursor.lastrowid
            db.commit()

            return {"seeker_id": seeker_id, "cand_id": cand_id}

    def test_api_matching_participant(self, auth_client, test_data):
        """Test GET /forms/matching/participant/<id>"""
        seeker_id = test_data["seeker_id"]
        response = auth_client.get(f"/forms/matching/participant/{seeker_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["participant_id"] == seeker_id
        assert len(data["matches"]) > 0
        assert data["matches"][0]["offerer_id"] == test_data["cand_id"]

    def test_api_matching_urgent(self, auth_client, test_data):
        """Test GET /forms/matching/urgent"""
        response = auth_client.get("/forms/matching/urgent?days_threshold=0")
        assert response.status_code == 200
        data = response.get_json()
        assert "coherence_crimes" in data
        assert "warnings" in data
        assert data["total_urgent"] > 0

    def test_api_matching_gaps(self, auth_client, test_data):
        """Test GET /forms/matching/gaps"""
        response = auth_client.get("/forms/matching/gaps")
        assert response.status_code == 200
        data = response.get_json()
        assert "gaps" in data
        assert len(data["gaps"]) == 8

    def test_api_matching_summary(self, auth_client, test_data):
        """Test GET /forms/matching/summary"""
        response = auth_client.get("/forms/matching/summary")
        assert response.status_code == 200
        data = response.get_json()
        assert "urgent_unmet_count" in data
        assert "coherence_crimes_count" in data
        assert "critical_gaps_count" in data
