# 对白、音频与运镜

## 说话者

```text
The young woman with a clear, soft voice (S1) says: <d>[Chinese] 我们出发吧。</d>
```

规则：

- 同一发声者跨镜头保持同一 `(Sx)`。
- 多人同时说话可写 `(S1,S2)`。
- `<d>` 内只放 `[Language]` 与用户原话。
- 完整句应保留句末标点。
- 不发声的人不要分配编号。

## 画外音

使用固定短语：

```text
says in an off-screen voiceover
```

对应人物在画面里时，紧接对白说明嘴唇保持闭合。

## 跨镜头对白

- 跨切镜使用 `<scenetrans>`，并明确声音跨镜头连续。
- 被视频末尾截断使用 `<cutoff>`。

## 画面文字

画面中实际出现的文字用英文双引号包围，原文和标点不变，例如：

```text
A sign reading "营业中" glows above the doorway.
```

## 音频分层

- `integrated_multimodal_description` / `detailed_description`：对白、唱歌、现场乐器、手机/电视/广播音乐、与动作同步的音效。
- `overall_soundscape`：全片环境底噪、脚步、衣料、机械、风雨、呼吸、碰撞等汇总。
- `non_diegetic_music`：角色听不到的观众配乐。

## 运镜

| 中文 | 推荐英文 |
|---|---|
| 推近 / 拉远 | Push In / Pull Out |
| 变焦 | Zoom In / Zoom Out |
| 水平摇镜 | Pan Left / Pan Right |
| 平移 | Truck Left / Truck Right |
| 俯仰 | Tilt Up / Tilt Down |
| 垂直升降 | Pedestal Up / Pedestal Down |
| 环绕 | Arc Shot |
| 跟拍 | Tracking Shot |
| 固定 | Static Shot |
| 抖动 | Shake Slightly / Shake Strongly |
| 主观 | POV |
| 旋转 | Roll Clockwise / Roll Counterclockwise |

自然句式：

```text
The camera pushes in with small amplitude at slow speed toward her face.
```

不要写成标签堆叠。不要同时写 `static shot` 与持续平移、环绕、推进。
