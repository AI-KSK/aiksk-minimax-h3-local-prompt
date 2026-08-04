#!/usr/bin/env python3
"""Reference-label mapping for ComfyUI MiniMax H3 Ref2VA workflows.

Standard library only. Mirrors the relevant ordering in official
MiniMaxH3ReferenceToVideo.execute: images; for each video, paired soundtrack
is presented before the video; standalone audios are presented last.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

REF_NODE_TYPE = "MiniMaxH3ReferenceToVideo"


def load_json(path: str | Path) -> Any:
    p = Path(path)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return json.loads(p.read_text(encoding="utf-8-sig"))


def iter_nodes(obj: Any) -> Iterable[dict[str, Any]]:
    if isinstance(obj, dict):
        if isinstance(obj.get("type"), str) and "id" in obj:
            yield obj
        for value in obj.values():
            yield from iter_nodes(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_nodes(value)


def is_connected(inp: dict[str, Any]) -> bool:
    link = inp.get("link")
    if isinstance(link, list):
        return bool(link)
    return link is not None


def suffix(name: str) -> int | None:
    m = re.search(r"_(\d+)$", name)
    return int(m.group(1)) if m else None


def relevant_inputs(node: dict[str, Any], prefix: str) -> list[dict[str, Any]]:
    result=[]
    for inp in node.get("inputs", []) or []:
        name=str(inp.get("name", ""))
        if name.startswith(prefix):
            result.append(inp)
    return result


def build_manifest_from_node(node: dict[str, Any], workflow_path: str | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    ignored: list[dict[str, Any]] = []

    image_inputs = relevant_inputs(node, "ref_images.ref_image_")
    video_inputs = relevant_inputs(node, "ref_videos.ref_video_")
    soundtrack_inputs = relevant_inputs(node, "ref_video_audios.ref_video_audio_")
    standalone_inputs = relevant_inputs(node, "ref_audios.ref_audio_")

    connected_images=[x for x in image_inputs if is_connected(x)]
    connected_videos=[x for x in video_inputs if is_connected(x)]
    soundtrack_by_suffix={suffix(str(x.get("name"))):x for x in soundtrack_inputs}
    connected_standalone=[x for x in standalone_inputs if is_connected(x)]

    pictures=[]
    for idx, inp in enumerate(connected_images, 1):
        pictures.append({
            "label": f"<Picture {idx}>",
            "port": inp.get("name"),
            "port_suffix": suffix(str(inp.get("name"))),
            "link": inp.get("link"),
            "kind": "reference_image",
        })

    videos=[]
    audios=[]
    audio_idx=0
    video_idx=0
    connected_video_suffixes=set()
    for vinp in connected_videos:
        vs=suffix(str(vinp.get("name")))
        connected_video_suffixes.add(vs)
        sinp=soundtrack_by_suffix.get(vs)
        paired_audio_label=None
        if sinp is not None and is_connected(sinp):
            audio_idx += 1
            paired_audio_label=f"<Audio {audio_idx}>"
            audios.append({
                "label": paired_audio_label,
                "port": sinp.get("name"),
                "port_suffix": vs,
                "link": sinp.get("link"),
                "kind": "video_soundtrack",
                "paired_video_port": vinp.get("name"),
                "paired_video_label": None,
            })
        video_idx += 1
        video_label=f"<Video {video_idx}>"
        videos.append({
            "label": video_label,
            "port": vinp.get("name"),
            "port_suffix": vs,
            "link": vinp.get("link"),
            "kind": "reference_video",
            "paired_audio_label": paired_audio_label,
        })
        if paired_audio_label:
            audios[-1]["paired_video_label"] = video_label

    for sinp in soundtrack_inputs:
        ss=suffix(str(sinp.get("name")))
        if is_connected(sinp) and ss not in connected_video_suffixes:
            errors.append(
                f"{sinp.get('name')} is connected but the same-numbered ref_video_{ss} is not connected; "
                "official ComfyUI will not register this soundtrack as <Audio N>."
            )
            ignored.append({"port":sinp.get("name"),"link":sinp.get("link"),"reason":"missing_same_numbered_video"})

    for ainp in connected_standalone:
        audio_idx += 1
        audios.append({
            "label": f"<Audio {audio_idx}>",
            "port": ainp.get("name"),
            "port_suffix": suffix(str(ainp.get("name"))),
            "link": ainp.get("link"),
            "kind": "standalone_audio",
        })

    if not pictures and not videos and audios:
        errors.append("Ref2VA audio cannot be the sole input under the official model specification.")
    if not pictures and not videos and not audios:
        errors.append("No connected Ref2VA reference assets were found.")
    if len(pictures)>9: errors.append("More than 9 reference images are connected.")
    if len(videos)>3: errors.append("More than 3 reference videos are connected.")
    if len(audios)>3:
        errors.append(
            f"{len(audios)} audio signals are registered (paired soundtracks + standalone audio), "
            "exceeding the official Ref2VA audio limit of 3."
        )

    # File count is ambiguous for video + extracted soundtrack. Report both views.
    raw_connections=len(pictures)+len(videos)+len(audios)
    logical_source_files=len(pictures)+len(videos)+sum(1 for x in audios if x["kind"]=="standalone_audio")
    if logical_source_files>12:
        errors.append("Logical source-file count exceeds the official mixed-input limit of 12.")
    if raw_connections>12:
        warnings.append(
            "Connected reference streams exceed 12 when video soundtracks are counted separately; "
            "verify how the upstream loader derives soundtrack streams from source files."
        )

    return {
        "schema_version":"1.4",
        "workflow_family":"official_comfy_native",
        "workflow_path":workflow_path,
        "node_id":node.get("id"),
        "node_type":node.get("type"),
        "pictures":pictures,
        "videos":videos,
        "audios":audios,
        "ignored":ignored,
        "counts":{
            "pictures":len(pictures),
            "videos":len(videos),
            "video_soundtracks":sum(x["kind"]=="video_soundtrack" for x in audios),
            "standalone_audios":sum(x["kind"]=="standalone_audio" for x in audios),
            "audio_signals":len(audios),
            "logical_source_files":logical_source_files,
            "connected_reference_streams":raw_connections,
        },
        "errors":errors,
        "warnings":warnings,
    }


def build_manifest_from_workflow(path: str | Path) -> list[dict[str, Any]]:
    data=load_json(path)
    nodes=[n for n in iter_nodes(data) if n.get("type")==REF_NODE_TYPE]
    return [build_manifest_from_node(n, str(path)) for n in nodes]


def build_manifest_from_manual(data: dict[str, Any]) -> dict[str, Any]:
    c=data.get("connected", data)
    def vals(key):
        x=c.get(key, [])
        return [int(v) for v in x]
    inputs=[]
    link=1
    for idx in vals("ref_images"):
        inputs.append({"name":f"ref_images.ref_image_{idx}","link":link}); link+=1
    for idx in vals("ref_videos"):
        inputs.append({"name":f"ref_videos.ref_video_{idx}","link":link}); link+=1
    for idx in vals("ref_video_audios"):
        inputs.append({"name":f"ref_video_audios.ref_video_audio_{idx}","link":link}); link+=1
    for idx in vals("ref_audios"):
        inputs.append({"name":f"ref_audios.ref_audio_{idx}","link":link}); link+=1
    node={"id":"manual","type":REF_NODE_TYPE,"inputs":inputs}
    m=build_manifest_from_node(node, None)
    m["workflow_family"]="manual_config"
    return m


def flatten_labels(manifest: dict[str, Any]) -> dict[str, dict[int, dict[str, Any]]]:
    out={"Picture":{},"Video":{},"Audio":{}}
    for key,label_type in (("pictures","Picture"),("videos","Video"),("audios","Audio")):
        for item in manifest.get(key,[]):
            m=re.match(rf"<{label_type}\s+(\d+)>", item.get("label", ""))
            if m: out[label_type][int(m.group(1))]=item
    return out


def render_mapping(manifest: dict[str, Any]) -> str:
    lines=[]
    for key in ("pictures","videos","audios"):
        for item in manifest.get(key,[]):
            detail=f"{item['label']} = {item['port']}"
            if item.get("kind")=="video_soundtrack":
                detail += f" (paired with {item.get('paired_video_label')})"
            lines.append(detail)
    for x in manifest.get("ignored",[]):
        lines.append(f"IGNORED = {x.get('port')} ({x.get('reason')})")
    return "\n".join(lines)
