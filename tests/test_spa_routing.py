"""
Tests del ruteo SPA y los payloads RSC de la navegación cliente.

Cubre:
- _dotform_to_dirform: mapeo de payloads de segmentos en forma de puntos
  a la forma de directorios de la exportación estática de Next.js.
- _alias_dynamic_segments: reescritura de /contracts/<id> a la plantilla SSG
  'placeholder' (carga completa y navegación cliente).
- Despacho del before_request de /contracts/: payloads RSC y navegaciones
  de navegador se sirven como frontend; la API sigue autenticada.
"""

import os

os.environ["SECRET_KEY"] = "test-secret"

import tempfile

import pytest

from app import _dotform_to_dirform, create_app
from app.contracts_bp import _alias_dynamic_segments
from app.utils import get_db

DIST_INDEX = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "app",
    "static",
    "dist",
    "index.html",
)
HAS_DIST = os.path.exists(DIST_INDEX)


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db_path=db_path)
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        with app.app_context():
            db = get_db()
            with open("app/schema.sql", "r", encoding="utf-8") as f:
                db.executescript(f.read())
            db.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (1, 'a@test.com', 'Alice', 'hash')"
            )
            db.commit()
        yield test_client

    os.close(db_fd)
    os.unlink(db_path)


def test_dotform_to_dirform_basic_segment():
    assert (
        _dotform_to_dirform("admin/network/__next.admin.network.txt")
        == "admin/network/__next.admin/network.txt"
    )


def test_dotform_to_dirform_page_segment():
    assert (
        _dotform_to_dirform("admin/network/__next.admin.network.__PAGE__.txt")
        == "admin/network/__next.admin/network/__PAGE__.txt"
    )


def test_dotform_to_dirform_single_segment():
    assert (
        _dotform_to_dirform("micromax/__next.micromax.__PAGE__.txt")
        == "micromax/__next.micromax/__PAGE__.txt"
    )


def test_dotform_to_dirform_nested():
    assert (
        _dotform_to_dirform("forms/cero/__next.forms.cero.txt")
        == "forms/cero/__next.forms/cero.txt"
    )


def test_dotform_to_dirform_flat_tree_file():
    # Los archivos _tree/_head/_index ya existen en forma de puntos y
    # el mapeo los deja intactos.
    assert (
        _dotform_to_dirform("admin/dashboard/__next._tree.txt")
        == "admin/dashboard/__next._tree.txt"
    )


def test_dotform_to_dirform_non_rsc_returns_none():
    assert _dotform_to_dirform("index.txt") is None
    assert _dotform_to_dirform("admin/network") is None
    assert _dotform_to_dirform("admin/network.html") is None
    assert _dotform_to_dirform("not-rsc.txt") is None


# --- Alias de la ruta dinámica /contracts/<id> ---


def test_alias_dynamic_segment_page_payload():
    assert (
        _alias_dynamic_segments("contracts/demo-sdv-s-001.txt")
        == "contracts/placeholder.txt"
    )
    assert (
        _alias_dynamic_segments("contracts/demo-sdv-s-001.html")
        == "contracts/placeholder.html"
    )


def test_alias_dynamic_segment_nested_payloads():
    assert (
        _alias_dynamic_segments("contracts/demo-sdv-s-001/__next._tree.txt")
        == "contracts/placeholder/__next._tree.txt"
    )
    assert (
        _alias_dynamic_segments(
            "contracts/demo-sdv-s-001/__next.contracts.demo-sdv-s-001.txt"
        )
        == "contracts/placeholder/__next.contracts.placeholder.txt"
    )
    assert (
        _alias_dynamic_segments(
            "contracts/demo-sdv-s-001/__next.contracts.demo-sdv-s-001.__PAGE__.txt"
        )
        == "contracts/placeholder/__next.contracts.placeholder.__PAGE__.txt"
    )


def test_alias_dynamic_segment_no_alias_for_static_routes():
    assert _alias_dynamic_segments("contracts/builder.txt") == "contracts/builder.txt"
    assert _alias_dynamic_segments("contracts/builder.html") == "contracts/builder.html"
    assert (
        _alias_dynamic_segments("contracts/negotiate.txt") == "contracts/negotiate.txt"
    )
    assert (
        _alias_dynamic_segments("contracts/negotiate.html")
        == "contracts/negotiate.html"
    )
    assert (
        _alias_dynamic_segments("contracts/__next.contracts.txt")
        == "contracts/__next.contracts.txt"
    )
    assert _alias_dynamic_segments("contracts.txt") == "contracts.txt"


# --- Despacho del before_request (frontend vs API) ---


@pytest.mark.skipif(not HAS_DIST, reason="frontend estático no construido")
def test_rsc_payload_dinamico_servido_sin_token(client):
    """La navegación cliente no manda token: el payload RSC de cualquier
    /contracts/<id> se sirve desde la plantilla SSG 'placeholder' (200),
    nunca un 401 de la API."""
    res = client.get(
        "/contracts/contracto-cualquiera-1.txt",
        headers={"Accept": "text/x-component"},
    )
    assert res.status_code == 200
    assert "text/plain" in res.content_type


@pytest.mark.skipif(not HAS_DIST, reason="frontend estático no construido")
def test_navegacion_navegador_recibe_html(client):
    """Una navegación completa del navegador recibe el HTML del frontend
    (plantilla SSG 'placeholder') y no el JSON 401 de la API."""
    res = client.get(
        "/contracts/contracto-cualquiera-1",
        headers={"Accept": "text/html,application/xhtml+xml"},
    )
    assert res.status_code == 200
    assert "text/html" in res.content_type
    assert b"<!DOCTYPE html>" in res.data


@pytest.mark.skipif(not HAS_DIST, reason="frontend estático no construido")
def test_builder_recibe_html(client):
    res = client.get("/contracts/builder", headers={"Accept": "text/html"})
    assert res.status_code == 200
    assert "text/html" in res.content_type


@pytest.mark.skipif(not HAS_DIST, reason="frontend estático no construido")
def test_negotiate_recibe_html(client):
    """La página protagonista /contracts/negotiate se sirve como frontend
    (no se reescribe a 'placeholder' ni devuelve 401 de la API)."""
    res = client.get("/contracts/negotiate", headers={"Accept": "text/html"})
    assert res.status_code == 200
    assert "text/html" in res.content_type


@pytest.mark.skipif(not HAS_DIST, reason="frontend estático no construido")
def test_lista_recibe_html(client):
    res = client.get("/contracts/", headers={"Accept": "text/html"})
    assert res.status_code == 200
    assert "text/html" in res.content_type


def test_api_contrato_sigue_autenticada(client):
    """La API real (fetch con Accept */*) mantiene su protección."""
    res = client.get("/contracts/contracto-cualquiera-1")
    assert res.status_code == 401
