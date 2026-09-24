# Cloudflare deployment contract

## Read-only preflight

```bash
npx wrangler --version
npx wrangler whoami
npx wrangler deploy --dry-run
```

Use the project-specific command when it wraps Wrangler with required configuration. Read official documentation for current flags instead of copying these examples blindly.

## Evidence ladder

1. Configuration parses and generated types match bindings.
2. Unit and deterministic integration tests pass.
3. Production bundle succeeds and contains no secret values or unexpected files.
4. Wrangler dry-run succeeds for the exact environment.
5. Authenticated account and deployment target match the request.
6. Authorized deployment returns a version/deployment identifier.
7. Cloudflare's remote surface reports that identifier as current.
8. A safe live request proves expected behavior without mutating production data.

## Secrets and rollback

- Record secret names and owning system, never values.
- Use `manage-github-secrets` for GitHub Actions storage. Use current Wrangler secret commands for Cloudflare-side values only after the exact mutation is authorized.
- A GitHub Secret and a Cloudflare server-side verifier are independent states; update them as a planned transaction when compatibility requires both.
- Preserve the previous deployment identifier and rollback procedure before a production change. Executing rollback is a separate consequential action.
