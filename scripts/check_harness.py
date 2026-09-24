#!/usr/bin/env python3
"""Validate a nohdol-metaskill harness and its generated descendants."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote


REQUIRED_FILES = (
    "AGENTS.md",
    "AGENTS.ko.md",
    "CLAUDE.md",
    "README.md",
    ".gitignore",
    ".agents/skills/metaskill/SKILL.md",
    ".agents/skills/README.ko.md",
    "docs/README.md",
    "docs/harness-changelog.md",
)
README_HEADINGS = (
    "## 이 프로젝트가 해결하는 문제",
    "## 설계 원칙",
    "## 시작하기",
    "## 주요 경로",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _frontmatter(path: Path) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0] != "---":
        return None
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return values
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return None


def check_required(root: Path) -> list[str]:
    return [f"missing required file: {path}" for path in REQUIRED_FILES if not (root / path).is_file()]


def check_skills(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / ".agents" / "skills"
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    expected: set[str] = set()
    for skill_file in skill_files:
        relative = skill_file.relative_to(root)
        raw = skill_file.read_bytes()
        metadata = _frontmatter(skill_file)
        if b"\r\n" in raw:
            errors.append(f"{relative}: CRLF is not allowed")
        if metadata is None:
            errors.append(f"{relative}: invalid frontmatter")
            continue
        if metadata.get("name") != skill_file.parent.name:
            errors.append(f"{relative}: name must match directory")
        description = metadata.get("description", "")
        if not description:
            errors.append(f"{relative}: description is required")
        if len(description.encode("utf-8")) > 1024:
            errors.append(f"{relative}: description exceeds 1024 bytes")
        if len(raw.decode("utf-8", errors="replace").splitlines()) > 500:
            errors.append(f"{relative}: SKILL.md exceeds 500 lines")
        expected.add(f"{skill_file.parent.name}/SKILL.md")

    catalog = skills_root / "README.ko.md"
    if catalog.is_file():
        text = catalog.read_text(encoding="utf-8")
        listed = LINK_RE.findall(text)
        skill_links = [item for item in listed if item.endswith("/SKILL.md")]
        for missing in sorted(expected - set(skill_links)):
            errors.append(f".agents/skills/README.ko.md: missing {missing}")
        for stale in sorted(set(skill_links) - expected):
            errors.append(f".agents/skills/README.ko.md: stale {stale}")
        for path in sorted(expected):
            if skill_links.count(path) != 1:
                errors.append(f".agents/skills/README.ko.md: expected one link for {path}")
    return errors


def check_documents(root: Path) -> list[str]:
    errors: list[str] = []
    readme = root / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        for heading in README_HEADINGS:
            if heading not in text:
                errors.append(f"README.md: missing heading {heading}")

    moc = root / "docs" / "README.md"
    if moc.is_file():
        links = set(LINK_RE.findall(moc.read_text(encoding="utf-8")))
        for directory in ("adr", "specs", "proposals"):
            for path in sorted((root / "docs" / directory).glob("*.md")):
                expected = f"{directory}/{path.name}"
                if expected not in links:
                    errors.append(f"docs/README.md: missing {expected}")

    digest_path = root / "AGENTS.ko.md"
    contract = root / "AGENTS.md"
    if digest_path.is_file() and contract.is_file():
        expected_hash = hashlib.sha256(contract.read_bytes()).hexdigest()[:12]
        match = re.search(
            r"(?m)^> source-hash: `([0-9a-f]{12})`$",
            digest_path.read_text(encoding="utf-8"),
        )
        if match is None or match.group(1) != expected_hash:
            errors.append("AGENTS.ko.md: source hash is stale or missing")
    return errors


def _link_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    else:
        value = value.split(maxsplit=1)[0]
    return unquote(value.split("#", 1)[0].split("?", 1)[0])


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    owned_markdown = []
    ignored_parts = {".git", "project", "_workspace", "third_party", "assets"}
    root_generated = {".venv", "venv", "node_modules", "site"}
    for directory, children, files in os.walk(root, followlinks=False):
        parent = Path(directory)
        children[:] = sorted(
            name for name in children
            if name not in ignored_parts
            and not (parent == root and name in root_generated)
            and not (parent == root / ".agents" and name == "projects")
            and not (parent / name).is_symlink()
        )
        owned_markdown.extend(parent / name for name in files if name.endswith(".md"))
    for path in sorted(owned_markdown):
        relative = path.relative_to(root)
        for raw in LINK_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            destination = _link_target(raw)
            if not destination or destination.startswith("#") or SCHEME_RE.match(destination):
                continue
            if destination.startswith("/"):
                continue
            target = (path.parent / destination).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{relative}: link escapes root: {destination}")
                continue
            if not target.exists():
                errors.append(f"{relative}: broken link: {destination}")
    return errors


def check_wiring(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "CLAUDE.md").read_text(encoding="utf-8").startswith("@AGENTS.md\n"):
        errors.append("CLAUDE.md: first line must import @AGENTS.md")
    for relative, expected in (
        (Path(".claude/skills"), "../.agents/skills"),
        (Path(".claude/agents"), "../.agents/agents"),
    ):
        path = root / relative
        if not path.is_symlink() or str(path.readlink()) != expected:
            errors.append(f"{relative}: expected symlink to {expected}")
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    for required in ("/REGISTRY.md", "/_workspace/", "/project/", "/.agents/projects/"):
        if required not in gitignore:
            errors.append(f".gitignore: missing {required}")
    return errors


def check_external_skills(root: Path) -> list[str]:
    errors: list[str] = []
    lock_path = root / "skills.lock.json"
    if not lock_path.exists():
        return errors
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"skills.lock.json: invalid JSON: {exc}"]
    names: set[str] = set()
    for entry in lock.get("skills", []):
        name = entry.get("name", "")
        if name in names:
            errors.append(f"skills.lock.json: duplicate {name}")
        names.add(name)
        if entry.get("status") == "installed":
            if not (root / ".agents" / "skills" / name / "SKILL.md").is_file():
                errors.append(f"skills.lock.json: installed skill missing: {name}")
            if not (root / "third_party" / name / "LICENSE").is_file():
                errors.append(f"skills.lock.json: license missing: {name}")
            if not re.fullmatch(r"[0-9a-f]{40}", entry.get("revision", "")):
                errors.append(f"skills.lock.json: unpinned revision: {name}")
    return errors


def check_placeholders(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in ("AGENTS.md", "AGENTS.ko.md", "CLAUDE.md", "README.md"):
        path = root / relative
        if path.is_file() and re.search(r"\{\{[A-Z0-9_]+\}\}", path.read_text(encoding="utf-8")):
            errors.append(f"{relative}: unresolved template placeholder")
    return errors


def run_checks(root: Path) -> list[str]:
    checks = (
        check_required,
        check_skills,
        check_documents,
        check_links,
        check_wiring,
        check_external_skills,
        check_placeholders,
    )
    errors: list[str] = []
    for check in checks:
        errors.extend(check(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = run_checks(args.root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    skill_count = len(list((args.root / ".agents" / "skills").glob("*/SKILL.md")))
    print(f"harness check: PASS ({skill_count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
