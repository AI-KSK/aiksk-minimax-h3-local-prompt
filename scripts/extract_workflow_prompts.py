#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
from typing import Any
from h3_refmap import iter_nodes, load_json

def strings(node):
    if "markdown" in str(node.get("type","")).lower(): return
    for i,v in enumerate(node.get("widgets_values") or []):
        if not isinstance(v,str): continue
        s=v.strip()
        if len(s)<20 or re.search(r"https?://|\.safetensors\b",s,re.I): continue
        if len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b",s))>=8 or "<Picture " in s or "[Shot 1]" in s:
            yield i,v

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("workflow",type=Path);p.add_argument("--out-dir",type=Path);args=p.parse_args()
    data=load_json(args.workflow);seen=set();found=[]
    for n in iter_nodes(data):
        for idx,text in strings(n) or []:
            h=hashlib.sha256(text.encode()).hexdigest()
            if h in seen:continue
            seen.add(h);found.append((n.get("id"),n.get("type"),idx,text,h))
    if not found: print("No likely prompt strings found.");return 2
    if args.out_dir:args.out_dir.mkdir(parents=True,exist_ok=True)
    for i,(nid,nt,wi,text,h) in enumerate(found,1):
        print(f"[{i}] node={nid} type={nt} widget={wi} sha256={h} chars={len(text)}")
        if args.out_dir:(args.out_dir/f"prompt_{i:02d}_node_{nid}_{h[:8]}.txt").write_text(text,encoding="utf-8")
    return 0
if __name__=="__main__":raise SystemExit(main())
