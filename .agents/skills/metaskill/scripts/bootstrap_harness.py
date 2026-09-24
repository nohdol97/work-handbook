#!/usr/bin/env python3
"""Create a goal-driven personal harness from reviewed local and external assets."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable

from install_external_skills import install_candidates


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
CORE_SKILLS = ("metaskill", "adr", "spec-driven-development", "test-driven-development")
LOCAL_CAPABILITY_SKILLS = {
    "cloudflare": "operate-cloudflare",
    "electron": "build-electron-app",
    "github-secrets": "manage-github-secrets",
}


def source_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _copytree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def _local_skill_source(factory: Path, skill_name: str) -> Path:
    direct = factory / ".agents" / "skills" / skill_name
    if direct.is_dir():
        return direct
    seeded = (
        factory
        / ".agents"
        / "skills"
        / "metaskill"
        / "assets"
        / "seed-skills"
        / skill_name
    )
    if seeded.is_dir():
        return seeded
    raise FileNotFoundError(f"local seed skill is missing: {skill_name}")


def _render_tree(root: Path, values: dict[str, str]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        path.write_text(text, encoding="utf-8")


def _frontmatter_description(skill_file: Path) -> str:
    for line in skill_file.read_text(encoding="utf-8").splitlines()[1:]:
        if line == "---":
            break
        if line.startswith("description:"):
            return line.removeprefix("description:").strip().strip("\"'")
    return "설명 없음"


def write_skill_catalog(target: Path) -> None:
    sections = [
        "# 공통 스킬 카탈로그",
        "",
        "각 섹션은 실제 공유 스킬 하나와 정확히 연결된다. 세부 판단은 링크된 영어 원본을 따른다.",
        "",
    ]
    for skill_file in sorted((target / ".agents" / "skills").glob("*/SKILL.md")):
        name = skill_file.parent.name
        description = _frontmatter_description(skill_file)
        sections.extend(
            [
                f"## {name}",
                "",
                f"- 원본: [{name}/SKILL.md]({name}/SKILL.md)",
                f"- 역할·트리거: {description}",
                "- 사용하지 않을 때: 원본 description의 경계와 루트 라우팅을 따른다.",
                "- 완료 기준: 원본 절차의 검증과 루트 4필드 증거를 모두 충족한다.",
                "",
            ]
        )
    (target / ".agents" / "skills" / "README.ko.md").write_text(
        "\n".join(sections), encoding="utf-8"
    )


def _write_korean_digest_hash(target: Path) -> None:
    digest = hashlib.sha256((target / "AGENTS.md").read_bytes()).hexdigest()[:12]
    path = target / "AGENTS.ko.md"
    text = path.read_text(encoding="utf-8").replace("{{SOURCE_HASH}}", digest)
    path.write_text(text, encoding="utf-8")


def _run(command: list[str], cwd: Path) -> None:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"command failed ({' '.join(command)}): {detail}")


def bootstrap(
    target: Path,
    name: str,
    goal: str,
    capabilities: Iterable[str] = (),
    offline: bool = False,
    init_git: bool = True,
) -> dict[str, object]:
    capabilities = sorted(set(capabilities))
    unknown = set(capabilities) - set(LOCAL_CAPABILITY_SKILLS)
    if unknown:
        raise ValueError(f"unknown capabilities: {', '.join(sorted(unknown))}")
    if not NAME_RE.fullmatch(name):
        raise ValueError("name must match ^[a-z0-9][a-z0-9-]{0,63}$")
    if not goal.strip():
        raise ValueError("goal must not be empty")

    target = target.resolve()
    factory = source_root().resolve()
    if target == factory or factory in target.parents:
        raise ValueError("target must not be the factory or one of its descendants")
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(f"target is not empty: {target}")
    target.mkdir(parents=True, exist_ok=True)

    template = factory / ".agents" / "skills" / "metaskill" / "assets" / "harness-template"
    _copytree(template, target)
    (target / ".agents" / "skills").mkdir(parents=True, exist_ok=True)
    (target / ".agents" / "agents").mkdir(parents=True, exist_ok=True)
    (target / ".agents" / "projects").mkdir(parents=True, exist_ok=True)
    (target / "project").mkdir(parents=True, exist_ok=True)
    (target / "_workspace").mkdir(parents=True, exist_ok=True)

    for skill_name in CORE_SKILLS:
        _copytree(
            _local_skill_source(factory, skill_name),
            target / ".agents" / "skills" / skill_name,
        )
    for capability, skill_name in LOCAL_CAPABILITY_SKILLS.items():
        if capability in capabilities:
            _copytree(
                _local_skill_source(factory, skill_name),
                target / ".agents" / "skills" / skill_name,
            )

    shutil.copy2(factory / "scripts" / "check_harness.py", target / "scripts" / "check_harness.py")
    values = {
        "HARNESS_NAME": name,
        "HARNESS_GOAL": goal.strip(),
        "CREATED_DATE": date.today().isoformat(),
        "CAPABILITIES": ", ".join(capabilities) if capabilities else "core only",
    }
    _render_tree(target, values)

    external_results = install_candidates(
        target,
        factory / ".agents" / "skills" / "metaskill" / "references" / "external-skills.json",
        capabilities,
        offline=offline,
    )
    write_skill_catalog(target)
    _write_korean_digest_hash(target)

    claude = target / ".claude"
    claude.mkdir(exist_ok=True)
    (claude / "skills").symlink_to("../.agents/skills")
    (claude / "agents").symlink_to("../.agents/agents")

    if init_git:
        _run(["git", "init", "-b", "main"], target)
    _run([sys.executable, "scripts/check_harness.py"], target)

    return {
        "target": str(target),
        "name": name,
        "goal": goal.strip(),
        "capabilities": capabilities,
        "external_skills": external_results,
        "git_initialized": init_git,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--no-git", action="store_true")
    args = parser.parse_args()

    result = bootstrap(
        args.target,
        args.name,
        args.goal,
        args.capability,
        offline=args.offline,
        init_git=not args.no_git,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
