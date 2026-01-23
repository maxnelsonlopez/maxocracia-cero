import sqlite3
import os

DB_PATH = '/Users/Max/Otros documentos/maxocracia-cero/comun.db'
SCHEMA_PATH = '/Users/Max/Otros documentos/maxocracia-cero/app/schema.sql'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema)
        conn.commit()
        print("Migration successful: MaxoContracts tables created/verified.")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
