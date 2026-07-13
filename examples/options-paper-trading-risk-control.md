# Sanitized Case: Options Paper-Trading Risk Control

## Disclosure Statement

This case concerns an AI-assisted automated **options paper-trading risk-control system**. It did not control live capital.

This public record describes the verification process and broad failure classes. It deliberately excludes:

- trading strategy
- symbols, positions, balances, or buying power
- account or broker configuration
- entry and exit thresholds
- position sizing
- private source code
- database schema
- local paths and scheduler identities
- credentials and session data
- reproducible implementation-specific attack steps

## Why the Case Mattered

The artifact affected a consequential PAPER-only workflow. A fluent implementation or passing happy-path tests were not sufficient evidence for granting broader authority.

## Review Progression

### Independent Review 1 — RED

The reviewer identified failure classes involving:

- invalid signed-position handling
- duplicate simulated action risk
- assumptions that did not hold across all position states

The findings were reproduced against the candidate artifact. Regression evidence was added before repair.

### Independent Review 2 — RED

A fresh reviewer inspected the repaired artifact and identified different classes involving:

- concurrent authority
- incomplete discovery of external state
- older paths bypassing newer controls
- mismatches between persisted and externally represented values

Those findings were independently reproduced and repaired. The full relevant suite was rerun.

### Independent Review 3 — GREEN in the Private Review Scope

A new review of the final artifact found no remaining P0 or P1 blockers within the reviewed scope.

## Evidence Receipts

The final private artifact recorded:

- `186` passing tests
- `42` passing subtests
- `20` forced concurrency iterations
- one natural PAPER run

These counts establish evidence volume only within their named scope. They do not prove trading profitability, live-money safety, universal broker compatibility, or freedom from all future defects.

## V2V Interpretation

| Stage | Supported level |
|---|---|
| AI-generated implementation | V0 |
| Final files and state inspected privately | V1 |
| Controlled test suites passed privately | V2 |
| Independent refutation and repair cycles passed privately | V3 |
| One natural PAPER run recorded privately | Reported V4 within the private PAPER scope |
| Sanitized public case, without raw receipts | V0 for the private-V4 claim |

## Public Verdict

```text
VERDICT: BLOCKED
V2V: V0
CLAIM: The private artifact reached V4 within its recorded PAPER scope.
SCOPE: What a public reader can establish from this sanitized case.
EVIDENCE: No publicly inspectable primary artifact; only this sanitized author report.
BLOCKER: The raw code, test output, execution records, and external-state receipts are intentionally private.
LIMITATIONS: No live-money, profitability, universal-broker, or publicly reproducible implementation claim.
NEXT: Treat the private V4 result as reported, not publicly reproduced.
```

## Lesson

The first review did not merely confirm the builder. It changed the artifact. The second review found a different class of failure. The private record reports progression through V2, V3, and narrowly scoped V4; the private-V4 claim remains V0 for public readers because its raw receipts are withheld.

The case is useful because it shows the distinction between generated code, passing tests, adversarial survival, and operational proof without disclosing the private trading system.
