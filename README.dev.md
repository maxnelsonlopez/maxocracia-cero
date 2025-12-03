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
- POST /vhv/calculate
- GET /vhv/products

## Configuración de rate limiting

- Backend de almacenamiento:
  - Por defecto: `memory://` para desarrollo y pruebas.
  - Producción: usar Redis, por ejemplo `REDIS_URL=redis://localhost:6379/0`.

- Límites por endpoint (por defecto en producción):
  - `login`: `5 per minute`
  - `register`: `10 per hour`
  - `refresh`: `20 per hour`

- Overrides (en `app.config` o variables de entorno):
  - `RATELIMIT_LOGIN_LIMIT`, `RATELIMIT_REGISTER_LIMIT`, `RATELIMIT_REFRESH_LIMIT`.
  - Fallback: `RATELIMIT_AUTH_LIMIT` para compatibilidad si no se definen los específicos.
  - General API: `RATELIMIT_API_LIMIT`.

- Ejemplo de arranque con Redis y límite personalizado para login:

```bash
REDIS_URL=redis://localhost:6379/0 \
RATELIMIT_LOGIN_LIMIT="3 per minute" \
PORT=5001 python run.py
```

## Uso de archivo .env

- Crea un `.env` basado en `config.example.env` y ajusta valores.
- Carga las variables antes de arrancar:

```bash
set -a
source .env
set +a
python run.py
```

Notas:

- Para prototipado rápido las contraseñas en `seeds/seed_demo.py` están en claro; en producción usar hashing y no poner contraseñas reales en seeds.
