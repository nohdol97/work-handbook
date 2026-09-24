---
name: manage-github-secrets
description: "Create, rotate, list, and verify GitHub Actions repository, environment, or organization secrets without exposing secret values. Use for gh secret operations, Actions credential setup, Cloudflare tokens in GitHub, or secret-name migration. Do not use for application runtime secret storage, local .env management, or server-side state that must change atomically with a GitHub secret. Re-run: GitHub Secret, Actions secret, gh secret, 시크릿 등록, 시크릿 교체."
---

# Manage GitHub Actions secrets

Change the intended GitHub secret while keeping values out of arguments, logs, documents, and repository history.

## Procedure

1. Resolve the exact owner/repository and scope: repository, environment, or organization.
2. Read workflow references and list existing secret names. Never attempt to read values; GitHub does not expose them.
3. Distinguish a Secret from an Actions Variable. Sensitive values remain Secrets.
4. Verify `gh` authentication. On macOS, treat a sandbox failure as inconclusive and repeat the same read-only check with narrow Keychain access before requesting login.
5. Identify the trusted ignored local source or interactive stdin. Never place the value in a command argument, shell history, chat, `_workspace/`, or a temporary tracked file.
6. If the user's request did not already authorize this exact credential mutation, confirm immediately before it.
7. Set the value using protected stdin, following [the command contract](references/command-contract.md).
8. Verify only the secret name, scope, and update timestamp with `gh secret list`. Do not claim the downstream service accepted the credential until its own safe read-only check succeeds.
9. When a server verifier, deployment setting, or application manifest must change with the secret, treat that as a separate transaction with a rollback plan. A Secret-only success is not end-to-end success.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Exposure | Values can enter arguments or logs | Values use protected stdin and remain unread |
| Targeting | Repository and environment scopes can be confused | Exact owner, repo, and scope are resolved first |
| Completion | Secret presence is treated as service success | GitHub metadata and downstream behavior are verified separately |
