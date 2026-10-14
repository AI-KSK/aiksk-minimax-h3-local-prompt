# JOKER141 武打 LoRA 触发词决策（2026-10-13 交叉核查）

此表依据 JOKER141 官方 Hugging Face 模型卡；属于 **LoRA 模型使用约定**，不属于 MiniMax H3 官方语法字段。输出时将所选触发词并入动作描述/开头自然语句，不新建 `lora:` / `triggers:` 等官方提示词字段。

| LoRA | 默认策略 | 可选策略 | 证据 |
|---|---|---|---|
| Combat V2 | **不加入**触发词，优先人体稳定 | 强动作 `prfight2`；重终结特技 `prfight2, prfin1`；需要对白时尽量先完成动作再说台词 | [Combat V2](https://huggingface.co/JOKER141/MiniMax-H3-Combat-Base-V2) |
| Weapon Combat V1 | 非零权重时加入 `BUNNY` | 当前版建议单独用，不默认与 Combat/Motion 等强动态叠加 | [Weapon](https://huggingface.co/JOKER141/MiniMax-H3-Weapon-Combat-LoRA) |
| GunFu | 非零权重时加入 `BUNNY` | 可与 Combat/Motion 构成枪斗实验；属电影叙事而非现实战术教学 | [GunFu](https://huggingface.co/JOKER141/MiniMaxH3-GunFu-Gunfight-LORA) |
| Motion Repair V2 | 不加入触发词 | 实验可加 `bunny_crisp_motion`，作者声明非必须 | [Motion](https://huggingface.co/JOKER141/MiniMax-H3-General-Motion-Continuity-Repair) |
| Fight Flow V1 | 非零权重按**主导互动逻辑**选一个 | 徒手 `Unarmed combat interaction`；兵器 `Melee weapon interaction`；枪斗 `Gun-fu interaction` | [Fight Flow](https://huggingface.co/JOKER141/H3-Fight-Flow-Fight-Interaction-LoRA) |

## 硬性选择规则

1. 禁止把全部五类触发词无条件拼到同一提示词。只有启用的 LoRA 可以带它对应的触发词。
2. Fight Flow 的三个触发词只选 **一个**，由战斗主导交互方式决定，不由道具存在与否决定。
3. Combat 默认为不触发；`prfin1` 要与 `prfight2` 联合用，不要把它当标准必填。
4. Weapon/GunFu 的 `BUNNY` 有重合，多个启用时去重；但 Weapon 与其他强动态 LoRA 混用默认应阻止，除非用户显式安排兼容性试验。
5. Motion 的 `bunny_crisp_motion` 不可强制，它是可选消融变量。
6. 触发词 **不能** 代替人物归属、接触后果、脚步与时间轴、音效同步的动作说明。
7. 实验性权重仅作为起始值，不应把作者单模型/单阶段建议误写成多 LoRA + Veda 已验证最优。
