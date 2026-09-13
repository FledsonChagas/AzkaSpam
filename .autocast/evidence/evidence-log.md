# Evidence Log

## Run Metadata

- date: 2026-09-10
- tool: OpenCode
- model: openai/gpt-5.5
- route: review-only, standard adoption setup, secure-change API foundation
- risk: secure
- branch: main
- commit: c720d0e for AutoCast adoption; a53a342 for API foundation

## Pilot Review Evidence

The initial AutoCast pilot reviewed AzkaSpam/imap-spamfilter without editing
files. The review covered architecture, Docker, IMAP credential handling,
`accounts.yml`, `.env.example`, rspamd/Redis/Unbound, Unraid scripts, security
risks, operational risks, and documentation quality.

## Findings Summary From Pilot

Blocking findings:

- IMAP credentials are stored plaintext in `accounts.yml` and can be duplicated in backups.
- `ssl: false` appears to allow plaintext IMAP login despite documentation mentioning STARTTLS.
- Dashboard/API and worker currently share one process and filesystem trust boundary.
- The app does not yet expose a full API to operate 100% of the application.
- Config edits are not fully atomic, fully validated, or audited.

Non-blocking findings:

- Compose, Unraid, and README have drift around dashboard mutability and config mounts.
- Docker image tags are not pinned.
- Bootstrap downloads config from branch `main` without checksum/signature.
- Auth lacks MFA, login rate limit, and lockout.
- Healthcheck only validates heartbeat freshness, not dependency health.

## Current Adoption Change

Files changed:

- `.autocast/README.md`
- `.autocast/project-brief.md`
- `.autocast/decision-records.md`
- `.autocast/backlog-by-route.md`
- `.autocast/task-brief-api-v1.md`
- `.autocast/evidence-log.md`

## Commands Run

| Command | Result | Notes |
|---|---|---|
| `git status --short --branch` | passed | Only `.autocast/` is untracked after adoption setup. |
| `git diff --stat` | passed | No tracked runtime files changed. |
| `python -m py_compile filter\dashboard.py filter\filter.py filter\test_api.py` | passed | Syntax check for API changes. |
| `python -m pytest filter` | passed | 16 tests passed, including new API tests. |
| `python -m py_compile filter\dashboard.py filter\filter.py filter\test_api.py` | passed | Post-review test hardening syntax check. |
| `python -m pytest filter` | passed | 21 tests passed after expanded API test suite. |

## API Foundation Evidence

Files changed:

- `filter/dashboard.py`
- `filter/test_api.py`

Endpoints added:

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/summary`
- `GET /api/messages`
- `GET /api/events`
- `GET /api/learned`
- `GET /api/accounts`
- `GET /api/rspamd/stats`
- `GET /api/safe-mode`

Security controls verified by tests:

- Protected API routes return JSON `401` when unauthenticated.
- Account passwords are masked in `/api/accounts`.
- Scoped users only see allowed account data.
- Non-admin users cannot access `/api/rspamd/stats`.

## Security Gates

- secrets checked: no secrets added; documentation only.
- dependency changes reviewed: no dependency changes.
- permission changes reviewed: no runtime permission changes.
- trust boundaries reviewed: documented in project brief and backlog.
- residual risk recorded: yes, pilot findings recorded above.

## Residual Risk

- Adoption artifacts do not fix existing security issues.
- Critical changes remain required before exposing AzkaSpam beyond a trusted local environment.

## AutoCast v0.10 Canonical Layout Evidence

Run metadata:

- branch: feat/autocast-canonical-layout
- route: standard
- profile: secure
- commit: pending

Task brief:

- `.autocast/tasks/task-brief-autocast-canonical-layout.md`

Framework source:

- source: https://github.com/FledsonChagas/AutoCast.git
- path: `.autocast/core`
- install method: submodule
- version: v0.10
- pinned commit: fd1ec992f3ac3979b9fd67a95e2539dc1b472687

Project-state migration:

- `.autocast/README.md` -> `.autocast/AUTOCAST.md`
- `.autocast/project-brief.md` -> `.autocast/project/project-brief.md`
- `.autocast/task-brief-api-v1.md` -> `.autocast/tasks/task-brief-api-v1.md`
- `.autocast/evidence-log.md` -> `.autocast/evidence/evidence-log.md`
- `.autocast/decision-records.md` -> `.autocast/decisions/decision-records.md`
- `.autocast/backlog-by-route.md` -> `.autocast/backlog/backlog-by-route.md`

Security gates:

- secrets checked: no project secrets added; framework is pinned by submodule commit.
- dependency changes reviewed: no production dependency changes.
- permission changes reviewed: no production permission changes.
- trust boundaries reviewed: no runtime trust boundary changes.
- residual risk recorded: yes.

Commands run:

| Command | Result | Notes |
|---|---|---|
| `git status --short --branch` | passed | Shows canonical layout moves, `.gitmodules`, and `.autocast/core` submodule changes. |
| `python -m pytest filter` | environment failed | Global Python lacks project deps (`waitress`, `imapclient`); no test failures from changed files. |
| `C:\Users\Micro\AppData\Local\Temp\opencode\spamfilter-venv\Scripts\python.exe -m pytest filter` | passed | 23 tests passed in dependency-isolated venv. |
| `node .autocast/core/bin/autocast.mjs route --task "Adopt AutoCast canonical layout"` | passed | Classified as `standard`, risk `medium`, task type `feature`. |
| `yaml.safe_load(.autocast/config.yml, .autocast/lock.yml)` | passed | AutoCast project YAML files parse. |

Residual risk:

- `.autocast/core` is a submodule; contributors must initialize submodules.
- Future AutoCast upgrades should be isolated from product changes.
