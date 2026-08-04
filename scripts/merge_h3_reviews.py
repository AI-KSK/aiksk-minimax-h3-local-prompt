#!/usr/bin/env python3
"""Merge isolated reviewer score sheets with strict duplicate checks."""
from __future__ import annotations

import argparse
from pathlib import Path

from h3_cv_common import read_csv, write_csv


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path)
    ap.add_argument("review_files", nargs="+", type=Path)
    args = ap.parse_args()
    rows, seen, reviewers = [], set(), set()
    fields = None
    for path in args.review_files:
        data = read_csv(path)
        local_reviewers = {r.get("reviewer_id", "").strip() for r in data}
        if "" in local_reviewers or len(local_reviewers) != 1:
            raise SystemExit(f"{path}: must contain exactly one non-empty reviewer_id")
        reviewer = next(iter(local_reviewers))
        if reviewer in reviewers:
            raise SystemExit(f"duplicate reviewer_id across files: {reviewer}")
        reviewers.add(reviewer)
        for r in data:
            key = (reviewer, r.get("blind_id", ""))
            if not key[1] or key in seen:
                raise SystemExit(f"duplicate or empty reviewer/blind_id: {key}")
            seen.add(key)
            rows.append(r)
        if data and fields is None:
            fields = list(data[0].keys())
    if not rows:
        raise SystemExit("no review rows")
    write_csv(args.output, rows, fields or [])
    print(f"merged {len(rows)} review rows from {len(reviewers)} reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
