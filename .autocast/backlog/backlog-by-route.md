# Backlog By AutoCast Route

## critical-change

- Encrypt IMAP credentials at rest using `AZKASPAM_SECRET_KEY`.
- Replace plaintext `accounts.yml` as runtime source with SQLite-backed account records.
- Implement local auth with MFA TOTP.
- Implement RBAC for owner, admin, and user roles.
- Add full audit log for every user/API/admin action.
- Separate API and worker into different process entrypoints.
- Implement safe worker control: pause, resume, restart account worker.
- Remove unsafe IMAP plaintext login path or implement verified STARTTLS.
- Define threat model for V2 SMTP gateway before any SMTP implementation.

## secure-change

- Create JSON API under `/api/*` with OpenAPI contract.
- Add job queue tables and worker execution for mutating email actions.
- Add endpoints for messages, quarantine, accounts, config, events, learned, safe-mode, rspamd stats, and system health.
- Harden Docker Compose defaults and published ports.
- Pin Docker base images and service images by version or digest.
- Replace bootstrap downloads from branch `main` with pinned release artifacts or checksums.
- Add structured logs and sensitive-field redaction.
- Add backup/restore APIs with secret-aware handling.
- Add API rate limiting for auth and mutating endpoints.

## standard

- Extract dashboard queries into reusable service/repository functions.
- Add tests for existing Flask routes.
- Add tests for account validation, config validation, safe-mode, rate limits, and migrations.
- Update documentation from imap-spamfilter naming to AzkaSpam naming.
- Document local Docker test path for a single Outlook account.
- Add development scripts for API-only and worker-only modes.

## fast-lane

- Fix documentation drift that still describes the dashboard as read-only.
- Align Unraid `accounts.yml` mount mode with the new admin config editor.
- Add `.env.example` entries for planned AzkaSpam variables.
- Add Playwright to the future TypeScript frontend once created.
- Add a top-level quickstart for local demo mode.

## review-only

- Review Flask vs FastAPI for the API layer.
- Review SQLite schema for V1 and PostgreSQL migration path for V2.
- Review multi-tenant architecture options for future SaaS.
- Review privacy/LGPD implications of storing email metadata.
- Review SMTP gateway design and abuse controls.
