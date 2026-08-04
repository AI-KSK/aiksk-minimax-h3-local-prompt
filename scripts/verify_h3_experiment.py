#!/usr/bin/env python3
"""Verify environment/case/prompt/asset locks and matched Profile coverage."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

from h3_cv_common import canonical_json_hash, load_json, read_csv, sha256_file, write_csv

EXTRA_FIELDS = ["actual_width", "actual_height", "actual_frames", "actual_fps", "actual_duration_sec", "audio_streams"]


def probe_media(path: Path) -> dict[str, str]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {k: "" for k in EXTRA_FIELDS}
    proc = subprocess.run([
        ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ], capture_output=True, text=True, check=False)
    if proc.returncode:
        raise ValueError(f"ffprobe failed for {path}: {proc.stderr.strip()}")
    data = json.loads(proc.stdout)
    videos = [x for x in data.get("streams", []) if x.get("codec_type") == "video"]
    audios = [x for x in data.get("streams", []) if x.get("codec_type") == "audio"]
    if not videos:
        raise ValueError(f"no video stream: {path}")
    v = videos[0]
    rate = v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1"
    try:
        a, b = rate.split("/")
        fps = float(a) / float(b)
    except Exception:
        fps = 0.0
    frames = v.get("nb_frames") or ""
    duration = v.get("duration") or data.get("format", {}).get("duration") or ""
    return {
        "actual_width": str(v.get("width", "")),
        "actual_height": str(v.get("height", "")),
        "actual_frames": str(frames),
        "actual_fps": f"{fps:.6f}" if fps else "",
        "actual_duration_sec": str(duration),
        "audio_streams": str(len(audios)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("environment", type=Path)
    ap.add_argument("--write-verified-manifest", type=Path)
    ap.add_argument("--allow-missing-videos", action="store_true")
    args = ap.parse_args()

    rows = read_csv(args.manifest)
    env = load_json(args.environment)
    env_hash = canonical_json_hash(env)
    errors, warnings = [], []
    run_ids, video_paths = set(), {}
    groups = defaultdict(list)
    expected_profiles = set()
    for r in rows:
        expected_profiles.add(r["profile"])
        rid = r["run_id"]
        if rid in run_ids:
            errors.append(f"duplicate run_id: {rid}")
        run_ids.add(rid)
        if r.get("environment_sha256") != env_hash:
            errors.append(f"{rid}: environment hash mismatch")
        for field, hash_field in [
            ("semantic_lock_file", "semantic_lock_sha256"),
            ("input_manifest", "input_manifest_sha256"),
            ("ref_manifest", "ref_manifest_sha256"),
            ("prompt_file", "prompt_sha256"),
        ]:
            if not r.get(field):
                continue
            p = Path(r[field])
            if not p.exists():
                errors.append(f"{rid}: missing {field}: {p}")
            elif r.get(hash_field) and sha256_file(p) != r[hash_field]:
                errors.append(f"{rid}: {hash_field} mismatch")
        groups[(r["case_id"], r["seed"])].append(r)

        video = Path(r.get("video_file", "")) if r.get("video_file") else None
        if not video or not video.exists():
            if not args.allow_missing_videos:
                errors.append(f"{rid}: missing video: {video}")
            r["status"] = "missing_video"
            continue
        resolved = str(video.resolve())
        if resolved in video_paths:
            errors.append(f"video path reused by {video_paths[resolved]} and {rid}")
        video_paths[resolved] = rid
        digest = sha256_file(video)
        r["video_sha256"] = digest
        try:
            r.update(probe_media(video))
        except ValueError as ex:
            errors.append(str(ex))
            continue
        gen = env.get("generation", {})
        checks = [
            ("actual_width", gen.get("width")),
            ("actual_height", gen.get("height")),
            ("actual_frames", gen.get("frames")),
            ("audio_streams", 1 if gen.get("require_audio", True) else None),
        ]
        for field, expected in checks:
            if expected is None or r.get(field, "") == "":
                continue
            actual = int(float(r[field]))
            if field == "audio_streams":
                if expected and actual < 1:
                    errors.append(f"{rid}: expected audio stream")
            elif actual != int(expected):
                errors.append(f"{rid}: {field}={actual}, expected={expected}")
        if gen.get("fps") and r.get("actual_fps"):
            if abs(float(r["actual_fps"]) - float(gen["fps"])) > 0.05:
                errors.append(f"{rid}: fps mismatch")
        r["status"] = "verified"

    for key, grp in groups.items():
        profs = [r["profile"] for r in grp]
        if len(profs) != len(set(profs)):
            errors.append(f"case/seed={key}: duplicate profile")
        if set(profs) != expected_profiles:
            errors.append(f"case/seed={key}: incomplete profiles {sorted(profs)} expected {sorted(expected_profiles)}")
        prompt_hashes = defaultdict(list)
        for r in grp:
            prompt_hashes[r.get("prompt_sha256", "")].append(r["profile"])
        for digest, profiles in prompt_hashes.items():
            if digest and len(profiles) > 1:
                warnings.append(f"case/seed={key}: identical prompt content across profiles={profiles}")

    for x in warnings:
        print("WARNING:", x)
    for x in errors:
        print("ERROR:", x)
    if errors:
        return 1
    if args.write_verified_manifest:
        fields = list(rows[0].keys()) if rows else []
        for f in EXTRA_FIELDS:
            if f not in fields:
                fields.append(f)
        write_csv(args.write_verified_manifest, rows, fields)
    print(f"PASS: {len(rows)} runs, {len(groups)} matched case/seed groups, profiles={sorted(expected_profiles)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
