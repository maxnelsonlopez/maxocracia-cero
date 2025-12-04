"""
Tests for Dashboard Analytics Endpoints.

Tests the new temporal trends, category breakdown, and resolution metrics endpoints.
"""

import json

import pytest

from app import create_app
from app.utils import get_db


class TestDashboardAnalytics:
    """Tests for enhanced dashboard analytics endpoints."""

    def test_get_trends_requires_auth(self, client):
        """Test that trends endpoint requires authentication."""
        response = client.get("/forms/dashboard/trends")
        assert response.status_code == 401

    def test_get_trends_with_auth(self, auth_client):
        """Test trends endpoint returns valid data."""
        response = auth_client.get("/forms/dashboard/trends?period=30")
        assert response.status_code == 200
        data = response.get_json()
        assert "exchanges_per_week" in data
        assert "uth_per_week" in data
        assert "participants_growth" in data
        assert isinstance(data["exchanges_per_week"], list)
        assert isinstance(data["uth_per_week"], list)
        assert isinstance(data["participants_growth"], list)

    def test_get_trends_with_custom_period(self, auth_client):
        """Test trends endpoint with custom period parameter."""
        response = auth_client.get("/forms/dashboard/trends?period=7")
        assert response.status_code == 200
        data = response.get_json()
        assert "exchanges_per_week" in data

    def test_get_categories_requires_auth(self, client):
        """Test that categories endpoint requires authentication."""
        response = client.get("/forms/dashboard/categories")
        assert response.status_code == 401

    def test_get_categories_with_auth(self, auth_client):
        """Test category breakdown endpoint."""
        response = auth_client.get("/forms/dashboard/categories")
        assert response.status_code == 200
        data = response.get_json()
        assert "exchange_types" in data
        assert "top_offered_categories" in data
        assert "top_needed_categories" in data
        assert "match_rate" in data
        assert isinstance(data["exchange_types"], dict)
        assert isinstance(data["top_offered_categories"], dict)
        assert isinstance(data["top_needed_categories"], dict)
        assert isinstance(data["match_rate"], (int, float))

    def test_get_resolution_requires_auth(self, client):
        """Test that resolution endpoint requires authentication."""
        response = client.get("/forms/dashboard/resolution")
        assert response.status_code == 401

    def test_get_resolution_metrics(self, auth_client):
        """Test resolution metrics endpoint."""
        response = auth_client.get("/forms/dashboard/resolution")
        assert response.status_code == 200
        data = response.get_json()
        assert "avg_resolution_score" in data
        assert "resolution_by_urgency" in data
        assert "avg_days_to_resolve" in data
        assert "success_rate_by_category" in data
        assert isinstance(data["avg_resolution_score"], (int, float))
        assert isinstance(data["resolution_by_urgency"], dict)
        assert isinstance(data["avg_days_to_resolve"], (int, float))
        assert isinstance(data["success_rate_by_category"], dict)

    def test_trends_data_structure(self, auth_client):
        """Test that trends data has correct structure."""
        response = auth_client.get("/forms/dashboard/trends?period=30")
        data = response.get_json()

        # Each week entry should be [week_label, value]
        if len(data["exchanges_per_week"]) > 0:
            assert len(data["exchanges_per_week"][0]) == 2
            assert isinstance(data["exchanges_per_week"][0][0], str)  # week label
            assert isinstance(data["exchanges_per_week"][0][1], (int, float))  # count

        if len(data["uth_per_week"]) > 0:
            assert len(data["uth_per_week"][0]) == 2
            assert isinstance(data["uth_per_week"][0][0], str)  # week label
            assert isinstance(data["uth_per_week"][0][1], (int, float))  # UTH value

    def test_categories_match_rate_range(self, auth_client):
        """Test that match rate is within valid range (0-100)."""
        response = auth_client.get("/forms/dashboard/categories")
        data = response.get_json()
        assert 0 <= data["match_rate"] <= 100

    def test_resolution_score_range(self, auth_client):
        """Test that resolution scores are within valid range (0-10)."""
        response = auth_client.get("/forms/dashboard/resolution")
        data = response.get_json()

        # Average resolution score should be 0-10
        assert 0 <= data["avg_resolution_score"] <= 10

        # Individual urgency scores should also be 0-10
        for score in data["resolution_by_urgency"].values():
            assert 0 <= score <= 10
