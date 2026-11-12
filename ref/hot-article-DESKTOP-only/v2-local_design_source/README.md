# AI 热度图文生成 · Windows 设计稿

本目录是 Windows 桌面版的设计交付源，独立于生产 Tkinter GUI 和业务代码。保留原有六步流程、品牌颜色及导出/图文交接规则，调整字体、布局、控件与任务反馈。

## 当前交付状态

- 已生成 20 个设计状态，共用一份声明式设计源。
- 本地 HTML 预览已进行浏览器交互和布局检查。
- **尚未更新到 Figma，也未验证插件在真实 Figma 中的渲染结果。** Figma MCP 返回 Starter 调用额度已耗尽；正常桌面插件导入路径又遇到截图超时及输入几何不可用。没有创建任何新 Figma 节点。
- 插件包通过 JavaScript 语法检查。可编辑图层、变量、组件及原型连线仍须在 Figma 实际运行后验收；本地预览通过不能替代 Figma 验收。
- 没有修改生产页面、配置、数据库或模型调用。原型中的正文、标题和日志都是设计示例。

同步记录见 [sync-status.json](sync-status.json)，验证范围见 [qa-report.json](qa-report.json)。

## 设计变化

| 项目 | Windows 版规则 |
| --- | --- |
| 字体 | 优先 Microsoft YaHei UI，缺失时 Noto Sans SC；正文 16px，辅助 14px，区块标题 20px，页面标题 28px |
| 控件 | 按钮和输入框 40px，单选/复选视觉 18px、选择行至少 40px；焦点使用 2px 蓝色描边 |
| 导航 | 宿主导航保留；六步在顶部切换，仅当前工作区滚动，避免数千像素的整页长卷 |
| 操作 | 底部 72px 操作栏固定；当前稿导出、生成图文稿、合并无需滚动寻找 |
| 风格库 | 左侧紧凑列表，右侧完整详情；保留常用、使用次数与排序信息 |
| 生成设置 | 原标题、立意和完整风格组成紧凑快照；方向横排，篇幅设置独立；支持 1–3 稿 |
| 稿件处理 | 切换稿件方向、各稿独立选标题；批量导出位于标签行右侧，预览可折叠 |
| 异常处理 | 单稿、双稿、部分失败、续跑、生成中和合并中分别提供状态稿；仅完整三稿显示合并操作 |
| 导出和交接 | 格式及目录选择；默认系统桌面、目录记忆；图文只交接当前稿，先保存再交接，由用户手动开始 |

窗口基准 1440×1000，另有 1280×800 最小窗口稿。尺寸均为逻辑像素；16px 对应 96 DPI 下的 12pt。生产落地应使用 Tk 的系统缩放与字体换算，不能把 Figma 的 px 数字直接当成 Tk 的 point。125%/150% 系统缩放、中文输入法、系统文件夹选择器及原生标题栏仍需实际 Windows GUI 验收。本地浏览器预览会缩放整张画布，其视觉字号不能作为原生字体大小的测量依据。

窗口顶部的“最小化、最大化、关闭”表示系统标题栏位置；生产版使用系统窗口控件，不把这些文字作为自绘标题栏实现。

## 本地预览

在项目根目录执行：

```powershell
python -m http.server 8876 --bind 127.0.0.1 --directory design/hot-article-windows
```

打开 <http://127.0.0.1:8876/>。顶部评审工具栏已移除，六步主页面使用工作区内部导航切换。特殊状态可使用 URL 参数查看，例如 `?scene=single5`（单稿）、`?scene=partial5`（部分成功）、`?scene=compact4`（最小窗口）、`?scene=foundations`（控件规范）。

本地预览的榜单数量默认为 5 条，默认结果列表和数量标记一致；这些预览调整位于 `index.html`，本次不修改 Figma 生成脚本和插件包。

预览支持方向勾选、每稿独立选标题、预览展开/收起、导出格式及目录记忆、图文交接顺序。目录保存在预览专用的 localStorage `windows-design-export-dir`，不会修改应用的实际导出目录。目录输入用于验证记忆效果；生产版应调用系统文件夹选择器。

“查看生成结果”是状态演示入口，不代表模型已经执行。没有实际导出、合并、文件保存、任务恢复或图文生成；历史任务、来源、常用设置等入口仅解释设计意图。

## 更新到已有 Figma 文件

目标文件：

<https://www.figma.com/design/x3uNLbtFAS8MOCnCTPu7aH/?node-id=0-1>

此步骤尚未执行成功。正常桌面导入方法：

1. 在 Figma 桌面应用打开上面的 AIDocStudio 文件。
2. 通过 **Plugins → Development → Import plugin from manifest…** 选择本目录的 `figma-plugin/manifest.json`。
3. 运行开发插件 **AIDocStudio · Windows 热度图文工作台**。
4. 点击 **创建可编辑设计**。插件仅新增 `03 · Windows 桌面版` 页面，保留原来的 Web 页面。
5. 完成后下载 `figma-windows-state.json` 记录实际节点及审计结果，检查六步、弹窗、最小窗口及控件规范，再确认设计交付。

插件只使用普通 Figma Plugin API，不访问网络。生成的是文本、Auto Layout、矢量图标、按钮组件实例及变量绑定，不将整页截图当作设计图层。新变量和样式使用 Windows 命名空间，旧稿不受影响。

如果 Windows 页面已经存在，插件会定位该页并停止，不重复创建或覆盖。若首次构建中途失败，先检查现有半成品页和错误信息，不要反复点击运行；应修复原因并人工确认该页如何处理。插件不会自动删除设计。

Figma 的连线覆盖主要步骤、稿件方向切换、导出弹窗、预览、合并和图文交接说明。各稿标题独立记忆、目录持久化等逻辑以 HTML 预览及业务契约为准；Figma 静态状态稿不模拟完整应用数据库。

## 重新生成

```powershell
python design/hot-article-windows/build_design.py
node --check design/hot-article-windows/figma-plugin/code.js
```

修改布局和文案：`build_design.py`。修改 HTML 的交互：`index.html`。修改 Figma 适配：`figma-plugin/renderer.js`。重新构建会覆盖 `design.json`、`design-data.js` 和 `figma-plugin/code.js`，不要直接修改这些生成物。

## 文件与来源

- `build_design.py`：六步、状态与控件规则的设计源。
- `design.json` / `design-data.js`：同源场景数据，分别供归档和 HTML 预览使用。
- `index.html`：本地交互评审页面。
- `figma-plugin/manifest.json` / `code.js`：Figma 桌面开发插件的运行包。
- `figma-plugin/renderer.js`：可编辑图层渲染器源文件。
- `figma-plugin/helpers/`：复用当前环境 Figma 技能提供的 `createVariableCollection`、`createSemanticTokens`、`createComponentWithVariants` helpers；来源为 `openai-curated-remote/figma/16.0.0/skills/figma-use` 的辅助脚本。
- 图标复用项目已有 `ui/assets/nav/*.svg` 与 `modules/hot_article/assets/figma/check.svg`，没有新增外部图片依赖。

## 后续生产落地范围

本轮仅设计，没有替换 `modules/hot_article/` 的生产 GUI。落地时保留独立应用服务与仓储接口，按本稿调整 Tkinter 布局、字体和焦点顺序；用真实任务事件替换示例状态，继续遵循输入快照、部分成功保留、续跑及单篇图文交接约定。
