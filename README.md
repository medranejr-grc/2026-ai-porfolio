# Michael E. Drane Jr. — Agent Governance & Security Engineering

I build autonomous agents, and I build the controls that keep them from acting past their
mandate — a published governance framework, two production compliance agents, and the same
discipline showing up everywhere else I've built.

**Scope:** agentic AI × security governance
**Stack:** Claude Code, Cursor, Google ADK/Vertex, GPT-5.x, Python

---

## Governance architecture — The Lacey Framework

Constitutional governance for AI agents: define the mission, the people it serves, and the
human-authority boundary *before* defining what the agent is allowed to do.

Public since August 2026 and actively maintained. The framework's execution layer proposes a
three-plane architecture — control, execution, and evidence — covering signed agent identity
manifests, session authorization, policy decision and enforcement points, credential brokering,
and integrity-protected audit evidence. Every stage is marked honestly as proposed or built;
nothing is claimed as production-hardened that isn't. Related ideas were submitted as a
personal-capacity public comment to NIST, March 2026.

> Authority may remain the same or narrow at a transition. It may not broaden.
>
> — the authority invariant, from the framework's Controlled Delegation Continuity Test: a
> falsifiable protocol for whether a mission and its human-authority boundary survive an
> agent-to-agent handoff under drift pressure.

**[github.com/medranejr-grc/lacey-framework](https://github.com/medranejr-grc/lacey-framework)**
— public, CC BY-SA 4.0 (essays) / CC0 (templates and examples).

---

## Production systems — GRC automation

Two internal builds, described at architecture level only, with the incident that shaped each
design decision.

### SOC 2 / Vendor Risk Reviewer — *in production*

Replaces a multi-hour manual read of a third-party audit report against an internal control
baseline. An 8-stage pipeline on Google's Agent Development Kit, deployed on Vertex — intake,
extraction, evidence read, control mapping, risk synthesis, a deterministic scoring engine, then
report. A human triggers every run; nothing is autonomous end to end. The rating itself is
assigned by a rules engine, never a model self-report, and every extracted quote is verified as
a literal substring of the source document before a scope claim is accepted.

**The incident that shaped it.** A silent ingestion bug once dropped the uploaded evidence
entirely — the model filled the gap with a plausible answer drawn from general knowledge,
undetected for roughly two weeks because every visible signal looked normal. That near-miss
produced the current design: hard content-length checks, explicit "the evidence doesn't cover
this" instructions, forced neutral defaults, and moving the hardest judgment calls out of the
prompt into deterministic code.

Outcome: a multi-hour manual review → single-digit minutes of machine drafting, plus a shorter
human pass.

### Security Questionnaire Drafting Engine — *proof of concept, paused*

Drafts sourced answers to customer security questionnaires across dozens of spreadsheet layouts.
A thin managed-agent shell over a deterministic Python pipeline — a source-authority waterfall
checks the highest-authority evidence first and stops as soon as it's confident. The model
composes wording over evidence the code has already selected and validated; it never chooses the
evidence. Every sourced sentence carries a code-attached citation, and confidence is a small set
of code-assigned categorical bands, never a numeric self-report.

**The incident that shaped it.** The worst bug found: an early version could affirm a
negatively-phrased question even when the retrieved evidence supported "no." Negation handling
is now hardcoded and applied uniformly, defaulting to "needs review" on any ambiguity rather
than guessing.

**Guardrail worth naming.** Retrieved content is always passed to the model as inert data, never
instructions — resistance to text injected inside a customer's own questionnaire. A
data-promotion check auto-blocks unlisted organization-shaped name patterns, and it once caught
a real third-party name leaking into an upstream file before use.

Paused as a standalone build in favor of evaluating a purchased tool — still runs narrowly as an
independent scoring check on that tool's output.

---

## Applied elsewhere — same controls, different domain

The same instincts — hard spend caps, non-negotiable human gates, verification before each
irreversible step — recur in systems built for entirely different purposes.

| System | Control pattern | Status |
|---|---|---|
| Media production pipeline | Hard spend caps across three cost centers (observe / warn / hardcap modes) · mandatory human approval gates with **no dollar-threshold bypass** · automated technical QC fired at each gate, not just at the end | Active · 122 modules |
| Six-agent commerce flywheel | Discovery → build → deploy → ads → feedback, on a scheduled cron trigger, with one deliberate human approval gate before any spend commits | Active · scheduled |
| Companion app (private, third party) | A constitutional operating instruction plus a hard architectural constraint — conversation history handled server-side only, never client-exposed | Production |
| Claude Code skill authoring | Eleven authored skills, composed — one skill invokes another as its own verification step inside a gated pipeline | Nine live |

**Real code, not just descriptions of it** — both systems above have live production repos that
stay private (competitive product-discovery method, client work, business strategy). What's safe
to actually read is broken out here:

- **[`samples/phantom/`](samples/phantom/)** — three unmodified files from the media pipeline's
  guardrail layer: spend caps with three-mode enforcement, automated technical QC, automated
  visual-layout QC.
- **[`samples/veldt-digital/`](samples/veldt-digital/)** — the six-agent flywheel's real GitHub
  Actions orchestration (scheduling, error paths, notification logic) — not the agent logic
  itself, which is the working part of a live business.

---

## Case study — governance response to a rogue procurement agent

**[Read the full deliverable →](case-study-capstone.md)** — the real capstone document in full,
not a summary, with only the co-authors' names withheld.

Capstone, Security Architect program, March 2026. A three-person team was given one incident
scenario and asked to produce a full cross-domain response, one member per domain. I led the Risk
& Governance deliverable and was its primary author — GRC went first, and our remediation
requirements set the constraints the other four domains built their technical controls against.

The scenario: a fictional company's autonomous procurement agent placed and confirmed a $12M
purchase order with zero human review, after ingesting fabricated news content and treating it
as fact — authenticating through a hidden, high-privilege service account nobody knew existed.

**Five root failures:**

1. No formal AI governance structure — no policy, no lifecycle, no accountability
2. No financial transaction controls — unlimited spending authority, no threshold
3. No segregation of duties — the same process initiated the order and confirmed it
4. No behavioral monitoring — no baselines, no alerts, no escalation path
5. No pre-deployment risk classification — deployed to production with no impact assessment

The response mapped each failure to a specific control clause — NIST AI RMF, ISO/IEC 42001, SOC 2
CC6.1, EU AI Act Article 14 — and proposed a Policy Decision Point / Policy Enforcement Point pair
mediating every agent transaction, routing anything above $10,000 to mandatory human review. It
defined 23 bidirectional integration points across five security domains: a literal data-flow
contract for what governance hands each domain and what it hands back, so oversight doesn't rot
into a document nobody's systems actually feed.

**18-month roadmap:**

| Phase | Window | Focus |
|---|---|---|
| Stop the bleeding | Mo. 1–6 | Suspend the agent, define the $10K human-approval gate, audit for unmanaged service accounts |
| Build the foundation | Mo. 7–12 | Formal AI management system, cross-domain telemetry, segregation of duties enforced in code |
| Certify and mature | Mo. 13–18 | ISO/IEC 42001 certification, adversarial testing of the agent's own guardrails, board-level reporting |

---

Same thesis running through all four: govern what an agent *is*, with a human boundary that can
narrow but never broaden, before trusting what it does. Built and verified across two commodity
harnesses (Claude Code, Cursor) and one managed-agent platform (Vertex/ADK) — near-frontier
models throughout.

*[ contact — pending ]*
