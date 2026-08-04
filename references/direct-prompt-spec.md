# Direct 直接运行版规范

Direct 不是“少写”，而是把结构隐藏在自然语言里。

## 通用顺序

1. 风格、场景、初始构图。
2. 主体身份和关键锚点。
3. 依时间发生的可见动作。
4. 相机动作。
5. 同步对白、音效、环境声、配乐。
6. 连续性和禁止项。

## T2VA模板

```text
[Style and opening composition]. [Subject and environment]. Over the full [duration]-second shot, [observable action path]. The camera [natural movement]. Audio: [dialogue/diegetic sound/ambience/music relationship]. Maintain [continuity constraints]. No subtitles or watermark unless explicitly requested.
```

## I2VA模板

```text
Start exactly from the supplied first frame, preserving the subject identity, clothing, colors, composition, key objects, and spatial relationships. Over [duration] seconds, [action begins and develops]. The camera [movement]. Audio: [synchronized sound]. Keep motion continuous and physically plausible.
```

## L2VA模板

```text
Build a plausible preceding state and action, then gradually converge so the final moment lands exactly on the supplied last frame. Preserve the last-frame identity, clothing, scene geometry, colors, pose, and composition. [Action path]. The camera [movement]. Audio: [synchronized sound].
```

## FL2VA模板

```text
Start exactly from the supplied first frame and continuously transition to the supplied last frame at the end of the [duration]-second video. Preserve identity and scene continuity while [explicit intermediate changes]. Prefer one continuous shot. The camera [movement]. Audio: [synchronized sound].
```

## Ref2VA模板

```text
Use <Picture 1> for [identity/scene/style], <Video 1> for [action/camera/timing], and <Audio 1> for [voice/rhythm/sound]. Create a [duration]-second [style] video in which [target timeline]. Preserve [must-keep attributes], transfer only [specified attributes], and do not copy [unwanted source attributes]. Audio: [copy/reference relationship].
```

不要引用不存在的标签。普通带声视频是否单独形成 `<Audio N>` 取决于工作流接法，不能自动假定。
