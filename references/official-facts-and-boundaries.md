# 官方事实与边界

截至本技能 v1.1 编写时，MiniMax H3 官方模型卡说明：

- H3-Base-FL2VA 支持无图、首帧、尾帧、首尾帧输入。
- H3-Base-Ref2VA 支持图片、视频和音频参考。
- 输出为视频 + 32 kHz 立体声音频，24 FPS，4–15秒。
- H3-Context-IR 与 H3-Regenerate-2K 不包含在当前开放权重本地发布中。
- 本地 H3-Base 主要验证768p链路；完整2K工作流依赖额外系统或API。
- 权重采用 MiniMax H3 Community License Agreement，应称“开放权重”，不要默认等同宽松开源许可证。

Ref2VA输入限制：

- 图片≤9。
- 视频≤3；每段2–15秒；总时长≤15秒。
- 音频≤3；每段2–15秒；总时长≤15秒。
- 音频必须与图片或视频共同输入，不能单独使用。
- 文件总数≤12。

官方来源见 `official-sources.md`。
