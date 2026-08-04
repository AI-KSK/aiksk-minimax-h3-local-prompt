# 官方提示词保留规则

用户的演示要求是：有官方提示词时优先使用官方原文。

## 操作顺序

1. 获取官方工作流 JSON。
2. 运行：

```bash
python scripts/extract_workflow_prompts.py video_minimax_h3_i2v.json --out-dir extracted
```

3. 查看终端候选项，确认真正的 prompt 节点。
4. 将提取结果原样粘贴到目标工作流。
5. 不修正拼写、不重排句子、不改标点，除非用户明确要求。

## 标注

- `官方原提示词`：从官方 JSON 逐字提取。
- `AI-K SK改写提示词`：根据官方规范重新创作。
- `官方结构模板`：只保留官方字段/首行规则，不代表正文为官方原文。

不得把 AI-K SK 自创示例叫作“官方提示词”。

## 官方模板地址

见 `official-sources.md`。脚本本身不联网，只读取用户已经下载的 JSON。
