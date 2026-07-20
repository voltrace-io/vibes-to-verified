# Verification Prompts — paste-ready blocks for any agent

These prompts work with any AI agent (ChatGPT, Claude, Gemini, Cursor, Hermes, or a custom pipeline). Paste them after an agent claims work is done. They map to the four gates: source, test, break it, real.

The human assigns the final score. An agent scoring its own work is a starting signal, never the verdict.

---

## Gate 1 — Source (V0 → V1)

```text
For every claim in your answer, attach the exact source behind it:
file path, command output, URL, data row, or quote with location.
If a claim has no attachable source, relabel it UNVERIFIED and
separate it from the evidence-backed claims. Do not remove it.
```

## Gate 2 — Test (V1 → V2)

```text
Write the test that would prove this result works: setup, expected
result, and the failure condition that would make you reject it.
Then run it twice against the final artifact, not a draft, and paste
both real outputs. If you cannot run it, say exactly what blocks you.
```

## Gate 3 — Break it (V2 → V3)

```text
Now act as a reviewer who has never seen this conversation and does
not care about your previous reasoning. Your only job is to find the
strongest reason this result is wrong, incomplete, or unsafe.
List concrete failure modes, then check each one against the actual
artifact or evidence. Report what survives and what breaks.
```

Single-agent honesty rule: the same model reviewing its own work is weaker than an independent reviewer. Treat self-review as `V2+`, not full `V3`, unless the reviewer had materially different context, tools, or data.

## Gate 4 — Real (V3 → V4)

```text
Describe the exact natural path this runs through in real use:
the real command, scheduler, user flow, or external system — not a
demo or mock. What durable state changes, and what observable
read-back proves it worked? Run that path if authorized and report
what you observed, including limits and what was not verified.
```

## Score (assign after the gates)

```text
Score this work against the four gates:
4/4 verified — source attached, test passed twice, challenged, real path observed
3/4 close — name the missing gate and the smallest fix
2/4 risky — treat as a draft
0–1/4 vibes — confident output without evidence
State which gate failed and the evidence for the score.
```

---

## Red flags that output is still V0

- "This should work" / "this will handle it" — prediction, not observation
- No file paths, no test output, no artifacts
- Screenshots or pasted code instead of executed runs
- "Tests pass" without the command and output
- An ID or success message with no read-back of the result
- The agent grades its own work as verified with no external check

## Domain quick cards

| Work type | V2 looks like | V4 looks like |
|---|---|---|
| Code | Tests pass twice on the final bytes | Deployed/natural path works with read-back |
| Research | Claims survive explicit accept/reject criteria | Someone tried to find a counterexample and failed |
| Creative/media | Real file exists, non-zero, reviewed against intent | Published path verified after posting |
| Automation | One controlled run passes | Ran through the real scheduler/event with logs |
| Decisions/purchases | Compared against explicit criteria | Terms verified on primary sources before committing |
