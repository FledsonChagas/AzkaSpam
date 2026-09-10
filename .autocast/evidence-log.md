# Evidence Log

## Run Metadata

- date: 2026-09-10
- tool: OpenCode
- model: openai/gpt-5.5
- route: review-only, then standard adoption setup
- risk: secure
- branch: main
- commit: pending

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

## Security Gates

- secrets checked: no secrets added; documentation only.
- dependency changes reviewed: no dependency changes.
- permission changes reviewed: no runtime permission changes.
- trust boundaries reviewed: documented in project brief and backlog.
- residual risk recorded: yes, pilot findings recorded above.

## Residual Risk

- Adoption artifacts do not fix existing security issues.
- Critical changes remain required before exposing AzkaSpam beyond a trusted local environment.
