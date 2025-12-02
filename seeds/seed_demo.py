import sqlite3
import secrets
import string
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Configuración
DB = Path(__file__).resolve().parents[1] / "comun.db"
SCHEMA = Path(__file__).resolve().parents[1] / "app" / "schema.sql"


# Generar contraseñas seguras
def generate_secure_password(length=12):
    """Genera una contraseña segura que cumple con los requisitos de validación."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = "".join(secrets.choice(characters) for _ in range(length))
        # Asegurar que la contraseña cumple con los requisitos
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
        ):
            return password


# Datos de usuarios demo con contraseñas seguras
demo_users = [
    {
        "email": "alice@example.com",
        "name": "Alice",
        "alias": "alice",
        "password": generate_secure_password(),
    },
    {
        "email": "bob@example.com",
        "name": "Bob",
        "alias": "bob",
        "password": generate_secure_password(),
    },
    {
        "email": "admin@example.com",
        "name": "Admin",
        "alias": "admin",
        "password": generate_secure_password(),
        "is_admin": True,
    },
]


def init_db():
    """Inicializa la base de datos con el esquema y datos de prueba."""
    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Crear esquema
        with open(SCHEMA, "r", encoding="utf-8") as f:
            cur.executescript(f.read())

        # Insertar usuarios demo
        for user in demo_users:
            try:
                cur.execute(
                    """
                    INSERT INTO users (
                        email, name, alias, password_hash, is_admin, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        user["email"],
                        user["name"],
                        user["alias"],
                        generate_password_hash(user["password"]),
                        user.get("is_admin", False),
                        datetime.utcnow(),
                        datetime.utcnow(),
                    ),
                )
                print(
                    f"Usuario creado: {user['email']} - Contraseña: {user['password']}"
                )

            except sqlite3.IntegrityError as e:
                print(f"Advertencia: {user['email']} ya existe en la base de datos")
                conn.rollback()
            except Exception as e:
                print(f"Error al crear usuario {user['email']}: {str(e)}")
                conn.rollback()
                raise

        conn.commit()
        print(f"\nBase de datos inicializada correctamente en: {DB}")

    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print("Inicializando base de datos de prueba...")
    init_db()
    print("Seeded demo DB at", DB)
