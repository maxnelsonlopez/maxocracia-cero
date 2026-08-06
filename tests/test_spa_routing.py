"""
Tests del ruteo SPA y los payloads RSC de la navegación cliente.

Cubre:
- _dotform_to_dirform: mapeo de payloads de segmentos en forma de puntos
  a la forma de directorios de la exportación estática de Next.js.
"""

import os

os.environ['SECRET_KEY'] = 'test-secret'

from app import _dotform_to_dirform


def test_dotform_to_dirform_basic_segment():
    assert _dotform_to_dirform("admin/network/__next.admin.network.txt") == \
        "admin/network/__next.admin/network.txt"


def test_dotform_to_dirform_page_segment():
    assert _dotform_to_dirform("admin/network/__next.admin.network.__PAGE__.txt") == \
        "admin/network/__next.admin/network/__PAGE__.txt"


def test_dotform_to_dirform_single_segment():
    assert _dotform_to_dirform("micromax/__next.micromax.__PAGE__.txt") == \
        "micromax/__next.micromax/__PAGE__.txt"


def test_dotform_to_dirform_nested():
    assert _dotform_to_dirform("forms/cero/__next.forms.cero.txt") == \
        "forms/cero/__next.forms/cero.txt"


def test_dotform_to_dirform_flat_tree_file():
    # Los archivos _tree/_head/_index ya existen en forma de puntos y
    # el mapeo los deja intactos.
    assert _dotform_to_dirform("admin/dashboard/__next._tree.txt") == \
        "admin/dashboard/__next._tree.txt"


def test_dotform_to_dirform_non_rsc_returns_none():
    assert _dotform_to_dirform("index.txt") is None
    assert _dotform_to_dirform("admin/network") is None
    assert _dotform_to_dirform("admin/network.html") is None
    assert _dotform_to_dirform("not-rsc.txt") is None
