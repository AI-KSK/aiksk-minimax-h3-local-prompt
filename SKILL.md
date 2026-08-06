---
name: "aiksk-minimax-h3-local-prompt"
description: "AI-K SK 专用 MiniMax H3 开放权重本地提示词工程技能 v1.5。面向本地非 API 的 H3-Base、ComfyUI 原生节点与 RunningHub 兼容工作流，生成、改写、校验 T2VA、I2VA、L2VA、FL2VA、Ref2VA 原生音画提示词；重点支持多图、多视频、视频配套音轨、独立音频的精确标签映射、职责分配、说话者绑定与冲突诊断，并保留 v1.3 的多任务、多 Seed、盲评交叉验证原则。"
---

# AI-K SK MiniMax H3 本地提示词工程 v1.5

## 0. 技能目标

把用户的中文创意、首帧、尾帧、首尾帧或多参考素材，转换为可直接粘贴到本地 MiniMax H3 工作流的提示词。默认不调用 MiniMax API，不依赖未开放的 H3-Context-IR 服务，不把本地 H3-Base 写成完整 2K 管线。

v1.5 的核心增强是 **Ref2VA 多参考输入**：在写提示词之前先读取工作流或素材清单，计算真实的 `<Picture N>`、`<Video N>`、`<Audio N>` 映射，再建立“来源—职责—目标”关系图。禁止凭节点尾号猜标签。

## 1. 绝对边界

1. 不调用 MiniMax API，不生成 API 请求体。
2. 不把 H3-Context-IR、H3-Regenerate-2K 写成本地已开放组件。
3. 不声称本地 H3-Base 等同官方完整 2K 系统。
4. 用户提供官方工作流提示词时，默认逐字保存；AI-K SK 改写必须另列。
5. 对白、歌词、画面文字保留原语言和标点，不擅自翻译。
6. 不把 RunningHub 自定义节点称为 ComfyUI 官方原生节点。
7. 看不到参考素材时不臆造内容，只建立编号与职责模板。
8. 不把 `<Audio N>` 与 `(Sx)` 混为同一套编号。
9. 不把 `ref_audio_0` 机械等同于 `<Audio 1>`。
10. 不把 R2V 参考图当作 FL2VA 首尾帧，除非提示词与任务明确把图片定义为具体帧锚点。

## 2. 模式路由

| 模式 | 输入 | 权重族 | 任务 |
|---|---|---|---|
| `T2VA` | 无图 | FL2VA | 文本生成原生音画视频 |
| `I2VA` | 首帧 | FL2VA | 从首帧向后发展 |
| `L2VA` | 尾帧 | FL2VA | 从合理前态收束到尾帧 |
| `FL2VA` | 首帧＋尾帧 | FL2VA | 在两帧之间构造连续路径 |
| `Ref2VA` | 图片／视频／音频多参考 | Ref2VA | 身份、场景、动作、镜头、节奏、音色或音频关系参考 |

输出 Profile：

- `direct`：默认，直接送入官方 ComfyUI 或 RunningHub 的自然语言提示词。
- `concise_structured`：AI-K SK 实验档位，简洁时间线＋连续性约束，不冒充官方 IR。
- `context_ir_emulation`：按官方 Prompting Guidance 人工组织三段或六段结构。
- `strict_context_ir`：仅用于用户提供的官方 IR 原文核验，不擅自改写。
- `enhanced`：兼容旧调用，等同 `context_ir_emulation`。

## 3. 时长与画布

内部同时记录：

```text
requested_duration:
effective_frames:
effective_duration:
fps: 24
width:
height:
```

ComfyUI 官方 H3 使用 `17k+5` 帧网格。用户明确给出帧数时，以实际帧数计算有效时长；不要把名义5秒直接当作关键帧对齐终点。

## 4. Ref2VA 必须先做编号解析

### 4.1 优先从工作流计算

```bash
python scripts/build_ref2va_manifest.py --workflow workflow.json --output ref-manifest.json
```

或直接检查：

```bash
python scripts/inspect_h3_workflow.py workflow.json --json-out workflow-report.json
```

### 4.2 ComfyUI 官方源码的真实顺序

1. 已连接参考图片依次得到 `<Picture 1>`、`<Picture 2>`……
2. 遍历已连接参考视频。
3. 某个 `ref_video_N` 若同时连接同尾号 `ref_video_audio_N`：
   - 配套音轨先占用下一个 `<Audio J>`；
   - 该视频再占用下一个 `<Video K>`。
4. 所有视频处理完成后，独立 `ref_audio_N` 才依次占用后续 `<Audio J>`。
5. 图片、视频、音频三类编号各自独立；端口尾号只用于工作流连接与视频—音轨配对，不是提示词标签号。

例：

```text
ref_video_0 + ref_video_audio_0 + ref_audio_0
→ ref_video_audio_0 = <Audio 1>
→ ref_video_0       = <Video 1>
→ ref_audio_0       = <Audio 2>
```

不接视频配套音轨时：

```text
ref_video_0 + ref_audio_0
→ ref_video_0 = <Video 1>
→ ref_audio_0 = <Audio 1>
```

### 4.3 绝对依赖与合法性

- `ref_video_audio_N` 必须依附已连接的同尾号 `ref_video_N`；否则官方 ComfyUI 实现不会把它登记为参考音频。
- `ref_video_N` 可以不接配套音轨。
- 图片、视频、配套音轨和独立音频可同时存在，没有普遍互斥。
- 官方模型规格：图片≤9；视频≤3；音频信号合计≤3；视频和音频每段2–15秒，各自总时长≤15秒；音频不能作为唯一输入；混合输入文件上限12。
- ComfyUI 源码可能接受比官方规格更宽的边界；技能以模型卡规格作为生产硬规则，并把实现差异列为警告。
- 上述标签顺序只对官方 `MiniMaxH3ReferenceToVideo` 实现作硬结论；RunningHub/RH 或其他自定义节点必须读取其实际源码或使用手工清单，不得默认照搬官方顺序。

## 5. Ref2VA 关系图

写提示词前建立：

```text
source_label → source_role → target_binding → retention_mode → exclusions
```

示例：

```text
<Picture 1> → face_identity + hairstyle → <Subject 1> → fully_preserved → ignore source background
<Picture 2> → costume → <Subject 1> → attribute_transfer → ignore source pose
<Video 1> → body motion + camera timing → target shot → reference → ignore source performer identity
<Audio 1> → synchronized footsteps and impacts from <Video 1> → target physical sounds → reference → no voice transfer
<Audio 2> → female voice timbre → <Subject 1> (S1) → reference → do not copy original words
```

禁止默认“一张图＝一个 Subject”。允许：

- 一个 Subject 由多张图或图＋视频共同定义；
- 一张图提供多个 Subject；
- 视频中的人物、动作、场景可以抽象为 `<Subject N>`；
- `<Video N>` 只表示整段视频资产、编辑源、续写起点或整体时间结构；
- 图片只承担身份／服装／场景来源时，写在 `<Subject N>` 来源中，不必机械创建独立 `<Picture N>` 定义；
- 图片承担首帧、尾帧、关键帧、构图或分镜锚点时，才把 `<Picture N>` 作为独立项目追踪。

## 6. `<Audio N>` 与 `(Sx)`

- `<Audio N>`：参考音频信号来源。
- `(S1)`、`(S2)`：目标视频中实际发声者，按首次发声顺序分配。
- 声音迁移必须显式绑定：

```text
<Audio 2> is the voice-timbre and delivery reference for <Subject 1> (S1).
```

- 只参考音色、节奏、情绪时，不自动复制原音频中的台词。
- 直接复用整段音轨或部分音轨时，用 `fully_copy` / `partially_copy`；只参考音色、节奏或声音质感时用 `reference`。
- `retention_analysis` 中禁止写 `(Sx)`。
- 若声音只是直接复用的BGM或完整音轨中的人声，不由具体人物重新发声，则使用 `<Audio N>` 作为声源，不凭空新增 `(Sx)`。

## 7. 视频与视频音轨的职责

```text
<Video N>：动作、表演节奏、镜头运动、切镜、构图变化、整段时间结构，或被直接编辑／续写的视频源。
<Audio N>（配套音轨）：同一参考视频中的对白、音乐、动作声、环境声及其时间关系。
```

二者一起输入的价值是参考音画同步；不是保证逐帧动作复制，也不是保证原音1:1保留。需要原音完全不变时，优先后期直接复用音轨。

## 8. 提示词生成步骤

1. 识别模式、工作流族与 Profile。
2. 读取工作流或手工清单，生成 `ref-manifest.json`。
3. 输出或内部确认素材编号表。
4. 建立 reference graph，给每份素材限定职责和排除项。
5. 决定音频是 `copy` 还是 `reference`，并绑定目标说话者。
6. 写 Direct／Concise／Context-IR 提示词。
7. 使用工作流清单进行静态校验：

```bash
python scripts/validate_h3_prompt.py prompt.txt \
  --mode ref2va --profile context_ir_emulation \
  --duration 5 --manifest ref-manifest.json --strict
```

8. 真实效果结论必须执行多任务、多 Seed、盲评的对照验证，静态 PASS 不等于生成质量优胜。

## 9. Direct Ref2VA 写法

Direct 也必须引用真实标签：

```text
Use <Picture 1> only for <Subject 1>'s facial identity and hairstyle, and use <Picture 2> only for her costume. Use the body motion and camera timing from <Video 1>, while ignoring the source performer's identity, clothing, and background. Use <Audio 1> only for synchronized footsteps and impact timing. Use the voice timbre and emotional delivery from <Audio 2> for <Subject 1> (S1), without copying the source words. [TARGET SHOT AND DIALOGUE].
```

## 10. Context-IR Ref2VA 六段结构

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

详细规则见：

- `references/ref2va-multireference-enhanced.md`
- `references/ref2va-audio-numbering.md`
- `references/ref2va-reference-graph.md`
- `references/context-ir-ref-spec.md`

## 11. 输出格式

默认输出：

```text
模式：
Profile：
适用工作流：

素材编号表：
Picture 1 = ...
Video 1 = ...
Audio 1 = ...
S1 = ...

最终英文提示词：
[单独代码块]

接线与风险：
[最多5条]
```

用户只要“提示词”时，内部仍先完成映射，但可仅输出最终可复制提示词。

## 12. 交叉验证边界

v1.5保留v1.3原则：

- 同任务、同素材、同工作流、同参数、匹配 Seed；
- Direct、Concise Structured、Context-IR 语义等价；
- 多任务、多 Seed、盲评、多评审；
- 硬失败与普通质量分开；
- 单环境最高 provisional，独立环境复现后才升级证据等级；
- 不用模拟视频或静态校验伪造“某种提示词一定更强”的结论。

多参考专项新增评分维度：标签准确率、职责隔离、身份保持、动作迁移、镜头迁移、音频来源正确性、说话者绑定、音画同步和无意属性泄漏。

## 13. 关联文件

- 快速卡：`references/quick-card.md`
- 多参考增强：`references/ref2va-multireference-enhanced.md`
- 音频编号：`references/ref2va-audio-numbering.md`
- 引用关系图：`references/ref2va-reference-graph.md`
- 冲突矩阵：`references/ref2va-conflict-matrix.md`
- 官方实现映射：`references/local-workflow-map.md`
- Context-IR Ref规范：`references/context-ir-ref-spec.md`
- 交叉验证：`references/cross-validation-protocol.md`
- 来源登记：`references/source-register.md`
- 工作流清单生成：`scripts/build_ref2va_manifest.py`
- 提示词校验：`scripts/validate_h3_prompt.py`
- 预注册矩阵：`scripts/create_h3_validation_matrix.py`
- 实验锁验收：`scripts/verify_h3_experiment.py`
- 盲评包：`scripts/prepare_h3_blind_review.py`
- 评审合并：`scripts/merge_h3_reviews.py`
- 配对分析：`scripts/analyze_h3_validation.py`
- 独立复现合并：`scripts/combine_h3_replications.py`
- 评分锚点：`references/scoring-rubric.md`
- 证据等级：`references/evidence-grading.md`
