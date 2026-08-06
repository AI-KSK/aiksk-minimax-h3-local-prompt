#!/usr/bin/env python3
"""Analyze matched Case/Seed/Profile blind reviews with conservative evidence labels."""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from h3_cv_common import MULTIREF_METRICS, median, parse_bool, read_csv


def two_stage_bootstrap(pair_by_case: dict[str, list[float]], repeats: int = 4000, seed: int = 1404) -> tuple[float, float]:
    if not pair_by_case:
        return (math.nan, math.nan)
    rng = random.Random(seed)
    cases = list(pair_by_case)
    vals = []
    for _ in range(repeats):
        sampled_cases = [rng.choice(cases) for _ in cases]
        sample = []
        for c in sampled_cases:
            seeds = pair_by_case[c]
            sample.extend(rng.choice(seeds) for _ in seeds)
        vals.append(statistics.mean(sample))
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("verified_manifest", type=Path)
    ap.add_argument("secret_mapping", type=Path)
    ap.add_argument("merged_reviews", type=Path)
    ap.add_argument("--baseline", default="direct")
    ap.add_argument("--output-json", type=Path)
    ap.add_argument("--output-md", type=Path)
    args = ap.parse_args()

    manifest = {r["run_id"]: r for r in read_csv(args.verified_manifest)}
    mapping = {r["blind_id"]: r for r in read_csv(args.secret_mapping)}
    reviews = read_csv(args.merged_reviews)
    by_blind = defaultdict(list)
    for r in reviews:
        if r.get("blind_id") not in mapping:
            raise SystemExit(f"unknown blind_id: {r.get('blind_id')}")
        by_blind[r["blind_id"]].append(r)
    reviewer_ids = {r["reviewer_id"] for r in reviews}
    expected_n = len(reviewer_ids)
    if expected_n < 2:
        raise SystemExit("at least two reviewers required")
    run_scores = {}
    for blind, m in mapping.items():
        rs = by_blind.get(blind, [])
        if len(rs) != expected_n:
            raise SystemExit(f"blind_id={blind} incomplete review coverage")
        rid = m["run_id"]
        if rid not in manifest:
            raise SystemExit(f"mapping references unknown run_id={rid}")
        metrics = {}
        for metric in MULTIREF_METRICS:
            vals = []
            for r in rs:
                raw = str(r.get(metric, "")).strip()
                if raw:
                    v = float(raw)
                    if not 0 <= v <= 5:
                        raise SystemExit(f"{blind}/{metric} outside 0–5")
                    vals.append(v)
            if vals:
                metrics[metric] = statistics.median(vals)
        hard_votes = sum(parse_bool(r.get("hard_fail")) for r in rs)
        hard_fail = hard_votes > expected_n / 2
        run_scores[rid] = {"hard_fail": hard_fail, "metrics": metrics}

    grouped = defaultdict(dict)
    for rid, row in manifest.items():
        grouped[(row["case_id"], row["seed"])][row["profile"]] = rid
    profiles = sorted({r["profile"] for r in manifest.values()})
    if args.baseline not in profiles:
        raise SystemExit("baseline not found")
    comparisons = {}
    for profile in profiles:
        if profile == args.baseline:
            continue
        per_metric = {}
        for metric in MULTIREF_METRICS:
            deltas, by_case, wins, ties, losses = [], defaultdict(list), 0, 0, 0
            for (case, seed), members in grouped.items():
                if args.baseline not in members or profile not in members:
                    raise SystemExit(f"incomplete matched group case={case} seed={seed}")
                b = run_scores[members[args.baseline]]
                p = run_scores[members[profile]]
                # Hard failures remain separate and do not get hidden by score averaging.
                bv = b["metrics"].get(metric)
                pv = p["metrics"].get(metric)
                if bv is None or pv is None:
                    continue
                d = pv - bv
                deltas.append(d)
                by_case[case].append(d)
                if d > 0.25:
                    wins += 1
                elif d < -0.25:
                    losses += 1
                else:
                    ties += 1
            if deltas:
                lo, hi = two_stage_bootstrap(by_case)
                per_metric[metric] = {
                    "matched_pairs": len(deltas),
                    "cases": len(by_case),
                    "mean_delta": statistics.mean(deltas),
                    "ci95": [lo, hi],
                    "wins": wins, "ties": ties, "losses": losses,
                }
        hard = {"baseline": 0, "profile": 0}
        for members in grouped.values():
            hard["baseline"] += int(run_scores[members[args.baseline]]["hard_fail"])
            hard["profile"] += int(run_scores[members[profile]]["hard_fail"])
        comparisons[profile] = {"hard_fail_counts": hard, "metrics": per_metric}

    task_types = {r["task_type"] for r in manifest.values()}
    cases = {r["case_id"] for r in manifest.values()}
    evidence = "exploratory"
    if len(task_types) >= 2 and len(cases) >= 6 and all(v["metrics"] for v in comparisons.values()):
        evidence = "provisional"
    result = {
        "study_family_id": next(iter(manifest.values())).get("study_family_id", ""),
        "study_plan_id": next(iter(manifest.values())).get("study_plan_id", ""),
        "environment_id": next(iter(manifest.values())).get("environment_id", ""),
        "baseline": args.baseline,
        "reviewers": sorted(reviewer_ids),
        "evidence_level": evidence,
        "comparisons": comparisons,
        "boundary": "Single-environment results cannot exceed provisional; real H3 renders and human reviews are required.",
    }
    lines = ["# MiniMax H3 v1.5 blind-review report", "", f"Evidence: **{evidence}**", ""]
    for profile, comp in comparisons.items():
        lines += [f"## {profile} vs {args.baseline}", "", f"Hard failures: {comp['hard_fail_counts']}", "", "| Metric | Pairs | Mean Δ | 95% CI | W/T/L |", "|---|---:|---:|---|---|"]
        for metric, x in comp["metrics"].items():
            lines.append(f"| {metric} | {x['matched_pairs']} | {x['mean_delta']:.3f} | [{x['ci95'][0]:.3f}, {x['ci95'][1]:.3f}] | {x['wins']}/{x['ties']}/{x['losses']} |")
        lines.append("")
    md = "\n".join(lines) + "\n"
    print(md)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(md, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
