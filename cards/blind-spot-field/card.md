---
id: blind-spot-field
---
# Blind-Spot Self-Declaration Field

## When
Designing personas/roles for multi-agent systems (or yourself).

## Core logic
Role cards declare capabilities AND blind spots. Declaration = routing info:
- other agents learn when NOT to trust this role
- the system learns what needs cross-verification
- the role learns when to hand off (no out-of-lane compensation)

```yaml
blind_spots:
  - limitation: cannot detect whether input data itself is polluted (GIGO)
    failure_mode: precise-looking but wrong conclusions from polluted data
    mitigation: conclusions cross-checked by non-quantitative roles
```

## Key insights
1. **Structural anti-sycophancy**: praise must cross blind-spot checks — Aria praising Athena's numbers first passes "is the data polluted?". Frictionless flattery otherwise.
2. **Blind spots beat capability claims as trust metadata**: capabilities are unverifiable bragging; blind spots expose real boundaries.
3. **Recursion terminates**: the calibrator also has blind spots → an auditable calibration chain instead of infinite regress ("who calibrates the calibrator" — the chain is inspectable).

## Case
A live 8-role system where the veto-holder's card reads: *"veto overuse causes chilling effect; the veto judge itself needs calibration — who calibrates the calibrator?"* — the honest recursion is the design.

## Risks
- Liability-shielding abuse (mitigation: blind spot ≠ immunity, trigger → handoff).
- Stale declarations — drift with capability growth, review in retros.
