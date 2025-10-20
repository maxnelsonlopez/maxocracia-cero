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

## 2025-10-19 -> 2025-10-20 — Refresh token rotation and auth hardening

- Implemented a rotating refresh-token system (server-side storage of hashed refresh tokens) to allow secure long-lived sessions without leaking access tokens:

  - `app/schema.sql` — added `refresh_tokens` table (user_id, jti, token_hash, issued_at, expires_at, revoked).
  - `app/refresh_utils.py` — new helper module: generates secure refresh tokens, hashes them, stores and verifies tokens, rotates (revoke old + create new) and revokes user tokens.
  - `app/auth.py` — updated flows:
    - `POST /auth/login` now sets a HttpOnly cookie `mc_refresh` containing the refresh token (format `<jti>.<raw>`) and returns the access token in the JSON body. This prevents client-side JavaScript from reading the refresh token.
      - `POST /auth/refresh` supports two modes:
        - Legacy: send `Authorization: Bearer <access_token>` and the server will verify the signature even if expired and re-issue a new access token.
        - Rotation (preferred): send the request with the HttpOnly cookie `mc_refresh` (browser sends cookie automatically). The server validates the token from the cookie, rotates it (revoke old, set new cookie) and returns a new access token in the response body.
    - `POST /auth/logout` revokes refresh tokens for the user to fully logout sessions.
  - `app/jwt_utils.py` — switched to timezone-aware datetime usage and store `exp` as epoch seconds to avoid timezone ambiguities and DeprecationWarnings.
  - `app/static/app.js` — UI no longer stores refresh tokens in localStorage. Instead the server sets a HttpOnly cookie `mc_refresh` on login and rotates it on refresh. The client uses `authFetch()` which transparently retries after calling `/auth/refresh` (cookies are sent automatically).
  - `tests/test_refresh_tokens.py` — new tests covering login/refresh rotation, reuse rejection, and expired-refresh rejection.

Notes & follow-ups:

- Current storage for `refresh_token` in the UI is `localStorage` (acceptable for local prototypes). For production, prefer HttpOnly secure cookies and CSRF protections.
- Consider hardening the refresh token hashing (HMAC using `SECRET_KEY`, or Argon2/bcrypt) and limiting the number of active refresh tokens per user.
- The rotation pattern prevents reuse of old refresh tokens; tests ensure attempted reuse is rejected.
