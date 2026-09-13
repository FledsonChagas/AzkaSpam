# Engineering Standards

## Code Style

Follow existing project patterns and prefer the smallest correct change.

## Backend

- Keep the IMAP worker behavior stable unless the task explicitly targets it.
- Prefer behavior-focused tests around email moves, learning, config loading,
  authentication, and authorization.
- Do not add broad refactors to security-critical changes.

## Frontend

The future frontend will be TypeScript and must consume stable `/api/*`
contracts. Do not couple frontend state directly to worker internals.

## Dependencies

- Avoid new dependencies unless the task brief justifies them.
- Pin security-sensitive dependencies.
- Record dependency changes in AutoCast evidence.

## Verification

Default Python verification:

```bash
python -m py_compile filter\dashboard.py filter\filter.py filter\bootstrap_train.py
python -m pytest filter
```

## Security

Apply secure by default, least privilege, server-side authorization, evidence,
and route-based review. Never commit real credentials, mailbox content, tokens,
session cookies, or production data.
