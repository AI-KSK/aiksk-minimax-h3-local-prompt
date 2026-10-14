# AIKSK H3 武打编排专项（Fight Choreography）

**地位**：AIKSK 生产启发式 / 领域知识，不是 MiniMax 官方新增语法、模型能力承诺或任何 LoRA 的效果保证。

**任务**：把用户的“打斗、武戏、武术、双人攻防、刀剑、枪斗、跑酷、动作修复”需求，编译为有因果、有接触、有空间关系的 H3 官方格式提示词。**先定人物和动作，再做运镜、声音和风格。**

## 0. 触发与读取顺序

当用户提及武打、功夫、打戏、武侠、格斗、对打、拳脚、刀剑、枪斗、特技、动作连续性、JOKER141 或 Work-Fisher 时启用本模块。

1. 先读取 `SKILL.md` 的官方模式路由。
2. Base T2VA/I2VA/FL2VA/L2VA 使用 `references/official/base-en.txt`；Ref2VA / Director r2v/v2v/rv2v 使用 `references/official/ref-en.txt`。
3. 素材有导演台映射时严格依 `@` picker 编号；不猜测 `<Picture N>`、`<Video N>`、`<Audio N>`。
4. 再读取本板块和 `references/playbooks/fight-lora-presets.json`。**LoRA 与 Veda 参数仅作为工作流外部配置建议，不要输出为新的 H3 语法段落。**
5. 最后编译为官方 Base 三字段或 Full-reference 六段式；只输出用户请求的形式。

## 1. 四条战斗题材路由

| 题材 | 主目标 | 动作词重点 | 首选实验预设 | 禁忌 |
|---|---|---|---|---|
| A. 徒手真实拳脚 | 重心、接触、攻守 | jab, slip, parry, step-in, elbow, recoil, reset | A0 / A2 | 瞬移、凭空踢中、无受击反馈 |
| B. 双人连续格斗 | 连招衔接、主动权转移 | probe → defend → counter → stagger → recover | A2 / A3 | 两人同时无限进攻、角色互换 |
| C. 兵器武戏 | 握柄/刀刃归属、接触点、空间轴线 | draw, thrust, bind, deflect, disengage | A4（Weapon only） | 武器凭空复制/穿手/随意换手 |
| D. 枪斗/枪械动作 | 近身控制与动作衔接 | aim, cover, disarm, reposition | A5 / A6 / A7 | 把动作段落写成真实世界的战术教学 |

Motion Repair V2 的 A8 适用于跑酷、翻滚、杂技等动作连续性实验。题材路由用来确定提示词与测试组，**不能从权重值推出保证的质量提升**。

## 2. 角色、场景与武器状态账本（先在内部建立）

每一条片段先固定：

- **Fighter A / Fighter B**：独立身份；脸型、发型、上衣、下装、标志物与身高比例。Ref2VA 分别使用一个 `<Subject N>`。
- **屏幕轴线**：开场 A 在屏幕左侧、B 在右侧；双方朝向何处；只有写出绕拍或过轴镜头才允许改左右关系。
- **行动归属**：谁先攻击、用哪只手/哪件武器、击向哪里；谁用什么肢体格挡；谁失去重心；下一拍从何处恢复。
- **接触几何**：明确身体或兵器的**接触点**与方向、接触后的动量/反应，不写只有“激烈交锋”的空话。
- **武器物理**：数量不变，主人不变；握持手、刀刃方向、武器落地/换手需明确过渡；禁止多出武器。
- **环境锚点**：门、柱、台阶或地面标记，用于保留人物距离、屏幕方向和落脚位置。
- **衣服/发丝**：可以随动作飘动，**不等于角色换衣或换脸**。

一个简短内部状态账本示例（不要原样复制进最终 H3 提示词）：

| Beat | A 的状态 | B 的状态 | 接触/方向 | 下一步因果 |
|---|---|---|---|---|
| 1 | 左侧右脚前踏 | 右侧上身后撤 | A 左拳向 B 肩侧探击 | B 抬左前臂 |
| 2 | 左拳被格挡、重心仍向前 | 左前臂挡开拳头 | 前臂接触 | A 顺势转髋 |
| 3 | A 旋髋侧踢 | B 后退并以双臂护住肋侧 | 护挡承受冲击 | B 转移到左脚、准备回击 |
| 4 | A 收腿稳定站立 | B 左脚蹬地向前反击 | 双方再度接近 | 最后维持两人可辨识姿态 |

注意：这一账本是**编剧层验证工具**，不是 JSON、模型控制骨架或精确物理仿真输入。

## 3. 核心动作因果公式

推荐：`起始站位 → 攻击预备动作 → 攻击轨迹 → 接触/有效格挡 → 受击反馈与重心变化 → 恢复站姿/转换主动权 → 下一招或结局`。

正例：`A steps from screen left and throws a right straight punch toward B's chest; B turns left and parries with the outside of the left forearm; the redirected punch carries A forward, so B pivots off-line and counters with a short right hook; A recoils, regains footing, and raises the guard.`

反例：`They fight fast with crazy acrobatic combos, rotating camera, sparks everywhere.`

每一拍最好只有 **1 次可辨识的主要攻击 + 1 次可辨识的防御/反应**；不要把十几种招式挤在一秒里。角色失去平衡时要说明落地或恢复，不要让下一帧无过渡重回站姿。

## 4. 按有效时长编排（24fps；实际以工作流帧格为准）

### 4.1 短档：约 5.17s / 124 帧（默认首测）

- 0.00–1.00：站位、距离、眼神、起手预备。
- 1.00–2.20：A 主动攻击，B 完成可看清的有效格挡。
- 2.20–3.65：B 反击，A 闪避/受击并出现可观察的重心变化。
- 3.65–5.17：双方恢复或定格到明确结尾，不增添新人物/新武器。

**只编排一轮明确交换**；宁可 3–4 个真实动作也不要 12 个模糊动作。必要时单镜头 + 平稳横向跟拍。

### 4.2 中档：约 10s（按实际有效帧数重算）

以 5–6 个节拍构成：试探 → 第一次格挡 → 主动权转换 → 环境/脚步变化 → 第二次有效接触 → 分开收势。若剪切镜头，上一镜出拳或格挡的末态必须在下一镜接上。

### 4.3 长档：约 15s / 八拍武打（Work-Fisher 风格的编排参考）

1. 定位和试探：先建立人物、空间与距离。
2. A 首次有效进攻，B 有明确格挡。
3. B 抓住破绽反击，A 被迫失去主动权。
4. A 受压后转位、重新获得立足点。
5. A 调整节奏展开第二轮攻击。
6. B 再次取得短暂优势；不是单方面连续挨打。
7. 双方完成最后一次可辨识的接触、格挡或反制。
8. 动作落地并以稳态结尾，明确谁在什么位置、手中有什么武器。

**八拍是叙事节奏，不要求生成 8 个镜头、8 次剪辑或者每拍等长。**

## 5. 镜头、动态与音画同步

- 中景/全身宽景通常比碎切特写更容易检查脚步、双人距离、肢体完整性。
- 默认保持一条可读空间轴线；复杂环绕镜头必须交代机位改变后的空间关系。
- 短视频最多一个主要运镜（横跟/小幅推进/平移）；激烈搏斗优先让**人物运动**承担速度感。
- 有实体接触才有拳击/兵器撞击音，反应音应发生在接触之后，脚步与落地声需匹配动作。
- 不需要对白时不分配 `(S1)`/`(S2)`；需要对白才加入稳定发言者 `(Sx)`，台词仍写 `<d>[Chinese] ...</d>`。
- 武戏音效重在节奏和层次：脚步 → 衣料摩擦 → 接触声 → 呼气/喘息 → 环境余音。`overall_soundscape` 不重复台词；配乐单列 `non_diegetic_music`。
- 真实风格优先人体重心、清楚接触、少粒子/光效。玄幻风格可添加能量轨迹，但必须保持武器归属和可理解的实际动作。

## 6. Ref2VA、Director 和动作参考

**双人参考图**：分别为两人建立 `<Subject 1>` / `<Subject 2>`； `<Picture 1>` 和 `<Picture 2>` 只是具体素材。若图片只证明人物身份，**不强行在 `subject_definitions` 中另建独立 Picture 锚点**；如兼任开场/收尾构图才单独定义 Picture 角色。

**动作参考视频**：若 `<Video 1>` 只提供身法、节奏或机位，则标记为动作参考，默认不要保留源视频的面孔/服装/场景；`summary` 使用 `reference generation`（当生成任务与输入关系对应时），**不要把动作迁移误写成 `video editing`**。

**视频编辑**：只有目标确实编辑 `<Video 1>` 才使用 `video editing` 和相应官方编辑开头句。

**图片顺序**：Director 素材槽索引和 `@` picker 是真值；两人左右站位与编号不是一回事。不可假设 Picture 1 一定左侧。

**必须守住官方语法**：Base 使用 `integrated_multimodal_description: / overall_soundscape: / non_diegetic_music:`；Ref2VA 使用 6 节。`fighter_ledger:`、`motion_beats:` 等仅可作为内部编排草稿，不得写成官方顶层字段。

## 7. JOKER141 九组 LoRA 预设知识（只读配置）

配方准确数据在 `references/playbooks/fight-lora-presets.json`，字段顺序是 Combat V2、Weapon V1、GunFu、Motion Repair V2、Fight Flow V1。**所有值是 ComfyUI `LoraLoaderModelOnly.strength_model`；不是提示词 token、Veda 稀疏率或 CFG。**

- A0：徒手基础，Combat 0.65。
- A1：Combat 1.0 + Motion V2 0.5（动作修复实验）。
- A2：Combat 0.65 + Fight Flow 0.65（双人攻防）。
- A3：Combat 0.70 + Motion V2 0.50 + Fight Flow 0.65（综合高动态，优先关注权重冲突）。
- A4：Weapon 0.45（**兵器 LoRA 单用**，防止强动态先验混用）。
- A5：GunFu 0.90（枪斗）。
- A6：GunFu 0.90 + Motion V2 0.50（枪斗连续性）。
- A7：GunFu 0.90 + Combat 0.50 + Motion V2 0.30（近身枪斗）。
- A8：Motion V2 0.90（通用动作/跑酷）。

这些是**测评起始值**，不是 9 个经过用户 RTX 4090 48GB 实测认证的最佳配方。切 A4–A7 时，必须将提示词题材改为相应兵器/枪斗；不能只改权重却仍沿用徒手打斗提示词。

对应权重文件：

- `H3_Combat_V2.safetensors`
- `Bunny_weapon_combatV1.safetensors`
- `GunFu.safetensors`
- `Motion_Repair_V2.safetensors`
- `H3_Fight_Flow_V1.safetensors`

参考：`https://huggingface.co/JOKER141`。不同 LoRA 版本可能改变结果，使用时核对本地模型文件，不自行假定新版本更优。

**单阶段工作流现状**：T2VA 的 FL2V Turbo 8 步 / R2VA 的 Ref2V Turbo 4 步；Veda 使用各自专用 predictor。4 步与 8 步是不同 Turbo 路线，不是 Veda 固有步数。Veda 对画质/动作的影响仍需分别对比；单阶段不必要求二阶段 Upscaler。

**其他组件**：Work-Fisher 的低清草稿→Latent 放大→高清二采，Speed Slider，BUNNY Conditioning Bridge 只是可选研究方向，**本板块既不假装它们已接入现有 JSON，也不要求启用**。

## 7.1 触发词、BASE 基线与提示词-预设同步（v1.8.1）

详见 `fight-trigger-policy.md` 和 `fight-prompt-mapping.md`。每当选择 A0–A8 时，要依据 `fight-lora-presets.json` 内 `prompt_strategy.scene` 切换镜头与题材；例如 A4 写清刀剑接触与收势，A7 是电影式近身枪斗，不能仍沿用 A2 徒手提示词。仅为 **非零** LoRA 选择作者推荐触发词。Fight Flow 依据主导互动类型选一个触发词；Combat 默认无触发词。

另设 `BASE` 诊断控制（所有五种 JOKER141 专项 LoRA 权重为零，但原有 Turbo 与 Veda 保持），**不改变 A0–A8 九组编号**。基础 JSON 内选择 BASE 必须使用手动权重覆盖或 `scripts/sync_fight_workflow.py --preset BASE` 导出新文件。

本 Skill 与 ComfyUI 控制是分离的：**在 ComfyUI UI 里切换预设并不会自动改写提示词**。离线同步脚本可以一起更新模式、选定预设和双路 Prompt，之后若再改 GUI 预设，需要重新导出或同步手动修改 Prompt。

**验证标记**：T2VA 8 步 Veda / R2VA 4 步 Veda 是用户的实验配置；Veda 发布 Predictor 的主要训练情境为 8 步 Turbo，4 步 Ref2VA 尚无本机质量认证。不要在提示词里加入 Veda 参数，也不要将其写成“经过验证的最优值”。

## 8. 失败诊断与最小改写

| 观察 | 优先检查 | 提示词修复动作 | 模型侧验证 |
|---|---|---|---|
| 打空、没有接触 | 攻防角色和方向不清 | 写明攻击肢体、接触位置、格挡、受击反馈 | A0 vs A2 |
| 互换身份、脸漂移 | `<Subject N>` 混用/参考图角色重复 | 两人各一 Subject；服饰与侧位锁 | Ref2VA A2 / A3 |
| 手臂多出/武器复制 | 动作太密、武器归属不清 | 砍掉一半招式，固定握持手与数量 | A4 Weapon-only |
| 没有主动权转移 | 两边一直同时攻击 | 显式 `A attacks → B blocks → B counters → A recovers` | A2 / A3 |
| 变慢、摆拍 | 太多镜头和特效 | 使用连续动作词、减轻运镜、减少粒子 | A0 / A1 |
| 脚底漂浮、瞬移 | 缺少转位/落脚解释 | 明确迈步、踩地、旋髋、结束站姿 | A1 / A8 |
| 光闪、画质变动 | 可能涉及稀疏注意力/不同模型 | 固定 seed/提示词后比照 Veda 开关 | 独立记录，不将故障归因于提示词 |

修复时**每次只改变一个维度**：提示词、LoRA 预设、采样步数、Veda 稀疏率、分辨率。不同维度同时改会失去归因能力。

## 9. 最终武打 QA

- 是否有两个不同且可辨认的角色，或准确的单角色任务？
- 是否说明初始左右位置、朝向、对峙距离和镜头轴线？
- 是否每拍都有实际动作、接触/有效格挡、身体反应和下一步因果？
- 是否说明惯用手/持武器手、武器数量、移动/丢弃的过程？
- 是否存在不可解释的跳位、瞬时起身或反向转身？
- 是否在有效时长内完成动作并有稳定收势？
- 是否正确处理音效、对白和配乐字段？
- 是否保证 Base 三字段、Ref2VA 六段与素材标签语义？
- 是否区分实验性 LoRA 权重与 MiniMax 官方语法？
- 是否避免声称“Veda 必然提速”或“某 LoRA 绝对修复动作”？

配套模板：`templates/fight_t2va_5s_master.txt`、`templates/fight_ref2va_5s_master.txt`。
配套完整示例：`examples/fight_t2va_5s_unarmed.txt`、`examples/fight_ref2va_5s_two_person.txt`。
