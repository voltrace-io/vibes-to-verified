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
| The installed `/v2v` skill differed from the manifest-bound candidate | Accepted | The short command identifier, validator, tests, installation paths, and documentation are now included in the staged candidate before manifest rebuild. |
| README and approval text still said Hermes live invocation was unclaimed | Accepted | Public copy now records one scoped Telegram-gateway `/v2v` invocation after `/reload-skills` while keeping Claude Code live execution and general compatibility unclaimed. |
| Claude's documented folder path would expose the old long command | Accepted | Claude and Hermes installation paths now both use the `v2v` directory slug. |
| V3/V4 production sources and QC files exposed private workspace structure and broke the full-directory Ruff command | Accepted | Production sources, QC records, and review intermediates remain under `.private/`; `video/reviews/` is ignored. Only the final V4 MP4 is promoted publicly. |
| The V4 launch asset was not manifest-bound or documented | Accepted | The exact MP4 is promoted to `media/exports/vibes-to-verified-launch-v4.mp4`, required by the validator, contract-tested, probed by the manifest, and documented with provenance and accessibility text. |
| Full-playback disclosure review backend could not ingest the local V4 file | Partially mitigated | Technical decode and black/freeze/silence checks passed; a 2 fps chronological contact sheet and exact-audio transcript were independently inspected for visible/audible disclosure. The backend ingestion limitation remains disclosed. |
| “Rights-cleared” wording lacked a public redistribution/license boundary | Accepted | Public copy now qualifies the creator's publication-rights report, withholds the private receipt, identifies the Suno track in `media/RIGHTS.md`, and excludes embedded narration/music from standalone MIT reuse. |
| Exact skill-release lessons existed only as installed-copy drift | Accepted | The slash-command, candidate-boundary, media-promotion, and immutable-editorial procedures are now included deliberately in `SKILL.md` and three tracked references. |

## Remaining Gate

A fresh reviewer must inspect the exact manifest-bound candidate. Publication remains unauthorized until that review passes and the user separately approves each public gate.
