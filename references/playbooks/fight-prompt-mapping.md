# 九组预设与提示词 / 工作流同步规范

## 配置来源与边界

- 固定 9 组：A0–A8，不改变用户原始工作流的数字编号 0–8。
- 额外 `BASE` **不是第十组常用预设**，是用“手动覆盖 + 五项全零”实现的对照状态；Turbo/Veda 继续启用。
- 触发词读取 `fight-trigger-policy.md`；实际权重读取 `fight-lora-presets.json`，不要手工复制不同版本数值。
- Prompt 输出遵循官方 Base 三字段 / Ref2VA 六段式，词语来源区分官方指南与 JOKER141 LoRA 模型卡。
- **ComfyUI 实时切换预设编号不会同步改写文本**。本 Skill 提供离线导出工具同步模式、预设和提示词；在 ComfyUI UI 内手动改预设后必须相应更新文本。否则两者不再匹配。

## 路由与题材

| 配方 | 题材 | 必须体现 | 默认触发词 |
|---|---|---|---|
| A0 | 徒手 | A 出拳 → B 格挡 → B 反击 → A 恢复 | 无 |
| A1 | 徒手+修复 | 重心、落脚、转向 | 无（Motion 词可选） |
| A2 | 徒手交互 | 持续双方攻防、主动权转换 | `Unarmed combat interaction` |
| A3 | 综合徒手 | 攻防+动作连续性，避免过载 | `Unarmed combat interaction` |
| A4 | 刀剑兵器 | 武器唯一主人、握持手、刀剑接触、离合、收势 | `BUNNY` |
| A5 | 枪斗 | 电影场面，枪械归属和动作后果 | `BUNNY` |
| A6 | 连续枪战 | 枪斗 + 肢体衔接 | `BUNNY` |
| A7 | 近身枪斗 | 电影式近距离动作、控枪归属、格挡和恢复 | `BUNNY` |
| A8 | 通用动作 | 跑酷、空翻、落地或角色动作连续 | 无（Motion 词可选） |
| BASE | 默认徒手控制 | 不启用专项 LoRA 的相同场景 | 无 |

## 程序化生成/同步

完整命令：

```bash
python scripts/sync_fight_workflow.py --preset A4 --mode R2VA --workflow integrations/AIKSK_H3_JOKER141_九预设_T2VA_R2VA_Veda_单阶段.json --output output/H3_A4_R2VA_weapon.json
```

运行会：① 从 JSON 读取权重/场景/触发词；② 生成符合所选模式的武打提示词；③ 同步设置控制节点与 Prompt 输入，保存新 JSON；④ 写旁路审计文件 `.audit.json`。原输入文件不覆盖。

`--preset BASE` 通过手动全零覆盖实现，而不是改变 A0–A8 的编号。`--combat-trigger intense/finisher` 和 `--motion-trigger` 可选择可选触发词；若所选 LoRA 权重为零则不会加入其触发词。`--fighter-a` / `--fighter-b` 可在文本中补充用户明确给出的角色信息；没有素材信息时 R2VA 不臆造面部、衣着。

这属于 **离线生成时的同步**，不是 ComfyUI 运行时监听，也不是由 Skill 自动修改已经打开的 ComfyUI 页面。
