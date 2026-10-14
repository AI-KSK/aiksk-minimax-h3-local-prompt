# v1.8.1 (2026-10-13) — Martial corrective update

- Retain 25 original v1.7 files; never rewrite official MiniMax reference content.
- Nine A0–A8 recipes preserved, separate BASE baseline added without renumbering.
- Trigger policy from JOKER141 author cards; default Combat untriggered, others conditional/optional as specified.
- Offline exported JSON automatically synchronizes scene prompt, task mode and preset; it does **not** add a live ComfyUI prompt binding.
- Source register and cross-validation refreshed; Veda R2VA 4-step caveat captured.
- New smoke tests for scene routing A4/A7, BASE, REF labels, JSON link validity and unchanged official source hashes.

# Changelog

## v1.8 Martial Arts Production — 2026-10-13

- 保留 v1.7 Director、官方语法引用和原有案例，不覆盖现有能力。
- 新增武打专项 `references/playbooks/fight-choreography.md`：徒手、双人攻防、兵器、GunFu、通用动作修复路由；状态账本、接触几何、5/10/15 秒动作节拍、屏幕轴线、音效和修复策略。
- 新增 `references/playbooks/fight-lora-presets.json`，收录 JOKER141 五类 LoRA 的 A0–A8 起始权重与准确文件名；明确只是 ComfyUI 实验配置，不是官方语法/已验证最优。
- 新增 2 个武打模板、2 个 Base/Ref2VA 完整武打示例。
- 更新 SKILL 路由、AGENTS、用途目录、镜头动作规约、错误修复矩阵与 Codex 安装说明。
- 增强 tests/test_structure.py；新增官方原始指南 SHA256 不变的回归校验，更新 MANIFEST 全量哈希。
- 延续“单阶段 T2VA/R2VA + Turbo + Veda”的现有编排观念，但本次不修改任何 ComfyUI JSON，也不声称已完成显卡实测。


## v1.7 Director Production — 2026-08-29

- 在 v1.6 rebuild 上升级，不推翻原有全域生产路由。
- 新增 AIMixer MiniMax H3 Director 专用模式映射：`t2v/i2v/fl2v → Base`，`r2v/v2v/rv2v → Ref2VA`。
- 明确 `<Subject N>` 的本质：Ref2VA 语义主体标签，不是导演台上传素材槽。
- 明确 `<Picture N>/<Video N>/<Audio N>` 是实际素材引用标签，优先通过导演台 `@` picker 获取正确编号。
- 新增“Subject vs Picture”决策规则：身份/可复用内容用 Subject；关键帧/构图/storyboard 锚点才独立追踪 Picture。
- 新增三图连续叙事编译器：Reference identity → Story role → Causal bridge → Timeline → Camera/audio → Official six-section compile。
- 新增跨镜头“因果桥”：上一镜头的最后动作必须为下一镜头的第一动作提供可观察的连接。
- Ref2VA generation `detailed_description` 默认目标提升到官方建议的约 350–500 English words；对白密集任务优先保证完整时间线。
- 新增 Ref2VA 官方 summary task types 映射：`keyframe completion / reference generation / video editing / video continuation / audio reuse / audio reference`。
- 明确 Ref2VA style opening：1–2 个英文句子在 `[Shot 1]` 之前建立整体风格；Base 则在 `[Shot 1]` 开头建立风格。
- 更新 H3 输入限制：Images ≤9；Videos ≤3 且单段 2–15s、总时长 ≤15s；Audio ≤3 且单段 2–15s、总时长 ≤15s；mixed files ≤12。
- 新增 Director common prompt 安全策略：默认每组完整六段式；advanced 模式只把共享 `subject_definitions` 前缀放 common，避免重复 section header。
- 新增 v2v/rv2v 的 `<Video 1>` 源视频处理规则。
- 新增 Codex 安装/上传说明和可复制指令。
- 增强自动测试：精确检查 Base 首行、六段顺序、Speaker/Shot/Ref2VA 关键规则和 Director 文件存在性。
- 交叉验证日期更新至 2026-08-29。

## v1.6 rebuild — 2026-08-11

- 保留全域 H3 生产定位。
- 以 MiniMax 官方 Base / Ref Prompt Guide 作为硬语法源。
- 增加用途路由、生产锁、失败修复、RunningHub/ComfyUI awareness。
