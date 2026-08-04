#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
from h3_refmap import build_manifest_from_workflow, iter_nodes, load_json, render_mapping

def main()->int:
    p=argparse.ArgumentParser(description="Inspect MiniMax H3 workflow, modes, models, prompts and Ref2VA labels")
    p.add_argument("workflow",type=Path)
    p.add_argument("--json-out",type=Path)
    args=p.parse_args()
    data=load_json(args.workflow); nodes=list(iter_nodes(data)); types=[str(n.get("type")) for n in nodes]
    official=sorted(set(t for t in types if t in {"MiniMaxH3ImageToVideo","MiniMaxH3ReferenceToVideo"}))
    rh=sorted(set(t for t in types if t.startswith("RHMiniMaxH3")))
    report={"workflow":str(args.workflow),"node_count":len(nodes),"official_nodes":official,"rh_nodes":rh,"ref_manifests":[]}
    print(f"nodes: {len(nodes)}")
    if official: print("family: official ComfyUI native\nH3 nodes:",", ".join(official))
    elif rh: print("family: RunningHub/custom H3\nH3 nodes:",", ".join(rh))
    else: print("family: no recognized H3 node")
    for n in nodes:
        vals=n.get("widgets_values") or []
        for v in vals:
            if isinstance(v,str) and "minimax_h3_" in v.lower() and v.lower().endswith(".safetensors"):
                report.setdefault("models",[]).append(v); print("model:",v)
    manifests=build_manifest_from_workflow(args.workflow)
    for i,m in enumerate(manifests):
        print(f"\nRef2VA node {i}, id={m.get('node_id')}")
        print(render_mapping(m) or "(no connected references)")
        for x in m.get("warnings",[]): print("WARN:",x)
        for x in m.get("errors",[]): print("ERROR:",x)
    report["ref_manifests"]=manifests
    if args.json_out:
        args.json_out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
