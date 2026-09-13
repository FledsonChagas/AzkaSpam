# AzkaSpam Project Brief

## Product Direction

AzkaSpam is an email spam filtering control plane and worker system. The V1
target is existing IMAP mailboxes such as Outlook, Gmail, and provider-hosted
mailboxes. The worker monitors mailboxes after delivery, scores messages with
rspamd, moves likely spam, learns from user actions, and exposes full operation
through an API and TypeScript frontend.

V2 may add an SMTP gateway path where mail flows through AzkaSpam before final
delivery.

## V1 Runtime Model

```txt
existing mailbox -> IMAP worker -> rspamd -> IMAP move/train -> SQLite -> API -> frontend
```

## Initial Deployment Model

- Docker-first and cloud-agnostic.
- Local/self-hosted V1 for personal and family use.
- Designed to evolve toward small-business and multi-tenant SaaS.
- SQLite for V1 speed and simplicity.
- PostgreSQL considered for V2/multi-tenant.

## Security Posture

Default AutoCast profile: `secure`.

Security-sensitive areas:

- IMAP credentials.
- Dashboard/API authentication.
- MFA and future SSO/OAuth.
- Email metadata and message actions.
- rspamd controller password.
- Redis Bayes corpus.
- Docker networking and published ports.
- Audit logs and operational telemetry.

## Product Requirements From Intake

- V1 uses IMAP post-delivery cleanup.
- V2 may add SMTP gateway.
- One Outlook account initially, but support multiple accounts.
- Local auth first.
- MFA required in V1 roadmap.
- OAuth/SSO can wait until V2.
- Users include application admins and regular mailbox users.
- IMAP credentials should be stored encrypted locally.
- Manual actions are required: move, learn spam, learn ham, review quarantine.
- Audit/history must record everything important.
- Frontend is the control panel for the filtering engine.
- rspamd remains the initial filtering engine.
- Future rules, custom models, and LLM integration remain open.
