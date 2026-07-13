# Vibes to Verified — Release Approval Card

## Status

**YELLOW — repaired local candidate, not published**

All deterministic checks pass. Prior independent-review findings are repaired and regression-covered. A fresh review of the exact manifest-bound candidate is still pending. No public action is authorized by this file.

## Candidate

- Project: `vibes-to-verified`
- Version: `0.1.0-rc1`
- Workspace: local private repository
- Manifest: [`manifest.json`](manifest.json)
- Review dispositions: [`reviews/review-dispositions.md`](reviews/review-dispositions.md)
- Manifest status: `local_candidate_not_published`
- Tracked files: 50
- Files bound by SHA-256 after manifest rebuild: 49 of 50; the manifest excludes only itself to avoid a self-hash cycle

## Verification Receipts

| Gate | Result |
|---|---|
| Required artifact validator | PASS — 37 required files |
| Contract tests | PASS — 48/48 against the manifest-bound candidate |
| Privacy scan | PASS — 50 tracked files, including text and supported media metadata |
| Ruff static analysis | PASS |
| Python compilation | PASS |
| Staged Git whitespace check | PASS |
| Internal Markdown links | PASS |
| SVG parsing | PASS |
| PNG dimensions and metadata | PASS |
| GPT Image source metadata | PASS — pixel content preserved; `caBX`, EXIF, and PNG info removed |
| MP4 contract | PASS |
| Clean Claude-style directory layout | PASS — copy validation only; live discovery unclaimed |
| Clean Hermes-style directory layout | PASS — copy validation only; live discovery unclaimed |
| Full-motion video review | PASS — no blocking visual defect |
| Prior skill/schema review findings | REPAIRED — regression-covered |
| Prior privacy/disclosure review findings | REPAIRED — scanner and public scope narrowed |
| Prior source/editorial review findings | REPAIRED — source and private-case claims recalibrated |
| Fresh manifest-bound contract review | PENDING |
| Fresh manifest-bound privacy review | PENDING |
| Fresh manifest-bound source/editorial review | PENDING |

## Scope

The package includes:

- portable Agent Skill
- V0–V4 evidence scale
- independent approach and refutation workflow
- evidence-card schema and semantic validator
- contract and privacy tests
- complete draft X Article and launch copy
- deterministic diagrams
- metadata-sanitized GPT Image 2 conceptual source with deterministic typography
- native vertical Manim video
- sanitized options PAPER-trading case whose private-V4 claim is public `BLOCKED / V0`

## Public Gates

| Public action | Current state |
|---|---|
| Create a public GitHub repository | NOT APPROVED |
| Push candidate and enable public CI | NOT APPROVED |
| Publish X Article | NOT APPROVED |
| Publish launch post and replies | NOT APPROVED |

## Approval Sequence

1. Rebuild `release/manifest.json` after this card is final.
2. Run the complete verification suite and require 48/48 tests.
3. Commit the immutable candidate locally.
4. Run fresh independent contract, privacy, and editorial reviews against that exact commit.
5. Repair any blocker, rebuild the manifest, and repeat if required.
6. Present the exact Article, launch post, replies, media, hashes, and commit.
7. Request GitHub publication approval.
8. Read back the public repository and CI result.
9. Bind the verified repository and case-study URLs into the Article, present the exact Article candidate, and request X Article approval.
10. Read back the Article URL.
11. Bind the verified Article URL into the launch copy, show the final launch bundle, and request posting approval.

Failure or ambiguity at any stage keeps the next gate closed.
