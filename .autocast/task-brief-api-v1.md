# Task Brief - Backend API V1 Foundation

## Objective

Create the first production-oriented backend API foundation for AzkaSpam while
keeping the existing IMAP worker behavior intact.

## Task Type

feature | architecture | security

## Scope

- Add JSON API endpoints for read-only operational data.
- Keep existing HTML dashboard working during migration.
- Extract reusable data functions from dashboard route handlers where needed.
- Add tests using temporary SQLite state.
- Prepare API contract suitable for a TypeScript frontend.

Initial endpoints:

- `GET /api/auth/me`
- `GET /api/summary`
- `GET /api/messages`
- `GET /api/events`
- `GET /api/learned`
- `GET /api/accounts`
- `GET /api/rspamd/stats`
- `GET /api/safe-mode`

## Out Of Scope

- CRUD mutations.
- IMAP credential encryption.
- MFA implementation.
- TypeScript frontend.
- SMTP gateway.
- Replacing YAML with SQLite as config source.

## Context

The current `dashboard.py` renders HTML directly from SQLite queries. The future
frontend needs stable JSON endpoints. Read-only endpoints are the safest first
step because they do not move messages, train Bayes, or alter credentials.

## Acceptance Criteria

- API endpoints return JSON only.
- Authenticated access is enforced server-side.
- Account scope is respected for non-admin users.
- Responses avoid returning IMAP passwords or secrets.
- Existing dashboard pages still work.
- Tests cover successful requests, unauthenticated requests, and scoped access.

## Verification Plan

- `python -m py_compile filter\dashboard.py filter\filter.py`
- `python -m pytest filter`
- Flask test client coverage for new `/api/*` endpoints.
- Manual local API smoke test against temporary SQLite state.

## Security Impact

Touches auth, permissions, personal email metadata, and API trust boundaries.
No new secret storage or email mutation should be added in this task.

## Risk Level

high

## Selected Route

secure-change
