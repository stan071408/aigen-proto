# AIGenPlatform 首页 · 方案3 能力宫格型 · v0.17.14

- 日期：2026-11-20（北京时间）
- 基于：v0.17.13（旧版不覆盖）
- 范围：仅本首页原型。按项总拍板，落实小勾《AGP原型定稿技术评审》v0.1.0 与牛牛意见。

## 相对 v0.17.13

1. **配图张数固定为封面 1 + 正文 4：** 图文生成第 4 步文案、定时向导第 04 步、编辑任务配图数量、设置页「每篇配图张数」、任务监控/总览示例与「共 n 张」一律改为只读「封面 1 张 + 正文 4 张（固定）」，去掉张数输入。示例数据按 5 张计（如 3/5）。
2. **看日志拆分 error_code 与 fail_reason：** `error_code` 只用码表中的码（依据接口清单 v0.1.8 与 Skill 首版码表）；`fail_reason` 为一句中文。`tcFailLabel` / `tcLogText` 按 `error_code` 取文案。映射：部分失败→`partial_failure`，内容被拒→`model_content_rejected`，超时→`model_upstream_error`（码表无单独 `timeout`），限流→`rate_limited`。已去掉 `partial_images`、`llm_timeout`。并补充 `publish_verify_failed`、`config_missing`（如模型未开通）、`quality_check_failed`、`needs_evidence` 示例。
3. **生成原稿不再提供取消：** 图文生成第 2 步生成中只保留「生成中…」，去掉「× 取消」。失败后仍可「重试」。即时任务无取消。
4. **保留默认去水印：** 设置页「默认去水印」开关保留，BS 为来源。
5. **已拍板的可选项：** 内容库图片规格改为「以实际返回为准」（不再写 png / 1080）；设置页去掉 LLM_API_KEY / ARK_API_KEY 密钥状态（密钥由 SP 配置）；定时向导「1000–1200 字」改为可选提示、不作校验；提示词改为「提示词未定稿」，不再展示 prompts v1.0.0；删除不可达的 `accountsPage`、`publishPage`（公众号/视频号）、`PUB_TASKS` 及其专用代码。
6. **未改：** 置灰「发布管理」下载浮层、设置页「下载 Windows 桌面应用」、生图方式仍为 API 固定参数。豆包仍仅在 CS 客户端中出现（同 v0.17.13）。空列表占位撑满视口的规则保持不变。

## 自检

- `home/.build/selftest-v0.17.14.js`：Chrome headless、`file://`、1366×768。15/15 通过：各主要页面可渲染，无 JS 错误；配图固定 1+4；看日志同时展示 error_code 与中文 fail_reason；生成原稿无取消按钮；设置页保留去水印、无密钥状态、提示词未定稿、下载按钮与 toast 仍在；内容库规格为「以实际返回为准」；发布管理浮层仍可打开；占位撑满函数仍在。
- 未跑全量套件。

## 文件

- `AIGenPlatform首页-方案3能力宫格型-261120-v0.17.14.html`
- `AIGenPlatform首页-说明-261120-v0.17.14.md`
