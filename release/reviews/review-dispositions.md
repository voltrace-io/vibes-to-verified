# Independent Review Dispositions

## Status

Pre-freeze review findings have been repaired. The final manifest-bound candidate still requires a fresh read-only review before publication can be recommended.

## Contract Review

| Finding | Disposition | Repair |
|---|---|---|
| Promotion evidence could support a different claim | Accepted | Semantic validation now requires promotion evidence to support the card `claim_id`. |
| Evidence could describe stale bytes | Accepted | Every evidence and operational record now binds `subject_artifact` to `scope.artifact`. |
| V2 accepted a free-text item labeled `test` | Accepted | Test records require procedure, expected result, observed result, and repetition count. |
| V3 accepted a self-labeled review | Accepted | Review records require reviewer, independence mode, attempted challenge, and result; only declared independent human or agent reviews promote to V3. |
| V4 accepted incomplete operational proof | Accepted | V4 requires separate natural-runtime and read-back records, monitoring, recovery visibility, and claim-dependent repetition. |
| GREEN could coexist with a refuted or blocked main claim | Accepted | GREEN now requires no open blockers and, at V3+, a survived main-claim disposition. |
| Verdict and evidence maturity lacked explicit axis tests | Accepted | Regression tests cover valid `GREEN / V0` and `RED / V4` combinations. |

## Privacy and Release Review

| Finding | Disposition | Repair |
|---|---|---|
| Manifest covered only selected files | Accepted | Manifest generation now hashes every tracked candidate file except the self-referential manifest. |
| Scanner skipped text files and binary metadata | Accepted | Scanner now requires the tracked boundary, scans UTF-8 and BOM-marked UTF-16 text, inspects PNG metadata/chunks, and reads video tags through `ffprobe`. |
| Scanner source embedded a private workspace literal | Accepted | The signature is assembled dynamically and remains covered by a leak fixture. |
| GPT Image source contained a C2PA/JUMBF `caBX` chunk | Accepted | The tracked source is a pixel-identical metadata-sanitized export; the public provenance note records the treatment. |
| Public files embedded an unverified repository destination | Accepted | Publication destinations are placeholders and the social card is URL-free until public read-back. |
| Public PAPER case transferred private V4 authority | Accepted | The private V4 classification is reported only; the public claim is `BLOCKED / V0` because raw primary receipts are withheld. |
| Automated disclosure scanning could be mistaken for semantic proof | Accepted | `SECURITY.md` now states the scanner boundary and requires human semantic review. |

## Source and Editorial Review

| Finding | Disposition | Repair |
|---|---|---|
| “64-agent proof prompt” exceeded the source | Accepted | Copy now says the proof-search prompt allowed up to 64 concurrent agents. |
| Exact private case results lacked public primary receipts | Accepted | Article links to a sanitized case, labels results as internally reported, and keeps the public private-V4 claim at V0. |
| Broad multi-agent and engineering generalizations were unsupported | Accepted | Prevalence framing was removed in favor of claim-specific or conditional language. |
| Categorical benefits exceeded evidence | Accepted | Benefits now use calibrated “can” language. |
| Package could be read as proven | Accepted | Launch metadata says `tested_not_proven`. |

## Exact-Candidate Follow-up

| Finding | Disposition | Repair or rationale |
|---|---|---|
| Git enumeration failure fell back to the surrounding workspace | Accepted | Default scanning now raises a tracked-boundary error and the CLI exits nonzero; no workspace fallback remains. |
| “Decodable text” exceeded the implemented UTF-8-only path | Accepted | The scanner now supports UTF-8 plus BOM-marked UTF-16 and documents other binary formats as outside semantic inspection. |
| GREEN-blocked and V3/V4 binding branches lacked direct negative tests | Accepted | Five focused regressions now cover blocked dispositions plus review and operational claim/artifact binding. |
| Manifest does not contain the commit that contains it | Not embedded | Embedding the future commit hash would create another self-reference cycle. The external release receipt pairs the immutable commit with the separately computed manifest hash; the manifest already binds every other tracked artifact. |
| One valid promotion record could mask another wrong-claim or stale-artifact record | Accepted | Every evidence record must now support and bind the card claim/artifact; level-specific test, review, runtime, and read-back sets use universal rather than existential checks. Mixed-record regressions cover V2, V3, and V4. |
| A refuted review could conflict with a survived disposition | Accepted | Current-artifact negative review results now conflict with a survived disposition and independently block `GREEN`; direct regression coverage is included. |
| Working-tree line endings could differ from committed SVG blobs | Accepted | Manifest generation now requires staged candidate files and hashes Git index blobs. The contract test compares every entry to its staged commit blob. |
| `files_scanned` telemetry implied unsupported binaries were semantically inspected | Accepted | CLI telemetry now reports `files_enumerated`; documentation separately names supported text and media inspection. |
| A publication-gate test embedded the planned repository destination as its sentinel | Accepted | The test now rejects generic hard-coded GitHub repository URLs in publication-facing files while retaining placeholder checks; no unpublished destination is stored in source. |

## `/v2v` Rename and Launch-Cut Review

| Finding | Disposition | Repair or rationale |
|---|---|---|
| The installed `/v2v` skill differed from the manifest-bound candidate | Accepted | Installed-copy equality is no longer claimed. Public copy now distinguishes current live discovery/resolution from exact-candidate natural invocation, which remains unclaimed. |
| README and approval text could imply the final skill body had been naturally invoked | Accepted | Public copy states that the one direct invocation preceded final package hardening and does not establish natural-path execution for this exact candidate. |
| `V4` was overloaded as both Operational evidence and a video revision label | Accepted | The release media now uses the neutral filename `vibes-to-verified-launch-cut-r1.mp4`; `V4` remains reserved for evidence maturity. |
| The Comfy footage was present but stretched until it read as stagnant imagery | Accepted | The final launch cut plays all five 49-frame Comfy plates at native 24 fps with ping-pong continuity, reduced global suppression, and zero detected freeze intervals. |
| Claude's documented folder path would expose the old long command | Accepted | Claude and Hermes installation paths both use the `v2v` directory slug. |
| Production sources and QC files exposed private workspace structure and broke the full-directory Ruff command | Accepted | Production sources, QC records, voice masters, and review intermediates remain under `.private/`; `video/reviews/` is ignored. Only the final narrated launch cut is promoted publicly. |
| The narrated launch asset was not manifest-bound or documented | Accepted | The exact MP4 is promoted to `media/exports/vibes-to-verified-launch-cut-r1.mp4`, required by the validator, contract-tested, probed by the manifest, and documented with provenance and accessibility text. |
| Full-playback disclosure review backend could not ingest the local launch cut | Partially mitigated | Technical decode and black/freeze/silence checks passed; a 2 fps chronological contact sheet and exact-audio transcript were independently inspected for visible/audible disclosure. The backend ingestion limitation remains disclosed. |
| “Rights-cleared” wording lacked a public redistribution/license boundary | Accepted | Public copy now qualifies the creator's publication-rights report, withholds the private receipt, identifies the Suno track in `media/RIGHTS.md`, and excludes embedded narration/music from standalone MIT reuse. |
| The changelog said production sources were “preserved” even though only authored code and deterministic assets are tracked and the private generation/compositing workspaces are excluded | Accepted | The changelog now distinguishes tracked authored/deterministic assets from excluded private production workspaces and account/rights receipts. |
| Exact skill-release lessons existed only as installed-copy drift | Accepted | The slash-command, candidate-boundary, media-promotion, and immutable-editorial procedures are included deliberately in the manifest-bound package. |
| The documented launch-cut hash still identified the superseded media | Accepted | `video/README.md` now records the exact promoted blob hash, and a regression test binds the documented hash to both the file bytes and manifest entry. |
| The changelog could imply exact-candidate natural invocation | Accepted | The historical invocation is now explicitly identified as pre-hardening; exact-candidate and Claude Code live invocation remain untested. |
| The changelog said final artifacts were not yet committed | Accepted | Release-state wording now records that the artifacts are committed locally while fresh review and publication approvals remain pending. |

## Fresh exact-candidate review round — 2026-07-14

**Substantive candidate:** commit `40c2264b851c9d92f1f60a204a0bdb44468f88c9`, tree `b6c6794e39922b436f2676cc8d2e5c5b966d1adf`.

| Review lane | Disposition | Evidence boundary |
|---|---|---|
| Contract/runtime | GREEN — no evidenced blocker | Exact archive matched the requested tree; 55 tracked files and 54 manifest entries matched; validator, 54/54 tests, privacy scanner, Ruff, compilation, whitespace, full media decode, and media-identity checks passed. |
| Privacy/disclosure | GREEN — no evidenced blocker in the bounded offline scope | All 55 tracked files were audited; privacy scan passed; manifest entries matched; sampled frames and media metadata showed no account, browser, private-path, notification, or production-workspace disclosure. Sampling was not every-frame semantic inspection; audio was decoded but not independently transcribed; legal sufficiency and the private rights receipt remain outside scope. |
| Editorial/source | GREEN / V3 — no publication blocker | Public copy, source attribution, neutral media naming, exact media identity, V0–V4 terminology, runtime boundaries, placeholders, rights qualification, and publication gates were consistent at the exact substantive commit. |

This section records external review of the substantive candidate. It does not self-certify the receipt-only successor that contains it; that successor must receive a narrow exact-diff review before publication reliance.

## Remaining Gate

A narrow reviewer must verify that the receipt-only successor changes only review-state documentation and manifest bindings relative to the substantive candidate. Publication remains unauthorized until that review passes and the user separately approves each public gate.

## Superseding v0.1.0 Release Round - 2026-07-15

The findings and dispositions above are historical receipts for earlier
candidates. They are preserved rather than rewritten. The following later
state supersedes their publication-state language:

- the repository URL and sanitized case-study URL were bound only after public
  read-back;
- the repository-focused X launch post was approved through its Discord card,
  published, and verified through X API v2 at
  <https://x.com/VoltraceGG/status/2077436347292271041>;
- the draft X Article and its separate Article-launch post/replies remain
  unpublished and outside that approval;
- GitHub `v0.1.0` tag and release creation were authorized for the exact frozen
  candidate only after validation, fresh independent review, and public CI
  succeed;
- the release round adds full-history Gitleaks CI, Dependabot, SHA-pinned GitHub
  Actions, durable tag-pinned install commands, and a Hermes Desktop literal
  `/v2v` dispatch receipt scoped to the unchanged `SKILL.md` bytes.

### Frozen substantive candidate reviews

The three independent lanes below reviewed the same staged manifest blob,
`4a6855b1827781b0c944fba945334b23fa1c4d34`, before these receipt rows were
appended. Their lane-specific snapshot fingerprints use different review
scripts and are retained in the private review record.

| Review lane | Disposition | Evidence boundary |
|---|---|---|
| Contract/runtime | GREEN - no contract blocker | Manifest coverage matched all 56 non-self artifacts; validator, 59/59 tests, privacy scanner, Ruff, compilation, staged whitespace, workflow lint, install-script parsing, staged Gitleaks, and all-history Gitleaks passed. The unchanged `SKILL.md` hash supports the narrowly scoped Hermes Desktop dispatch claim. |
| Privacy/disclosure | GREEN - no privacy or security blocker in the bounded scope | All 57 tracked files were enumerated; Gitleaks found no leak in the staged candidate or any of 15 reachable commits; media metadata and visual samples disclosed no account data, local identifiers, raw strategy, or private implementation details. Ignored `.private/` browser and evidence captures contain credential-like local material and must remain private; they have never been tracked. |
| Editorial/source/release | GREEN - no release blocker | Public-value claims, source boundaries, rights language, install paths, the verified repository-post receipt, and the unpublished Article boundary were consistent. The Article's sanitized-case link was subsequently changed from mutable `main` to immutable `v0.1.0`; the tag must exist before that link resolves. |

The later Hermes-generated reference-only edit occurred in the installed clone
after the scoped proof invocation ended. It did not touch this candidate or
`SKILL.md`; the exact edit was removed, the installed clone was reconfirmed
clean at `a88ecf9`, and a private before/after remediation receipt was retained.
The runtime claim remains limited to the earlier observed invocation and does
not assert that later Hermes turns were side-effect-free.

Appending these receipts, updating the gate table, and correcting the tag link
creates a successor candidate. Rebuild the manifest and require a narrow
exact-diff review of only those successor changes before relying on this receipt
for tag creation. Until that review and exact-commit public CI pass, the tag
gate remains closed.
