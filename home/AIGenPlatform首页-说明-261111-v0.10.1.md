# AIGenPlatform 首页 · 方案3 v0.10.1 说明

时间：2026-11-11 21:40（Asia/Shanghai，UTC+8）  
基础：v0.10.0（只读，未覆盖）  
性质：小改，修订号 +1

## 文件路径

- 产出 HTML：`/workspace/aigen-platform/home/AIGenPlatform首页-方案3能力宫格型-261111-v0.10.1.html`
- 本说明：`/workspace/aigen-platform/home/AIGenPlatform首页-说明-261111-v0.10.1.md`
- 构建：`/workspace/aigen-platform/home/.build/v101build.py`（源在 `.build/v101/`）
- 测试：`/workspace/aigen-platform/home/.build/t15.js`（由 t14 更新）
- 自测记录：`.build/selftest-v0.10.1-{file,sbx,soa}-{1366x768,1920x1080}.json`
- 截图目录：`/workspace/aigen-platform/home/shots/`，文件名含 `-261111-v0.10.1.png`
- 未改：`…-v0.10.0.html`、`说明-261111-v0.10.0.md`（mtime 仍为 20:55 / 20:58）

顶栏版本徽标已同步为 **v0.10.1**（说明条仍为「交互原型 · 示例数据」）。首页、登录、总览、管理/系统 6 页与热榜第 1 步除 `#hotCount` / `#hotDemoSel` 外未改。

## 测试结果

t15 在 3 环境（`file://`、srcdoc `allow-scripts`、srcdoc `allow-scripts allow-same-origin`）× 2 视口（1366×768 / 1920×1080）共 6 组，**均为 133/133**（t14 的 123 项按新结构更新后仍过，另增 10 项）。

新增/加严断言包括：

- 全部 `input[type=number]` 使用 `appearance:textfield`，隐藏原生 spinner
- 数字控件容器同一计算样式（高度 / 圆角 / 描边色宽 / 背景）
- 无「−/+」按钮文案，改为右侧自绘上下箭头
- 箭头点击 ±1；钳制 1–10（标题数 / `#hotCount`）、1–20（立意数）、100–5000（字数范围）
- 键盘上下键、非法值回退
- 点击箭头前后 `scrollTop` 差 ≤ 2，输入框不失焦闪烁
- 热榜第 1 步 `#hotCount` 同样式，`#hotDemoSel` 为统一下拉（自绘箭头、同圆角/描边/高度）
- 第 1 步三种来源空态候选区无遗留数字控件
- 设置卡三源等高，实测 **219px**（与 v0.10.0 相同）

## 控件规范值（计算样式）

| 令牌 / 属性 | 值 |
|---|---|
| 高度 `--ctl-h` | 36px |
| 宽度 `--ctl-step-w` | 92px |
| 圆角 `--ctl-radius` | **12px**（输入框 / 下拉 / 数字框统一；与图一较大圆角对齐，不再单独改步进器一家。沿用该变量的按钮也变为 12px） |
| 描边 `--ctl-border` / `--ctl-border-w` | `#6b7c94`（计算色 `rgb(107, 124, 148)`）/ 2px |
| 背景 | `#ffffff` |
| 数字 | 左对齐，左内边距 12px，字色 `#111827` |
| 箭头区 | 宽 22px，浅灰底 `#f1f3f6`，左 1px 分隔 `#e3e7ee`（不是第二层外边框） |
| 三角 | `#7a8699`；hover 主色蓝 + `#e8f0fb`；按下 `#d5e4f8`；禁用 `#c0c6d0` |
| focus-within | 描边主色蓝 + 3px 浅蓝光圈 `--ctl-focus-ring: 0 0 0 3px rgba(28,95,196,.30)` |
| 单位（个 / 条 / 字） | 框右侧 8px，12px / `#5b6b82`，行高 36px |
| 字数范围 | 两个 92×36 框 + 「—」+ 右侧「字」，钳制 100–5000 |
| 热榜 `#hotCount` | 同上 36×92 / 12px / 2px `#6b7c94`，单位「条」 |
| 热榜 `#hotDemoSel` | 高度 36px、圆角 12px、2px 描边、自绘下拉箭头 |
| 设置卡等高 | **219px**（plat / topic / direct，hdiff = 0） |

结构（沿用类名 `.ctl-step`）：一个容器 + `input[type=number]` + 右侧 `.ctl-spin` 里两个独立 `button`（内联 SVG 三角，`tabindex="-1"`，`aria-label`「增加/减少」）。原生 `::-webkit-inner-spin-button` 已隐藏，`-moz-appearance:textfield`。点击箭头 `mousedown` preventDefault，不改变页面滚动、不使框失焦闪烁。

## 遗留小 number 框：原因与处理

项总图二在第 1 步候选空态虚线框左上出现约 60px 宽、值为「5」、带原生上下箭头的原生 number 框。

**原因：** `measureS1SetMin()`（第 1 步三种来源设置卡等高探测）会把 `formHTML()`（内含默认值为 5 的 `#titleCount` / `#platCount`）写入一个探测节点，并 `appendChild` 到 `#step-1`。v0.10.0 将该探测节点设为 `position:absolute;left:0;top:0;visibility:hidden`。探测节点与真实表单 ID 重复，且 Chrome 仍会把未升级的原生 `input[type=number]` 控件（约 60px，带原生 spinner）绘制到候选空态虚线框内部左上——不是候选区模板里写了输入框，而是等高探测的溢出/漏绘。

**处理：**

1. 探测节点改为相对 `#step-1` 绝对定位到 `left:-12000px`（仍留在第 1 步内以继承同一包含块，避免测高偏差把卡片撑到 300px+），并加 `s1-measure-probe`、`opacity:0`、`aria-hidden`，`try/finally` 清理。
2. 全站隐藏 number 原生 spinner。
3. 渲染后清扫 `.s1-res` / `.rf-empty` / `.s1-empty-big` 中任何未包在 `.ctl-step` 里的 number 输入。

三种来源 × 空态（及有结果态）已断言并截图确认候选区内无多余控件。

另：热榜第 1 步首屏若仍走旧 `countCtl`（`− input +` 的 `.count-control`），升级时曾只替换中间 input、留下两侧「−/+」。现升级会整个替换 `.count-control`，单位「条」保留。截图已复核无双层控件。

## 新数字控件 vs 图一目标（文字对照）

图一（项总目标）：单独一个圆角输入框，约 2px 深蓝灰描边、白底、较大圆角；数字「5」靠左、黑字；框内右侧垂直排列灰色 ▲▼，垫一块浅灰底小竖条；箭头与数字共用同一外边框，没有嵌套描边。

v0.10.1 实现与图一一致的部分：单框、2px `#6b7c94`、白底、12px 大圆角、数字左对齐并留 12px 内边距、右侧自绘灰三角 + `#f1f3f6` 竖条、竖条只在框内（可选 1px 内部分隔，无双层外边框）、无「−/+」、原生 spinner 隐藏。单位在框外右侧，图一特写未画单位，实现按需求保留「个/条/字」。

与图一的可感差异（未决，见下）：图一特写里三角略大、竖条更「垫一块」；本实现箭头为 10×8 的 SVG 三角、竖条通高 22px，在 36px 高度下比例略紧。对照已用放大截图复核，无错位、无双层描边。

## 假设与未决

- 将 `--ctl-radius` 从 8px 统一到 12px，覆盖输入框、下拉、数字框；共用该变量的主/次按钮圆角一并变为 12px（未再拆一套按钮圆角）。
- 热榜 `#hotCount` 单位保持原「条」，不改为「个」。`#hotTopic` 与热榜第 1 步其余部分保持原样。
- 「直接指定标题」没有数字控件，故无该来源的控件放大图；空态与设置卡全貌已拍。
- 控件规范一览仍是评审用叠加层，不进入正式导航。
- 箭头尺寸是否还要再放大、竖条是否改成「非通高的小垫块」，等项总对照图一再拍板。
- 未改 briefSrc / hotJs / hotCss / embedCss / bridgeJs 源码块（热榜第 1 步控件改动全部由 fieldCss / fieldJs 覆盖与升级完成）。

## 主要截图（均已逐张查看）

- 第 1 步三种来源全貌，及平台热榜 / 主题生成的数字控件放大（含单位「个」）
- 第 1 步候选区空态（证明虚线框内无遗留 number）
- 字数范围控件（800 — 1200 字）
- 热榜第 1 步 `#hotCount` 放大与全貌（含统一后的 `#hotDemoSel`）
- 控件规范一览（v0.10.1 文案与新数字控件）
