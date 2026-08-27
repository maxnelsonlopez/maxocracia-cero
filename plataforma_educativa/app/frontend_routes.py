# -*- coding: utf-8 -*-
"""Rutas del frontend estático (servido por Flask, sin build)."""

from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__)


@frontend_bp.route("/")
def index():
    """Sirve la aplicación de una sola página (login + perfil + árbol)."""
    return render_template("index.html")
