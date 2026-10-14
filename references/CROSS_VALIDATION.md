# Cross Validation — 2026-08-29

This v1.7 package was validated against four independent primary documentation layers.

## Validation A — MiniMax official Base Prompt Guide

Confirmed:

- T2VA begins directly with the three core fields.
- I2VA uses the official first-frame instruction before the three core fields.
- FL2VA uses the official first/last-frame alignment instruction.
- L2VA uses the official final-frame alignment instruction.
- Base core fields remain `integrated_multimodal_description`, `overall_soundscape`, `non_diegetic_music`.
- `[Shot 1]` has no cut timestamp; later shots use strictly increasing timestamps.
- Speaker IDs remain stable; dialogue uses `<d>[Language] ...</d>`.

Source: MiniMax-AI/MiniMax-H3 `skills/h3-prompt-writing/references/base-en.txt`.

## Validation B — MiniMax official Full-reference Prompt Guide

Confirmed:

- Six sections in fixed order: `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`.
- Four reference label types: `<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>`.
- A Subject can be defined by multiple reference assets.
- An image used only to define character/scene/costume/style should be cited inside a Subject rather than forced into a standalone Picture definition.
- Standalone Picture is appropriate for first/key/last/edited frame, composition anchor, or storyboard role.
- Official summary task types: keyframe completion, reference generation, video editing, video continuation, audio reuse, audio reference.
- Visual retention markers: fully_preserved, partially_preserved, attribute_transfer, weak_reference.
- Audio markers: fully_copy, partially_copy, reference, weak_reference.
- Full-reference `detailed_description` establishes overall style in 1–2 English sentences before `[Shot 1]`.
- Generation tasks normally target approximately 350–500 English words in `detailed_description`.

Source: MiniMax-AI/MiniMax-H3 `skills/h3-prompt-writing/references/ref-en.txt`.

## Validation C — MiniMax + ComfyUI runtime/workflow documentation

Confirmed:

- H3 supports multimodal text/image/video/audio context and native stereo audio.
- Output duration 4–15 seconds; 24 FPS; stereo 32 kHz.
- Ref2VA limits: images ≤9; videos ≤3, each 2–15s, total ≤15s; audio ≤3, each 2–15s, total ≤15s; mixed files ≤12.
- ComfyUI natively supports T2V/I2V/R2V and additional first/last/reference workflows through native H3 nodes.
- ComfyUI duration is subject to H3 frame-grid behavior; therefore prompt timestamps should follow the effective workflow duration when exact snapping matters.

Sources: MiniMax H3 repository + ComfyUI official MiniMax H3 tutorial.

## Validation D — AIMixer Director official repository

Confirmed:

- Director wraps the official ComfyUI H3 image/reference conditioning + sampler pipeline.
- Director tasks: t2v, i2v, fl2v, r2v, v2v, rv2v.
- t2v/i2v/fl2v use fl2va; r2v/v2v/rv2v use ref2va.
- R2V material prompts use `<Picture N>` / `<Video N>` / `<Audio N>` and support `@` picker.
- Common prompt is concatenated with each group prompt.
- v2v/rv2v source segment is automatically bound as `<Video 1>`.
- Director's common prompt documentation explicitly mentions character lock / `subject_definitions`, supporting the separation between uploaded material tags and semantic Subject definitions.

Source: AIMixer/ComfyUI_MiniMaxH3_Director README_EN.

## Result

No primary-source conflict was found that requires a Director-specific replacement grammar.

Therefore v1.7 uses this hierarchy:

**MiniMax official grammar → actual Director material mapping → user intent → AIKSK production heuristics.**


## 2026-10-13 — Fight-addon external source cross-check (v1.8.1)

### Independent axes

1. **Official prompt grammar:** protected original MiniMax Base/Ref text stays byte-identical; no LoRA/Veda keys promoted into official H3 fields.
2. **Author LoRA statements:** five JOKER141 model cards checked for triggers, use context, stacking warnings. Combat default no trigger, optional `prfight2` / `prfin1`; Weapon/GunFu `BUNNY`; Motion optional `bunny_crisp_motion`; Fight Flow selects exactly one interaction-class phrase. Reference register includes primary URLs.
3. **Workflow engineering:** A0–A8 remain the nine numbered presets; BASE sets five manual weights to zero (without disabling Turbo or Veda). Offline exporter uses actual JSON node IDs and includes smoke tests for A4, A7, R2VA and BASE; node validity is still **not** a GPU inference validation.

### Discrepancies corrected

- Added prompt-strategy mapping and trigger selection; never use unarmed prompt with Weapon/GunFu preset.
- Added independent BASE control and non-overwriting exporter.
- Documented 4-step R2VA Veda outside main 8-step training conditions.
- Explicit limitation: ComfyUI runtime preset control **does not** automatically recompile prompt text. Rerun exporter after changing recipe.
- Original official-source validation date was 2026-08-29; source **rechecked for martials** on 2026-10-13 without claiming all upstream guides were byte-for-byte current.

### Verification scope

Zip content/hashes, official unchanged files, prompt grammar, 9 presets plus BASE, source references, sync script and bundled JSON structure validated locally. No MiniMax, ComfyUI, Veda, or GPU inference was executed.
