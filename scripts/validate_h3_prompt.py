#!/usr/bin/env python3
"""Static MiniMax H3 prompt validator v1.5. Does not run the model."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
from h3_refmap import build_manifest_from_workflow, flatten_labels, load_json

CORE=("integrated_multimodal_description:","overall_soundscape:","non_diegetic_music:")
REF=("subject_definitions:","summary:","retention_analysis:","detailed_description:","overall_soundscape:","non_diegetic_music:")
PLACEHOLDER=re.compile(r"(?:\.\.\.|…{2,}|\[(?:STYLE|ACTION|SUBJECT|SCENE|CAMERA|SOUND|TARGET|ROLE|FILL|TODO)[^\]]*\]|\b(?:TBD|TODO|PLACEHOLDER)\b)",re.I)

def positions(text,fields):return [re.search(rf"(?m)^\s*{re.escape(f)}",text).start() if re.search(rf"(?m)^\s*{re.escape(f)}",text) else -1 for f in fields]
def sections(text,fields):
    ps=positions(text,fields);out={}
    for i,f in enumerate(fields):
        if ps[i]<0:continue
        m=re.search(rf"(?m)^\s*{re.escape(f)}",text[ps[i]:]);start=ps[i]+m.end();later=[x for x in ps[i+1:] if x>=0];end=min(later) if later else len(text);out[f]=text[start:end].strip()
    return out

def labels(text,kind):return {int(x) for x in re.findall(rf"<{kind}\s+(\d+)>",text,re.I)}
def shot_times(body):
    out=[]
    for m in re.finditer(r"\[Shot\s+(\d+)\](?:\s+At\s+(\d{2}):(\d{2})\.(\d{3}),)?",body,re.I):
        t=None if m.group(2) is None else int(m.group(2))*60+int(m.group(3))+int(m.group(4))/1000
        out.append((int(m.group(1)),t))
    return out

def check_shots(body,duration,e,w):
    ss=shot_times(body)
    if not ss:e.append("no [Shot 1] found");return
    ids=[x[0] for x in ss]
    if ids!=list(range(1,len(ids)+1)):e.append(f"shots must be consecutive and unique; found {ids}")
    if ss[0][1] is not None:e.append("Shot 1 must not have a timestamp")
    ts=[x[1] for x in ss[1:]]
    if any(x is None for x in ts):e.append("every shot after Shot 1 requires At MM:SS.mmm")
    vv=[x for x in ts if x is not None]
    if any(b<=a for a,b in zip(vv,vv[1:])):e.append("shot timestamps must strictly increase")
    if duration is not None and any(x>=duration for x in vv):e.append("shot timestamp reaches or exceeds total duration")

def get_manifest(args):
    if args.manifest:return load_json(args.manifest)
    if args.workflow:
        ms=build_manifest_from_workflow(args.workflow)
        if not ms:raise ValueError("no MiniMaxH3ReferenceToVideo node found")
        if args.node_index>=len(ms):raise ValueError("node-index out of range")
        return ms[args.node_index]
    return None

def check_manifest(text,m,e,w):
    for x in m.get("errors",[]):e.append("manifest: "+x)
    for x in m.get("warnings",[]):w.append("manifest: "+x)
    available=flatten_labels(m)
    for kind in ("Picture","Video","Audio"):
        used=labels(text,kind);avail=set(available[kind])
        missing=sorted(used-avail)
        if missing:e.append(f"prompt references unavailable {kind} labels: {missing}; available={sorted(avail)}")
    if re.search(r"\bref_(?:video_audio|audio|video|image)_\d+\b",text,re.I):
        e.append("prompt contains ComfyUI port names; use <Picture N>/<Video N>/<Audio N> labels from the manifest")
    # Voice binding is checked by profile-specific logic. Retention analysis must not carry (Sx).
    # Adjacent Audio(Sx) is often conceptual confusion.
    if re.search(r"<Audio\s+\d+>\s*\(S\d+\)",text,re.I):
        w.append("write the target subject/voice followed by (Sx); <Audio N> is a source label, not the speaker itself")


def check_voice_binding(text,e):
    for line in text.splitlines():
        if re.search(r"<Audio\s+\d+>",line,re.I) and re.search(r"\b(?:voice|timbre|speaker|delivery|vocal)\b",line,re.I):
            if not re.search(r"\(S\d+\)",line):
                e.append(f"voice-reference line lacks target speaker binding (Sx): {line[:140]}")

def check_dialogue(text,e,w):
    if text.lower().count("<d>")!=text.lower().count("</d>"):e.append("unbalanced <d> tags")
    for m in re.finditer(r"<d>(.*?)</d>",text,re.S|re.I):
        b=m.group(1).strip();mm=re.match(r"\[([^\]]+)\]\s*(.*)",b,re.S)
        if not mm:e.append("each <d> must begin with [Language]");continue
        spoken=mm.group(2).strip()
        if not spoken:e.append("empty dialogue")
        elif spoken[-1] not in ".!?。？！":w.append("dialogue may lack terminal punctuation")
        prefix=text[max(0,m.start()-260):m.start()]
        if not re.search(r"\(S\d+(?:,S\d+)*\)",prefix):w.append("dialogue has no nearby stable speaker ID")

def check_context_ref(text,args,e,w):
    ps=positions(text,REF)
    for f,p in zip(REF,ps):
        if p<0:e.append("missing section "+f)
    if all(x>=0 for x in ps) and ps!=sorted(ps):e.append("Ref2VA sections are out of order")
    sec=sections(text,REF)
    if sec.get("detailed_description:"):
        check_shots(sec["detailed_description:"],args.duration,e,w)
        n=len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b",sec["detailed_description:"]))
        if n<350 or n>500:w.append(f"detailed_description usual generation range is 350–500 English words; found {n}")
    if re.search(r"\(S\d+\)",sec.get("retention_analysis:","")):e.append("retention_analysis must not contain speaker IDs")
    check_voice_binding(sec.get("subject_definitions:",""),e)
    summary=sec.get("summary:","")
    if summary and not re.match(r"\[(?:reference generation|keyframe completion|video editing|video continuation|audio reuse|audio reference)(?:\s*\+\s*(?:reference generation|keyframe completion|video editing|video continuation|audio reuse|audio reference))*\]",summary):
        w.append("summary lacks a recognized task-type prefix")
    # Audio label used outside definitions should be defined.
    defs=sec.get("subject_definitions:","")
    used_else=labels("\n".join(v for k,v in sec.items() if k!="subject_definitions:"),"Audio")
    defined=labels(defs,"Audio")
    if used_else-defined:e.append(f"Audio labels used but not defined in subject_definitions: {sorted(used_else-defined)}")

def validate(args,text):
    e=[];w=[]
    profile="context_ir_emulation" if args.profile=="enhanced" else args.profile
    if args.duration is not None and not 4<=args.duration<=15:e.append("target duration should be 4–15 seconds")
    if not args.allow_placeholders and (m:=PLACEHOLDER.search(text)):e.append("unfilled placeholder: "+m.group(0)[:80])
    check_dialogue(text,e,w)
    if args.mode=="ref2va":
        try:m=get_manifest(args)
        except Exception as ex:e.append("manifest error: "+str(ex));m=None
        if m:check_manifest(text,m,e,w)
        else:
            if args.pictures+args.videos+args.audios==0:e.append("Ref2VA requires --manifest/--workflow or declared asset counts")
            if args.audios and not (args.pictures or args.videos):e.append("audio cannot be the sole Ref2VA input")
            if args.pictures>9 or args.videos>3 or args.audios>3:e.append("declared Ref2VA limits exceeded")
        if profile in {"context_ir_emulation","strict_context_ir"}:check_context_ref(text,args,e,w)
        else:
            check_voice_binding(text,e)
            if not re.search(r"<(?:Subject|Picture|Video|Audio)\s+\d+>",text,re.I):w.append("direct Ref2VA prompt contains no explicit reference labels")
    else:
        if profile in {"context_ir_emulation","strict_context_ir"}:
            ps=positions(text,CORE)
            for f,p in zip(CORE,ps):
                if p<0:e.append("missing section "+f)
            if all(x>=0 for x in ps) and ps!=sorted(ps):e.append("base sections are out of order")
            sec=sections(text,CORE)
            if sec.get(CORE[0]):check_shots(sec[CORE[0]],args.duration,e,w)
        else:
            if len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b",text))<25:w.append("direct prompt may be underspecified")
    return e,w

def main()->int:
    p=argparse.ArgumentParser(description="Validate MiniMax H3 prompt v1.5")
    p.add_argument("prompt",type=Path);p.add_argument("--mode",required=True,choices=["t2va","i2va","l2va","fl2va","ref2va"])
    p.add_argument("--profile",required=True,choices=["direct","concise_structured","context_ir_emulation","strict_context_ir","enhanced"])
    p.add_argument("--duration",type=float);p.add_argument("--manifest",type=Path);p.add_argument("--workflow",type=Path);p.add_argument("--node-index",type=int,default=0)
    p.add_argument("--pictures",type=int,default=0);p.add_argument("--videos",type=int,default=0);p.add_argument("--audios",type=int,default=0)
    p.add_argument("--allow-placeholders",action="store_true");p.add_argument("--strict",action="store_true")
    args=p.parse_args();text=args.prompt.read_text(encoding="utf-8-sig")
    e,w=validate(args,text)
    for x in e:print("ERROR:",x)
    for x in w:print("WARN:",x)
    if e or (args.strict and w):return 1
    if w:return 2
    print("PASS: prompt structure and declared Ref2VA mapping are consistent")
    return 0
if __name__=="__main__":raise SystemExit(main())
