---
name: aiksk-minimax-h3-local-prompt
description: "AI-KSK MiniMax H3 full-domain prompt engineering and creative production skill. Use for T2VA, I2VA, FL2VA, L2VA, Ref2VA, multimodal reference mapping, dialogue/audio/camera/timing control, production locks, prompt profiles, creative video playbooks, video editing or continuation, ads, short drama, MV, 3D animation, game intros, explainers, digital humans, action, transformation, fashion, food, documentary, POV, loops, prompt repair, and ComfyUI or RunningHub workflow-aware routing. Official MiniMax H3 prompt grammar remains the hard base; AI-KSK layers add routing, consistency, reference safety, planning, failure diagnosis, and reusable creative recipes without presenting experimental heuristics as official requirements."
---

# AI-KSK MiniMax H3 全域提示词工程与创意生产 v1.6

> This is a rebuilt v1.6 line: keep the broad 'all-domain production' positioning, but rebuild the rule hierarchy from the ground up. Official MiniMax H3 grammar is the hard base; AI-KSK adds a stronger production compiler on top.

## 0. Core principle

This skill does not merely “rewrite a prompt”. It converts user intent, assets, timing, reference relationships, shot design, audio roles, dialogue, and production goals into an H3-ready prompt package.

The operating rule is:

**Official grammar first → asset truth second → production intent third → AI-KSK enhancement fourth.**

When any AI-KSK rule conflicts with the current official H3 prompt guide, the official guide wins.

Never call an AI-KSK heuristic “official MiniMax behavior”.

---

# Layer 0 — Official H3 grammar lock

Before writing any final H3 prompt, identify the model mode and load the corresponding official reference.

## 0.1 Five official prompt modes

| Mode | Input pattern | Official guide |
|---|---|---|
| `T2VA` | text only | `references/official/base-en.txt` |
| `I2VA` | first frame + text | `references/official/base-en.txt` |
| `FL2VA` | first + last frame + text | `references/official/base-en.txt` |
| `L2VA` | last frame + text | `references/official/base-en.txt` |
| `Ref2VA` | image/video/audio references + text | `references/official/ref-en.txt` |

## 0.2 Base-mode hard structure

For T2VA/I2VA/FL2VA/L2VA, preserve the official field order:

1. keyframe alignment instruction when required;
2. `integrated_multimodal_description`;
3. `overall_soundscape`;
4. `non_diegetic_music`.

Do not rename these fields.

## 0.3 Ref2VA hard structure

For full-reference Ref2VA, preserve the official six-section order:

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

Do not invent new reference labels after `subject_definitions`.

## 0.4 Language contract

- Structural rewrite prose is English.
- Dialogue, lyrics, and visible text preserve the user's original language.
- Use stable `(S1)`, `(S2)` speaker IDs.
- Use `<d>[Language] ...</d>` for actual spoken or sung text.
- Do not translate or rewrite the user's exact dialogue unless explicitly requested.

## 0.5 Runtime facts that must not be contradicted

Treat these as current H3 boundaries unless the bundled source register is updated:

- output duration: 4–15 seconds;
- output frame rate: 24 FPS;
- output audio: stereo 32 kHz;
- H3-Base output target: 768p-class local base generation;
- Ref2VA supports up to 9 images, 3 videos, 3 audios, with mixed-file limits controlled by the runtime/model spec;
- official H3-Context-IR and H3-Regenerate-2K are not equivalent to this local prompt skill.

Do not impose a fake universal 10-second ceiling.

---

# Layer 1 — Task router

Route by **what the user wants to preserve, create, or change**, not merely by how many files are attached.

## 1.1 Fast router

- No visual/audio references → `T2VA`.
- One image explicitly used as first frame → `I2VA`.
- One image explicitly used as final frame → `L2VA`.
- Two images explicitly used as first + last frame → `FL2VA`.
- Any image/video/audio used as reusable identity/style/motion/audio/source-edit reference → `Ref2VA`.
- If one workflow mixes keyframes and omni-references, respect the actual connected workflow first and use a hybrid routing note rather than silently pretending all inputs are native Ref2VA or all are keyframes.

## 1.2 Intent classes

Every request should also be tagged internally with one or more intent classes:

- `GEN` — generation from scratch;
- `CONT` — continuation;
- `EDIT` — edit an existing video;
- `IDENTITY` — preserve person/character identity;
- `STYLE` — transfer visual style;
- `MOTION` — borrow motion/camera/rhythm;
- `AUDIO_REF` — voice/music/audio reference;
- `AUDIO_REUSE` — copy/reuse source audio;
- `KEYFRAME_PATH` — connect explicit start/end states;
- `DIALOGUE` — spoken lines;
- `MUSIC` — score/lyrics/beat-led creation;
- `PRODUCT` — product/brand objective;
- `NARRATIVE` — story/short-film objective;
- `EXPLAINER` — education/knowledge objective.

These classes guide the AI-KSK layer but never replace official output fields.

---

# Layer 2 — Prompt compiler

Use this sequence for every non-trivial request.

## STEP 1 — Extract immutable user requirements

Create an internal constraint set:

- subject identity;
- wardrobe / hairstyle / age / species;
- product geometry / logo / packaging;
- scene / location;
- requested action;
- camera requirement;
- duration;
- aspect ratio if relevant to framing;
- dialogue / lyrics / narration exact wording;
- audio role;
- beginning state;
- ending state;
- forbidden changes.

Never improve away a user's hard constraint.

## STEP 2 — Build an asset map

For each input asset, determine:

- asset type: image / video / audio;
- role: keyframe / subject reference / environment reference / source video / motion reference / voice reference / music reference / reusable soundtrack;
- whether it must be copied, preserved, transferred, weakly referenced, or only used as inspiration;
- whether the user expects pixel/frame identity or semantic identity.

## STEP 3 — Build continuity locks

Use only locks that matter to the task:

- identity lock;
- wardrobe lock;
- face/hair lock;
- body/proportion lock;
- prop lock;
- environment lock;
- composition lock;
- product geometry lock;
- logo/text lock;
- motion-direction lock;
- camera-axis lock;
- lighting lock;
- voice-timbre lock;
- dialogue-content lock;
- music-rhythm lock;
- source-audio reuse lock.

Do not overload prompts with every possible lock.

## STEP 4 — Build the timeline

For each shot/continuous segment specify only useful information:

- composition;
- subject position;
- visible state;
- action and state change;
- camera movement;
- sound event;
- dialogue/lyrics if any;
- exact reference appearance point;
- transition to the next state.

Prefer observable state changes over vague plot language.

## STEP 5 — Compile into official grammar

- Base mode → compile into official three-field structure.
- Ref2VA → compile into official six-section structure.

## STEP 6 — Validate

Before final output, check:

- no unresolved reference labels;
- no label renumbering midway;
- no contradictory beginning/end state;
- no impossible cut times;
- no speaker-ID drift;
- no accidental copying of reference dialogue when only voice timbre was requested;
- no unsupported claim disguised as an official feature.

---

# Layer 3 — Ref2VA reference engine

Ref2VA is where most local prompt failures occur. Build the reference graph before writing prose.

## 3.1 Reference label roles

Use official label semantics:

- `<Subject N>` — reusable visible subject/content;
- `<Picture N>` — concrete image/frame anchor;
- `<Video N>` — whole-video source/edit/continuation/temporal reference;
- `<Audio N>` — audio signal that is copied or referenced.

## 3.2 Visual relationship markers

Use only official-compatible meanings in `retention_analysis`:

- `fully_preserved`
- `partially_preserved`
- `attribute_transfer`
- `weak_reference`

## 3.3 Audio relationship markers

Use only official-compatible meanings:

- `fully_copy`
- `partially_copy`
- `reference`
- `weak_reference`

## 3.4 Critical distinction: `<Audio N>` vs `(Sx)`

- `<Audio N>` identifies a referenced signal/source asset.
- `(Sx)` identifies the target video's actual speaker/vocal source.
- A voice reference can be `<Audio 1>` while the target speaker is `<Subject 2> (S1)`.
- If the source audio is only a timbre/delivery reference, do not copy source words.
- If audio is directly reused, describe reuse accurately rather than calling it a voice reference.

## 3.5 Multi-reference priority

When multiple references conflict, resolve in this order unless the user explicitly states otherwise:

1. exact source/edit relationship;
2. explicit identity reference;
3. explicit keyframe/frame anchor;
4. explicit motion/camera reference;
5. explicit wardrobe/prop/environment reference;
6. general style reference;
7. weak atmosphere reference.

If two equal-priority references contradict each other, ask or clearly state the chosen interpretation.

---

# Layer 4 — Camera, action, timing, dialogue, audio

## 4.1 Camera grammar

Describe camera motion as a combination of:

- motion type;
- amplitude when meaningful;
- speed when meaningful.

Useful families:

- static / locked-off;
- push in / pull out;
- truck left/right;
- pan / tilt;
- orbit / arc;
- crane / jib;
- handheld follow;
- shoulder-level chase;
- dolly zoom when genuinely intended;
- overhead / top-down move;
- POV/body-mounted movement;
- rack focus / focus pull when the focal change matters.

Do not stack five camera movements into a 5-second shot.

## 4.2 Action grammar

Prefer a state-transition chain:

`initial state → trigger → physical action → visible intermediate state → final state`

For complex action, decompose joint/prop interactions instead of saying “fights intensely” or “moves naturally”.

## 4.3 Dialogue grammar

For each vocal source:

- stable speaker ID;
- visible/off-screen/narrator role;
- exact dialogue in `<d>`;
- emotional/delivery cue only when useful;
- physical action synchronized with speech when relevant.

For Chinese dialogue:

`<d>[Chinese] 原台词。</d>`

Preserve wording unless rewrite is explicitly requested.

## 4.4 Audio grammar

Keep four layers conceptually separate:

1. dialogue / singing;
2. diegetic ambience;
3. physical sound effects;
4. non-diegetic music.

Do not repeat full dialogue inside `overall_soundscape`.

## 4.5 Timing strategy

- Match actual workflow duration.
- `[Shot 1]` has no cut timestamp.
- Later cuts use strictly increasing times.
- FL2VA generally benefits from a continuous single-shot path unless cuts are explicitly useful.
- Dialogue-dense clips may be split at natural pauses as a quality strategy, but this is not an official hard rule.

---

# Layer 5 — Production locks

Use locks sparingly and with explicit purpose.

## 5.1 Identity lock

Use when a character must remain the same across angle/action changes:

- preserve face identity;
- preserve hairstyle and hair color;
- preserve age and major facial proportions;
- preserve body silhouette unless transformation is requested;
- do not duplicate the subject.

## 5.2 Costume / product lock

For fashion/product work:

- preserve garment cut, material, pattern, logo location, accessories;
- preserve product silhouette, dimensions, surface finish, label placement;
- describe allowed changes separately from forbidden changes.

## 5.3 Composition lock

Use when editing or continuing a source:

- preserve camera height;
- preserve subject screen position;
- preserve horizon / major background geometry;
- only change the requested region/state.

## 5.4 Motion lock

When using a motion reference:

- preserve action timing and broad trajectory;
- do not blindly copy source identity or environment unless requested;
- identify whether camera motion or body motion is the true target.

## 5.5 Audio lock

State whether the target must:

- copy audio;
- preserve timing only;
- preserve voice timbre only;
- preserve music rhythm only;
- replace dialogue while keeping vocal identity;
- retain ambience while replacing music.

---

# Layer 6 — Full-domain prompt playbook router

The official MiniMax skill set includes one general H3 prompt-writing skill plus eight style-specific video skills. This AI-KSK rebuild keeps those classes but expands the catalog into a broader production router.

Read `references/playbooks/use-case-catalog.md` for the detailed recipes.

## 6.1 Narrative / cinematic

1. Cinematic short film
2. Chinese micro-drama / short dialogue scene
3. Suspense / horror beat
4. Comedy reaction scene
5. Romance / emotional close-up
6. Documentary / observational shot
7. POV / first-person sequence
8. Action / fight choreography
9. Transformation / creature / fantasy VFX
10. Dance / performance / sports motion

## 6.2 Commercial / social

11. Minimalist product ad
12. Brand promo / launch film
13. Beauty / fashion showcase
14. Food / cooking commercial
15. Tech / device / UI showcase
16. E-commerce talking product demo
17. Architecture / travel / hotel promo

## 6.3 Stylized / animation

18. 3D animation short
19. Hand-drawn + live-action fusion
20. Papercraft stop-motion explainer
21. Paper collage explainer
22. Clay / miniature / toy-world sequence
23. Anime / 2D stylized shot
24. Game intro / character menu / UI animation

## 6.4 Audio-led

25. MV / lyric visual
26. Singing performance
27. Voice-reference digital human
28. Two-person dialogue
29. Narration-led explainer
30. Sound-design-led atmospheric clip

## 6.5 Reference-heavy / editing

31. Character identity reference generation
32. Multi-image identity + costume composition
33. Environment transfer
34. Motion/camera reference transfer
35. Source-video edit
36. Source-video continuation
37. Audio replacement / voice-reference edit
38. BGM reuse / rhythm reference
39. First-frame continuation
40. First-to-last-frame controlled transition
41. Last-frame landing
42. Loop-like ending / return-to-start planning

## 6.6 Utility prompts

43. Prompt compression
44. Prompt expansion
45. Prompt repair after a failed generation
46. Reference-map repair
47. Dialogue timing repair
48. Camera simplification
49. Identity-drift repair
50. Product-geometry repair

---

# Layer 7 — Output profiles

The skill supports multiple output profiles. These are AI-KSK profiles, not official MiniMax modes.

## 7.1 `official_full` — default high-quality profile

- Keep official field grammar exactly.
- Rich shot-by-shot detail.
- Strongest for final production.

## 7.2 `official_compact`

- Same official grammar.
- Remove redundant adjectives and repeated visual facts.
- Keep action, camera, timing, references, dialogue, and audio intact.

## 7.3 `director`

- Official grammar plus stronger cinematic blocking, performance, lens/composition intent, and sound design.
- Use only when the user asks for cinematic/directorial enhancement.

## 7.4 `identity_lock`

- Official grammar plus explicit identity/wardrobe/prop continuity constraints.
- Best for character reference generation and multi-angle sequences.

## 7.5 `edit_lock`

- Ref2VA only.
- Minimize unintended changes to source-video structure, composition, identity, lighting, and timing.
- Explicitly isolate requested edits.

## 7.6 `motion_reference`

- Ref2VA only.
- Prioritize body/camera/rhythm transfer while separating source identity/environment unless requested.

## 7.7 `audio_control`

- Prioritize voice/music/sound relationships and speaker-role correctness.

## 7.8 `creative_max`

- AI-KSK high-creativity profile.
- May enrich staging, sound, props, camera and transitions while remaining inside the user's intent.
- Never invent product claims, factual claims, logos, or copyrighted dialogue.

---

# Layer 8 — Prompt repair engine

When a user provides a failed result, diagnose before rewriting.

## 8.1 Identity drift

Likely causes:

- identity anchor described only once;
- too many unrelated style changes;
- reference role unclear;
- action overwhelms identity constraints.

Repair:

- strengthen first appearance anchor;
- reuse the same `<Subject N>`;
- reduce non-essential transformations;
- isolate allowed vs forbidden changes.

## 8.2 Action too weak

Repair:

- replace abstract verbs with physical state changes;
- state direction, contact, reaction and endpoint;
- simplify camera if camera motion competes with body motion.

## 8.3 Camera chaos

Repair:

- one dominant move per shot;
- remove redundant pans/orbits/zooms;
- convert minor reframing to a single push/truck rather than a cut.

## 8.4 Dialogue cut off / rushed

Repair:

- reduce visual complexity during speech;
- shorten or split dialogue only with permission if wording must change;
- move cuts to natural pauses;
- use continuity tags only when they match the actual intended behavior.

## 8.5 Audio mismatch

Repair:

- separate `<Audio N>` reference identity from `(Sx)` speaker identity;
- state reference vs copy explicitly;
- keep dialogue out of soundscape/music sections.

## 8.6 Product deformation

Repair:

- promote product geometry/material/logo placement to immutable constraints;
- reduce aggressive camera distortion;
- reduce transformation/effects touching the product itself.

## 8.7 First/last frame mismatch

Repair:

- describe intermediate state changes instead of re-describing both endpoint images;
- eliminate unnecessary cuts;
- ensure final action logically lands on the last image.

---

# Layer 9 — RunningHub / ComfyUI operating rules

This skill can be used with local ComfyUI or RunningHub, but prompt syntax and workflow wiring are separate layers.

## 9.1 When workflow JSON is available

Inspect the actual connected assets before assigning reference labels.

Do not infer numbering only from visible node names if custom nodes reorder inputs.

## 9.2 When workflow JSON is not available

Ask for a simple asset manifest or use the user's explicit mapping:

```text
Picture 1 = ...
Video 1 = ...
Audio 1 = ...
```

Then compile the prompt.

## 9.3 Hybrid workflows

If a RunningHub/ComfyUI custom workflow combines first/last-frame conditioning with Ref2VA references, keep two conceptual layers:

- keyframe alignment;
- omni-reference relationships.

Do not collapse them into one label system unless the actual custom node implementation does so.

---

# Layer 10 — Response modes

## User asks only for prompt

Return only the final copyable H3 prompt.

## User asks for workflow engineering output

Return:

```text
Mode:
Intent classes:
Profile:
Duration:
Asset map:
Reference map:
Locks:
Final prompt:
Validation / risks:
```

## User asks for multiple variants

Default variants:

1. `official_full`
2. `official_compact`
3. one task-specific profile (`director`, `identity_lock`, `edit_lock`, `motion_reference`, or `audio_control`)

Do not generate meaningless stylistic variants that differ only by adjectives.

---

# Layer 11 — Evidence boundaries

The following are official-grounded and may be stated as such when the bundled official guides support them:

- five prompt modes;
- base three-field structure;
- Ref2VA six-section structure;
- reference-label semantics;
- official visual/audio retention markers;
- speaker and dialogue formatting;
- shot/cut notation;
- camera-motion guidance;
- current H3 runtime specs recorded in the source register.

The following are AI-KSK production heuristics and must be labeled internally as such:

- prompt profiles;
- lock hierarchy;
- multi-reference conflict priority;
- production playbooks;
- failure-repair rules;
- dialogue-density splitting strategy;
- product / identity / action repair recipes.

The following must never be falsely claimed:

- that this skill reproduces official H3-Context-IR exactly;
- that local prompt rewriting equals H3-Regenerate-2K;
- that an experimental community LoRA or custom node is an official MiniMax feature;
- that unseen source media contains specific details.

---

# Layer 12 — Associated files

Core official references:

- `references/official/base-en.txt`
- `references/official/ref-en.txt`

AI-KSK production references:

- `references/playbooks/use-case-catalog.md`
- `references/playbooks/ref2va-reference-recipes.md`
- `references/playbooks/dialogue-audio-recipes.md`
- `references/playbooks/camera-action-recipes.md`
- `references/playbooks/failure-repair-matrix.md`
- `references/CROSS_VALIDATION.md`
- `references/SOURCE_REGISTER.md`

Templates:

- `templates/t2va_master.txt`
- `templates/i2va_master.txt`
- `templates/fl2va_master.txt`
- `templates/l2va_master.txt`
- `templates/ref2va_master.txt`

---

# Layer 13 — Trigger phrases

Use this skill when the request mentions or implies:

- MiniMax H3 prompt / 提示词 / Prompt;
- T2VA / I2VA / FL2VA / L2VA / Ref2VA;
- 文生视频 / 图生视频 / 首尾帧 / 尾帧 / 参考生视频;
- 参考图 / 参考视频 / 参考音频 / 声音参考;
- 视频编辑 / 续写 / 人物一致性 / 动作参考;
- 镜头设计 / 运镜 / 分镜 / 音效 / 对白 / 歌词 / MV;
- 产品广告 / 品牌片 / 3D 动画 / 游戏开场 / 纸艺 / 拼贴;
- AI 短剧 / 数字人 / 双人对话 / 打斗 / 变身 / 舞蹈;
- H3 Prompt 修复 / 重写 / 压缩 / 扩写 / 诊断。
