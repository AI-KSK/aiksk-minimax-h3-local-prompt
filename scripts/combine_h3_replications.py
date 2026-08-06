#!/usr/bin/env python3
"""Combine two or more independent preregistered environment reports conservatively."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reports", nargs="+", type=Path)
    ap.add_argument("--output-json", type=Path)
    ap.add_argument("--output-md", type=Path)
    args = ap.parse_args()
    if len(args.reports) < 2:
        raise SystemExit("at least two reports are required")
    reports = [json.loads(p.read_text(encoding="utf-8-sig")) for p in args.reports]
    envs = [r.get("environment_id") for r in reports]
    if len(set(envs)) != len(envs):
        raise SystemExit("replications must use distinct environment_id values")
    families = {r.get("study_family_id") for r in reports}
    if len(families) != 1:
        raise SystemExit("reports must share one study_family_id")
    plans = [r.get("study_plan_id") for r in reports]
    if len(set(plans)) != len(plans):
        raise SystemExit("replications should use independently registered study_plan_id values")
    profiles = set.intersection(*(set(r.get("comparisons", {})) for r in reports))
    combined = {}
    for profile in sorted(profiles):
        directions = []
        for r in reports:
            metrics = r["comparisons"][profile].get("metrics", {})
            overall = metrics.get("overall_quality") or next(iter(metrics.values()), None)
            if not overall:
                directions.append("no_data")
            elif overall.get("mean_delta", 0) > 0.25:
                directions.append("positive")
            elif overall.get("mean_delta", 0) < -0.25:
                directions.append("negative")
            else:
                directions.append("neutral")
        consistent = len(set(directions)) == 1 and directions[0] in {"positive", "negative"}
        all_provisional = all(r.get("evidence_level") == "provisional" for r in reports)
        combined[profile] = {
            "directions": directions,
            "evidence_level": "supported_replicated" if consistent and all_provisional else "not_replicated",
        }
    result = {
        "study_family_id": next(iter(families)),
        "environments": envs,
        "study_plans": plans,
        "comparisons": combined,
        "boundary": "This confirms directional replication only; it does not pool distinct environments as one random sample.",
    }
    lines = ["# MiniMax H3 v1.5 replication summary", "", "| Profile | Directions | Evidence |", "|---|---|---|"]
    for p, x in combined.items():
        lines.append(f"| {p} | {' / '.join(x['directions'])} | {x['evidence_level']} |")
    md = "\n".join(lines) + "\n"
    print(md)
    if args.output_json:
        args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.write_text(md, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
