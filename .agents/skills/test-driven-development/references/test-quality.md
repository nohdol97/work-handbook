# Test quality rules

- Test observable behavior through the highest stable public seam available.
- Use expected values from the spec, a known literal, a worked example, or an independent system signal. Production logic must not construct its own expected result.
- Prefer real collaborators when deterministic and cheap. Mock irreversible, slow, unavailable, or externally owned boundaries, not internal implementation details.
- A failure must identify the missing behavior. Fixture, import, syntax, or environment errors are not a valid red state.
- Keep one behavior per cycle. Table-driven cases are one cycle only when they exercise the same rule.
- Do not inflate timeouts without naming and observing the awaited state.
- Preserve the original failure when artifact capture or cleanup also fails.
