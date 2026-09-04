# -*- coding: utf-8 -*-
"""Tests del Buscador educativo (B2): corpus verificado.

Regla de la casa: tests SIN red. Toda la red pasa por
``buscador._http_get_bytes`` (vía ``_http_get_text`` / ``_http_get_json``);
aquí se reemplaza por dobles. Ningún test depende de internet.
"""

import sqlite3

import pytest

from app import buscador, create_app

RSS_EJEMPLO = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Blog de la ciudad</title>
<item><title>La huerta comunitaria</title><link>https://blog.org/huerta</link>
<description>Cómo sembrar en común</description><pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate></item>
<item><title>Riego por goteo</title><link>https://blog.org/riego</link>
<description>Ahorrar agua</description></item>
</channel></rss>"""

ATOM_EJEMPLO = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Canal</title>
<entry><title>Video de conteo</title><link href="https://videos.org/conteo"/>
<summary>Contar semillas</summary></entry>
</feed>"""

HTML_CON_TITULO = "<html><head><title>Blog vivo</title></head><body>hola</body></html>"


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


def _token_otro(client):
    client.post("/api/auth/register", json={"username": "lucia", "password": "clave-segura-2"})
    resp = client.post("/api/auth/login", json={"username": "lucia", "password": "clave-segura-2"})
    return resp.get_json()["token"]


def test_parse_feed_rss_y_atom():
    rss = buscador.parse_feed(RSS_EJEMPLO)
    assert len(rss) == 2
    assert rss[0]["url"] == "https://blog.org/huerta"
    assert "huerta" in rss[0]["titulo"].lower()

    atom = buscador.parse_feed(ATOM_EJEMPLO)
    assert len(atom) == 1
    assert atom[0]["url"] == "https://videos.org/conteo"


def test_feed_nace_candidato_e_idempotente(client):
    tok = _token_coordinador(client)
    r1 = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed", "tipo": "blog", "titulo": "Blog"},
        headers={"X-Auth-Token": tok},
    )
    assert r1.status_code == 201
    assert r1.get_json()["feed"]["verificada"] == 0

    r2 = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed", "tipo": "blog", "titulo": "Blog"},
        headers={"X-Auth-Token": tok},
    )
    assert r2.status_code == 201
    feeds = client.get("/api/buscador/feeds").get_json()["feeds"]
    assert len([f for f in feeds if f["url"] == "https://blog.org/feed"]) == 1


def test_feed_requiere_coordinador(client):
    _token_coordinador(client)
    otro = _token_otro(client)
    resp = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed"},
        headers={"X-Auth-Token": otro},
    )
    assert resp.status_code == 403


def test_verificar_feed_rss_ok(monkeypatch, client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    monkeypatch.setattr(buscador, "_http_get_text", lambda url, timeout=None: (200, RSS_EJEMPLO))
    ver = client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})
    assert ver.get_json()["feed"]["verificada"] == 1


def test_verificar_feed_html_con_titulo_ok(monkeypatch, client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    monkeypatch.setattr(buscador, "_http_get_text", lambda url, timeout=None: (200, HTML_CON_TITULO))
    ver = client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})
    assert ver.get_json()["feed"]["verificada"] == 1


def test_verificar_feed_404_no_verifica(monkeypatch, client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/muerto"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    monkeypatch.setattr(buscador, "_http_get_text", lambda url, timeout=None: (404, "nope"))
    ver = client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})
    assert ver.get_json()["feed"]["verificada"] == 0


def test_verificar_feed_sin_red_502(client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    resp = client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})
    assert resp.status_code == 502
    assert "fail_open" in resp.get_json()


def test_ingerir_exige_verificacion(client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    resp = client.post(f"/api/buscador/feeds/{fid}/ingerir", json={}, headers={"X-Auth-Token": tok})
    assert resp.status_code == 403


def test_ingerir_idempotente_y_corpus_busca(monkeypatch, client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    monkeypatch.setattr(buscador, "_http_get_text", lambda url, timeout=None: (200, RSS_EJEMPLO))
    client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})

    r1 = client.post(f"/api/buscador/feeds/{fid}/ingerir", json={}, headers={"X-Auth-Token": tok})
    assert r1.get_json()["ingeridos"] == 2
    r2 = client.post(f"/api/buscador/feeds/{fid}/ingerir", json={}, headers={"X-Auth-Token": tok})
    assert r2.get_json()["ingeridos"] == 2

    data = client.get("/api/buscador/corpus?q=huerta").get_json()
    assert any(r["url"] == "https://blog.org/huerta" for r in data["resultados"])
    assert all(r["capa"] == "corpus" for r in data["resultados"])

    unificada = client.get("/api/buscador?q=huerta").get_json()
    assert unificada["por_capa"].get("corpus", 0) >= 1


def test_materializar_semilla_verificada(client):
    tok = _token_coordinador(client)
    seeds = client.get("/api/buscador/seeds").get_json()["seeds"]
    verificada = next(s for s in seeds if s["verificada"])
    resp = client.post(
        f"/api/buscador/seeds/{verificada['id']}/materializar", json={}, headers={"X-Auth-Token": tok}
    )
    assert resp.status_code == 201
    doc = resp.get_json()["doc"]
    assert doc["url"] == verificada["url"]

    data = client.get("/api/buscador/corpus?q=maxocracia").get_json()
    assert data["resultados"]  # la semilla vive ahora en el corpus


def test_materializar_candidata_403(client):
    tok = _token_coordinador(client)
    nueva = client.post(
        "/api/buscador/seeds",
        json={"titulo": "Candidata", "url": "https://candidata.org/x"},
        headers={"X-Auth-Token": tok},
    ).get_json()["seed"]
    resp = client.post(
        f"/api/buscador/seeds/{nueva['id']}/materializar", json={}, headers={"X-Auth-Token": tok}
    )
    assert resp.status_code == 403


def test_corpus_degrada_a_like_sin_fts(monkeypatch, app, client):
    tok = _token_coordinador(client)
    fid = client.post(
        "/api/buscador/feeds",
        json={"url": "https://blog.org/feed"},
        headers={"X-Auth-Token": tok},
    ).get_json()["feed"]["id"]
    monkeypatch.setattr(buscador, "_http_get_text", lambda url, timeout=None: (200, RSS_EJEMPLO))
    client.post(f"/api/buscador/feeds/{fid}/verificar", json={}, headers={"X-Auth-Token": tok})
    client.post(f"/api/buscador/feeds/{fid}/ingerir", json={}, headers={"X-Auth-Token": tok})

    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute("DROP TABLE IF EXISTS buscador_docs_fts")
    conn.commit()
    conn.close()

    data = client.get("/api/buscador/corpus?q=huerta").get_json()
    assert any(r["url"] == "https://blog.org/huerta" for r in data["resultados"])


def test_wayback_first_capture_parsea(monkeypatch):
    monkeypatch.setattr(
        buscador,
        "_http_get_json",
        lambda url, timeout=None: [["timestamp", "original"], ["20120101000000", "https://blog.org/"]],
    )
    assert buscador.wayback_first_capture("https://blog.org/") == "20120101000000"
