# vibe coding isn’t the problem. stopping at vibes is.

## a five-level system for turning AI-generated work into verified evidence

vibe coding deserves some of its criticism.

people generate software they do not understand, watch it pass one happy-path demo, and call it production-ready. fluent code gets mistaken for correct code. a confident agent report gets mistaken for an inspected artifact. a passing test gets stretched into a claim about the real system.

that is how slop acquires authority.

but the initial vibe is not the failure.

starting from intent instead of syntax can be useful. it can help domain experts build, make early exploration cheaper, and turn ideas into testable artifacts faster.

we should keep that speed.

what we need is a credible path from generated output to earned trust.

not vibes **or** rigor.

vibes **to** verified.

## 64 agents can still share one blind spot

this started with a strange artifact published by OpenAI: the full prompt reportedly used for a GPT-5.6 Sol Ultra attempt at the Cycle Double Cover Conjecture.

[the published prompt](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf) is not the mathematical proof. its abstract says the prompt “led to” a proof, but i have not independently verified that proof or the underlying mathematical claim.

what i could inspect was the orchestration design.

it gave the model access to as many as 64 concurrent agents, but agent count was not the interesting part. the prompt tried to prevent those agents from becoming one large agreement machine.

it required:

- a genuinely diverse portfolio of approaches
- independence during early rounds
- an explicit registry of approach families
- blocked status for routes that stalled at theorem-strength gaps
- several incompatible routes kept alive simultaneously
- adversarial agents checking concrete failure modes
- lemmas, constructions, equations, or counterexamples instead of status reports
- repeated synthesis and redirection rather than one wave of parallel output

that is a much stronger design than “ask five agents and let one summarize them.”

parallelizing production is not the same as parallelizing disagreement. this prompt tried to do both.

## agent count is not independence

if 64 agents receive the same framing, share the same favored approach, inherit the same assumptions, and optimize for the same desired conclusion, they can produce 64 versions of the same mistake.

the volume of agreement makes the result feel stronger even when the evidence has not changed.

this is correlated error disguised as consensus.

independence has to be designed:

- different approach families
- delayed exposure to the favored answer
- explicit disagreement retention
- reviewers rewarded for finding counterexamples
- claims small enough to falsify
- final artifacts inspected instead of persuasive summaries

agreement may increase confidence.

it does not increase evidence maturity by itself.

## the one instruction i would not steal

OpenAI’s prompt also told the system to assume that a complete affirmative proof existed. it said not to answer that the conjecture was open and to return only after an affirmative proof survived audit.

that may increase persistence. it also creates pressure to convert an unresolved gap into a finished answer.

for a benchmark, that trade may be deliberate.

for software, security, research, automation, or trading infrastructure, it is dangerous.

if the desired result does not exist, the system must be allowed to say so.

if decisive evidence is unavailable, it must be allowed to stop.

if a concrete failure survives, it must be allowed to return red.

my version preserves five legitimate verdicts:

- **green:** the scoped claim survives the required gates
- **yellow:** meaningful support exists, but named limitations remain
- **red:** a concrete counterexample or failed criterion exists
- **blocked:** decisive evidence or access is unavailable
- **rejected:** the objective is malformed, unfalsifiable, unsafe, or not worth the cost

persistence is useful.

forced certainty is not.

## the V2V scale

that distinction led to a separate question:

> how mature is the evidence behind the verdict?

not how polished is the answer.

not how many agents agree.

not how confident the model sounds.

### V0 — vibes

an answer or artifact exists. no traceable evidence is attached.

examples:

- the agent says the feature is complete
- the code looks plausible
- a screenshot shows one successful demo
- a file or URL is claimed but never inspected

V0 is not shameful. it is a starting state.

it just should not receive production authority.

### V1 — grounded

the claim points to primary, inspectable evidence:

- exact sources
- final files
- raw data
- current configuration
- artifact hashes
- external read-back

V1 establishes that the reasoning touches reality. it does not establish that the interpretation is correct.

### V2 — tested

the claim survives a controlled, repeatable test against explicit acceptance and rejection criteria.

controlled tests are useful, but passing them still cannot tell you whether the test author missed the dangerous boundary.

### V3 — adversarial

independent reviewers attempt to falsify atomic claims against the final artifact.

credible failures must be reproduced. repairs need regression evidence. modified artifacts must be reviewed again.

“looks correct” does not count.

### V4 — operational

the final artifact works through its natural environment and invocation path, with observable results and named limits.

not a mocked route.

not a manual substitute for the scheduler.

not an HTTP success code without reading the destination.

V4 is always scoped. it means operational evidence exists for the claim and environment that were actually exercised. it does not mean “proved safe forever.”

## verdict and evidence are different axes

this matters because favorable and well-evidenced are not synonyms.

`green / V0` means someone believes it works without attached proof.

`green / V2` means it passed controlled tests.

`red / V4` can mean a failure was repeatedly observed in the real environment.

that last result is negative, but the evidence is mature.

this prevents an uncomfortable trick: treating “green” as rigor and “red” as failure of the verification process.

sometimes red is the most valuable verified result you can get.

## what this looks like on a real AI-built system

we used the underlying process while hardening an automated options paper-trading risk-control system.

no live capital was involved.

this is not a trading-strategy disclosure. i am not publishing positions, account data, entry criteria, risk thresholds, broker configuration, private code, infrastructure, or implementation-specific attack steps.

what matters is the verification progression.

### review one: red

an independent reviewer found failure classes involving invalid signed-position handling, duplicate simulated actions, and assumptions that did not hold across all position states.

we reproduced the findings, added regression evidence, and repaired the candidate.

### review two: red again

a fresh reviewer inspected the repaired artifact and found different classes involving concurrent authority, incomplete discovery of external state, older paths bypassing newer controls, and mismatches between persisted and externally represented values.

those findings were also reproduced and repaired.

### review three: green in the private review scope

a new reviewer inspected the final artifact and found no remaining critical blockers within the reviewed boundary.

the internal verification record, summarized in [the sanitized public case](https://github.com/voltrace-io/vibes-to-verified/blob/v0.1.0/examples/options-paper-trading-risk-control.md), reported:

- 186 passing tests
- 42 passing subtests
- 20 forced concurrency iterations
- one natural PAPER run

those receipts do not prove profitability, live-money safety, universal broker compatibility, or freedom from future defects.

they report a narrower progression inside the private engineering scope:

```text
AI-generated implementation          V0
final artifacts inspected privately  V1
controlled suites passed privately   V2
independent refutation privately      V3
natural PAPER run recorded privately  reported V4 in that PAPER scope
public claim about private V4         V0, blocked on raw receipts
```

that V4 classification belongs to the private engineering record. the private-V4 claim remains V0 for public readers because the raw code, execution records, and external-state receipts are intentionally withheld.

more importantly, the reviews changed the artifact.

the first reviewer did not provide reassurance. it found a real defect class.

the second did not simply agree with the repair. it found another one.

that is what productive disagreement looks like.

## the workflow

Vibes to Verified turns that process into a portable agent skill.

it asks the agent to:

1. bound the task, authority, and disclosure limits
2. convert the objective into atomic falsifiable claims
3. define acceptance and rejection criteria
4. preserve materially different approach families
5. maintain an explicit approach registry
6. give fresh refuters the final artifact instead of the builder’s confidence
7. reproduce failures and require regression evidence
8. verify the natural operational path before claiming V4
9. issue a structured evidence card with verdict, level, scope, limitations, and next action

it also has a lightweight mode. not every task needs an army of agents. if one direct test can settle a low-risk claim, run the test.

verification should reduce uncertainty, not manufacture ceremony.

## make your agents prove it

i packaged the workflow as an MIT-licensed Agent Skill:

[repository](https://github.com/voltrace-io/vibes-to-verified)

it includes:

- the complete `SKILL.md`
- the V2V specification
- verdict-versus-evidence rules
- an approach registry
- an independent refutation contract
- a machine-readable evidence-card schema
- sanitized coding, research, and paper-trading examples
- package validation and privacy tests

version 0.1 is intentionally small.

no dashboard. no hosted platform. no verification theater.

just a reusable workflow that can be installed, challenged, forked, and improved.

## keep the speed. add the proof.

vibe coding can lower the barrier to building software.

that is worth protecting.

but lower barriers will not earn durable trust if generated systems repeatedly ship with authority their evidence never earned.

the answer is not to return building to a smaller priesthood.

it is to make verification more accessible too.

start with the vibe.

ground it.

test it.

try to break it.

then observe what survives in the real system.

keep the speed.

add the proof.
