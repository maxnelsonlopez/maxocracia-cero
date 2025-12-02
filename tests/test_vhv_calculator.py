"""
Tests for VHV Calculator

Tests mathematical calculations, API endpoints, axiomatic constraints,
and case studies from paper_formalizacion_matematica_maxo.txt
"""

import json

import pytest

from app import create_app
from app.utils import get_db, init_db
from app.vhv_calculator import (
    CASE_STUDY_HUEVO_ETICO,
    CASE_STUDY_HUEVO_INDUSTRIAL,
    VHVCalculator,
)


@pytest.fixture
def app():
    """Create test app."""
    app = create_app(db_path=":memory:")
    app.config["TESTING"] = True

    with app.app_context():
        init_db(app)

    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def calculator():
    """Create calculator instance."""
    return VHVCalculator()


class TestVHVCalculator:
    """Test VHV calculation logic."""

    def test_calculate_t_component(self, calculator):
        """Test T component calculation."""
        t = calculator.calculate_t_component(
            direct_hours=10, inherited_hours=5, future_hours=3
        )
        assert t == 18.0

    def test_calculate_v_component(self, calculator):
        """Test V component calculation."""
        v = calculator.calculate_v_component(
            organisms_affected=1,
            f_consciousness=0.9,
            f_suffering=25.0,
            f_abundance=0.001,
            f_rarity=1.0,
        )
        assert v == pytest.approx(0.0225, rel=1e-4)

    def test_calculate_r_component(self, calculator):
        """Test R component calculation."""
        r = calculator.calculate_r_component(
            minerals_kg=10,
            water_m3=5,
            petroleum_l=2,
            land_hectares=0.1,
            frg_factor=1.5,
            cs_factor=2.0,
        )
        # (10*1.0 + 5*0.1 + 2*2.0 + 0.1*100) * 1.5 * 2.0
        expected = (10 + 0.5 + 4 + 10) * 1.5 * 2.0
        assert r == pytest.approx(expected, rel=1e-2)

    def test_calculate_maxo_price_basic(self, calculator):
        """Test basic Maxo price calculation."""
        price = calculator.calculate_maxo_price(
            t_component=1.0,
            v_component=0.01,
            r_component=0.5,
            alpha=100,
            beta=2000,
            gamma=1.0,
            delta=100,
        )
        # 100*1.0 + 2000*0.01^1.0 + 100*0.5 = 100 + 20 + 50 = 170
        assert price == pytest.approx(170.0, rel=1e-2)

    def test_axiom_alpha_greater_than_zero(self, calculator):
        """Test axiom: α > 0."""
        with pytest.raises(ValueError, match="α must be > 0"):
            calculator.calculate_maxo_price(
                t_component=1,
                v_component=1,
                r_component=1,
                alpha=0,  # Invalid
                beta=1,
                gamma=1,
                delta=1,
            )

    def test_axiom_beta_greater_than_zero(self, calculator):
        """Test axiom: β > 0."""
        with pytest.raises(ValueError, match="β must be > 0"):
            calculator.calculate_maxo_price(
                t_component=1,
                v_component=1,
                r_component=1,
                alpha=1,
                beta=-1,  # Invalid
                gamma=1,
                delta=1,
            )

    def test_axiom_gamma_greater_or_equal_one(self, calculator):
        """Test axiom: γ ≥ 1."""
        with pytest.raises(ValueError, match="γ must be ≥ 1"):
            calculator.calculate_maxo_price(
                t_component=1,
                v_component=1,
                r_component=1,
                alpha=1,
                beta=1,
                gamma=0.5,  # Invalid
                delta=1,
            )

    def test_axiom_delta_greater_or_equal_zero(self, calculator):
        """Test axiom: δ ≥ 0."""
        with pytest.raises(ValueError, match="δ must be ≥ 0"):
            calculator.calculate_maxo_price(
                t_component=1,
                v_component=1,
                r_component=1,
                alpha=1,
                beta=1,
                gamma=1,
                delta=-5,  # Invalid
            )


class TestCaseStudies:
    """Test case studies from the paper."""

    def test_huevo_etico_price(self, calculator):
        """
        Test ethical egg case study.
        Expected: ~12 Maxos (from paper líneas 318-329)
        """
        result = calculator.calculate_vhv(**CASE_STUDY_HUEVO_ETICO, **DEFAULT_PARAMS)

        # Should be approximately 12 Maxos
        assert result["maxo_price"] >= 10.0
        assert result["maxo_price"] <= 20.0

        # Time contribution should be higher (more labor)
        assert result["breakdown"]["time_contribution"] > 10

        # Life contribution should be LOW (minimal suffering)
        assert result["breakdown"]["life_contribution"] < 5

    def test_huevo_industrial_price(self, calculator):
        """
        Test industrial egg case study.
        Expected: ~45 Maxos (from paper líneas 306-317)
        """
        result = calculator.calculate_vhv(
            **CASE_STUDY_HUEVO_INDUSTRIAL, **DEFAULT_PARAMS
        )

        # Should be approximately 45 Maxos
        assert result["maxo_price"] >= 35.0
        assert result["maxo_price"] <= 55.0

        # Life contribution should be HIGH (massive suffering penalty)
        assert result["breakdown"]["life_contribution"] > 25

    def test_ethical_cheaper_than_industrial(self, calculator):
        """
        Test that ethical egg is cheaper than industrial.
        This validates the core value proposition of Maxocracia.
        """
        ethical_result = calculator.calculate_vhv(
            **CASE_STUDY_HUEVO_ETICO, **DEFAULT_PARAMS
        )
        industrial_result = calculator.calculate_vhv(
            **CASE_STUDY_HUEVO_INDUSTRIAL, **DEFAULT_PARAMS
        )

        assert ethical_result["maxo_price"] < industrial_result["maxo_price"]

        # Should be significantly cheaper (at least 2x)
        ratio = industrial_result["maxo_price"] / ethical_result["maxo_price"]
        assert ratio >= 2.0


class TestVHVAPI:
    """Test VHV API endpoints."""

    def test_get_parameters(self, client):
        """Test GET /vhv/parameters."""
        response = client.get("/vhv/parameters")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "alpha" in data
        assert "beta" in data
        assert "gamma" in data
        assert "delta" in data

        # Check default values
        assert data["alpha"] == 100.0
        assert data["beta"] == 2000.0
        assert data["gamma"] == 1.0
        assert data["delta"] == 100.0

    def test_calculate_endpoint(self, client):
        """Test POST /vhv/calculate."""
        payload = {
            "name": "Test Product",
            **CASE_STUDY_HUEVO_ETICO,
        }

        response = client.post(
            "/vhv/calculate", json=payload, headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "vhv" in data
        assert "maxo_price" in data
        assert "breakdown" in data

        assert "T" in data["vhv"]
        assert "V" in data["vhv"]
        assert "R" in data["vhv"]

    def test_calculate_and_save(self, client):
        """Test POST /vhv/calculate with save=true."""
        payload = {
            "name": "Test Product to Save",
            "category": "test",
            "save": True,
            **CASE_STUDY_HUEVO_ETICO,
        }

        response = client.post(
            "/vhv/calculate", json=payload, headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "product_id" in data
        assert data["product_id"] > 0

    def test_get_products(self, client):
        """Test GET /vhv/products."""
        # First create a product
        payload = {
            "name": "Test Product",
            "category": "food",
            "save": True,
            **CASE_STUDY_HUEVO_ETICO,
        }
        client.post(
            "/vhv/calculate", json=payload, headers={"Content-Type": "application/json"}
        )

        # Now get products
        response = client.get("/vhv/products")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "products" in data
        assert "total" in data
        assert data["total"] >= 1

    def test_get_product_by_id(self, client):
        """Test GET /vhv/products/<id>."""
        # Create a product
        payload = {
            "name": "Specific Product",
            "category": "electronics",
            "description": "Test description",
            "save": True,
            **CASE_STUDY_HUEVO_ETICO,
        }
        calc_response = client.post(
            "/vhv/calculate", json=payload, headers={"Content-Type": "application/json"}
        )
        product_id = json.loads(calc_response.data)["product_id"]

        # Get product
        response = client.get(f"/vhv/products/{product_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["name"] == "Specific Product"
        assert data["category"] == "electronics"
        assert "components" in data

    def test_compare_products(self, client):
        """Test GET /vhv/compare."""
        # Create two products
        payload1 = {"name": "Product A", "save": True, **CASE_STUDY_HUEVO_ETICO}
        payload2 = {"name": "Product B", "save": True, **CASE_STUDY_HUEVO_INDUSTRIAL}

        response1 = client.post(
            "/vhv/calculate",
            json=payload1,
            headers={"Content-Type": "application/json"},
        )
        response2 = client.post(
            "/vhv/calculate",
            json=payload2,
            headers={"Content-Type": "application/json"},
        )

        id1 = json.loads(response1.data)["product_id"]
        id2 = json.loads(response2.data)["product_id"]

        # Compare
        response = client.get(f"/vhv/compare?ids={id1},{id2}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "products" in data
        assert "comparison" in data
        assert len(data["products"]) == 2
        assert "cheapest" in data["comparison"]
        assert "most_expensive" in data["comparison"]

    def test_get_case_studies(self, client):
        """Test GET /vhv/case-studies."""
        response = client.get("/vhv/case-studies")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "case_studies" in data
        assert len(data["case_studies"]) >= 2

    def test_update_parameters_requires_auth(self, client):
        """Test PUT /vhv/parameters requires authentication."""
        payload = {"alpha": 150, "notes": "Test update"}

        response = client.put(
            "/vhv/parameters", json=payload, headers={"Content-Type": "application/json"}
        )

        # Should fail without token
        assert response.status_code == 401


# Default parameters for case study tests
DEFAULT_PARAMS = {"alpha": 100.0, "beta": 2000.0, "gamma": 1.0, "delta": 100.0}
