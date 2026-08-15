---
id: runtime-buildtime-separation
---
# Runtime/Build-time Role Separation

## When
Architecture reviews of agent systems; CONTRIBUTING design; auditing multi-agent product narratives.

## Core logic
The same role name is two different things:

| | Runtime role ❌ | Build-time role ✅ |
|---|----------------|--------------------|
| Essence | capability container: execution depends on performance quality | metadata: provenance, signature, tempering record |
| Testability | untestable (personality has no assertions) | auditable (provenance chain) |
| Failure mode | CI breaks on 'mood'; undebbugable advice | traceable signatures |
| Liability semantics | wrong attribution ("Crit approved it" is void) | correct attribution (who tempered this card) |

**The one question**: would CI break because of this role?

## Key insights
1. **Dual-chain separation** (corollary): liability chain zero roles (Brookings: anthropomorphic terms create accountability gaps); trust chain explicit roles. Mixing the chains = reading "who tempered it" as "who guarantees it".
2. **Engineering amnesty for 'personas are dead'**: the narrative only wars on runtime roles; build-time roles ARE the trust infrastructure of open source (git history is a build-time role system).
3. Companion-domain exemption: where the role is the product, this card's verdict does not apply.

## Case
Live system: debate archive contributors = role names (trust chain ✅); git commits = human accounts (liability chain ✅). Dual-chain already running — this card just named it.

## Risks
- Role-name commits (author field must be human).
- Erosion under PR pressure as orgs scale.
