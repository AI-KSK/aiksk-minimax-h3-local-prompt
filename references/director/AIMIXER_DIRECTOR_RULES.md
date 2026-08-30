# AIMixer MiniMax H3 Director Prompt Rules — AIKSK v1.7

Validated: 2026-08-29

## 1. Fundamental rule

AIMixer `ComfyUI_MiniMaxH3_Director` is a director/orchestration layer over the official ComfyUI MiniMax H3 pipeline. It does not replace the MiniMax prompt grammar.

Therefore:

| Director task | Prompt family | Model family |
|---|---|---|
| `t2v` | Base / T2VA | fl2va |
| `i2v` | Base / I2VA | fl2va |
| `fl2v` with both endpoints | Base / FL2VA | fl2va |
| `fl2v` with first only | Base / I2VA | fl2va |
| `fl2v` with last only | Base / L2VA | fl2va |
| `r2v` | Full-reference / Ref2VA | ref2va |
| `v2v` | Full-reference / Ref2VA | ref2va |
| `rv2v` | Full-reference / Ref2VA | ref2va |

## 2. What Director material labels mean

Director R2V exposes uploaded material references as:

- `<Picture N>`
- `<Video N>`
- `<Audio N>`

Prefer the UI `@` picker whenever possible. Do not guess slot indices when common and group materials coexist.

`<Subject N>` is different. It is not a Director file slot. It is a semantic reusable subject defined inside Ref2VA `subject_definitions`.

### Plain-language model

- `<Picture 1>` = “这是一张具体照片。”
- `<Subject 1>` = “这几张照片里的这个女人，是同一个角色；以后叫她 Subject 1。”

## 3. Subject creation rule

Create a `<Subject N>` when visible content must be recognized and reused across the target video:

- same person/character across multiple images;
- same animal/creature;
- same product/prop;
- same reusable environment/style/action/pose when it genuinely needs tracking.

One Subject may be defined by several assets:

```text
<Subject 1> is the same woman whose identity and appearance are established by <Picture 1>, <Picture 2>, and <Picture 3>.
```

Do not create gratuitous Subjects for every noun. Subject labels are tracking identities, not decorative tags.

## 4. Picture creation / tracking rule

A reference image should remain an independently tracked `<Picture N>` when the image itself is a concrete target-frame or planning anchor:

- first frame;
- last frame;
- keyframe;
- edited keyframe;
- composition anchor;
- storyboard / shot-planning anchor.

If the image is used only to define a character, costume, prop, or style, cite it inside the corresponding Subject definition and do not force an extra standalone Picture definition.

## 5. Full-reference section order

For `r2v/v2v/rv2v`, use exactly:

1. `subject_definitions:`
2. `summary:`
3. `retention_analysis:`
4. `detailed_description:`
5. `overall_soundscape:`
6. `non_diegetic_music:`

## 6. Official summary task types

Use only the task types justified by actual asset roles:

- `keyframe completion`
- `reference generation`
- `video editing`
- `video continuation`
- `audio reuse`
- `audio reference`

Combine with ` + ` when necessary.

Presence alone does not create a task type. A video used only for motion/camera reference is normally `reference generation`, not `video editing`.

## 7. v2v / rv2v rule

Director binds each source-video segment as `<Video 1>`.

If directly editing it:

```text
summary:
[video editing] The target video is an edited version of <Video 1>. ...
```

If original audio is retained, include `audio reuse` only when the actual signal remains audible.

## 8. Common prompt rule

Director common prompt is concatenated with each group prompt.

### Safe default — recommended for creators

Leave common prompt empty/off and write one complete six-section prompt per material group.

This is easiest to audit and prevents duplicate/misaligned section headers.

### Advanced shared-definition mode

Use common prompt only as the beginning of `subject_definitions:` containing shared identities. Each group prompt must continue the same section with any group-specific definition lines and then proceed to `summary:`. Do not create a second `subject_definitions:` header in the group.

Example common prefix:

```text
subject_definitions:
<Subject 1> is the same heroine established by <Picture 1> and <Picture 2>.
```

Example group continuation:

```text
<Picture 3> is the composition anchor for [Shot 1].

summary:
...
```

## 9. Multi-shot story compiler

For each story, build this chain before prose:

`Identity → Reference role → Story beat → Causal bridge → Timing → Camera → Audio → Official compile`

### Causal bridge requirement

Every scene change should preserve at least one observable continuity carrier:

- body motion;
- gaze direction;
- prop contact;
- forward momentum;
- sound cue;
- camera direction;
- state change.

Example:

`pet boar → boar lifts head/snorts/leans forward → cut → chase already moving`

and:

`run away → look back → reach for chain → cut → hand completes grip and body swings onto boar`

This is an AIKSK production heuristic, not a MiniMax field-name requirement, but it is the default Director narrative strategy.

## 10. Timing rule

Plan using the user's requested duration, but compile timestamps against the **effective workflow duration** when the Director/ComfyUI frame grid snaps the requested value.

- `[Shot 1]` has no timestamp.
- `[Shot 2+]` use strictly increasing cut times.
- Do not place a cut after the effective end time.

## 11. Ref2VA detail density

For generation tasks, official guidance normally targets roughly **350–500 English words** in `detailed_description`.

Do not shorten merely because there is only one shot. For dialogue-dense content, fit the actual spoken timeline first.

## 12. Director input/runtime constraints to respect

Current H3 Ref2VA limits from the official model specification:

- Images ≤ 9
- Videos ≤ 3; each 2–15 s; total video duration ≤ 15 s
- Audio ≤ 3; each 2–15 s; total audio duration ≤ 15 s
- Total mixed input files ≤ 12
- Output duration 4–15 s
- Output 24 FPS, stereo 32 kHz audio

## 13. Final Director QA

Before returning a prompt, check:

- correct Base vs Ref2VA family;
- labels correspond to actual slots;
- no accidental Subject/Picture conflation;
- same character uses same Subject ID across shots;
- no new labels introduced after `subject_definitions`;
- official section order intact;
- retention markers match actual role;
- story beats are causally connected;
- timestamps fit duration;
- dialogue uses stable `(Sx)` and `<d>[Language]...` when present;
- soundscape and audience-only score are separated.
