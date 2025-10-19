import sqlite3
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app=None):
    from pathlib import Path
    if app is None:
        from flask import current_app
        app = current_app
    db_path = app.config['DATABASE']
    schema_path = Path(app.root_path) / 'schema.sql'
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print('Initialized DB at', db_path)
