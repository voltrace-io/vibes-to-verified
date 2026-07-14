---
name: v2v
description: Use when AI-generated work, agent conclusions, code, research, automation, or consequential decisions must move from plausible output to scoped, falsifiable, independently challenged, operationally evidenced results. Applies the V2V Scale, adversarial portfolio search, atomic claims, refutation rounds, and evidence-card reporting without assuming the desired answer exists.
version: 0.1.0
author: Voltrace
license: MIT
metadata:
  hermes:
    tags: [verification, adversarial-review, agent-skills, evidence, vibe-coding]
    related_skills: []
---

# Vibes to Verified

## Overview

Vibes to Verified is a portable verification workflow for AI-assisted work. It preserves the speed of vibe coding while matching authority to evidence.

The problem is not starting with a vibe. The problem is granting production authority to output that never moved beyond one.

The workflow separates two questions:

1. **Verdict:** What does the evidence currently suggest?
2. **V2V level:** How mature is that evidence?

A confident answer can be `GREEN / V0`. A rigorously reproduced failure can be `RED / V4`. Never collapse those axes.

> Keep the speed. Add the proof.

## When to Use

Use this skill when a false conclusion could compound:

- AI-generated code on security, money, identity, permissions, deletion, publication, or external side-effect boundaries
- Agent architectures, migrations, concurrency, retries, recovery, or durable state
- Research claims that may influence action
- Trading or financial automation in simulation or production
- Expensive or difficult-to-reverse decisions
- Claims presented as tested, safe, complete, production-ready, or verified
- Reviews where several plausible approaches could share the same blind spot

Do not use the full workflow for:

- trivial edits
- easily reversible formatting
- ordinary information lookup
- low-stakes brainstorming
- tasks with no evidence source capable of distinguishing success from failure

For smaller tasks, use only the claim, acceptance criteria, direct test, and evidence card.

## Operating Principles

1. **Do not assume the desired answer exists.** `BLOCKED`, `RED`, and `REJECTED` are legitimate outcomes.
2. **Consensus is not proof.** Similar agents with shared context can make correlated errors.
3. **Claims must be atomic.** If a refuter cannot falsify a claim, rewrite it.
4. **Artifacts outrank prose.** Tests, source records, runtime output, hashes, and read-back decide.
5. **Independence must be real.** Do not give refuters the original persuasive reasoning.
6. **Scope every verdict.** Verification is never universal or permanent.
7. **Bound the search.** Default to three rounds: independent attempts, refutation, repair plus final verification.
8. **No artifact, no green light.** Self-reported completion remains unverified.

## The V2V Scale

| Level | Name | Minimum evidence |
|---:|---|---|
| `V0` | **Vibes** | A claim or generated result exists; no traceable evidence is attached. |
| `V1` | **Grounded** | The claim points to primary sources, exact files, code paths, raw data, or other traceable evidence. |
| `V2` | **Tested** | The claim survives a controlled, repeatable test against explicit acceptance criteria. |
| `V3` | **Adversarial** | Independent reviewers attempt to refute atomic claims; concrete failures are reproduced, repaired, and re-reviewed. |
| `V4` | **Operational** | The final artifact works through its real environment and natural invocation path, with observable read-back, monitoring, recovery visibility, and repetition when the claim requires it. |

### Level Rules

- Higher levels inherit all lower-level requirements.
- Passing unit tests is `V2`, not automatically `V3` or `V4`.
- A review that merely agrees with the builder is not adversarial evidence.
- A mocked path cannot establish operational proof for a real external boundary.
- `V4` means operationally verified **within the named scope**, not proved forever.
- If a required artifact cannot be inspected, cap the level below the requirement it would satisfy.

## Verdicts

| Verdict | Meaning |
|---|---|
| `GREEN` | The scoped claim currently survives the required evidence and verification gates. |
| `YELLOW` | The claim has meaningful support, but named limitations prevent full authority. |
| `RED` | A concrete counterexample, failed criterion, or unsafe condition exists. |
| `BLOCKED` | Required evidence or access is unavailable, so the claim cannot be decided. |
| `REJECTED` | The objective is malformed, unfalsifiable, unsafe, or not worth the requested verification cost. |

Verdict precedence is conservative: `REJECTED` or `RED` cannot be overridden by confidence; unresolved required evidence forces `BLOCKED` or `YELLOW`, not `GREEN`.

## Workflow

### Step 0: Bound the Task

Write:

- exact objective
- why the result matters
- permitted actions and forbidden actions
- time, tool, and side-effect budget
- required V2V level
- public/private disclosure boundary

Do not launch broad fan-out before the task is bounded.

### Step 1: Convert the Objective into Atomic Claims

Bad:

> The system is safe.

Good:

> Two concurrent workers sharing the same durable store cannot both acquire submission authority for the same operation.

Each claim must include:

```yaml
id: C-01
claim: One precise falsifiable statement.
scope: Where and when the statement is intended to hold.
acceptance: Observable condition that supports the claim.
rejection: Observable counterexample that falsifies it.
evidence_required: Exact artifact or execution needed.
```

If the claim contains several independently falsifiable statements, split it.

### Step 2: Build an Independent Approach Portfolio

Choose incompatible reasoning families appropriate to the task. Examples:

- builder or constructive approach
- state-machine or invariant analysis
- adversarial or abuse-case analysis
- operator or usability analysis
- evidence and provenance audit
- economic or incentive analysis
- recovery and failure-mode analysis

Preserve independence during the first pass:

- Do not tell every worker the favored answer.
- Do not expose one worker's persuasive narrative to another.
- Vary the framing, not just the wording.
- Ask for concrete claims, mechanisms, tests, or counterexamples.

If only one agent/context is available, simulate separation with sequential role passes and disclose that this is weaker than independent review.

### Step 3: Maintain the Approach Registry

Record each approach in `templates/approach-registry.md` or an equivalent structured artifact.

Statuses:

- `active`
- `promising`
- `blocked`
- `refuted`
- `survived`
- `deferred`

An elegant reduction that ends at a missing assumption equivalent to the original task is `blocked`, not nearly complete.

Reopen a blocked route only when new evidence, a new invariant, or a materially different mechanism appears.

### Step 4: Collect and Deduplicate Claims

The coordinator must:

1. merge independently produced claims
2. separate duplicate wording from genuinely independent mechanisms
3. retain disagreement
4. assign stable claim IDs
5. attach exact evidence locations
6. remove status reports and vague optimism

Agreement count may raise a claim's prior, but it does not raise its V2V level.

### Step 5: Run a Refutation Round

Give refuters:

- the atomic claim list
- the final candidate artifact or raw evidence
- acceptance and rejection criteria
- permission to return `BLOCKED`

Do **not** give them the original agents' chains of reasoning unless a specific argument itself must be audited.

For each claim, require:

```text
claim_id | survives | counter_evidence | reproduction | severity | smallest_repair
```

A claim survives only when no refuter produces valid counter-evidence within the defined scope. “Looks correct” is not a refutation result.

### Step 6: Reproduce, Repair, and Re-run

For every credible failure:

1. reproduce it against the real candidate artifact
2. create a regression test or durable evidence record
3. repair the smallest sufficient boundary
4. run focused tests
5. run the full relevant suite
6. present the **new final artifact** to a fresh reviewer

Do not let a reviewer approve bytes or state that were later modified.

Maximum default cycle count: two repair cycles after the initial refutation round. If serious failures remain, return `RED` or `BLOCKED` instead of looping indefinitely.

### Step 7: Establish Operational Proof

`V4` requires the natural path, not a substitute:

- real scheduler, event, command, or user flow
- real durable state
- real external boundary when authorized
- real read-back or observable outcome
- repeated execution when repetition is part of the claim
- monitoring and recovery visibility

A successful POST, click, exit code, or self-report is not enough when public/read-back verification is possible.

### Step 8: Issue the Evidence Card

Use `templates/evidence-card.yaml` and validate it against `schemas/evidence-card.schema.json` when tooling permits.

Schema validation enforces structural prerequisites only. It cannot prove artifact authenticity, test relevance, or reviewer independence; inspect those claims directly before promotion.

Every promotion record must support the card's `claim_id` and bind `subject_artifact` to `scope.artifact`. V2 test records declare procedure, expected result, observed result, and repetition count. V3 review records declare reviewer, independence mode, attempted challenge, and result. The validator can enforce those declarations but cannot authenticate the reviewer identity. `GREEN / V3+` additionally requires an empty `open_blockers` list and a `survived` disposition for the main claim.

The final report must contain:

- claim
- verdict
- V2V level
- scope
- acceptance criteria
- surviving evidence
- claim dispositions and counter-evidence
- operational proof, if any
- limitations
- disclosure boundary
- smallest next action

## Evidence Promotion Rules

| Promotion | Required proof |
|---|---|
| `V0 → V1` | Traceable primary source, artifact, file, or raw evidence attached |
| `V1 → V2` | Controlled test with explicit expected and observed result |
| `V2 → V3` | Independent refutation of atomic claims against the final artifact |
| `V3 → V4` | Natural real-environment execution plus observable read-back and scoped repetition |

Never promote because:

- the answer is detailed
- several agents agree
- a builder says tests passed
- a mocked demo looks realistic
- a file path was claimed but not checked
- the external action returned an ID without read-back

## Output Contract

Return this compact summary first:

```text
VERDICT: GREEN | YELLOW | RED | BLOCKED | REJECTED
V2V: V0 | V1 | V2 | V3 | V4
CLAIM: <atomic scoped claim>
SCOPE: <where the verdict holds>
EVIDENCE: <exact artifacts and results>
LIMITATIONS: <named gaps>
NEXT: <smallest useful action>
```

Then provide the full evidence card and claim dispositions.

Do not use “proved,” “safe,” “complete,” or “production-ready” without a named scope and evidence level.

## Lightweight Mode

For a bounded low-to-medium-risk task:

1. Write one atomic claim.
2. Define acceptance and rejection criteria.
3. Inspect the primary artifact.
4. Run one direct test.
5. Issue a verdict and V2V level.

Do not manufacture a multi-agent ceremony when a direct test decides the question.

## Common Pitfalls

1. **Agent count theater.** More workers with the same framing produce correlated confidence.
2. **Builder-as-verifier.** The author reviews their own persuasive reasoning instead of the final artifact.
3. **Non-atomic claims.** “The auth layer has problems” cannot be decisively refuted.
4. **Equivalent missing lemma.** A hard problem is renamed and declared nearly solved.
5. **Test-path substitution.** A manual or mocked path is presented as natural operation.
6. **Stale review.** The reviewed artifact changes after approval.
7. **Consensus promotion.** Agreement raises confidence but not evidence maturity.
8. **Infinite search.** The workflow refuses legitimate `BLOCKED` or `RED` outcomes.
9. **Disclosure leakage.** Verification receipts expose secrets, private paths, strategies, account data, or exploitable implementation details.
10. **Green without scope.** The verdict silently expands beyond what was tested.

## Privacy and Publication

Before publishing a case study:

- disclose the problem class and verification process
- remove secrets, credentials, account data, private identifiers, paths, schedules, proprietary thresholds, and reproducible attack details
- preserve exact receipts only when they do not expose protected implementation
- label simulated, paper, mocked, or sandbox execution honestly
- state what was not independently verified

Use `disclosure_boundary` in every public evidence card.

## Verification Checklist

- [ ] Objective and authority are bounded
- [ ] Claims are atomic and falsifiable
- [ ] Acceptance and rejection criteria are explicit
- [ ] Independent approaches use materially different frames
- [ ] Approach registry records blocked and refuted routes
- [ ] Refuters receive the final artifact, not only summaries
- [ ] Every failure is reproduced or marked unverified
- [ ] Repairs have regression evidence
- [ ] Full relevant tests run against final bytes
- [ ] Natural execution is used before claiming `V4`
- [ ] External outcomes are read back when possible
- [ ] Verdict and V2V level remain separate
- [ ] Scope and limitations are visible
- [ ] Public output passes the disclosure boundary
- [ ] Exact artifacts exist and are non-empty

## Closing Rule

Vibe coding is not the problem. Stopping at vibes is.

Build fast. Challenge the result. Keep only what survives.
