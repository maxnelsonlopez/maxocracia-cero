import sqlite3
from typing import Callable, Dict, Optional, Union

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app=None):
    from pathlib import Path

    if app is None:
        from flask import current_app

        app = current_app
    db_path = app.config["DATABASE"]
    schema_path = Path(app.root_path) / "schema.sql"
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    # Migración idempotente para BDs existentes: token_version permite
    # revocar los JWT al cerrar sesión (CREATE TABLE IF NOT EXISTS no altera).
    user_cols = [row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
    if "token_version" not in user_cols:
        conn.execute(
            "ALTER TABLE users ADD COLUMN token_version INTEGER NOT NULL DEFAULT 0"
        )
    conn.commit()
    conn.close()
    print("Initialized DB at", db_path)


# --- Shells del frontend estático (la llegada no puede romper) ---
# El frontend se exporta estático (Next `output: 'export'`) y Flask lo sirve
# desde app/static/dist. Las páginas cuyas rutas API hacen sombra a la página
# en producción (/tvi/stats, /vhv/parameters) negocian contenido con el
# decorador frontend_shell: al navegador (Accept: text/html) se le sirve el
# HTML; a la API (fetch con Accept */* o application/json) el JSON de siempre.
# El blueprint contracts tiene su propio mecanismo previo y más general
# (before_request _serve_frontend_collisions en contracts_bp.py, con alias a
# placeholder y payloads RSC): no se duplica aquí. Sin build exportado todo
# degrada al JSON (los tests corren sin dist salvo app/static/dist).


def client_prefers_html() -> bool:
    """True si la petición es navegación de navegador (pide HTML, no JSON)."""
    from flask import request

    accept = request.headers.get("Accept", "")
    return "text/html" in accept and "application/json" not in accept


def contract_shell_for(contract_id: str) -> Optional[str]:
    """Shell estático para una ruta /contracts/<id>; None si no hay página."""
    import re

    cid = (contract_id or "").strip()
    if cid == "negotiate":
        return "contracts/negotiate.html"
    if re.fullmatch(r"[0-9a-fA-F-]{36}", cid) or cid.startswith("from-need-"):
        return "contracts/placeholder.html"
    return None


def serve_frontend_shell(dist_rel: str, dist_dir: Optional[str] = None):
    """Sirve el HTML estático si existe; None si no hay build exportado."""
    import os

    from flask import current_app, send_from_directory

    if dist_dir is None:
        dist_dir = os.path.join(current_app.root_path, "static", "dist")
    if os.path.exists(os.path.join(dist_dir, dist_rel)):
        return send_from_directory(dist_dir, dist_rel)
    return None


def resolve_user_id(db, ref):
    """Resuelve un id, alias o correo de usuario a su id (directorio de calle).

    En la calle nadie se sabe un id numérico: se transfiere al alias o al
    correo del vecino. Retorna None si no hay coincidencia exacta.
    """
    if ref is None:
        return None
    try:
        candidate = int(ref)
        if candidate > 0:
            row = db.execute(
                "SELECT id FROM users WHERE id = ?", (candidate,)
            ).fetchone()
            return row[0] if row else None
    except (ValueError, TypeError):
        pass
    text = str(ref).strip()
    if not text:
        return None
    row = db.execute("SELECT id FROM users WHERE alias = ?", (text,)).fetchone()
    if row:
        return row[0]
    row = db.execute("SELECT id FROM users WHERE email = ?", (text.lower(),)).fetchone()
    return row[0] if row else None


def frontend_shell(dist_rel_or_fn: Union[str, Callable[[Dict], Optional[str]]]):
    """Decorador: sirve el shell HTML al navegador antes que el JSON.

    Va POR FUERA de @token_required (más arriba) para que la navegación sin
    token reciba la página y el JS pida la API ya autenticado.
    """

    from functools import wraps

    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if client_prefers_html():
                rel = (
                    dist_rel_or_fn(kwargs)
                    if callable(dist_rel_or_fn)
                    else dist_rel_or_fn
                )
                if rel:
                    shell = serve_frontend_shell(rel)
                    if shell is not None:
                        return shell
            return fn(*args, **kwargs)

        return wrapper

    return deco
