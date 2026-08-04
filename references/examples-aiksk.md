# AI-K SK 原创示例

以下示例根据官方规范创作，**不是官方原提示词**。

## Direct I2VA：舞台歌手

```text
Start exactly from the supplied first frame, preserving the singer's face, hairstyle, outfit, stage position, spotlight colors, and microphone placement. Over five seconds, she takes a controlled breath, begins singing with precise lip movement, gently raises her free hand, and leans slightly toward the audience while her hair and jacket respond naturally. The camera pushes in slowly with small amplitude, maintaining stable portrait framing. Audio: a clear female singing voice, subtle breath detail, light stage reverb, faint crowd ambience, and soft instrumental accompaniment. Keep identity and costume stable; no subtitles or watermark.
```

## Enhanced FL2VA：从放下手到比心

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 5.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, clean portrait cinematography, a stable medium shot preserves the woman, her clothing, the softly lit background, and the exact opening composition from Picture 1. She first relaxes her shoulders and shifts her gaze toward the camera. Her forearms then rise smoothly from below the frame, her wrists rotate inward, and her fingers progressively form a heart shape at chest level. During the final second, the remaining pose and framing differences narrow until her hands, facial expression, body angle, and composition land exactly on Picture 2. The camera holds a static shot throughout. A quiet breath and subtle fabric movement remain synchronized with her motion.

overall_soundscape: Soft indoor room tone continues throughout, with a faint breath and light fabric rustle as her arms rise.

non_diegetic_music: N/A
```

## Direct Ref2VA：身份 + 动作 + 音色

```text
Use <Picture 1> for the woman's facial identity, silver-white hair, pale skin, and white futuristic outfit. Use <Video 1> only for the forward explorer stance, arm timing, and camera rhythm; do not copy the source person's face, clothing, or background. Use <Audio 1> only as a reference for the target woman's clear, restrained vocal timbre and measured delivery; do not copy its original words. Create an eight-second cinematic star-ocean exploration scene in which she advances on a futuristic deck, faces a colossal squid rising behind her, steadies her stance, and delivers the supplied Chinese line with synchronized lips. Preserve her identity and outfit throughout. Audio includes her referenced voice, ocean spray, metal deck vibration, deep creature movement, and restrained audience-only orchestral pulses.
```
