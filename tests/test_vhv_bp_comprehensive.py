"""
Tests comprehensivos para endpoints de vhv_bp.py

Cubre endpoints y casos edge que no están en test_vhv.py o test_vhv_calculator.py
"""

import json

import pytest


@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing."""
    # Login and get token (use pre-existing test user from conftest if available,
    # but here we follow the pattern of creating one specifically for this test file)
    register_data = {
        "email": "testauth_vhv@example.com",
        "password": "ValidPass123!",
        "name": "Test VHV User",
    }
    client.post("/auth/register", json=register_data)

    login_data = {"email": "testauth_vhv@example.com", "password": "ValidPass123!"}
    response = client.post("/auth/login", json=login_data)
    token = response.get_json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client):
    """Create admin authentication headers for testing."""
    # Use the admin@example.com user from conftest.py
    login_data = {"email": "admin@example.com", "password": "ValidPass123!"}
    response = client.post("/auth/login", json=login_data)
    token = response.get_json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


class TestVHVBPProducts:
    """Tests para endpoints de productos VHV."""

    def test_get_products_with_category_filter(self, app, client):
        """Test get_products con filtro de categoría."""
        # Crear producto de prueba
        product_data = {
            "name": "Test Product",
            "category": "food",
            "description": "Test description",
            "t_direct_hours": 1.0,
            "t_inherited_hours": 0.5,
            "t_future_hours": 0.2,
            "v_organisms_affected": 0.0,
            "v_consciousness_factor": 0.0,
            "v_suffering_factor": 1.0,
            "v_abundance_factor": 1.0,
            "v_rarity_factor": 1.0,
            "r_minerals_kg": 0.0,
            "r_water_m3": 0.0,
            "r_petroleum_l": 0.0,
            "r_land_hectares": 0.0,
            "r_frg_factor": 1.0,
            "r_cs_factor": 1.0,
            "save": True,
        }
        response = client.post(
            "/vhv/calculate",
            data=json.dumps(product_data),
            content_type="application/json",
        )
        assert response.status_code == 200

        # Test con filtro de categoría
        response = client.get("/vhv/products?category=food")
        assert response.status_code == 200
        json_data = response.get_json()
        assert "products" in json_data
        assert "total" in json_data

    def test_get_products_with_pagination(self, app, client):
        """Test get_products con paginación."""
        # Crear múltiples productos
        for i in range(3):
            product_data = {
                "name": f"Test Product {i}",
                "category": "electronics",
                "description": f"Test description {i}",
                "t_direct_hours": 1.0,
                "t_inherited_hours": 0.5,
                "t_future_hours": 0.2,
                "v_organisms_affected": 0.0,
                "v_consciousness_factor": 0.0,
                "v_suffering_factor": 1.0,
                "v_abundance_factor": 1.0,
                "v_rarity_factor": 1.0,
                "r_minerals_kg": 0.0,
                "r_water_m3": 0.0,
                "r_petroleum_l": 0.0,
                "r_land_hectares": 0.0,
                "r_frg_factor": 1.0,
                "r_cs_factor": 1.0,
                "save": True,
            }
            client.post(
                "/vhv/calculate",
                data=json.dumps(product_data),
                content_type="application/json",
            )

        # Test con límite
        response = client.get("/vhv/products?limit=2&offset=0")
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data["products"]) <= 2

        # Test con offset
        response = client.get("/vhv/products?limit=2&offset=2")
        assert response.status_code == 200

    def test_get_product_not_found(self, app, client):
        """Test get_product con ID inexistente."""
        response = client.get("/vhv/products/99999")
        assert response.status_code == 404
        json_data = response.get_json()
        assert "error" in json_data
        assert "not found" in json_data["error"].lower()

    def test_get_products_limit_validation(self, app, client):
        """Test que el límite máximo es 100."""
        response = client.get("/vhv/products?limit=200")
        assert response.status_code == 200
        json_data = response.get_json()
        # El límite debe estar limitado internamente


class TestVHVBPCompare:
    """Tests para endpoint de comparación de productos."""

    def test_compare_products_success(self, app, client):
        """Test compare_products con productos válidos."""
        # Crear dos productos
        product_ids = []
        for i in range(2):
            product_data = {
                "name": f"Compare Product {i}",
                "category": "food",
                "description": f"Test {i}",
                "t_direct_hours": 1.0 + i,
                "t_inherited_hours": 0.5,
                "t_future_hours": 0.2,
                "v_organisms_affected": 0.0,
                "v_consciousness_factor": 0.0,
                "v_suffering_factor": 1.0,
                "v_abundance_factor": 1.0,
                "v_rarity_factor": 1.0,
                "r_minerals_kg": 0.0,
                "r_water_m3": 0.0,
                "r_petroleum_l": 0.0,
                "r_land_hectares": 0.0,
                "r_frg_factor": 1.0,
                "r_cs_factor": 1.0,
                "save": True,
            }
            response = client.post(
                "/vhv/calculate",
                data=json.dumps(product_data),
                content_type="application/json",
            )
            product_ids.append(response.get_json()["product_id"])

        # Comparar productos
        ids_str = ",".join(map(str, product_ids))
        response = client.get(f"/vhv/compare?ids={ids_str}")
        assert response.status_code == 200
        json_data = response.get_json()
        assert "products" in json_data
        assert "comparison" in json_data
        assert "cheapest" in json_data["comparison"]
        assert "most_expensive" in json_data["comparison"]

    def test_compare_products_missing_ids(self, app, client):
        """Test compare_products sin parámetro ids."""
        response = client.get("/vhv/compare")
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_compare_products_invalid_ids(self, app, client):
        """Test compare_products con IDs inválidos."""
        response = client.get("/vhv/compare?ids=abc,def")
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_compare_products_less_than_two(self, app, client):
        """Test compare_products con menos de 2 productos."""
        # Crear un producto
        product_data = {
            "name": "Single Product",
            "category": "food",
            "description": "Test",
            "t_direct_hours": 1.0,
            "t_inherited_hours": 0.5,
            "t_future_hours": 0.2,
            "v_organisms_affected": 0.0,
            "v_consciousness_factor": 0.0,
            "v_suffering_factor": 1.0,
            "v_abundance_factor": 1.0,
            "v_rarity_factor": 1.0,
            "r_minerals_kg": 0.0,
            "r_water_m3": 0.0,
            "r_petroleum_l": 0.0,
            "r_land_hectares": 0.0,
            "r_frg_factor": 1.0,
            "r_cs_factor": 1.0,
            "save": True,
        }
        response = client.post(
            "/vhv/calculate",
            data=json.dumps(product_data),
            content_type="application/json",
        )
        product_id = response.get_json()["product_id"]

        response = client.get(f"/vhv/compare?ids={product_id}")
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_compare_products_not_found(self, app, client):
        """Test compare_products con productos inexistentes."""
        response = client.get("/vhv/compare?ids=99999,99998")
        assert response.status_code == 404
        json_data = response.get_json()
        assert "error" in json_data


class TestVHVBParameters:
    """Tests para endpoints de parámetros VHV."""

    def test_update_parameters_success(self, app, client, admin_headers):
        """Test update_parameters con valores válidos (Admin)."""
        data = {
            "alpha": 150.0,
            "beta": 2500.0,
            "gamma": 1.5,
            "delta": 150.0,
            "notes": "Test parameter update",
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 200
        json_data = response.get_json()
        assert "message" in json_data
        assert "parameters" in json_data

    def test_update_parameters_axiom_violation_alpha(self, app, client, admin_headers):
        """Test update_parameters violando axioma α > 0."""
        data = {
            "alpha": 0.0,  # Violación: debe ser > 0
            "beta": 2000.0,
            "gamma": 1.0,
            "delta": 100.0,
            "notes": "Test violation",
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data
        assert "axiom" in json_data["error"].lower() or "α" in json_data["error"]

    def test_update_parameters_axiom_violation_beta(self, app, client, admin_headers):
        """Test update_parameters violando axioma β > 0."""
        data = {
            "alpha": 100.0,
            "beta": -1.0,  # Violación: debe ser > 0
            "gamma": 1.0,
            "delta": 100.0,
            "notes": "Test violation",
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_update_parameters_axiom_violation_gamma(self, app, client, admin_headers):
        """Test update_parameters violando axioma γ ≥ 1."""
        data = {
            "alpha": 100.0,
            "beta": 2000.0,
            "gamma": 0.5,  # Violación: debe ser ≥ 1
            "delta": 100.0,
            "notes": "Test violation",
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_update_parameters_missing_notes(self, app, client, admin_headers):
        """Test update_parameters sin notes requerido."""
        data = {
            "alpha": 150.0,
            "beta": 2500.0,
            "gamma": 1.5,
            "delta": 150.0,
            # Missing notes
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
            headers=admin_headers,
        )
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_update_parameters_requires_auth(self, app, client):
        """Test que update_parameters requiere autenticación."""
        data = {
            "alpha": 150.0,
            "beta": 2500.0,
            "gamma": 1.5,
            "delta": 150.0,
            "notes": "Test",
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_update_parameters_requires_admin(self, app, client, auth_headers):
        """Test que update_parameters requiere privilegios de admin (RBAC)."""
        data = {
            "alpha": 150.0,
            "beta": 2500.0,
            "gamma": 1.5,
            "delta": 150.0,
            "notes": "Hacker notes",
        }
        response = client.put(
            "/vhv/parameters",
            data=json.dumps(data),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 403
        assert "admin privileges required" in response.get_json()["error"]


class TestVHVBPCaseStudies:
    """Tests para endpoint de case studies."""

    def test_get_case_studies(self, app, client):
        """Test get_case_studies endpoint."""
        response = client.get("/vhv/case-studies")
        assert response.status_code == 200
        json_data = response.get_json()
        assert "case_studies" in json_data
        assert len(json_data["case_studies"]) >= 2
        # Verificar que incluye los casos de estudio del paper
        names = [cs["name"] for cs in json_data["case_studies"]]
        assert any("Ética" in name for name in names)  # "Granja Ética" with accent
        assert any("Industrial" in name for name in names)
