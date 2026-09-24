---
name: build-electron-app
description: "Design, implement, secure, package, and verify Electron desktop applications with separated main, preload, renderer, and worker authority; validated IPC; OS-backed secret storage; deterministic tests; and explicit build-versus-release boundaries. Use for Electron apps, desktop wrappers, installers, or Electron security reviews. Do not use for an ordinary web app or to infer publication from a packaging request. Re-run: Electron, desktop app, installer, 데스크톱 앱, 프로그램 패키징."
---

# Build Electron applications

Deliver a desktop application whose renderer cannot silently acquire operating-system, credential, automation, or publication authority.

## 1. Classify the request

- Build/package/installer wording authorizes source changes and local artifacts only.
- Deploy/distribute/publish/release wording authorizes the matching remote tag and release only after local delivery gates pass.
- A new project request does not imply Electron. When wrapping an existing workflow, require the user to report satisfactory local acceptance before adding the shell.

Keep implementation, packaging, signing, notarization, updating, tag push, workflow completion, and release publication as separate evidence states.

## 2. Write the contract

Use `spec-driven-development` and record:

- trusted main-process responsibilities;
- minimal preload API and validated IPC schemas;
- renderer states and failure recovery;
- worker ownership, cancellation, concurrency, and logs;
- secret fields and persistence policy;
- navigation, window, permission, and external-link policy;
- packaging targets, size budgets, signing status, and release boundary.

Read [security-and-delivery.md](references/security-and-delivery.md) before implementation.

## 3. Implement through TDD

1. Test payload validation, sender validation, and denied channels before handlers.
2. Keep `contextIsolation` enabled and Node integration disabled in renderer windows.
3. Expose narrow typed preload methods; never expose raw IPC or Node primitives.
4. Own privileged operations in main or a dedicated worker with bounded concurrency and cancellation.
5. Store secrets with `safeStorage` or memory-only fallback. Persist no plaintext fallback.
6. Deny unexpected navigation, popups, permissions, protocols, and external URL schemes.
7. Test nominal and minimum supported viewports deterministically.
8. Build and smoke-test the packaged application, not only the development server.

## 4. Package and deliver

Exclude development browsers, profiles, source maps containing secrets, logs, and local configuration from installers. Measure artifact sizes and inspect archive contents. Disclose unsigned or unnotarized artifacts plainly.

For an authorized release, verify the source commit, collision-free tag, workflow conclusion, required assets, and SHA-256 digests. Do not treat a successful package command as a published release.

## With / without

| Metric | Without this skill | With this skill |
|---|---|---|
| Authority | Renderer code can reach raw Node or IPC | Main, preload, renderer, and worker boundaries stay explicit |
| Secrets | Convenience fallback can persist plaintext | OS-backed encryption or memory-only failure is required |
| Delivery | Build, signing, and release collapse into one claim | Every delivery state has separate evidence |
