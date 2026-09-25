# -*- coding: utf-8 -*-
"""Narrador de actividad en terminal: lenguaje natural, silenciable y sin
secretos (nunca cuerpos, tokens, cabeceras ni correos completos)."""

import pytest

from app import actividad, create_app


@pytest.fixture(autouse=True)
def _metricas_limpias():
    actividad.reiniciar_metricas()
    yield
    actividad.reiniciar_metricas()


def _app(tmp_path):
    return create_app(db_path=str(tmp_path / "actividad.db"))


def test_describir_mapea_endpoints_conocidos():
    assert (
        actividad.describir("maxo.transfer", "POST", "/maxo/transfer")
        == "transfirió Maxo"
    )
    assert actividad.describir("auth.login", "POST", "/auth/login") == "inició sesión"
    assert actividad.describir("no.existe", "GET", "/raro") == "GET /raro"


def test_actor_prefiere_alias_y_enmascara_correo(app):
    with app.test_request_context("/"):
        from flask import request as flask_request

        flask_request.user = {"alias": "Ana", "email": "ana@dominio.org"}
        assert actividad.actor() == "Ana"

        flask_request.user = {"email": "ana@dominio.org"}
        assert actividad.actor() == "a***@dominio.org"

        flask_request.user = {}
        assert actividad.actor() == "un visitante"


def test_narra_sin_filtrar_secretos(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOG_HUMANO", "1")
    app = _app(tmp_path)
    app.config["TESTING"] = True
    client = app.test_client()

    resp = client.get(
        "/users", headers={"Authorization": "Bearer secreto-no-debe-salir"}
    )
    assert resp.status_code == 401

    client.post(
        "/auth/login",
        json={"email": "nadie@example.com", "password": "ClaveSecreta123!"},
    )

    out = capsys.readouterr().out
    assert "un visitante" in out
    assert "consultó el directorio" in out
    assert "inició sesión" in out
    assert "secreto-no-debe-salir" not in out
    assert "ClaveSecreta123" not in out


def test_silencio_con_log_humano_cero(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOG_HUMANO", "0")
    app = _app(tmp_path)
    app.config["TESTING"] = True
    app.test_client().get("/users")
    assert "consultó el directorio" not in capsys.readouterr().out


def test_resumen_metricas_cuenta_estados():
    actividad.reiniciar_metricas()
    actividad._acumular(200, 10.0, "auth.login")
    actividad._acumular(500, 30.0, "maxo.transfer")

    linea = actividad.resumen_metricas()
    assert "2 acciones" in linea
    assert "1 bien" in linea
    assert "1 fallos" in linea
    assert "inició sesión" in linea


def test_metricas_cada_emite_resumen(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOG_HUMANO", "1")
    monkeypatch.setenv("LOG_METRICAS_CADA", "2")
    app = _app(tmp_path)
    app.config["TESTING"] = True
    client = app.test_client()

    client.get("/users")
    client.get("/users")

    assert "[métricas] 2 acciones" in capsys.readouterr().out
