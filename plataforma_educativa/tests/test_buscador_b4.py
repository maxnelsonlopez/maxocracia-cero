# -*- coding: utf-8 -*-
"""Tests del Buscador educativo (B4): juez LLM + cola nocturna + parlamento.

Regla de la casa: tests SIN red. El juez (``score_engine._chat_completions``)
se reemplaza por dobles; la cadena local→OpenRouter→nada se gobierna por
variables de entorno.
"""

import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from app import buscador, create_app
from app import score_engine


def _juez_ok(urls):
    return json.dumps(
        {
            "veredictos": [
                {"url": u, "banda": "rastreable", "razones": ["autor con nombre"]}
                for u in urls
            ]
        }
    )


@pytest.fixture(autouse=True)
def _sin_red(monkeypatch):
    def _boom(url, timeout=None, accept="*/*"):
        raise RuntimeError("sin red en tests")

    def _boom_json(url, timeout=None):
        raise RuntimeError("sin red en tests")

    monkeypatch.setattr(buscador, "_http_get_bytes", _boom)
    monkeypatch.setattr(buscador, "_http_get_json", _boom_json)
    monkeypatch.setattr(score_engine, "_INTERVALO", 0)
    monkeypatch.delenv("BUSCADOR_SEARXNG_URL", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "true")


def _token_coordinador(client):
    client.post("/api/auth/register", json={"username": "max", "password": "clave-segura-1"})
    resp = client.post("/api/auth/login", json={"username": "max", "password": "clave-segura-1"})
    return resp.get_json()["token"]


def _token_otro(client):
    client.post("/api/auth/register", json={"username": "lucia", "password": "clave-segura-2"})
    resp = client.post("/api/auth/login", json={"username": "lucia", "password": "clave-segura-2"})
    return resp.get_json()["token"]


# --------------------------------------------------------------------------
# El juez (score_engine)
# --------------------------------------------------------------------------

def test_juez_local_responde_con_motor_trazable(monkeypatch):
    vistos = {}

    def _falso(base_url, api_key, model, sistema, usuario):
        vistos["base"] = base_url
        vistos["rubrica"] = sistema
        return _juez_ok(["https://blog.org/a", "https://blog.org/b"])

    monkeypatch.setattr(score_engine, "_chat_completions", _falso)
    items = [
        {"url": "https://blog.org/a", "titulo": "A", "resumen": "", "fuente": "blog"},
        {"url": "https://blog.org/b", "titulo": "B", "resumen": "", "fuente": "blog"},
    ]
    veredictos, motor = score_engine.juzgar_lote(items)
    assert motor.startswith("jan:")
    assert [v["url"] for v in veredictos] == ["https://blog.org/a", "https://blog.org/b"]
    assert all(v["banda"] == "rastreable" and v["razones"] for v in veredictos)
    assert "PROCEDENCIA" in vistos["rubrica"]  # la rúbrica manda procedencia


def test_juez_tolera_prosa_y_banda_invalida(monkeypatch):
    monkeypatch.setattr(
        score_engine,
        "_chat_completions",
        lambda *a: 'Claro, aquí va:\n{"veredictos": [{"url": "https://x.org/", "banda": "confiable", "razones": []}]} fin.',
    )
    (v,), _ = score_engine.juzgar_lote([{"url": "https://x.org/", "titulo": "", "resumen": "", "fuente": ""}])
    assert v["banda"] == "desconocida"  # banda ajena → honesta, nunca inventada
    assert v["razones"]


def test_juez_falla_al_respaldo_openrouter(monkeypatch):
    llamadas = []

    def _falso(base_url, api_key, model, sistema, usuario):
        llamadas.append(base_url)
        if "localhost" in base_url:
            raise RuntimeError("hub apagado")
        return _juez_ok(["https://blog.org/a"])

    monkeypatch.setattr(score_engine, "_chat_completions", _falso)
    monkeypatch.setenv("OPENROUTER_API_KEY", "clave-de-prueba")
    (_, motor) = (None, None)
    veredictos, motor = score_engine.juzgar_lote([{"url": "https://blog.org/a", "titulo": "", "resumen": "", "fuente": ""}])
    assert motor.startswith("openrouter:")
    assert len(llamadas) == 2  # local falló, el respaldo respondió


def test_sin_juez_es_fail_open(monkeypatch):
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    with pytest.raises(score_engine.SinJuez):
        score_engine.juzgar_lote([{"url": "https://blog.org/a", "titulo": "", "resumen": "", "fuente": ""}])


# --------------------------------------------------------------------------
# Cola nocturna (Nivel 2)
# --------------------------------------------------------------------------

def test_cola_encola_y_ejecuta_con_juez(monkeypatch, client):
    tok = _token_coordinador(client)

    # El doble juzga URLs genéricas: responde a cada lote con sus propias urls.
    def _eco(base_url, api_key, model, sistema, usuario):
        import re

        urls = re.findall(r"https?://[^\s—]+", usuario)
        return _juez_ok(urls)

    monkeypatch.setattr(score_engine, "_chat_completions", _eco)
    n = client.post("/api/buscador/scoring/encolar", json={}, headers={"X-Auth-Token": tok}).get_json()["encoladas"]
    assert n > 0
    # Idempotente: encolar dos veces no duplica pendientes.
    n2 = client.post("/api/buscador/scoring/encolar", json={}, headers={"X-Auth-Token": tok}).get_json()["encoladas"]
    estado = client.get("/api/buscador/scoring/estado").get_json()
    assert estado["pendientes"] == n2 > 0

    ejecutado = client.post("/api/buscador/scoring/ejecutar", json={}, headers={"X-Auth-Token": tok}).get_json()
    assert ejecutado["procesadas"] > 0 and ejecutado["motor"].startswith("jan:")

    body = client.get("/api/buscador/score?url=https://doi.org/10.5281/zenodo.17526611").get_json()
    assert body["nivel"] == 2 and body["motor"].startswith("jan:")


def test_ejecutar_sin_juez_502_fail_open(monkeypatch, client):
    tok = _token_coordinador(client)
    monkeypatch.setenv("LOCAL_ORACLE_ENABLED", "false")
    client.post("/api/buscador/scoring/encolar", json={}, headers={"X-Auth-Token": tok})
    resp = client.post("/api/buscador/scoring/ejecutar", json={}, headers={"X-Auth-Token": tok})
    assert resp.status_code == 502
    assert "fail_open" in resp.get_json()


def test_ui_muestra_insignia_del_juez():
    """La UI distingue el veredicto del juez LLM (B4 visible)."""
    import os

    raiz = os.path.join(os.path.dirname(__file__), "..")
    js = open(os.path.join(raiz, "static", "app.js"), encoding="utf-8").read()
    assert "nivel_score" in js and "juez" in js


def test_scoring_requiere_coordinador(client):
    _token_coordinador(client)
    otro = _token_otro(client)
    assert client.post("/api/buscador/scoring/encolar", json={}, headers={"X-Auth-Token": otro}).status_code == 403
    assert client.post("/api/buscador/scoring/ejecutar", json={}, headers={"X-Auth-Token": otro}).status_code == 403


# --------------------------------------------------------------------------
# Parlamento de parámetros (patrón M9)
# --------------------------------------------------------------------------

def test_resolver_con_procedencia_y_cooldown(app, client):
    tok = _token_coordinador(client)
    r1 = client.post(
        "/api/buscador/parametros/buscador_zenodo_size/resolver",
        json={"valor": "8", "resolucion": "Asamblea 04-09-2026: más academia por búsqueda"},
        headers={"X-Auth-Token": tok},
    )
    assert r1.status_code == 201
    params = client.get("/api/buscador/parametros").get_json()["parametros"]
    assert params["buscador_zenodo_size"]["valor"] == "8"
    assert params["buscador_zenodo_size"]["procedencia"].startswith("parlamento-B4#")

    r2 = client.post(
        "/api/buscador/parametros/buscador_zenodo_size/resolver",
        json={"valor": "3", "resolucion": "Prisa de alguien"},
        headers={"X-Auth-Token": tok},
    )
    assert r2.status_code == 409  # la prisa no gobierna (anti-flip-flop)

    vieja = (datetime.now(timezone.utc) - timedelta(days=15)).isoformat()
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute("UPDATE buscador_parameter_resolutions SET created_at = ?", (vieja,))
    conn.commit()
    conn.close()
    r3 = client.post(
        "/api/buscador/parametros/buscador_zenodo_size/resolver",
        json={"valor": "3", "resolucion": "Asamblea posterior: menos ruido"},
        headers={"X-Auth-Token": tok},
    )
    assert r3.status_code == 201

    historial = client.get("/api/buscador/resoluciones").get_json()["resoluciones"]
    assert len(historial) == 2 and historial[0]["valor"] == "3"


def test_resolver_valida_entrada(client):
    tok = _token_coordinador(client)
    assert client.post(
        "/api/buscador/parametros/no_existe/resolver", json={"valor": "1", "resolucion": "X"},
        headers={"X-Auth-Token": tok},
    ).status_code == 404
    assert client.post(
        "/api/buscador/parametros/buscador_zenodo_size/resolver", json={"valor": "1", "resolucion": "  "},
        headers={"X-Auth-Token": tok},
    ).status_code == 400
    _token_otro(client)
    otro = client.post("/api/auth/login", json={"username": "lucia", "password": "clave-segura-2"}).get_json()["token"]
    assert client.post(
        "/api/buscador/parametros/buscador_zenodo_size/resolver", json={"valor": "1", "resolucion": "X"},
        headers={"X-Auth-Token": otro},
    ).status_code == 403
