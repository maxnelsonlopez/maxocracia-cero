# Implementación local recomendada: Flask + SQLite (Cero dependencias externas)

Este documento adapta el "Resumen de Documentación - Proyecto Común (Maxocracia)" para una implementación local sencilla usando Python Flask y SQLite. El objetivo es permitir prototipado rápido y ejecución totalmente local (sin servicios externos). Está pensado para desarrolladores que quieren comenzar con una base funcional y luego evolucionarla.

## Objetivo

Proporcionar una guía práctica, con estructuras de datos, endpoints mínimos, scripts de inicialización y buenas prácticas para implementar Común con Flask y SQLite.

---

## Principios de diseño

- Cero dependencias externas para el desarrollo inicial: Flask + SQLite + librerías Python estándar y ligeras (p. ej. SQLAlchemy, Flask-Login opcional).
- Código modular: separación entre modelos (data), rutas (API), servicios (lógica), y tareas (migrations, seeders).
- Fácil transición a producción: arquitectura que permita reemplazar SQLite por PostgreSQL y añadir servicios externos cuando sea necesario.

---

## Estructura sugerida del repositorio

```
/ (raíz)
├── app/
│   ├── __init__.py       # crea app Flask y configura DB
│   ├── models.py         # modelos SQLAlchemy
│   ├── schemas.py        # marshmallow schemas (opcional)
│   ├── auth.py           # endpoints y lógica de autenticación
│   ├── users.py          # endpoints relacionados a usuarios
│   ├── resources.py      # endpoints para recursos y necesidades
│   ├── maxo.py           # lógica de puntos Maxo
│   └── utils.py          # utilidades comunes
├── migrations/           # scripts de inicialización/migración
├── docs/
│   └── IMPLEMENTACION_FLASK_SQLITE.md
├── seeds/                # scripts para poblar DB de ejemplo
├── tests/                # pruebas unitarias mínimas
├── requirements.txt      # dependencias (si se desean)
├── run.py                # arranque de la app en dev
└── README.md
```

---

## Tecnologías mínimas recomendadas

- Python 3.10+
- Flask
- SQLAlchemy (ORM ligero) o usar sqlite3 directo si se quiere evitar ORM
- Alembic (opcional para migraciones) o script SQL simple
- Werkzeug/Flask-Login para autenticar (o token simple JWT si se prefiere)
- Marshmallow (opcional) para validación/serialización

> Nota: Para un prototipo purista "cero dependencias externas", puedes usar solo la librería estándar `sqlite3` y `flask`.

---

## Modelo de datos (SQLite) — Esquema inicial

A continuación se muestra un esquema inicial SQL para SQLite que cubre perfiles, intercambios (intercambios del VerityLedger), recursos/necesidades y reputación.

SQL para crear tablas principales:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  alias TEXT,
  password_hash TEXT,
  phone TEXT,
  city TEXT,
  neighborhood TEXT,
  values TEXT, -- JSON string of values/principles
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL UNIQUE,
  bio TEXT,
  skills TEXT, -- JSON string
  availability TEXT, -- JSON string
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE interchange (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  interchange_id TEXT UNIQUE,
  date TEXT,
  giver_id INTEGER,
  receiver_id INTEGER,
  type TEXT, -- JSON array/string
  description TEXT,
  urgency TEXT,
  uth_hours REAL,
  urf_description TEXT,
  economic_value_approx TEXT,
  impact_resolution_score INTEGER,
  reciprocity_status TEXT,
  human_dimension_attended TEXT, -- JSON
  facilitator_notes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (giver_id) REFERENCES users(id),
  FOREIGN KEY (receiver_id) REFERENCES users(id)
);

CREATE TABLE resources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  title TEXT,
  description TEXT,
  category TEXT,
  available BOOLEAN DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE reputation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  score REAL DEFAULT 0,
  reviews_count INTEGER DEFAULT 0,
  updated_at TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE maxo_ledger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  change_amount REAL,
  reason TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Endpoints REST mínimos (Flask)

A continuación los endpoints básicos para comenzar. Todos los endpoints deben devolver JSON y usar códigos HTTP apropiados.

Autenticación básica (sesiones simples o JWT):

- POST /auth/register — { email, password, name, alias }
- POST /auth/login — { email, password } -> token/session
- POST /auth/logout — invalidar sesión

Usuarios / Perfiles:

- GET /users — lista (paginada)
- GET /users/<id> — detalle de usuario
- POST /users — crear usuario (si no se usa /auth/register)
- PUT /users/<id> — actualizar perfil
- DELETE /users/<id> — eliminar cuenta (soft-delete recomendado)

Recursos y Necesidades:

- GET /resources — listar recursos / necesidades
- POST /resources — crear recurso/necesidad
- GET /resources/<id>
- PUT /resources/<id>
- DELETE /resources/<id>
- POST /resources/<id>/claim — solicitar ayuda (genera intercambio)

Intercambios (VerityLedger):

- GET /interchanges — listar intercambios
- POST /interchanges — crear registro de intercambio (Formulario A)
- GET /interchanges/<id>
- PUT /interchanges/<id>

Maxo / Puntos:

- GET /maxo/balance/<user_id>
- POST /maxo/transfer — { from_user, to_user, amount, reason }
- GET /maxo/ledger/<user_id>

Reputación y valoraciones:

- POST /reputation/<user_id>/review — { score, comment }
- GET /reputation/<user_id>

Dashboard / Estadísticas (resumen):

- GET /dashboard/summary — total intercambios, UTH total, tasa de resolución, participantes activos

---

## Lógica mínima para Maxo (borrador)

- Cada intercambio puede generar un crédito/debito de Maxos.
- Fórmula simple de ejemplo:
  - credit = uth_hours _ factor_uth + (impact_resolution_score) _ factor_impact
- Mantener `maxo_ledger` con todas las transacciones y calcular balance sumando `change_amount`.

---

## Seguridad y privacidad (para prototipo local)

- Almacenar hashes de contraseña (bcrypt recommended). No almacenar contraseñas en claro.
- Usar HTTPS en producción (localmente ok HTTP para prototipado).
- Validar y sanitizar todas las entradas (evitar SQL injection, XSS).
- No incluir datos sensibles en logs.

---

## Scripts útiles y comandos

- Inicializar DB (SQLite):

```bash
python - <<PY
import sqlite3
conn = sqlite3.connect('comun.db')
with open('app/schema.sql', 'r') as f:
    conn.executescript(f.read())
conn.close()
print('DB initialized')
PY
```

- Correr la app en modo desarrollo:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
python run.py
```

- Poblar datos de ejemplo (seeds):

```bash
python seeds/seed_demo.py
```

---

## Tests y calidad

- Añadir pruebas unitarias para modelos y endpoints (usar pytest/flask-testing).
- Tests básicos sugeridos:
  - Registro y login
  - Crear recurso y reclamarlo
  - Crear intercambio y calcular Maxo
  - Calificación/reputación

---

## Migración a producción (resumen)

- Reemplazar SQLite por PostgreSQL.
- Añadir Nginx + Gunicorn para servir la app.
- Configurar HTTPS (Let's Encrypt).
- Externalizar medios (S3/Cloud) y usar base de datos gestionada si es posible.
- Añadir mecanismos de escalado y monitorización.

---

## Notas finales y decisiones de diseño

- Empezar simple y migrar después que los requisitos se estabilicen.
- Mantener la transparencia de datos y permitir exportaciones CSV/JSON para auditoría.
- Documentar las fórmulas del Maxo y los cambios en un archivo `docs/maxo_spec.md`.

---

## Ejemplo: Implementación mínima (esqueleto de `run.py`)

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

---

## Siguientes pasos (acciones concretas)

1. Crear `app/schema.sql` con el SQL del apartado "Modelo de datos".
2. Implementar `app/__init__.py`, `app/models.py` y un par de endpoints (`/auth/register`, `/auth/login`, `/users`).
3. Escribir `seeds/seed_demo.py` para poblar la base de datos con datos de ejemplo.
4. Añadir pruebas básicas y CI local (GitHub Actions opcional si se usa remoto).

---

Si quieres, implemento el esqueleto del proyecto en el workspace (archivos, scripts, `schema.sql`, `run.py`, `app/__init__.py`, `app/models.py`, `app/auth.py`, `seeds/seed_demo.py`) y lo pruebo localmente. ¿Lo genero ahora?
