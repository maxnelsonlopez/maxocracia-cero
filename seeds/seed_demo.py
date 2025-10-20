import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB = Path(__file__).resolve().parents[1] / 'comun.db'
SCHEMA = Path(__file__).resolve().parents[1] / 'app' / 'schema.sql'

conn = sqlite3.connect(DB)
cur = conn.cursor()
with open(SCHEMA, 'r', encoding='utf-8') as f:
    cur.executescript(f.read())

# insert demo users with hashed passwords
users = [
    ('alice@example.com', 'Alice', 'alice', 'password1'),
    ('bob@example.com', 'Bob', 'bob', 'password2')
]
for email, name, alias, pwd in users:
    try:
        cur.execute('INSERT INTO users (email, name, alias, password_hash) VALUES (?, ?, ?, ?)',
                    (email, name, alias, generate_password_hash(pwd)))
    except Exception:
        pass

conn.commit()
conn.close()
print('Seeded demo DB at', DB)
