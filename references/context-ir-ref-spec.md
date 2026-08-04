# Context-IR Ref2VA 规范

六段顺序固定：

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

此结构来自官方Prompting Guidance，用于人工模拟Context-IR组织方式，不代表本地模型唯一语法。

标签语义、引用图、音频编号和说话者绑定必须先遵守：

- `ref2va-reference-graph.md`
- `ref2va-audio-numbering.md`
- `ref2va-multireference-enhanced.md`

`detailed_description`普通生成任务通常350–500英文词；只统计该段。`retention_analysis`禁止说话者ID。所有标签一旦定义，六段含义保持一致。
