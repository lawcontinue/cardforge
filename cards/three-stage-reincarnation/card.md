---
id: three-stage-reincarnation
---
# Three-Stage Reincarnation of Roles

## When
Designing multi-agent systems, product narratives announcing "de-roleing", or organizations moving role-based → skills-based.

## Core logic
"Personas are dead" precisely means: **runtime entity-hood dies**. Roles reincarnate in three places:

| Destination | Form | Function |
|-------------|------|----------|
| Build-time · provenance | card signatures, source fields | credibility signal ("tempered in N real debates") |
| Relational layer · warmth | blameable, trustable emotional interface | user vent & stickiness |
| Interface layer · blind spots | role-card self-declared limitations | trust-routing metadata |

Punchline: **no roles at runtime, provenance at build, warmth in relations, blind spots at the interface.**

## Key insights
1. **Provenance dissolves the self-reference paradox**: "selling method cards signed by roles" is only contradictory if signatures are runtime capability claims. Signatures as build metadata → decoupled.
2. **Emotional venting is a system requirement**: users need someone to grumble at. Keep the grumble target in the relational layer; keep failure liability in code+rules. CI never breaks because a role is moody; users may still curse the role.
3. **Structural isomorphism with skills-based orgs**: skills organize the work (methods reign inside), roles retain accountability (roles interface outside) — same structure, two domains.

## Case
This very repository: every card carries role signatures (provenance), the debate system's grumble-target survives in docs, commits carry human authors only.

## Risks
- Unfalsifiable as prediction — design principle only.
- Reincarnation must not leak back into the dependency graph.
