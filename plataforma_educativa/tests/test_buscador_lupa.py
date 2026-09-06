# -*- coding: utf-8 -*-
"""Tests de la Lupa (B6): meta-panorama y diff de artículos.

Regla de la casa: tests SIN red. La lupa llama a
``buscador._http_get_json``; aquí se reemplaza por dobles.
"""

import pytest

from app import buscador
from app import lupa


def _rev(rid, usuario, resumen, tamano, fecha="2026-09-01T00:00:00Z"):
    return {"id": rid, "timestamp": fecha, "user": usuario,
            "comment": resumen, "size": tamano}


PANORAMA_PAYLOAD = {
    "query": {
        "pages": [
            {
                "title": "Prueba",
                "protection": [{"type": "edit", "level": "autoconfirmed"}],
                "revisions": [
                    _rev(30, "Automoderador", "Revertidos los cambios de 1.2.3.4", 5000),
                    _rev(29, "1.2.3.4", "agrego dato", 4900),
                    _rev(28, "~2026-1", "Deshecha la edición 27", 4950),
                    _rev(27, "Editora", "amplía sección", 9000),
                    _rev(26, "Editora", "inicio", 1000),
                ],
            }
        ]
    }
}


@pytest.fixture(autouse=True)
def _sin_red(monkeypatch):
    def _boom(url, timeout=None):
        raise RuntimeError("sin red en tests")

    monkeypatch.setattr(buscador, "_http_get_json", _boom)
    monkeypatch.delenv("BUSCADOR_SEARXNG_URL", raising=False)


def test_titulo_desde_url():
    assert lupa.titulo_desde_url("https://es.wikipedia.org/wiki/Fotos%C3%ADntesis") == "Fotosíntesis"
    assert lupa.titulo_desde_url("https://es.wikipedia.org/wiki/América_Latina#Historia") == "América Latina"
    assert lupa.titulo_desde_url("https://blog.org/x") == ""


def test_panorama_cuenta_hechos(monkeypatch):
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: PANORAMA_PAYLOAD)
    pano = lupa.panorama("Prueba")
    assert pano["titulo"] == "Prueba"
    assert pano["proteccion"] == [{"tipo": "edit", "nivel": "autoconfirmed"}]
    assert pano["muestra"] == 5
    assert pano["revertidas"] == 2  # Automoderador + Deshecha
    assert pano["anonimas"] == 2  # IP + cuenta temporal ~
    assert pano["top_editores"][0] == {"usuario": "Editora", "ediciones": 2, "bot": False}
    assert any(s["delta"] == 8000 for s in pano["saltos_tamano"])  # 1000 → 9000
    assert pano["indicios_guerra"] is False  # n < 10: el indicio exige muestra
    for r in pano["revisiones"]:
        assert {"revid", "fecha", "usuario", "resumen", "tamano", "reversion", "anonimo"} <= set(r)


def test_panorama_guerra_con_muestra(monkeypatch):
    revs = [_rev(i, f"anon{i}" if i % 2 else "XBot", "Revertida edición", 100)
            for i in range(100, 112)]
    payload = {"query": {"pages": [{"title": "Caliente", "protection": [], "revisions": revs}]}}
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: payload)
    pano = lupa.panorama("Caliente")
    assert pano["indicios_guerra"] is True
    assert pano["top_editores"][0]["bot"] is True


def test_panorama_articulo_inexistente_404(monkeypatch, client):
    monkeypatch.setattr(
        buscador, "_http_get_json",
        lambda url, timeout=None: {"query": {"pages": [{"title": "X", "missing": True}]}},
    )
    assert client.get("/api/buscador/lupa?titulo=X").status_code == 404


def test_diff_detecta_adjetivo_retirado():
    d = lupa.diff_palabras("el gobierno corrupto miente siempre", "el gobierno miente siempre")
    assert d["quitadas"] == ["corrupto"] and d["puestas"] == []
    assert d["n_quitadas_total"] == 1 and d["truncado"] is False


def test_diff_cuenta_totales_aunque_trunque():
    d = lupa.diff_palabras("a b c d", "a X Y Z", max_fragmentos=1)
    assert d["n_puestas_total"] == 3 and d["truncado"] is True


def test_comparar_trae_ambos_textos(monkeypatch):
    def _falsa(url, timeout=None):
        if "revids=1" in url:
            c = "el dictador benevolente habló"
        else:
            c = "el presidente habló"
        return {"query": {"pages": [{"revisions": [{"slots": {"main": {"content": c}}}]}]}}

    monkeypatch.setattr(buscador, "_http_get_json", _falsa)
    d = lupa.comparar("1", "2")
    assert d["de"] == 1 and d["a"] == 2
    assert any("dictador" in q or "benevolente" in q for q in d["quitadas"])
    assert any("presidente" in p for p in d["puestas"])


def test_endpoints_lupa(client):
    assert client.get("/api/buscador/lupa").status_code == 400
    assert client.get("/api/buscador/lupa/diff").status_code == 400
    assert client.get("/api/buscador/lupa/diff?de=1").status_code == 400
    assert client.get("/api/buscador/lupa/diff?de=x&a=y").status_code == 400
    body = client.get("/api/buscador/lupa?titulo=Prueba").get_json()
    assert body["fail_open"].startswith("wikipedia:")  # sin red: 502 honesto
    assert client.get("/api/buscador/lupa?titulo=Prueba").status_code == 502


def test_ui_lupa_con_timeline_y_diff():
    """La UI ofrece lupa en la referencia y visor de historial (B6 visible)."""
    import os

    raiz = os.path.join(os.path.dirname(__file__), "..")
    html = open(os.path.join(raiz, "templates", "index.html"), encoding="utf-8").read()
    js = open(os.path.join(raiz, "static", "app.js"), encoding="utf-8").read()
    for pedazo in ("lupa-q", "btn-lupa", "lupa-resultado"):
        assert pedazo in html
    for pedazo in ("abrirLupa", "renderLupa", "lupa/diff", "indicios_guerra"):
        assert pedazo in js


def test_lupa_acepta_url(client, monkeypatch):
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: PANORAMA_PAYLOAD)
    resp = client.get("/api/buscador/lupa?url=https://es.wikipedia.org/wiki/Prueba")
    assert resp.status_code == 200
    assert resp.get_json()["titulo"] == "Prueba"
