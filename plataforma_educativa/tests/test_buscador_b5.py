# -*- coding: utf-8 -*-
"""Tests del Buscador educativo (B5): capas abiertas directas sin docker.

Wikipedia (referencia) + OpenAlex (academia con DOI). Regla de la casa:
tests SIN red — ``buscador._http_get_json`` se reemplaza por dobles que
despachan según la URL pedida.
"""

import pytest

from app import buscador

WIKI_PAYLOAD = {
    "query": {
        "search": [
            {"title": "Fotosíntesis", "snippet": "La <span class=\"searchmatch\">fotosíntesis</span> es un proceso"},
            {"title": "Clorofila", "snippet": "Pigmento verde"},
        ]
    }
}

OPENALEX_PAYLOAD = {
    "results": [
        {
            "id": "https://openalex.org/W123",
            "doi": "https://doi.org/10.1234/ejemplo",
            "title": "Photosynthesis pathways",
            "publication_year": 2023,
            "authorships": [{"author": {"display_name": "Ana Ríos"}}],
            "abstract_inverted_index": {"Photosynthesis": [0], "converts": [1], "light": [2]},
            "cited_by_count": 42,
        },
        {
            "id": "https://openalex.org/W999",
            "doi": "",
            "title": "Sin DOI ni resumen",
            "publication_year": 2020,
            "authorships": [],
            "abstract_inverted_index": {},
            "cited_by_count": 0,
        },
    ]
}


@pytest.fixture(autouse=True)
def _sin_red(monkeypatch):
    def _falsa(url, timeout=None):
        if "wiki" in url:
            return WIKI_PAYLOAD
        if "openalex" in url:
            return OPENALEX_PAYLOAD
        raise RuntimeError("sin red en tests")

    monkeypatch.setattr(buscador, "_http_get_json", _falsa)
    monkeypatch.delenv("BUSCADOR_SEARXNG_URL", raising=False)


def test_wikipedia_parsea_y_construye_url():
    res = buscador.engine_wikipedia("fotosintesis")
    assert len(res) == 2
    assert res[0]["url"] == "https://es.wikipedia.org/wiki/Fotos%C3%ADntesis"
    assert res[0]["capa"] == "referencia" and res[0]["fuente"] == "wikipedia"
    assert "<span" not in res[0]["resumen"] and "fotosíntesis" in res[0]["resumen"]


def test_openalex_parsea_doi_y_citas():
    res = buscador.engine_openalex("photosynthesis")
    assert len(res) == 2
    assert res[0]["url"] == "https://doi.org/10.1234/ejemplo"
    assert res[0]["doi"] and "Ana Ríos" in res[0]["autores"]
    assert "42 citas" in res[0]["resumen"] and "Photosynthesis converts light" in res[0]["resumen"]
    assert res[1]["url"] == "https://openalex.org/W999"  # sin DOI: usa el id


def test_resumen_openalex_vacio_sin_indice():
    assert buscador._resumen_openalex({}) == ""
    assert buscador._resumen_openalex(None) == ""


def test_buscar_incluye_referencia_y_academica(client):
    data = client.get("/api/buscador?q=fotosintesis").get_json()
    assert data["por_capa"].get("referencia", 0) >= 1
    assert data["por_capa"].get("academica", 0) >= 1
    wiki = next(r for r in data["resultados"] if r["fuente"] == "wikipedia")
    assert wiki["banda"] == "rastreable"  # dominio abierto, honestidad intacta
    for r in data["resultados"]:
        assert r["url"] and r["banda"] in buscador.BANDAS and r["razones"]


def test_hermanas_wikimedia_comparten_motor():
    books = buscador.engine_wikibooks("fotosintesis")
    versi = buscador.engine_wikiversity("fotosintesis")
    assert books and books[0]["fuente"] == "wikibooks"
    assert books[0]["url"].startswith("https://es.wikibooks.org/wiki/")
    assert versi and versi[0]["fuente"] == "wikiversidad"
    assert versi[0]["url"].startswith("https://es.wikiversity.org/wiki/")


def test_orden_canonico_referencia_antes_que_academia(client):
    data = client.get("/api/buscador?q=fotosintesis").get_json()
    assert data["orden_capas"] == ["semillas", "corpus", "referencia", "academica", "web"]
    capas = [r["capa"] for r in data["resultados"]]
    assert "referencia" in capas and "academica" in capas
    assert capas.index("referencia") < capas.index("academica")
    fuentes = {r["fuente"] for r in data["resultados"] if r["capa"] == "referencia"}
    assert {"wikipedia", "wikibooks", "wikiversidad"} <= fuentes


def test_motores_caidos_son_fail_open(monkeypatch, client):
    monkeypatch.setattr(
        buscador, "_http_get_json", lambda url, timeout=None: (_ for _ in ()).throw(RuntimeError("caído"))
    )
    data = client.get("/api/buscador?q=maxocracia").get_json()
    assert any(f.startswith("wikipedia:") for f in data["motores_fail_open"])
    assert any(f.startswith("openalex:") for f in data["motores_fail_open"])
    assert data["por_capa"].get("semillas", 0) >= 1  # la búsqueda sigue
