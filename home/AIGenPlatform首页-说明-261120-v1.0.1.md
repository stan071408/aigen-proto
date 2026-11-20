# AIGenPlatform 首页 · 方案3 能力宫格型 · v1.0.1

- 日期：2026-11-20（北京时间）
- 基于：v1.0.0 定稿（旧版不覆盖）
- 范围：仅本首页原型。按项总批准的评审《AGP原型定稿技术评审》v0.1.1 修正。

## 相对 v1.0.0

1. **去掉 API 兜底：** 删除设置页「API 兜底」开关、编辑任务「API 兜底：跟随设置 / 开 / 关」（小标题改为「生图方式与配图数量」），以及营销首页 `#sec-acct` 中「豆包不可用时改走 API / 密钥掩码 / 界面只显示是否已配置」的表述，改为「API 生图额度不限」。并清理 `toggleApiFallback`、`SET.apiFallback`、`tcApiFb`、`onApiLimitInput`、`API_QUOTA`、`apiImageLimit` 等专用逻辑。
2. **看日志错误码：** `needs_evidence` 改为码表中的 `internal_needs_evidence`（中文文案不变）。新增 `timeout` 文案「任务超过时限未完成。」（整条命令超过 `timeout_s`），避免只显示「任务失败。」。上游请求超时或网络中断仍用 `model_upstream_error`。说明不再写「码表无单独 timeout」。
3. **总览配图张数：** 「总生成图片」按 15 篇文章 × 封面 1 + 正文 4 计，展示为 15 张文章封面 + 60 张文章配图（不再把正文 4 张误计成 5 张，也不再把内容库图片记录重复加总）。

## 自检

- `home/.build/selftest-v1.0.1.js`：Chrome headless、`file://`、1366×768。9/9 通过：总览 15+60，无 API 兜底，timeout / internal_needs_evidence 文案正确，各页可渲染，无 JS 错误。
- 未跑全量套件。

## 文件

- `AIGenPlatform首页-方案3能力宫格型-261120-v1.0.1.html`
- `AIGenPlatform首页-说明-261120-v1.0.1.md`
