# Security Profile

## Default Profile

secure

AzkaSpam defaults to `secure` because it handles IMAP credentials, personal email
metadata, authentication, Docker infrastructure, and external network
integrations.

## Escalation

Use `critical` for:

- authentication or authorization changes
- MFA, OAuth, SSO, session handling, or RBAC
- credential encryption, key handling, or secret storage
- email-moving, training, quarantine, or destructive mailbox actions
- API/worker process separation
- Docker, CI/CD, infrastructure, or deployment permission changes
- SMTP gateway work

## Project-Specific Security Rules

- IMAP credentials must never be sent without TLS.
- IMAP credentials must not be returned by API responses.
- Mutating email actions must be auditable.
- Future SaaS/multi-tenant work requires explicit tenant-isolation review.
- Evidence committed to the repository must be sanitized.
- Raw sensitive evidence must remain local and out of version control.
