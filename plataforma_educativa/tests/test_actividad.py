# -*- coding: utf-8 -*-
"""Narrador de actividad de la escuela: lenguaje natural, silenciable y sin
secretos (nunca cuerpos, tokens ni contraseñas)."""

import pytest

from app import actividad, create_app


@pytest.fixture(autouse=True)
def _metricas_limpias():
    actividad.reiniciar_metricas()
    yield
    actividad.reiniciar_metricas()


def _app(tmp_path):
    return create_app(db_path=str(tmp_path / "actividad.db"))


def test_describir_mapea_rutas():
    assert actividad.describir("POST", "/api/auth/login") == "inició sesión"
    assert (
        actividad.describir("POST", "/api/auth/register") == "llegó como cuenta nueva"
    )
    assert actividad.describir("POST", "/api/topics/3/test") == "hizo un test"
    assert actividad.describir("GET", "/api/topics/3") == "abrió un tema"
    assert (
        actividad.describir("POST", "/api/meetings/2/join") == "se anotó a un encuentro"
    )
    assert actividad.describir("GET", "/api/otra-cosa") == "GET /api/otra-cosa"


def test_narra_sin_filtrar_passwords(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOG_HUMANO", "1")
    app = _app(tmp_path)
    app.config["TESTING"] = True
    client = app.test_client()

    reg = client.post(
        "/api/auth/register",
        json={"username": "ana", "password": "ClaveSecreta123"},
    )
    assert reg.status_code == 201

    out = capsys.readouterr().out
    assert "llegó como cuenta nueva" in out
    assert "ClaveSecreta123" not in out


def test_actor_usa_el_username(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOG_HUMANO", "1")
    app = _app(tmp_path)
    app.config["TESTING"] = True
    client = app.test_client()

    token = client.post(
        "/api/auth/register",
        json={"username": "lucia", "password": "clave123"},
    ).get_json()["token"]
    capsys.readouterr()  # descartar la narración del registro

    client.get("/api/me", headers={"X-Auth-Token": token})

    assert "lucia · escuela" in capsys.readouterr().out


def test_silencio_con_log_humano_cero(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOG_HUMANO", "0")
    app = _app(tmp_path)
    app.config["TESTING"] = True
    app.test_client().get("/api/tree")
    assert "árbol" not in capsys.readouterr().out


def test_resumen_metricas_cuenta_estados():
    actividad.reiniciar_metricas()
    actividad._acumular(200, 5.0, "GET", "/api/tree")
    actividad._acumular(500, 60.0, "POST", "/api/topics/1/test")

    linea = actividad.resumen_metricas()
    assert "2 acciones" in linea
    assert "1 bien" in linea
    assert "1 fallos" in linea
