# The V2V Scale

The Vibes to Verified Scale measures evidence maturity, not optimism, polish, or agreement.

## V0 — Vibes

A claim, design, or generated artifact exists, but no traceable evidence supports it.

Common signals:

- “the agent says it is done”
- a detailed explanation without inspected artifacts
- screenshots with no reproducible path
- a claimed file, URL, or result that has not been read back

Allowed language:

- hypothesis
- candidate
- plausible
- unverified

## V1 — Grounded

The claim is connected to primary, inspectable evidence.

Examples:

- exact source URL and captured text
- exact repository path and final file contents
- raw data with provenance
- current configuration read from the live system
- artifact hash, size, and creation record

V1 does not establish that the interpretation is correct. It establishes that the reasoning is anchored to something real.

## V2 — Tested

The claim survives a controlled, repeatable test against explicit criteria.

Required:

- named claim
- acceptance condition
- rejection condition
- test procedure
- expected result
- observed result
- final artifact identity

Unit, integration, property, simulation, dry-run, and controlled browser tests can establish V2 within their scope.

A passing suite does not automatically establish:

- independent review
- correct threat model
- natural production execution
- behavior outside exercised cases

## V3 — Adversarial

Independent reviewers attempt to falsify atomic claims against the final artifact.

Required:

- independent or explicitly role-separated refuters
- atomic claim list
- counter-evidence search
- reproduction of credible failures
- regression evidence for repairs
- fresh review after final modification

Review independence is weaker when reviewers share the same model, context, prompt framing, or favored approach. Disclose those limitations.

## V4 — Operational

The artifact works through its natural environment and invocation path, with repetition shown when the claim requires it.

Examples:

- real scheduler invokes the final script
- real durable state survives restart
- authorized external call is read back from the destination
- natural user flow reaches the intended outcome
- monitoring exposes failure and recovery

Required:

- real final artifact
- natural trigger
- observable outcome
- scoped repetition when relevant
- named environmental limits
- rollback or recovery visibility for consequential systems

V4 is never universal. A valid statement is:

> V4 within same-host execution against the sandbox service path observed in the named environment.

An invalid statement is:

> Proven safe.

## Promotion Checklist

| From | To | Gate |
|---|---|---|
| V0 | V1 | Attach traceable primary evidence. |
| V1 | V2 | Run a controlled repeatable test. |
| V2 | V3 | Survive independent falsification attempts. |
| V3 | V4 | Work through the natural real-world path with read-back. |

## Demotion

Demote an evidence level when:

- the artifact changed after review
- source provenance is lost
- the test no longer reproduces
- the environment materially changed
- operational read-back becomes unavailable
- a new counterexample invalidates a required claim

Evidence maturity is a property of a scoped claim plus identified artifacts, not a permanent badge attached to a project.
