# 本地工作流映射

## 官方ComfyUI原生

- `MiniMaxH3ImageToVideo`：T2VA / I2VA / L2VA / FL2VA；依据`first_frame`、`last_frame`连接情况切换。
- `MiniMaxH3ReferenceToVideo`：Ref2VA；输入`ref_images`、`ref_videos`、`ref_video_audios`、`ref_audios`。

### R2V输入

- `ref_images.ref_image_N`：参考图片。
- `ref_videos.ref_video_N`：参考视频画面帧。
- `ref_video_audios.ref_video_audio_N`：同尾号参考视频的配套音轨；无对应视频时不登记。
- `ref_audios.ref_audio_N`：独立音频参考。
- `ref_image_size=match`：保持比例，只缩小到生成画布像素面积。
- `ref_image_size=max`：保持比例，只缩小到短边最多2048，身份细节更强但更慢。

官方R2V模板当前只接`ref_image_0`和`ref_image_1`；其余视频/音频输入为空。

## AI-K SK／RunningHub兼容

RH节点命名可能与原生不同。若工作流无法自动识别，手工创建`examples/manual-ref-config-schema.json`格式的接线清单，再用Manifest生成器计算标签。禁止凭工作流文件名推断Audio编号。
