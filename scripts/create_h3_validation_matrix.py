#!/usr/bin/env python3
"""Create a preregistered Case × Seed × Profile run matrix."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from h3_cv_common import applicable_metrics, canonical_json_hash, load_json, resolve, sha256_file, write_csv

FIELDS = [
    "experiment_id", "environment_id", "environment_sha256", "study_family_id", "study_plan_id",
    "preregistered_at", "cases_file", "cases_sha256", "baseline_profile", "hard_fail_rule",
    "analysis_policy", "run_id", "case_id", "task_type", "seed", "profile", "semantic_lock_file",
    "semantic_lock_sha256", "input_manifest", "input_manifest_sha256", "ref_manifest",
    "ref_manifest_sha256", "prompt_file", "prompt_sha256", "video_file", "video_sha256",
    "applicable_metrics", "status", "notes",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", type=Path)
    ap.add_argument("environment", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--allow-self-parity", action="store_true")
    args = ap.parse_args()

    cases = load_json(args.cases)
    env = load_json(args.environment)
    profiles = cases.get("profiles") or ["direct", "concise_structured", "context_ir_emulation"]
    seeds = cases.get("seeds") or [1001, 1002, 1003]
    plan = cases.get("analysis_plan") or {}
    baseline = plan.get("baseline_profile", "direct")
    if baseline not in profiles:
        raise SystemExit("baseline_profile is not present in profiles")
    if len(set(profiles)) != len(profiles):
        raise SystemExit("profiles contain duplicates")

    env_hash = canonical_json_hash(env)
    cases_hash = canonical_json_hash(cases)
    base = args.cases.parent.resolve()
    rows = []
    for case in cases.get("cases", []):
        case_id = case["case_id"]
        prompts = case.get("prompts", {})
        missing = [p for p in profiles if p not in prompts]
        if missing:
            raise SystemExit(f"case={case_id} missing prompts for profiles={missing}")
        author = str(case.get("prompt_author_id", ""))
        reviewer = str(case.get("parity_reviewer_id", ""))
        if author and reviewer and author == reviewer and not args.allow_self_parity:
            raise SystemExit(f"case={case_id} prompt author and parity reviewer must differ")

        semantic = resolve(base, case.get("semantic_lock_file"))
        input_manifest = resolve(base, case.get("input_manifest"))
        ref_manifest = resolve(base, case.get("ref_manifest"))
        for p in [semantic, input_manifest, ref_manifest]:
            if p and not p.exists():
                raise SystemExit(f"case={case_id} missing file: {p}")

        for seed in seeds:
            for profile in profiles:
                prompt = resolve(base, prompts[profile])
                if not prompt or not prompt.exists():
                    raise SystemExit(f"case={case_id} missing prompt file: {prompt}")
                pattern = case.get("video_pattern", "outputs/{case_id}_seed{seed}_{profile}.mp4")
                video = resolve(base, pattern.format(case_id=case_id, seed=seed, profile=profile))
                run_id = f"{case_id}__s{seed}__{profile}"
                rows.append({
                    "experiment_id": env.get("experiment_id", "CHANGE_ME"),
                    "environment_id": env.get("environment_id", "CHANGE_ME"),
                    "environment_sha256": env_hash,
                    "study_family_id": cases.get("study_family_id", "CHANGE_ME"),
                    "study_plan_id": cases.get("study_plan_id", "CHANGE_ME"),
                    "preregistered_at": cases.get("preregistered_at", "CHANGE_ME"),
                    "cases_file": str(args.cases.resolve()),
                    "cases_sha256": cases_hash,
                    "baseline_profile": baseline,
                    "hard_fail_rule": plan.get("hard_fail_rule", "majority"),
                    "analysis_policy": plan.get("policy", "H3-CV-v1.5-clustered"),
                    "run_id": run_id,
                    "case_id": case_id,
                    "task_type": case.get("task_type", "unknown"),
                    "seed": seed,
                    "profile": profile,
                    "semantic_lock_file": str(semantic or ""),
                    "semantic_lock_sha256": sha256_file(semantic) if semantic else "",
                    "input_manifest": str(input_manifest or ""),
                    "input_manifest_sha256": sha256_file(input_manifest) if input_manifest else "",
                    "ref_manifest": str(ref_manifest or ""),
                    "ref_manifest_sha256": sha256_file(ref_manifest) if ref_manifest else "",
                    "prompt_file": str(prompt),
                    "prompt_sha256": sha256_file(prompt),
                    "video_file": str(video or ""),
                    "video_sha256": "",
                    "applicable_metrics": ";".join(case.get("applicable_metrics") or applicable_metrics(case.get("task_type", ""))),
                    "status": "planned",
                    "notes": "",
                })
    if not rows:
        raise SystemExit("cases file contains no cases")
    write_csv(args.output, rows, FIELDS)
    print(f"created {len(rows)} runs: cases={len(cases.get('cases', []))}, seeds={len(seeds)}, profiles={profiles}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
