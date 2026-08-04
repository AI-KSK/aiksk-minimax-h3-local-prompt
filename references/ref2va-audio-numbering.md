# Ref2VA 音频编号与说话者绑定

## 1. 四套名称不要混用

| 名称 | 层级 | 示例 | 含义 |
|---|---|---|---|
| 节点端口 | ComfyUI接线 | `ref_video_audio_0` | 与尾号0的视频配对的音轨输入 |
| 提示词音频标签 | 模型参考源 | `<Audio 1>` | 第一个被登记的音频参考信号 |
| 视频标签 | 模型参考源 | `<Video 1>` | 第一个被登记的视频参考 |
| 说话者ID | 目标视频声源 | `(S1)` | 目标视频中第一个实际发声者 |

## 2. 官方ComfyUI标签分配算法

```text
Picture labels:
按已连接 ref_image 输入顺序连续编号。

Video labels:
按已连接 ref_video 输入顺序连续编号。

Audio labels:
第一阶段：遍历已连接 ref_video；若同尾号 ref_video_audio 已连接，先为该音轨分配下一个 Audio 标签。
第二阶段：所有视频处理完成后，再按已连接 ref_audio 输入顺序分配后续 Audio 标签。
```

## 3. 情形表

### A. 视频无音轨＋独立音频

```text
ref_video_0       → <Video 1>
ref_audio_0       → <Audio 1>
```

### B. 视频有配套音轨＋独立音频

```text
ref_video_audio_0 → <Audio 1>
ref_video_0       → <Video 1>
ref_audio_0       → <Audio 2>
```

### C. 两个视频均有音轨＋独立音频

```text
ref_video_audio_0 → <Audio 1>
ref_video_0       → <Video 1>
ref_video_audio_1 → <Audio 2>
ref_video_1       → <Video 2>
ref_audio_0       → <Audio 3>
```

注意：Video和Audio独立编号，因此同一来源文件可对应`<Video 1>`与`<Audio 2>`，编号不同不表示来源不同。

### D. 只接视频音轨，不接对应视频

```text
ref_video_audio_0 → 不登记；无有效<Audio N>
```

## 4. 声音引用

```text
<Audio 1> is used only as a reference for footsteps, impacts, and their timing relative to <Video 1>.
<Audio 2> is the voice-timbre and emotional-delivery reference for <Subject 1> (S1), without copying the original words.
```

## 5. Copy与Reference

- `fully_copy`：完整源音轨作为完整最终音轨。
- `partially_copy`：只复制一部分时间或层，或在复制后增删混音。
- `reference`：不复制信号，只参考音色、节奏、音乐风格、台词内容或音效质感。
- `weak_reference`：只保留宽泛类别或氛围。

## 6. 禁止项

- 禁止写`ref_audio_0`来代替`<Audio N>`。
- 禁止认为`ref_audio_0`永远是`<Audio 1>`。
- 禁止用`<Audio 1>`代替`(S1)`。
- 禁止音色参考时自动复制原台词。
- 禁止在`retention_analysis`中写`(Sx)`。
