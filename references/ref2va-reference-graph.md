# Ref2VA 引用关系图

## 数据结构

每个参考源至少记录：

```text
label:
source_port:
source_asset:
role:
target:
retention_mode:
active_time_or_shots:
exclude:
confidence:
```

## 角色拆分

图片可承担：身份、面容、发型、服装、道具、场景、风格、构图、具体关键帧。

视频可承担：动作、表演节奏、镜头运动、切镜、空间变化、原视频编辑、原视频续写。视频中的人物或物体若作为可见内容复用，仍建立`<Subject N>`。

音频可承担：完整复用、部分复用、音色、情绪、节奏、台词/歌词内容、动作声音、环境声、音乐风格或连续性。

## 多源定义一个Subject

```text
<Subject 1> is the woman whose facial identity and hairstyle come from <Picture 1>, whose costume comes from <Picture 2>, and whose body movement is guided by the performer in <Video 1>.
```

必须补排除项：

```text
The original performer identity, clothing, body shape, and background from <Video 1> are not transferred.
```

## 一源定义多个Subject

同一张场景图可分别提供：人物、车辆、环境和光线。不要把整张图机械定义成一个Subject；按目标中需要稳定追踪的内容拆分。

## Picture与Subject区别

图片只作为人物来源：

```text
<Subject 1> is the woman in <Picture 1> ...
```

图片本身是首帧或构图锚点：

```text
<Picture 1> is the opening frame of [Shot 1] ...
```

## Video与Subject区别

```text
<Video 1> is the temporal-structure and camera-motion reference.
<Subject 2> is the sword-fighting action demonstrated in <Video 1>.
```

Video标签跟踪整段来源；Subject跟踪目标中实际复用的可见内容。
