# v1.5快速卡

```text
先读工作流 → 生成Manifest → 列Picture/Video/Audio/Speaker表 → 分职责 → 写提示词 → 用Manifest校验
```

音频编号：

```text
每个已连接视频的同号配套音轨先占Audio号
→ 视频占Video号
→ 全部视频完成后，独立音频继续占Audio号
```

关键区别：

```text
<Audio N> = 参考声音来源
(Sx)      = 目标视频实际发声者
```

硬依赖：

```text
ref_video_audio_N 必须有 ref_video_N
```

常用：

```bash
python scripts/build_ref2va_manifest.py --workflow workflow.json --output refs.json
python scripts/validate_h3_prompt.py prompt.txt --mode ref2va --profile direct --manifest refs.json
```
