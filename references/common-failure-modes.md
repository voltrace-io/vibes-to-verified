# Common Failure Modes

## 1. Agent Count Theater

Many agents receive nearly identical framing and produce correlated conclusions. Agreement is reported as independent verification.

**Repair:** assign incompatible approach families and preserve early independence.

## 2. Builder-as-Verifier

The same context that constructed the solution judges its own reasoning.

**Repair:** give a fresh reviewer the final artifact, claims, and acceptance criteria without the builder's persuasive narrative.

## 3. Non-Atomic Claims

“The system is secure” cannot be decisively tested or refuted.

**Repair:** split into scoped statements with observable rejection conditions.

## 4. Equivalent Missing Assumption

A hard task is reduced to a lemma or compatibility statement with equivalent difficulty, then described as nearly solved.

**Repair:** mark the route `blocked` until a new mechanism proves the missing statement.

## 5. Test-Path Substitution

A manual command or mocked environment is used to claim the scheduler, browser, broker, or production path works.

**Repair:** reserve V4 for the natural invocation path and real read-back.

## 6. Stale Review

A reviewer approves version A; version B is shipped after repairs or refactoring.

**Repair:** identify final bytes or state and re-review after every material change.

## 7. Consensus Promotion

Several agents agree, so an unsupported claim is promoted from V0 or V1.

**Repair:** only evidence gates promote V2V levels.

## 8. Success-ID Confusion

An external service returns an ID or HTTP success, but the destination is never inspected.

**Repair:** read back the exact external object and compare against the approved artifact.

## 9. Neutral-Fallback Corruption

A failed scorer or reviewer returns a midpoint that looks like a real judgment and silently alters ranking or confidence.

**Repair:** use an explicit unavailable state and degrade to deterministic evidence or `BLOCKED`.

## 10. Unbounded Search

The workflow refuses to return failure and keeps launching agents until one produces the desired answer.

**Repair:** cap rounds and accept `RED`, `BLOCKED`, and `REJECTED`.

## 11. Privacy Leakage Through Receipts

A public case study includes private paths, account data, strategies, credentials, schedules, or exploitable details to appear transparent.

**Repair:** publish the problem class, verification process, broad failure classes, and non-sensitive receipts. Define a disclosure boundary before drafting.

## 12. Green Without Scope

A narrow test result is generalized into “safe,” “complete,” or “production-ready.”

**Repair:** bind every verdict to environments, artifacts, dates, assumptions, and limitations.

## 13. Review Without Reproduction

A reviewer reports a plausible bug that is immediately treated as fact.

**Repair:** reproduce against the final artifact or mark the finding unverified.

## 14. Tests Without Threat Model

A large suite passes but never exercises the actual dangerous boundary.

**Repair:** derive tests from atomic claims and rejection criteria, not coverage volume alone.

## 15. Operational Proof Without Monitoring

One natural run succeeds and the system is declared reliable.

**Repair:** name the repetition scope and ensure failures remain observable and recoverable.
