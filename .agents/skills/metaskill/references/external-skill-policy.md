# External skill evaluation policy

Use the catalog JSON as the machine-readable allowlist and the dated proposal as the human-readable evidence record.

## Discovery

1. Check the skills.sh leaderboard for established candidates.
2. Run specific searches for the target capability and adjacent terminology.
3. Prefer first-party maintainers for tool-specific behavior.
4. Record install count and repository reputation only as discovery signals.

## Required review

Before an `auto` decision:

- read the complete SKILL.md and every executable script;
- inspect dependencies, network calls, credential handling, mutation and publication commands;
- compare trigger descriptions and authority with every local skill;
- verify the repository is not archived and the exact commit exists;
- verify a redistributable SPDX license and license file;
- record all security audit statuses and require every configured provider to pass;
- choose the smallest skill that owns the needed responsibility;
- write why a local rule or existing skill is insufficient.

## Installation

Install from the full commit SHA, never a moving branch. Copy only the reviewed subtree, copy the upstream license under `third_party/<skill>/LICENSE`, and record the result in `skills.lock.json`.

If any check becomes unknown or fails, change the candidate to `manual` or `rejected`. Do not silently fall back to a newer branch or a similarly named fork.
