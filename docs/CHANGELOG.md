# Changelog

All notable changes to this project will be documented in this file.

Dates are ISO 8601 (YYYY-MM-DD). This changelog focuses on developer-facing changes: API, schema, DB seeds, and important operational notes.

## 2025-10-19 — Core API and interchanges

- Added `feature/core-api` branch and pushed to origin. PR URL suggested by remote:

  - https://github.com/maxnelsonlopez/maxocracia-cero/pull/new/feature/core-api

- Files added/changed (high level):

  - `app/interchanges.py` — new Flask blueprint implementing `/interchanges` POST and GET endpoints.
  - `app/maxo.py` — crediting helper used by the interchanges flow (`credit_user` and `get_balance`).
  - `app/__init__.py` — registered `interchanges` blueprint in the app factory.
  - `app/schema.sql` — SQLite schema updated (renamed `values` -> `values_json` to avoid reserved-word conflicts).
  - `run.py` — updated to read `PORT` environment variable (fallback 5000) to avoid local port conflicts.
  - `seeds/seed_demo.py` — fixed seed script to match updated schema and create `comun.db`.
  - `.gitignore` — ensured `comun.db` is ignored to keep DB out of the repo.

- Behavior and verification notes:

  - POSTing a test interchange (e.g. `interchange_id: INT-TEST-002`) creates an `interchanges` row and automatically inserts a `maxo_ledger` credit for the receiver.
  - Example verification query (performed during development):

    SELECT id, user_id, amount, note, created_at FROM maxo_ledger;

    Result (example):

    1 | 1 | 5.5 | Credit for interchange INT-TEST-002 | 2025-10-19 19:03:33

  - Server successfully run on a non-default port to avoid conflicts:

    PORT=5001 /usr/local/bin/python3 run.py

- Known limitations and follow-ups:
  - Seeds currently include plaintext demo passwords — update seeds to create hashed passwords before sharing publicly.
  - The Maxo crediting logic is minimal/heuristic. A formal Maxo specification and business rules should be implemented and documented.
  - No unit or integration tests yet — see TODO for adding pytest tests and CI.

## How this changelog is generated

This file is hand-maintained. For each feature/bugfix, add a short entry with files changed, a brief verification note, and any follow-ups.

---

Credits: generated during interactive development session between developer and assistant on 2025-10-19.

## 2025-10-20 — UI polish and security fixes

- Persist JWT in the browser UI and show user profile; use authenticated user ID for balance, transfers and claims.
- Add `/auth/me` endpoint to return profile information derived from the JWT.
- Harden `/maxo/transfer`: validate inputs, return helpful errors including current balance when funds are insufficient, perform ledger writes atomically.
- Improve client-side error handling to avoid uncaught exceptions in handlers that made UI buttons appear unresponsive.
- Seeded demo DB passwords updated to hashed values where plaintext remained.

