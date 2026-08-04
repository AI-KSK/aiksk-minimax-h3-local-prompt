#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from h3_refmap import build_manifest_from_manual, build_manifest_from_workflow, load_json, render_mapping

def main()->int:
    p=argparse.ArgumentParser(description="Build exact MiniMax H3 Ref2VA Picture/Video/Audio label mapping")
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--workflow", type=Path)
    g.add_argument("--manual-config", type=Path)
    p.add_argument("--node-index", type=int, default=0)
    p.add_argument("--output", type=Path)
    p.add_argument("--fail-on-error", action="store_true")
    args=p.parse_args()
    if args.workflow:
        manifests=build_manifest_from_workflow(args.workflow)
        if not manifests:
            print("ERROR: no MiniMaxH3ReferenceToVideo node found", file=sys.stderr); return 1
        if args.node_index>=len(manifests):
            print(f"ERROR: node-index {args.node_index} out of range; found {len(manifests)} node(s)",file=sys.stderr); return 1
        manifest=manifests[args.node_index]
    else:
        manifest=build_manifest_from_manual(load_json(args.manual_config))
    print(render_mapping(manifest))
    for x in manifest.get("warnings",[]): print("WARN:",x)
    for x in manifest.get("errors",[]): print("ERROR:",x)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"Saved: {args.output}")
    return 1 if args.fail_on_error and manifest.get("errors") else 0
if __name__=="__main__": raise SystemExit(main())
