#!/usr/bin/env python3
"""Create physically separated admin/shared/reviewer blind-review packages."""
from __future__ import annotations

import argparse
import csv
import random
import shutil
import subprocess
from pathlib import Path

from h3_cv_common import MULTIREF_METRICS, read_csv, sha256_text, write_csv


def clean_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        proc = subprocess.run([
            ffmpeg, "-y", "-v", "error", "-i", str(src), "-map", "0", "-map_metadata", "-1", "-c", "copy", str(dst)
        ], check=False)
        if proc.returncode == 0:
            return
    shutil.copy2(src, dst)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("verified_manifest", type=Path)
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--reviewers", required=True, help="comma-separated reviewer IDs")
    ap.add_argument("--seed", type=int, default=1404)
    args = ap.parse_args()

    rows = read_csv(args.verified_manifest)
    reviewers = [x.strip() for x in args.reviewers.split(",") if x.strip()]
    if len(reviewers) < 2:
        raise SystemExit("at least two reviewers are required")
    out = args.output_dir
    if out.exists():
        shutil.rmtree(out)
    (out / "admin").mkdir(parents=True)
    (out / "shared" / "media").mkdir(parents=True)
    rng = random.Random(args.seed)
    shuffled = rows[:]
    rng.shuffle(shuffled)
    mapping = []
    for idx, r in enumerate(shuffled, 1):
        blind = f"B{idx:05d}"
        src = Path(r["video_file"])
        if not src.exists():
            raise SystemExit(f"missing video for blind package: {src}")
        ext = src.suffix.lower() or ".mp4"
        dst = out / "shared" / "media" / f"{blind}{ext}"
        clean_copy(src, dst)
        mapping.append({
            "blind_id": blind,
            "run_id": r["run_id"],
            "case_id": r["case_id"],
            "seed": r["seed"],
            "profile": r["profile"],
            "task_type": r["task_type"],
            "media_file": str(dst.resolve()),
        })
    write_csv(out / "admin" / "secret_mapping.csv", mapping, list(mapping[0].keys()))
    (out / "admin" / "package_fingerprint.txt").write_text(
        sha256_text("\n".join(x["blind_id"] + x["run_id"] for x in mapping)) + "\n", encoding="utf-8"
    )
    public = [{"blind_id": x["blind_id"], "task_type": x["task_type"], "media_file": x["media_file"]} for x in mapping]
    write_csv(out / "shared" / "review_items.csv", public, ["blind_id", "task_type", "media_file"])
    fields = ["reviewer_id", "blind_id", "hard_fail", "hard_fail_reason"] + MULTIREF_METRICS + ["notes"]
    for reviewer in reviewers:
        rdir = out / "reviewers" / reviewer
        rdir.mkdir(parents=True)
        template = []
        for x in public:
            row = {f: "" for f in fields}
            row.update({"reviewer_id": reviewer, "blind_id": x["blind_id"]})
            template.append(row)
        write_csv(rdir / "review_scores.csv", template, fields)
        shutil.copy2(out / "shared" / "review_items.csv", rdir / "review_items.csv")
    print(f"blinded {len(rows)} videos for reviewers={reviewers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
