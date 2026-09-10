# AutoCast Adoption

AzkaSpam uses AutoCast as its delivery methodology for AI-assisted work.

Reference framework location for this workstation:

```txt
C:\Users\Micro\Desktop\OpenCode\Harness
```

This project does not vendor the whole AutoCast framework. It keeps only the
project-specific adoption artifacts here and references the local framework as
the standard source.

## Required Loop

Every non-trivial task should follow:

```txt
request -> intake -> task brief -> route -> workflow -> build -> verify -> judge -> evidence
```

## Default Profile

AzkaSpam defaults to `secure` because the application handles email credentials,
personal email metadata, authentication, Docker infrastructure, and external
network integrations.

Escalate to `critical` for auth, MFA, authorization, secret encryption, worker
control, CI/CD, Docker hardening, or any change that can move, delete, train, or
expose email data.

## Project Artifacts

- `project-brief.md` - product, architecture, and security context.
- `decision-records.md` - adopted architectural decisions.
- `backlog-by-route.md` - candidate work grouped by AutoCast route.
- `task-brief-api-v1.md` - first executable backend plan.
- `evidence-log.md` - pilot evidence and future run log seed.
