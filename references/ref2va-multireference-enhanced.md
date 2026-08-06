# Ref2VA 多参考增强规范 v1.5

## 一、先生成素材编号表

没有编号表，不写最终提示词。编号必须来自工作流或明确手工清单。

```text
Picture 1 = ref_image_0 = 人物面容与发型
Picture 2 = ref_image_1 = 服装
Video 1 = ref_video_0 = 动作与镜头节奏
Audio 1 = ref_video_audio_0 = 动作声时间关系
Audio 2 = ref_audio_0 = 女声音色
S1 = 目标女角色
```

## 二、定义Subject

```text
<Subject 1> is the female swordswoman whose facial identity and hairstyle come from <Picture 1>, whose white combat costume comes from <Picture 2>, and whose body choreography is guided by <Video 1>.
```

不要把`<Video 1>`本身当作人物；人物动作可作为Subject属性或独立Subject。

## 三、定义Video与Audio

```text
<Video 1> is the body-motion, shot-timing, and low-angle tracking-camera reference; the source performer's identity, clothing, body shape, and environment are excluded.
<Audio 1> is the synchronized physical-sound reference paired with <Video 1>, used only for footsteps, sword whooshes, impacts, and their timing.
<Audio 2> is the voice-timbre and emotional-delivery reference for <Subject 1> (S1); its original words are not copied.
```

## 四、Summary任务类型

- `reference generation`：只参考身份、动作、镜头、风格、音色。
- `keyframe completion`：图片是具体首帧/尾帧/关键帧。
- `video editing`：直接修改原视频。
- `video continuation`：从原视频末尾继续。
- `audio reuse`：音频信号直接复用。
- `audio reference`：只参考音色、节奏或声音质感。

任务可组合，但不能因为输入里“有视频/音频”就自动写video editing或audio reuse。

## 五、Retention

视觉：`fully_preserved`、`partially_preserved`、`attribute_transfer`、`weak_reference`。

音频：`fully_copy`、`partially_copy`、`reference`、`weak_reference`。

每个需要单独追踪的标签写一行。`retention_analysis`不写`(Sx)`。

## 六、Detailed Description

1. 先写总体风格1–2句。
2. `[Shot 1]`无时间戳；后续Shot用`At MM:SS.mmm`。
3. 每个Shot写构图、位置、光线、动作变化、相机、声音和参考标签生效点。
4. 普通生成通常350–500英文词；编辑任务按复杂度，不机械凑字数。
5. 第一次出现重要Subject时写清可见参考特征；后续保持同一标签。
6. 声音来源在实际生效的Shot或音频阶段引用。

## 七、声音与对白

```text
<Subject 1> (S1) says in the clear, restrained female voice referenced from <Audio 2>, <d>[Chinese] 别挡我的路。</d>
```

若Audio 2只提供音色，不得把原音频台词带入。完整句在`</d>`前保留句末标点。

## 八、完整最小结构

```text
subject_definitions:
[definitions]

summary:
[task prefix + target + main relationships]

retention_analysis:
[one line per tracked reference]

detailed_description:
[style + shots + actions + sound + dialogue]

overall_soundscape:
[ambience and physical sounds]

non_diegetic_music:
[audience-only score or N/A]
```
