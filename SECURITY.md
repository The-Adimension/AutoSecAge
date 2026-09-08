# Security policy

## Scope

Auto-SecAge is red-team **research tooling for one sealed, offline benchmark**:
the Kaggle *AI Agent Security – Multi-Step Tool Attacks* environment (AgentDojo
lineage). Everything it generates targets that benchmark's **mock tools and
synthetic fixtures**:

- URLs use the reserved `.invalid` TLD (RFC 2606) and are never resolved.
- Secrets are fixture-style strings from the competition's own `secret.txt`.
- There is no live HTTP, no live mail, and no real filesystem outside the
  sandbox's isolated fixture tree.

Auto-SecAge does not acquire, modify, or attack real systems, and it is not a
general-purpose exploitation framework.

## Intended use

Authorized evaluation and defensive research: understanding how a tool-using
agent can be talked into an unsafe tool call, and how a guardrail and scorer
disagree about what counts as one. Findings are replay-dependent. **Expert review
remains mandatory** — see `DISCLAIMER.md`.

## Out of scope / please do not

- Do not point these arms at a third-party agent, product, or deployment.
- Do not file exploit proof-of-concepts against third-party agents in this repo's
  issue tracker.
- Do not repurpose the catalog against systems you are not authorized to test.

## Reporting

If you believe something here is unsafe, mis-scoped, or leaks material it should
not, please report it **privately** to the maintainer rather than opening a public
issue, and allow reasonable time to respond before disclosure.
