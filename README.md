# AI-KSK MiniMax H3 全域提示词工程 v1.7 — Director Production

> 把创作意图、参考素材、人物一致性、动作、镜头、声音、对白、时间轴和编辑目标，编译成 MiniMax H3 官方兼容的结构化提示词。
>
> v1.7 新增 AIMixer / ComfyUI_MiniMaxH3_Director（导演台）生产规则。

这不是官方 Skill 的搬运，也不冒充 MiniMax 官方实现。官方 H3 Prompt Grammar 是硬语法基准，AI-KSK 在其上叠加面向实际创作、ComfyUI / RunningHub / 导演台的 Prompt Production Compiler。

## v1.7 一句话逻辑

> 先认人，再认图；先定故事，再定镜头；上一幕必须推得出下一幕；最后才编译成 H3 官方格式。

## v1.7 新增什么

| 变更 | 说明 |
|---|---|
| 导演台模式映射 | `t2v/i2v/fl2v → Base`，`r2v/v2v/rv2v → Ref2VA`，附模型族对应 |
| Subject / Picture 语义分离 | `<Subject N>` 是语义身份，不是导演台上传素材槽 |
| 三图连续叙事编译器 | Reference identity → Story role → Causal bridge → Timeline → Camera/audio → 六段式 |
| 跨镜头因果桥 | 上一镜头末端动作必须为下一镜头首个动作提供可观察连接 |
| 官方 summary task types | keyframe completion / reference generation / video editing / video continuation / audio reuse / audio reference |
| detailed_description 密度 | generation 任务默认对齐官方约 350–500 English words |
| H3 输入限制修正 | Images ≤9；Videos ≤3；Audio ≤3；单段 2–15s；总时长 ≤15s；mixed files ≤12 |
| common prompt 安全策略 | 默认每组写完整六段式；advanced 模式只共享 `subject_definitions` 前缀 |
| Codex 安装说明 | 新增 `CODEX_INSTALL.md`、`AGENTS.md` |
| 结构自测增强 | 精确校验 Base 首行、六段顺序、Director 必需文件与示例时间戳 |

完整条目见 [CHANGELOG.md](CHANGELOG.md)。

## 两大语法家族

### Base family — `t2v / i2v / fl2v / l2va`

1. keyframe alignment instruction（I2VA / FL2VA / L2VA 需要时）
2. `integrated_multimodal_description`
3. `overall_soundscape`
4. `non_diegetic_music`

### Full-reference family — `r2v / v2v / rv2v`

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

段序和字段名不得重排或改名。

## MiniMax H3 五大官方模式

| 模式 | 输入 | 目标 |
|---|---|---|
| `T2VA` | Text | 纯文本生成完整音视频 |
| `I2VA` | Image + Text | 从首帧图片生成音视频 |
| `FL2VA` | First Frame + Last Frame + Text | 控制首尾帧之间的连续过程 |
| `L2VA` | Last Frame + Text | 根据目标尾帧生成合理前序过程 |
| `Ref2VA` | Image / Video / Audio References + Text | 用多模态素材生成、编辑或续写音视频 |

## AIMixer Director 映射

导演台没有另造一套 H3 Prompt Grammar。它是官方 ComfyUI MiniMax H3 conditioning / sampling 链路上的多段导演层，因此提示词仍然回落到官方两大家族：

| Director 任务 | Prompt 家族 | 模型族 |
|---|---|---|
| `t2v` | Base / T2VA | fl2va |
| `i2v` | Base / I2VA | fl2va |
| `fl2v` 首尾都有 | Base / FL2VA | fl2va |
| `fl2v` 只有首帧 | Base / I2VA | fl2va |
| `fl2v` 只有尾帧 | Base / L2VA | fl2va |
| `r2v` | Full-reference / Ref2VA | ref2va |
| `v2v` | Full-reference / Ref2VA | ref2va |
| `rv2v` | Full-reference / Ref2VA | ref2va |

详见 [AIMIXER_DIRECTOR_RULES.md](references/director/AIMIXER_DIRECTOR_RULES.md)，中文平民化版本见 [DIRECTOR_PROMPT_LOGIC_ZH.md](references/director/DIRECTOR_PROMPT_LOGIC_ZH.md)。

## Subject 不等于 Picture

v1.7 最核心的一条认知。导演台素材槽只产生素材标签，语义身份要由提示词自己建立：

```text
<Picture N>  → 哪一个文件 / 哪一帧
<Video N>    → 源视频、编辑源、续写源、动作或镜头参考
<Audio N>    → 被复制或被参考的音频信号
<Subject N>  → 这个可复用的人 / 动物 / 产品 / 环境是"谁"
```

一句口诀：**Picture 管哪张图，Subject 管这是谁。**

同一个角色出现在三张图里，应合并为一个 Subject，而不是三个角色：

```text
<Subject 1> is the same woman whose identity and appearance are established
by <Picture 1>, <Picture 2>, and <Picture 3>.
```

图片只有在承担首帧、尾帧、关键帧、编辑关键帧、构图锚点或 storyboard 作用时，才需要作为独立 `<Picture N>` 继续追踪。只提供长相、服装、道具、风格的图片，写进对应 Subject 定义里即可，不必强行多写一条 Picture。

## 因果桥：多镜头不是三张图轮播

v1.7 把"三图看起来像幻灯片"当成一类明确的失败，并给出修复路径。每次切镜至少保留一个可观察的连续性载体：身体动作、视线方向、道具接触、前冲动量、声音提示、镜头方向、状态变化。

```text
摸猪 → 野猪抬头喷鼻前倾 → 切 → 追逐已经在进行
跑 → 回头 → 伸手抓链条 → 切 → 手完成抓握 → 借力上猪
```

这是 AI-KSK 生产经验，不是 MiniMax 官方字段要求，但它是导演台叙事的默认策略。完整示例见 [examples/director_r2v_10s_three_image_story.txt](examples/director_r2v_10s_three_image_story.txt)。

## 编译流程

```text
用户想法
↓
识别 Base / Ref2VA 家族与 Director 任务
↓
提取不可变约束（谁不能变、起止状态、时长、台词、禁止项）
↓
建立素材真实角色映射（身份 / 关键帧 / 构图 / 动作 / 编辑源 / 音频）
↓
合并同一可复用内容为 Subject 图谱
↓
拆成可观察的故事节拍，而非情节概述动词
↓
为每次切镜建立因果桥
↓
按信息量分配时长（对齐有效时长，不是机械平均）
↓
每镜只写有用信息：构图 / 位置 / 动作 / 一个主导运镜 / 声音 / 对白 / 生效引用
↓
编译为官方 Base 或六段式结构
↓
17 项 QA 校验
↓
输出最终 H3 Prompt
```

## 运行时事实（2026-08-29 校验）

- 输出时长 4–15 秒，24 FPS，立体声 32 kHz
- Base 生成短边默认 768 px；2K 归属 H3-Regenerate-2K
- Ref2VA：Images ≤ 9
- Ref2VA：Videos ≤ 3，单段 2–15s，总时长 ≤ 15s
- Ref2VA：Audio ≤ 3，单段 2–15s，总时长 ≤ 15s
- 混合输入文件总数 ≤ 12
- 官方 H3-Context-IR 是托管预处理 / 编排系统，与本地提示词 Skill 不是同一件事

不要臆造"通用 10 秒上限"。

## Director common prompt 策略

导演台 common prompt 会与每个素材组的 prompt 拼接，所以它是最容易破坏段序的地方。

- 安全默认（推荐给创作者和 Codex 自动化）：common prompt 留空，每组写一份完整六段式。最好审计，也不会出现重复 section header。
- 进阶共享模式：common prompt 只放 `subject_definitions:` 开头和共享身份定义；组内 prompt 接着写组内定义行，然后直接进入 `summary:`，不要再写第二个 `subject_definitions:`。

## Production Locks

按任务只启用真正需要的一致性约束，不把所有 Lock 同时塞进 Prompt：

| Lock | 作用 |
|---|---|
| Identity / Face / Hair / Body | 保持人物身份、脸部、发型、体型轮廓 |
| Wardrobe / Accessory | 保持服装与配饰 |
| Product / Logo / Text | 保持商品几何、材质、包装、标识与文字 |
| Environment / Composition | 保持构图、机位与环境几何 |
| Motion / Camera Axis | 保持动作方向与镜头轴线 |
| Lighting | 保持光照关系 |
| Voice / Dialogue / Source Audio | 保持音色、精确台词、源音频复用关系 |

明确区分"可以变的"和"不可以变的"，比堆叠约束更有效。

## Output Profiles

| Profile | 用途 |
|---|---|
| `official_full` | 默认终稿：精确语法 + 充分细节 |
| `official_compact` | 精确语法 + 压缩冗余 |
| `director` | 强化调度、因果转场、运镜与声音 |
| `identity_lock` | 强化人物 / 服装 / 产品连续性 |
| `edit_lock` | Ref2VA 源编辑，尽量只改指定内容 |
| `motion_reference` | 迁移身体 / 镜头 / 节奏，不误抄身份与环境 |
| `audio_control` | 声音、说话者、对白、BGM 关系优先 |
| `creative_max` | 在用户约束内做创意增强 |

这些是 AI-KSK 生产 Profile，不是 MiniMax 官方模式。

## 失败修复

| 症状 | 修复方向 |
|---|---|
| Identity Drift 人物跑脸 | 同一角色合并到一个 Subject，身份来源图全部写进该定义，删掉多余风格变换 |
| 三图幻灯片感 | 建立复现 Subject、给每张图故事角色、补因果桥、跨切镜延续动作与声音 |
| Action Too Weak | 用物理过渡和终点替换抽象意图 |
| Camera Chaos | 每镜一个主导运镜，去掉装饰性堆叠 |
| Dialogue Cut Off | 降低说话期间视觉复杂度，切点放自然停顿，未获许可不改原台词 |
| Audio Mismatch | 校正说话者 ID、音色与画面同步关系 |
| Product Deformation | 把几何 / 材质 / LOGO / 文字提升为硬连续性约束 |

更细的矩阵见 [failure-repair-matrix.md](references/playbooks/failure-repair-matrix.md)。

## 50 类创作玩法

影视剧情、商业广告、动画风格化、音频驱动、Reference / Editing 五大类，完整路由见 [use-case-catalog.md](references/playbooks/use-case-catalog.md)。

## 安装

### Codex

```bash
git clone https://github.com/AI-KSK/aiksk-minimax-h3-local-prompt.git ~/.codex/skills/aiksk-minimax-h3-local-prompt
```

Windows PowerShell：

```powershell
git clone https://github.com/AI-KSK/aiksk-minimax-h3-local-prompt.git "$env:USERPROFILE\.codex\skills\aiksk-minimax-h3-local-prompt"
```

也可以放入任何能读取本地 Skill 文件的 Agent 环境，包括 Claude Code、Cursor、Windsurf 和自定义 Agent Framework。核心 Prompt Writing 不依赖外部 API。

要点：Skill root 必须是包含 `SKILL.md` 的那一层，不要只上传 `SKILL.md`，也不要删 `references/official/`，它们是硬语法来源。详见 [CODEX_INSTALL.md](CODEX_INSTALL.md)。

### 自测

```bash
python tests/test_structure.py
```

通过应输出 `OK v1.7`。校验内容包括版本号、Base 首行原文、六段顺序、官方 task types 与 retention markers、Speaker 语法、Director 必需文件、示例的六段唯一性与时间戳。

完整性校验可比对 [MANIFEST.json](MANIFEST.json) 中的 sha256。

## 使用示例

用户输入：

```text
使用第一张图中的女孩作为人物参考。
使用视频 1 里的跑步动作和镜头运动。
女孩穿红色风衣，在雨夜东京街头奔跑。
不要使用视频 1 中的人物外貌和场景。
保持第一张图的人物脸部、发型和服装。
最后停在便利店门口。
```

Skill 先解析为：

```text
Family: Full-reference / Ref2VA（Director r2v）
Task type: reference generation

<Subject 1> → 女孩身份，由 <Picture 1> 建立
<Video 1>   → 动作 + 镜头参考

Locks: Identity / Wardrobe / Motion direction
Forbidden transfer: Video 1 的人物身份与环境
```

然后再编译成正式六段式 Prompt。

## 从 v1.6 升级

整目录替换即可，没有需要迁移的配置。行为差异：

- `SKILL.md` 重构为 Layer 0–14，更短但规则更硬，新增 Director 层与因果桥
- Ref2VA `detailed_description` 目标字数上调到官方建议的约 350–500 English words
- H3 输入限制补全为单段时长与总时长双重约束
- `templates/ref2va_master.txt` 从空壳段名扩写为带角色注释的骨架
- `tests/test_structure.py` 从关键词存在性检查升级为精确规则校验，会强校验 `version: "1.7.0-2026.08.29"` 和 Director 文件存在
- v1.6 散落在 `SKILL.md` 里的 50 类玩法明细，统一收在 `references/playbooks/use-case-catalog.md`

## 项目结构

```text
aiksk-minimax-h3-local-prompt/
├── SKILL.md                  # 主规则，Layer 0–14
├── AGENTS.md                 # 给 coding agent 的操作约定
├── CODEX_INSTALL.md          # Codex 安装 / 上传说明
├── MANIFEST.json             # 文件清单与 sha256
├── CHANGELOG.md
├── references/
│   ├── official/             # 官方硬语法来源
│   │   ├── base-en.txt
│   │   └── ref-en.txt
│   ├── director/             # 导演台规则
│   │   ├── AIMIXER_DIRECTOR_RULES.md
│   │   └── DIRECTOR_PROMPT_LOGIC_ZH.md
│   ├── playbooks/
│   │   ├── use-case-catalog.md
│   │   ├── ref2va-reference-recipes.md
│   │   ├── dialogue-audio-recipes.md
│   │   ├── camera-action-recipes.md
│   │   └── failure-repair-matrix.md
│   ├── CROSS_VALIDATION.md
│   └── SOURCE_REGISTER.md
├── templates/
│   ├── t2va_master.txt
│   ├── i2va_master.txt
│   ├── fl2va_master.txt
│   ├── l2va_master.txt
│   ├── ref2va_master.txt
│   └── director_r2v_master.txt
├── examples/
│   └── director_r2v_10s_three_image_story.txt
└── tests/
    └── test_structure.py
```

## Design Principle

```text
Official Grammar
↓
Asset Truth / Director Mapping
↓
User Hard Constraints
↓
AI-KSK Enhancement
```

如果 AI-KSK 扩展规则与 MiniMax 官方 H3 Prompt Grammar 冲突，始终以官方规则为准。AI-KSK 的生产经验不会被描述成 MiniMax 官方要求。

## 交叉验证

规则在 2026-08-29 针对四层独立一手文档重新交叉验证：MiniMax 官方 Base Prompt Guide、官方 Full-reference Prompt Guide、MiniMax + ComfyUI 运行时文档、AIMixer Director 官方 README。

结论是没有发现需要为导演台另造一套语法的一手来源冲突。明细见 [CROSS_VALIDATION.md](references/CROSS_VALIDATION.md)，来源清单见 [SOURCE_REGISTER.md](references/SOURCE_REGISTER.md)。

## Disclaimer

本项目是社区 Prompt Engineering / Agent Skill 项目，不是 MiniMax 官方 SDK，不是 H3-Context-IR 的复刻，也不是 H3-Regenerate-2K 的替代实现。

MiniMax、MiniMax H3、AIMixer 及相关商标归其各自权利人所有。

## Official References

- [MiniMax H3](https://github.com/MiniMax-AI/MiniMax-H3)
- [Official H3 Prompt Writing Skill](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing)
- [MiniMax H3 on Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- [ComfyUI MiniMax H3 教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)
- [AIMixer ComfyUI_MiniMaxH3_Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director)

## Author

**AI-KSK**

AI / AIGC / ComfyUI / Workflow Engineering






