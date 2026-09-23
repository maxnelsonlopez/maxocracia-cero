# -*- coding: utf-8 -*-
"""Tests de la negociación de contenido página-vs-API (llegada en producción).

En producción Flask sirve el frontend estático y las rutas API hacen sombra
a las páginas (/contracts/<id>, /contracts, /tvi/stats, /vhv/parameters):
al navegador (Accept: text/html) se le sirve el shell; a la API el JSON.
Sin build exportado se degrada al JSON (este repo no versiona dist/).
"""

from app.utils import (
    client_prefers_html,
    contract_shell_for,
    serve_frontend_shell,
)

HTML = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
JSON = {"Accept": "application/json"}


def test_contract_shell_for_rutas_dinamicas():
    assert contract_shell_for("negotiate") == "contracts/negotiate.html"
    assert (
        contract_shell_for("123e4567-e89b-12d3-a456-426614174000")
        == "contracts/placeholder.html"
    )
    assert contract_shell_for("from-need-3-7") == "contracts/placeholder.html"


def test_contract_shell_for_sin_pagina():
    assert contract_shell_for("stats") is None
    assert contract_shell_for("builder") is None
    assert contract_shell_for("") is None
    assert contract_shell_for("../../../etc/passwd") is None


def test_client_prefers_html_navegacion_vs_api(app):
    with app.test_request_context("/", headers=HTML):
        assert client_prefers_html() is True
    with app.test_request_context("/", headers=JSON):
        assert client_prefers_html() is False
    with app.test_request_context("/"):
        assert client_prefers_html() is False


def test_serve_frontend_shell_con_dist(app, tmp_path):
    (tmp_path / "pagina.html").write_text("<html></html>", encoding="utf-8")
    with app.test_request_context("/"):
        resp = serve_frontend_shell("pagina.html", dist_dir=str(tmp_path))
        assert resp is not None
        assert resp.status_code == 200
        assert serve_frontend_shell("ausente.html", dist_dir=str(tmp_path)) is None


def test_navegador_recibe_la_pagina_en_produccion(client):
    # Con build exportado (app/static/dist) el navegador recibe HTML y la
    # página hidrata por API ya autenticada: la llegada no rompe.
    uuid = "123e4567-e89b-12d3-a456-426614174000"
    for path in (
        "/contracts/",
        "/contracts/negotiate",
        f"/contracts/{uuid}",
        "/tvi/stats",
        "/vhv/parameters",
    ):
        res = client.get(path, headers=HTML)
        assert res.status_code == 200, path
        assert "text/html" in res.content_type, path


def test_id_desconocido_sirve_placeholder_al_navegador(client):
    # El blueprint contracts aliasa cualquier id al shell placeholder
    # (before_request propio, previo a este cambio): el navegador nunca ve
    # un JSON crudo; la API con Accept json sí recibe su 401/404.
    res = client.get("/contracts/zzz-no-es-id", headers=HTML)
    assert res.status_code == 200
    assert "text/html" in res.content_type
    res = client.get("/contracts/zzz-no-es-id", headers=JSON)
    assert res.status_code in (401, 404)
    assert res.is_json


def test_api_no_afectada_por_la_negociacion(client):
    res = client.get("/vhv/parameters", headers=JSON)
    assert res.status_code == 200
    assert "alpha" in res.get_json()
