# AI-K SK MiniMax H3 本地提示词技能 v1.4

> A local, non-API prompt engineering and validation toolkit for MiniMax H3 in ComfyUI.

面向 **MiniMax H3 开放权重 H3-Base、本地 ComfyUI、非 API 默认路径**。v1.4重点补齐 Ref2VA 多参考输入：工作流真实标签映射、视频配套音轨与独立音频的编号顺序、`<Audio N>`／`(Sx)`区分、来源—职责—目标关系图、冲突诊断及专项交叉验证。

## v1.4关键修复

- 新增工作流级 `Ref2VA Manifest`，不再用端口尾号猜 `<Audio N>`。
- 精确实现 ComfyUI 官方源码顺序：视频配套音轨先登记 Audio，视频随后登记 Video；独立音频最后登记。
- `ref_video_audio_N` 无同号视频时标记为无效输入。
- 音频信号合计按官方模型规格限制为3；纯音频 Ref2VA 拒绝。
- 区分 `<Audio N>`参考来源与 `(Sx)`目标发声者。
- 新增多图、多视频、配套音轨、独立声音的完整范例。
- 新增标签越界、未接素材、端口名误写、声音角色未绑定、视频身份泄漏等校验。
- 新增多参考专项交叉验证指标，不以静态测试代替实际生成结论。

## 安装

解压到：

```text
C:\Users\KSK\.codex-tokenrhythm\skills\aiksk-minimax-h3-local-prompt\
```

## 常用命令

```bash
python scripts/inspect_h3_workflow.py video_minimax_h3_r2v.json
python scripts/build_ref2va_manifest.py --workflow video_minimax_h3_r2v.json --output ref-manifest.json
python scripts/scaffold_h3_prompt.py --mode ref2va --profile context_ir_emulation --manifest ref-manifest.json --duration 5
python scripts/validate_h3_prompt.py prompt.txt --mode ref2va --profile context_ir_emulation --duration 5 --manifest ref-manifest.json --strict

# 真实生成对照验证
python scripts/create_h3_validation_matrix.py examples/validation-cases-v14.json examples/experiment-environment-v14.json experiment/run-manifest.csv
python scripts/verify_h3_experiment.py experiment/run-manifest.csv examples/experiment-environment-v14.json --write-verified-manifest experiment/verified.csv
python scripts/prepare_h3_blind_review.py experiment/verified.csv experiment/blind-package --reviewers R1,R2
python scripts/merge_h3_reviews.py experiment/blind-package/admin/merged_reviews.csv experiment/blind-package/reviewers/R1/review_scores.csv experiment/blind-package/reviewers/R2/review_scores.csv
python scripts/analyze_h3_validation.py experiment/verified.csv experiment/blind-package/admin/secret_mapping.csv experiment/blind-package/admin/merged_reviews.csv --baseline direct --output-json experiment/report.json --output-md experiment/report.md

python -m unittest discover -s tests -v
```

## 重要事实

官方 R2V 模板当前只实际连接两张参考图；节点预留的视频、视频音轨和独立音频接口并不代表模板已经接好这些素材。技能必须按工作流实际连线生成标签表。

## v1.3能力继承

v1.4保留并重新提供可执行的预注册矩阵、环境/素材/提示词哈希、匹配Case/Seed、盲评包隔离、多评审合并、硬失败分离、案例→Seed两阶段bootstrap与独立环境复现工具。单环境结果最高为`provisional`。

## 验收

- Python脚本编译通过。
- 自动测试：23项全部通过。
- 测试结论仅覆盖工具链与规则，不代替真实H3生成盲评。

## 自定义节点边界

官方标签排序算法只对`MiniMaxH3ReferenceToVideo`作硬结论。RunningHub/RH或其他自定义节点必须读取实际源码或使用手工Manifest，不得默认照搬。
