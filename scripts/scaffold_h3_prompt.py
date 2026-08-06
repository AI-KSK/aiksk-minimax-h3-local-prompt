#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from h3_refmap import load_json, render_mapping

def manifest_defs(m):
    lines=[]
    for p in m.get("pictures",[]): lines.append(f"{p['label']} is [FRAME OR COMPOSITION ROLE, only if independently tracked].")
    for v in m.get("videos",[]): lines.append(f"{v['label']} is [VIDEO SOURCE / MOTION / CAMERA / TEMPORAL STRUCTURE ROLE].")
    for a in m.get("audios",[]):
        if a.get("kind")=="video_soundtrack": lines.append(f"{a['label']} is the synchronized soundtrack paired with {a.get('paired_video_label')}, used for [COPY OR REFERENCE ROLE].")
        else: lines.append(f"{a['label']} is the standalone audio reference for [VOICE / MUSIC / SFX ROLE] and is bound to [TARGET OR Sx].")
    lines.insert(0,"<Subject 1> is [TARGET SUBJECT] defined by [ASSIGNED PICTURE/VIDEO SOURCES].")
    return "\n".join(lines)

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=["t2va","i2va","l2va","fl2va","ref2va"],required=True)
    p.add_argument("--profile",choices=["direct","concise_structured","context_ir_emulation","strict_context_ir","enhanced"],default="direct")
    p.add_argument("--duration",type=float,default=5)
    p.add_argument("--manifest",type=Path)
    p.add_argument("--mapping-only",action="store_true")
    args=p.parse_args()
    profile="context_ir_emulation" if args.profile=="enhanced" else args.profile
    m=load_json(args.manifest) if args.manifest else None
    if args.mode=="ref2va" and not m:
        p.error("Ref2VA requires --manifest in v1.5 so labels are never guessed")
    if m:
        print("# MATERIAL LABEL MAP\n"+render_mapping(m)+"\n")
        if args.mapping_only:return 0
    d=args.duration
    if args.mode=="ref2va":
        if profile=="direct":
            print("Use [PICTURE LABELS] only for [IDENTITY / COSTUME / SCENE ROLES]. Use [VIDEO LABELS] only for [MOTION / CAMERA / TEMPORAL ROLES], while excluding source identity, clothing, body shape, and background unless explicitly requested. Use [AUDIO LABELS] according to the mapping above, distinguishing synchronized soundtrack roles from standalone voice or music roles. Bind any voice reference to the correct <Subject N> (Sx). Create a clear %.2f-second target video with [SHOT, ACTION, CAMERA, DIALOGUE, PHYSICAL SOUND, AMBIENCE, MUSIC, CONTINUITY, EXCLUSIONS]."%d)
        elif profile=="concise_structured":
            print(f"[0.00s–{d/2:.2f}s] [OPENING, SUBJECTS, REFERENCE ROLES, ACTION, CAMERA, AUDIO]\n[{d/2:.2f}s–{d:.2f}s] [CONTINUATION, END STATE, AUDIO AND CONTINUITY]\nReference constraints: [ROLE ISOLATION AND EXCLUSIONS]")
        else:
            print("subject_definitions:\n"+manifest_defs(m)+"\n\nsummary:\n[reference generation / keyframe completion / video editing / video continuation / audio reuse / audio reference] [TARGET AND MAIN RELATIONSHIPS].\n\nretention_analysis:\n[ONE LINE PER TRACKED LABEL USING VALID MARKERS].\n\ndetailed_description:\n[STYLE].\n[Shot 1] [COMPOSITION, SUBJECT, ACTION, CAMERA, SOUND, REFERENCES].\n[Shot 2] At 00:02.500, [CONTINUATION].\n\noverall_soundscape:\n[AMBIENCE AND PHYSICAL SOUNDS].\n\nnon_diegetic_music:\n[N/A OR AUDIENCE-ONLY SCORE].")
        return 0
    anchors={
        "t2va":"Create a %.2f-second [STYLE] video: [SCENE, ACTION PATH, CAMERA, AUDIO, CONSTRAINTS]."%d,
        "i2va":"Start exactly from the supplied first frame and develop [ACTION] over %.2f seconds; preserve [ANCHORS]. [CAMERA, AUDIO, END STATE]."%d,
        "l2va":"Build a plausible preceding action and land exactly on the supplied last frame at %.2f seconds. [ACTION, CAMERA, AUDIO, CONTINUITY]."%d,
        "fl2va":"Start from the supplied first frame and continuously transition to the supplied last frame at %.2f seconds. [INTERMEDIATE PATH, CAMERA, AUDIO, CONTINUITY]."%d,
    }
    print(anchors[args.mode])
    return 0
if __name__=="__main__": raise SystemExit(main())
