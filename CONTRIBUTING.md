# Contributing

Vibes to Verified should become more rigorous through real counterexamples and use, not feature accumulation.

## Useful Contributions

- Reproduced failure modes
- Sanitized real-world evidence cards
- Platform installation guides verified against current releases
- Schema improvements with backward-compatibility notes
- Tests that catch invalid evidence promotion
- Integrations that preserve verdict, scope, and artifact identity
- Clear documentation corrections

## Before Opening a Pull Request

1. State the claim your change addresses.
2. Include acceptance and rejection criteria.
3. Add or update tests when behavior changes.
4. Run:

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

5. Remove secrets, account data, private paths, and proprietary implementation details.
6. Explain the maximum V2V level your evidence supports.

## Case Studies

A public case study must include:

- problem class
- simulated, sandbox, PAPER, or live status
- verdict and V2V level
- scoped evidence
- limitations
- disclosure boundary

Do not submit:

- credentials or tokens
- private repository contents
- personal financial data
- medical or identity data
- exploit details that create avoidable risk
- unverifiable marketing claims

## Design Changes

Changes to the scale or verdict definitions require:

- a concrete failure in the current specification
- an example the new rule handles better
- migration impact
- independent review

New levels should not be added merely to create finer-looking precision.

## Code of Conduct

Challenge claims, not people. Refutation is a quality mechanism, not a status contest.
