---
id: decision-three-questions
---
# Progressive Decision Three-Questions

## When
Any decision — file edit to architecture bet. Humans and agents alike.

## Core logic
Review depth must match irreversibility:

| Grade | Criteria (most conservative axis wins) | Required |
|-------|----------------------------------------|----------|
| Simple (<30min, reversible) | low risk single op | Q1 |
| Medium (30min-2h, partial) | bugfix, feature, external interaction | Q1+Q2 |
| Major (>2h / irreversible / P0) | tech choice, architecture, public release | Q1+Q2+Q3 |

- **Q1 baseline**: ≥1 verifiable number/file/source. "Feels right" fails. All estimates carry ±30%.
- **Q2 worst-3**: specific scenarios + trigger conditions. Can't name 3 = either haven't thought, or genuinely low-risk — distinguish which.
- **Q3 opposition**: ≥1 concrete objector + reasoning. No objector = blind spot until you role-play one.

## Key insights
1. **Order is not swappable**: without Q1, Q2 risk-listing follows your desired conclusion.
2. **Q3 is a meta-check on Q1/Q2**: objector perspectives expose biased data sources and missed risk surfaces — Q3 output often rewrites Q1/Q2.
3. Ships as **decision gates**: `no-baseline` and `missing-opposition` lint rules.

## Case
Open-sourcing decision (2026-08-15): live-checked ecosystem data first (2 awesome lists, all-capability plugins, preview-stage API), three worst outcomes (API churn / zero-demand / focus dilution), three named objectors → output: staged plan with timebox instead of all-in.

## Risks
- Q1 as deferral tactic (bind a deadline).
- Don't bureaucratize trivial decisions.
