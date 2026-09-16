# Six-agent commerce flywheel — orchestration (excerpted)

Three real GitHub Actions workflow files, unmodified, from a private six-agent product-discovery
and ad-automation pipeline. These are the scheduling and orchestration layer only — what runs,
when, in what order, and how failures are surfaced.

**Not included:** the agent logic itself (`product_discovery/`, `intelligence/`), the strategic
docs, and anything describing niche selection or ad-angle methodology. That's the working part of
a live business, not a portfolio artifact — publishing it would hand away the actual method, not
just demonstrate that I can build one. `${{ secrets.* }}` references below are GitHub Actions'
own secret-injection syntax — no key material, ever, touches the repo.

- **`weekly_discovery.yml`** — Monday-morning cron. Runs the discovery agent non-interactively,
  uploads its output as a build artifact, and emails a notification on success or failure —
  distinct paths for each, so a silent failure can't look like a quiet success.
- **`weekly_feedback.yml`** — Friday-evening cron, ahead of Monday's discovery run. Synthesizes
  the week's performance data into constraints for the next cycle — this is the feedback loop
  that makes the flywheel smarter over time, though the synthesis logic itself isn't in this
  excerpt.
- **`daily_monitor.yml`** — daily cron watching live campaign performance across every active
  product.

Real module paths (`intelligence.daily_monitor`, `product_discovery.discovery_agent`,
`intelligence.feedback_writer`) are visible here and confirm the architecture described in the
main portfolio: a scheduled, six-agent pipeline with one deliberate human approval gate before
spend, not a description invented for this page.
