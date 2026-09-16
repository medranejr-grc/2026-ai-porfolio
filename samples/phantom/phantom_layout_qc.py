#!/usr/bin/env python3
"""
Phantom Studios — Visual Layout QC
Extracts frames, draws Phantom safe zones, and outputs a contact sheet for human review.

Zone definitions for 720×1280 (9:16 vertical, Phantom default):
  FACE ZONE    y=60–440   — floating girl heads (tf_scenes) should land here
  HERO ZONE    y=280–1050 — full-body artist / main subject
  CAPTION BAND y=1150–1280 — keep all key subjects OUT of this band

White void signature check: corners/sides should be near-white (RGB >200) for the
white-void aesthetic used in tf_scenes.

Usage:
  python phantom_layout_qc.py tf_scenes/scene_01.mp4              # single clip
  python phantom_layout_qc.py tf_scenes/*.mp4 --job-dir output/qc  # batch
  python phantom_layout_qc.py fullvideo_v4_FINAL.mp4 --timestamps 5 30 60 90 120
  python phantom_layout_qc.py clips/bricks_sync_1_fixed.mp4 --scene-type lipsync
  python phantom_layout_qc.py hero_whitevoid.png                  # still image
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow required — run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

# Phantom 9:16 vertical output dimensions (matches build_fullvideo*.py)
FRAME_W, FRAME_H = 720, 1280

# Zone definitions: (y_start, height, fill_rgba, border_rgba, label)
ZONES = {
    "face_zone": {
        "y": 60, "h": 380,
        "fill": (80, 200, 255, 55),
        "border": (80, 200, 255, 200),
        "label": "FACE ZONE — girl heads (tf_scenes)",
        "scene_types": ["face", "tf_scene", "auto"],
    },
    "hero_zone": {
        "y": 280, "h": 770,
        "fill": (80, 255, 150, 40),
        "border": (80, 255, 150, 160),
        "label": "HERO ZONE — full body / artist",
        "scene_types": ["artist", "lipsync", "broll", "auto"],
    },
    "caption_band": {
        "y": FRAME_H - 130, "h": 130,
        "fill": (255, 60, 60, 90),
        "border": (255, 60, 60, 220),
        "label": "CAPTION BAND — keep subject out",
        "scene_types": ["face", "artist", "lipsync", "broll", "tf_scene", "auto"],
    },
}

# White void: pixels with all channels above this are "near-white"
WHITE_THRESHOLD = 200
# Fraction of sampled border pixels that must be near-white to flag as white void scene
WHITE_VOID_MIN_RATIO = 0.35


def get_duration(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", path],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def extract_frame(video_path: str, timestamp: float, out_path: str) -> bool:
    """Extract one frame, padded/scaled to FRAME_W×FRAME_H with white letterbox."""
    r = subprocess.run(
        ["ffmpeg", "-y", "-ss", str(timestamp), "-i", video_path,
         "-frames:v", "1",
         "-vf", (
             f"scale={FRAME_W}:{FRAME_H}:force_original_aspect_ratio=decrease,"
             f"pad={FRAME_W}:{FRAME_H}:(ow-iw)/2:(oh-ih)/2:white"
         ),
         out_path],
        capture_output=True,
    )
    return r.returncode == 0 and Path(out_path).exists()


def load_still(path: str) -> Image.Image:
    """Load an image file, resized to FRAME_W×FRAME_H with white letterbox."""
    img = Image.open(path).convert("RGB")
    img.thumbnail((FRAME_W, FRAME_H), Image.LANCZOS)
    canvas = Image.new("RGB", (FRAME_W, FRAME_H), (255, 255, 255))
    x = (FRAME_W - img.width) // 2
    y = (FRAME_H - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def check_white_void(img: Image.Image) -> dict:
    """
    Sample border/corner pixels to detect the Phantom white-void aesthetic.
    Returns {"white_void": bool, "ratio": float}.
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    sample_step = 8
    margin = 40  # px inward from edge

    samples = []
    # Top strip
    for x in range(0, w, sample_step):
        for y in range(0, min(margin, h), 4):
            samples.append(rgb.getpixel((x, y)))
    # Left strip (skip top/bottom corners already counted)
    for y in range(100, h - 200, sample_step):
        for x in range(0, min(margin, w), 4):
            samples.append(rgb.getpixel((x, y)))
    # Right strip
    for y in range(100, h - 200, sample_step):
        for x in range(max(0, w - margin), w, 4):
            samples.append(rgb.getpixel((x, y)))
    # Below caption band upper edge (check if white continues there)
    caption_top = h - 130
    for x in range(0, w, sample_step):
        for y in range(max(0, caption_top - margin), caption_top, 4):
            samples.append(rgb.getpixel((x, y)))

    if not samples:
        return {"white_void": False, "ratio": 0.0}

    near_white = sum(
        1 for r, g, b in samples if r > WHITE_THRESHOLD and g > WHITE_THRESHOLD and b > WHITE_THRESHOLD
    )
    ratio = near_white / len(samples)
    return {"white_void": ratio >= WHITE_VOID_MIN_RATIO, "ratio": round(ratio, 2)}


def annotate_frame(img: Image.Image, scene_type: str, timestamp: float, void_result: dict) -> Image.Image:
    """Draw zone overlays and metadata onto a frame."""
    base = img.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for zone_name, z in ZONES.items():
        if scene_type not in z["scene_types"]:
            continue
        y0, h = z["y"], z["h"]
        # Fill
        draw.rectangle([0, y0, FRAME_W, y0 + h], fill=z["fill"])
        # Border
        draw.rectangle([0, y0, FRAME_W - 1, y0 + h], outline=z["border"], width=2)
        # Label
        draw.text((6, y0 + 4), z["label"], fill=(255, 255, 255, 230))

    # Top info bar
    draw.rectangle([0, 0, FRAME_W, 48], fill=(0, 0, 0, 170))
    void_tag = "WHITE VOID OK" if void_result["white_void"] else "NO WHITE VOID"
    info = f"t={timestamp:.1f}s  type={scene_type}  [{void_tag}]  ratio={void_result['ratio']:.0%}"
    draw.text((8, 13), info, fill=(255, 255, 255, 255))

    composed = Image.alpha_composite(base, overlay)
    return composed.convert("RGB")


def make_contact_sheet(annotated_frames: list, cols: int = 3) -> Image.Image:
    scale = 0.33
    tw = int(FRAME_W * scale)
    th = int(FRAME_H * scale)
    rows = (len(annotated_frames) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), (25, 25, 25))
    for i, frame in enumerate(annotated_frames):
        r, c = divmod(i, cols)
        thumb = frame.resize((tw, th), Image.LANCZOS)
        sheet.paste(thumb, (c * tw, r * th))
    return sheet


def qc_clip(
    path: str,
    scene_type: str = "auto",
    timestamps: list = None,
    job_dir: str = "output/qc",
) -> dict:
    p = Path(path)
    is_image = p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
    duration = 0.0

    if is_image:
        raw_frames = [load_still(path)]
        frame_timestamps = [0.0]
    else:
        duration = get_duration(path)
        if duration <= 0:
            return {"path": path, "status": "FAIL", "error": "Could not read duration"}

        if timestamps:
            frame_timestamps = [t for t in timestamps if t < duration]
        else:
            frame_timestamps = [
                duration * 0.10,
                duration * 0.50,
                duration * 0.85,
            ]

        raw_frames = []
        with tempfile.TemporaryDirectory() as tmp:
            for ts in frame_timestamps:
                out = f"{tmp}/f_{ts:.3f}.png"
                if extract_frame(path, ts, out):
                    raw_frames.append(Image.open(out).copy())

    if not raw_frames:
        return {"path": path, "status": "FAIL", "error": "No frames extracted"}

    annotated = []
    frame_reports = []
    for img, ts in zip(raw_frames, frame_timestamps):
        void = check_white_void(img)
        ann = annotate_frame(img, scene_type=scene_type, timestamp=ts, void_result=void)
        annotated.append(ann)
        frame_reports.append({"timestamp_sec": round(ts, 2), **void})

    # Save contact sheet
    sheet = make_contact_sheet(annotated)
    out_dir = Path(job_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sheet_path = str(out_dir / f"qc_{p.stem}.png")
    sheet.save(sheet_path)

    # Warnings
    warnings = []
    void_flags = [f["white_void"] for f in frame_reports]

    if scene_type in ("face", "tf_scene"):
        if not any(void_flags):
            warnings.append(
                "White void not detected — tf_scene clips should have white/near-white background. "
                "Verify the source still used the white void environment."
            )
    if any(void_flags) and not all(void_flags):
        warnings.append("White void inconsistent across frames — possible dirty background or transition artifact.")

    return {
        "path": path,
        "scene_type": scene_type,
        "duration_sec": round(duration, 2),
        "frames_checked": len(frame_reports),
        "frame_reports": frame_reports,
        "contact_sheet": sheet_path,
        "status": "WARN" if warnings else "PASS",
        "warnings": warnings,
        "checklist": [
            "[ ] Subject head NOT cut off by caption band (bottom 130px — red zone)",
            "[ ] tf_scene face lands in FACE ZONE (y=60–440 — blue zone)",
            "[ ] Artist/full-body clip fills HERO ZONE (y=280–1050 — green zone)",
            "[ ] White void background visible in border areas for tf_scenes",
            "[ ] No unwanted objects or text in the caption band",
            "[ ] Glow / shimmer aesthetic intact — no harsh dark edges from bad compositing",
            "[ ] Lip sync clip: mouth movement visible and not obscured by framing",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Phantom Studios — Visual Layout QC (Gate 1 / Gate 2 visual check)"
    )
    parser.add_argument("videos", nargs="+", help="Video files or still images to check")
    parser.add_argument(
        "--scene-type", default="auto",
        choices=["auto", "face", "tf_scene", "artist", "broll", "lipsync"],
        help="Scene type hint for zone expectations (default: auto shows all zones)",
    )
    parser.add_argument(
        "--timestamps", nargs="+", type=float, default=None,
        help="Specific timestamps in seconds to sample (default: 10/50/85%% of clip)",
    )
    parser.add_argument("--job-dir", default="output/qc",
                        help="Directory to write contact sheet PNGs (default: output/qc)")
    parser.add_argument("--json", action="store_true", dest="output_json",
                        help="Output machine-readable JSON instead of human-readable text")
    args = parser.parse_args()

    reports = []
    for vid in args.videos:
        if not Path(vid).exists():
            print(f"SKIP: {vid} not found", file=sys.stderr)
            continue
        print(f"  Checking {vid}...", file=sys.stderr)
        report = qc_clip(
            vid,
            scene_type=args.scene_type,
            timestamps=args.timestamps,
            job_dir=args.job_dir,
        )
        reports.append(report)

    if args.output_json:
        print(json.dumps(reports, indent=2))
    else:
        for r in reports:
            status = r.get("status", "FAIL")
            sym = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}.get(status, "?")
            print(f"\n{sym} {status}  {r['path']}")
            if "error" in r:
                print(f"   ERROR: {r['error']}")
                continue
            print(f"   {r.get('duration_sec', 0):.2f}s | {r['frames_checked']} frame(s) | type={r['scene_type']}")
            print(f"   Contact sheet -> {r['contact_sheet']}")
            for w in r.get("warnings", []):
                print(f"   WARN  {w}")
            print("   Checklist:")
            for item in r.get("checklist", []):
                print(f"     {item}")
        print()

    any_fail = any(r.get("status") == "FAIL" for r in reports)
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
