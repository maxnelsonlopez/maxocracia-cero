# API & Usage (Flask + SQLite)

This document summarizes the API endpoints, data contracts, example curl commands including JWT authentication, how to run the app locally, and how to run tests.

## Getting started (local)

- Create virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

- Initialize DB and seed (optional):

```bash
python3 seeds/seed_demo.py
```

- Run server (choose a free port):

```bash
PORT=5001 python3 run.py
```

## Authentication (JWT)

Register a user:

```bash
curl -X POST http://127.0.0.1:5001/auth/register -H 'Content-Type: application/json' -d '{"email":"alice@example.com","password":"password1","name":"Alice"}'
```

Login and obtain token:

```bash
curl -s -X POST http://127.0.0.1:5001/auth/login -H 'Content-Type: application/json' -d '{"email":"alice@example.com","password":"password1"}' | jq -r '.token'
```

Use token in Authorization header:

```bash
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5001/maxo/1/balance
```

## Endpoints (summary)

- POST /auth/register

  - body: { email, password, name, alias }
  - returns 201 on success

- POST /auth/login

  - body: { email, password }
  - returns { token, user_id }

- GET /interchanges

  - returns list of interchanges

- POST /interchanges

  - body: { interchange_id, giver_id, receiver_id, uth_hours, impact_resolution_score, description }
  - on success returns { message, credit }

  - optional fields:
    - `uvc_score` (number): componente de Unidades de Vida Consumidas
    - `urf_units` (number): componente de Unidades de Recursos Finitos
  - credit formula (configurable):
    - `credit = uth_hours*MAXO_WEIGHT_UTH + impact_resolution_score*MAXO_WEIGHT_IMPACT + uvc_score*MAXO_WEIGHT_UVC + urf_units*MAXO_WEIGHT_URF`
    - defaults: `MAXO_WEIGHT_UTH=1.0`, `MAXO_WEIGHT_IMPACT=0.5`, `MAXO_WEIGHT_UVC=0.0`, `MAXO_WEIGHT_URF=0.0`
  - implementation: `app/maxo.py:12–26` y uso en `app/interchanges.py:35–44,27–33`

### VHV (Vector de Huella Vital)

- Definición: `VHV = (tiempo_total_consumido, seres_vivos_consumidos, recursos_consumidos)`.
- En `interchange` se almacena como:
  - `vhv_time_seconds` (número): segundos totales consumidos (por defecto `uth_hours*3600`).
  - `vhv_lives` (número): fracciones o enteros de vidas consumidas (por defecto `uvc_score` si se provee, o `0`).
  - `vhv_resources_json` (JSON texto): desglose de recursos (energía, agua, CO2, etc.).
- Body opcional en `POST /interchanges`:
  - `vhv_time_seconds`: número.
  - `vhv_lives`: número.
  - `vhv_resources`: objeto JSON.
- Notas:
  - VHV registra datos objetivos; la conversión a crédito usa pesos separados (ver fórmula de crédito).
  - Los campos VHV son opcionales; si no se envían, se derivan valores básicos para mantener compatibilidad.

- POST /reputation/review

  - body: { user_id, score }
  - adds/updates reputation average for the user

- GET /reputation/<user_id>

  - returns { user_id, score, reviews_count }

- POST /resources

  - body: { user_id, title, description, category }
  - creates a resource and returns 201

- GET /resources

  - returns list of available resources

- POST /resources/<id>/claim

  - body: { user_id }
  - claims a resource (marks unavailable)

- GET /maxo/<user_id>/balance

  - returns { user_id, balance }

- POST /maxo/transfer
  - protected (Authorization: Bearer <token>)
  - body: { from_user_id, to_user_id, amount, reason }
  - requires token user_id == from_user_id
 - enforces sufficient balance (no overdraft)

## Rate limiting

The API enforces per-endpoint rate limits using Flask-Limiter.

- Defaults (production):
  - `POST /auth/login`: `5 per minute`
  - `POST /auth/register`: `10 per hour`
  - `POST /auth/refresh`: `20 per hour`
  - General API: `200 per day`, `50 per hour`

- Testing behavior:
  - In testing (`app.config['TESTING']=True`) the defaults are permissive to avoid interfering with the suite.
  - Individual tests can override limits via `app.config`.

- Configuration keys (can be provided via app config or environment variables loaded at startup):
  - `RATELIMIT_LOGIN_LIMIT`: overrides login limit (e.g. `"5 per minute"`).
  - `RATELIMIT_REGISTER_LIMIT`: overrides register limit.
  - `RATELIMIT_REFRESH_LIMIT`: overrides refresh limit.
  - `RATELIMIT_AUTH_LIMIT`: legacy/fallback override used when endpoint-specific keys are not set.
  - `RATELIMIT_API_LIMIT`: override for general API limits.
  - `REDIS_URL`: storage backend for limiter (default `memory://` for local/testing). Example: `redis://localhost:6379/0`.

- Implementation details:
  - Limiter setup: `app/limiter.py:7–12`.
  - Dynamic endpoint limits: `app/limiter.py:33–72` (`LOGIN_LIMITS`, `REGISTER_LIMITS`, `REFRESH_LIMITS`).
  - Decorators applied in auth routes: `app/auth.py:24–26`, `app/auth.py:71–73`, `app/auth.py:200–202`.

- Error response example (HTTP 429):

```json
{
  "error": "Demasiadas peticiones",
  "message": "5 per 1 minute",
  "retry_after": 60
}
```

- Example: quickly hitting login limit

```bash
for i in $(seq 1 10); do
  curl -s -X POST http://127.0.0.1:5001/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"email":"alice@example.com","password":"password1"}' | jq -r '.error';
done
```

Notes:
- For production, prefer Redis storage (`REDIS_URL`) for accurate distributed rate limiting.
- The limiter key function is the remote address (client IP).

### Recommended production configuration

- Copy `config.example.env` to `.env` and set values:

```
SECRET_KEY=change_me_in_production
FLASK_ENV=production
PORT=5001
REDIS_URL=redis://localhost:6379/0
RATELIMIT_LOGIN_LIMIT="5 per minute"
RATELIMIT_REGISTER_LIMIT="10 per hour"
RATELIMIT_REFRESH_LIMIT="20 per hour"
RATELIMIT_API_LIMIT="50 per hour"
```

- Load the `.env` before running locally:

```bash
set -a
source .env
set +a
PORT=${PORT:-5001} python3 run.py
```

## Tests

Run the test suite locally:

```bash
python3 -m pytest -q
```

CI uses GitHub Actions (see `.github/workflows/ci.yml`) to run the same tests.

## I accidentally merged/closed the PR — what to do?

If you merged and closed the PR by mistake, you have options:

- Revert the merge commit on `main` and open a fresh PR from `feature/core-api`:

```bash
# on main
git checkout main
git pull
# find the merge commit SHA then
git revert <merge-sha>
# push the revert and open a new PR if needed
```

- Or open a new PR from `feature/core-api` (already pushed). The repo shows an active PR URL if one exists. If you want me to open a new PR or prepare a revert commit, I can do that — tell me which you'd prefer.

## Notes & Security

- Seeds now store password hashes (werkzeug). Demo passwords are still plain text in the seeds file and should only be used locally.
- JWT secret is `SECRET_KEY` env var; change it in production.
- The current Maxo crediting logic is simple and should be replaced with a formal spec before public deployment.

## Demo script

There's a small demo script at `scripts/demo.sh` that walks through register/login, creating an interchange, checking balances, transferring Maxo, creating and claiming a resource, and posting a reputation review. Run the server and then:

```bash
./scripts/demo.sh
```

---

Document created by the development session on 2025-10-19.
