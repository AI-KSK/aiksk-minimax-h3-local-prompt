# Changelog

## v1.7.1 — 2026-08-30

- 恢复 v1.6 的 Response modes 路由（v1.7 重构时遗失）：只要提示词就只给可复制提示词；要工作流产出则给 Family / Director task / Profile / Duration / Asset map / Reference map / Locks / Final prompt / Validation risks；要多版本则默认 `official_full` + `official_compact` + 一个任务相关 profile，不产出只换形容词的伪变体。
- 该段以 `Layer 14 — Response modes` 插入，原 Supporting files 顺延为 Layer 15。
- 字段名对齐 v1.7 术语：v1.6 的 `Mode` / `Intent classes` 改为 `Family` / `Director task`。
- `tests/test_structure.py` 增加 Response modes 存在性校验。
- 交叉验证日期不变，仍为 2026-08-29；本版只恢复文档段落，未改动任何官方语法结论。

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
- 新增 Codex 安装/上传说明和可复制指令（`CODEX_INSTALL.md`、`AGENTS.md`）。
- 新增 `MANIFEST.json`：文件清单 + sha256 完整性校验。
- 新增 `templates/director_r2v_master.txt` 与 `examples/director_r2v_10s_three_image_story.txt`。
- `templates/ref2va_master.txt` 从空段名骨架扩写为带角色注释的可填写骨架。
- 增强自动测试：精确检查 Base 首行、六段顺序、Speaker/Shot/Ref2VA 关键规则和 Director 文件存在性，通过输出 `OK v1.7`。
- README 重写为 v1.7 门面页，新增导演台映射表、Subject/Picture 语义、因果桥、common prompt 策略与 v1.6 升级说明。
- 交叉验证日期更新至 2026-08-29，来源扩展到四层：MiniMax Base Guide、MiniMax Full-reference Guide、MiniMax + ComfyUI 运行时文档、AIMixer Director README。

## v1.6 rebuild — 2026-08-11

- Kept the original v1.6 product name and broad all-domain positioning.
- Rebuilt the core hierarchy from scratch.
- Preserved official MiniMax H3 base/ref prompt guides as hard grammar sources.
- Added 50-use-case production router.
- Added task profiles: official_full, official_compact, director, identity_lock, edit_lock, motion_reference, audio_control, creative_max.
- Added reference conflict priority and production lock system.
- Added prompt repair engine.
- Added dedicated playbooks for Ref2VA, dialogue/audio, camera/action, and failure repair.
- Removed the universal >10s dialogue hard rule; official H3 supports 4–15s output.
- Kept H3-Context-IR clearly separate from local prompt heuristics.
- Added cross-validation and source register.
