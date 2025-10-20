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
