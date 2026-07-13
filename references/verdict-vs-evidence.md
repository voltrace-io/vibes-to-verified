# Verdict Versus Evidence

Vibes to Verified uses two independent axes.

## Axis 1: Verdict

The verdict answers:

> What does the current evidence suggest about this claim?

- `GREEN`: survives required gates within scope
- `YELLOW`: supported but limited
- `RED`: concrete failure exists
- `BLOCKED`: evidence is unavailable or insufficient
- `REJECTED`: objective is malformed, unsafe, unfalsifiable, or not worth the cost

## Axis 2: V2V Level

The level answers:

> How mature is the evidence supporting that verdict?

- `V0`: Vibes
- `V1`: Grounded
- `V2`: Tested
- `V3`: Adversarial
- `V4`: Operational

## Matrix Examples

| Verdict / Level | Interpretation |
|---|---|
| `GREEN / V0` | Someone believes it works. No evidence is attached. |
| `GREEN / V2` | It passed controlled tests within scope. |
| `GREEN / V3` | It passed tests and survived independent refutation. |
| `GREEN / V4` | It also worked through the natural real environment. |
| `YELLOW / V3` | Strongly reviewed evidence exists, but an explicit limitation blocks full authority. |
| `RED / V2` | A controlled test reproduces a failure. |
| `RED / V4` | The failure is repeatedly observed in real operation. |
| `BLOCKED / V1` | Sources exist, but the decisive artifact or access is unavailable. |
| `REJECTED / V1` | Evidence shows the objective itself should not proceed. |

## Authority Rule

The authority granted to an output must not exceed its evidence level.

Examples:

- `GREEN / V1` may justify further testing, not autonomous production action.
- `GREEN / V2` may justify a sandbox or PAPER trial.
- `GREEN / V3` may justify supervised deployment when operational proof is the remaining gap.
- `GREEN / V4` may justify scoped operation with monitoring, not unlimited authority.

Domain risk can require stricter gates. Live money, public deletion, identity, medical, security, and irreversible actions may require additional human or regulatory approval even at V4.

## Conservative Resolution

When several claims compose one decision:

- required `RED` claim → overall `RED`
- required `BLOCKED` claim → overall `BLOCKED` or `YELLOW`
- optional `YELLOW` claim → disclose limitation
- overall V2V level cannot exceed the weakest required claim

Never average away a critical failure.
