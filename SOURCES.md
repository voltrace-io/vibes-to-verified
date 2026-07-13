# Sources and Provenance

This file records the public source chain used to develop Vibes to Verified.

## Original X Post

- Author: Balázs Pozsgay (`@pozsgaybalazs`)
- URL: https://x.com/pozsgaybalazs/status/2076409894152884720
- Visible text: “We used this one:” followed by a PDF link
- Inspected in read-only mode on `2026-07-13`.

## OpenAI Prompt PDF

- Title: `PROMPT USED FOR "A PROOF OF THE CYCLE DOUBLE COVER CONJECTURE"`
- Publisher named in document: OpenAI
- Public URL: https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf
- Retrieved on: `2026-07-13`
- Size: `123015` bytes
- SHA-256: `0e48deee28caba82ee5b4191d4c5c6ec4d62e5d27890fa7f0d2c8868f8b758f3`

The PDF contains the prompt, not the mathematical proof. Its abstract states that the prompt was given to GPT-5.6 Sol Ultra and “led to its proof” of the Cycle Double Cover Conjecture. This repository does not independently verify that mathematical proof or claim the conjecture has been settled.

## Mechanics Adapted

The source prompt informed these mechanics:

- diverse independent approach families
- delayed convergence
- explicit approach registry
- blocking theorem-strength missing lemmas
- adversarial review of concrete claims
- repeated synthesis and redirection
- rejection of partial progress presented as completion

## Mechanics Deliberately Changed

Vibes to Verified does **not** copy the instruction to assume an affirmative solution exists or forbid an open/blocked conclusion.

The portable workflow preserves calibrated outcomes:

- `GREEN`
- `YELLOW`
- `RED`
- `BLOCKED`
- `REJECTED`

It also adds:

- the V2V evidence maturity scale
- verdict-versus-evidence separation
- bounded convergence
- operational verification
- artifact identity requirements
- public disclosure boundaries
- privacy-safe case-study guidance

## Claude Code Skill Directory Convention

Official Claude Code documentation was checked through the public Anthropic documentation/search surface. The current documented project convention is:

```text
.claude/skills/*/SKILL.md
```

Source: https://docs.anthropic.com/en/docs/claude-code/skills

## Verification Note

Source attribution is evidence for the origin of the inspiration. It is not evidence that the resulting Vibes to Verified framework is effective. Effectiveness must be established through the repository's own tests, adversarial review, and real use.
