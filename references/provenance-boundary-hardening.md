# Provenance boundaries for operational verification

Use this when a claim depends on data being official, first-party, fresh, or captured through a particular natural path.

## Core rule

Enforce provenance at every callable authority boundary, not only in the CLI or scheduler that normally reaches it. Removing a command-line override does not close a bypass if an imported function still accepts a caller-controlled status such as `eligible`, `approved`, or `verified`.

## Trust ladder

1. **Parser output is unverified.** A file matching the expected schema proves shape, not origin. Label direct/manual normalization as operator-supplied or unverified.
2. **Capture orchestration may promote it.** Upgrade evidence only after the orchestrator establishes the expected origin and path, such as exact HTTPS host/path, allowlisted browser operation, fresh post-baseline download, stable file, and successful parsing.
3. **Derived decisions revalidate.** Before producing authority-bearing output, require exact source role, evidence tier, capture method, canonical URL, bounded freshness, and any independent reconciliation available.
4. **Natural entrypoints use fixed sources.** Production CLI and scheduler paths should use fixed canonical input locations. Do not expose source-path or status overrides when those values decide authority.
5. **Pure APIs accept evidence, not conclusions.** Pass a sourced evidence object into internal functions; derive status inside the function. Do not accept a bare `eligible`, `safe`, `approved`, or similar conclusion from the caller.

## The self-attestation trap

A hash carried inside the same caller-controlled JSON object does not prove provenance. An attacker or buggy producer can relabel public data as first-party, recompute internally consistent hashes, and pass role/method checks. Schema validity, labels, and self-reported hashes establish internal consistency only.

For authority-bearing decisions:

- recompute hashes from the raw source bytes at the decision boundary;
- bind the normalized record to a stable source artifact path or immutable object ID;
- require a capture receipt produced by the allowlisted capture operation, not copied from the normalized payload;
- recompute canonical payload hashes for browser-read summaries;
- verify the capture receipt, raw artifact, normalized record, and derived record agree;
- state the attacker model honestly. Without a platform signature or independently protected receipt, do not claim resistance to a fully privileged local forger.

A capture receipt should include the operation, exact origin/path, capture timestamps, source artifact identity, byte size, and raw hash. The verifier must recompute what it can; merely comparing duplicated receipt fields is not independent evidence.

### Raw bytes versus normalized parser content

Keep two hashes when parsing can normalize source material:

- `source_raw_sha256`: hash the exact bytes after the capture has landed on disk;
- `source_sha256`: hash the decoded or canonical form consumed by the parser.

At the authority boundary, recompute both, verify the receipt's byte count against the raw file, then reparse the source and compare every authority-bearing normalized field. This avoids a subtle false mismatch on Windows and BOM-bearing CSVs: `Path.write_text()` may translate `\n` to `\r\n`, while `read_text()` and CSV parsing may normalize newlines. Tests must compute the raw hash from `read_bytes()` *after* writing the fixture and compute the normalized hash with the same decoding and newline semantics as production.

For browser-read summaries with no downloaded file, retain the allowlisted source payload, canonicalize it deterministically (`sort_keys`, fixed separators, explicit UTF-8), record canonical byte length and hash in the capture receipt, then reparse and reconcile the normalized summary before granting authority.

### Removing caller-controlled overrides completely

When deleting a status or source override from an authority CLI, search and update every active wrapper, scheduler script, generated dispatcher copy, and imported function signature. A removed parser flag is not complete if a wrapper still passes it or an internal API still accepts the conclusion. Verify the fixed-source natural scheduler after the removal; a unit test of the parser alone is insufficient.

### Natural-path surface prerequisites

A fail-closed natural run can legitimately stop because its exact browser surface or other read-only prerequisite is absent. Preserve that receipt rather than weakening target selection or broadening URL matching. Establish the exact allowlisted surface through an isolated/reversible target, rerun the real scheduler, validate durable read-back, and then restore the browser state (for example, close the temporary target). Report the first failure as prerequisite evidence, not as a successful V4 run or as proof the feature is broken.

## Full-field reconciliation and freshness

Reconcile every field that can grant authority, not just the headline metric. If impressions reconcile but verified followers, account status, permissions, or compliance can differ between the bound source and the derived trajectory, the boundary remains bypassable.

Freshness must be checked against a trusted wall-clock `as_of`, not only relative to another source. Two mutually consistent captures from years ago are still stale. Test stale/stale, future/future, stale/fresh, and fresh/stale combinations. Use injectable time in pure tests and real current time in the natural path.

## Adversarial tests

For every positive provenance path, add negative cases for:

- missing capture method;
- wrong source role or evidence tier;
- wrong origin or near-prefix URL;
- stale or future-dated evidence;
- manually supplied data presented as native;
- mismatched independent totals or hashes;
- a fully relabeled, internally consistent payload whose raw source artifact is absent or does not match;
- a derived verified-follower/account-status value that disagrees with its bound summary source;
- jointly stale sources that agree with each other but fail wall-clock freshness;
- a direct function call that bypasses the normal CLI;
- a production CLI attempt to override fixed source or status inputs.

A reviewer should challenge both the natural route and every public/importable function that can emit the claimed result.

## Immutable-runtime tests

Tests that import hard-coded live scripts outside the reviewed Git commit do not, by themselves, verify immutable candidate bytes. Prefer a committed mirror. If the runtime cannot be vendored or relocated:

1. hash the exact external runtime artifacts;
2. assert those hashes before loading them;
3. include the external hashes in the candidate manifest and evidence card;
4. add positive and negative contract tests, including missing and mismatched attestations;
5. disclose that the candidate spans Git plus hash-bound external artifacts.

Do not claim exact-commit reproducibility from a test that silently imports mutable live code.

## Verdict rule

If the natural scheduler is safe but an internal authority API accepts unsourced conclusions, the broad provenance claim is `RED` or `YELLOW`, not `GREEN`. Narrowing scope is legitimate only when the callable API is explicitly excluded and cannot affect the asserted operational authority.