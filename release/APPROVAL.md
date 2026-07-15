# Vibes to Verified - v0.1.0 Freeze and Release Receipt

## Status

**AUTHORIZED RELEASE CANDIDATE - GitHub release approved; repository launch post published and verified**

This dated receipt records the release authorization and evidence boundary for
`v0.1.0`. The controlling launch workflow authorized the exact candidate to be
tagged and published as a GitHub release after its required validation, fresh
review, and public CI gates pass. This authorization does not extend to the
draft X Article or its separate Article-launch post and replies.

## Candidate Snapshot

- Project: `vibes-to-verified`
- Release target: `v0.1.0`
- Public repository: <https://github.com/voltrace-io/vibes-to-verified>
- Last public baseline before the release changes:
  `a88ecf950f9a499c5715f1ef076c42d9fa17acde`
- Baseline tree: `74136cf0ffb2162340ee46b0ff706a7c9afc2d0e`
- Manifest: [`manifest.json`](manifest.json)
- Manifest status: `release_candidate`
- Manifest hashing rule: every tracked file except the manifest itself is bound
  by SHA-256; excluding the manifest avoids a self-hash cycle

The manifest value `approved_pending_creation` is a freeze-time authorization
snapshot. The immutable tag, GitHub release URL, and successful CI run are the
external read-back receipts after publication.

## Verified Public State

| Artifact | Receipt |
|---|---|
| Source repository | Public and readable at the repository URL above |
| Baseline `main` CI | Passed for `a88ecf9` before this release round |
| Repository launch post | Published and verified: <https://x.com/VoltraceGG/status/2077436347292271041> |
| X post read-back | X API v2 matched author `@VoltraceGG`, normalized approved copy, post ID, and one 720x1280 video |
| X Article | Not published; remains a separate approval gate |
| Article-launch post and replies | Not published; remain a separate approval gate |

## Hermes Runtime Boundary

On 2026-07-15, a literal `/v2v` command was entered in Hermes Desktop. The UI
showed `loading skill: v2v` and Hermes injected its skill-invocation message.
Runtime inspection resolved `/v2v` to the installed V2V skill, identified the
session source as `desktop`, and found the installed repository clean at
`a88ecf9`. The installed `SKILL.md` SHA-256 is:

```text
0370fd3c0315e3d309914d47114df4390eaa4b18d68b5a7c8655caeab9127e7d
```

That hash matches the skill body in this release candidate. The receipt proves
Hermes Desktop slash dispatch for those bytes. It does not prove Claude Code
live discovery or execution, and it does not generalize to every Hermes
interface or configuration.

Hermes Desktop did not expose `/reload-skills` in its slash palette during this
check. A terminal or gateway may expose it; Desktop users should start a new
session or restart Desktop after installation.

## Release Gates

| Gate | Freeze-time disposition |
|---|---|
| Exact staged manifest | PASS for the substantive candidate; rebuild required after review-receipt append |
| Required artifact validator | PASS |
| Complete contract tests | PASS - 59 of 59 |
| Privacy scan | PASS - all 57 tracked files enumerated |
| Ruff and Python compilation | PASS |
| Full-history Gitleaks scan | PASS locally across all 15 reachable commits; exact-commit public CI read-back pending |
| Fresh contract/runtime review | GREEN for the substantive frozen candidate |
| Fresh privacy/disclosure review | GREEN, within its documented bounded scope |
| Fresh editorial/release review | GREEN; immutable tag link correction applied before the successor review |
| Receipt-only successor review | Required after the manifest rebuild |
| Exact-commit public CI read-back | Required before tag |
| Create and push `v0.1.0` tag | GitHub release approved after all gates pass |
| Create GitHub release | Approved for the exact verified tag |
| Publish X Article | Not approved by this receipt |
| Publish Article-launch post or replies | Not approved by this receipt |

## Authorized Procedure

1. Stage every intended candidate file except `release/manifest.json`.
2. Build the manifest from the staged Git blobs, then stage the manifest.
3. Run the validator, complete tests, privacy scan, compilation, Ruff, staged
   whitespace check, and full-history secret scan.
4. Obtain fresh independent contract/runtime, privacy/disclosure, and
   editorial/release reviews against the frozen candidate.
5. Commit and push the exact candidate, require successful public CI and
   secret-scan read-back, and protect `main` with those required checks.
6. Create a new annotated `v0.1.0` tag at that exact commit. Do not publish the
   stale local release-candidate tag.
7. Publish and read back the GitHub release for that tag.

Any failed or ambiguous gate stops tag and release creation. It does not
authorize reposting the already-public X launch post.
