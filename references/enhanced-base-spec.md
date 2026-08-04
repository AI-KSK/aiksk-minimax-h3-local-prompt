# Enhanced 基础模式规范

适用：T2VA、I2VA、L2VA、FL2VA。

## 固定结构

T2VA直接从三个字段开始：

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

I2VA第一行必须是：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

FL2VA第一行必须按实际时长和最后镜头替换：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

L2VA第一行必须按实际时长和最后镜头替换：

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

首行后空一行。`S.SS`严格两位小数；`N`必须等于主描述中的实际最后 Shot。

## Shot规则

- `[Shot 1]` 不写时间戳。
- 后续：`[Shot 2] At 00:03.500, the camera cuts to...`
- Shot编号从1连续递增。
- 时间戳严格递增，且小于总时长。
- 仅改变距离或小角度时优先运镜，不滥用切镜。
- FL2VA默认优先单镜头连续插值。

## 关键帧路径

- I2VA：首帧锚定 → 动作开始 → 连续发展 → 结果或反应。
- L2VA：合理前态 → 明确过渡 → 最后阶段收束 → 精准落到尾帧。
- FL2VA：首帧状态 → 中间可观察变化 → 差异逐步缩小 → 尾帧状态。

## 三个字段

### integrated_multimodal_description

沿时间写可见、可听内容：风格、构图、主体、动作、镜头、对白、唱歌、剧情内音乐、同步音效。

### overall_soundscape

1–4句连续英文，写环境声、物理动作声和非语言人声。只有用户明确要求完全静音时才写 `N/A`。

### non_diegetic_music

1–3句，写角色听不到、观众听到的配乐。无配乐写 `N/A`。不要只写“epic/emotional”，要写乐器、速度、节奏和动态。
