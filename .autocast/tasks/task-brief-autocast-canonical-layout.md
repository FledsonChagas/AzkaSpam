# Task Brief - AutoCast Canonical Layout

## Objective

Migrate AzkaSpam's AutoCast adoption to the canonical v0.10 `.autocast/`
layout.

## Task Type

architecture | documentation

## Scope

- Add AutoCast framework source under `.autocast/core/`.
- Prefer a Git submodule for the framework source.
- Move project-specific state out of the `.autocast/` root into canonical
  project, tasks, evidence, decisions, and backlog directories.
- Add `AUTOCAST.md`, `config.yml`, and `lock.yml`.
- Preserve existing evidence and decisions.
- Do not alter production code.

## Out Of Scope

- Backend API changes.
- Worker changes.
- Security control implementation.
- Frontend work.

## Context

AutoCast v0.10 defines `.autocast/core/` as framework source and `.autocast/*`
outside `core/` as project state.

## Acceptance Criteria

- `.autocast/core/` points to AutoCast v0.10.
- `.autocast/lock.yml` records source, path, version, and pinned commit.
- `.autocast/config.yml` sets project name `AzkaSpam`, default profile
  `secure`, adapter `opencode`, and conformance target `L3`.
- Existing project brief, task brief, evidence, decisions, and backlog are
  preserved under canonical directories.
- Tests still pass.

## Verification Plan

- `git status --short --branch`
- `python -m pytest filter`
- `node .autocast/core/bin/autocast.mjs route --task "Adopt AutoCast canonical layout"` if Node and the CLI entrypoint are available.

## Security Impact

No production runtime security behavior changes. The task changes methodology,
framework source tracking, and project evidence layout.

## Risk Level

medium

## Selected Route

standard

## Selected Profile

secure
