# Task Brief - Encrypted IMAP Credentials

## Objective

Ensure IMAP credentials are not stored in plaintext in the AzkaSpam runtime
configuration.

## Task Type

security | architecture

## Scope

- Require encrypted IMAP credentials in account configuration.
- Reject plaintext `password` values in `accounts.yml`.
- Add local helper commands to generate a key and encrypt IMAP passwords.
- Let the worker and `bootstrap_train.py` receive decrypted passwords through
  the existing `Account.password` field after config validation.
- Update dashboard config validation and API masking to avoid exposing encrypted
  password material.
- Update Docker/Compose/bootstrap/docs for the key and encrypted field.
- Add tests without real IMAP connections or real secrets.

## Out Of Scope

- Moving accounts from YAML to SQLite.
- Separating API and worker.
- MFA, SSO, or OAuth.
- Credential rotation workflow.
- STARTTLS support.

## Context

The prior critical-change prevents IMAP credentials from being sent over a
plaintext connection. The next highest risk is at-rest exposure: `accounts.yml`
currently contains plaintext IMAP passwords and dashboard backups can duplicate
that content.

## Acceptance Criteria

- `password_encrypted` is required for each account.
- Plaintext `password` is rejected with a clear error.
- Missing or invalid encryption key fails closed.
- Invalid ciphertext fails closed.
- Existing worker and bootstrap training paths decrypt via `load_accounts()`.
- `/api/accounts` does not return plaintext or ciphertext.
- Documentation explains key generation, encryption, backup impact, and the new
  config field.
- Tests use generated test keys and no real credentials.

## Verification Plan

- `python -m py_compile filter\dashboard.py filter\filter.py filter\bootstrap_train.py filter\test_config.py filter\test_api.py`
- `python -m pytest filter`
- Parse `accounts.yml.example` as YAML.
- Parse Unraid XML templates.

## Security Impact

Touches credential handling, secret storage, Docker configuration, and config
validation. This is a critical security change.

## Risk Level

critical

## Selected Route

critical-change

## Selected Profile

critical
