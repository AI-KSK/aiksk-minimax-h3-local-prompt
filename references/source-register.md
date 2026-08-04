# 来源登记 v1.4

检索与复核日期：2026-08-04。

| 等级 | 来源 | 用途 |
|---|---|---|
| A | MiniMaxAI/MiniMax-H3 model card：`https://huggingface.co/MiniMaxAI/MiniMax-H3` | 模型模式、输出规格、图片/视频/音频数量和时长边界 |
| A | Ref提示词指南：`https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md` | Subject/Picture/Video/Audio语义、六段结构、音频copy/reference、说话者规则 |
| A | Base提示词指南：`https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md` | Shot、时间戳、对白、声音与配乐规则 |
| A | ComfyUI官方实现：`https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_minimax_h3.py` | 官方节点输入、参考遍历顺序、视频—音轨配对、标签登记顺序、缩放和截帧行为 |
| A | 本次源码快照提交：`9a9fdb10ed144ce760d9682cb247526ea23cc525` | 将2026-08-04复核结果固定到具体ComfyUI代码快照 |
| A | 官方R2V模板：`https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json` | 官方模板实际接线与示例说明 |
| A | 用户上传R2V工作流SHA-256：`099d24eda6263854818975c7209db6f29ebfd0339936c928f12293d5ab029ffb` | 验证当前文件实际只连接两张参考图，视频和音频输入为空 |
| C | 重复社区实测 | 只能形成待验证假设，不进入硬规则 |

## 证据冲突处理

模型卡规定参考视频/音频2–15秒、视频≤3、音频≤3且音频不能唯一输入；ComfyUI源码的运行时边界与Autogrow接口可能更宽。生产规则以模型卡为硬边界，源码行为只用于解释当前实现、标签顺序和风险。

## 自定义节点边界

`ref_video_audio_N`优先登记、独立`ref_audio_N`随后登记的算法，是对官方`MiniMaxH3ReferenceToVideo`源码的结论。RunningHub/RH或第三方节点如果没有逐行核对源码，只能使用`manual-ref-config-schema.json`建立手工映射，不得声称标签顺序与官方实现一致。
