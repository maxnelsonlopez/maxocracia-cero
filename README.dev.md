# Dev README — Cómo arrancar el prototipo local (Flask + SQLite)

1. Crear un entorno virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Ejecutar el seed para crear `comun.db` si no existe:

```bash
python seeds/seed_demo.py
```

3. Arrancar la aplicación:

```bash
python run.py
```

Endpoints iniciales:

- POST /auth/register
- POST /auth/login
- GET /users
- GET /resources

Notas:

- Para prototipado rápido las contraseñas en `seeds/seed_demo.py` están en claro; en producción usar hashing y no poner contraseñas reales en seeds.
