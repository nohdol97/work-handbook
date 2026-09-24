---
name: adr
description: "Record, supersede, and review durable architecture decisions with context, alternatives, consequences, and document-map synchronization. Use when work changes architecture, ownership, data flow, security boundaries, deployment, repository layout, or a long-lived workflow rule. Do not use for routine implementation details or unsettled proposals. Re-run: ADR, architecture decision, 구조 결정, 결정 기록."
---

# Architecture decision records

Preserve why a durable choice was made without turning routine implementation into permanent policy.

## Procedure

1. Read related specs, existing ADRs, and the current implementation before drafting.
2. Decide whether the choice is durable: it must affect architecture, ownership, data flow, security, deployment, repository layout, or a long-lived workflow rule.
3. If alternatives are still open, write or update a proposal/spec first. An ADR records a decision; it does not manufacture one.
4. Allocate the next three-digit number under `docs/adr/` without renumbering history.
5. Write the ADR in Korean using [the template](references/template.md). State context, decision, alternatives, positive and negative consequences, affected surfaces, and verification.
6. When replacing a decision, keep the older ADR and mark both directions: old → superseded by NNN; new → supersedes NNN.
7. Update `docs/README.md` and `docs/harness-changelog.md` in the same commit.
8. Open every affected file and run the root integrity check before claiming completion.

Do not cite conversation memory as a durable source after the ADR exists. Cite the ADR itself.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Rationale | Decisions survive only in chat or commits | Context, alternatives, and consequences remain searchable |
| Evolution | Old decisions are silently rewritten | Supersession preserves the decision chain |
| Navigation | ADRs exist but are hard to find | The docs map and changelog move with the decision |
