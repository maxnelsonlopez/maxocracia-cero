# -*- coding: utf-8 -*-
"""Tests del feed público del Concilio (ventana pública, T13).

GET /verificador/concilio/feed y /verificador/concilio/cycles/<id>:
sin login, curado (misiones + consenso), sin bitácora cruda ni secretos.
"""

import json


def _ciclo(ws, cid, consenso=1.0, con_resumen=True):
    d = ws / "cycles" / cid
    d.mkdir(parents=True)
    (d / "ciclo.json").write_text(
        json.dumps(
            {
                "cycle_id": cid,
                "consensus": consenso,
                "ejecutable": True,
                "quorum_ok": True,
                "oraculos": ["Economic", "Dissident"],
                "motores": [{"engine": "deepseek", "model": "deepseek-chat"}],
            }
        ),
        encoding="utf-8",
    )
    if con_resumen:
        (d / "resumen.md").write_text(
            "# Resumen\n\n**Elegidas:**\n"
            "1. Regar las matas de la plaza — approve (95%)\n"
            "2. Pintar la banca rota — approve (80%)\n",
            encoding="utf-8",
        )
    return d


def test_feed_publico_sin_login(client, tmp_path, monkeypatch):
    ws = tmp_path / "ws"
    _ciclo(ws, "ciclo-20260925-120552-aaa")
    _ciclo(ws, "ciclo-20260924-101307-bbb", consenso=0.8)
    monkeypatch.setenv("CONCILIO_WORKSPACE", str(ws))

    res = client.get("/verificador/concilio/feed")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 2
    primero = data["ciclos"][0]
    assert primero["cycle_id"] == "ciclo-20260925-120552-aaa"
    assert primero["consenso"] == 1.0
    assert primero["ejecutable"] is True
    assert "Regar las matas de la plaza" in primero["elegidas"][0]
    assert "deepseek/deepseek-chat" in primero["motores"]
    assert "resumen" not in primero  # el feed es curado, no crudo


def test_feed_sin_workspace_devuelve_vacio(client, tmp_path, monkeypatch):
    monkeypatch.setenv("CONCILIO_WORKSPACE", str(tmp_path / "vacio"))
    res = client.get("/verificador/concilio/feed")
    assert res.status_code == 200
    assert res.get_json() == {"ciclos": [], "count": 0}


def test_detalle_de_ciclo(client, tmp_path, monkeypatch):
    ws = tmp_path / "ws"
    _ciclo(ws, "ciclo-20260925-120552-aaa")
    monkeypatch.setenv("CONCILIO_WORKSPACE", str(ws))

    res = client.get("/verificador/concilio/cycles/ciclo-20260925-120552-aaa")
    assert res.status_code == 200
    data = res.get_json()
    assert "Regar las matas" in data["resumen"]
    assert len(data["elegidas"]) == 2


def test_ciclo_inexistente_y_traversal(client, tmp_path, monkeypatch):
    ws = tmp_path / "ws"
    (ws / "cycles").mkdir(parents=True)
    monkeypatch.setenv("CONCILIO_WORKSPACE", str(ws))

    assert client.get("/verificador/concilio/cycles/no-existe").status_code == 404
    assert client.get("/verificador/concilio/cycles/..").status_code == 404
    assert client.get("/verificador/concilio/cycles/a%2Fb").status_code == 404
