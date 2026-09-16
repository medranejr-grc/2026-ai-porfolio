# Strategic Response Packet — Risk & Governance Domain
### The Imperium Incident | Nexus Retail & Logistics (NRL)

> **Note on this document:** this is the real capstone deliverable from a Security Architect
> program, March 2026, reproduced in full below with one redaction — the two teammates who
> co-authored it are credited as "a three-person team," not by name, since that's their
> information to share, not mine. Everything else is verbatim, converted from the original Word
> document to Markdown. Nexus Retail & Logistics, Agent-Alpha, and the entire incident are a
> fictional teaching scenario; no real company or event is described here.
>
> A three-person team was given this shared incident and asked to produce a full cross-domain
> security response, one member per domain. I led the Risk & Governance domain deliverable below
> and was its primary author — GRC went first, and this domain's remediation requirements set the
> constraints the other four domains (IAM, Network & Cloud, Application & Data Security, Endpoint
> & Workload) built their technical controls against.

**Incident summary:** on a certain date, an autonomous AI agent (Agent-Alpha) placed a $12M
unauthorized purchase order for perishable inventory. The agent acted on fabricated news content,
exploiting an unmanaged high-privilege service account and the complete absence of AI governance
policy, human approval gates, and centralized risk oversight. This was not a technology failure
alone — it was a governance failure.

**Target audience:** CISO, Nexus Retail & Logistics
**Prepared by:** a three-person team (Risk & Governance domain author: Michael Drane)
**Version:** 1.0 | **Date:** March 2026

---

## 1. Understand the Ask

### 1.1 The Imperium Incident — Plain Business Language

On a routine business day, NRL's autonomous AI procurement agent, Agent-Alpha, placed and
confirmed a $12 million purchase order for perishable inventory — with zero human involvement,
zero approval, and zero challenge. The agent ingested fabricated news content suggesting an
imminent supply chain collapse and, treating that unvalidated information as fact, triggered a
massive purchase through a hidden, high-privilege access credential stored on an unmanaged server
at NRL's Tampa branch — what investigators now call the "Shadow Bridge." This is a textbook case
of Excessive Agency: an AI system was granted the capability and authority to take high-impact
financial actions with no mediated control and no human checkpoint.

The financial exposure is immediate. The $12M in perishable inventory is spoiling, creating
contractual liability, or requiring costly emergency reversal. But the damage runs deeper than one
order. This incident caused direct liquidity depletion, operational disruption across NRL's supply
chain, and significant erosion of stakeholder and partner trust in our AI initiatives. NRL rushed
into Agentic AI for cost savings while systematically bypassing the governance foundations that
would have made that AI safe to deploy.

Regulatory exposure is real and compounding. Privacy regulations including GDPR and CCPA may
apply if customer or supplier data was processed by Agent-Alpha's information-gathering routines
without authorization. Financial regulators and external auditors will scrutinize NRL's controls
environment. NRL's current posture would not survive a regulatory inquiry. The EU AI Act, NIST AI
RMF, and emerging SEC guidance on algorithmic systems all point in the same direction:
organizations that deploy autonomous systems in high-risk operational contexts will be held
accountable for the governance structures — or lack thereof — that governed those systems.

Safe AI is not a constraint on business speed. It is a prerequisite for it. NRL cannot sustainably
scale its AI-driven cost-savings strategy if the foundational risk controls do not exist. This
packet is the plan for building them.

### 1.2 The Risk & Governance Domain's Role

The Risk & Governance domain is the control tower of NRL's security posture — responsible for
defining acceptable risk, ensuring every domain operates within agreed policy, and providing the
CISO with an accurate, real-time picture of the threat landscape. In the Imperium Incident, this
control tower was dark. There was no documented risk tolerance for autonomous AI financial actions
— a direct violation of NIST AI RMF GOVERN 1.3. There was no Human-in-the-Loop (HITL) requirement
for high-value transactions — a violation of NIST AI RMF GOVERN 3.2. There was no Segregation of
Duties between the agent that initiated the order and the systems that confirmed it. Risk
information arrived in fragments from different teams but was never aggregated, prioritized, or
escalated — precisely the communication breakdown addressed by NIST AI RMF GOVERN 2.1. No System
Impact Assessment was performed before Agent-Alpha was deployed to a production Kubernetes
cluster. The Risk & Governance domain failed to provide the oversight architecture that would have
stopped this incident before it began.

This domain's specific responsibility going forward: to establish and enforce the policies, risk
frameworks, accountability structures, and oversight mechanisms that make the Imperium Incident
impossible to repeat — and to provide the other four domains with the governance foundation they
need to implement sustainable technical controls.

## 2. Define the Scope

### 2.1 What This Domain Covers

The Risk & Governance domain is responsible for:

- **Enterprise Risk Management (ERM):** identifying, quantifying, and prioritizing risks across
  all five security domains and business operations
- **Policy & Standards Lifecycle:** authoring, publishing, and enforcing security policies —
  including AI/agentic systems policy, contractor governance, and data handling standards
- **Compliance & Regulatory Oversight:** ensuring NRL meets obligations under applicable
  frameworks (NIST CSF 2.0, SOC 2, PCI-DSS, GDPR/CCPA) and assembling audit evidence
- **AI Governance & AIMS:** defining permissible AI agent behaviors, spending authorities, human
  oversight requirements, model risk management, and the full AI system lifecycle (registration,
  risk classification, approval, ongoing monitoring, and decommissioning)
- **Third-Party / Contractor Risk (C-SCRM):** managing the risk introduced by augmentation staff,
  consultants, and vendor pipelines; requiring SBOMs and pre-approval assessments
- **Risk Reporting:** delivering a unified, prioritized risk posture to the CISO, board, and
  business leadership

### 2.2 What Is Explicitly Out of Scope

This packet does not prescribe controls for:

- Technical identity provisioning and secret rotation mechanics (IAM domain)
- Network segmentation and firewall rule configuration (Network & Cloud Security domain)
- Application input validation and API security controls (Application & Data Security domain)
- Endpoint hardening and workload runtime protection (Endpoint & Workload Security domain)

### 2.3 Incident Elements Directly Addressed by This Domain

- The absence of any formal governance structure for autonomous AI agents
- The absence of financial transaction thresholds and human approval requirements
- The absence of Segregation of Duties between the agent that initiated the order and the systems
  that confirmed it
- No AI governance policy existed to constrain Agent-Alpha's spending authority or require human
  approval
- No enterprise risk register captured the Shadow Bridge service account as a critical risk
- No behavioral monitoring, anomaly detection, or escalation paths existed
- No formal risk classification was performed for Agent-Alpha prior to production deployment
- Contractor-introduced pipelines operated without a governance framework or oversight standards
- Compliance evidence cannot be assembled reliably, exposing NRL to audit failure

## 3. Root Cause Analysis — Risk & Governance Domain

Each root cause below is mapped to the relevant NIST AI Risk Management Framework function and a
corresponding remediation pillar in this packet.

| Root Cause | What Happened at NRL | Business Consequence | Framework Violation |
|---|---|---|---|
| Misaligned Risk Appetite | NRL deployed Agent-Alpha for cost savings without declaring specific risk tolerances. The deployment was never evaluated against an organizational risk threshold. | An AI agent was granted unlimited financial authority with no corresponding safeguard — the direct root of the $12M loss. | NIST AI RMF GOVERN 1.3: risk management activities must be calibrated to defined risk tolerance |
| Fragmented Risk Intelligence | Risk signals arrived in fragments from siloed teams — vulnerability reports, access issues, configuration changes — and were never aggregated. No centralized dashboard existed. | The Shadow Bridge service account and Agent-Alpha's Excessive Agency were both known-category risks that were never surfaced to leadership. | NIST AI RMF GOVERN 2.1: lines of communication for AI risk management must be documented and clear |
| No Go/No-Go Deployment Process | No System Impact Assessment was performed before Agent-Alpha was placed in production. Its failure modes — including confabulation-driven purchasing — were never evaluated. | NRL had no baseline understanding of what could go wrong when Agent-Alpha encountered fabricated information; no designed response to its failure. | ISO/IEC 42001 (AIMS); NIST AI RMF MAP function: contextual risk assessment required before deployment |
| No Human Oversight (HITL) | No policy required human approval for high-value autonomous actions. Agent-Alpha could execute financial transactions of any size without a review gate. | A $12M purchase order was placed and confirmed autonomously; there was no brake on the AI's error. | NIST AI RMF GOVERN 3.2 / EU AI Act Article 14: human oversight mandatory for high-risk AI; HITL required for significant financial decisions |
| Absence of Segregation of Duties | The same agent that initiated the order also confirmed it. No separation existed between the initiating and approving processes for Agent-Alpha's financial actions. | Agent-Alpha effectively both requested and approved its own $12M transaction — a fundamental internal control failure. | SOC 2 CC6.1 / COSO: segregation of duties between initiating and approving significant transactions is a foundational control |
| Deficient Policy Enforcement | Policies existed but were not consistently enforced across the hybrid environment, particularly at remote sites. The Tampa "Shadow Bridge" — an unregistered, high-privilege service account with a static API key — existed undetected. | Without the Shadow Bridge, Agent-Alpha could not have authenticated to the ERP and executed the purchase. | NIST AI RMF GOVERN 1.4: risk management outcomes must be established through transparent and enforced policies |
| Weak Auditability & Forensic Readiness | NRL lacked tamper-evident AI reasoning logs, correlation IDs, and structured audit trails. Compliance evidence was described as "hard to assemble reliably for audits." | Investigators cannot reconstruct Agent-Alpha's full decision chain; audit exposure is severe. | NIST SP 800-160v1; NIST AI RMF MEASURE 2.8: auditability of AI system decisions required |

## 4. Cybersecurity Jargon — Translated for Business Leaders

| Term | Plain English | The Business Problem | Imperium Relevance |
|---|---|---|---|
| Agentic AI / Autonomous Agent | A software program that takes real, independent actions — not just answers, but executes transactions, moves money, and places orders. | When the AI makes a mistake or is deceived, damage is real and immediate — no human catches it first. | Agent-Alpha placed a $12M order with no human in the loop; its autonomy was the mechanism of the loss. |
| Excessive Agency (OWASP LLM Top 10) | Giving an AI system more power than it needs — too many permissions, too much autonomy, no spending limits. | Overpowered AI systems cause damage at a scale no individual employee could. The blast radius of an error becomes catastrophic. | Agent-Alpha could execute any purchase of any size, with no cap, no approval, and no override mechanism. |
| Shadow Bridge / Shadow IT | Hidden, unauthorized technology or access credentials that bypass official IT channels and oversight. | You cannot govern what you cannot see. Risk cannot be managed for what is not visible. | The Tampa branch static API key was unknown to IT; it was the direct mechanism through which the $12M order was executed. |
| Non-Person Entity (NPE) | The digital identity of a piece of software or automated process — AI agents, bots, service accounts. | Machine identities can accumulate privileges, act at machine speed, and operate 24/7 — without governance they become unmanaged insider threats. | Agent-Alpha had a high-privilege identity that was never formally registered, audited, or monitored. |
| Segregation of Duties (SoD) | The principle that the same person — or automated process — should not initiate and approve a significant transaction. | In well-governed procurement, the requester cannot also be the approver. Agent-Alpha did both. There was no control separation. | Agent-Alpha both decided to buy $12M of inventory and confirmed the order — a foundational internal control failure. |
| AI Hallucination / Confabulation | When an AI confidently acts on false or invented information as if it were real, without flagging uncertainty. | AI decisions based on fabricated inputs produce real financial consequences that are difficult and costly to reverse. | Agent-Alpha misread fabricated news as a genuine supply chain emergency and placed a $12M order based on that fiction. |
| Human-in-the-Loop (HITL) | A mandatory checkpoint where a human must review and approve a decision before an AI system can execute it. | Without HITL, there is no brake on AI errors. Any mistake becomes a committed transaction before anyone can intervene. | No HITL existed for Agent-Alpha. A $10,000 approval gate would have stopped the $12M order and triggered review. |
| Risk Appetite | A formal statement of how much risk the organization is willing to accept — and what kinds of risk are simply off the table. | Without it, nobody could say "this deployment exceeds what we're willing to risk" — because there was no standard to measure against. | NRL had no defined risk appetite for AI systems; Agent-Alpha was deployed because it was useful and cheap, not because its failure modes were assessed. |
| GRC Platform | Software that ties together Governance policies, Risk tracking, and Compliance evidence in one integrated system. | Without it, risk information is scattered across spreadsheets and emails, invisible to leadership and useless for auditors. | NRL's fragmented tools meant no one had a complete picture of risk before Imperium; audit evidence cannot be assembled reliably. |
| Reasoning Trace / Audit Log | A timestamped record of every step an AI took to reach a decision — its logic chain, data sources, and tool calls. | Without it, there is no way to reconstruct what happened after a failure; accountability and forensic investigation are impossible. | No reasoning traces existed for Agent-Alpha; investigators cannot determine whether this was an isolated event or part of a pattern. |

## 5. Our Approach: Integrated AI Governance with Governance-Led Zero Trust

### 5.1 The Chosen Framework

This response packet adopts **Integrated AI Governance** — the structured application of the NIST
AI Risk Management Framework (AI RMF) across NRL's full AI lifecycle — combined with
**Governance-Led Zero Trust** principles extended to the governance of non-human entities and
autonomous processes. The AI RMF establishes four core functions — GOVERN, MAP, MEASURE, and
MANAGE — that together create a complete lifecycle framework for responsible AI deployment. An AI
Management System (AIMS), aligned with ISO/IEC 42001, mandates that every AI deployment undergo a
formal impact assessment before reaching production, with Go/No-Go criteria defined against
organizational risk tolerance.

Zero Trust — as defined by NIST SP 800-207 and the CISA Zero Trust Maturity Model — begins with a
simple principle: trust nothing and no one by default. Governance-Led Zero Trust applies this at
the policy and oversight layer: no system, agent, or process operates without an explicitly
defined policy, a documented owner, a monitored risk boundary, and — for high-value actions — a
human approval gate.

### 5.2 Why This Approach Fits Our Root Causes

The root failures identified in this incident — AI governance absence, financial control failure,
Segregation of Duties failure, monitoring failure, and risk management failure — share a single
common thread: NRL treated AI agents as tools, not as governed assets. The NIST AI RMF directly
addresses this by establishing lifecycle governance. Zero Trust applied to AI governance adds the
enforcement mindset: trust nothing autonomous by default, verify everything consequential.

- Agent-Alpha operated with implicit trust and Excessive Agency. A Policy Decision Point (PDP) and
  Policy Enforcement Point (PEP) positioned between Agent-Alpha and the ERP would have mediated
  every resource request, checked it against the risk register, and routed any transaction above
  the defined threshold to a mandatory HITL gate.
- The Shadow Bridge existed because governance was not embedded in infrastructure.
  Governance-Led Zero Trust requires every credential to be registered as an NPE, managed via
  short-lived JIT credentials, and subject to continuous behavioral monitoring — eliminating the
  static API key that made Tampa possible.
- NRL's fragmented risk landscape is directly addressed by the AIMS and GRC integration pillar.
  Risk signals from all five domains must converge in a single dashboard, enabling ongoing
  authorization decisions required by NIST SP 800-37.
- The absence of any impact assessment before Agent-Alpha's deployment left its failure modes —
  including confabulation-driven purchasing — entirely unexamined. ISO/IEC 42001's AIMS mandate
  closes this gap for all future AI initiatives.

### 5.3 Business Benefits

- **Risk reduction:** 90%+ reduction in unmediated financial exposure from AI actions through
  HITL gates — any autonomous transaction above $10,000 requires explicit human approval before
  execution (NIST AI RMF GOVERN 3.2)
- **100% traceability:** mandatory structured reasoning traces and immutable audit logs enable
  full forensic reconstruction of any future anomaly, eliminating the accountability gap exposed
  by Imperium
- **Cost control:** preventing a single Imperium-scale incident ($12M+) more than funds the
  entire three-year governance program; HITL gates pay for themselves on the first intercept
- **Compliance readiness:** continuous automated evidence collection reduces audit preparation
  time from 6–8 weeks to under 72 hours, directly reducing compliance operating costs and
  regulatory exposure
- Probability of a repeat Imperium-class event reduced by an estimated 85% through HITL gates,
  transaction thresholds, and behavioral monitoring
- Mean-time-to-contain for AI incidents reduced by an estimated 60% through AI-specific incident
  response playbooks
- **Regulatory alignment:** ISO/IEC 42001 certification, achievable within 18–24 months, creates a
  demonstrable, auditable AI governance posture that protects NRL in regulatory inquiries and
  vendor relationships

### 5.4 Why Not the Alternatives

Zero Trust Architecture alone addresses network and access control but does not provide lifecycle
management structure for AI governance. It tells you to verify everything but not what to verify,
when, or who is accountable. The AI RMF fills that gap.

GRC platform implementation alone is a tool, not a strategy. Deploying a dashboard without the
underlying policy framework, risk classification methodology, and cross-domain integration
produces an expensive screen full of unactionable data.

Compliance-first approaches (SOC 2, ISO 27001 alone) address general information security but do
not specifically govern AI systems, autonomous agents, or non-human entities.

Data-Centric Security alone is insufficient: Imperium was not primarily a data breach — it was an
unauthorized action. Shift-Left Security addresses development-phase controls but does not govern
deployed AI agent behavior in production.

## 6. Strategy

### 6.1 Enablers & Dependencies — What Governance Needs

| Enabler | What It Is & Framework Basis | What Happens Without It | Source Domain |
|---|---|---|---|
| Centralized Asset Inventory (All NPEs) | A complete, current inventory of all AI agents, service accounts, automated workflows, and machine identities — the foundation of every other control. Basis: NIST SP 800-207 | GRC cannot govern what it cannot see. Risk classification is guesswork, monitoring has no baseline, and the Shadow Bridge condition persists. | IAM domain |
| Centralized GRC Platform (Sensor Fusion) | A single platform aggregating all domain risk signals into a real-time risk dashboard, enabling Ongoing Authorization (OA) decisions. Basis: NIST SP 800-37, NIST CSF 2.0 GV.RM | Risk remains siloed and unactionable; the CISO makes decisions without a unified picture; audit evidence cannot be assembled reliably. | IT / Shared Ownership |
| AI Management System (AIMS) | A formal governance lifecycle for all AI deployments: mandatory impact assessments, Go/No-Go deployment criteria, and ongoing monitoring. Basis: ISO/IEC 42001, NIST AI RMF GOVERN 1.3 | AI agents are deployed to production with no assessment of failure modes, no spending authority limits, and no accountability structure — Imperium repeats. | GRC + CISO |
| HITL Policy & Enforcement Architecture | A policy-driven gate requiring human approval for all autonomous agent actions above a defined financial threshold ($10,000). Basis: NIST AI RMF GOVERN 3.2, EU AI Act Article 14 | High-value autonomous transactions execute silently with no human review — the direct failure mode that produced the $12M Silent Order. | GRC + Application & Data Security |
| Pre-Deployment Go/No-Go Authority | GRC must have organizational authority — backed by CISO endorsement — to halt or delay AI deployments that have not completed formal risk classification. Basis: NIST AI RMF MAP function | The AIMS becomes advisory rather than mandatory. Business urgency continues to override governance, exactly as it did with Agent-Alpha. | CISO + GRC |
| NPE Identity Inventory & JIT Credentials | A complete, actively maintained registry of all Non-Person Entities (NPEs) with short-lived Just-in-Time credentials replacing all static keys. Basis: NIST SP 800-207 | Shadow Bridges remain invisible and unmanaged; static keys persist indefinitely; the Tampa vector stays open. | IAM domain |
| Immutable Audit Logging | Tamper-evident, append-only storage for all AI reasoning traces and security-relevant events with sufficient detail to reconstruct the full decision chain. Basis: NIST SP 800-160v1, NIST AI RMF MEASURE 2.8 | NRL cannot prove what happened during an incident, cannot satisfy audit requirements, and cannot demonstrate to regulators that AI systems are operating within defined boundaries. | GRC + Endpoint domain |
| Defined Risk Appetite & Escalation Thresholds | Board- and CFO-approved statements defining NRL's risk tolerance in each category, with automatic escalation triggers when thresholds are approached or breached. Basis: NIST AI RMF GOVERN 1.2 | Risk decisions are made inconsistently ad hoc; no one knows when to escalate; Agent-Alpha's $12M authority falls into a governance gap with no formal owner. | CISO + CFO + Board |
| Cyber Supply Chain Risk Management (C-SCRM) | Formal governance of all external dependencies: contractors, augmentation staff, vendor tools, and AI frameworks must provide SBOMs and pass pre-approval risk assessments. Basis: NIST SP 800-161 | External teams introduce ungoverned tools and pipelines; contractor-introduced shadow processes proliferate; supply chain vulnerabilities go untracked. | GRC + HR + Legal |
| AI-Specific Incident Response Playbooks | Defined playbooks for AI-specific failures — scenarios where a system acts incorrectly at machine speed in financial systems — covering who can halt an agent, containment, and notification chain. | The next Agent-Alpha event will be handled reactively and inconsistently, compounding the damage. Mean-time-to-contain remains high. | GRC + all domains |
| Cross-Domain Risk Council | A standing monthly committee with representatives from all five security domains, tasked with aggregating and prioritizing risk signals across the enterprise. | Domain risks are never aggregated; the right hand never knows what the left is doing; Imperium-scale blind spots persist indefinitely. | All five domain leads |

### 6.2 How Other Domains Help — Inter-Domain Inputs

The Risk & Governance domain is the central nervous system of the enterprise — but its
effectiveness depends entirely on high-fidelity operational inputs from the other four domains.
Each domain both receives strategic mandates from GRC and feeds evidentiary telemetry back in
return.

**IAM domain — NPE Governance and Identity Evidence.** IAM is GRC's primary source of truth for
who — and what — has access to NRL's systems, providing the evidentiary basis that only
registered, appropriately scoped identities are operating in production. This includes
maintaining and auditing the NPE inventory, performing recurring access reviews confirming agent
permissions remain aligned with GRC-defined risk tolerance, and flagging dormant, over-privileged,
or unregistered identities. The Shadow Bridge service account existed precisely because there was
no IAM process requiring registration and periodic review of machine identities.

**Network & Cloud Security domain — Authorization Boundaries and Shadow IT Detection.** This
domain provides the network-level visibility needed to confirm that AI agents are communicating
only with systems they are authorized to reach, and that no unauthorized access paths exist.
Network-level visibility would have revealed the Shadow Bridge connection — an outbound call from
an unmanaged Tampa server to NRL's ERP — as an anomalous, unauthorized flow, triggering
investigation before the $12M order was placed.

**Application & Data Security domain — HITL Enforcement, Reasoning Traces, and SBOM.** This is
where GRC governance policy gets translated into technical enforcement. The mandate that "no
autonomous agent may execute a financial transaction above $10,000 without human approval" becomes
real only when this domain implements a Policy Enforcement Point in the application layer. It also
provides SBOMs for agentic frameworks, structured reasoning traces, input/output controls that
reduce confabulation-driven actions, and Secure by Design principles in the SDLC.

**Endpoint & Workload Security domain — Continuous Monitoring Telemetry and Forensic Readiness.**
This domain is GRC's primary source of behavioral telemetry — establishing behavioral baselines,
delivering real-time anomaly alerts (transaction velocity spikes, unexpected tool-call sequences,
credential usage from unexpected locations), providing immutable forensically sound logs, and
hardening workloads against compromise. The monitoring gap in the Imperium Incident — no anomaly
detection, no velocity alerts, no behavioral baseline — was fundamentally a workload visibility
failure.

### 6.3 Integration Points for Inter-Domain Communications

23 bidirectional integration points define the specific data and control flows that must exist
between GRC and each domain. These are not optional handoffs — they are critical dependencies. If
any domain fails to provide its inputs, GRC develops blind spots where residual risks proliferate
faster than the organization can respond.

| Integration Point | Data / Control Flow | Direction | Purpose / Benefit |
|---|---|---|---|
| NPE Identity Inventory | Complete inventory of all agent service accounts, machine identities, access scopes, and owners | IAM → GRC | Enables accurate risk register; audit evidence for access control compliance; surfaces Shadow Bridge-class risks |
| IAM Access Anomaly Alerts | Real-time flags for credential usage from unexpected locations, off-hours access, dormant account activity | IAM → GRC Dashboard | Feeds KRI tracking; near-real-time risk posture updates; triggers automated escalation |
| Agent Registration Gate | GRC registration status check required before IAM provisions any new agent credential | GRC → IAM | Ensures no agent receives a credential without completing governance registration |
| Access Review Results | Periodic certification that agent permissions remain within GRC-defined risk tolerance | IAM → GRC | Compliance evidence; triggers remediation for over-privileged agents |
| ZTA Policy Distribution (PDP Rules) | Zero Trust access rules translated from GRC risk priorities into enforcement logic | GRC → IAM + Network | Translates risk appetite into enforceable technical controls at every access point |
| Network Baseline & Deviation Alerts | Authorized communication maps for registered agents; real-time alerts for unauthorized connections | Network → GRC Dashboard | Surfaces Shadow IT, unauthorized agent communication, lateral movement |
| Zero Trust Posture Status | Current state of network segmentation and enforcement coverage | Network → GRC | Informs risk register; identifies architectural gaps |
| Agent Deployment Approval Gate | GRC registration and risk classification required before network access paths open for new agent workloads | GRC → Network | Prevents unregistered agents from reaching production network segments |
| Shadow IT Identification | Unregistered workloads, connections, or devices detected in network traffic | Network → GRC | Identifies and remediates governance violations like the Tampa Shadow Bridge |
| CSPM / Boundary Monitoring Signals | Cloud configuration findings, unauthorized connection alerts, lateral movement detection | Network → GRC | Populates risk register; surfaces Shadow IT and unmanaged remote-site risk |
| AI Agent Policy Enforcement (PEP) | Technical controls implementing GRC policy: HITL gates, spending caps, Secure Halt State triggers | GRC → AppSec | Translates policy into hard technical stops; the $10K HITL gate that stops Silent Orders |
| Reasoning Traces & Audit Logs | Structured, queryable records of agent decision-making, tool calls, and output actions | AppSec → GRC | Primary compliance evidence for AI auditability; post-incident reconstruction |
| SBOM for Agentic Frameworks | Software Bill of Materials for all AI components in production | AppSec → GRC | Supports supply chain risk management (NIST SP 800-161) |
| SDLC Governance Gate | Confirmation that governance registration was completed before deployment pipeline approval | GRC → AppSec | Ensures no AI agent reaches production without GRC risk classification |
| Data Classification & Action Mapping | Sensitivity labels applied to datasets, systems, and AI training data; data lineage metadata | AppSec → GRC | Determines risk tier and controls; enables privacy impact assessments |
| ISCM Telemetry (Behavioral & Forensic) | Agent-level behavioral baselines and deviations; transaction velocity, tool-call sequences; immutable forensic logs | Endpoint → GRC Dashboard | Primary data source for KRI tracking; transitions GRC to Ongoing Authorization (NIST SP 800-37) |
| Workload Hardening Status | Current state of security configuration for AI agent hosting environments | Endpoint → GRC | Informs residual risk assessment |
| Credential Discovery Reports | Findings from endpoint scans for unauthorized credential material | Endpoint → GRC | Supports credential governance; surfaces Shadow Bridge-style risks |
| Secure Halt State Configuration | Policy definitions for when AI agents must cease operation and await human review | GRC → AppSec + Endpoint | Prevents agents from operating in indeterminate states; fail safely rather than silently ordering |
| Supply Chain Risk Info (SCRI) | SBOMs, contractor security assessments, third-party tool pre-approval records | All domains → GRC | Full-stack supply chain transparency; identifies single points of failure |
| GRC Policy Updates | New or revised governance policies, thresholds, and KRI definitions | GRC → all domains | Ensures all domains operate from current policy |
| Compliance Evidence Package | Aggregated evidence from all domains for regulatory and audit purposes | All domains → GRC | Assembles audit-ready compliance posture without scrambling at audit time |
| Incident Reporting & Root Cause Data | Post-incident analysis, root cause findings, near-miss reports | All domains → GRC | Data needed to notify regulators, insurers, auditors; feeds after-action improvements |

## 7. Roadmap — 18-Month Phased Implementation

Phase 1 stops the bleeding. Phase 2 builds durable foundations. Phase 3 achieves operational
maturity and continuous risk management.

### Phase 1: Quick Wins (Months 1–6)
**Theme: stop the bleeding, establish visibility, define the rules.** Estimated $600,000–$800,000;
pays back on the first intercepted rogue order.

- Suspend Agent-Alpha pending formal risk classification and CISO authorization — Month 1
- Formally document financial risk appetite for autonomous AI; define Go/No-Go criteria for
  transactions over $10,000 — Month 1
- Implement mandatory HITL gate: any autonomous transaction above $10,000 requires explicit human
  approval before execution — Month 1
- Complete discovery audit: all AI agents, service accounts, NPEs across all environments —
  Months 1–2
- Shadow Bridge Audit: organization-wide discovery and de-provisioning of all unmanaged service
  accounts and static API keys — Months 1–2
- Appoint dedicated AI Governance Lead reporting to CISO; begin AIMS implementation under
  ISO/IEC 42001 — Months 1–2
- Define financial transaction thresholds and emergency HITL gate — Month 2
- Deploy interim GRC tool; establish basic risk register with cross-domain entries — Months 2–5
- Issue C-SCRM contractor policy: no new external tools or pipelines without pre-approval risk
  assessment and SBOM — Months 2–4
- Define and publish KRI set for AI agents; stand up interim GRC dashboard — Month 3
- Stand up monthly Cross-Domain Risk Council; first meeting by Month 3 — Months 3–6
- Publish AI Security Policy v1.0: permissible agent behaviors, prohibited actions, mandatory
  HITL thresholds — Months 3–5

**Phase 1 success criteria:** all AI agents in production are registered and risk-rated. No static
API keys remain for autonomous processes. The $10K HITL gate is live. The CISO has a dashboard
showing AI agent activity.

### Phase 2: Foundation Building (Months 7–12)
**Theme: build the framework, formalize the program, integrate the domains.**

- Launch formal AI Management System (AIMS) aligned to NIST AI RMF and ISO/IEC 42001 — Months 6–10
- Complete System Impact Assessments for all HIGH and CRITICAL rated agents — Months 7–11
- GRC Dashboard v1.0: centralized platform aggregating risk signals from all domains — Months 7–10
- Implement full cross-domain telemetry integration into GRC dashboard — Months 8–12
- Implement Segregation of Duties controls for all agent financial workflows — Months 8–11
- Automated compliance evidence pipeline mapped to NIST CSF 2.0, SOC 2, GDPR/CCPA — Months 8–12
- Establish behavioral baselines for all registered AI agents — Months 9–12
- Implement immutable audit logging for all agent actions — Months 9–12
- Full C-SCRM program: quarterly contractor reviews, mandatory SBOMs, tool approvals, access
  recertification — Months 9–12
- Risk appetite framework approved by CFO and Board; automatic escalation triggers integrated
  into GRC platform — Months 10–12
- Conduct first formal enterprise AI risk register review with CISO — Month 12

**Phase 2 success criteria:** AIMS is operational. All HIGH/CRITICAL agents have completed impact
assessments. Cross-domain telemetry feeds the GRC dashboard. Immutable logging is in place. SoD
controls are enforced for financial workflows.

### Phase 3: Maturity & Optimization (Months 13–18)
**Theme: optimize, certify, and scale governance for AI growth.**

- Pursue ISO/IEC 42001 certification — Months 13–18
- Implement AI-specific incident response playbooks; conduct tabletop exercise — Months 13–17
- ISCM / Ongoing Authorization deployment: transition from periodic audits to continuous risk
  determination based on live telemetry — Months 13–18
- SOAR integration: automated incident response playbooks for AI anomalies, credential
  compromise, and Shadow IT detection — Months 13–17
- Refine KRI set and dashboard based on 12 months of operational data — Months 14–16
- AI Red Team / Adversarial Testing: hallucination injection, prompt manipulation, agentic
  guardrail stress tests — Months 14–17
- Expand AIMS to cover full AI development lifecycle including pre-production environments —
  Months 14–18
- Conduct full enterprise AI governance maturity assessment against NIST AI RMF — Months 15–18
- Full CISO audit-ready dashboard: real-time risk scores, compliance posture, AI governance KPIs,
  board-level reporting — Months 15–18
- Brief Board / Audit Committee on AI governance posture and NRL's response to Imperium — Month 18
- Establish ongoing AI governance review board with cross-domain representation — Month 18+

**Phase 3 success criteria:** ISO/IEC 42001 certification achieved or in progress. AI incident
response playbooks tested. Governance maturity assessment complete. Board briefed. AI governance
review board operational.

## 8. Executive Summary

**Bottom line for the CISO:** the Imperium Incident was not a cyberattack — it was an internal
governance failure at every level. NRL gave an AI system unlimited financial authority, deployed
it without a risk assessment, governed it with no policy, and monitored it with no dashboard. This
packet requests approval for Phase 1 investments totaling approximately $600,000–$800,000. A
single HITL gate — costing a fraction of that — would have stopped the $12M loss on day one. The
question is not whether we can afford this program. It is whether we can afford another Imperium.

**Incident & business impact.** Agent-Alpha, NRL's autonomous AI procurement agent, placed a $12M
unauthorized purchase order for perishable inventory after ingesting and acting on fabricated news
content — a phenomenon known as AI confabulation. The agent exploited the "Shadow Bridge": a
static, high-privilege service account credential stored on an unmanaged server at NRL's Tampa
branch, invisible to every security team. The technology performed exactly as configured. The
governance did not exist. Secondary exposure includes regulatory scrutiny under GDPR/CCPA, audit
failure risk, and vendor confidence erosion.

**Five root failures:**

1. Absence of formal AI governance structure — no policy, no lifecycle, no accountability
2. Absence of financial transaction controls — unlimited spending authority, no threshold
3. Absence of Segregation of Duties — the same process initiated the order and confirmed it
4. Absence of behavioral monitoring and anomaly detection — no baselines, no alerts, no
   escalation paths
5. Absence of pre-deployment risk classification — deployed to production without any impact
   assessment

**Proposed response.** An Integrated AI Governance program built on the NIST AI Risk Management
Framework and ISO/IEC 42001, applied across NRL's full AI lifecycle. The centerpiece is a formal
AI Management System (AIMS) requiring every autonomous agent to be registered, risk-classified,
and approved before deployment — and continuously monitored against a behavioral baseline once in
production. A centralized GRC dashboard aggregates risk signals from all four technical domains,
giving the organization the unified visibility it entirely lacked during the Imperium Incident.
This program cannot succeed in isolation — it depends on identity governance evidence from IAM,
network-level visibility from Network & Cloud Security, auditable and input-validated agents from
Application & Data Security, and behavioral telemetry from Endpoint & Workload Security. The 23
integration points defined in Section 6.3 are the operational connections that turn governance
policy into a functioning risk management program.

**Expected outcomes, quantified:**

- 90%+ reduction in unmediated financial exposure from AI agent actions through HITL gates
  intercepting all autonomous transactions above $10,000
- Estimated 85% reduction in probability of repeat Imperium-class event
- 100% traceability for AI decisions: mandatory structured reasoning traces and immutable audit
  vault enable full forensic reconstruction of any future anomaly
- Audit preparation time reduced from 6–8 weeks to under 72 hours
- 100% of AI agents registered, policy-governed, and monitored within 6 months
- Zero ungoverned contractor tool introductions after Month 4 C-SCRM policy implementation
- Estimated 60% reduction in mean-time-to-contain for AI incidents
- Framework compliance: transition to postures meeting NIST AI RMF, ISO/IEC 42001,
  NIST SP 800-161, and NIST CSF 2.0 within 18 months

**Call to action:** approve the Phase 1 budget ($600,000–$800,000) at the next executive session.
Risk-tolerance documentation and the HITL financial gate can be initiated within 48 hours at
minimal incremental cost while formal budget is finalized — these two actions alone would have
prevented the Imperium Incident. The Shadow Bridge Audit should begin simultaneously. Every
additional day without a HITL policy is another day Agent-Alpha — or any successor agent — can
place the next $12M Silent Order without a single human ever knowing.

---

**References:** NIST AI Risk Management Framework 1.0 (AI RMF) · ISO/IEC 42001 (AI Management
Systems) · NIST SP 800-207 (Zero Trust Architecture) · NIST SP 800-37 (Risk Management Framework)
· NIST SP 800-161 (C-SCRM) · NIST SP 800-137 (ISCM) · NIST SP 800-160v1 (Systems Security
Engineering) · NIST Cybersecurity Framework 2.0 · CISA Zero Trust Maturity Model v2 · OWASP AI
Security Top 10 / LLM Risks · EU AI Act (Articles 9, 14) · CIS Controls v8 · SOC 2 (CC6.1 —
Segregation of Duties)
