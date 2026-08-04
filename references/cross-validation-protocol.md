# v1.4真实生成交叉验证协议

## 目的

验证不同提示词Profile和多参考职责写法的真实生成差异。静态校验、示例视频、模拟评分不得当作质量结论。

## 冻结项

模型权重与哈希、文本编码器、VAE、ComfyUI提交、工作流哈希、分辨率、帧数、采样器、加速、硬件、全部参考素材哈希、标签Manifest、语义锁、Prompt Profile和Seed。

## Profile

- direct
- concise_structured
- context_ir_emulation

三者必须保持同一目标语义、素材职责、对白原文、镜头数和排除项。

## 多参考专项评分（0–5）

1. `label_accuracy`：提示词标签与实际接线一致。
2. `role_isolation`：每份素材只影响指定职责。
3. `identity_consistency`：目标人物身份稳定。
4. `motion_transfer`：目标动作与视频参考的一致性。
5. `camera_transfer`：运镜与构图节奏迁移。
6. `audio_source_accuracy`：配套音轨和独立音频未串号。
7. `speaker_binding`：声音正确绑定目标人物。
8. `av_sync`：动作与声音时间关系。
9. `attribute_leakage`：是否错误带入视频源人物、服装、背景、声音或台词。
10. `overall_quality`：可用性总评。

硬失败：标签引用不存在、错音色绑定、目标人物被源视频人物替换、完全无目标动作、无应有音轨、严重音画错位。

## 设计

每类任务至少3个Case，每Case至少3个匹配Seed；随机盲化；至少2名评审；按Case→Seed两阶段bootstrap；单环境最高provisional；第二独立环境方向一致后才能写supported_replicated。
