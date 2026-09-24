# Electron security and delivery contract

## Process boundary

- Main process owns application lifecycle, windows, permissions, filesystem access, secret encryption, updates, and worker creation.
- Preload exposes the smallest typed API with `contextBridge`; it validates no authority itself and forwards only named operations.
- Main validates sender frame, channel, payload shape, size, path, URL, and current application state before acting.
- Renderer contains presentation and non-sensitive state only. It receives redacted errors and cannot choose a development or privileged runtime profile in a public build.
- Long-running or crash-prone domain work runs in one owned worker with explicit start, cancel, progress, and terminal-result messages.

## Window and network policy

- Keep `nodeIntegration: false`, `contextIsolation: true`, and sandboxing enabled where supported.
- Deny unexpected window creation and navigation. Open only allowlisted HTTPS destinations through the operating system.
- Deny permissions by default and grant only the exact feature scope.
- Use a strict Content Security Policy without unsafe remote code.

## Secrets

- Collect only values required by the feature and mask them in the UI.
- Encrypt with Electron `safeStorage` before persistence. If encryption is unavailable, keep the value in memory or fail closed.
- Never send full secret values back to the renderer after storage.
- Redact tokens, identity, query secrets, and private URLs from logs, crash reports, screenshots, and update checks.

## Packaging and release evidence

1. Unit and IPC contract tests pass.
2. Deterministic renderer tests pass at minimum and nominal viewports.
3. Production build contains no development-only controls.
4. Native package and maker succeed on the current platform.
5. Packaged smoke launches, reaches a usable state, and exits cleanly.
6. Archive inspection excludes local config, secrets, profiles, caches, and unnecessary runtimes.
7. Signing and notarization are reported as passed, failed, unavailable, or not configured—never inferred.
8. Release claims require verified tag, workflow, asset set, sizes, and digests on the remote.
