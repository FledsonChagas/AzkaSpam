# Decision Records

## ADR-001 - Adopt AutoCast For AzkaSpam Delivery

Decision: use AutoCast as the standard methodology for planning, building,
reviewing, verifying, and recording evidence for AzkaSpam tasks.

Context: AzkaSpam handles security-sensitive email credentials, user data,
authentication, Docker infrastructure, and actions that can move or train email.

Alternatives considered:

- Ad hoc development.
- Only issue-based planning.
- Full framework vendoring into the repository.

Reason: AutoCast provides route selection, explicit task briefs, secure defaults,
review discipline, and evidence records without requiring a runtime dependency.

Security impact: positive. Sensitive work is classified before implementation,
and critical changes require stronger review.

Tradeoffs: more ceremony for small tasks, but lower chance of unsafe changes.

Reversibility: medium.

## ADR-002 - Do Not Vendor The Full AutoCast Framework

Decision: keep project-specific AutoCast files in `.autocast/` and reference the
framework at `C:\Users\Micro\Desktop\OpenCode\Harness`.

Context: Harness already exists locally and is a separate repository.

Alternatives considered:

- Clone or copy Harness into `.autocast/`.
- Add Harness as a git submodule.
- Only mention AutoCast in README.

Reason: copying the framework creates maintenance drift. A submodule is heavier
than needed for this pilot. Local project artifacts are enough for adoption.

Security impact: neutral to positive. The project avoids large unrelated files
and keeps evidence specific to AzkaSpam.

Tradeoffs: another developer needs the Harness repo or a public AutoCast source
to resolve the referenced standard.

Reversibility: easy.

## ADR-003 - V1 Uses IMAP, V2 May Add SMTP Gateway

Decision: V1 remains an IMAP post-delivery filter for existing mailboxes.

Context: the initial target is one Outlook mailbox, then personal/family use,
then small business. The current code already supports IMAP and rspamd.

Alternatives considered:

- Rebuild immediately as SMTP gateway.
- Implement SMTP and IMAP simultaneously.

Reason: IMAP provides the fastest working product for existing accounts without
requiring MX/DNS control or operating a mail server.

Security impact: positive for V1 scope reduction. SMTP gateway work is deferred
until a dedicated threat model.

Tradeoffs: V1 cleans after delivery rather than blocking before inbox delivery.

Reversibility: medium.

## ADR-004 - Backend Stays Python, Frontend Will Be TypeScript

Decision: keep the filtering backend in Python and build a TypeScript frontend
after the API is stable.

Context: current IMAP/rspamd/SQLite logic is Python and has tests. Rewriting the
worker now would increase risk before the product contract is stable.

Alternatives considered:

- Rewrite backend in TypeScript.
- Keep server-rendered Flask HTML only.

Reason: Python is suitable for IMAP automation. TypeScript provides stronger UX
velocity for the control panel.

Security impact: positive if the API contract enforces server-side auth and all
mutating operations are audited.

Tradeoffs: two-language stack.

Reversibility: medium.

## ADR-005 - Separate API And Worker

Decision: evolve toward separate API and worker processes/containers.

Context: the current daemon starts the dashboard in the same process. Future API
work must operate the application without risking the long-running worker loop.

Alternatives considered:

- Keep dashboard/API inside the worker process.
- Rewrite into a single async service.

Reason: process separation provides better fault isolation, permissions, scaling,
and operational control.

Security impact: positive. The API and worker can eventually use different file,
network, and secret access.

Tradeoffs: needs shared DB/job coordination.

Reversibility: medium.
