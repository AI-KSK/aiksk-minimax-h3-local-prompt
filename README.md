# AIKSK MiniMax H3 全域提示词规范 v1.8.1 — Director + 武打编排

这是 AIKSK MiniMax H3 本地提示词体系的 **v1.8.1 武打专项修订版（保留 v1.7 全部结构）**。

核心目标不是“写得像提示词”，而是让 Claude / Codex / 其他 Agent 能稳定把创作者的自然语言需求、图片、视频、音频和镜头意图，编译成 **MiniMax H3 官方兼容的完整提示词**，并且能够正确服务于 **AIMixer / ComfyUI_MiniMaxH3_Director（导演台）**。

## 原有生产逻辑（继续沿用）

> **先认人，再认图；先定故事，再定镜头；上一幕必须推得出下一幕；最后再编译成 H3 官方格式。**

## 两大语法家族

### Base family
用于 `t2v / i2v / fl2v / l2va`：

1. keyframe alignment instruction（需要时）
2. `integrated_multimodal_description`
3. `overall_soundscape`
4. `non_diegetic_music`

### Full-reference / Ref2VA family
用于导演台 `r2v / v2v / rv2v`：

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

## AIMixer Director 关键认知

AIMixer Director **没有另造一套 H3 Prompt Grammar**。它是官方 ComfyUI MiniMax H3 conditioning/sampling 链路上的多段导演层。

- 导演台素材槽直接产生：`<Picture N>` / `<Video N>` / `<Audio N>`
- `<Subject N>` 不是上传槽，而是 Ref2VA 提示词中由 `subject_definitions` 创建的“语义身份证”
- 同一个人物出现在三张图片里时，应优先定义为同一个 `<Subject N>`，而不是当成三个人
- 图片只有在承担首帧、尾帧、关键帧、构图锚点或 storyboard 作用时，才需要作为独立 `<Picture N>` 持续追踪

详见：

- `references/director/AIMIXER_DIRECTOR_RULES.md`
- `references/director/DIRECTOR_PROMPT_LOGIC_ZH.md`
- `templates/director_r2v_master.txt`
- `examples/director_r2v_10s_three_image_story.txt`

## 新增：武打 / 双人攻防 / 兵器 / 枪斗板块

- 自动路由：武打、对打、刀剑、枪斗、跑酷、JOKER141、Work-Fisher 相关需求读取 `references/playbooks/fight-choreography.md`。
- 动作编排：人物站位 → 起手 → 攻击路径 → 实际接触/格挡 → 受击重心 → 反击/恢复 → 最后稳态。
- 5 秒一轮有效攻防、10 秒多拍衔接、15 秒八拍故事弧。八拍不是八个镜头。
- 单独锁定 Fighter A / Fighter B 的脸、衣着、站位与武器归属；减少瞬移、换人、武器复制。
- `references/playbooks/fight-lora-presets.json` 收录 JOKER141 A0–A8 的 9 种**实验起始权重**，与提示词语法严格分开。
- 对应模板：`templates/fight_t2va_5s_master.txt`、`templates/fight_ref2va_5s_master.txt`。
- 完整案例：`examples/fight_t2va_5s_unarmed.txt`、`examples/fight_ref2va_5s_two_person.txt`。

## v1.8.1 新增：可执行预设同步与验证

新增 `references/playbooks/fight-trigger-policy.md`（模型作者触发词使用条件）、`references/playbooks/fight-prompt-mapping.md`（9组动作风格映射），以及 `scripts/sync_fight_workflow.py`（离线工作流同步器）。

同样保留九组 A0–A8，**额外 BASE 是五个专项 LoRA 全部为 0 的对照状态**，但 Turbo + Veda 继续启用。导出工具能同步模式、Prompt 和预设；如果后来只在 ComfyUI UI 里改预设，Prompt 不会自动联动，必须重新导出或自己编辑。

直接从解压目录执行：

```bash
python scripts/sync_fight_workflow.py --preset A4 --mode R2VA --output output/AIKSK_H3_A4_R2VA.json
```

想做基础对照：

```bash
python scripts/sync_fight_workflow.py --preset BASE --mode T2VA --output output/AIKSK_H3_BASE_T2VA.json
```

输出与旁路审计信息写入 `output/`，不会改动 `integrations/` 里的原版工作流。R2VA 模式必须在 ComfyUI 中先上传真实两张参考图，不假定文件名存在。

本次升级**不更改** `references/official/` 的 MiniMax 原始指南，不改变 Base 三字段、Ref2VA 六段式；不对任何武打 LoRA 或 Veda 提速效果做保证。没有额外安装神经网络模型，也没有改写 ComfyUI JSON。

## 给 Codex

直接把整个目录作为 Skill / project context 使用即可。推荐先让 Codex 阅读：

1. `SKILL.md`
2. `references/official/base-en.txt`
3. `references/official/ref-en.txt`
4. `references/director/AIMIXER_DIRECTOR_RULES.md`
5. `CODEX_INSTALL.md`

执行结构测试：

```bash
python tests/test_structure.py
```

成功应输出：

```text
OK v1.8.1
```

## 验证日期

**官方语法**在 **2026-08-29** 校对包装内的官方语法，来源包括：MiniMax 官方仓库/Prompt Guide、ComfyUI 官方 H3 文档、AIMixer Director 官方 README。具体见 `references/CROSS_VALIDATION.md`。**武打模型卡于 2026-10-13 联网交叉核查**，不是一次重新验证 MiniMax 官方语法。
