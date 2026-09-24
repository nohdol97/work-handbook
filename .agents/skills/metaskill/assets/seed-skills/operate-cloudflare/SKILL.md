---
name: operate-cloudflare
description: "Design, configure, deploy, and verify Cloudflare Workers, Pages, bindings, and related resources with current official documentation, explicit secret handling, dry-run checks, rollback awareness, and live deployment evidence. Use for Wrangler, Workers, Pages, KV, D1, R2, Durable Objects, or Cloudflare deployment. Do not use for DNS, billing, token rotation, destructive resource removal, or public deployment unless the request authorizes that exact action. Re-run: Cloudflare, Wrangler, Workers deploy, Pages 배포, 클라우드플레어."
---

# Operate Cloudflare

Use current Cloudflare documentation and separate local correctness, configuration validity, credential state, deployment, and live behavior into distinct evidence states.

## 1. Classify authority

- Build/configure/test wording authorizes local files and non-mutating validation only.
- Deploy/publish wording authorizes the exact named Cloudflare target after dry-run and identity checks.
- Secret registration, token rotation, DNS changes, permission changes, billing, production data mutation, rollback, and resource deletion are separate explicit boundaries.

Resolve the account, project, environment, custom domain, and existing deployment before mutation. Never infer production from a default Wrangler profile.

## 2. Retrieve current contracts

Fetch the relevant official Cloudflare documentation, installed Wrangler version/schema, and project configuration before writing current flags, bindings, compatibility dates, limits, or APIs. Prefer installed types and official docs over memory.

Read [deployment-contract.md](references/deployment-contract.md) for the verification ladder and failure handling.

## 3. Implement and validate

1. Write a spec for behavior, bindings, secret names, environments, routes, migrations, and rollback.
2. Keep values out of configuration and logs. Commit complete fake schemas or names only.
3. Use TDD for request behavior and deterministic local fixtures for external services.
4. Run the project's type generation, static checks, tests, build, and Wrangler dry-run/config validation.
5. Inspect the produced bundle for secrets, unexpected assets, Node compatibility assumptions, and size limits.
6. Verify `wrangler whoami`. On macOS, repeat a sandbox-only authentication failure with narrow host/Keychain access before requesting login.

## 4. Deploy and prove

For an authorized deployment, target the exact environment and account. Capture the deployed version or deployment identifier. Verify the remote deployment and one safe live behavior through Cloudflare's own surface. A successful CLI exit without remote identity and behavior evidence is incomplete.

On failure, preserve the previous known-good deployment, identify whether code, configuration, binding, permission, or propagation failed, and resume from the first unproven state. Do not delete/recreate resources or rotate credentials as a generic retry.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Currency | Commands rely on remembered Wrangler behavior | Official docs, installed types, and schema are checked first |
| Authority | Local build and deployment can blur together | Build, secret, deploy, DNS, and destructive actions remain separate |
| Completion | CLI exit is treated as publication proof | Remote identity and safe live behavior prove deployment |
