# Independent project lifecycle

## Create

1. Validate names with `^[a-z0-9][a-z0-9._-]*$` and resolve the destination under `project/`.
2. Ensure no directory, Git worktree, or remote collision exists.
3. Use the stack's standard scaffolder and initialize `git init -b main` only when no repository exists.
4. Add a project `.gitignore` before secrets, profiles, caches, downloads, or artifacts are created.
5. Write `.agents/projects/<name>/AGENTS.md` from observed facts: purpose, stack, commands, secret schema, authority boundary, verification ladder, artifacts, and known failures.
6. Add one `REGISTRY.md` row with observed facts and `unknown` for unresolved non-blocking fields.
7. Write the first behavior spec and implement through TDD.
8. Validate, stage named paths, inspect the staged diff, and commit.
9. Unless local-only, verify the authenticated GitHub owner, check exact-name collision, create a private repository, push, and compare the remote branch SHA with local `HEAD`.

## Carry in

1. Inspect the source status, branch, worktree root, remotes, tracked files, README, manifests, and commands.
2. Existing history or a remote makes this carry-in, never scaffolding.
3. A dirty source requires an explicit choice: committed HEAD only, preserve modifications, or continue using the source in place. Do not claim a clean clone preserved uncommitted work.
4. Copy no `.env`, cookies, profiles, auth state, logs, traces, downloads, or ignored secrets.
5. Create the central project harness and registry row only after destination name and repository identity agree.
6. Verify the root ignores the project and the child remains an independent worktree.

## Transfer between harnesses

1. Treat a transfer as a coordinated carry-in plus source-ownership removal. Inventory the child repositories, central project harnesses, installation-local workspaces, shared skills, specs, ADRs, and deployment responsibilities on both sides before moving anything.
2. Require a clean child worktree unless the user explicitly chooses how to preserve dirty state. Record each repository's HEAD, branch, origin, and status before the move.
3. Move the existing repository directory intact under the destination `project/`. Do not recreate, flatten, or rewrite the child Git repositories, and do not copy ignored credentials or runtime state into tracked files.
4. Move or recreate the matching central project harness and installation-local workspace only when its ownership follows the product. Update source and destination registries with current rows and dated transfer history.
5. The destination validates the carried repositories, routing, shared skills, and domain contracts before the source removes active ownership assets. Preserve historical ADRs and mark superseded decisions instead of deleting audit history.
6. Re-read HEAD, branch, origin, and status after the move and compare them with the pre-move record. Run both harness integrity checks, then commit and push each affected tracked root independently.

## Update and push

- Record child branch, upstream, ahead/behind, and status before editing.
- Push only repositories changed and committed by the current task.
- Stop if an ordinary push would publish unrelated pre-existing commits.
- On rejection, inspect and report remote state; never force-push, reset, or silently rebase.
- Read the configured upstream ref after push and compare it with the task commit before reporting delivery.
