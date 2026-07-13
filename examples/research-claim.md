# Example: Research Claim

This example demonstrates how the V2V Scale applies outside software.

## Claim

> A named intervention causes the observed outcome in the studied population.

That sentence is not yet atomic enough. Rewrite it with:

- intervention definition
- population
- comparator
- outcome
- time window
- acceptable evidence type

## V2V Application

### V0 — Vibes

A model explains a plausible mechanism.

### V1 — Grounded

Primary studies, protocols, datasets, and outcome definitions are identified. Secondary summaries are not silently substituted for primary evidence.

### V2 — Tested

The analysis is reproducible against the cited data or a preregistered experiment tests the claim.

### V3 — Adversarial

Independent reviewers challenge:

- confounding
- selection effects
- measurement validity
- statistical assumptions
- alternative mechanisms
- publication bias
- scope generalization

Counter-evidence and failed replications are retained rather than averaged away.

### V4 — Operational

For many scientific claims, V4 may require repeated real-world replication across relevant settings. A single analysis should not claim this level.

## Calibrated Output

```text
VERDICT: YELLOW
V2V: V1
CLAIM: The intervention is associated with the named outcome in the cited observational cohort.
SCOPE: One cohort and the reported measurement window.
EVIDENCE: Primary paper and dataset provenance inspected.
LIMITATIONS: Causality, replication, and generalization remain unverified.
NEXT: Reproduce the analysis and test specified confounds.
```

The wording is intentionally weaker than the original causal claim because the evidence is weaker.
