# GitHub Secret command contract

## Read-only discovery

```bash
gh auth status -h github.com
gh secret list --repo OWNER/REPOSITORY
gh secret list --repo OWNER/REPOSITORY --env ENVIRONMENT
```

These commands expose names and metadata, not values.

## Safe writes

Prefer interactive stdin:

```bash
gh secret set SECRET_NAME --repo OWNER/REPOSITORY
```

Or redirect from an exact ignored file without printing it:

```bash
gh secret set SECRET_NAME --repo OWNER/REPOSITORY < /absolute/path/to/ignored-secret-file
```

For an environment, add `--env ENVIRONMENT`. For an organization, resolve visibility deliberately with the official `gh secret set --org` options before mutation.

Never use `--body VALUE`, `echo VALUE | ...`, shell tracing, or a command that expands the value into process arguments. Never inspect the ignored source merely to move it.
