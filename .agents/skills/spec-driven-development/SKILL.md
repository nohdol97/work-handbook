---
name: spec-driven-development
description: "Define or revise an executable behavior contract before implementing a feature, bug fix, refactor, gate, hook, or workflow change. Use when behavior or authority changes and reviewers need stable numbered requirements and acceptance criteria. Do not use for wording-only or behavior-invariant metadata edits. Re-run: SDD, spec first, write a spec, 스펙부터, 요구사항 정리."
---

# Spec-driven development

Make implementation answer to a stable behavior contract instead of letting the finished code define its own success.

## Procedure

1. Observe the current repository, behavior, tests, adjacent ADRs, and authority boundaries.
2. Resolve discoverable facts before asking questions. Batch only unresolved choices that materially change the solution.
3. Create or update `docs/specs/NNN-title.md` from [the template](references/template.md).
4. Write the problem from the user's perspective, then goals and explicit non-goals.
5. Number every requirement. Include inputs, outputs, states, failure behavior, security and publication boundaries, migration, and rollback when relevant.
6. Give every requirement an observable acceptance criterion and the test or surface that will prove it.
7. Record structural choices separately with `adr`; link rather than duplicating the rationale.
8. Update `docs/README.md` in the same change.
9. Freeze the smallest coherent slice, then hand its first failing criterion to `test-driven-development`.
10. At completion, compare the implementation and fresh evidence against each criterion. Report any unchecked item as unverified.

The spec is not an implementation diary. Keep progress logs elsewhere and update the spec only when intended behavior changes.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Completion | The implementation judges itself | Numbered observable criteria judge delivery |
| Scope | Adjacent improvements expand silently | Goals and non-goals define the slice |
| Review | Reviewers infer intent from the diff | Review compares the diff with one stable contract |
