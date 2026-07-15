#!/usr/bin/env python
"""Build a hash manifest for the immutable launch candidate."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release" / "manifest.json"
MANIFEST_RELATIVE = OUTPUT.relative_to(ROOT).as_posix()


def tracked_release_files() -> list[str]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    files = sorted(
        item.decode("utf-8")
        for item in raw.split(b"\0")
        if item and item.decode("utf-8") != MANIFEST_RELATIVE
    )
    if not files:
        raise SystemExit("no tracked release files found")
    return files


def staged_blob(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT)


def require_staged_candidate() -> None:
    raw = subprocess.check_output(["git", "diff", "--name-only", "-z"], cwd=ROOT)
    unstaged = {
        item.decode("utf-8")
        for item in raw.split(b"\0")
        if item and item.decode("utf-8") != MANIFEST_RELATIVE
    }
    if unstaged:
        joined = ", ".join(sorted(unstaged))
        raise SystemExit(f"stage tracked candidate changes before manifest build: {joined}")


def video_probe(path: Path) -> dict:
    raw = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_name,width,height,r_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        text=True,
    )
    return json.loads(raw)


def main() -> None:
    require_staged_candidate()
    artifacts = []
    for relative in tracked_release_files():
        data = staged_blob(relative)
        if not data:
            raise SystemExit(f"missing or empty release artifact: {relative}")
        artifacts.append(
            {
                "path": relative,
                "size_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    muted_video_path = ROOT / "media" / "exports" / "vibes-to-verified-vertical.mp4"
    launch_video_path = ROOT / "media" / "exports" / "vibes-to-verified-launch-cut-r1.mp4"
    manifest = {
        "project": "vibes-to-verified",
        "repository_url": "https://github.com/voltrace-io/vibes-to-verified",
        "version": "0.1.0",
        "status": "release_candidate",
        "generated_on": datetime.now(timezone.utc).date().isoformat(),
        "artifacts": artifacts,
        "video_probe": video_probe(muted_video_path),
        "launch_video_probe": video_probe(launch_video_path),
        "verification_commands": [
            "python scripts/validate.py",
            "python -m unittest discover -s tests -v",
            "python scripts/privacy_scan.py",
            "python -m compileall -q scripts media video tests",
            "ruff check scripts media video tests",
            "gitleaks git --redact --verbose --log-opts=--all .",
            "git diff --cached --check",
        ],
        "security_scan": {
            "tool": "gitleaks",
            "version": "8.30.1",
            "scope": "all_reachable_commits",
            "asset_sha256": "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb",
        },
        "publication_gates": {
            "public_github_repository": "published_verified",
            "github_release_v0_1_0": "approved_pending_creation",
            "x_article_and_launch_bundle": "not_published",
            "x_repository_launch_post": "published_verified",
        },
        "publication_receipts": {
            "x_repository_launch_post": {
                "status": "published_verified",
                "url": "https://x.com/VoltraceGG/status/2077436347292271041",
                "post_id": "2077436347292271041",
                "author_username": "VoltraceGG",
                "readback_source": "X API v2",
                "verified_on": "2026-07-15",
            },
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {OUTPUT} {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
