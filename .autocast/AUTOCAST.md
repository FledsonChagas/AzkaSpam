# AutoCast Project Entrypoint

AzkaSpam uses AutoCast v0.10 as its AI-assisted development framework standard.

## Framework Source

Use `.autocast/core/` as the AutoCast framework source.

Do not edit `.autocast/core/` for project-specific decisions unless updating the
pinned AutoCast framework version.

## Project State

Use project-specific AutoCast state from:

- `.autocast/project/`
- `.autocast/tasks/`
- `.autocast/evidence/`
- `.autocast/decisions/`
- `.autocast/backlog/`

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

- `project/project-brief.md` - product, architecture, and security context.
- `project/engineering-standards.md` - local engineering rules.
- `project/security-profile.md` - local secure-by-default posture.
- `decisions/decision-records.md` - adopted architectural decisions.
- `backlog/backlog-by-route.md` - candidate work grouped by AutoCast route.
- `tasks/` - task briefs.
- `evidence/` - task evidence and run logs.

## Agent Instruction

When asked to use AutoCast:

1. Read this file first.
2. Read `.autocast/config.yml` and `.autocast/lock.yml`.
3. Use `.autocast/core/` for framework rules, routes, profiles, security,
   workflows, and templates.
4. Use project files outside `core/` for local context, tasks, evidence,
   decisions, and backlog.
5. Do not mix framework updates with project task work.
