# -*- coding: utf-8 -*-
"""Tests del Buscador educativo (B3): score con memoria + razones del corpus.

Regla de la casa: tests SIN red. Toda la red pasa por
``buscador._http_get_bytes`` (vía ``_http_get_text`` / ``_http_get_json``);
aquí se reemplaza por dobles.
"""

from datetime import datetime, timedelta, timezone

import pytest

from app import buscador, create_app

RSS_EJEMPLO = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Blog de la ciudad</title>
<item><title>La huerta comunitaria</title><link>https://blog.org/huerta</link>
<description>Cómo sembrar en común</description></item>
</channel></rss>"""

CDX_EJEMPLO = [["timestamp", "original"], ["20200101000000", "https://blog.org/huerta"]]

ZENODO_PAYLOAD = {
    "hits": {
        "hits": [
            {
                "doi": "10.5281/zenodo.99999999",
                "links": {"self_html": "https://zenodo.org/records/99999999"},
                "metadata": {
                    "title": "Papeleta de prueba",
                    "description": "Resumen",
                    "publication_date": "2026-01-02",
                    "creators": [{"name": "Alguien"}],
                },
            }
        ]
    }
}


@pytest.fixture(autouse=True)
def _sin_red(monkeypatch):
    def _boom(url, timeout=None, accept="*/*"):
        raise RuntimeError("sin red en tests")

    def _boom_json(url, timeout=None):
        raise RuntimeError("sin red en tests")

    monkeypatch.setattr(buscador, "_http_get_bytes", _boom)
    monkeypatch.setattr(buscador, "_http_get_json", _boom_json)
    monkeypatch.delenv("BUSCADOR_SEARXNG_URL", raising=False)


def _token_coordinador(client):
    client.post("/api/auth/register", json={"username": "max", "password": "clave-segura-1"})
    resp = client.post("/api/auth/login", json={"username": "max", "password": "clave-segura-1"})
    return resp.get_json()["token"]


def _siembra_feed_con_memoria(monkeypatch, client, tok):
    """Feed verificado e ingerido con longevidad Wayback grabada."""
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed", "titulo": "Blog de la ciudad"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    monkeypatch.setattr(buscador, "_http_get_text", lambda url, timeout=None: (200, RSS_EJEMPLO))
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: CDX_EJEMPLO)
    client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})
    client.post(f"/api/buscador/feeds/{fid}/ingerir", json={}, headers={"X-Auth-Token": tok})
    return fid


def test_score_cache_miss_luego_hit(client):
    r1 = client.get("/api/buscador/score?url=https://blog-ejemplo.com/post").get_json()
    assert r1["cache"] == "miss"
    assert r1["banda"] == "desconocida" and r1["razones"]
    r2 = client.get("/api/buscador/score?url=https://blog-ejemplo.com/post").get_json()
    assert r2["cache"] == "hit"
    assert r2["banda"] == r1["banda"] and r2["motor"] == r1["motor"]


def test_score_cache_caduca_con_ttl(app, client):
    client.get("/api/buscador/score?url=https://vieja.org/x")
    vieja = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat()
    conn = __import__("sqlite3").connect(app.config["DATABASE"])
    conn.execute("UPDATE buscador_scores SET scored_at = ? WHERE url = ?", (vieja, "https://vieja.org/x"))
    conn.commit()
    conn.close()
    r = client.get("/api/buscador/score?url=https://vieja.org/x").get_json()
    assert r["cache"] == "miss"  # la memoria caduca, se recalcula (P8)


def test_corpus_feed_aporta_procedencia_y_longevidad(monkeypatch, client):
    tok = _token_coordinador(client)
    _siembra_feed_con_memoria(monkeypatch, client, tok)
    data = client.get("/api/buscador?q=huerta").get_json()
    doc = next(r for r in data["resultados"] if r["url"] == "https://blog.org/huerta")
    assert doc["capa"] == "corpus"
    assert any("corpus verificado" in z for z in doc["razones"])
    assert any("20200101000000" in z for z in doc["razones"])


def test_corpus_semilla_materializada_es_verificada(client):
    tok = _token_coordinador(client)
    seeds = client.get("/api/buscador/seeds").get_json()["seeds"]
    verificada = next(s for s in seeds if s["verificada"])
    client.post(
        f"/api/buscador/seeds/{verificada['id']}/materializar", json={}, headers={"X-Auth-Token": tok}
    )
    data = client.get("/api/buscador/corpus?q=maxocracia").get_json()
    doc = next(r for r in data["resultados"] if r["url"] == verificada["url"])
    assert doc["banda"] == "verificada"
    assert any("materializada" in z for z in doc["razones"])


def test_score_endpoint_suma_razones_del_corpus(monkeypatch, client):
    tok = _token_coordinador(client)
    _siembra_feed_con_memoria(monkeypatch, client, tok)
    body = client.get("/api/buscador/score?url=https://blog.org/huerta").get_json()
    assert any("corpus verificado" in z for z in body["razones"])
    assert any("20200101000000" in z for z in body["razones"])


def test_cero_ocultacion_todas_las_capas_presentes(monkeypatch, client):
    tok = _token_coordinador(client)
    _siembra_feed_con_memoria(monkeypatch, client, tok)
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: ZENODO_PAYLOAD)
    d1 = client.get("/api/buscador?q=maxocracia").get_json()
    d2 = client.get("/api/buscador?q=huerta").get_json()
    capas = set(d1["por_capa"]) | set(d2["por_capa"])
    assert {"semillas", "corpus", "academica"} <= capas  # nada se oculta (P3)
    for r in d1["resultados"] + d2["resultados"]:
        assert r["url"] and r["banda"] in buscador.BANDAS and r["razones"]
