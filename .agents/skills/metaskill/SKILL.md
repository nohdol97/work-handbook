---
name: metaskill
description: "Create, bootstrap, audit, improve, consolidate, or retire personal development harnesses and their independent project repositories; select and pin external skills; maintain README, ADR, SDD, TDD, validation, automatic improvement, and verified push contracts. Use for 새 하네스, 하네스 만들어, 하네스 개선, project scaffold or carry-in, external skill selection, and reusable harness feedback discovered during work. Not for ordinary product implementation after routing is established. Re-run: metaskill, harness, scaffold, evolve, 하네스, 프로젝트 반입."
---

# Harness metaskill

Build a harness from its goal and authority boundaries, not by copying every asset from an older repository.

## 1. Classify the request

Inspect the target path, Git state, remotes, README, manifests, and any existing AGENTS file before asking questions.

Choose one mode:

1. **New harness**: no harness exists and the user wants one.
2. **Harness improvement**: an existing harness contract or shared asset changes.
3. **Project creation**: a new independent product repository belongs under a harness.
4. **Project carry-in**: an existing Git repository is brought under central routing without rewriting history.
5. **External-skill evolution**: discover, evaluate, pin, update, or remove a third-party skill.
6. **Cross-harness transfer**: independent repositories and their platform ownership move between registered harnesses without rewriting child history.
7. **Consolidation or retirement**: ownership overlaps or an asset is superseded; destructive removal requires explicit approval.

Resolve discoverable facts first. Batch only unanswered choices that materially change goal, project types, deployment, irreversible actions, public/private visibility, or secret boundaries.

## 2. New-harness workflow

1. Write the design inputs from [the blueprint](references/blueprint.md): goal, non-goals, project types, expected recurring work, deployment surfaces, credentials, irreversible actions, and completion evidence.
2. Select only capabilities supported by evidence: `cloudflare`, `electron`, `github-secrets`. Record plausible future capabilities as candidates instead of installing them.
3. Run the generator:

```bash
python3 .agents/skills/metaskill/scripts/bootstrap_harness.py \
  --target /absolute/path/to/harness \
  --name harness-name \
  --goal "concrete goal" \
  --capability capability
```

4. The generator installs local core skills and automatically fetches only approved, pinned external skills. Use `--offline` only when network access is unavailable; report its pending entries.
5. Review every rendered placeholder, README claim, authority boundary, and selected skill against the stated goal.
6. Run the generated root's `scripts/check_harness.py` and tests.
7. Initialize `main` when needed, stage named files, inspect the staged diff, and create a Conventional Commit.
8. Unless the user requested local-only, verify the GitHub identity, check name collision, create a private source repository, push, and confirm the remote branch SHA equals local `HEAD`.
9. Report that new or renamed skills become reliably discoverable in a new CLI session.

Never create a public repository, release, deployment, credential, or project-specific agent merely because the harness is new.

## 3. Improvement and automatic feedback

1. Read the current root contract, relevant skill, tests, spec, ADR, README surfaces, and changelog.
2. Reproduce or inspect the current behavior.
3. Classify the change as normative when it alters an obligation, threshold, exception, scope, permission, hook, script, or firing condition. Define testable behavior before editing.
4. Make the smallest coherent change in an existing asset where possible.
5. Update every navigation and history surface required by the root documentation contract.
6. Run focused tests, official skill validation, the full harness integrity check, and fresh completion verification.
7. Commit and push the root change independently from product changes; verify the upstream ref.

Every task includes this feedback pass. Current-task evidence makes a concrete reusable additive or corrective improvement standing-approved. Speculation, deletion, consolidation, project-only assets, secrets, permission changes, and new publication remain outside that approval.

## 4. External skills

Read [external-skill-policy.md](references/external-skill-policy.md) and the complete candidate files before changing the catalog.

- Search broadly, but automatic installation uses only `references/external-skills.json` entries marked `auto`.
- A candidate needs a full commit SHA, approved license, all recorded audits passing, a distinct trigger, complete instruction review, and a written reason.
- Installation copies the reviewed subtree and upstream license and writes `skills.lock.json`.
- A failed or unknown gate produces a manual recommendation. Do not replace it with a moving branch or fork.
- Re-run the dated proposal and update the catalog, docs map when relevant, and changelog for every allowlist change.

## 5. Project repositories

Read [project-lifecycle.md](references/project-lifecycle.md).

For new projects, establish the central project harness, registry row, spec, tests, independent Git repository, verified commit, private remote, push, and remote-SHA check. For carry-in, preserve history and uncommitted-work distinctions; do not run a scaffolder or `git init` over an existing repository. For cross-harness transfer, record child identity before and after, validate the destination before removing source ownership, synchronize both registries, and preserve superseded decision history.

Root-only work never pushes a child. A targeted project push stops when it would include unrelated pre-existing commits. Never force-push or silently rewrite history.

## 6. Required verification

From the affected harness root, run:

```bash
python3 scripts/check_harness.py
python3 -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

Run the active official skill-creator `quick_validate.py` against each created or changed local skill. For generated harnesses, run both offline generation tests and one online pinned-skill smoke when network access is available.

## 7. Completion report

State:

- selected mode and why;
- goal and capability decisions;
- tracked, installation-local, project, and external-skill changes;
- validation command, observed result, proof rationale, and unverified scope;
- local commit and verified upstream ref, or the exact local-only/blocking reason;
- whether a new session is needed for skill discovery;
- common-harness feedback applied or why no reusable improvement was observed.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Harness design | Older repositories are copied wholesale | Goal and capability boundaries select the smallest coherent structure |
| External skills | Popular latest versions are trusted implicitly | Reviewed subtrees, licenses, audits, and SHAs make installation reproducible |
| Method | Specs, tests, and ADRs drift into optional habits | SDD, TDD, and ADR ownership are built into the generated contract |
| Delivery | Local repositories can remain unshared | Verified task commits push by default and remote refs are checked |
| Evolution | Friction stays local or speculative rules accumulate | Evidence-bound improvements ship; unsupported expansion stays gated |
