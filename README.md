# AI-KSK MiniMax H3 全域提示词工程与创意生产 v1.6

> 基于 MiniMax H3 官方 Prompt Grammar 构建的全域提示词工程 Skill。
>
> 不只是“把一句话扩写成 Prompt”，而是把 **创作意图、参考素材、人物一致性、动作、镜头、声音、对白、时间轴和编辑目标** 编译成可直接用于 MiniMax H3 的结构化提示词。

这不是官方 Skill 的简单搬运，也不冒充 MiniMax 官方实现。AI-KSK v1.6 保留官方 H3 Prompt Grammar 作为底层兼容基准，在其上增加面向实际创作、ComfyUI 和 RunningHub 工作流的 **Prompt Production Compiler**。

## 核心能力

- 支持 T2VA、I2VA、FL2VA、L2VA、Ref2VA 五种 H3 模式
- 多图片、视频、音频 Reference Mapping
- 人物、服装、产品、构图、动作、镜头和音频一致性锁
- Camera、Action、Timeline、Dialogue、Native Audio 编译
- 50 类高频创作玩法与 8 种输出 Profile
- 人物跑脸、动作不足、运镜混乱、对白截断、音画不同步等失败修复
- ComfyUI / RunningHub 工作流 JSON 与素材清单路由

```text
用户想法
↓
识别 H3 模式与任务意图
↓
分析图片 / 视频 / 音频角色
↓
建立 Reference Map 与 Consistency Locks
↓
规划动作 / 镜头 / 对白 / 声音 / 时间轴
↓
编译为官方 H3 Prompt Grammar
↓
检查引用、冲突、时序和格式
↓
输出最终 H3 Prompt
```

## MiniMax H3 五大模式

| 模式 | 输入 | 目标 |
|---|---|---|
| `T2VA` | Text | 纯文本生成完整音视频 |
| `I2VA` | Image + Text | 从首帧图片生成音视频 |
| `FL2VA` | First Frame + Last Frame + Text | 控制首尾帧之间的连续过程 |
| `L2VA` | Last Frame + Text | 根据目标尾帧生成合理前序过程 |
| `Ref2VA` | Image / Video / Audio References + Text | 使用多模态素材生成、编辑或续写音视频 |

Base 模式保留官方字段：

- `integrated_multimodal_description`
- `overall_soundscape`
- `non_diegetic_music`

Ref2VA 保留官方六段式结构：

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

## Ref2VA Reference Engine

针对 H3 最复杂的 Ref2VA 模式，先建立引用关系，再生成提示词：

```text
<Subject N>  → 可复用的可见主体
<Picture N>  → 图片或具体帧锚点
<Video N>    → 源视频、编辑、续写、动作或镜头参考
<Audio N>    → 声音、音乐、音色或可复用音频信号
```

引擎会区分：

- Identity / Style / Motion / Camera / Environment Reference
- Voice / Music / Audio Reference
- Source Video / Continuation Source / Edit Source
- `<Audio N>` 引用信号与 `(Sx)` 目标说话者
- `fully_preserved`、`attribute_transfer`、`weak_reference` 等保留关系
- `fully_copy`、`partially_copy`、`reference` 等音频关系

主要解决引用编号混乱、人物串脸、动作和身份错误绑定、参考声音与说话者混淆、错误复用原台词，以及多参考素材冲突。

## Production Locks

v1.6 按任务只启用真正需要的一致性约束：

| Lock | 作用 |
|---|---|
| Identity / Face / Hair | 保持人物身份、脸部和发型 |
| Wardrobe / Body | 保持服装、体型和人体比例 |
| Product / Logo | 保持商品结构、材质、包装和标识 |
| Composition / Environment | 保持构图、机位和环境几何 |
| Motion / Camera | 保持动作轨迹、镜头方向和轴线 |
| Audio / Voice | 保持音色、节奏、对白或源音频关系 |

不会把所有 Lock 同时塞进 Prompt，避免约束过载。

## 50 类 H3 创作玩法

### 影视 / 剧情

电影短片、AI 短剧、中文对白、悬疑、恐怖、喜剧、爱情、纪录片、第一人称 POV、打斗、动作设计、变身、奇幻特效、舞蹈、体育运动。

### 商业 / 广告

产品广告、品牌宣传片、新品发布、美妆、时尚、食品、烹饪、科技产品、UI 展示、电商带货、建筑、酒店、旅游宣传。

### 动画 / 风格化

3D Animation、手绘 + 真人、Paper Collage、Papercraft、Stop Motion、Clay、Miniature、Toy World、Anime、2D Animation、Game Intro、Game Character UI。

### 音频驱动

MV、Lyrics Video、Singing、数字人、Voice Reference、双人对白、Narration、Sound Design。

### Reference / Editing

人物一致性、多图人物参考、服装参考、环境迁移、动作参考、镜头参考、视频编辑、视频续写、声音替换、BGM Reference、首帧生成、首尾帧控制、尾帧控制。

完整路由见 [`references/playbooks/use-case-catalog.md`](references/playbooks/use-case-catalog.md)。

## Camera & Action Compiler

不堆叠 `cinematic`、`dynamic camera` 一类空泛形容词，而是拆分为可执行关系：

```text
Camera Motion
+ Direction
+ Speed
+ Amplitude
+ Subject Movement
+ State Change
+ Final State
```

复杂动作采用：

```text
Initial State
→ Trigger
→ Physical Action
→ Intermediate State
→ Final State
```

支持 Push In、Pull Out、Pan、Tilt、Orbit、Truck、Crane、Handheld、Chase、POV、Overhead、Rack Focus、Dolly Zoom 等常用镜头设计，并限制短时长镜头中的无效运镜堆叠。

## Native Audio Prompt System

声音被拆分为四个独立层次：

```text
Dialogue / Singing
Diegetic Ambience
Physical SFX
Non-diegetic Music
```

支持中英文对白、多人对白、Singing、Voice Reference、环境音、动作音效、BGM、节奏参考和源视频音频复用。

中文对白格式：

```text
<d>[Chinese] 中文台词。</d>
```

## Output Profiles

| Profile | 用途 |
|---|---|
| `official_full` | 完整官方结构，适合最终生产 |
| `official_compact` | 保持官方结构并压缩冗余描述 |
| `director` | 强化运镜、调度、表演、构图和声音设计 |
| `identity_lock` | 强化人物、服装、体型和道具一致性 |
| `edit_lock` | 编辑视频时尽量只改变指定内容 |
| `motion_reference` | 强化动作、镜头和节奏迁移 |
| `audio_control` | 强化声音引用、说话者、对白、BGM 和音效 |
| `creative_max` | 在用户意图内增强镜头、动作、场景、节奏和转场 |

这些是 AI-KSK 生产 Profile，不是 MiniMax 官方模式。

## Prompt Repair Engine

生成失败后先诊断原因，再做定向修复：

- `Identity Drift`：人物跑脸或身份不一致
- `Action Too Weak`：动作幅度、方向或终态不清楚
- `Camera Chaos`：运镜堆叠或镜头轴线冲突
- `Dialogue Cut Off`：对白被截断或节奏过密
- `Audio Mismatch`：说话者、音色和画面不同步
- `Product Deformation`：产品几何、材质或 LOGO 变形
- `First / Last Frame Mismatch`：首尾帧无法自然连接
- `Reference Mapping Error`：图片、视频、音频引用关系错误

## ComfyUI / RunningHub Support

Prompt 层和 Workflow 层保持分离。提供工作流 JSON 或素材清单后，Skill 会按真实连接关系判断 `Picture 1`、`Video 1`、`Audio 1`，避免只根据文件顺序猜测引用编号。

适用于 H3 T2VA、I2VA、FL2VA、L2VA、Ref2VA、Hybrid Conditioning 和 RunningHub AI 应用。

## 安装

### Codex

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/AI-KSK/aiksk-minimax-h3-local-prompt.git ~/.codex/skills/aiksk-minimax-h3-local-prompt
```

Windows PowerShell 示例：

```powershell
git clone https://github.com/AI-KSK/aiksk-minimax-h3-local-prompt.git "$env:USERPROFILE\.codex\skills\aiksk-minimax-h3-local-prompt"
```

也可以放入任何能够读取本地 Skill 文件的 Agent 环境，包括 Claude Code、Cursor、Windsurf、本地 Agent 和自定义 Agent Framework。核心 Prompt Writing 不依赖外部 API。

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

AI-KSK Skill 会先解析为：

```text
Mode: Ref2VA
Intent: IDENTITY / MOTION / CAMERA / REFERENCE

<Picture 1> → Character Identity
<Video 1>   → Motion + Camera Reference

Locks: Identity / Wardrobe / Motion Reference
Forbidden Transfer: Video 1 Character Identity / Environment
```

然后再编译成 MiniMax H3 Ref2VA 正式 Prompt。

## 项目结构

```text
aiksk-minimax-h3-local-prompt/
├── SKILL.md
├── references/
│   ├── official/
│   │   ├── base-en.txt
│   │   └── ref-en.txt
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
│   └── ref2va_master.txt
└── tests/
    └── test_structure.py
```

## Design Principle

```text
Official Grammar
↓
Asset Truth
↓
User Intent
↓
AI-KSK Enhancement
```

如果 AI-KSK 的扩展规则与 MiniMax 官方 H3 Prompt Grammar 冲突，始终以官方规则为准。AI-KSK 扩展层不会被描述成 MiniMax 官方能力。

## Disclaimer

本项目是社区 Prompt Engineering / Agent Skill 项目，不是 MiniMax 官方 SDK，不是 H3-Context-IR 的复刻，也不是 H3-Regenerate-2K 的替代实现。

MiniMax、MiniMax H3 及相关商标归其各自权利人所有。

## Official References

- [MiniMax H3](https://github.com/MiniMax-AI/MiniMax-H3)
- [Official H3 Prompt Writing Skill](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing)
- [MiniMax H3 on Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-H3)

## Author

**AI-KSK**

AI / AIGC / ComfyUI / Workflow Engineering
