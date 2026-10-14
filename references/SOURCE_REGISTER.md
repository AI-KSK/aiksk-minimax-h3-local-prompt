# Source Register

Original syntax cross-validation: 2026-08-29
Martial LoRA source cross-check: 2026-10-13

## Primary — MiniMax official

- MiniMax H3 repository: https://github.com/MiniMax-AI/MiniMax-H3
- MiniMax H3 prompt-writing skill: https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- Base guide: https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt
- Full-reference guide: https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt

## Primary — ComfyUI official

- MiniMax H3 in ComfyUI: https://docs.comfy.org/tutorials/video/minimax/minimax-h3

## Primary — AIMixer Director

- Repository: https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director
- README_EN: https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director/blob/main/README_EN.md

## Provenance policy

1. MiniMax official Prompt Guides govern H3 grammar, field names, label semantics, dialogue syntax, retention markers, and prompt-mode structure.
2. MiniMax official repository governs model/runtime limits.
3. ComfyUI official documentation validates native node behavior and supported local workflow families.
4. AIMixer repository governs Director-specific grouping, material tags, common-prompt concatenation, source-video binding, and Director task routing.
5. AIKSK causal bridges, production locks, story routers, and repair strategies are production heuristics. They must not be presented as MiniMax official requirements.

## Primary — JOKER141 author model cards (martial add-on, checked 2026-10-13)

- Combat V2 + optional triggers: https://huggingface.co/JOKER141/MiniMax-H3-Combat-Base-V2
- Weapon Combat + BUNNY / standalone warning: https://huggingface.co/JOKER141/MiniMax-H3-Weapon-Combat-LoRA
- GunFu + BUNNY / tested first-pass recipe: https://huggingface.co/JOKER141/MiniMaxH3-GunFu-Gunfight-LORA
- Motion Repair V1/V2 + optional bunny_crisp_motion: https://huggingface.co/JOKER141/MiniMax-H3-General-Motion-Continuity-Repair
- Fight Flow + interaction-class triggers: https://huggingface.co/JOKER141/H3-Fight-Flow-Fight-Interaction-LoRA

## Primary — runtime and workflow (checked 2026-10-13)

- Veda ComfyUI and 8-step Predictor training caveat: https://github.com/veda-sparse/Veda-on-ComfyUI
- Work-Fisher reference (optional two-pass, not bundled runtime): https://huggingface.co/Work-Fisher/MiniMax-H3-Wuxia-Fight-Workflow

## Evidence classes

- Author guidance: **triggers** and specifically attributed per-model/pair weight examples.
- AIKSK experiments: the original **A0–A8** composite preset values and BASE control strategy; no RTX 4090 validation claimed.
- Runtime integration: bundled original ComfyUI JSON + offline sync utility; static tests only.
- Official MiniMax grammar remains from 2026-08-29 source packaging; official reference files are not rewritten.
