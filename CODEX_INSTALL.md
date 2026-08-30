# Codex 使用 / 上传说明

## 推荐方式

把解压后的整个 `aiksk-minimax-h3-local-prompt-v1.7-director` 目录交给 Codex，不要只上传 `SKILL.md`。

原因：`SKILL.md` 会引用 `references/official/`、`references/director/`、`references/playbooks/` 和 `templates/`，缺文件会降低规则完整度。

## 给 Codex 的可复制指令

```text
请把这个目录作为 AIKSK MiniMax H3 Prompt Skill v1.7 使用。

执行前必须：
1. 阅读 SKILL.md；
2. 根据任务模式读取 references/official/base-en.txt 或 references/official/ref-en.txt；
3. 如果任务涉及 AIMixer / ComfyUI_MiniMaxH3_Director，再读取 references/director/AIMIXER_DIRECTOR_RULES.md；
4. 不得把 AIKSK 的生产经验伪装成 MiniMax 官方硬规则；
5. 最终提示词必须通过 tests/test_structure.py 中体现的核心规范；
6. 对 r2v/v2v/rv2v，必须正确区分 <Subject N> 与 <Picture N>/<Video N>/<Audio N>；
7. 当用户提供多张同一角色图片时，优先建立一个跨图 Subject 身份，而不是为每张图创造不同角色；
8. 多镜头叙事必须建立 causal bridge：上一镜头的末端状态/动作，要自然导向下一镜头的起始动作。

先运行：python tests/test_structure.py
通过后再使用。
```

## 如果 Codex 要安装成 Skill

保持目录结构完整；Skill root 必须是包含 `SKILL.md` 的这一层。

不要把 `references/official/` 删除，因为它们是硬语法来源。
