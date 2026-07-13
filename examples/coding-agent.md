# Example: Coding Agent Concurrency Claim

This example is synthetic and demonstrates structure, not a tested product.

## Objective

Determine whether two concurrent workers can both acquire authority for the same external side effect.

## Atomic Claim

```yaml
id: C-01
claim: Two workers sharing one durable store cannot both acquire submission authority for the same operation identifier.
scope: Same host, shared SQLite-compatible store, final candidate implementation.
acceptance: Exactly one worker receives authority in every exercised race.
rejection: Two workers receive authority for the same operation identifier.
evidence_required: Concurrency test, persisted state inspection, and independent refutation.
```

## Independent Approaches

| Family | Question |
|---|---|
| Builder | What atomic claim mechanism prevents two winners? |
| State machine | Which transitions can race or repeat? |
| Adversary | Can stale reads, retries, or crashes create a second winner? |
| Evidence | Are tests exercising the final durable implementation? |
| Operator | Does the natural scheduler invoke the same path? |

## Expected Progression

- Source inspection with exact code locations: `V1`
- Repeatable forced-race test: `V2`
- Independent refuters fail to find a second-winner path after repairs: `V3`
- Real scheduler repeatedly invokes the final implementation with observable state: `V4`

## Example Verdict

```text
VERDICT: YELLOW
V2V: V2
CLAIM: Two same-host workers cannot both acquire authority.
SCOPE: Controlled forced-race harness against the final candidate store.
EVIDENCE: One winner in all recorded test runs.
LIMITATIONS: No independent refutation or natural scheduler execution yet.
NEXT: Run a fresh adversarial review against the final artifact.
```
