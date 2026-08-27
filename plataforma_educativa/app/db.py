# -*- coding: utf-8 -*-
"""Capa de acceso a datos de la Plataforma Educativa.

Usa la librería estándar ``sqlite3`` (no hace falta SQLAlchemy). Se crea una
conexión por petición, guardada en ``g`` y cerrada al terminar el contexto de
solicitud de Flask.
"""

import sqlite3

from flask import current_app, g


def get_db():
    """Devuelve la conexión SQLite de la petición en curso (la crea si no existe)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    """Cierra la conexión de la petición al terminar el contexto."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Registra el teardown que cierra la conexión por petición."""
    app.teardown_appcontext(close_db)


def query_db(query, args=(), one=False):
    """Ejecuta una consulta de lectura y devuelve filas (dict-like) o una sola."""
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    if one:
        return rows[0] if rows else None
    return rows


def execute_db(query, args=()):
    """Ejecuta una escritura y hace commit. Devuelve el cursor con lastrowid."""
    cur = get_db().execute(query, args)
    get_db().commit()
    return cur
