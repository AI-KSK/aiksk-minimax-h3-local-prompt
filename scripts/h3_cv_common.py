#!/usr/bin/env python3
"""Shared utilities for AI-K SK MiniMax H3 v1.5 validation tools."""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any, Iterable

MULTIREF_METRICS = [
    "label_accuracy",
    "role_isolation",
    "identity_consistency",
    "motion_transfer",
    "camera_transfer",
    "audio_source_accuracy",
    "speaker_binding",
    "av_sync",
    "attribute_leakage_control",
    "overall_quality",
]

BASE_METRICS = [
    "keyframe_alignment",
    "identity_consistency",
    "action_accuracy",
    "camera_accuracy",
    "dialogue_accuracy",
    "no_extra_speech",
    "av_sync",
    "overall_quality",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def canonical_json_hash(data: Any) -> str:
    return sha256_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def resolve(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def median(values: Iterable[float]) -> float | None:
    vals = list(values)
    return statistics.median(vals) if vals else None


def parse_bool(value: str | bool | int | None) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "fail", "failed"}


def applicable_metrics(task_type: str) -> list[str]:
    return MULTIREF_METRICS if task_type.lower() in {"ref2va", "r2v"} else BASE_METRICS
