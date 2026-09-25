# -*- coding: utf-8 -*-
"""Actividad de la escuela en lenguaje natural (terminal).

Por defecto imprime una línea por acción relevante: quién (usuario local),
qué hizo, cómo salió y cuánto tardó. Se silencia con ``LOG_HUMANO=0`` (o
false/no/off). Nunca registra cuerpos, tokens ni cabeceras.

Cada ``LOG_METRICAS_CADA`` peticiones (default 100; 0 lo apaga) imprime un
resumen de métricas de la ventana.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from collections import Counter

from flask import Flask, g, request

from .db import get_db

log = logging.getLogger("escuela.actividad")
_HANDLER_MARCA = "_escuela_actividad_handler"
_RUTAS_SILENCIOSAS = ("/static/", "/favicon")

# Prefijos -> acción en lenguaje natural (orden: el más específico primero).
_ACCIONES = (
    ("/api/auth/login", "inició sesión"),
    ("/api/auth/register", "llegó como cuenta nueva"),
    ("/api/me/share-progress", "compartió su progreso"),
    ("/api/me/rounds", "miró sus rondas"),
    ("/api/me/idioma", "cambió su idioma"),
    ("/api/me", "revisó su perfil"),
    ("/api/tree", "miró el árbol de saberes"),
    ("/api/monitors", "miró los monitores"),
    ("/api/community/lights", "miró las luces de la ciudad"),
    ("/api/buscador/lupa", "examinó el historial de un artículo"),
    ("/api/buscador", "buscó en la ciudad"),
    ("/api/availability", "marcó su disponibilidad"),
    ("/api/meetings/generate", "generó la semana de encuentros"),
    ("/api/meetings", "miró sus encuentros"),
    ("/api/materials/", "abrió un material"),
    ("/api/suggest", "pidió una sugerencia"),
)

_metricas_lock = threading.Lock()
_metricas = {
    "total": 0,
    "ok": 0,
    "aviso": 0,
    "error": 0,
    "ms": 0.0,
    "acciones_ventana": Counter(),
}


def _env_flag(nombre, default):
    valor = os.environ.get(nombre)
    if valor is None:
        return default
    return valor.strip().lower() not in ("0", "false", "no", "off", "")


def _default_activo(app) -> bool:
    """ON por defecto en la plataforma; OFF en tests salvo LOG_HUMANO=1."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return False
    if os.environ.get("FLASK_ENV") == "testing":
        return False
    return not app.config.get("TESTING", False)


def _metricas_cada():
    try:
        return max(0, int(os.environ.get("LOG_METRICAS_CADA", "100")))
    except (TypeError, ValueError):
        return 100


class _StdoutActual(logging.StreamHandler):
    """Handler que re-apunta a sys.stdout en cada emisión (tests, reloader) y
    sobrevive a consolas cp1252: nunca revienta por un carácter."""

    def emit(self, record):
        self.stream = sys.stdout
        try:
            super().emit(record)
        except UnicodeEncodeError:
            msg = self.format(record)
            encoding = getattr(self.stream, "encoding", None) or "utf-8"
            safe = msg.encode(encoding, "replace").decode(encoding, "replace")
            self.stream.write(safe + self.terminator)


def _instalar_handler():
    if getattr(log, _HANDLER_MARCA, False):
        return
    handler = _StdoutActual()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S")
    )
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False
    setattr(log, _HANDLER_MARCA, True)


def actor():
    """Usuario local si la petición viene autenticada; visitante si no."""
    uid = getattr(g, "user_id", None)
    if not uid:
        return "un visitante"
    try:
        row = (
            get_db()
            .execute("SELECT username FROM users WHERE id = ?", (uid,))
            .fetchone()
        )
        if row and row["username"]:
            return str(row["username"])[:40]
    except Exception:
        pass
    return f"usuario #{uid}"


def describir(metodo, ruta):
    if ruta.startswith("/api/topics/"):
        if ruta.endswith("/test"):
            return "hizo un test"
        if ruta.endswith("/start"):
            return "empezó un tema"
        if ruta.endswith("/evidence"):
            return "aportó un material"
        if ruta.endswith("/request-mentorship"):
            return "pidió mentoría"
        if ruta.endswith("/mentorship/verify"):
            return "verificó una mentoría"
        if ruta.endswith("/round"):
            return "cerró una ronda"
        if ruta.endswith("/materials"):
            return "abrió la biblioteca del tema"
        return "abrió un tema"
    if ruta.startswith("/api/meetings/"):
        if ruta.endswith("/join"):
            return "se anotó a un encuentro"
        if ruta.endswith("/attend"):
            return "asistió a un encuentro"
    for prefijo, accion in _ACCIONES:
        if ruta.startswith(prefijo):
            return accion
    return f"{metodo} {ruta}"


def _resultado(status):
    if status >= 500:
        return "algo falló"
    if status == 401:
        return "sin sesión válida"
    if status == 403:
        return "sin permiso"
    if status == 429:
        return "frenado por el límite"
    if status >= 400:
        return "no salió"
    return "salió bien"


def reiniciar_metricas():
    with _metricas_lock:
        _metricas.update(
            {
                "total": 0,
                "ok": 0,
                "aviso": 0,
                "error": 0,
                "ms": 0.0,
                "acciones_ventana": Counter(),
            }
        )


def resumen_metricas():
    with _metricas_lock:
        total = _metricas["total"]
        if total == 0:
            return ""
        top = _metricas["acciones_ventana"].most_common(3)
        promedio = _metricas["ms"] / total
        linea = (
            f"[métricas] escuela · {total} acciones · {_metricas['ok']} bien · "
            f"{_metricas['aviso']} con aviso · {_metricas['error']} fallos · "
            f"{promedio:.0f} ms promedio"
        )
        if top:
            favoritas = ", ".join(f"{metodo} {ruta} ({n})" for (metodo, ruta), n in top)
            linea += f" · más frecuentes: {favoritas}"
        _metricas["acciones_ventana"] = Counter()
    log.info(linea)
    return linea


def _acumular(status, ms, metodo, ruta):
    with _metricas_lock:
        _metricas["total"] += 1
        _metricas["ms"] += ms
        if status >= 500:
            _metricas["error"] += 1
        elif status >= 400:
            _metricas["aviso"] += 1
        else:
            _metricas["ok"] += 1
        _metricas["acciones_ventana"][(metodo, ruta)] += 1
        total = _metricas["total"]
    cada = _metricas_cada()
    if cada and total % cada == 0:
        resumen_metricas()


def init_actividad(app: Flask) -> None:
    """Registra el narrador humano si LOG_HUMANO está activo (default: sí)."""
    activo = _env_flag("LOG_HUMANO", _default_activo(app))
    if not activo:
        return

    _instalar_handler()
    log.info(
        "[escuela] Narrando la actividad en la terminal · " "silenciar con LOG_HUMANO=0"
    )

    @app.before_request
    def _marcar_inicio():
        request.environ["escuela_act_t0"] = time.perf_counter()

    @app.after_request
    def _narrar(response):
        ruta = request.path or "/"
        if any(ruta.startswith(prefijo) for prefijo in _RUTAS_SILENCIOSAS):
            return response

        t0 = request.environ.get("escuela_act_t0")
        ms = (time.perf_counter() - t0) * 1000.0 if t0 else 0.0
        frase = describir(request.method, ruta)
        resultado = _resultado(response.status_code)
        sufijo = f" · {response.status_code}" if response.status_code >= 400 else ""
        log.info(f"{actor()} · escuela · {frase} · {resultado}{sufijo} ({ms:.0f} ms)")
        _acumular(response.status_code, ms, request.method, ruta)
        return response
