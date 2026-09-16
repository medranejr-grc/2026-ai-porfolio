#!/usr/bin/env python3
"""
Phantom Studios — FFmpeg Technical QC
Run at Gate 1 (post-animation, pre-lip-sync) and Gate 3 (pre-delivery).

Usage:
  python phantom_ffmpeg_qc.py <video>
  python phantom_ffmpeg_qc.py clips/bricks_sync_1_fixed.mp4 --expect-audio
  python phantom_ffmpeg_qc.py fullvideo_v4_FINAL.mp4 --expected-res 720x1280
  python phantom_ffmpeg_qc.py tf_scenes/scene_01.mp4 --no-audio    # silent b-roll pre-mux
  python phantom_ffmpeg_qc.py phantom_clips/p_01.mp4 --json        # machine-readable
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Phantom-standard 9:16 vertical spec (what build_fullvideo*.py outputs)
PHANTOM_SPEC = {
    "width": 720,
    "height": 1280,
    "fps": 30,
    "video_codec": "h264",
    "pix_fmt": "yuv420p",
    "audio_codec": "aac",
    "loudness_target_lufs": -16.0,
    "loudness_tolerance": 3.0,   # ±3 LUFS before warning
}


def probe(path: str) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def detect_black_frames(path: str) -> list:
    result = subprocess.run(
        ["ffmpeg", "-i", path, "-vf", "blackdetect=d=0.3:pix_th=0.10", "-an", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    events = []
    for line in result.stderr.splitlines():
        if "black_start" not in line:
            continue
        parts = {}
        for token in line.split():
            if ":" in token:
                k, _, v = token.partition(":")
                parts[k] = v
        try:
            events.append({
                "start": float(parts.get("black_start", 0)),
                "end": float(parts.get("black_end", 0)),
                "duration": float(parts.get("black_duration", 0)),
            })
        except ValueError:
            pass
    return events


def measure_loudness(path: str):
    """Return integrated LUFS float, or None if no audio / measurement fails."""
    result = subprocess.run(
        ["ffmpeg", "-i", path,
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    lines = result.stderr.splitlines()
    for i, line in enumerate(lines):
        if '"input_i"' in line:
            # loudnorm prints a JSON block; grab it
            block_lines = []
            for j in range(max(0, i - 1), min(len(lines), i + 15)):
                block_lines.append(lines[j])
            block = "\n".join(block_lines)
            try:
                start = block.index("{")
                end = block.rindex("}") + 1
                data = json.loads(block[start:end])
                val = data.get("input_i", "")
                return float(val) if val not in ("", "-inf") else None
            except (ValueError, json.JSONDecodeError):
                pass
    return None


def run_qc(path: str, expect_audio: bool = True, expected_res: str = None) -> dict:
    warnings = []
    failures = []

    data = probe(path)
    streams = data.get("streams", [])
    fmt = data.get("format", {})

    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

    if not video_streams:
        failures.append("NO VIDEO STREAM — file may be corrupt")
        return {"path": path, "status": "FAIL", "failures": failures, "warnings": warnings, "metrics": {}}

    vs = video_streams[0]
    width = vs.get("width", 0)
    height = vs.get("height", 0)
    codec = vs.get("codec_name", "unknown")
    pix_fmt = vs.get("pix_fmt", "unknown")
    duration = float(fmt.get("duration") or vs.get("duration") or 0)

    fps_raw = vs.get("r_frame_rate", "0/1")
    try:
        num, den = fps_raw.split("/")
        fps = round(int(num) / int(den), 2)
    except (ValueError, ZeroDivisionError):
        fps = 0.0

    # --- Codec ---
    if codec not in ("h264", "hevc"):
        warnings.append(f"Video codec is '{codec}' — expected h264. Re-encode before delivery.")
    if pix_fmt != "yuv420p":
        warnings.append(f"Pixel format is '{pix_fmt}' — expected yuv420p. Social platforms may reject.")

    # --- FPS ---
    if not (29 <= fps <= 31):
        warnings.append(f"FPS is {fps} — expected 30. Clip may animate at wrong rate in stitch.")

    # --- Resolution ---
    if expected_res:
        ew, eh = (int(x) for x in expected_res.lower().split("x"))
    else:
        ew, eh = PHANTOM_SPEC["width"], PHANTOM_SPEC["height"]

    if width != ew or height != eh:
        warnings.append(
            f"Resolution is {width}×{height}, expected {ew}×{eh}. "
            "Blurred-fill normalization required before stitch."
        )

    # --- Duration sanity ---
    if duration < 1.0:
        failures.append(f"Duration {duration:.2f}s — likely truncated or corrupt.")

    # --- Audio ---
    if not audio_streams:
        if expect_audio:
            failures.append(
                "NO AUDIO STREAM — per-scene lip sync clips must have baked-in audio. "
                "Re-submit or check job output."
            )
        # Silent pre-mux clips are fine when --no-audio is set
    else:
        a = audio_streams[0]
        a_codec = a.get("codec_name", "")
        if a_codec not in ("aac", "mp3", "opus"):
            warnings.append(f"Audio codec is '{a_codec}' — expected aac for final delivery.")

        # Loudness check (only useful for clips with real audio content)
        lufs = measure_loudness(path)
        if lufs is not None:
            target = PHANTOM_SPEC["loudness_target_lufs"]
            tol = PHANTOM_SPEC["loudness_tolerance"]
            if abs(lufs - target) > tol:
                warnings.append(
                    f"Loudness is {lufs:.1f} LUFS — target {target} LUFS ±{tol}. "
                    "Run 'ffmpeg -af loudnorm=I=-16:TP=-1.5:LRA=11' before delivery."
                )
        else:
            warnings.append("Loudness measurement failed — verify audio content manually.")

    # --- Black frames ---
    black_frames = detect_black_frames(path)
    for bf in black_frames:
        if bf["duration"] >= 0.5:
            failures.append(f"Black frame {bf['duration']:.2f}s at t={bf['start']:.2f}s — likely bad transition or missing clip.")
        else:
            warnings.append(f"Short black flash ({bf['duration']:.2f}s) at t={bf['start']:.2f}s — check transition overlap.")

    status = "FAIL" if failures else ("WARN" if warnings else "PASS")

    return {
        "path": path,
        "status": status,
        "metrics": {
            "duration_sec": round(duration, 2),
            "resolution": f"{width}×{height}",
            "fps": fps,
            "video_codec": codec,
            "pix_fmt": pix_fmt,
            "audio_streams": len(audio_streams),
            "file_size_mb": round(int(fmt.get("size", 0)) / 1_048_576, 1),
        },
        "failures": failures,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Phantom Studios — FFmpeg Technical QC (Gate 1 / Gate 3)"
    )
    parser.add_argument("video", help="Video file to inspect")
    parser.add_argument("--expected-res", default=None,
                        help="Override expected resolution WxH (default: 720x1280)")
    parser.add_argument("--no-audio", action="store_true",
                        help="Don't flag missing audio (use for pre-mux silent clips)")
    parser.add_argument("--expect-audio", action="store_true",
                        help="Hard-fail if no audio stream (use for per-scene lip sync clips)")
    parser.add_argument("--json", action="store_true", dest="output_json",
                        help="Output machine-readable JSON")
    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"ERROR: File not found: {args.video}", file=sys.stderr)
        sys.exit(2)

    # --expect-audio overrides --no-audio; default is to warn (not hard-fail) on missing audio
    expect_audio = True
    if args.no_audio:
        expect_audio = False
    if args.expect_audio:
        expect_audio = True

    try:
        report = run_qc(args.video, expect_audio=expect_audio, expected_res=args.expected_res)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    if args.output_json:
        print(json.dumps(report, indent=2))
    else:
        status = report["status"]
        sym = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}.get(status, "?")
        m = report["metrics"]
        print(f"\n{sym} {status}  {report['path']}")
        if m:
            print(
                f"   {m.get('resolution')} | {m.get('fps')}fps | {m.get('video_codec')} | "
                f"{m.get('pix_fmt')} | {m.get('audio_streams')} audio | "
                f"{m.get('duration_sec')}s | {m.get('file_size_mb')} MB"
            )
        for f in report["failures"]:
            print(f"   FAIL  {f}")
        for w in report["warnings"]:
            print(f"   WARN  {w}")
        if not report["failures"] and not report["warnings"]:
            print("   All checks passed.")
        print()

    sys.exit({"PASS": 0, "WARN": 1, "FAIL": 2}.get(report["status"], 2))


if __name__ == "__main__":
    main()
