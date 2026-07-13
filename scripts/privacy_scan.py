#!/usr/bin/env python
"""Fail closed when tracked public files contain likely secrets or private metadata."""

from __future__ import annotations

import argparse
import re
import struct
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BACKSLASH = chr(92)
WINDOWS_USERS_PREFIX = "C:" + BACKSLASH + "Users" + BACKSLASH
WINDOWS_USERS_SLASH_PREFIX = "C:" + "/" + "Users" + "/"
WORKSPACE_PREFIX = "C:" + BACKSLASH + "Ai" + "_Work" + BACKSLASH

PATTERNS = {
    "private_windows_user_path": re.compile(
        re.escape(WINDOWS_USERS_PREFIX) + r"[^\\\s]+", re.I
    ),
    "private_windows_user_path_slash": re.compile(
        re.escape(WINDOWS_USERS_SLASH_PREFIX) + r"[^/\s]+", re.I
    ),
    "private_msys_user_path": re.compile(r"/[a-z]/Users/[^/\s]+", re.I),
    "private_ai_work_path": re.compile(re.escape(WORKSPACE_PREFIX), re.I),
    "github_token": re.compile(r"gh[opusr]_[A-Za-z0-9_]{20,}"),
    "openai_key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "discord_webhook": re.compile(
        r"https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9._-]+", re.I
    ),
    "telegram_token": re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
    "generic_secret_assignment": re.compile(
        r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
    "private_ipv4": re.compile(
        r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
    ),
}

ALLOWED_LITERAL_PATHS = {
    ".claude/skills/vibes-to-verified",
    "~/.hermes/skills/vibes-to-verified",
}
PNG_METADATA_CHUNKS = {b"caBX", b"eXIf"}


class TrackedFileEnumerationError(RuntimeError):
    """Raised when the tracked release boundary cannot be established."""


def _git_tracked_files(root: Path) -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=root, stderr=subprocess.DEVNULL
        )
        files = [root / raw.decode("utf-8") for raw in output.split(b"\0") if raw]
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        raise TrackedFileEnumerationError(
            "git ls-files failed; tracked release tree unavailable"
        ) from exc
    if not files:
        raise TrackedFileEnumerationError("tracked release tree is empty")
    return files


def iter_public_files(root: Path):
    for path in _git_tracked_files(root):
        try:
            relative = path.relative_to(root)
        except ValueError:
            raise TrackedFileEnumerationError("tracked path escaped the release root")
        if not path.is_file():
            raise TrackedFileEnumerationError(
                f"tracked release file is missing or not regular: {relative.as_posix()}"
            )
        yield path


def _scan_text(relative: Path, text: str) -> list[str]:
    findings: list[str] = []
    normalized = text
    for allowed in ALLOWED_LITERAL_PATHS:
        normalized = normalized.replace(allowed, "<allowed-install-path>")
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(normalized):
            line = normalized.count("\n", 0, match.start()) + 1
            findings.append(f"{relative.as_posix()}:{line}: {name}")
    return findings


def _decode_supported_text(data: bytes) -> str | None:
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16")
        except UnicodeDecodeError:
            return None
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _png_chunk_types(data: bytes) -> list[bytes]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")
    chunks: list[bytes] = []
    offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunks.append(chunk_type)
        offset += 12 + length
        if chunk_type == b"IEND":
            break
    return chunks


def _scan_png(root: Path, path: Path) -> list[str]:
    relative = path.relative_to(root)
    findings: list[str] = []
    try:
        data = path.read_bytes()
        chunks = _png_chunk_types(data)
        for chunk in sorted(PNG_METADATA_CHUNKS & set(chunks)):
            findings.append(
                f"{relative.as_posix()}:1: png_metadata_chunk:{chunk.decode('ascii')}"
            )
        with Image.open(path) as image:
            metadata_parts = []
            for key, value in image.info.items():
                metadata_parts.extend([str(key), str(value)])
            for key, value in dict(image.getexif()).items():
                metadata_parts.extend([str(key), str(value)])
        if metadata_parts:
            findings.extend(_scan_text(relative, "\n".join(metadata_parts)))
    except Exception as exc:
        findings.append(f"{relative.as_posix()}:1: png_metadata_inspection_failed:{exc}")
    return findings


def _scan_video(root: Path, path: Path) -> list[str]:
    relative = path.relative_to(root)
    try:
        output = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format_tags:stream_tags",
                "-of",
                "json",
                str(path),
            ],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return [f"{relative.as_posix()}:1: video_metadata_inspection_failed:{exc}"]
    return _scan_text(relative, output)


def scan(root: Path, *, files: Iterable[Path] | None = None) -> list[str]:
    findings: list[str] = []
    candidates = iter_public_files(root) if files is None else files
    for path in candidates:
        suffix = path.suffix.lower()
        if suffix == ".png":
            findings.extend(_scan_png(root, path))
            continue
        if suffix in {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}:
            findings.extend(_scan_video(root, path))
            continue

        text = _decode_supported_text(path.read_bytes())
        if text is None:
            continue
        findings.extend(_scan_text(path.relative_to(root), text))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        files = list(iter_public_files(root))
    except TrackedFileEnumerationError as exc:
        print("PRIVACY SCAN FAILED")
        print(f"- tracked_file_enumeration_failed: {exc}")
        return 1
    findings = scan(root, files=files)
    if findings:
        print("PRIVACY SCAN FAILED")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PRIVACY SCAN PASSED")
    print(f"files_enumerated={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
