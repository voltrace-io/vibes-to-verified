#!/usr/bin/env python
"""Validate the Vibes to Verified package and evidence cards."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "evidence-card.schema.json"
REQUIRED_PATHS = [
    "README.md",
    "SKILL.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "SOURCES.md",
    ".github/workflows/validate.yml",
    "requirements-dev.txt",
    "references/v2v-scale.md",
    "references/verdict-vs-evidence.md",
    "references/common-failure-modes.md",
    "templates/evidence-card.yaml",
    "templates/approach-registry.md",
    "templates/refutation-round.md",
    "schemas/evidence-card.schema.json",
    "examples/coding-agent.md",
    "examples/research-claim.md",
    "examples/options-paper-trading-risk-control.md",
    "examples/evidence-card-v0.yaml",
    "article/article.md",
    "article/launch-copy.md",
    "article/media-map.md",
    "media/ALT_TEXT.md",
    "media/exports/article-cover.png",
    "media/exports/github-social-card.png",
    "media/exports/v2v-scale.png",
    "media/exports/v2v-workflow.png",
    "media/exports/paper-trading-receipt.png",
    "media/exports/vibes-to-verified-launch-v4.mp4",
    "media/exports/vibes-to-verified-vertical.mp4",
    "scripts/build_release_manifest.py",
    "release/manifest.json",
    "release/APPROVAL.md",
    "release/reviews/review-dispositions.md",
    "video/README.md",
    "video/plan.md",
    "video/vibes_to_verified.py",
]


def parse_skill_frontmatter(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter at byte 0")
    match = re.search(r"\n---\s*\n", content[4:])
    if not match:
        raise ValueError("SKILL.md frontmatter is not closed")
    end = match.start() + 4
    frontmatter = yaml.safe_load(content[4:end])
    body = content[end + len(match.group(0)) - 1 :].strip()
    if not isinstance(frontmatter, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    if not body:
        raise ValueError("SKILL.md body must not be empty")
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        raise ValueError("Skill name must be lowercase kebab-case and at most 64 characters")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Skill description is required")
    if len(description) > 1024:
        raise ValueError("Skill description exceeds 1024 characters")
    if len(content) > 100_000:
        raise ValueError("SKILL.md exceeds 100,000 characters")
    return frontmatter


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def load_evidence_card(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Evidence card must be a mapping: {path}")
    return value


def validate_semantics(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    level = card.get("v2v_level")
    verdict = card.get("verdict")
    claim_id = card.get("claim_id")
    evidence = [item for item in card.get("evidence", []) if isinstance(item, dict)]
    operational = [
        item for item in card.get("operational_proof", []) if isinstance(item, dict)
    ]
    scope = card.get("scope", {})
    scope_artifact = (
        str(scope.get("artifact", "")).strip() if isinstance(scope, dict) else ""
    )

    def supports_claim(item: dict[str, Any]) -> bool:
        return claim_id in item.get("supports", [])

    def matches_artifact(item: dict[str, Any]) -> bool:
        return str(item.get("subject_artifact", "")).strip() == scope_artifact

    if level != "V0":
        artifact_key = scope_artifact.lower()
        if artifact_key in {
            "",
            "unknown",
            "n/a",
            "none",
            "replace with an exact path, url, commit, hash, or state identifier.",
        }:
            errors.append(f"{level} requires an identified artifact")

        if not evidence or not all(supports_claim(item) for item in evidence):
            errors.append(f"{level} evidence must support the card claim_id")
        elif not all(matches_artifact(item) for item in evidence):
            errors.append(f"{level} evidence must match scope.artifact")

    if level in {"V2", "V3", "V4"}:
        tests = [item for item in evidence if item.get("kind") == "test"]
        if not tests:
            errors.append(f"{level} requires at least one test evidence item")
        else:
            if not all(supports_claim(item) for item in tests):
                errors.append(f"{level} test evidence must support the card claim_id")
            elif not all(matches_artifact(item) for item in tests):
                errors.append(f"{level} test evidence must match scope.artifact")

    if level in {"V3", "V4"}:
        reviews = [
            item
            for item in evidence
            if item.get("kind") == "review"
            and item.get("independence")
            in {"independent_agent", "independent_human"}
        ]
        if not reviews:
            errors.append(f"{level} requires at least one independent review evidence item")
        else:
            if not all(supports_claim(item) for item in reviews):
                errors.append(f"{level} review evidence must support the card claim_id")
            elif not all(matches_artifact(item) for item in reviews):
                errors.append(f"{level} review evidence must match scope.artifact")

        dispositions = [
            item
            for item in card.get("claim_dispositions", [])
            if isinstance(item, dict) and item.get("claim_id") == claim_id
        ]
        if not dispositions:
            errors.append(f"{level} requires a disposition for the card claim_id")
    else:
        dispositions = [
            item
            for item in card.get("claim_dispositions", [])
            if isinstance(item, dict) and item.get("claim_id") == claim_id
        ]

    if level == "V4":
        runtimes = [item for item in operational if item.get("kind") == "runtime"]
        readbacks = [item for item in operational if item.get("kind") == "readback"]

        if not runtimes:
            errors.append("V4 requires runtime operational proof")
        else:
            if not all(supports_claim(item) for item in runtimes):
                errors.append("V4 runtime proof must support the card claim_id")
            elif not all(matches_artifact(item) for item in runtimes):
                errors.append("V4 runtime proof must match scope.artifact")

        if not readbacks:
            errors.append("V4 requires readback operational proof")
        else:
            if not all(supports_claim(item) for item in readbacks):
                errors.append("V4 readback proof must support the card claim_id")
            elif not all(matches_artifact(item) for item in readbacks):
                errors.append("V4 readback proof must match scope.artifact")

    main_review_results = {
        item.get("result")
        for item in evidence
        if item.get("kind") == "review"
        and supports_claim(item)
        and matches_artifact(item)
    }
    main_statuses = {item.get("status") for item in dispositions}
    negative_review_results = main_review_results & {"refuted", "blocked"}
    if "survived" in main_statuses and negative_review_results:
        errors.append(
            "survived main-claim disposition conflicts with a refuted or blocked review"
        )

    if verdict == "GREEN":
        if card.get("open_blockers"):
            errors.append("GREEN requires open_blockers to be empty")
        if main_statuses & {"refuted", "blocked"}:
            errors.append("GREEN cannot accompany a refuted or blocked main claim")
        if negative_review_results:
            errors.append("GREEN cannot accompany a refuted or blocked review result")
        if level in {"V3", "V4"} and "survived" not in main_statuses:
            errors.append(f"GREEN / {level} requires a survived main-claim disposition")

    return errors


def validate_card(path: Path) -> list[str]:
    schema = load_schema()
    card = load_evidence_card(path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(card)]
    errors.extend(validate_semantics(card))
    return errors


def validate_package() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"Required file is empty: {relative}")

    try:
        frontmatter = parse_skill_frontmatter(ROOT / "SKILL.md")
        if frontmatter.get("name") != "v2v":
            errors.append("SKILL.md name must be v2v")
    except Exception as exc:  # validation should report every failure together
        errors.append(str(exc))

    try:
        load_schema()
    except Exception as exc:
        errors.append(f"Invalid JSON schema: {exc}")

    cards = [
        ("Template", ROOT / "templates" / "evidence-card.yaml"),
        ("Example", ROOT / "examples" / "evidence-card-v0.yaml"),
    ]
    for label, card_path in cards:
        if card_path.is_file():
            errors.extend(f"{label}: {error}" for error in validate_card(card_path))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "card",
        nargs="?",
        type=Path,
        help="Optional evidence-card YAML file to validate",
    )
    args = parser.parse_args()

    errors = validate_package()
    if args.card:
        card_path = args.card if args.card.is_absolute() else Path.cwd() / args.card
        errors.extend(f"Card: {error}" for error in validate_card(card_path))

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED")
    print(f"root={ROOT}")
    print(f"required_files={len(REQUIRED_PATHS)}")
    if args.card:
        print(f"card={args.card}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
