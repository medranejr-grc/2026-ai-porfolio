# Phantom Studios: guardrail code (excerpted)

Three real files, unmodified, pulled from a larger private production pipeline (122 Python
modules) that generates AI music videos and ad content. This is the pipeline's engineering
guardrail layer: the part that has nothing to do with creative output and everything to do with
not letting an agent spend money or ship a bad frame unsupervised.

**Not included:** the generation/creative code, client folders, and business-development
documents (GTM strategy, outreach scripts) that live in the same private repo. Those stay
private; this excerpt is scoped to the control layer specifically, because that's the part
relevant to agent governance rather than to the media business itself.

- **`phantom_budget.py`**: cost estimation and spend guardrails across three cost centers
  (generation API, editing credits, orchestration tokens), enforced in three modes: observe /
  warn / hardcap. Every price marked `verified=False` is flagged as needing confirmation against
  real billing before the total is trusted; the tool refuses to assert confidence it hasn't
  earned.
- **`phantom_ffmpeg_qc.py`**: automated technical QC (resolution, audio presence, spec
  conformance) run at fixed pipeline gates, before lip-sync and before delivery. Machine-readable
  `--json` output.
- **`phantom_layout_qc.py`**: automated visual-layout QC that draws the pipeline's safe-zone
  definitions over extracted frames and flags subjects that land outside them, for human review
  before a clip is approved.

The pattern across all three: a human approval gate exists at every stage that spends money or
ships output, and these tools exist to make that human's review fast and evidence-based rather
than a guess.
