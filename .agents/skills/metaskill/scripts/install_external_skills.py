#!/usr/bin/env python3
"""Install reviewed external skills from exact Git revisions."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Iterable


SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def load_catalog(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_errors(candidate: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    name = candidate.get("name", "")
    if not SKILL_NAME_RE.fullmatch(name):
        errors.append("invalid skill name")
    if policy.get("require_full_commit_sha") and not FULL_SHA_RE.fullmatch(
        candidate.get("revision", "")
    ):
        errors.append("revision is not a full commit SHA")
    if candidate.get("license") not in set(policy.get("allowed_licenses", [])):
        errors.append("license is not approved")
    required = policy.get("required_audit_status", "pass")
    audits = candidate.get("audits", {})
    if not audits or any(status != required for status in audits.values()):
        errors.append("recorded security audits are not all passing")
    if not str(candidate.get("repository", "")).startswith("https://github.com/"):
        errors.append("repository is not an HTTPS GitHub source")
    skill_path = Path(candidate.get("path", ""))
    if skill_path.is_absolute() or ".." in skill_path.parts:
        errors.append("skill path escapes the repository")
    return errors


def eligible_candidates(
    catalog: dict[str, Any], capabilities: Iterable[str]
) -> list[dict[str, Any]]:
    selected = {"core", *capabilities}
    policy = catalog["auto_install_policy"]
    result: list[dict[str, Any]] = []
    for candidate in catalog["candidates"]:
        if candidate.get("decision") != "auto":
            continue
        if not selected.intersection(candidate.get("capabilities", [])):
            continue
        errors = candidate_errors(candidate, policy)
        if errors:
            raise ValueError(f"{candidate.get('name')}: {', '.join(errors)}")
        result.append(candidate)
    return sorted(result, key=lambda item: item["name"])


def _run(command: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"command failed ({' '.join(command)}): {detail}")
    return completed.stdout.strip()


def _frontmatter_name(skill_file: Path) -> str | None:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("name:"):
            return line.removeprefix("name:").strip().strip("\"'")
    return None


def _load_lock(target: Path) -> dict[str, Any]:
    path = target / "skills.lock.json"
    if not path.exists():
        return {"schema_version": 1, "skills": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_lock(target: Path, lock: dict[str, Any]) -> None:
    lock["updated_at"] = date.today().isoformat()
    lock["skills"] = sorted(lock["skills"], key=lambda item: item["name"])
    (target / "skills.lock.json").write_text(
        json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def install_candidates(
    target: Path,
    catalog_path: Path,
    capabilities: Iterable[str],
    offline: bool = False,
) -> list[dict[str, Any]]:
    target = target.resolve()
    catalog = load_catalog(catalog_path)
    candidates = eligible_candidates(catalog, capabilities)
    lock = _load_lock(target)
    by_name = {item["name"]: item for item in lock["skills"]}
    results: list[dict[str, Any]] = []

    for candidate in candidates:
        name = candidate["name"]
        destination = target / ".agents" / "skills" / name
        existing = by_name.get(name)
        if destination.exists():
            if existing and existing.get("revision") == candidate["revision"]:
                results.append({"name": name, "status": "already-installed"})
                continue
            raise FileExistsError(f"external skill destination already exists: {destination}")

        lock_entry = {
            "name": name,
            "source": candidate["source"],
            "repository": candidate["repository"],
            "revision": candidate["revision"],
            "path": candidate["path"],
            "license": candidate["license"],
            "reviewed_at": catalog["reviewed_at"],
            "decision": candidate["decision"],
            "status": "pending" if offline else "installed",
        }

        if offline:
            by_name[name] = lock_entry
            results.append({"name": name, "status": "pending-offline"})
            continue

        with tempfile.TemporaryDirectory(prefix=f"skill-{name}-") as temporary:
            checkout = Path(temporary)
            _run(["git", "init", "--quiet"], checkout)
            _run(["git", "remote", "add", "origin", candidate["repository"]], checkout)
            _run(
                ["git", "fetch", "--quiet", "--depth=1", "origin", candidate["revision"]],
                checkout,
            )
            _run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], checkout)
            observed_revision = _run(["git", "rev-parse", "HEAD"], checkout)
            if observed_revision != candidate["revision"]:
                raise RuntimeError(
                    f"{name}: fetched {observed_revision}, expected {candidate['revision']}"
                )

            source = (checkout / candidate["path"]).resolve()
            source.relative_to(checkout.resolve())
            if not (source / "SKILL.md").is_file():
                raise FileNotFoundError(f"{name}: reviewed skill subtree is missing")
            if _frontmatter_name(source / "SKILL.md") != name:
                raise ValueError(f"{name}: upstream frontmatter name does not match")

            shutil.copytree(source, destination)
            license_source = (checkout / candidate["license_path"]).resolve()
            license_source.relative_to(checkout.resolve())
            if not license_source.is_file():
                shutil.rmtree(destination)
                raise FileNotFoundError(f"{name}: upstream license file is missing")
            license_destination = target / "third_party" / name / "LICENSE"
            license_destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(license_source, license_destination)

        by_name[name] = lock_entry
        results.append({"name": name, "status": "installed"})

    lock["skills"] = list(by_name.values())
    _write_lock(target, lock)
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    catalog = args.catalog or Path(__file__).resolve().parents[1] / "references" / "external-skills.json"
    results = install_candidates(args.target, catalog, args.capability, args.offline)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
