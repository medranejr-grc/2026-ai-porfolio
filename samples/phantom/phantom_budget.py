"""
Cost estimation + budget guardrails for Phantom/Veldt generation runs.
(Pattern inspired by OpenMontage's cost-tracker; re-implemented from scratch — no AGPL code.)

WHY: before /teaser sends teasers all day, before /autobuild auto-regenerates on QC failures, and
before any UGC batch, we need to KNOW the spend and CAP it. This estimates each op, logs a per-job
ledger, and enforces caps in one of three modes: observe / warn / hardcap.

PRICES are seeded with best-known values; anything marked verified=False MUST be confirmed against
WAVESPEED_API_REFERENCE.md and real billing before trusting the totals. The framework is the value;
the cents are config you tune.

Usage:
    from phantom_budget import Budget, estimate, estimate_recipe, TEASER, PREMIUM_FULL
    b = Budget(jobdir, cap_job=10.0, cap_op=1.50, mode="warn")
    b.charge("beam animate", "kling_v3_std_i2v", estimate("kling_v3_std_i2v", seconds=10))
    print(b.summary())
    # planning without spending:
    print("teaser ~", estimate_recipe(TEASER))
"""
import os, json, sys, argparse
from datetime import datetime, timezone

# THREE COST CENTERS (know all three; don't just count WaveSpeed):
#   1. WaveSpeed  -> real out-of-pocket $ (auto-top-up). The prices below. THE one that matters.
#   2. Higgsfield -> Nano Banana Pro edits @ ~2 credits each, covered by the monthly Plus sub
#                    (marginal $/video ~= 0). Pulled 2026-07-02: 955.4 credits, Plus plan.
#   3. Anthropic API -> the agent (me): orchestration + vision-QC tokens. NOT auto-estimable here;
#                    scales with how hands-on the run is -> a real argument for a leaner pipeline.
#                    Check the Anthropic console for the true number.
#
# CALIBRATION: prices below are REAL, from WAVESPEED_API_REFERENCE.md (WaveSpeed model pages).
# Micah premium burned ~$20 WaveSpeed (2x $10 auto-top-ups) — a clean recipe (~$13) x ITERATION_FACTOR
# lands right at that. THE DOMINANT COST IS KLING ANIMATION at $0.90/clip FLAT — ~$9 of the ~$13.
# => animation RE-ROLLS are where money burns (Micah's 4 beam variants alone = $3.60). Minimize by
#    nailing the still + motion prompt first-try / auto-QC BEFORE animating.
ITERATION_FACTOR = 1.7   # real jobs re-roll; a clean recipe undercounts. Kling re-rolls dominate.

# op_key: (unit, price_per_unit, verified)   unit in {"image","video_sec","clip"}  (clip/image = flat)
PRICES = {
    "seedream_image":     ("image",     0.04, True),    # $0.04/image (doc)
    "instant_character":  ("image",     0.05, False),   # "per-image", $ unspecified — estimate
    "nano_banana_edit":   ("image",     0.02, True),    # Higgsfield: ~2 credits, sub-covered
    "kling_v3_std_i2v":   ("clip",      0.90, True),    # ~$0.90/clip FLAT (doc) — the dominant cost
    "infinitetalk":       ("video_sec", 0.03, True),    # $0.03/sec (doc) -> 10s = $0.30
    "seedvr2_720":        ("video_sec", 0.02, True),
    "seedvr2_1080":       ("video_sec", 0.03, True),
    "seedvr2_2k":         ("video_sec", 0.04, True),
    "seedvr2_4k":         ("video_sec", 0.05, True),
    "vace_joiner":        ("clip",      0.20, True),     # $0.20/call (doc)
    "video_upscaler_pro": ("video_sec", 0.03, True),    # ~$0.03/sec @1080p (doc)
}

class BudgetExceeded(Exception): pass

def estimate(op, seconds=None, count=1):
    if op not in PRICES:
        raise KeyError(f"unknown op '{op}' — add it to PRICES")
    unit, price, _ = PRICES[op]
    if unit == "video_sec":
        if seconds is None:
            raise ValueError(f"{op} is priced per second — pass seconds=")
        return round(price * seconds * count, 4)
    return round(price * count, 4)

def estimate_recipe(items):
    """items = [(op, {kwargs}), ...] -> CLEAN total $ (no re-rolls)."""
    return round(sum(estimate(op, **kw) for op, kw in items), 4)

def job_estimate(items):
    """Realistic $ including iteration/re-rolls. Returns (clean, realistic)."""
    clean = estimate_recipe(items)
    return clean, round(clean * ITERATION_FACTOR, 2)

# --- recipe templates (tune to your actual plans) ---
TEASER = [("seedream_image", {}), ("kling_v3_std_i2v", {})]                        # 1 still + 1 anim clip
PREMIUM_FULL = (                                                                    # ~Micah-scale
    [("seedream_image", {"count": 8}), ("instant_character", {"count": 4})]         # ~12 stills
    + [("kling_v3_std_i2v", {"count": 10})]                                         # ~10 b-roll anims @ $0.90
    + [("infinitetalk", {"seconds": 10, "count": 6})]                              # 6 perf lip-sync
    + [("seedvr2_1080", {"seconds": 10, "count": 6})]                              # upscale the 6
)

class Budget:
    def __init__(self, jobdir, cap_job=10.0, cap_op=2.0, mode="warn"):
        assert mode in ("observe", "warn", "hardcap")
        self.ledger = os.path.join(jobdir, "budget_ledger.json")
        self.cap_job, self.cap_op, self.mode = cap_job, cap_op, mode
        self.entries = json.load(open(self.ledger)) if os.path.exists(self.ledger) else []

    @property
    def spent(self): return round(sum(e["cost"] for e in self.entries), 4)

    def _flag(self, msg):
        if self.mode == "observe": return True
        print(f"  [budget:{self.mode}] {msg}", file=sys.stderr)
        if self.mode == "hardcap": raise BudgetExceeded(msg)
        return False

    def charge(self, label, op, cost):
        ok = True
        if cost > self.cap_op:
            ok = self._flag(f"op '{label}' ${cost:.2f} exceeds per-op cap ${self.cap_op:.2f}") and ok
        if self.spent + cost > self.cap_job:
            ok = self._flag(f"job total ${self.spent + cost:.2f} exceeds cap ${self.cap_job:.2f} ('{label}')") and ok
        self.entries.append({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                             "label": label, "op": op, "cost": round(cost, 4)})
        json.dump(self.entries, open(self.ledger, "w"), indent=2)
        return ok

    def summary(self):
        n, unverified = len(self.entries), [k for k, v in PRICES.items() if not v[2]]
        return (f"spent ${self.spent:.2f} / cap ${self.cap_job:.2f} over {n} ops "
                f"(mode={self.mode}). NOTE: prices unverified for: {', '.join(unverified)}")

if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")  # Windows cp1252 console
    except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["teaser", "premium", "estimate"])
    ap.add_argument("--op"); ap.add_argument("--seconds", type=float); ap.add_argument("--count", type=int, default=1)
    a = ap.parse_args()
    if a.cmd == "teaser":
        c, r = job_estimate(TEASER); print(f"teaser   clean ${c:.2f} | realistic ${r:.2f}  (WaveSpeed only)")
    elif a.cmd == "premium":
        c, r = job_estimate(PREMIUM_FULL); print(f"premium  clean ${c:.2f} | realistic ${r:.2f}  (WaveSpeed only; Micah actual ~$20)")
    else:
        print(f"{a.op} ~ ${estimate(a.op, seconds=a.seconds, count=a.count):.2f}")
    print("  + Higgsfield: Nano Banana edits, sub-covered (~0 marginal). + Anthropic API (agent tokens): check console.")
    unv = [k for k, v in PRICES.items() if not v[2]]
    print(f"(verify WaveSpeed prices vs dashboard: {', '.join(unv)})")
