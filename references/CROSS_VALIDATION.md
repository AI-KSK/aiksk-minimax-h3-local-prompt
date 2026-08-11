# Cross Validation — 2026-08-11

## Official sources checked

1. MiniMax H3 official repository
   - https://github.com/MiniMax-AI/MiniMax-H3
2. Official base prompt guide
   - https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md
3. Official Ref2VA prompt guide
   - https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md
4. Official H3 skills directory
   - https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills

## Confirmed official grammar

- Five modes: T2VA, I2VA, FL2VA, L2VA, Ref2VA.
- Base modes use keyframe instruction when applicable + three core fields.
- Ref2VA uses six sections in fixed order.
- Structural prose is English; dialogue/lyrics/visible text preserve original language.
- Stable speaker IDs and `<d>[Language] ...</d>` are used for vocal content.
- Ref2VA uses `<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>` labels.
- Visual retention markers: fully_preserved / partially_preserved / attribute_transfer / weak_reference.
- Audio markers: fully_copy / partially_copy / reference / weak_reference.

## Confirmed current H3 runtime facts

From the official H3 repository at validation time:

- output duration: 4–15 seconds;
- output frame rate: 24 FPS;
- audio output: stereo 32 kHz;
- shorter side is 768 px by default for base output; 2K is associated with H3-Regenerate-2K;
- Ref2VA: up to 9 images, 3 videos, 3 audio clips; source video/audio duration and mixed-file limits follow official model specification;
- H3-Context-IR is a hosted preprocessing/orchestration system and is not part of the open-source H3-Base release.

## Official style-skill coverage checked

The official H3 skills directory currently lists one general prompt-writing skill and eight style-specific skills, including:

- 3D animation short;
- brand promo;
- co-op game intro;
- hand-drawn live video;
- minimalist product ad;
- music-video subtitle;
- paper collage explainer;
- papercraft stop-motion explainer.

AI-KSK v1.6 rebuild incorporates these categories into a broader use-case router, but its additional categories are AI-KSK production recipes, not official MiniMax skills.

## What AI-KSK intentionally adds beyond official prompt writing

- intent classifier;
- continuity locks;
- reference conflict priority;
- 50-use-case production router;
- prompt profiles;
- prompt repair engine;
- product/identity/dialogue/action-specific recipes;
- RunningHub/ComfyUI workflow-awareness.

These additions are production heuristics. They do not override official field names or label semantics.
