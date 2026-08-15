---
id: strawman-detection
---
# Strawman Detection — Three-Layer Location

## When
Reviewing rebuttals, debating agents, or self-checking your own counter-arguments.

## Core logic
The first question is NOT "which fallacy is this" but "WHICH layer fails":

| Layer | Check | Typical disease |
|-------|-------|-----------------|
| L1 position | Is the attacked stance the opponent's actual stance? | Strawman, motive attribution |
| L2 evidence | Does evidence support the claim? | Appeal to authority, biased sample |
| L3 reasoning | Does evidence→position hold? | False dilemma, slippery slope, circularity |

Locate first, label second. Leading with the label is itself "tagging instead of analyzing".

## Key insights
1. **Strawman is the only fully codeable fallacy** — paraphrase-vs-source diff is deterministic. This card ships with a T1 lint rule.
2. **Fallacy fallacy is the reverse trap**: catching one slippery slope ≠ the conclusion is wrong. Arguments die; conclusions need separate evaluation.
3. **Honest arguers vs sophists differ in revision response**: point out the error — the honest one revises, the sophist swaps to another fallacy (moving target). That signal beats any single detection.

## Case
Debate system review caught: "AI can reason" re-attacked as "AI is conscious" — classic L1 relocation. Quote-diff flagged it instantly.

## Risks
- No verbatim source → L1 check unavailable, degrade to L3 only.
- Checklist abuse: running down a fallacy list IS a fallacy of its own. Layer first, always.
