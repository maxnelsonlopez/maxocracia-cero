# -*- coding: utf-8 -*-
"""Tests del Buscador educativo (B1): semillas, fail-open, score Nivel 1.

Regla de la casa: tests SIN red. El motor HTTP (``buscador._http_get_json``)
se reemplaza por dobles — levantar excepción (fail-open) o devolver payloads
canned. Ningún test depende de internet ni de SearXNG instalado.
"""

import sqlite3

import pytest

from app import buscador, create_app

# --------------------------------------------------------------------------
# Dobles de red (payloads canned)
# --------------------------------------------------------------------------

ZENODO_PAYLOAD = {
    "hits": {
        "hits": [
            {
                "doi": "10.5281/zenodo.99999999",
                "links": {"self_html": "https://zenodo.org/records/99999999"},
                "metadata": {
                    "title": "Papeleta de prueba",
                    "description": "<p>Resumen &nbsp;con <b>HTML</b> ruidoso</p>",
                    "publication_date": "2026-01-02",
                    "creators": [{"name": "Lopez Restrepo, Max Nelson Hernando"}],
                },
            }
        ]
    }
}

SEARX_PAYLOAD = {
    "results": [
        {"title": "Resultado web", "url": "https://ejemplo.org/a", "content": "contenido", "engine": "mojeek"}
    ]
}

WAYBACK_PAYLOAD = {
    "url": "https://muerto.org/pagina",
    "archived_snapshots": {
        "closest": {
            "url": "https://web.archive.org/web/20250101000000/https://muerto.org/pagina",
            "timestamp": "20250101000000",
            "status": "200",
        }
    },
}


@pytest.fixture(autouse=True)
def _sin_red(monkeypatch):
    """Por defecto, TODO intento de red levanta excepción (fail-open visible)."""

    def _boom(url, timeout=None):
        raise RuntimeError("sin red en tests")

    monkeypatch.setattr(buscador, "_http_get_json", _boom)
    monkeypatch.delenv("BUSCADOR_SEARXNG_URL", raising=False)


# --------------------------------------------------------------------------
# Helpers de autenticación (el primer usuario registrado es coordinador)
# --------------------------------------------------------------------------

def _token_coordinador(client):
    client.post("/api/auth/register", json={"username": "max", "password": "clave-segura-1"})
    resp = client.post("/api/auth/login", json={"username": "max", "password": "clave-segura-1"})
    return resp.get_json()["token"]


def _token_otro(client):
    client.post("/api/auth/register", json={"username": "lucia", "password": "clave-segura-2"})
    resp = client.post("/api/auth/login", json={"username": "lucia", "password": "clave-segura-2"})
    return resp.get_json()["token"]


# --------------------------------------------------------------------------
# Semillas canónicas
# --------------------------------------------------------------------------

def test_semasillas_canonicas_sembradas(client):
    seeds = client.get("/api/buscador/seeds").get_json()["seeds"]
    claves = {s["seed_key"] for s in seeds}
    assert "zenodo:10.5281/zenodo.17526611" in claves
    assert len([s for s in seeds if s["verificada"]]) >= 6   # 5 DOI + GitHub
    assert len([s for s in seeds if not s["verificada"]]) >= 2  # video + grokipedia


def test_sync_idempotente(app, client):
    same = create_app(db_path=app.config["DATABASE"])
    n1 = len(client.get("/api/buscador/seeds").get_json()["seeds"])
    n2 = len(same.test_client().get("/api/buscador/seeds").get_json()["seeds"])
    assert n1 == n2 > 0


def test_sync_no_revierte_verificacion_humana(app):
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute("UPDATE buscador_seeds SET verificada = 1 WHERE seed_key = 'video:youtube:H0erSu3377Y'")
    conn.commit()
    conn.close()
    buscador.sync_seeds_file(app.config["DATABASE"])
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    fila = conn.execute(
        "SELECT verificada FROM buscador_seeds WHERE seed_key = 'video:youtube:H0erSu3377Y'"
    ).fetchone()
    conn.close()
    assert fila["verificada"] == 1


# --------------------------------------------------------------------------
# Búsqueda unificada y fail-open
# --------------------------------------------------------------------------

def test_buscar_devuelve_bloque_verificado_y_reporta_zenodo_caido(client):
    data = client.get("/api/buscador?q=maxocracia").get_json()
    assert data["por_capa"].get("semillas", 0) >= 1
    assert any(
        r["capa"] == "semillas" and r["banda"] == "verificada" for r in data["resultados"]
    )
    assert any(f.startswith("zenodo:") for f in data["motores_fail_open"])
    for r in data["resultados"]:
        assert r["url"] and r["banda"] in buscador.BANDAS and r["razones"]


def test_semilla_candidata_aparece_con_banda_honesta(client):
    data = client.get("/api/buscador?q=maxocracia").get_json()
    semillas = [r for r in data["resultados"] if r["capa"] == "semillas"]
    verificadas = [s for s in semillas if s["verificada"]]
    candidatas = [s for s in semillas if not s["verificada"]]
    assert verificadas and candidatas
    assert semillas.index(verificadas[0]) < semillas.index(candidatas[-1])
    for c in candidatas:
        assert c["banda"] == "rastreable"


def test_buscar_sin_query_400(client):
    assert client.get("/api/buscador").status_code == 400


def test_zenodo_engine_parsea(monkeypatch):
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: ZENODO_PAYLOAD)
    res = buscador.engine_zenodo("prueba")
    assert res[0]["url"] == "https://doi.org/10.5281/zenodo.99999999"
    assert res[0]["fecha"] == "2026-01-02"
    assert "Lopez Restrepo" in res[0]["autores"]
    assert "<b>" not in res[0]["resumen"] and "HTML" in res[0]["resumen"]


def test_searxng_solo_con_configuracion(monkeypatch, client):
    data = client.get("/api/buscador?q=maxocracia").get_json()
    assert "web" not in data["por_capa"]

    monkeypatch.setenv("BUSCADOR_SEARXNG_URL", "http://127.0.0.1:8888")
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: SEARX_PAYLOAD)
    data = client.get("/api/buscador?q=maxocracia").get_json()
    assert data["por_capa"].get("web") == 1
    web = next(r for r in data["resultados"] if r["capa"] == "web")
    assert web["banda"] == "desconocida"  # dominio cualquiera: honestidad, no exclusión


def test_searxng_caido_es_fail_open(monkeypatch, client):
    monkeypatch.setenv("BUSCADOR_SEARXNG_URL", "http://127.0.0.1:8888")
    data = client.get("/api/buscador?q=maxocracia").get_json()
    assert any(f.startswith("searxng:") for f in data["motores_fail_open"])
    assert data["por_capa"].get("semillas", 0) >= 1  # la búsqueda sigue


def test_formato_searx(client):
    data = client.get("/api/buscador?q=maxocracia&format=searx").get_json()
    assert data["results"]
    for r in data["results"]:
        assert {"title", "url", "content"} <= set(r)


# --------------------------------------------------------------------------
# Score de confiabilidad Nivel 1
# --------------------------------------------------------------------------

def test_score_semilla_verificada(client):
    body = client.get("/api/buscador/score?url=https://doi.org/10.5281/zenodo.17526611").get_json()
    assert body["banda"] == "verificada"
    assert body["motor"] == "heuristico:v1"


def test_score_doi_rastreable(client):
    body = client.get("/api/buscador/score?url=https://doi.org/10.9999/nope.1").get_json()
    assert body["banda"] == "rastreable"
    assert any("DOI" in r for r in body["razones"])


def test_score_desconocida_con_razones(client):
    body = client.get("/api/buscador/score?url=https://blog-ejemplo.com/post").get_json()
    assert body["banda"] == "desconocida"
    assert any("HTTPS" in r for r in body["razones"])
    assert any("excluida" in r for r in body["razones"])  # etiqueta, no censura


def test_score_dominio_abierto(client):
    body = client.get("/api/buscador/score?url=https://es.wikipedia.org/wiki/Conteo").get_json()
    assert body["banda"] == "rastreable"


# --------------------------------------------------------------------------
# Wayback Machine (rescate de memoria)
# --------------------------------------------------------------------------

def test_archivo_rescate(monkeypatch, client):
    monkeypatch.setattr(buscador, "_http_get_json", lambda url, timeout=None: WAYBACK_PAYLOAD)
    body = client.get("/api/buscador/archivo?url=https://muerto.org/pagina").get_json()
    assert body["archivo"]["snapshot_url"].startswith("https://web.archive.org/web/")
    assert body["archivo"]["timestamp"] == "20250101000000"


def test_archivo_fail_open(client):
    body = client.get("/api/buscador/archivo?url=https://muerto.org/pagina").get_json()
    assert body["archivo"] is None
    assert "wayback" in body["fail_open"]


# --------------------------------------------------------------------------
# Siembra y verificación (regla M15: solo coordinador)
# --------------------------------------------------------------------------

def test_siembra_requiere_coordinador(client):
    _token_coordinador(client)  # el primer registro es coordinador
    otro = _token_otro(client)  # el segundo, no
    resp = client.post(
        "/api/buscador/seeds",
        json={"titulo": "Blog", "url": "https://blog.org/x"},
        headers={"X-Auth-Token": otro},
    )
    assert resp.status_code == 403


def test_siembra_valida_url(client):
    tok = _token_coordinador(client)
    resp = client.post(
        "/api/buscador/seeds",
        json={"titulo": "Rara", "url": "ftp://rara.org/x"},
        headers={"X-Auth-Token": tok},
    )
    assert resp.status_code == 400


def test_coordinador_siembra_candidata_y_verifica(client):
    tok = _token_coordinador(client)
    resp = client.post(
        "/api/buscador/seeds",
        json={
            "titulo": "Blog independiente",
            "url": "https://blogindependiente.org/feed",
            "tipo": "blog",
            "etiquetas": "educacion,blog",
        },
        headers={"X-Auth-Token": tok},
    )
    assert resp.status_code == 201
    seed = resp.get_json()["seed"]
    assert seed["verificada"] == 0  # nace candidata (regla M15)

    ver = client.post(
        f"/api/buscador/seeds/{seed['id']}/verificar", json={}, headers={"X-Auth-Token": tok}
    )
    assert ver.get_json()["seed"]["verificada"] == 1

    data = client.get("/api/buscador?q=independiente").get_json()
    assert any(s["url"] == "https://blogindependiente.org/feed" for s in data["resultados"])


def test_verificar_inexistente_404(client):
    tok = _token_coordinador(client)
    resp = client.post("/api/buscador/seeds/99999/verificar", json={}, headers={"X-Auth-Token": tok})
    assert resp.status_code == 404


# --------------------------------------------------------------------------
# Parámetros gobernable (B4: parlamento)
# --------------------------------------------------------------------------

def test_parametros_canon(client):
    body = client.get("/api/buscador/parametros").get_json()["parametros"]
    assert body["buscador_zenodo_size"]["valor"] == "5"
    assert body["buscador_zenodo_size"]["procedencia"] == "canon-B1"
    assert body["buscador_score_ttl_dias"]["valor"] == "90"
