---
name: test-driven-development
description: "Implement features, fixes, refactors, gates, hooks, and scripts through a practical red-green-refactor loop tied to an accepted specification. Use before production behavior changes. Allows documented structural verification only for generated files, documentation-only work, or cases where deterministic tests are genuinely impractical. Re-run: TDD, test first, failing test, red green refactor, 테스트부터."
---

# Test-driven development

Use a failing test to prove the check can detect the missing behavior, then implement the smallest coherent change.

## Loop

1. Read the active spec and select one acceptance criterion.
2. Name the public seam and the production change that would make the test fail.
3. Write the smallest behavior-focused test or deterministic reproduction.
4. Run it and confirm it fails for the expected missing behavior, not a syntax, fixture, or environment error.
5. Implement only enough production code to pass that criterion.
6. Run the focused test until green, then the relevant surrounding suite.
7. Refactor only while all tests stay green.
8. Repeat for the next criterion.
9. Finish with a fresh full verification and record command, observed result, proof rationale, and unverified scope.

Read [test-quality.md](references/test-quality.md) when choosing seams, mocks, or exceptions.

Do not delete pre-existing user work merely because it preceded a test. When inheriting untested code, first capture current behavior, add a regression test that fails against the intended change, then modify it safely.

## Exceptions

Generated files, documentation-only changes, initial scaffolding, and behavior that cannot be deterministically exercised may use structural or independent observable verification. State the reason in the spec and completion report. Configuration that controls behavior is not automatically exempt.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Test validity | A passing test may never have detected the bug | The expected red state proves detection |
| Scope | Implementation anticipates future requirements | One acceptance criterion drives one minimal slice |
| Confidence | Completion rests on code inspection | Focused and full fresh runs support the claim |
