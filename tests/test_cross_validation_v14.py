from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import h3_cv_common
import create_h3_validation_matrix
import merge_h3_reviews
import prepare_h3_blind_review
import combine_h3_replications


@contextmanager
def argv(*items: str):
    old = sys.argv[:]
    sys.argv = [old[0], *items]
    try:
        yield
    finally:
        sys.argv = old


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class CrossValidationV14Tests(unittest.TestCase):
    def test_ref2va_metric_set_contains_audio_and_leakage_controls(self):
        metrics = h3_cv_common.applicable_metrics("ref2va")
        self.assertIn("audio_source_accuracy", metrics)
        self.assertIn("speaker_binding", metrics)
        self.assertIn("attribute_leakage_control", metrics)

    def test_non_ref_task_uses_base_metrics(self):
        metrics = h3_cv_common.applicable_metrics("fl2va")
        self.assertIn("keyframe_alignment", metrics)
        self.assertNotIn("audio_source_accuracy", metrics)

    def test_canonical_hash_is_order_independent(self):
        a = h3_cv_common.canonical_json_hash({"b": 2, "a": 1})
        b = h3_cv_common.canonical_json_hash({"a": 1, "b": 2})
        self.assertEqual(a, b)

    def make_plan(self, td: Path, missing_profile: bool = False):
        for name in ["direct.txt", "concise.txt", "ir.txt", "semantic.md", "input.json", "refs.json"]:
            (td / name).write_text("x", encoding="utf-8")
        prompts = {
            "direct": "direct.txt",
            "concise_structured": "concise.txt",
            "context_ir_emulation": "ir.txt",
        }
        if missing_profile:
            prompts.pop("context_ir_emulation")
        cases = {
            "study_family_id": "family-v14",
            "study_plan_id": "plan-v14-A",
            "preregistered_at": "2026-08-04T16:00:00+08:00",
            "profiles": ["direct", "concise_structured", "context_ir_emulation"],
            "seeds": [101, 202],
            "analysis_plan": {"baseline_profile": "direct", "hard_fail_rule": "majority", "policy": "H3-CV-v1.4-clustered"},
            "cases": [{
                "case_id": "ref_case_01",
                "task_type": "ref2va",
                "prompt_author_id": "A",
                "parity_reviewer_id": "B",
                "semantic_lock_file": "semantic.md",
                "input_manifest": "input.json",
                "ref_manifest": "refs.json",
                "prompts": prompts,
                "video_pattern": "outputs/{case_id}_seed{seed}_{profile}.mp4",
            }],
        }
        env = {"experiment_id": "exp-v14", "environment_id": "env-A", "generation": {"width": 1344, "height": 768, "frames": 124, "require_audio": True}}
        write_json(td / "cases.json", cases)
        write_json(td / "env.json", env)
        return td / "cases.json", td / "env.json"

    def test_matrix_has_case_seed_profile_cartesian_product(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            cases, env = self.make_plan(td)
            output = td / "runs.csv"
            with argv(str(cases), str(env), str(output)):
                self.assertEqual(create_h3_validation_matrix.main(), 0)
            rows = h3_cv_common.read_csv(output)
            self.assertEqual(len(rows), 6)
            self.assertEqual({r["profile"] for r in rows}, {"direct", "concise_structured", "context_ir_emulation"})
            self.assertEqual({r["seed"] for r in rows}, {"101", "202"})
            self.assertTrue(all("audio_source_accuracy" in r["applicable_metrics"] for r in rows))

    def test_matrix_rejects_missing_profile_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            cases, env = self.make_plan(td, missing_profile=True)
            with argv(str(cases), str(env), str(td / "runs.csv")):
                with self.assertRaises(SystemExit):
                    create_h3_validation_matrix.main()

    def test_matrix_rejects_self_parity_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            cases, env = self.make_plan(td)
            data = json.loads(cases.read_text(encoding="utf-8"))
            data["cases"][0]["parity_reviewer_id"] = "A"
            write_json(cases, data)
            with argv(str(cases), str(env), str(td / "runs.csv")):
                with self.assertRaises(SystemExit):
                    create_h3_validation_matrix.main()

    def test_merge_reviews_accepts_distinct_reviewers(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            r1 = [{"reviewer_id": "R1", "blind_id": "B00001", "hard_fail": "", "overall_quality": "4"}]
            r2 = [{"reviewer_id": "R2", "blind_id": "B00001", "hard_fail": "", "overall_quality": "5"}]
            write_csv(td / "r1.csv", r1)
            write_csv(td / "r2.csv", r2)
            with argv(str(td / "merged.csv"), str(td / "r1.csv"), str(td / "r2.csv")):
                self.assertEqual(merge_h3_reviews.main(), 0)
            self.assertEqual(len(h3_cv_common.read_csv(td / "merged.csv")), 2)

    def test_merge_reviews_rejects_duplicate_reviewer_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            r1 = [{"reviewer_id": "R1", "blind_id": "B00001", "hard_fail": "", "overall_quality": "4"}]
            r2 = [{"reviewer_id": "R1", "blind_id": "B00002", "hard_fail": "", "overall_quality": "5"}]
            write_csv(td / "r1.csv", r1)
            write_csv(td / "r2.csv", r2)
            with argv(str(td / "merged.csv"), str(td / "r1.csv"), str(td / "r2.csv")):
                with self.assertRaises(SystemExit):
                    merge_h3_reviews.main()

    def test_blind_package_requires_two_reviewers(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            write_csv(td / "manifest.csv", [{"run_id": "r1", "case_id": "c1", "seed": "1", "profile": "direct", "task_type": "ref2va", "video_file": "missing.mp4"}])
            with argv(str(td / "manifest.csv"), str(td / "blind"), "--reviewers", "R1"):
                with self.assertRaises(SystemExit):
                    prepare_h3_blind_review.main()

    def test_replication_combiner_requires_distinct_environments(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            base = {
                "study_family_id": "family-v14",
                "environment_id": "env-A",
                "study_plan_id": "plan-A",
                "evidence_level": "provisional",
                "comparisons": {"context_ir_emulation": {"metrics": {"overall_quality": {"mean_delta": 0.5}}}},
            }
            write_json(td / "a.json", base)
            b = dict(base)
            b["study_plan_id"] = "plan-B"
            write_json(td / "b.json", b)
            with argv(str(td / "a.json"), str(td / "b.json")):
                with self.assertRaises(SystemExit):
                    combine_h3_replications.main()

    def test_replication_combiner_supports_consistent_independent_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            td = Path(tmp)
            a = {
                "study_family_id": "family-v14", "environment_id": "env-A", "study_plan_id": "plan-A", "evidence_level": "provisional",
                "comparisons": {"context_ir_emulation": {"metrics": {"overall_quality": {"mean_delta": 0.5}}}},
            }
            b = {
                "study_family_id": "family-v14", "environment_id": "env-B", "study_plan_id": "plan-B", "evidence_level": "provisional",
                "comparisons": {"context_ir_emulation": {"metrics": {"overall_quality": {"mean_delta": 0.7}}}},
            }
            write_json(td / "a.json", a)
            write_json(td / "b.json", b)
            out = td / "combined.json"
            with argv(str(td / "a.json"), str(td / "b.json"), "--output-json", str(out)):
                self.assertEqual(combine_h3_replications.main(), 0)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["comparisons"]["context_ir_emulation"]["evidence_level"], "supported_replicated")


if __name__ == "__main__":
    unittest.main()
