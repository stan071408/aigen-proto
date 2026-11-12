## v0.5.2.120（2026-11-03）
- 原稿生成「多稿生成」工具栏移除「生成主题稿」按钮：保留 主题方向 / 生成稿数 / 生成原稿 / 加入批量生成 / 批量图文稿生成设置；「生成原稿」仍一条龙先按主题稿 Prompt 现场生成主题稿再写原稿。
- 删除宿主 `_article_generate_topics` 与 `article_topics_btn` 接线；独立原稿窗口 `modules/article_gen/ui/main_window.py` 多稿模式不再创建该按钮并删除 `_start_topics` / `_run_topics`（单稿模式保留按钮用于生成单篇标题）。控制器 `generate_topics` 与 CLI `gen-topics` 保留。
- 更新 test_article_workspace / test_progress_dialog / test_api_only_architecture 断言按钮已移除。

## v0.5.2.118（2026-11-03）
- 原稿生成「单稿生成」移除「标题来源」切换及「手动输入」选项：标题固定由主题方向生成，单稿行直接显示 主题方向 / 生成文章标题 / 文章标题 / 生成单篇（文章标题输入框仍可编辑）。
- 删除宿主 `_article_on_title_source_changed` / `_article_apply_title_source` 与 `article_title_source_segment`；独立原稿窗口 `modules/article_gen/ui/main_window.py` 同步移除分段控件、`TITLE_SOURCE_SETTING`（遗留 `ui.title_source=manual` 不再读取，等同由主题方向生成）及手动模式下隐藏主题稿 Prompt 的分支。
- 更新 test_article_workspace 相关用例。

## v0.5.2.86（2026-10-28）
- 按 Figma `36:2474` 补齐剩余状态：第四步生成中（36:3791）方向卡显示运行徽标（按日志阶段显示撰写正文 / 梳理观点 / 分析机制，否则“生成中”），日志“运行中”黄色徽标，底栏“生成中 · 已完成结果将立即保存”+「取消生成」「查看生成结果」，运行中隐藏篇幅卡。
- 第四步部分完成（36:3994）：方向徽标已完成 / 请求超时 / 失败，日志“部分完成”，底栏「N 稿成功 · M 稿超时/未完成」+「处理成功稿」「继续生成」（续跑只补未完成方向）；新一轮生成从空日志开始。
- 第五步部分完成（36:4191）：只显示成功稿页签，“N 稿已完成”，本次创作卡说明下方「继续生成深度稿」（144），不显示合并。
- 合并中（36:5296）：三稿合并日志自动展开，状态为黄色“运行中”徽标（未运行时为普通文字），底栏保留当前稿操作并显示「查看合并结果」（运行中展开日志，完成后进入第六步）。新增 W_ERR 色板，警示色按设计改为 #fff5df/#80530d。
- 排查 test_article_workspace 偶发 TclError：见 design-qa.md，未确认为测试隔离问题，未改测试。
- 验证：新增 3 项状态回归，热度业务与布局 36 项通过；全量 tests 756 通过 / 1 跳过 / 1 失败（test_single_root_window_and_section_switch，同类 Tcl 库读取 TclError，单独复测通过）。

## v0.5.2.85（2026-10-27）
- 按 Figma `36:2474`（03 · Windows 桌面版）重做热度图文生产 Tkinter 工作区：固定 88px 页眉（标题、已自动保存、历史任务）、80px 六步页签、单步工作区与 72px 固定操作栏；不再整页滚动，仅榜单/立意/风格列表、文章预览与日志在卡片内滚动。
- 字体改为 Microsoft YaHei UI（缺失时 Noto Sans SC），正文 16px、辅助 14px、标题 20/28px；按钮与输入框 40px；新增 Windows 色板令牌与 18px 单选/复选资源 `modules/hot_article/assets/windows/`（Figma REST 导出原样 SVG + PNG）。
- 第一至三步改为「列表 + 右侧详情」：点击单选只选中并刷新详情，由底栏「继续…」进入下一步；第四步快照/方向卡/篇幅/生成日志；第五、六步方向页签、候选标题、折叠预览、本次创作卡、三稿合并日志折叠栏，导出/图文/合并操作移至底栏并作用于当前稿。
- 生成图文稿先显示 560×386 交接确认，再进入 560×476 导出弹窗；默认榜单条数 5（与 v0.5.2.84 预览一致）。模块模型设置与「刷新当天榜单」移入页眉「更多」菜单。业务流程、服务接口与持久化不变。
- 验证：重写热度布局契约 15 项；全量 tests 754 项通过，1 项既有 Tk 根窗口初始化偶发失败（test_nav_item_switches_workspace）单独复测通过；热度业务与布局 33 项通过。真实 MainWindow 各状态截图与 Figma 并排对照见 design-qa.md。

## v0.5.2.82（2026-10-27）
- 按 Figma `7:3601`（Step 05 三稿文章处理）修正剩余差异：候选标题选中/未选中文字与边框色、预览标题色、提示文字色与间距、「导出全部稿件」10px 文字及 #bbd2c6 描边。
- 三稿合并日志改为设计行样式：10px 时间列 + 12px 列间距（按实际字形定位）、行间 #f1e5cf 分隔线，内容未溢出时隐藏滚动条。
- 步骤引导：标题改为常规字重 #70538b，序号徽标 #e4d9f0/#785294，激活行 #e4dbf2，行内边距按设计收紧。
- 宿主导航接入 Figma 导航图标（图文生成 / AI 热度图文生成 / 头条发布 / 系统设置 / API 连接设置），资源位于 `ui/assets/nav`，闲置/悬停/激活三态；无设计图标的「Relay 接单台」保持原样。
- 验证：新增 2 项布局/图标回归；全量 tests 通过。1280×900 宿主窗口第五步截图与 Figma 对照见 design-qa.md。

## v0.5.2.81（2026-10-27）
- 按最新 Figma 六步设计更新生产 Tkinter 展示层：正文与引导比例、字体层级、风格卡、第四步紧凑摘要及标签下重设入口、生成方向卡与真实运行日志。
- 统一主操作和稿件操作按钮的像素尺寸；第五、六步保留局部页签、独立标题、折叠预览与就近操作；导出弹窗调整为 400×384px。
- 集成本地 Figma 选中标记资源，保留原生控件状态与键盘操作；不修改后台业务、宿主导航或 Figma 文件。核对范围和原生渲染差异见 design-qa.md。
- 验证：热度模块业务与布局 33 项通过；原文章工作区 24 项逐项独立进程复测通过。联合运行遇到既有 Tk 根窗口初始化异常，因此不记为单次联合通过；编译与差异检查通过。模型调用使用替身。

## v0.5.2.80（2026-10-26）
- 根据最终本地原型创建可编辑 Figma 文件，包含六步画板、完整流程、导出弹窗及独立组件/令牌页。
- 保存页面组装脚本与设计索引，修复捕获图层转组件后的高度压缩、绝对定位及右侧引导重叠；连接跨步骤与导出演示入口。
- 验证：Figma 尺寸/布局结构读回、低分辨率单图视觉检查及 JavaScript 语法检查；本次不修改生产 GUI 与后台。

## v0.5.2.79（2026-10-26）
- 再按指定地址最终原型补齐六步界面：浅绿连续榜单列表、来源/排名/采集时间/热度、蓝色立意按钮、步骤内运行反馈及来源专属空态。
- 主题输入支持实际缓存分类下拉和热门主题快捷选择；引导随滚动更新，窄窗口收起引导、重排输入操作与生成方向；运行时锁定输入。
- 底部设置改为折叠区，保留历史、模型覆盖和强制刷新入口；恢复历史写稿日志，移除第六步多余的可见日志与重复说明。
- 验证：热度业务与界面 29 项、原有文章工作区 24 项分组复测通过；覆盖真实宿主挂载、单/双/三稿、取消保存和指定单稿保存后图文交接。编译与差异检查通过，更新原型核对记录。

## v0.5.2.78（2026-10-26）
- 按最终 HTML 原型重建原生热度图文六步工作区：恢复分区配色、步骤引导、紧凑写作风格卡、三列生成方向及独立运行日志。
- 第五、六步恢复局部稿件页签、候选标题、统一折叠预览和就近操作；批量导出位于页签栏右侧，导出弹窗采用纵排格式卡及目录选择。
- 修复隐藏页签控件覆盖、Tk 变量解释器绑定及重新选择后的滚动定位，保持后台业务和宿主其他工作区独立。
- 验证：模块业务、桌面布局交互与原有文章工作区联合回归 44 项通过；编译和差异检查通过。原型核对记录见 design-qa.md。

## v0.5.2.77（2026-10-26）
- 新增独立 `modules/hot_article`：领域、仓储、应用编排、固定技能适配与原生 Tkinter 六步界面；宿主仅增加导航及图文交接钩子。
- 集成 topic-research 0.3.1、topic-insight 0.6.10；支持真实热榜、核心立意、常用风格、分稿、部分失败续跑、取消恢复、三稿合并、标题选择与预览。
- 支持 DOCX/Markdown 单稿和批量导出、系统桌面默认目录与目录记忆、导出后单稿配图准备；交给原有图文页面后由用户手动开始。
- 增加真实阶段日志、输入快照、历史恢复、模型阶段覆盖、核查记录及无 GUI CLI；不修改原有生图/去水印/发布内核。
- 验证：模块 17 项测试通过；全量回归 738 项通过、1 项 Tk 初始化偶发失败（该项及上一轮同类失败项单独复测通过）。相关编排/导出/失败项复测 27 项通过，编译检查通过。
- 真实小样本：头条/百度各解析 50 条、有效立意、1186 字差异化稿及三个候选标题、四个有效配图点位，DOCX/Markdown/配图说明输出验证通过。真实完整三稿融合与最终生图待产品环境验收。

## v0.5.2.76（2026-10-25）
- 第五、六步生成图文稿统一先打开导出弹窗，导出成功并保存单篇交接数据后进入图文生成页面，带入所选标题和正文。
- 取消或失败不跳转；浏览器下载回退明确提示确认下载完成，目录写入等待实际完成。
- 验证：JavaScript语法与差异检查通过。

## v0.5.2.75（2026-10-25）
- 第六步标题文案调整为“合并稿文章处理”。
- 验证：文案替换与差异检查通过。

## v0.5.2.74（2026-10-25）
- 写作风格结果卡片压缩标题、正文、标签及优点列表间距。
- 全部稿件导出移至方向切换栏右侧；合并三稿移至各稿图文稿按钮之后，仅完整三稿显示。
- 本稿导出、图文稿、三稿合并统一主按钮样式，包含第六步本稿导出。
- 验证：JavaScript语法与按钮位置/条件源码检查通过。

## v0.5.2.73（2026-10-25）
- 第四步设置区下增加文章生成运行日志，记录各稿开始、完成、总体结束或失败，自动滚动到最新记录。
- 第五步下增加三稿合并日志，合并模拟分阶段运行，运行时锁定操作，完成后进入第六步。
- 验证：JavaScript语法与日志阶段接入检查通过。

## v0.5.2.72（2026-10-25）
- 第四步摘要改为标签、正文、重设操作的信息行，收紧间距并保留完整写作风格说明。
- 生成方向采用勾选框与标题同排、说明下置的紧凑三列布局，小屏自适应。
- 验证：差异检查通过，未改变选择与生成逻辑。

## v0.5.2.71（2026-10-25）
- 第五步预览文章与第六步统一为浅底边框折叠框，共用标题栏和展开正文样式。
- 验证：差异检查通过。

## v0.5.2.70（2026-10-25）
- 首次导出目录选择定位桌面，确认权限后保存；通过IndexedDB持久保存目录句柄，下次弹窗自动恢复。
- 导出时检查并请求已保存目录权限；不支持目录API时明确显示浏览器下载设置提示。
- 验证：JavaScript语法、目录写入及导出回归检查通过。

## v0.5.2.69（2026-10-25）
- 导出弹窗增加目录选择，通过浏览器文件系统API写入所选目录，不支持时明确回退默认下载位置。
- 合并三稿进入第六步，提供三个标题单选、折叠正文预览、导出格式与目录选择、单篇图文稿原型反馈。
- 第六步沿用第五步样式并自动滚动定位；重新生成或上游失效时隐藏旧合并稿。
- 验证：语法、MD/DOCX下载、目录写入关闭、DOCX结构及第六步入口条件检查通过。

## v0.5.2.68（2026-10-25）
- 本稿及全部稿件导出增加格式选择弹窗，支持取消、Esc关闭及确认导出DOCX或Markdown。
- 实际生成有效DOCX与MD文件，保留各稿选定标题，批量导出包含所有稿件。
- 验证：语法、DOCX ZIP完整性与XML解析、标题转义和Markdown内容检查通过。

## v0.5.2.67（2026-10-25）
- 稿件方向切换栏移入稿件卡片标题位置，移除重复方向分组标题，采用下划线选中状态。
- 验证：JavaScript语法、7种方向组合检查通过。

## v0.5.2.66（2026-10-25）
- 第五步新增差异化稿、广度稿、深度稿切换入口，按实际生成方向展示，切换保留各稿标题选择。
- 折叠预览移动到本稿操作按钮行上方，全部稿件导出范围保持不变。
- 验证：JavaScript语法和差异检查通过。

## v0.5.2.65（2026-10-25）
- 第五步顶部支持全部稿件同时导出；各稿独立选择标题，默认首个标题。
- 导出本稿与生成图文稿按钮移至各卡片内，就近反馈；图文稿只处理当前一篇，合并三稿条件保留。
- 验证：语法及全部7种方向组合的独立标题、就近按钮、批量导出入口与合并门槛检查通过。

## v0.5.2.64（2026-10-25）
- 第五步重设计为独立稿件卡片，方向标题、候选单选项与折叠预览分层展示。
- 底部统一操作区新增当前选择摘要；选中稿件边框高亮，保持导出/图文稿选择门槛与三稿合并条件。
- 验证：JavaScript语法、7种稿件组合的卡片/选择/预览/按钮门槛检查通过。

## v0.5.2.63（2026-10-25）
- 第五步候选标题支持单选；选择后启用导出和图文稿操作，仅处理所选标题对应稿件。
- 预览标题跟随选择更新；合并三稿仍独立于标题选择。
- 验证：JavaScript语法和差异检查通过。

## v0.5.2.62（2026-10-25）
- 第五步每稿增加独立的文章预览折叠区，默认收起，支持键盘展开与收起，显示对应稿件的示例正文。
- 验证：JavaScript语法与差异检查通过。

## v0.5.2.61（2026-10-25）
- 第五步改名三稿文章处理，移除数量说明与各稿已生成标识。
- 每稿展示用户提供的三个候选标题，均不超过30字；导出同步包含候选标题。
- 验证：JavaScript语法、标题字数和差异检查通过。

## v0.5.2.60（2026-10-25）
- 修复第四、第五步未指定网格区域造成第五步排入侧栏的问题；第五步渲染完成后再滚动和聚焦。
- 验证：浏览器完成单稿、双稿、三稿生成并确认第五步可见；合并三稿仅三稿显示，图文稿原型反馈可用。

## v0.5.2.59（2026-10-25）
- 统一第四步摘要标签，互换写作风格标签与名称；生成后自动进入第五步文章处理设置。
- 第五步展示方向与候选标题，提供示例文章导出、图文稿流程反馈，以及完整三稿专属合并操作。
- 验证：JavaScript 语法检查及全部 7 种生成方向组合的摘要、合并门槛检查通过。

## v0.5.2.58（2026-10-25）
- 原型重设计：第四步摘要采用纵向排布，原标题突出展示，立意细线强调，风格名称与重设同排，完整描述独立呈现，移除分栏与大面积底色。
- 验证：JavaScript 语法与差异检查通过，保留两个重设入口。

## v0.5.2.57（2026-10-25）
- 原型文案：移除第四步摘要中的写作名称标签，保留风格名称、说明与重设入口。
- 验证：目标标签唯一匹配与差异检查通过。

## v0.5.2.56（2026-10-25）
- 原型调整：强化第四步摘要层级，栏目标题加粗，重新设定改为有边框与底色的操作按钮，写作名称去除标签式背景，增加内容分隔。
- 验证：CSS 作用域与差异检查通过，保留原有重设交互。

## v0.5.2.55（2026-10-25）
- 原型调整：第四步摘要同时显示写作名称、完整写作风格说明，保留重新设定入口，增加风格栏宽度。
- 验证：JavaScript 语法及名称/说明字段引用检查通过。

## v0.5.2.54（2026-10-25）
- 原型调整：第四步摘要重设计为原标题独立标题带、立意与风格分栏，保留重设入口；统一三个操作按钮宽度，开始生成改为开始生成文章。
- 验证：JavaScript 语法、响应式宽度规则与差异检查通过。

## v0.5.2.53（2026-10-25）
- 原型调整：减少第四步顶部间距与外层留白；增加写作风格重新设定；核心立意重选保留已有风格结果及选择，选择后返回第四步。
- 验证：JavaScript 语法与立意重选保留分支检查通过。

## v0.5.2.52（2026-10-25）
- 原型调整：移除风格列表下一步按钮与第五步提示；第四步标题改为生成三稿文章，操作按钮统一开始生成；核心立意增加重新设定，返回立意结果选择并关闭旧稿件。
- 验证：JavaScript 语法、删除元素引用及差异检查通过。

## v0.5.2.51（2026-10-25）
- 原型调整：风格结果按钮改为清空数据，清空当前结果、选择和后续稿件，恢复等待占位；选中风格后直接打开并滚动至第四步设置区。常用与使用记录保留。
- 验证：JavaScript 语法、清空分支与选中后的步骤调用检查通过。

## v0.5.2.50（2026-10-25）
- 原型调整：写作风格等待获取、切换来源、加载中和空结果均保留结果区域，参照核心立意占位设计展示标题、状态、图标及操作提示。
- 验证：JavaScript 语法及占位状态调用检查通过。

## v0.5.2.49（2026-10-25）
- 原型调整：切换写作风格后滚动至当前卡片；下一步按钮改为“开始生成三稿文章”；更新第四步引导标题和说明，相似度沿用技能术语。
- 验证：JavaScript 语法与差异检查通过，确认滚动只由写作风格单选触发。

## v0.5.2.48（2026-10-25）
- 原型新增第四步：沿用原标题、立意与风格，支持差异化/广度/深度任意组合、每稿字数、模拟进度及分稿切换；仅完整三稿显示第五步入口，合成仅占位。
- 依据 topic-insight write 技能设计，未实际调用 API；结果为明确标注的缩略示例。
- 验证：JavaScript 语法、七种组合与未完成门槛测试通过；浏览器验证前三步进入第四步、三稿生成与第五步入口。

## v0.5.2.47（2026-10-25）
- 原型调整：已有风格按常用优先、使用次数降序获取，再按数量截取；确认下一步时记录使用次数，同一结果重复确认不重复计数，保存在浏览器本地。
- 验证：JavaScript 语法、常用优先、次数排序及同次数稳定排序测试通过。数据库仍由离线示例模拟。

## v0.5.2.46（2026-10-25）
- 原型文案：页面标题、左侧菜单及对应名称统一改为“AI 热度图文生成”。
- 验证：确认旧功能名称已全部替换。

## v0.5.2.45（2026-10-25）
- 原型新增常用风格设置：独立于下一步单选，支持多个常用、取消和最多 5 个限制，浏览器本地保存；移除“写作名称”标签。
- 验证：JavaScript 语法检查、5 个上限及取消后重新添加逻辑测试通过。

## v0.5.2.44（2026-10-25）
- 原型调整：按钮改为“获取已有风格”；重排风格详情，强化描述与标签层次，将风格优点和核心抓手合并为编号列表。
- 验证：JavaScript 语法、字段引用、按钮文案和差异检查通过。

## v0.5.2.43（2026-10-25）
- 原型调整：核心立意成功返回后滚动至结果区域；第三步改为原标题获取、已有风格复用双入口，切换时清空选择和结果。已有风格由离线示例模拟数据库读取。
- 验证：JavaScript 语法检查、双来源默认值与分支逻辑、滚动调用和差异检查通过。

## v0.5.2.42（2026-10-25）
- 原型文案：第三步引导标题改为“确认文章的写作风格”。
- 验证：确认仅替换对应引导标题。

## v0.5.2.41（2026-10-25）
- 原型调整：提示去掉步骤前缀，移除已选核心立意汇总区域；写作分类统一更名为写作风格，第三步引导改为“从立意走向表达”。
- 验证：JavaScript 语法与遗留引用检查通过，保留核心立意选择及第三步联动。

## v0.5.2.40（2026-10-24）
- 原型调整：将写作分类卡片的对话对象、核心抓手标签加粗。
- 验证：检查对应标签与 font-weight:700 样式规则。

## v0.5.2.39（2026-10-24）
- 原型调整：用用户提供的数字反差型、政策解释型两条数据替换通用示例；写作风格全文独占一行，风格优点与核心抓手分栏展示，保留标签、对话对象及单选。
- 验证：语法与模拟交互测试通过，覆盖两条实际数据、字段渲染及重新获取空状态。

## v0.5.2.38（2026-10-24）
- 原型调整：写作风格支持单选并进入下一步摘要；条数移至标题后，右侧增加重新获取；刷新返回未展示的示例分类，无更多数据时显示空状态。
- 验证：语法与模拟交互测试通过，覆盖 5/3/0 条返回及单选入口。第四步仅选择摘要，未实施生成业务。

## v0.5.2.37（2026-10-24）
- 原型调整：写作分类结果展示名称、风格、标签、对话对象和风格优点/核心抓手；获取完成后自动滚动到结果区域。
- 验证：JavaScript 语法及模拟 DOM 测试通过，覆盖五项数据、滚动触发、默认数量及不足数量。

## v0.5.2.36（2026-10-24）
- 原型调整：精简主题输入提示，移除第三步表单中的已选核心立意展示。
- 验证：JavaScript 语法及浏览器前三步交互已检查。

## v0.5.2.35（2026-10-24）
- 原型新增第三步：选择核心立意后自动进入写作分类设置，展示原标题与立意，支持数量设定、模拟获取、运行反馈及分类结果；右侧增加第三步引导。
- 验证：浏览器验证前三步流程，默认返回 5 条、请求 20 条时返回实际 8 条；更新原标题或立意会清空第三步结果。仅离线 HTML 原型。

## v0.5.2.34（2026-10-24）
- 原型调整：火焰和排名合为紧凑徽标，第一名采用暖橙色，其他名次采用浅灰色，统一高度与对齐。
- 验证：JavaScript 语法检查及浏览器徽标内容、配色、高度检查通过。

## v0.5.2.33（2026-10-24）
- 原型调整：第二步已选原标题后增加底部对齐的分类标签；榜单列表交换分类与排名位置，第一名火焰随排名移动。
- 验证：JavaScript 语法及浏览器分类、排名位置检查通过。

## v0.5.2.32（2026-10-24）
- 原型调整：重选原标题按钮取消边框，与已选原标题内容区域垂直居中对齐，随标题高度自适应。
- 验证：浏览器确认边框为零、内容中心对齐。

## v0.5.2.31（2026-10-24）
- 原型调整：立意详情两栏改为 38.2% / 61.8%，右栏更宽；移除观点编号及状态文案，保留单选和选中边框。
- 验证：浏览器确认栏宽比例与单选切换，JavaScript 语法检查通过。

## v0.5.2.30（2026-10-24）
- 原型调整：核心立意改为单选卡片，提供选中边框、状态及已选观点摘要；更换原标题或重新生成时清空选择，为后续步骤保留观点数据。
- 验证：JavaScript 语法及浏览器单选交互检查。

## v0.5.2.29（2026-10-24）
- 原型调整：增加重选原标题按钮，回到榜单位置；核心立意卡片改为观点编号、突出观点正文、下方双栏展示展开方向与原标题关联，采用蓝灰白配色。
- 验证：浏览器检查重选跳转和结果生成；仅改原型。

## v0.5.2.28（2026-10-24）
- 修改内容：接入 AI Relay（relay.newbeeai.online）供给方协议（RSP 1.0），把「发布文章到头条」暴露为平台动作（写文章暂不接入）。新增 `modules/relay_supplier/`：crypto（HMAC-SHA256 验签/签名，5 分钟时间窗+多 secret 轮换）、envelopes（RSP 1.0 信封构造）、tasks（data/relay.db 订单幂等库，order_id 重放终态）、endpoint（信封分发：ping/invoke/poll/cancel，未知类型 not_supported）、server（ThreadingHTTPServer，默认 127.0.0.1:57380，仅 POST /relay，体≤1MB）、callback（终态回调 /v1/callbacks/{order_id}，退避 1/4/16/60/300s）、toutiao_bridge（订单→头条无界面发布编排：docx 下载校验→账号精确解析（多账号必须指定）→落 OutputDoc→upsert 入库→platform 定时（+2h~7d）或立即发布→轮询终态 10min；错误映射：未登录 not_available、结果未确认/失败 permanent 不可重试防重复发布、忙碌 rate_limited）、handlers（动作执行器：publish_toutiao_article 异步 + list_toutiao_accounts 同步）、manifest（manifest 构造/校验/导出 Config/relay_manifest.json）。
- GUI：独立「Relay 接单台」窗口（modules/relay_supplier/view/relay_manager_window.py，tk.Toplevel）——状态条+设置（启用/端口/密钥掩码/公网 URL/费用）+订单监控表（5s 刷新+双击详情）+运行日志；主导航唯一入口「Relay 接单台」，不混入既有弹窗/页面。主窗口：启动 bootstrap（启用则自动拉起端点）、关闭时停端点释放共享控制器、「头条发布」页改注入共享 AppController（订单与界面共用单 worker、同一张待发布表）。
- 验证：新增 modules/relay_supplier/tests/ 42 项（签名/信封/状态机/真实端口回环/回调重试/编排与错误映射/manifest/窗口，全部不启浏览器不触外网），加入 pytest.ini testpaths；全量 `python -m pytest -q` 833 passed（含 2 项已知 tkinter 环境 flake 未复现）。
- 涉及模块：modules/relay_supplier/**、ui/main_window.py、ui/views/navigation.py、tests/conftest.py、pytest.ini、README.md、docs/ARCHITECTURE.md、docs/README.md、docs/ai_relay_supplier.md（新增）、LOCAL_CHANGELOG.md

## v0.5.2.27（2026-10-24）
- 原型调整：移除核心立意设置重复标题，采用浅蓝灰统一底色；原标题去除嵌套卡片，生成条数与按钮并排，缩减纵向空间。
- 验证：浏览器核对标题选择与生成交互，保留榜单标题栏调整。

- 原型微调：数据总数移至榜单标题后，修改条件移至标题栏右侧，移除筛选摘要区域。
- 验证：浏览器核对标题栏与修改条件入口；git diff --check 通过。

## v0.5.2.26（2026-10-24）
- 原型微调：取消 Tips 一秒延迟，到达榜单区域立即显示，保留五秒自动消失。
- 验证：git diff --check 通过。

## v0.5.2.25（2026-10-24）
- 原型微调：榜单区域到位一秒后弹出 Tips，展示五秒；关闭、选中标题、重置及重新获取均取消待显示提示。
- 验证：git diff --check 通过。

## v0.5.2.24（2026-10-24）
- 原型调整：主题方向可选，为空匹配所有分类，仍受平台与文章标题数限制；更新输入提示，摘要显示全部分类。
- 验证：浏览器检查空主题获取；git diff --check 通过。

## v0.5.2.23（2026-10-24）
- 原型调整：标题与按钮改为获取平台当前榜单热门数据，移除时间范围控件和筛选条件，摘要、日志及引导同步更新。
- 验证：浏览器确认表单无时间控件、获取返回五条且摘要无时间条件；JavaScript 语法通过。

## v0.5.2.22（2026-10-24）
- 原型微调：结果数量改为共 N 条数据；移除筛选摘要中的请求条数，修改条件与摘要同排。
- 验证：git diff --check 通过。

## v0.5.2.21（2026-10-24）
- 原型微调：榜单成功后先滚动，待结果区域到达视口顶部再触发三秒浮动提示，每次获取仅触发一次。
- 验证：提示触发与滚动位置绑定，git diff --check 通过。

## v0.5.2.20（2026-10-24）
- 原型调整：右侧步骤状态随页面滚动位置更新，进入核心立意设置区域才激活第二步，浏览榜单时仍为第一步；浮动引导提示三秒后消失。
- 验证：浏览器检查榜单与核心立意设置的步骤激活状态。

## v0.5.2.19（2026-10-24）
- 原型调整：第二步引导改为页面顶部浮动提示，成功获取后显示六秒，可手动关闭；选中标题、重新获取或重置时收起，不占榜单布局。
- 验证：浏览器确认成功后浮层可见、fixed 定位且不在榜单容器内；JavaScript 语法通过。

## v0.5.2.18（2026-10-24）
- 原型微调：火焰图标移至第 1 名前且去掉 HOT 字样；选中标题自动定位核心立意设置；数量标签改为生成条数。
- 验证：浏览器确认图标顺序、生成条数标签及 Step 2 定位到视口顶部 18px；JavaScript 语法通过。

## v0.5.2.17（2026-10-24）
- 原型微调：成功获取原标题后自动滚动并聚焦榜单数据区域，显示第二步选择热门标题获取立意的提示；空结果与失败不跳转。
- 验证：JavaScript 语法与浏览器交互检查。

## v0.5.2.16（2026-10-24）
- 原型微调：排名移至原标题后方，以第 N 名展示；平台排名第一的条目增加火焰 HOT 图标。
- 验证：保留排名正序逻辑，git diff --check 通过。

## v0.5.2.15（2026-10-24）
- 原型修正：步骤按纵向展开，保留 Step 1；日志、榜单结果、Step 2 设置、核心立意结果依次位于其下方，获取后不再替换顶部设定或跳回顶部。
- 验证：浏览器确认五个区域可见且纵坐标依次递增；JavaScript 语法通过。

## v0.5.2.14（2026-10-24）
- 原型调整：侧栏使用统一线性 SVG 图标，图文稿件、文档加 AI 星芒、发布箭头分别对应三个业务入口；设置及 API 入口同步统一。
- 验证：五个导航图标均为内联 SVG，无新增外部资源。

## v0.5.2.13（2026-10-24）
- 原型微调：去掉核心立意获取按钮箭头与数量说明；已选原标题卡片改为白底、蓝色边线、深蓝文字。
- 验证：git diff --check 通过。

## v0.5.2.12（2026-10-24）
- 原型调整：结果区更名为平台榜单热门数据，移除重复标题与表头；原标题添加平台排名和来源热度，先按排名正序再截取 N 条，同名次按平台稳定排列。
- 验证：浏览器确认排名 1、1、2、2、3 正序及热度展示；JavaScript 语法通过。排名与热度均为模拟值。

## v0.5.2.11（2026-10-24）
- 原型微调：移除文章标题数旁的最多 N 条提示及获取按钮箭头（含执行后恢复文案）。
- 验证：git diff --check 通过。

## v0.5.2.10（2026-10-24）
- 原型微调：文章标题数默认五条，获取平台榜单热门数据按钮居中。
- 验证：git diff --check 通过。

## v0.5.2.9（2026-10-24）
- 原型调整：热门主题由模拟分类表按热度降序取前八条，无分类时整体隐藏；点击分类填入主题方向，下拉列表保留全部分类。
- 验证：浏览器验证空状态隐藏、十条分类仅显示前八条及点击填入；JavaScript 语法通过。尚未连接真实数据库。

## v0.5.2.8（2026-10-24）
- 原型微调：移除主题方向右侧的分类表状态标签，保留分类选择与手动输入。
- 验证：移除对应动态更新，git diff --check 通过。

## v0.5.2.7（2026-10-24）
- 原型微调：移除时间范围右侧的时区与采集时间提示文字，时间筛选逻辑不变。
- 验证：git diff --check 通过。

## v0.5.2.6（2026-10-24）
- 原型微调：第一步说明移至标题右侧，同一行底部对齐；窄屏允许换行。
- 验证：git diff --check 通过。

## v0.5.2.5（2026-10-24）
- 原型修正：恢复文章标题数 N，紧凑排列在主题方向旁；恢复最多 N 条、不足返回实际数量的行为。
- 验证：浏览器确认控件恢复及原标题返回 8/10 条和不足提示；JavaScript 语法通过。

## v0.5.2.4（2026-10-24）
- 原型调整：移除设定区标题、采集时间说明、分类空数据说明及原标题数量控件；紧凑排列时间、平台与主题，日期输入保留完整宽度。原标题默认返回全部匹配示例。
- 验证：浏览器确认移除项不再显示、获取后返回 8 条原标题；内联 JavaScript 语法检查通过。

## v0.5.2.3（2026-10-24）
- 原型调整：日志下方展示返回数据，首次执行完成前隐藏返回区域；设置蓝色、日志暖黄色、数据绿色、步骤引导紫色，以独立配色区分四区。
- 验证：浏览器确认初始返回区域隐藏、执行完成后显示、数据位于日志下方且无横向溢出；JavaScript 语法通过。

## v0.5.2.2（2026-10-24）
- 修改内容：按六条原型批注移除顶部栏与横向步骤条，更新宣传语和第一步名称；改为设定、日志、返回数据、步骤引导四区域，两个步骤共用结果与运行日志。
- 验证：浏览器确认原标题 8/10、核心立意 3/3 返回与日志联动；JavaScript 语法检查通过。仅修改 HTML 原型，未接入业务。

## v0.5.0.6（2026-10-23）
- 修改摘要：移除 Codex++ 本地代理与第三方模型覆盖，继承官方 Codex 用户设置；移除自动启动 guard 的指令。
- 涉及模块：.codex/config.toml、AGENTS.md。
- 验证：配置与指令不再引用 57321/57322，git diff --check 通过。

## v0.5.0.5（2026-10-23）
- 修改内容：左侧导航栏移除「待生成列表」「运行日志」两个入口，仅保留「图文生成」「头条发布」「系统设置」（及底部 API 设置 / 账号状态卡）。原稿/图文工作区内的运行日志页与待生成列表功能不变，只是不再从侧栏直达。
- 验证：清理死代码方法 _focus_pending / _focus_log；`python -m pytest tests/test_article_workspace.py tests/test_vendor_toutiao_integration.py -q`，导航/头条用例通过（2 项组高度持久化为环境性 tkinter Tcl flake，单跑通过）。
- 涉及模块：ui/views/navigation.py、LOCAL_CHANGELOG.md

## v0.5.0.4（2026-10-23）
- 修改内容：点击「头条发布」进入的 ToutiaoPublisher 工作区去除自家左侧栏——内嵌窗口原在右画布内又自带 196px 深色 rail（品牌 + 工作区：发布任务/账号管理/发布记录/应用设置 + 状态卡），与宿主导航栏重叠加出双列侧栏。现移除该内部 rail，主内容（待发布文章表 + 批量定时排期 + 运行日志）占满整个工作区宽度，账号管理/发布记录/应用设置入口随 rail 一并移除；宿主 AIDocStudio 左侧导航栏保留，作为返回主界面的入口。
- 验证：清理死代码（_build_rail/_nav_item/_focus_articles/_focus_accounts/_refresh_overview 及 rail 计数 StringVar 的遗留 set），`python -m pytest vendors/toutiao_publisher/tests/ tests/test_vendor_toutiao_integration.py -q`，257 passed。
- 涉及模块：vendors/toutiao_publisher/view/main_window.py、LOCAL_CHANGELOG.md

## v0.5.0.2（2026-10-21）
- 修改内容：移除左侧工作区重复的「原稿生成」入口，导航首项为「图文生成」；保留图文生成页内原稿生成控件与既有功能。
- 验证：更新导航回归断言，`python -m pytest tests/test_article_workspace.py -q`，24 passed。
- 涉及模块：ui/views/navigation.py、tests/test_article_workspace.py、LOCAL_CHANGELOG.md

## v0.5.0.1（2026-10-18）
- 修改内容：通过 Product Design 工作流将当前 Tkinter 界面结构同步到既有 Figma 文件。
  1. 更新图文生成、原稿生成、系统设置画板，新增单稿、批量图文稿、API 连接设置、完整设置状态，共 7 个可编辑画板；保留原有颜色变量与按钮组件，连接 51 处原型跳转。
  2. 新增 `design/aidocstudio-prototype/sync-current.js`，记录当前界面同步构建过程。目标文件 `wXKAjxrPRFw5TWGz89qcf9`；Figma 服务端缺少微软雅黑，使用 Noto Sans SC。账号、目录、正文均采用示例数据；完整设置为字段概览，徽标点击连线演示实际三击切换。
  3. 验证：7 个画板容器边界检查通过，47 个组件实例，所有 UI 为可编辑图层、无整屏图片；主工作区 512px JPEG 预览核对。未修改应用代码，未运行业务测试。
- 涉及模块：design/aidocstudio-prototype/sync-current.js、LOCAL_CHANGELOG.md

## docDev-v0.5.0.5（2026-10-18）
- 修改内容：批量「按篇数轮换」跨方向不切换 bug 修复 + 批量窗口加宽。
  1. Bug 修复：批量各方向各起一次图文流水线（PipelineService.run），而 run() 每次开始/结束都把豆包轮换游标归零到默认账号——因此「心不蒙尘」quota=4 时，每个方向都从头用它，生满 4 篇后仍继续用它，按篇数轮换从不切换。现为 run() 增加 `reset_rotation: bool = True` 参数（False 时跳过开始/结束归零），批量各方向统一传 False 使轮换游标延续到下一方向，整个批次共用同一个「本次生成」窗口；generate_batch 在整批开始与结束（含失败/强制终止）经 `_reset_batch_rotation` 统一归零，不残留 used。一键图文稿流程是单方向每次独立生成，维持原「每次生成归零」语义不变。
  2. 批量窗口（BatchWindow 批量生成图文稿）宽度 860 → 1060 (+200px)。
  3. 测试：新增 run(reset_rotation=False) 跨两次 run 延续轮换、批量各方向 run 均传 False、窗口几何 1060x360 等用例并更新受影响断言；全量 787 测试全绿（1 项 tkinter TclError 环境 flake 单跑通过）。
- 涉及模块：pipeline/service.py、ui/controllers/article_controller.py、ui/views/batch_window.py、tests/test_accounts.py、tests/test_batch_generation.py、LOCAL_CHANGELOG.md
- 时间：2026-10-18

## docDev-v0.5.0.4（2026-10-17）
- 修改内容：修正 tag 编号为四位制——本地提交 tag 一律 `vX.Y.Z.N`（三位 tag 只用于远程推送的发布点）。
  1. docDev 线重编号：docDev-v0.5.1/0.5.2/0.5.3 → docDev-v0.5.0.1/0.5.0.2/0.5.0.3（基线为已推送发布点 v0.5.0，N 从 1 起）；三个提交信息前缀同步改写（内容不变，hash 变更：8f37896→cbea604、d8f53d9→192e8c2、753ad35→65a907f）。
  2. AGENTS.md 双轨约定补四位编号硬规则与示例；changelog 条目同步改名。
  3. 已推送远程的三位 tag（v0.3.x、v0.4.0、v0.5.0 及更早）保持原样不动。
- 涉及模块：AGENTS.md、LOCAL_CHANGELOG.md
- 时间：2026-10-17

## docDev-v0.5.0.2（2026-10-17）
- 修改内容：批量窗口模态化 + 修复批量图文稿不进「图文稿列表」+ 列表新增「来源」列。
  1. 「批量图文稿生成设置」弹窗（BatchWindow）改为模态：打开时显式定位居中（相对主窗口；主窗口未映射时兜底屏幕居中），映射完成后 grab_set 安装模态（复用设置弹窗的延迟重试模式，最多 1 秒）；批量结束、进度窗销毁后宿主调用 reactivate_modal() 重新拿回 grab；destroy 时终止重试链防止残留 after 回调。
  2. Bug 修复：批量生成的图文稿此前要等下次进入/重启才出现在图文稿列表——图文流水线构造现在透传宿主 _on_doc_done 单篇回调（成稿一篇实时刷新一篇），批量 done 回调另调 _pipeline_reload_items() 兜底（中途失败/终止前已完成的篇目同样入列）。
  3. 「图文稿列表」在「状态」列前新增「来源」列（批量生成 / 单次生成）：pipeline_items 表新增 source 列（默认「单次生成」），app_db.initialize 对旧库自动 ALTER 补齐并回填；job_store.add_item 与 PipelineService 构造新增 source 参数；一键流程两处标记「单次生成」，批量全链路标记「批量生成」；_pipeline_reload_items 渲染来源，删除操作列因新列从 #4 移到 #5（_on_article_tree_click 按列表类型区分）。
  4. 测试：新增模态+居中/删除列路由/来源入列与 service 真实转发/add_item 缺省与显式/旧库列迁移 等用例并更新受影响断言；全量 717 测试全绿。
- 涉及模块：ui/views/batch_window.py、ui/main_window.py、ui/views/main_sections.py、
  ui/controllers/article_controller.py、ui/controllers/pipeline_controller.py、
  pipeline/app_db.py、pipeline/job_store.py、pipeline/service.py、
  tests/test_batch_generation.py、tests/test_article_workspace.py、
  tests/test_app_db.py、LOCAL_CHANGELOG.md
- 时间：2026-10-17

## docDev-v0.5.0.1（2026-10-17）
- 修改内容：批量生成按钮从「仅原稿」升级为全链路——批量窗口「开始批量生成」现在逐方向执行「主题稿 → 原稿 → 导出 → 图文稿」完整流程，与主界面「一键生成图文稿」语义完全一致。
  1. generate_batch 新增 plan_root/base_config 参数：原稿导出到 {原稿目录}/{方向} 后，中间产物复制到 {图文稿保存目录}/{方向}，以 plan_batch 模式跑 PipelineService（豆包配图→去水印→合并），成稿落 {图文稿保存目录}/{方向}/OutputDoc。
  2. 图文稿保存目录取启动批量时主界面「图文稿保存目录」当前值（全部方向共用，未设置则拒绝启动）；流水线配置在启动时主线程快照一次（state.build_config），批量中途改设置不影响本轮。
  3. 复制逻辑抽取为 pipeline_controller.copy_products_to_plan_dir（一键流程 start_with_export_dir 与批量共用，行为不变：同目录跳过复制/无产物失败/占用文件跳过）。
  4. 强制终止贯通图文阶段：ArticleController.cancel() 透传当前 PipelineService.cancel()；OperationCancelled 转 GenerationCancelled 中止整批。忙碌管理对齐一键流：批量期间禁用图文工作区开始按钮并暂停目录轮询，结束自动恢复。
  5. 失败口径与文章阶段对称：图文稿任一篇失败 → 该方向计失败（原稿已导出保留），其余方向不受影响；进度事件带「[方向] 图文稿：」前缀回投运行日志与进度窗。
  6. 文案同步：批量窗口标题/进度窗标题/工作区按钮改为「批量生成图文稿」「批量图文稿生成设置」。
  7. 测试 24 用例（新增 9：plan_root 校验、图文阶段失败隔离、failed_count 计失败、取消中止整批、cancel 透传、复制 helper 三情形、启动快照断言）；全量 712 测试全绿。
- 涉及模块：ui/controllers/article_controller.py、ui/controllers/pipeline_controller.py、
  ui/main_window.py、ui/views/batch_window.py、ui/views/article_workspace.py、
  tests/test_batch_generation.py、LOCAL_CHANGELOG.md
- 时间：2026-10-17

## v0.3.6（2026-10-17）
- 修改内容：集成旧项目 DeepSeekArticleGenAPI 的「加入批量生成」+「批量生成输出稿设置」能力到宿主原稿生成工作区。
  1. 主界面主题方向行新增两个按钮：「加入批量生成」（先落库当前方向 Prompt/保存目录，再把方向+生成稿数+输出目录 upsert 进批量清单，同方向覆盖更新）与「批量原稿生成设置」（单例窗口，已打开则置顶聚焦）。
  2. 新增宿主风格批量窗口 ui/views/batch_window.py：Treeview 列=主题方向/每次生成选题数/每次生成篇数/输出目录/操作(删除)，底部「开始批量生成/关闭」；运行中禁用启动、删除与关闭。数据模型复用 vendored BatchDirectionItem（纯 dataclass），保持 settings key ui.batch.directions 的 JSON 契约与旧项目兼容。
  3. MainWindow 批量方法组：清单懒加载缓存、DB settings 持久化（不进 XML settings.config）、加入/删除/同步窗口、启动批量（busy/空清单检查 + 模态进度窗 + 进度回投运行日志 + 完成写总耗时）。
  4. ArticleController.generate_batch：后台线程内独立 Storage，整批共用一个生成 channel；逐方向串行「现场主题稿 → 写库 → 原稿（篇数夹紧到实际选题数）→ 导出中间产物」，单方向失败隔离不中断整批，GenerationCancelled 中止全批；输出目录优先级=清单条目 > 方向配置 > 默认导出根，保留 {目录}/{方向} 约定。
  5. 新增 tests/test_batch_generation.py 15 用例（数据契约校正/读写去重/加入覆盖/删除/空清单与 busy 拦截/窗口列与运行态/串行+失败隔离+输出目录优先级）；全量 703 测试全绿。
- 涉及模块：ui/views/batch_window.py（新增）、ui/views/article_workspace.py、
  ui/main_window.py、ui/controllers/article_controller.py、
  tests/test_batch_generation.py（新增）、LOCAL_CHANGELOG.md
- 时间：2026-10-17

## v0.2.3.11（2026-10-16）
- 修改内容：新增多稿合并生成能力——同主题 3 个角度的原稿经「审核员评审 → 合并」产出 1 篇最终原稿（保留 3 篇候选 + 新增 1 篇合并稿 = 3+1）。
  1. 流程：3 篇候选原稿（各自含标题/正文/摘要/标签/配图）→ 评审 Agent 逐篇分析（信息密度/角度/结构/钩子/配图/AI味，输出 strengths/weaknesses/best_fragments/overall）→ 合并 Agent 取各稿精华重写为 1 篇终稿，配图点位与封面提示词按**新正文**重新生成（不复用单篇旧配图）。
  2. 新增接口：prompt_builder.build_review_prompt / build_merge_prompt（REVIEW_PROMPT / MERGE_PROMPT 模板）；generator.generate_merged_article（评审→合并→复用 reconcile_image_plan/validate_article 校验，merged_from 记录来源标题，不自动入库由调用方 add_article）。
  3. Article 新增 merged_from 字段，storage 增列 merged_from_json 并做旧库 _ensure_column 迁移；_row_to_article 兼容旧库无列。
  4. 新增 test_article_merge.py 5 用例（评审合并/预置评审/3+1 入库/配图对齐/取消中断）；article_gen 全模块 67 测试全绿，pipeline/full-flow/storage 回归 101 测试全绿。
- 涉及模块：modules/article_gen/core/domain/models.py、core/infra/storage.py、
  core/workflow/prompt_builder.py、core/workflow/generator.py、
  modules/article_gen/tests/test_article_merge.py、LOCAL_CHANGELOG.md
- 时间：2026-10-16

## v0.2.3.10（2026-10-16）
- 修改内容：修复火山方舟网关下模型推理未关闭导致生成耗时过长（主题稿 51s、原稿 28s）。
  1. 根因：原 DISABLE_THINKING_PAYLOAD 只发 enable_thinking=false，但火山方舟（ark）
     OpenAI 兼容层不识别该参数（官方文档明确"未出现 enable_thinking，请勿混淆"），
     推理照常输出——日志确认主题稿 1826/2421 token 为 reasoning（占 75%）。
  2. 修复：改为双写 {"thinking": {"type": "disabled"}, "enable_thinking": False}，
     thinking.type 是火山方舟官方关闭推理的参数，enable_thinking 兼容百炼 qwen。
  3. 实测（火山方舟 deepseek-v4-flash）：主题稿耗时 51s→9.5s，completion token
     2421→328，推理消失；llm_client 单测断言同步更新。
- 涉及模块：modules/article_gen/core/infra/llm_client.py、
  modules/article_gen/tests/test_llm_client.py、LOCAL_CHANGELOG.md
- 时间：2026-10-16

## v0.2.3.8（2026-10-14）
- 修改内容：增强原稿生成 Prompt，提升 AI 生成文章质量（方案第一步：提示词层）。
  1. 在默认原稿模板（Config/prompts/default_article_prompt.config，version 1→2）与代码兜底
     SYSTEM_TEMPLATE（prompt_builder.py）中新增四块内容：
     - 内容展开原则：具体场景→真实例子→比喻/对比三步展开、每段要有新信息、论述分层推进、
       保留限定词分寸感（避免注水凑字数/堆形容词）。
     - 负面约束清单：禁止翻案腔起手、相邻句同构、序数词当小标题、翻译腔（过长前置定语/
       「当…时」从句/句首连接词连用/生硬倒装）、空话套话收尾、AI 腔高频词、编造数据。
     - 结尾要求：最后一段（合）用有记忆点的金句收尾并单独成段。
     - 参考句式锚点：4 条可灵活化用的句式模板（few-shot 种子）。
  2. 原有全部约束（结构/字数/排版/配图点位/JSON 输出格式）保持不变；BizConfig 输出格式
     商业配置未改动；方向级 system_override 仍优先于默认模板。
- 涉及模块：Config/prompts/default_article_prompt.config、
  modules/article_gen/core/workflow/prompt_builder.py、LOCAL_CHANGELOG.md
- 时间：2026-10-14

## v0.2.3.6（2026-10-14）
- 修改内容：修复一键生成图文稿时「复制原稿中间产物失败 WinError 32」导致图文生成阶段中断。
  1. 根因：当「图文稿保存目录/{方向}」与原稿导出目录是同一目录（用户配置重叠，如图文稿保存目录设为原稿根目录）时，start_with_export_dir 对自身文件执行 shutil.copy2 自复制触发 WinError 32，图文生成未执行，导致无 OutputDoc、图文稿列表为空。
  2. 修复：两目录 resolve 相同则跳过复制直接以该目录为图文生成输入；不同目录复制时单个文件被占用（OSError）只跳过并记日志，不再整体中断。
  3. 修复后图文生成正常产出「{目录}/OutputDoc」（与归档的 OriginalDoc 同级），并写入 pipeline_items 供图文稿列表展示。
- 涉及模块：ui/controllers/pipeline_controller.py、tests/test_full_flow.py、LOCAL_CHANGELOG.md
- 时间：2026-10-14

## v0.2.3.5（2026-10-14）
- 修改内容：调试模式开启后，把每次与 API 接口交互的数据与过程详细内容写入 Log/YYYY-MM-DD-APIRequest.log。
  1. llm_client 新增 API_REQUEST_DEBUG 开关与 _api_request_log：请求（时间/URL/完整 payload）、响应（状态/耗时/响应体）、流程（第 N 次尝试、重试与退避）全部记录；探活（check_health）统一走 _post 同样被记录。
  2. ui/state 在 debug_mode 变化时经 set_api_request_debug 同步开关（含启动初值），徽标三连击切调试模式即生效。
- 涉及模块：modules/article_gen/core/infra/llm_client.py、ui/state.py、modules/article_gen/tests/test_llm_client.py、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-14

## v0.2.3.1（2026-10-14）
- 修改内容：修复自定义 API 连接通道（如 EToken）在生成时报「未知通道」。
  1. 根因：build_client 对未知通道要求 args 提供 base_url，而文章生成等路径以无参 open_channel() 构建客户端（args=None），自定义通道配置未回落 store，直接抛「未知通道: EToken」。
  2. 修复：build_client 未知通道分支的 base_url/model/api_key/wire_api 改为 args → store 已保存设置（API 连接设置弹窗写入）→ 默认值 依次回落；两者均无 base_url 才维持报错。
- 涉及模块：modules/article_gen/core/obs/config.py、modules/article_gen/tests/test_channel_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-13

## v0.2.2.7（2026-10-14）
- 修改内容：修复提交给 API 的主题稿/原稿 prompt 未合并 BizConfig 输出格式商业配置的问题。
  1. 根因：上版只在默认模板路径拼接输出格式；用户自定义 prompt 或方向配置 prompt（user_prompt / system_override）原样提交，丢失输出格式段。
  2. 修复：合并逻辑上提到提交层——topic_plan_prompt_text / build_article_prompt 在最终提交前统一合并 BizConfig 输出格式（默认/自定义/方向配置三路均生效）；已自带输出格式的旧完整 prompt 不重复追加（_ensure_output_format 按「输出格式（严格 JSON」标记去重）。
  3. 新增测试 test_output_format_is_merged_into_submitted_prompts 覆盖默认/自定义/方向配置三路与防重复。
- 涉及模块：modules/article_gen/core/workflow/prompt_builder.py、modules/article_gen/tests/test_prompt_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-14

## v0.2.2.5（2026-10-13）
- 修改内容：主题稿/原稿的「输出格式（严格 JSON）」段从业务 Prompt 分离为商业配置，存入工程根目录 BizConfig/。
  1. 新增 BizConfig/TitlePrompt.config（主题稿输出格式）与 BizConfig/OriginialPrompt.config（原稿输出格式），XML 格式与 Config/prompts 一致，通过 read_prompt_config 读取。
  2. Config/prompts/default_topic_prompt.config、default_article_prompt.config 及 prompt_builder 内嵌模板移除输出格式段；最终 prompt = 业务部分 + BizConfig 输出格式拼接，代码内置等值兜底常量保证 BizConfig 缺失时行为不变。
  3. app_paths 新增 BIZ_CONFIG_DIR，config_store 新增 TITLE_PROMPT_CONFIG / ORIGINAL_PROMPT_CONFIG 常量。
- 涉及模块：BizConfig/TitlePrompt.config、BizConfig/OriginialPrompt.config（新增）、app_paths.py、modules/article_gen/core/infra/config_store.py、modules/article_gen/core/workflow/prompt_builder.py、modules/article_gen/tests/test_prompt_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-13

## v0.2.2.2（2026-10-12）
- 修改内容：图文生成主页「开始生成」改为一键生成图文稿（主题稿 → 原稿 → 图文生成）。
  1. 主窗口新增 _start_full_flow：校验主题方向/原稿保存目录/图文稿保存目录后，先调 generate_articles（一条龙：主题稿 Prompt 生成主题稿 → 原稿 Prompt 生成原稿并导出到「原稿保存目录/{方向}」），成功后进入第二阶段。
  2. PipelineController 新增 start_with_export_dir：把原稿中间产物（docx + 配图说明 md）复制到「图文稿保存目录/{方向}」，以配图模式（plan_batch）运行图文生成流水线，最终稿落「图文稿保存目录/{方向}/OutputDoc」并写入图文稿列表。
  3. 目录轮询自动启动仍走原 _start（仅图文生成），按钮「开始生成」绑定 _start_full_flow；新增 _pipeline_full_worker 在流水线结束后释放原稿忙碌态。
- 涉及模块：ui/main_window.py、ui/controllers/pipeline_controller.py、ui/views/main_sections.py、tests/test_full_flow.py（新增）、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.29（2026-10-12）
- 修改内容：图文稿最终成稿路径与图文稿列表数据接入。
  1. 图文生成最终成稿保存到「图文稿保存目录/{主题方向}/OutputDoc」（新增 OUTPUT_DOC_SUBDIR 常量）。
  2. 图文生成（pipeline service）每篇成稿成功后写入 pipeline_items（job_store），图文稿列表 tab 即显示生成的图文稿；每篇完成回调刷新列表（_on_doc_done 增加 _pipeline_reload_items 调度）。
- 涉及模块：pipeline/config.py、pipeline/service.py、ui/main_window.py、tests/test_pipeline.py、tests/test_plan_pipeline.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.28（2026-10-12）
- 修改内容：原稿与图文稿的最终保存路径按「主题方向」分目录，图文稿保存目录文案更新。
  1. 生成主题稿 / 生成原稿最终保存到「原稿保存目录/{主题方向}」；原稿导出新增 _resolve_export_dir 统一计算并自动建目录。
  2. 图文生成最终成稿直接保存到「文档目录/{主题方向}」（去掉原 Output 子目录）；成稿与源文档同名时跳过归档，避免最终稿被误移到 OriginalDoc。
  3. 图文生成分组的「文档目录」文案改为「图文稿保存目录」。
- 涉及模块：ui/controllers/article_controller.py、pipeline/service.py、ui/views/main_sections.py、tests/test_article_workspace.py、tests/test_pipeline.py、tests/test_plan_pipeline.py、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.27（2026-10-12）
- 修改内容：修复导航切回「图文生成」工作区时模式被重置为「文档生成」的 Bug。
  1. 根因：导航「图文生成」入口 _on_doc_mode 旧实现强制 state.mode.set(MODE_BATCH)，从原稿生成切回时把用户选择的「配图生成」重置。
  2. 修复：_on_doc_mode 只切换工作区，不再重置模式；新增回归测试覆盖两种模式的保持。
  3. 核对图文稿列表删除链路：删除图文稿（pipeline_items）后列表即时刷新且切换工作区后不再显示。
- 涉及模块：ui/views/navigation.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.26（2026-10-12）
- 修改内容：生成稿件列表拆分并更名，图文稿独立展示。
  1. 原稿生成页「生成稿件列表」tab 更名为「原稿列表」，仍显示原稿（articles）。
  2. 图文生成页「生成稿件列表」tab 更名为「图文稿列表」，改为显示图文生成产物（pipeline_items 图文稿）。
  3. job_store 新增 list_all_items / delete_item；两个列表各自刷新与删除（原稿删 articles，图文稿删 pipeline_items），操作列点击按列表类型分流。
- 涉及模块：pipeline/job_store.py、ui/views/article_workspace.py、ui/views/main_sections.py、ui/main_window.py、tests/test_article_workspace.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.25（2026-10-12）
- 修改内容：生成稿件列表（原稿生成页与图文生成页）增加操作列与删除功能。
  1. 两个稿件列表在「状态」列后新增「操作」列，每行显示「删除」。
  2. 点击操作列的「删除」弹出确认框，确认后从数据库物理删除该稿件记录并同步刷新两个列表。
  3. 控制器新增 ArticleController.delete_article（经 Storage.delete_article）。
- 涉及模块：ui/views/article_workspace.py、ui/views/main_sections.py、ui/main_window.py、ui/controllers/article_controller.py、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.24（2026-10-12）
- 修改内容：API 连接设置弹窗布局与自定义通道支持。
  1. 去掉弹窗「API 连接」标题；「检测连接」按钮水平居中并消除与底部保存/取消按钮的空白。
  2. 通道改为可编辑下拉：预设通道可选，也支持手动输入自定义通道名保存并使用。
  3. 内核 obs/config 支持未知通道：resolve_llm_config / build_client 在自定义通道下按表单 args 构建 OpenAI 兼容客户端，「检测连接」对自定义通道同样可用。
- 涉及模块：ui/views/api_settings_dialog.py、modules/article_gen/core/obs/config.py、modules/article_gen/tests/test_channel_config.py、tests/test_api_settings_dialog.py（新增）、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.23（2026-10-12）
- 修改内容：主界面导航入口改名，新增 API 连接设置弹窗。
  1. 导航「账号管理」→「系统设置」（仍打开原设置弹窗）；「设置」→「API 连接设置」。
  2. 点击「API 连接设置」弹出与 DeepSeekArticleGenAPI 一致的连接配置弹窗：通道（下拉）/ 模型 / 接口地址 / API Key（掩码）+「检测连接」+ 保存/取消；取消恢复快照。
  3. 连接参数写入文章内核 Storage settings 表（键名与 DeepSeekArticleGenAPI env_store 一致：channel.active、{channel}.base_url/.model/.api_key/.wire_api），检测连接后台线程校验连通性并写入主日志。
- 涉及模块：ui/views/navigation.py、ui/main_window.py、ui/views/api_settings_dialog.py（新增）、LOCAL_CHANGELOG.md
- 时间：2026-10-12

## v0.2.1.22  2. 测试加固：test_article_workspace 增加 autouse 方向目录隔离，杜绝全量测试读写真实 Config/directions（此前部分用例只隔离设置与文章库，目录回填触发自动保存会写回真实方向配置）。
（2026-10-11）
- 修改内容：图文生成页面「图片生成」分组标题改为「图文生成」。
- 涉及模块：ui/views/main_sections.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

  4. 测试加固：test_pending_articles / test_pipeline 创建 MainWindow 的用例隔离文章库与主题方向目录（避免读写真实 data/app.db 与 Config/directions）。
## v0.2.1.21（2026-10-11）
- 修改内容：原稿生成与图文生成页面的「主题方向」控件改为与 DeepSeekArticleGenAPI 一致的可编辑分组下拉（TopicComboBox）。
  1. 移植 DeepSeekArticleGenAPI 的 TopicComboBox 到 ui/views/topic_combo.py：可编辑 Entry + ▼ 下拉，下拉按 TitleConfig.md 分组展示（分类加粗置灰不可选，主题可选），配色适配宿主 ui.theme。
  2. 内容以 DeepSeekArticleGenAPI 为主：分组来自 modules/article_gen/TitleConfig.md（野史/头条号热门/低粉爆款等 5 组 52 个主题）；已配置但未收录的方向自动并入「已有配置」分组，不影响既有方向。
  3. 主窗口刷新/方向切换/忙碌互斥全部适配新控件（新增 get/set/set_enabled/values 兼容接口），主题方向持久化与 Prompt 按方向保存逻辑不变。
- 涉及模块：ui/views/topic_combo.py（新增）、ui/views/article_workspace.py、ui/main_window.py、ui/theme.py、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

## v0.2.1.20（2026-10-11）
- 修改内容：原稿保存目录、主题方向、生成稿数三个控件数据持久化。
  1. 原稿保存目录归属当前主题方向：输入或选择目录后防抖保存到方向配置（output_dir），切方向/重启自动回填。
  2. 主题方向：切换时保存到全局设置（article_last_direction），启动时优先恢复上次选择。
  3. 生成稿数：变更即保存到全局设置（article_topic_count，夹紧 1-20），启动时恢复初始值。
- 涉及模块：pipeline/config.py、ui/views/article_workspace.py、ui/main_window.py、ui/controllers/article_controller.py、modules/article_gen/core/application/direction_service.py、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

## v0.2.1.19（2026-10-11）
- 修改内容：修复「生成原稿」按钮的行为——改为一条龙生成，先按主题稿 Prompt 现场生成主题稿，再按原稿 Prompt 生成原稿并导出。
  1. 原实现要求方向下必须先手动生成主题稿，否则报错「还没有主题稿」；现与旧版 _run_articles 语义对齐：主题稿总是现场生成并写库作历史记录，不再读取历史主题稿。
  2. 控制器 generate_articles 新增 topic_prompt 参数，主窗口「生成原稿」把主题稿 Prompt 一并传入；日志先提示「先生成主题稿：方向 × N」，再逐篇生成原稿。
- 涉及模块：ui/controllers/article_controller.py、ui/main_window.py、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

## v0.2.1.18（2026-10-11）
- 修改内容：图文生成页「运行日志和生成稿件列表」分组样式与原稿生成页对齐。
  1. 去掉图文页底部分组的卡片标题与提示语、1px 描边边框，改为与原稿生成页一致的无边框纯面板直接承载 Article.TNotebook。
  2. 两个分组的容器背景、边框与 Notebook 样式（Article.TNotebook）现已完全一致。
- 涉及模块：ui/views/main_sections.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

## v0.2.1.17（2026-10-11）
- 修改内容：图文生成页与原稿生成页布局调整。
  1. 图文生成页底部「启动和设置」分组替换为「运行日志和生成稿件列表」Notebook：运行日志 tab 显示主日志，生成稿件列表 tab 与原稿生成页列表共享同一数据源（两个页面各自的列表同时刷新）。
  2. 原稿生成页与图文生成页的「开始配图」「终止」按钮和「作业进度」进度条全部去掉，相关控制器方法（_article_run_pipeline / _article_cancel_pipeline / _article_set_progress）一并移除。
  3. 原稿生成页的「原稿生成」分组支持拖动调整高度并持久化（新增 article_group_height 设置键，与图文生成页的 pipeline_article_group_height 并存）。
- 涉及模块：ui/views/article_workspace.py、ui/views/main_sections.py、ui/main_window.py、pipeline/config.py、tests/test_article_workspace.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

## v0.2.1.16（2026-10-11）
- 修改内容：原稿生成页「导出目录」改为「原稿保存目录」，控件升级为与图文生成页「文档目录」相同的目录选择样式（输入框 + 选择目录按钮）。
  1. 标签文案「导出目录」→「原稿保存目录」。
  2. 输入框右侧新增「选择目录...」按钮，点击弹出目录选择对话框并回填输入框。
  3. 同步更新控制器与测试中的相关注释口径。
- 涉及模块：ui/views/article_workspace.py、ui/main_window.py、ui/controllers/article_controller.py、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-11

## v0.2.1.14（2026-10-10）
- 修改内容：设置弹窗分组改名与主界面控件迁移。
  1. 设置弹窗「调试与登录」分组标题改为「通用设置」。
  2. 新增账号默认值：每次生成篇数 4、默认账号 否（注册表为空时首个账号仍为默认）、固定对话标题 是。
  3. 主界面「启动定时器」移到设置弹窗「通用设置」标题行，位于「新增账号」左侧，同一行。
  4. 主界面「开始生成」从「启动和设置」移到「图片生成」行，位于「配图生成」之后、「文档目录」之前。
- 涉及模块：ui/debug_dialog.py、ui/views/main_sections.py、ui/main_window.py、ui/state.py、pipeline/accounts.py、pipeline/service.py、tests/test_accounts.py、tests/test_pending_articles.py、tests/test_settings_config.py、tests/test_poller_toggle.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.13（2026-10-10）
- 修改内容：设置弹窗继续精简，并修掉版权申明与底部按钮之间的空白。
  1. 去掉“调试模式（含详细日志）”勾选框：调试模式改为连点标题徽标三次切换（NORMAL ⇄ DEBUG），也可在 Config/settings.config 维护。
  2. 去掉完整配置下的“账号切换等待秒数”控件，改为只在 Config/settings.config 维护。
  3. 窗口高度贴合内容（原来固定多留 40px），版权申明与“保存 / 取消”之间不再出现空白区域。
  4. 同步更新配置文件注释与 README / 流程文档中的调试模式入口说明。
- 涉及模块：ui/debug_dialog.py、pipeline/config.py、README.md、docs/doubao_generation_flow.md、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.12（2026-10-10）
- 修改内容：设置弹窗交互与文案精简。
  1. 设置窗口保持模态：弹窗重新前置时重新安装 grab，保证输入不会落到主窗口。
  2. “新增账号 / 详细日志”改用 CompactAccent 样式，高度比“保存”少 4px。
  3. 去掉“调试与登录”分组的“默认显示”标签。
  4. 去掉账号列表上方的“豆包账号列表：生成从……”说明与“共 N 个账号……”提示。
  5. 去掉底部操作栏“保存后写入 Config/settings.config……”说明。
  6. 标题徽标支持连点三次切换调试模式：NORMAL ⇄ DEBUG（0.5 秒内三次）。
- 涉及模块：ui/debug_dialog.py、ui/theme.py、ui/main_window.py、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.11（2026-10-10）
- 修改内容：调整设置弹窗标题与“调试与登录”分组操作区。
  1. 移除标题栏“默认精简设置 · Config/settings.config”副标题。
  2. “新增账号…”按钮去掉省略号；“新增账号 / 详细日志”改为与“保存”一致的 Accent 按钮样式。
  3. 将两个按钮移动到“调试与登录”卡片标题行，位于“默认显示”标签前并保持同一行。
- 涉及模块：ui/debug_dialog.py、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.10（2026-10-10）
- 修改内容：设置弹窗最上方自绘标题栏增加 1px 边框，并移除原本的独立底部分隔线，避免视觉上出现双线。
- 涉及模块：ui/debug_dialog.py、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.9（2026-10-10）
- 修改内容：修复设置弹窗既有“点击后不显示”问题，并把设置窗口改为真正的模态窗口。
  1. 模态 grab_set 从窗口映射前改到映射成功后执行，避免 “window not viewable” 错误被静默吞掉。
  2. 弹窗创建后显式 deiconify / lift / focus_force，并临时置顶 250ms，避免被最大化主窗口遮住。
  3. 模态安装失败时短暂重试；窗口关闭或 root 不可见时安全停止，不遗留 after 回调。
  4. 打开设置失败时写入运行日志，不再把构造异常静默吞掉。
- 涉及模块：ui/debug_dialog.py、ui/main_window.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.8（2026-10-10）
- 修改内容：修复设置弹窗去掉系统标题栏后可能被最大化主窗口遮住的问题；弹窗创建完成后显式前置并聚焦，临时置顶 250ms 后恢复正常层级。
- 涉及模块：ui/debug_dialog.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.7（2026-10-10）
- 修改内容：按用户澄清，保留设置弹窗自绘标题条中的「设置」文字行，改为隐藏系统窗口标题栏；自绘标题条支持拖动窗口，Esc 可关闭。
- 涉及模块：ui/debug_dialog.py、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.6（2026-10-10）
- 修改内容：去掉设置弹窗顶部标题条中与系统窗口标题重复的「设置」文字行，保留副标题与 NORMAL / DEBUG 徽标。
- 涉及模块：ui/debug_dialog.py、tests/test_settings_config.py、LOCAL_CHANGELOG.md
- 时间：2026-10-10

## v0.2.1.5（2026-10-09）
- 修改内容：移除“原稿生成”分组标题后“主题方向 → 主题稿 → 原稿 → 导出”的说明文案，原稿生成页与图文生成页共用分组同步生效；不更新 Figma。
- 涉及模块：ui/views/article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-09

## v0.2.1.4（2026-10-09）
- 修改内容：修复图文生成页启动设置截断图片生成的问题，并支持原稿生成分组高度调整与持久化。
  1. 原稿生成、图片生成、启动和设置改为同一滚动布局，启动设置紧随图片分组，自动联动且不受旧分隔条坐标影响。
  2. 图文生成页原稿分组底部增加拖动调整条，Prompt 编辑区随高度伸缩；调整高度后下方分组同步移动。
  3. 将 pipeline_article_group_height 登记到 XML 配置的自动保存状态分组，松手后保存，启动时恢复，并对异常与越界高度做回退或限制。
  4. 增加实际窗口布局、拖动联动、小窗口滚动、XML 高度保存与启动恢复回归测试；全量测试 702 passed，git diff --check 通过。
- 涉及模块：pipeline/config.py、ui/{main_window.py,views/article_workspace.py,views/main_sections.py}、tests/{test_article_workspace.py,test_pending_articles.py,test_settings_config.py}、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-09

## v0.2.1.3（2026-10-09）
- 修改内容：将完整“原稿生成”分组复制到图文生成页，位于“图片生成”上方，支持在同一页完成原稿生成、配图与图文合并。
  1. 提取共用原稿生成视图，保留多稿/单稿、主题方向、生成数量、导出目录、配图操作及 Prompt 子分组。
  2. 两页共用输入变量、Prompt、作业进度与忙碌状态；切换页面保留待保存的 Prompt，图文生成页显示原稿任务日志。
  3. 原稿与图片生成区域增加垂直滚动条与鼠标滚轮支持，适配较小窗口。
  4. 新增复制分组、按钮参数连接、共享状态及 Prompt 保存回归测试；全量测试 697 passed，git diff --check 通过。
  5. 按项目约定不更新 Figma 设计、生成脚本或插件文件。
- 涉及模块：ui/{main_window.py,views/article_workspace.py}、tests/{test_article_workspace.py,test_pending_articles.py}、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-09

## v0.2.1.2（2026-10-09）
- 修改内容：在项目 AGENTS.md 中记录界面修改默认不更新 Figma 生成脚本、插件及设计内容，仅在用户明确要求时同步。
- 涉及模块：AGENTS.md、LOCAL_CHANGELOG.md
- 时间：2026-10-09

## v0.2.1.1（2026-10-09）
- 修改内容：将图文生成页“图片要求设定”移入“图片生成”，作为文档生成控件下排的子分组。
  1. 子分组保留图片要求编辑框、滚动条与自动保存状态，沿用现有分组边框样式。
  2. 同步 HTML 原型、Figma 生成脚本与 README 中的界面结构说明。
  3. 界面相关测试 93 passed；HTML 原型浏览器检查确认子分组位于模式行下方，内容未越出分组边界；Figma 插件语法检查通过。
- 涉及模块：ui/{main_window.py,views/main_sections.py}、tests/test_pending_articles.py、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-09

## v0.2.0.16（2026-10-08）
- 修改内容：细化原稿生成页分组边框与页签样式，并精简图文生成页标题。
  1. Prompt 分组恢复完整外边框，内部仍保留主题稿与原稿提示编辑区。
  2. 移除运行日志/生成稿件列表分组外框，仅保留日志内容区自身的输入框边框。
  3. 统一运行日志与生成稿件列表页签的选中/未选中内边距，选中高度按未选中高度显示。
  4. 图文生成页“文档生成模式”分组标题改为“图片生成”，并移除“目录批处理”说明。
  5. 移除“图片要求设定”标题后的提示词说明。
  6. 同步更新 HTML 原型、Figma 生成脚本、README 与界面回归测试。
  7. 全量 `pytest` 694 passed，`git diff --check` 与 Figma 插件语法检查通过。
- 涉及模块：ui/{theme.py,main_window.py,views/article_workspace.py,views/main_sections.py}、tests/{test_article_workspace.py,test_pending_articles.py}、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-08

## v0.2.0.15（2026-10-08）
- 修改内容：调整原稿生成页 Prompt 与稿件列表布局。
  1. 移除稿件列表分组的可见标题，保留运行日志与生成稿件列表两个 Tab。
  2. 去掉运行日志 Tab 行的默认灰色背景，页签与卡片保持同一底色。
  3. 将 Prompt 分组移入“原稿生成”卡片，并放到“开始配图”操作行下方。
  4. Prompt 提示改为“一个主题方向对应一个主题稿Prompt 和一个原稿Prompt”。
  5. 同步更新 HTML 原型、Figma 生成脚本和界面回归测试。
  6. 全量 `pytest` 694 passed，`git diff --check` 通过。
- 涉及模块：ui/{theme.py,views/article_workspace.py}、tests/test_article_workspace.py、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、LOCAL_CHANGELOG.md
- 时间：2026-10-08

## v0.2.0.14（2026-10-07）
- 修改内容：按最新界面要求精简图文生成工作区与原稿生成控件。
  1. 「生成主题稿」与「生成文章标题」统一使用强调按钮样式。
  2. 「文档目录」目录输入框与「选择目录」移动到「启动定时器」后同一行。
  3. 移除可见的「待生成文档列表」分组；保留隐藏兼容 Treeview，继续支撑批处理刷新、行移除与列宽持久化。
  4. 移除「启动和设置」中的「设置」按钮，设置弹窗仍由左侧导航进入。
  5. 同步更新 HTML 原型与 Figma 生成脚本，并调整布局回归测试。
  6. 全量 `pytest` 694 passed，Python 语法与 Figma 插件语法检查通过。
- 涉及模块：ui/{main_window.py,views/article_workspace.py,views/main_sections.py}、tests/{test_article_workspace.py,test_pending_articles.py}、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.13（2026-10-07）
- 修改内容：统一原稿生成操作样式，并重构稿件列表区域。
  1. “生成主题稿”和“生成原稿”统一使用强调按钮样式。
  2. 数量控件文案由“选题数”改为“生成稿数”。
  3. 稿件列表区改为两个 Tab：默认“运行日志”，第二个“生成稿件列表”；原状态消息改为写入运行日志。
  4. HTML 原型支持 Tab 切换，Figma 生成插件同步增加页签、运行日志面板和隐藏的稿件列表面板。
  5. 更新布局、日志与按钮样式测试；全量 `pytest` 693 passed / 1 skipped，Figma 插件语法检查通过。
- 涉及模块：ui/{main_window.py,views/article_workspace.py}、tests/test_article_workspace.py、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.12（2026-10-07）
- 修改内容：精简原稿生成控件并统一第二阶段稿件术语。
  1. 移除“开始配图”下方的状态 Label；HTML 原型与 Figma 插件同步移除对应状态节点。
  2. 移除独立的“篇数”控件，生成原稿时直接复用“选题数”输入值。
  3. 全工程第二阶段稿件术语统一为“原稿”，覆盖界面、日志、模块、测试、文档与原型。
  4. 更新原稿生成布局与数量复用测试；全量 `pytest` 693 passed / 1 skipped，Python 语法与 Figma 插件检查通过。
- 涉及模块：ui/{main_window.py,views/article_workspace.py}、tests/test_article_workspace.py、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、文章模块与全工程文案
- 时间：2026-10-07

## v0.2.0.11（2026-10-07）
- 修改内容：统一「主题稿」与 `DocGenStudio` 命名，调整原稿生成工作模式与导出目录布局。
  1. 将工程中的稿件术语统一为「主题稿」，包含界面、Prompt、测试、文档和原型。
  2. 将工程中的宿主品牌统一为 `DocGenStudio`，并重命名启动器为 `DocGenStudio.bat` / `DocGenStudio.command`。
  3. 原稿生成工作模式行移除模式说明 Label，将「导出目录」移到「单稿生成」后同行显示。
  4. 同步更新 HTML 原型与 Figma 插件，并修正 README 中工程实际路径。
  5. 全量 `pytest` 692 passed / 1 skipped；Figma 插件 `node --check` 通过。
- 涉及模块：全工程命名替换、`DocGenStudio.bat`、`DocGenStudio.command`、ui/{main_window.py,views/article_workspace.py}、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、tests/test_article_workspace.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.10（2026-10-07）
- 修改内容：调整原稿生成区的按钮布局与工作模式文案。
  1. 「生成主题稿」移到「选题数」之后、「篇数」之前，并与主题方向、两个数量控件同排。
  2. 「生成原稿」移到「篇数」之后，与上一控件同排；导出目录改为独立行。
  3. 工作模式「主题稿生成」改为「多稿生成」，「单原稿生成」改为「单稿生成」；模式提示同步更新。
  4. 同步 HTML 原型与 Figma 插件的控件顺序，并移除原型中遗留的「导出全部」按钮。
  5. 更新布局顺序与模式文案测试；全量 `pytest` 692 passed / 1 skipped。
- 涉及模块：ui/{main_window.py,views/article_workspace.py}、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、tests/test_article_workspace.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.9（2026-10-07）
- 修改内容：调整工作区导航名称与顺序，并移除重复入口。
  1. 左侧工作区「文章生成」改为「原稿生成」，并移到第一行；「文档生成」改为「图文生成」。
  2. 移除左侧工作区「配图生成」入口；「文档生成 / 配图生成」保留为图文生成工作区内部的模式单选。
  3. 同步更新应用原稿工作区标题、HTML 原型与 Figma 插件导航文案。
  4. 更新导航顺序/入口测试；全量 `pytest` 692 passed / 1 skipped。
- 涉及模块：ui/{main_window.py,views/navigation.py,views/article_workspace.py}、design/aidocstudio-prototype/{index.html,figma-plugin/code.js}、tests/test_article_workspace.py、tests/test_pending_articles.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.8（2026-10-07）
- 修改内容：文章生成页保留 Prompt 浏览/修改，并取消「导出全部」，改为生成原稿后直接导出到「导出目录」。
  1. 在稿件列表上方新增「Prompt」卡片：左「主题稿 Prompt」、右「原稿 Prompt」两块可编辑文本域，按主题方向自动载入、切换方向自动重载并防抖保存，支持「恢复默认」。
  2. 生成主题稿 / 原稿 / 单篇时使用编辑区中的实时 Prompt 文本；方向未配置 Prompt 时自动回填默认 Prompt。
  3. 去掉「导出全部」按钮与 `ArticleController.export_articles()`；生成原稿（批量与单篇）后直接导出到界面「导出目录」，留空时回落到方向配置目录、再回落到默认导出根。
  4. 新增/更新测试：Prompt 载入-修改-恢复默认、单篇导出目录优先级；全量 `pytest` 692 passed / 1 skipped。
- 涉及模块：ui/{main_window.py,views/article_workspace.py,controllers/article_controller.py}、tests/test_article_workspace.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.7（2026-10-07）
- 修改内容：重新按 DeepSeekArticleGenAPI `personal` 分支（8b3431b）合并，纠正上一版误按 `main` 合成的问题。
  1. 三方合并保留 AIDocStudio 集成改写（`modules.article_gen.*` 全限定导入、统一 `APP_DB`），同时合入个人版 `ui/main_window.py`、`ui/segmented.py` 与界面架构测试。
  2. 宿主工作区接入个人版双模式：新增「主题稿生成 / 单原稿生成」工作模式栏与「由主题方向生成 / 手动输入」标题来源栏；`ui/views/segmented.py` 提供 Figma 风格分段控件。
  3. 单原稿支持先生成文章标题再写一篇、或直接用手动标题写一篇；`ArticleController` 新增 `generate_single_title()` / `generate_single_article()`，复用主题稿与原稿 Prompt，入库并自动导出。
  4. 修正宿主工作区 `body` 同容器混用 `grid`/`pack` 的几何管理器冲突（工作区改用格子布局）；「生成主题稿」改用选题数、「生成原稿」用篇数，两个数量不再互相串用。
  5. 新增 `tests/test_article_workspace.py` 双模式切换用例与单原稿入库/导出用例；全量 `pytest` 691 passed / 1 skipped。
- 涉及模块：ui/{main_window.py,views/article_workspace.py,views/segmented.py,controllers/article_controller.py}、modules/article_gen/{ui/main_window.py,ui/segmented.py,tests/test_api_only_architecture.py,LOCAL_CHANGELOG.md}、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.6（开发中）
- 修改内容：按浏览器批注调整 AIDocStudio 原型。
  1. 文档生成页“启动和设置”中的设置 / 开始生成 / 强制终止三个按钮整组水平居中，进度条独占下一行。
  2. 左侧导航移除“配图生成”入口，保留文档生成、文章生成、待生成列表、运行日志和账号管理。
  3. 同步更新 HTML 原型和 Figma 生成插件；已重新运行插件刷新 Figma 原型。
- 涉及模块：design/aidocstudio-prototype/index.html、design/aidocstudio-prototype/figma-plugin/code.js、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.5（开发中）
- 修改内容：新增 AIDocStudio 图文文档全流程 HTML 交互原型，并同步导入 Figma。
  1. 新增 `design/aidocstudio-prototype/index.html`：覆盖文档生成、文章生成、设置弹窗三个 1440 × 1024 状态，支持顶部状态切换、进度演示、连接检测与设置弹窗交互。
  2. 新增 `design/aidocstudio-prototype/figma-plugin/`：以本地开发插件创建 `AIDocStudio / 00 Foundations`、`AIDocStudio / 01 Screens` 与 `AIDocStudio / Tokens`，生成 3 个可编辑画板、9 个按钮/状态组件、29 个颜色变量和 6 条原型连线。
  3. Figma 文件：`https://www.figma.com/design/wXKAjxrPRFw5TWGz89qcf9/AIDocStudio-图文文档全流程界面原型`。
  4. `modules/article_gen/design/figma-sync/cu.mjs` 改为自动发现 Codex CUA Node 运行时，避免运行时目录版本变化后脚本失效。
- 涉及模块：design/aidocstudio-prototype/{index.html,figma-plugin/**}、modules/article_gen/design/figma-sync/cu.mjs、LOCAL_CHANGELOG.md
- 时间：2026-10-07

## v0.2.0.4（开发中）
- 修改内容：M4+M5+M6 落地——文章导出与配图流水线编排打通，「方向 → 文章 → 导出 → 生图 → 去水印 → 合并成稿」整条链路可在唯一窗口内跑通。
  1. M4 编排层：新增 `pipeline/job_store.py`（`pipeline_jobs` / `pipeline_items` / `pipeline_artifacts` 的短事务读写）与 `pipeline/orchestrator.py`（按方向选出「尚未出成稿」的文章 → 导出 docx + 配图说明 md 到作业区 → 调宿主 `PipelineService` 跑 plan_batch）；不复制生图 / 去水印 / 合并算法。
  2. M4 进度与取消：按合并方案 §10 的权重把 EXPORT..MERGE 重新归一化到单进度条（EXPORT 0.000-0.067，其后线性映射到底层整体进度）；「终止」透传 `PipelineService.cancel()`，已完成产物保留。
  3. M4 界面接线：文章工作区新增「开始配图 / 终止 / 作业进度」控件；`ArticleController.run_full_pipeline()` 复用宿主设置（图片要求 / 去水印 / 合并）组装 `plan_batch` 配置，后台线程执行、进度经 `win.after` 回投。
  4. M5 契约标记：`export_cover_spec()` 首行写 `<!-- aidoc-contract: v1; article-id: …; task-id: … -->`；`plan_reader` 忽略非标题行，三种既有点位格式不受影响。
  5. M5 工作区隔离：产物落到 `<导出根>/<主题方向>/<YYYYMMDD-HHmmss>-<job_id>/`，成功后源文件归档 `OriginalDoc/`；导出与归档后的实际路径回写作业条目，便于回溯。
  6. M2 收口：新增 `migrate_legacy_settings()`，首次建统一库时把旧文章库 `settings` 的缺失键（含百炼 API Key）补齐到 `data/app.db`，只读旧库、不覆盖已有值；`initialize()` 仅在真正的统一库上执行迁移。
  7. M6 测试：新增 `tests/test_orchestrator.py`（导出 / 作业登记 / 契约标记 / 跳过已出稿 / 取消透传 / 建库，共 6 项）、`tests/test_app_db.py` 补设置迁移 3 项、`tests/test_article_workspace.py` 补配图控件与控制器接线 2 项；全量 `pytest` 689 passed / 1 skipped。
  8. M6 文档：`README.md` 标题与开篇改为 AIDocStudio 图文文档全流程，新增全链路、作业区、契约、统一数据与配置说明。
- 涉及模块：pipeline/{job_store,orchestrator,app_db}.py、app_paths.py、ui/{main_window.py,views/article_workspace.py,controllers/article_controller.py}、modules/article_gen/core/workflow/exporter.py、tests/{test_orchestrator,test_app_db,test_article_workspace}.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-06

## v0.2.0.3（开发中）
- 修改内容：M3 UI 收口——保留 DocGenStudio 唯一 Tk 根窗口，新增「文章生成」工作区。
  1. 新增 `ui/views/article_workspace.py`：文章生成页面（主题方向 / 选题数量 / 生成主题稿 / 生成原稿 / 导出全部 + 稿件列表），控件统一取自 `ui.theme`。
  2. 新增 `ui/controllers/article_controller.py`：封装 `modules.article_gen` 的主题稿 / 原稿 / 导出能力，后台线程内新建独立 `Storage`，结果与进度经 `win.after` 回投主线程。
  3. `ui/main_window.py`：工作区改为双页面容器（流水线 / 文章生成）互斥显示，新增 `_show_article_workspace` / `_show_pipeline_workspace` 与文章工作区薄转发方法。
  4. `ui/views/navigation.py`：左侧导航新增「文章生成」入口与 `set_active_section()`；文档/配图入口切回流水线工作区。
  5. `main.py`：启动时 `app_paths.ensure_dirs()` + `pipeline.app_db.initialize()`；新增 `AIDocStudio.bat` 启动脚本。
  6. 文章内核遗留库默认值改指统一 `APP_DB`；`DeepSeekArticleGenAPI.bat` 改为从工程根以 `-m modules.article_gen.main` 启动。
  7. 新增 `tests/test_article_workspace.py`：验证唯一根窗口、两工作区互斥显示与导航切换。
- 涉及模块：ui/main_window.py、ui/views/{article_workspace,navigation,__init__}.py、ui/controllers/{article_controller,__init__}.py、main.py、AIDocStudio.bat、modules/article_gen/{ui/main_window.py,DeepSeekArticleGenAPI.bat}、tests/test_article_workspace.py、LOCAL_CHANGELOG.md
- 时间：2026-10-06

## v0.2.0.2（开发中）
- 修改内容：M2 数据与配置统一——工程级统一库 + 配置分层。
  1. 新增 `app_paths.py`：集中定义 Config / directions / prompts / data / Log / 导出根目录，消除合并前各处用 `__file__` 各自推断导致的路径漂移。
  2. 配置分层：`modules/article_gen/Config/*.config` 拆为 `Config/directions/*.config`（主题方向）与 `Config/prompts/*.config`（默认 Prompt）；`config_store.py`、`direction_service.py` 改从工程级目录解析。
  3. 统一数据库：新增 `pipeline/app_db.py`，在 `data/app.db` 同时建文章域（`tasks`/`articles`/`topic_plans`/`settings`/`direction_configs`）与流水线域（`pipeline_jobs`/`pipeline_items`/`pipeline_artifacts`）表，幂等建库、WAL + busy_timeout。
  4. 文章内核 `Storage` 默认库由 `data/articles.db` 改为统一库；开启 WAL 与 busy_timeout；`--db` 默认同步、`default_export_dir()` / 日志目录 / 计时文件均改从 `app_paths` 取值。
  5. `.gitignore` 增加 `/data/`（运行期数据库不入库）；新增 `tests/test_app_db.py` 校验两域建表、幂等与 WAL。
- 涉及模块：app_paths.py、pipeline/app_db.py、Config/directions/**、Config/prompts/**、modules/article_gen/{main.py,core/**}、.gitignore、tests/test_app_db.py、LOCAL_CHANGELOG.md
- 时间：2026-10-06

## v0.2.0.1（开发中）
- 修改内容：AIDocStudio 合并工程 M0+M1 落地——以 DocGenStudio/simple 为宿主，git subtree 导入 DeepSeekArticleGenAPI。
  1. M0：`git clone --branch simple` 建立 `E:\Codex\AIDocStudio`，新建 `merge/aidocstudio` 分支，添加 `article-api` remote，以 `git subtree add --prefix=modules/article_gen article-api main --squash` 导入文章内核。
  2. M1：把文章内核 13 个文件的根绝对导入（`from core.*` / `from ui.*` / `import core`）统一改写为 `modules.article_gen.*` 全限定导入，消除与宿主顶层 `ui` 包的命名冲突。
  3. 新增 `modules/__init__.py`、`modules/article_gen/__init__.py` 包标记；移除 `modules/article_gen/tests/conftest.py` 的 `sys.path` 注入（该注入会遮蔽宿主 `ui`）。
  4. 新增 `pytest.ini`：testpaths 覆盖两侧 tests，模块路径靠 `__init__.py` 与工程根 rootdir 区分。
  5. `modules/article_gen/tests/test_api_only_architecture.py`：`from main import build_parser` 改为全限定导入，子进程 cwd 指向工程根。
  6. `requirements.txt` 合并文章内核依赖：`requests>=2.31`、`markdown-it-py>=4`、`pytest>=8`。
- 涉及模块：modules/__init__.py、modules/article_gen/**、pytest.ini、requirements.txt、LOCAL_CHANGELOG.md
- 时间：2026-10-06

## v0.1.23.1（开发中）
- 修改内容：按「DocGenStudio 界面原型」（Figma）重做主界面与设置弹窗视觉，业务逻辑、配置字段与公开接口不变。
  1. 新增 `ui/theme.py`：集中墨青配色 / 字体 / ttk 样式（clam）与卡片、药丸、按钮、文本框工厂，颜色不再散落在各视图。
  2. 新增 `ui/views/navigation.py`：左侧深墨青导航（文档生成 / 配图生成 / 待生成列表 / 运行日志 / 账号管理 / 设置 + 当前账号状态卡），点击映射到主窗口既有行为（切模式、定位列表/日志、打开设置）。
  3. `ui/views/main_sections.py`：工作区改为四张卡片（文档生成模式 / 图片要求设定 / 待生成文档列表 / 启动和设置），保留 `spec_text`、`dir_row`、`dir_entry`、`_pending_tree`、`start_btn`、`stop_btn`、`progress`、`log_text` 等控件名，以及 `_input_frame` / `_pending_frame` 的 `fill=both + expand` 弹性几何。
  4. `ui/main_window.py`：装配「左侧导航 + 右侧画布工作区」骨架，启动时初始化主题；模式切换与列表刷新同步导航高亮、待生成计数药丸与导航计数。
  5. `ui/debug_dialog.py`：弹窗改为「标题条（NORMAL / DEBUG 徽标）+ 白底描边卡片分组 + 底部说明与保存/取消」；分组内容、精简/完整调试切换与 XML 配置持久化不变。
  6. `tests/test_pending_articles.py`：模式单选按钮改为「按带 value 的选项控件」定位（左侧导航存在同名文案），分组标题断言改为原型文案。
- 涉及模块：ui/theme.py、ui/views/navigation.py、ui/views/main_sections.py、ui/views/__init__.py、ui/main_window.py、ui/debug_dialog.py、README.md、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-06

## v0.1.21.2（开发中）
- 修改内容：将设置中的「调试模式」与「详细调试日志」合并为一个「调试模式（含详细日志）」开关。
  1. `ui/debug_dialog.py` 删除独立「详细调试日志」复选框，开启合并开关时同时启用调试行为和 `[调试]` 明细显示。
  2. `AppState` 以 `debug_mode` 为唯一用户入口，兼容字段 `verbose_log` 自动跟随；`Config/settings.config` 只保留 `debug_mode` 配置项。
  3. 主窗口详细日志显示改由 `debug_mode` 控制；`PipelineConfig.verbose_log` 和底层 `DoubaoImageBot` 参数保留为兼容字段，由应用状态自动同步。
  4. 旧 `verbose_log` 设置继续可读取但不单独显示、不独立持久化，避免两个调试开关产生分叉。
- 涉及模块：ui/state.py、ui/debug_dialog.py、ui/main_window.py、pipeline/config.py、pipeline/models.py、pipeline/service.py、Config/settings.config、tests/test_settings_config.py、tests/test_pipeline.py、tests/test_log_split.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05

## v0.1.21.1（开发中）
- 修改内容：执行设置简化第一阶段，将兼容/排障/算法回退类选项从设置弹窗移到配置文件。
  1. 设置弹窗保留日常项：豆包等待与下载模式、去水印开关与覆盖策略、合并输出、批量扫描、日志与账号列表；底部「保存 / 取消」继续保留。
  2. `Config/settings.config` 新增「高级配置（配置文件专用，设置弹窗已隐藏）」分组，收录冷却秒数、输入慢动作、水印引擎/内核/掩码、覆盖源文档、删除图片、文档间隔、账号切换等待等已隐藏项。
  3. 高级分组增加分组级用途/修改方式/取值规则/风险提示，并为每个高级项补齐可输入值、默认值、生效条件和风险；账号列表列宽归入自动保存的界面状态分组。
  4. 移除下载模式对 `force_top_left_remove` 的弹窗联动，避免打开设置时清掉手工 XML 值；隐藏设置仍保留原键名、默认值、持久化和流水线行为。
- 涉及模块：pipeline/config.py、ui/debug_dialog.py、Config/settings.config、tests/test_settings_config.py、tests/test_accounts.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05

## v0.1.16.28（开发中）
- 修改内容：将去水印首次擦除改为 `DocGenStudio 识别 + DocGenStudio 复核重擦 + SSWatermarkRemove 掩码/Alpha/快路径/LaMa` 混合内核。
- 修复：豆包固定对话标题在前 5 个历史对话中匹配第二项时可能漏匹配。
  1. 侧栏标题读取优先聚合 `a[href*="/chat/"]`，且第一组选择器只命中部分条目时
     继续汇总其余选择器，不再提前结束。
  2. `limit=1` 得到的不完整标题缓存不再直接用于 `limit=5` 匹配；标题不足时
     等待侧栏渲染后重试一次，确保第二条及后续对话能进入匹配列表。
  1. 新增 `masking_hybrid.py`，移植 SS 的 auto/full/stroke 逐框策略、框线提取、
     半透明 Alpha 掩码细化，以及 4 字/6 字羽化规则。
  2. 新增 `alpha_recovery.py`、`fast_inpaint.py`、`pipeline_inpaint.py`，按
     Alpha 反解 → 平坦背景 Telea → IOPaint/LaMa 顺序降级。
  3. `pipeline/service.py` 保留豆包定点识别和擦除后复核/升级重擦，仅替换首次
     擦除的掩码与内核算路；`legacy` 仍可一键回退旧掩码与裸 LaMa。
  4. 设置弹窗与 XML 新增 `watermark_pipeline`、`ss_mask_strategy`、
     `ss_alpha_recovery`、`ss_fast_inpaint`、`ss_mask_refine` 开关。
- 涉及模块：pipeline/config.py、pipeline/models.py、pipeline/service.py、
  ui/state.py、ui/debug_dialog.py、vendors/watermark_remove/services/、
  Config/settings.config、tests/test_hybrid_pipeline.py、README.md、
  docs/watermark_removal_flow.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-29

## v0.1.16.27
- 当前本地 tag：v0.1.16.27
- 修改内容：修复成功文章自动重命名后未能即时从待发布列表移除的问题。
  1. 待发布列表先按原始无编号路径建行，流水线处理时才自动添加 `NNN-` 前缀；
     成功回调路径与列表行不一致，导致单行删除失配。
  2. 删除时先按完整绝对路径精确匹配，未命中再按“父目录 + 去掉自动编号的文件名
     + 扩展名”匹配，确保只删除同一目录、同一格式的对应文章。
  3. 新增自动编号重命名场景的回归测试；失败篇及手动编号（如 `88-`）行为不变。
- 涉及模块：ui/main_window.py、tests/test_pending_row_renamed.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.26
- 当前本地 tag：v0.1.16.26
- 修改内容：为 `original_http` 增加图片 URL 质量门槛。
  1. 当某个图片 ID 只捕获到 `cthumb_lwm3`、`ds_wm` 等低清缩略图时，
     不再直接把它当作最佳 URL，而是输出明确的 `[质量门槛]原图Http` 运行日志，
     并继续滚动/收集最多 15 秒，等待 `cgen`、`i_pre` 或无 `~tplv-` 原图等合格候选。
  2. 下载前再执行一次硬性质量过滤：混合批次跳过低清图并继续下载其余图片；
     全部候选均为低清时输出 `[错误]` 并拒绝下载，避免拇指图进入去水印与合并。
  3. 新增等待成功、等待超时和下载层拒绝低清候选的回归测试。
- 涉及模块：vendors/doubao_bot/models/config.py、image_wait.py、automation.py、
  tests/test_wait_scan_optim.py、tests/test_download_fix.py、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.25
- 当前本地 tag：v0.1.16.25
- 修改内容：修复豆包分批返回多图时，`original_http` 只下载首张的问题。
  1. 配图流水线在提交前把点位数量注入 `expected_images`；已知预期但尚未集齐时，
     首图后的 3 秒稳定期不再提前结束收集，至少继续观察 15 秒。
  2. `_wait_for_new_image_urls()` 仍保留总超时与部分收集宽限兜底；预期张数未知的
     普通单文档模式保持原有 3 秒稳定退出行为。
  3. `DoubaoImageBot.run()` 将 `expected_images` 透传到等图阶段，`original_http`
     下载的最佳 URL 列表因此包含同一轮分批返回的全部图片。
- 涉及模块：pipeline/service.py、vendors/doubao_bot/models/config.py、
  vendors/doubao_bot/models/image_wait.py、vendors/doubao_bot/models/automation.py、
  tests/test_wait_scan_optim.py、tests/test_plan_pipeline.py、tests/test_conversation_select.py、
  docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.24
- 当前本地 tag：v0.1.16.24
- 修改内容：修复长对话 DOM 虚拟化导致豆包已出图却超时并重复提交。
  1. 空等超时抛错前先信任本轮网络响应并执行 DOM 兜底；只要能恢复图片就继续
     正常去重、下载与收尾，避免同一提示词二次生成。
  2. 新图 URL 的 `rcl` 明确晚于本轮基线时，不再因被虚拟化 DOM 误列入历史
     节点而过滤掉。
  3. 已抓到本轮图片后，若消息节点总数未增长，完成信号允许回退扫描最近 3 条
     消息，兼容豆包虚拟化列表。
  4. 新增虚拟化历史过滤、空等超时恢复和完成信号限时回退回归测试。
- 涉及模块：vendors/doubao_bot/models/image_wait.py、tests/test_wait_scan_optim.py、
  docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.23
- 当前本地 tag：v0.1.16.23
- 修改内容：`original_http` 模式改为直接 HTTP 下载每张图片的最佳 URL。
  1. 按图片 ID 择优：无 `~tplv-` 的原图 URL 优先，其次为 `i_pre` 等高清处理图。
  2. 不再调用 `to_original_url()` 还原地址，避免签名绑定处理路径导致 403。
  3. 不再在下载失败后转「下载原图」按钮方案；失败直接记录并继续下一篇。
  4. 运行日志输出原图Http模式实际请求的“最佳 URL”。
- 涉及模块：vendors/doubao_bot/models/automation.py、download_http.py、config.py、
  tests/test_download_fix.py、pipeline/config.py、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.22
- 当前本地 tag：v0.1.16.22
- 修改内容：去掉主界面进度条后面的状态文字 Label。
  1. 移除 `ui/main_window.py` 中按钮行右侧的 `status_label`。
  2. 进度条改为占满按钮行右侧剩余空间，界面不再显示“就绪/运行中/完成”等同排文字。
- 涉及模块：ui/main_window.py、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.21
- 当前本地 tag：v0.1.16.21
- 修改内容：浏览图等待超时时，把实际选中的最佳 URL 写入运行日志。
  1. 运行日志按图片逐条输出“最佳 URL {实际下载地址}”，方便直接核对本次下载目标。
  2. 详细日志继续输出图片 ID、质量等级和仅供诊断的“还原原图URL”；
     原图还原地址不写入运行日志，避免与实际浏览图下载地址混淆。
  3. 新增运行日志与详细日志分层回归断言。
- 涉及模块：vendors/doubao_bot/models/image_wait.py、tests/test_wait_scan_optim.py、
  docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.20
- 当前本地 tag：v0.1.16.20
- 修改内容：浏览图高清预览等待超时时，把实际选中的最佳 URL 写入详细日志。
  1. 按图片 ID 输出“最佳URL”、质量等级和候选模板归类；同一图片存在多个 URL 时
     仍由 `_pick_best_url()` 选择最高质量项。
  2. 额外输出去掉 `~tplv-` 后的“还原原图URL”，并标明该地址仅供诊断、签名绑定
     处理路径，直接请求可能 403，避免与浏览图实际下载地址混淆。
  3. 新增回归测试，确认超时日志包含实际最佳 URL，且不会误写较早收集到的低清 URL。
- 涉及模块：vendors/doubao_bot/models/image_wait.py、tests/test_wait_scan_optim.py、
  docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.19
- 当前本地 tag：v0.1.16.19
- 修改内容：修复长对话历史消息 DOM 虚拟化导致的提示词提交误判。
  1. 豆包长对话发送新消息后，历史消息节点可能被虚拟化，节点总数会从 180 降至 73；
     旧逻辑把这误判为“消息节点未增加”，即使豆包已收到提示词并完成生图也抛错。
  2. 提交确认改为“消息节点增加，或严格读取确认输入框已真实清空”二者任一成立即成功；
     输入框 detached 仍返回失败，不会把元素失效误当成清空。
  3. 补充消息数下降、输入框 detached、输入框仍有内容三类回归测试。
- 涉及模块：vendors/doubao_bot/models/prompt_writer.py、tests/test_submit_verification.py、
  docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-28

## v0.1.16.18
- 当前本地 tag：v0.1.16.18
- 修改内容：修复豆包输入框 DOM 重渲染导致的提交失败，并阻止多个任务共用同一 profile。
  1. 新增 `ProfileLock`：浏览器 `start()` 对 `user_data_dir` 做跨进程文件锁，第二个任务
     直接报“登录目录正在被另一个任务使用”；正常关闭、启动失败和异常退出都会释放锁。
  2. 残留浏览器清理先探测 profile 锁；有任务运行时不执行 PowerShell 强杀，避免误杀正在使用的 Chromium。
  3. 提示词提交遇到输入框 detached 时重新 `_find_input()` 并重试；点击超时缩短为 5 秒。
  4. 回车后比较消息节点基线，必须确认新增用户消息；未确认时自动尝试发送按钮，仍失败则抛错
     并交上层重试，不再把“输入框已清空”误当成提交成功。
- 涉及模块：vendors/doubao_bot/models/profile_lock.py、browser.py、prompt_writer.py、image_wait.py、
  config.py、automation.py、pipeline/cleanup.py、pipeline/service.py、tests/test_submit_verification.py、
  README.md、docs/doubao_generation_flow.md
- 时间：2026-09-28

## v0.1.16.16
- 当前本地 tag：v0.1.16.16
- 修改内容：`Config/settings.config` 按设置弹窗分组重排，并保证写入值与弹窗当前显示值一致。
  1. 设置弹窗六个 LabelFrame 对应 XML 的 `group`：豆包生成、去水印、合并输出、批量文档生成、调试与登录、版权申明。
     主界面路径/图片要求与自动保存尺寸另列分组，内部运行态和已移除的兼容字段不再写入。
  2. 保存时只写入与设置界面双向同步的键，值直接取共享 Tk 变量的当前值；回归测试逐项校验保存值与弹窗显示值。
  3. XML 根节点记录 `legacy_json_migrated`，旧 JSON 不再在后续启动覆盖项目配置；现有 browse 模式、路径、版权和列宽值均保留。
- 涉及模块：pipeline/config.py、Config/settings.config、tests/test_settings_config.py、README.md、docs/doubao_generation_flow.md
- 时间：2026-09-28

## v0.1.16.15
- 当前本地 tag：v0.1.16.15
- 修改内容：修复 browse 模式误下原图，恢复设置弹窗操作按钮，并把全部设置迁移为项目 XML 配置。
  1. `browse` 只接受带 `~tplv-` 的页面浏览图 URL；等待、收尾与下载入口均过滤原图，
     没有浏览图时拒绝下载并记录错误，避免原图混入浏览图模式。
  2. 设置弹窗底部恢复「保存 / 取消」；保存显式落盘后关闭，取消恢复打开弹窗前的设置，
     直接关闭窗口等同于取消。
  3. 全部设置写入项目 `Config/settings.config`（UTF-8 XML），每项都有中文注释与可输入值说明；
     旧 `~/.doubao_bot/pipeline_settings.json` 首次加载时自动合并迁移。
  4. 手工编辑 XML 发生类型错误时回落到该项默认值，设置界面仍可正常启动。
- 涉及模块：vendors/doubao_bot/models/download_browse.py、image_utils.py、image_wait.py、
  pipeline/config.py、ui/debug_dialog.py、ui/state.py、Config/settings.config、tests、README.md、docs
- 时间：2026-09-28

## v0.1.16.14
- 当前本地 tag：v0.1.16.14
- 修改内容：修复新建对话已下载图片后，固定标题误写入豆包聊天输入栏的问题。
  1. 重命名快捷键由 `Ctrl+Alt+R` 改为 `Ctrl+Shift+R`，使用豆包原生重命名弹窗。
  2. `_RENAME_INPUT_JS` 仅接受可见 dialog / modal 内部的 `input` 或
     `contenteditable`，并主动聚焦该输入框；聊天输入栏不再作为候选。
  3. 未检测到弹窗内输入框时直接返回失败，不向当前页面输入任何标题文本。
- 涉及模块：vendors/doubao_bot/models/conversation.py、pipeline/service.py、
  tests/test_conversation_select.py、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-27

## v0.1.16.13
- 当前本地 tag：v0.1.16.13
- 修改内容：重做豆包固定对话标题流程，彻底移除旧的「用户输入标题 + 账号标题记忆 + legacy 勾选项」语义。
  1. pipeline/accounts.py：新增 `login_nickname()`，只接受有效 `display` 登录昵称；
     `js_error` 等占位值按空昵称处理。展示名 `spec_label()` 仍按昵称 → 配置名 → ID 回落。
  2. pipeline/service.py：账号开启「固定对话标题」时，仅在前 5 个对话中精确匹配
     `[图片生成]{登录账号昵称}`；未命中或未开启时按第一个对话 / 自动新建流程。
     本次实际新建对话且图片成功后，在去水印前调用 `rename_current_conversation()`
     固定同名标题；失败或昵称无效只输出 `[错误]` 日志，不重试、不阻塞后续文章。
  3. vendors/doubao_bot：`RunResult` 新增 `created_conversation`；`run()` 开始时清除旧
     新建标记，`_select_conversation()` 不再允许「当前标题等于目标」绕过前 5 个匹配。
  4. UI：删除主界面「豆包对话标题」输入区和设置弹窗 legacy 固定标题勾选项；
     账号列表「固定对话标题」列及点击切换逻辑保留。
  5. 兼容：`PipelineConfig.conversation_title` / `rename_conversation_on_done` 与
     `PipelineService(on_conversation_title=...)` 保留为占位，旧 settings / 标题记忆文件不再读取。
- 涉及模块：pipeline/accounts.py、pipeline/models.py、pipeline/service.py、
  vendors/doubao_bot/models/automation.py、vendors/doubao_bot/models/conversation.py、
  vendors/doubao_bot/models/errors.py、ui/main_window.py、ui/debug_dialog.py、ui/state.py、
  tests、README.md、docs/doubao_generation_flow.md
- 时间：2026-09-27

## v0.1.16.12

- 当前本地 tag：v0.1.16.12
- 修改内容：豆包账号列表新增账号级「固定对话标题」列。
  1. 列位置在「默认账号」后；值只有「是 / 否」，新账号默认「否」，单击单元格
     即在两值间切换，并立即持久化到 accounts.json（`fixed_conversation_title`）。
     旧版 6 列列宽自动迁移为 7 列，不改动用户已调整的其它列宽。
  2. pipeline/accounts.py：账号规范新增 `fixed_conversation_title`；旧注册表缺字段
     自动按 False 兼容；`upsert_account()` 支持显式切换。
  3. pipeline/service.py：多账号按当前账号自己的值判断；「是」调用
     `rename_current_conversation()`，「否」接受豆包自动标题并写回账号记忆，
     避免后续文档重复新建对话。未配置账号的 legacy 模式继续使用原全局开关。
  4. ui/debug_dialog.py / ui/state.py：账号列表 7 列、单击切换、列宽迁移与持久化；
     原「是否固定对话标题」勾选项保留为 legacy 兼容项并更新文案。
- 涉及模块：pipeline/accounts.py、pipeline/service.py、pipeline/models.py、
  ui/debug_dialog.py、ui/state.py、tests/test_account_list.py、tests/test_accounts.py、
  README.md、docs/doubao_generation_flow.md
- 时间：2026-09-27

## v0.1.14.23

- 当前本地 tag：v0.1.14.23
- 修改内容：S2 架构优化 —— 新建 docs/ARCHITECTURE.md（三段式 pipeline / ui / vendors 职责边界、数据流、扩展指南、模块文件头规范）。
- 涉及模块：docs
- 时间：2026-09-18

## v0.1.14.22
账号「每日额度 / 当日禁用」机制整体移除（用户从未提出该设计要求）。
- 移除 accounts.py：`ACCOUNT_DISABLE_AFTER_FAILURES`、`ACCOUNT_RISK_HINTS`、
  `risk_hint()`、`DEFAULT_LIMITS`、`_roll_day()`、`allow_start()`、
  `mark_disabled()`；`record_done` 简化为仅成功时累加 total；
  `rotation_pick` 重写为纯环形轮换（无健康检查），轮换计数仅针对本次生成，
  `reset_rotation` 归零；加载旧 accounts.json 时自动剔除 legacy
  `health` / `limits` 字段。
- 移除 service.py：run() 主循环的 `allow_start` 检查、
  `skipped_for_account` 计数、`risk_hint` / `mark_disabled` 调用、
  `account_exhausted` 置位块；所有账号始终可用，点击「开始生成」
  不再被「本轮 1 篇全部因账号额度/禁用被跳过」拦截。
- 移除 models.py：`PipelineResult.account_exhausted` 字段。
- 移除 main_window.py：`_skip_auto_start_once` 一次性标志、
  `_resume_after_pipeline` 的 account_exhausted 分支，恢复为
  完成后无条件重挂定时器链 + 立即补扫。
- accounts_cli.py：list/status 不再显示 health/limits，移除 `--daily` 参数。
- 测试：删除额度/禁用相关过时用例（TestLimits、TestAccountSuspendedAutoStart、
  account_exhausted 轮询用例等），新增「旧版 health/limits 字段加载即剔除」
  迁移测试与「配额满切换备选账号（无健康检查）」轮换测试；
  test_pending_articles.py 统计列断言索引修正（v0.1.14.16 插入状态列后移位）。
  全量 444 通过（唯一 error 为 Tkinter 环境偶发问题，单跑通过，与改动无关）。

## v0.1.14.21
账号耗尽暂停机制改为只对当次生成生效，之后自动恢复。
- 原机制：流水线返回 account_exhausted 后，UI 记录当日日期（
  `_account_suspended_date`），同一天内定时器轮询全部静默跳过，
  直到跨天或用户手动点击「开始生成」才解除。
- 新机制（v0.1.14.21）：改为一次性标志 `_skip_auto_start_once`——
  账号耗尽轮结束后仅跳过「立即补扫 + 下一个轮询 tick」这一次扫描，
  之后的轮询恢复正常自动开始；手动「开始生成」不受任何限制。
  （[main_window.py:407-410](file:///e:/Codex/DocGenStudio/ui/main_window.py#L407-L410)，
  [main_window.py:879-884](file:///e:/Codex/DocGenStudio/ui/main_window.py#L879-L884)）
- 保留一次性跳过的目的：防止耗尽轮结束后立即原地重扫形成无间隔死循环；
  正常轮询间隔（60 秒）成为两次尝试之间的最小间隔。
- 日志文案同步更新：「本轮不再补扫；下次轮询将自动重试，手动「开始生成」不受限制。」
- 测试：test_directory_poller.py 相应更新（3 个新用例 + 2 处标志替换），46 通过。

## v0.1.14.20
豆包内容拒绝不重试，立即标记 doubao_failed 并跳到下一篇；添加状态写入诊断日志。
- 问题 1：`_generate_by_plan` / `_generate_retry` 遇到 DoubaoRefusedError 时
  仍按通用异常重试，导致同一篇文章被反复尝试（用户误以为是「下一篇还是当前文档」）。
- 修复：在两个生成方法的重试循环中，`except DoubaoRefusedError` 单独捕获并
  立即 `raise`，不进入重试
  （[service.py:1012-1015](file:///e:/Codex/DocGenStudio/pipeline/service.py#L1012-L1015)，
  [service.py:1238-1241](file:///e:/Codex/DocGenStudio/pipeline/service.py#L1238-L1241)）。
- 问题 2：状态未写入可能因路径 key 不匹配或异常被吞导致，用户无法定位。
- 修复：`_run_one` / `_run_one_plan` 的 finally 块添加诊断日志
  （[service.py:835-843](file:///e:/Codex/DocGenStudio/pipeline/service.py#L835-L843)，
  [service.py:936-944](file:///e:/Codex/DocGenStudio/pipeline/service.py#L936-L944)）：
  成功标记时输出 `[状态] xxx | 已标记为「豆包处理失败」（store_key=...）`，
  异常时输出 `[状态] xxx | 写入 store 失败：...`。

## v0.1.14.19
修复配图模式下豆包拒绝后文章状态未更新为「豆包处理失败」的问题。
- 根因：`_generate_by_plan` 的重试循环用 `except Exception` 捕获所有异常
  （含 `DoubaoRefusedError`）并存入 `last_exc`，重试结束后统一抛出
  `RuntimeError("豆包未生成任何图片")`，导致外层 `_run_one_plan` 的
  `except DoubaoRefusedError` 无法命中，`is_refused` 未被设置，
  `set_status(doubao_failed)` 不执行。
- 修复（[service.py:1028-1035](file:///e:/Codex/DocGenStudio/pipeline/service.py#L1028-L1035)）：
  重试结束后若 `last_exc` 是 `DoubaoRefusedError`，原样抛出；
  否则保持原 `RuntimeError` 行为。
- 普通模式 `_generate_retry` 最后一次异常已 `raise` 原样抛出，无需修改。
- 测试：389 通过（唯一 error 为 Tkinter 环境问题，与改动无关）。

## v0.1.14.18
run() 主循环添加动态跳过检查，确保同一次运行中被标记为 doubao_failed 的文章不被重复处理。
- 之前只在 `_collect_documents` 阶段（批量开始前）过滤，但 run() 主循环中 docs 列表
  已固定。如果文章 A 在本次运行中被标记为失败，且后续因路径 key 不匹配等原因未被
  `_filter_failed_docs` 过滤，仍会被重复处理。
- 新增 `_is_doc_doubao_failed(doc)` 方法
  （[service.py:684-701](file:///e:/Codex/DocGenStudio/pipeline/service.py#L684-L701)），
  在 run() 主循环每篇处理前调用，检查该文章是否已在 store 中标记为 doubao_failed。
- run() 主循环（[service.py:482-489](file:///e:/Codex/DocGenStudio/pipeline/service.py#L482-L489)）：
  命中时输出 `[跳过] xxx | 该文章已标记为「豆包处理失败」，不再重复处理`，continue 跳过。
- 双重保障：`_filter_failed_docs` 预过滤 + `_is_doc_doubao_failed` 运行时动态检查。
- 测试：12 通过。

## v0.1.14.17
修复 store 路径 key 不匹配导致 UI 读不到状态的问题。
- v0.1.14.16 中 service.py 写 store 用 `str(doc)`，UI 读 store 用 `str(p.resolve())`，
  当路径含 `..` 或服务启动前 UI 先刷新时 key 不一致。
- 统一为 `str(Path(path).resolve())`：
  - service.py `_run_one` / `_run_one_plan` 的 incr/set_status 调用
  - service.py `_filter_failed_docs` 的路径比较
  - UI `_refresh_pending_articles` 已在用 `str(p.resolve())`，无需改动

## v0.1.14.16
豆包错误检测成功后，修复同一篇文章被重复处理 + 待发布列表增加状态列。
- 问题 1：豆包返回错误被成功识别并跳过，但下次定时器触发时同一篇文章又被
  重新收集处理。根因：`_collect_documents` 无过滤机制，已拒绝的文章仍被收录。
  - 修复 1a：`pending_articles_store` 新增 `status` 列 + `set_status` /
    `get_failed_paths` / `get_all_with_status` 函数
    （[pending_articles_store.py:30-156](file:///e:/Codex/DocGenStudio/pipeline/pending_articles_store.py#L30-L156)）。
    含旧表 ALTER TABLE 迁移，自动为已有数据库添加 status 列。
  - 修复 1b：`_run_one` / `_run_one_plan` 的 finally 块在 `DoubaoRefusedError`
    时调用 `set_status(path, "doubao_failed")`，成功时调用 `set_status(path, "published")`
    （[service.py:773-784](file:///e:/Codex/DocGenStudio/pipeline/service.py#L773-L784)，
    [service.py:872-884](file:///e:/Codex/DocGenStudio/pipeline/service.py#L872-L884)）。
  - 修复 1c：`_collect_documents` 批量模式返回前调用 `_filter_failed_docs`
    过滤掉 `doubao_failed` 文章
    （[service.py:618-619](file:///e:/Codex/DocGenStudio/pipeline/service.py#L618-L619)，
    [service.py:653-674](file:///e:/Codex/DocGenStudio/pipeline/service.py#L653-L674)）。
    单文档模式不过滤（用户显式选了该文件）。
- 问题 2：待发布文章列表增加「状态」列。
  - 列位置：手机号列后，已生成数列前
    （[main_window.py:190-202](file:///e:/Codex/DocGenStudio/ui/main_window.py#L190-L202)）。
  - 三种状态：待发布（默认）、已发布（生成成功）、豆包处理失败（内容拒绝）。
  - `_refresh_pending_articles` 改用 `get_all_with_status` 读取状态
    （[main_window.py:690-744](file:///e:/Codex/DocGenStudio/ui/main_window.py#L690-L744)）。
- 问题 3：豆包处理失败的文章不再被处理。
  - `_filter_failed_docs` 在 `_collect_documents` 返回前过滤，确保批量扫描
    和定时器轮询都不会重新收录已拒绝的文章。
- 测试：390 通过（唯一 error 为 Tkinter 环境问题，与改动无关）。

## v0.1.14.15
修复豆包错误检测仍然失效 + 强制终止按钮无反馈两个问题。
- 问题 1：豆包返回「抱歉，由于模型可能带来准确性问题」后，v0.1.14.13 的诊断日志
  仅在调试模式输出（`_log_debug`），用户非调试模式看不到任何诊断信息，且
  `_DETECT_ERROR_JS` 可能因 DOM 结构变化漏读错误话术。
  - 修复 1a：将「抱歉，由于模型可能带来准确性问题…」和「由于模型可能带来准确性问题」
    加入 `DOUBAO_ERROR_TEXTS` 内置规则
    （[config.py:407-409](file:///e:/Codex/DocGenStudio/vendors/doubao_bot/models/config.py#L407-L409)），
    即使外部 `doubao_errors.log` 读取失败也能命中。
  - 修复 1b：`detect_error_message` 诊断日志从 `_log_debug` 改为 `_log`
    （主日志，非调试模式也可见），格式不变
    （[image_wait.py:786-821](file:///e:/Codex/DocGenStudio/vendors/doubao_bot/models/image_wait.py#L786-L821)）。
  - 修复 1c：`detect_error_message` 新增全页文本兜底扫描——`_DETECT_ERROR_JS`
    未命中时，再读 `document.body.innerText` 全文做 substring 匹配，覆盖
    iframe / shadow DOM / 非 message 节点中的错误话术。
  - 修复 1d：`page.evaluate` 抛 `PlaywrightError` 时输出主日志（非静默返回 None），
    便于定位页面崩溃 / 导航中断等导致检测失效的根因。
- 问题 2：用户点「强制终止」按钮无任何反馈。
  - 修复 2a：`_stop` 在 `is_busy=False` 或 `_service=None` 时输出日志反馈
    （[main_window.py:884-893](file:///e:/Codex/DocGenStudio/ui/main_window.py#L884-L893)），
    用户不再面对「点了没反应」的体验。
  - 修复 2b：`run()` 中 `page.wait_for_timeout(POST_SUBMIT_WAIT_MS)` 改为
    `self._pause(page, POST_SUBMIT_WAIT_MS)`，使 300ms 等待可被取消打断
    （[automation.py:421-425](file:///e:/Codex/DocGenStudio/vendors/doubao_bot/models/automation.py#L421-L425)）。
  - 修复 2c：`run()` 在 `_select_conversation` 与 `submit_prompt` 之间补
    `_check_cancel()`，取消请求能在对话切换后、提交前即时响应。
- 测试：[tests/test_error_detection.py](file:///e:/Codex/DocGenStudio/tests/test_error_detection.py)
  3 例适配新行为（诊断日志改查 `info_logs`；内置规则匹配顺序调整）。
  全量 389 通过（唯一 error 为 Tkinter 环境问题，与改动无关）。

## v0.1.14.14
修复豆包内容拒绝被误计为账号失败 → 连续 6 次触发「当日所有账号额度耗尽/禁用」的问题。
- 根因：豆包返回「由于模型可能带来准确性问题」类拒绝话术时，v0.1.14.13 修复
  前 `_raise_if_refused` 未检测到 → 当作正常回复处理 → 无图 → RuntimeError →
  `item.ok=False` → `record_done(ok=False)` → `failures += 1`。连续 6 次拒绝
  后触发 `ACCOUNT_DISABLE_AFTER_FAILURES = 6` 的「连续失败 6 篇当日暂停」
  机制 → 所有账号被禁用 → `account_exhausted=True` → UI 输出
  「当日所有账号额度耗尽/禁用，本轮不再补扫」。用户并未配置此限制。
- 修复：DoubaoRefusedError 是豆包内容拒绝（非账号问题），不应计入失败计数。
  1. `pipeline/models.py:128`：`ItemResult` 新增 `is_refused: bool = False`。
  2. `pipeline/service.py:30`：导入 `DoubaoRefusedError`。
  3. `pipeline/service.py:752-756, 840-844`：`_run_one` / `_run_one_plan`
     新增 `except DoubaoRefusedError as exc` 单独捕获，设置
     `item.is_refused=True`，日志「[跳过] xxx | 豆包内容拒绝，继续下一篇」。
  4. `pipeline/service.py:508-517`：主循环 `record_done` 与
     `_log_rotation_after_doc` 传入 `ok_for_health = bool(item.ok) or
     item.is_refused`（拒绝时 ok=True，不增 failures、不占配额）。
  5. `pipeline/service.py:522-523`：风控/登录失效检测加
     `not item.is_refused` 守卫，避免拒绝误触发 mark_disabled。
- 测试：[tests/test_refused_not_counted.py](file:///e:/Codex/DocGenStudio/tests/test_refused_not_counted.py)
  5 例（is_refused 字段存在/可设；拒绝传 ok=True 不增 failures；连续 6 次
  拒绝不禁用账号；真失败仍计 failures）。
- 回归：全量 463 通过（不含本文件慢测试）；本文件 5/5 通过。

## v0.1.14.13
修复豆包错误话术未被检测到 → 未跳过下一篇的问题（用户报告「由于模型可能带来准确性问题」未触发）。
- 任务 1：`detect_error_message` 命中失败时输出诊断日志。
  - [image_wait.py:790-800](file:///e:/Codex/DocGenStudio/vendors/doubao_bot/models/image_wait.py#L790-L800)：
    `page.evaluate(_DETECT_ERROR_JS)` 返回的 text 非空但 `_match_error_text`
    返回 None 时，把 text 尾部 300 字符（去掉换行）输出到 `_log_debug`，
    格式「[错误检测] 页面文本尾部 300 字符（未命中已知规则）：xxx」。
  - 用户运行后可在详细日志文件看到豆包实际渲染到 DOM 的页面文本尾部，
    据此判断是错误话术未渲染、还是 `_DETECT_ERROR_JS` 读不到、
    还是 doubao_errors.log 里的规则文本与豆包原文有差异。
- 任务 2：stall_timeout 早退前补调 `_raise_if_refused`。
  - [image_wait.py:249-259](file:///e:/Codex/DocGenStudio/vendors/doubao_bot/models/image_wait.py#L249-L259)：
    `_wait_for_new_image_urls` 在 stall_timeout 触发抛 TimeoutError 前，
    先调一次 `_raise_if_refused`。豆包可能在 stall 期间才渲染完错误消息
    （如「由于模型可能带来准确性问题」），此时抛 `DoubaoRefusedError`
    让上层跳到下一篇，比 TimeoutError 触发自动重试更有意义。
- 任务 3：`wait_and_download` 返回空前补调 `_raise_if_refused`。
  - [automation.py:197-201](file:///e:/Codex/DocGenStudio/vendors/doubao_bot/models/automation.py#L197-L201)：
    `_wait_for_new_image_urls` 末尾已调一次 `_raise_if_refused`，但返回
    空 list 后、`wait_and_download` 返回 [] 前再补一次。兜底覆盖
    「等待循环末尾错误消息未渲染、此处才渲染完」的边界场景。
- 测试：[tests/test_error_detection.py](file:///e:/Codex/DocGenStudio/tests/test_error_detection.py)
  7 例（detect_error_message 4 例：空文本无诊断、未命中输出尾部、命中不诊断、
  去换行；stall_timeout 抛 DoubaoRefusedError；wait_and_download 返回空前
  调用 _raise_if_refused、DoubaoRefusedError 传播）。
- 回归：全量 463 通过，0 失败。

## v0.1.14.12
待发布文章列表列宽持久化 + 默认模式改为 plan_batch。
- 任务 1：待发布文章列表列宽持久化。
  - `_build_pending_articles_section` 末尾调用 `_restore_pending_tree_widths`
    从 SETTINGS_FILE 读 `pending_tree_col_widths`（dict{col_id: width}），
    按保存宽度覆盖默认；绑定 `<ButtonRelease-1>` →
    `_on_pending_tree_col_resized`：用户拖拽列边界后遍历所有列
    `tree.column(cid, "width")` 取当前宽度写回 SETTINGS_FILE。
  - 保存的列宽 dict 含全部 7 列（title/size/images/phone/success/fail/last）。
- 任务 2：选择目录持久化——已在 v0.1.11+ 由 AppState._PERSIST_KEYS 实现
  （`input_dir` / `plan_input_dir` / `doc_path` 三个变量都已在持久化清单内，
  trace_add 即时写入 SETTINGS_FILE，下次启动自动恢复）。本次仅补回归测试
  `test_directory_paths_persist_across_runs` 显式验证跨次启动恢复行为。
- 任务 3：默认模式由 `single` 改为 `plan_batch`，对齐定时器自动扫描配图
  说明文档的常用工作流；用户切换模式后由 _PERSIST_KEYS 覆盖默认值。
  - `ui/state.py:67-69`：`settings.get("mode", "plan_batch")`。
- 测试：
  - `test_pending_articles.py` 新增 TestPendingTreeWidthsPersistence 3 例
    （恢复应用保存宽度、无保存 noop、拖拽保存）+ TestDefaultModeIsPlanBatch
    3 例（默认 plan_batch、用户选择覆盖默认、目录路径跨次持久化）。
  - `test_pipeline.py::TestConfigBuild::test_defaults_from_ui_state`：
    补 monkeypatch SETTINGS_FILE 隔离，断言默认 mode 改为 plan_batch。
  - 回归：专项 38/38 通过；全量 455 通过（1 个 Tcl 环境抖动单独重跑通过）。

## v0.1.14.11
待发布文章列表细化 + 「4. 启动和设置」栏高度可调并持久化。
- 任务 1：标题去掉「_封面配图提示词」/「__封面配图提示词」后缀。
  `_refresh_pending_articles` 计算 title 时按双下划线优先匹配剥离，
  避免列表里出现长后缀占空间。
- 任务 2：待生成图片数算法分两路。
  - 配图说明文档（`*_封面配图提示词.md`）：调用 `plan_reader.load_plan`
    解析，返回 `len(plan.points)`（封面 1 + 配图 N，与流水线生成
    图片数一致）；
  - 普通 .md/.markdown：仍按 `![alt](url)` 引用计数；
  - .docx 或读取失败：-1（UI 显示「—」）；
  - 新增 `pipeline/pending_articles_store.count_pending_images(path)`
    封装上述分流逻辑，解析失败回退到引用计数。
- 任务 3：主窗口用 `ttk.PanedWindow(orient="vertical")` 包裹上下两区。
  - 上半 pane：0/1/2/3 四个 LabelFrame（生成模式、对话标题、图片要求、
    输入文档+待发布列表）；
  - 下半 pane：「4. 启动和设置」栏（按钮行+进度条+运行日志）；
  - 用户拖拽 sash 调节两区高度，松开鼠标时 `<ButtonRelease-1>` 触发
    `_on_paned_sash_released` 保存 `sashpos(0)` 到 `SETTINGS_FILE`
    的 `main_paned_sash_pos` 字段；
  - 启动后 `after(200, _restore_paned_sash)` 读回位置并用 `sashpos(0, pos)`
    恢复；位置超出现窗口高度时不应用，避免上半被挤没；
  - 持久化复用 `pipeline/config.load_settings/save_settings`。
- 测试：
  - `test_pending_articles.py` 新增 TestCountPendingImages 3 例（plan
    点位数、普通 md 回退、docx -1）；TestRefreshPendingArticles 新增
    title_strips_plan_suffix 与 plan_doc_images_count_via_load_plan；
    新增 TestPanedWindowSashPersistence 5 例（key 常量、无设置 noop、
    恢复应用位置、拖拽保存、超窗高不应用）。
  - 回归：专项 43/43 通过；全量 448 通过（2 个 Tcl 环境抖动单独重跑通过）。

## v0.1.14.10
新增「待发布文章列表」Treeview，常驻「3. 输入文档」栏下方。
- 背景：旧实现仅在选目录后把文档名打到日志，定时器轮询期间也无可见反馈。
  用户要求把目录下所有文章结构化展示，含历史生成统计。
- 列：文章标题 / 文章大小 / 待生成图片数（Markdown `![]()` 计数，.docx 显示
  「—」）/ 手机号(目录名称) / 已生成数 / 生成失败数 / 上次生成时间。
- 历史统计用 SQLite 持久化（`~/.doubao_bot/pending_articles.db`），跨多次
  流水线运行累计。
- 新增 `pipeline/pending_articles_store.py`：
  - 表 `articles(path PK, success, fail, last_ts)`；每次调用开关连接，
    无全局连接对象，避免多线程竞争；
  - API：`incr(path, ok, ts)`（upsert + 对应字段自增，失败仅日志不抛）、
    `get_all()`（返回 `{path:(s,f,t)}` 快照）、`clear()`；
  - `count_markdown_images(path)`：正则 `r"!\[[^\]]*\]\([^)]+\)"` 计数
    .md/.markdown，.docx 或读取失败返回 -1。
- `pipeline/service.py`：`_run_one` / `_run_one_plan` 的 finally 末尾
  调用 `incr(str(doc), ok, time.time())`（try/except 包裹，失败不阻断）。
- `ui/main_window.py`：
  - 新增 `_build_pending_articles_section`：在「3. 输入文档」栏下追加
    LabelFrame + ttk.Treeview（7 列 + 垂直滚动条，参考 debug_dialog 的
    Treeview 模式）；
  - 新增 `_refresh_pending_articles`：清空旧行 → 按当前模式收集文档
    （single=cfg.doc_path 1 篇；batch=discover_documents；
    plan_batch=_discover_plan_documents）→ 逐行计算列值并 insert；
    `tree` 取值用 `self.__dict__.get` 避免 MainWindow.__new__ 测试
    fixture 触发 Tk __getattr__ 递归；
  - 触发点 5 处：__init__ 末尾（after 300ms 等绘制完成）、_choose_dir
    末尾（plan_batch 与 batch 两条分支）、_sync_mode_view 末尾（模式
    切换）、_on_directory_poller_tick 的 finally（仅非暂停态）、
    _resume_after_pipeline 末尾（流水线结束更新已生成数/失败数/时间）。
- 新增 `tests/test_pending_articles_store.py`（14 例：incr 累计/失败不抛/
  clear 清空/count_markdown_images 各场景）。
- 新增 `tests/test_pending_articles.py`（20 例：_FakeTree 替代真 Tk
  widget 避免 __new__ 递归；single/batch/plan_batch 收集；行值正确；
  docx 显示「—」；根目录与子目录 phone 列；store 历史累计显示；刷新
  替换旧行；空 tree noop；_format_size 与 _phone_dir_name 单测）。
- 回归：专项 34/34 通过；全量 439 通过（0 失败）。

## v0.1.14.9
文章生成期间暂停轮询定时器，生成结束（成功/失败/终止）后重新起一个完整计时周期。
- 背景：旧实现在生成期间仍保留 60 秒 after 链（tick 仅靠 is_busy 空转），
  生成耗时被计入轮询计时；恢复后节奏漂移（可能立刻又到 tick）。用户要求：
  一旦开始生成，定时器开启时即暂停，生成完毕或失败后才继续计时。
- `ui/main_window.py`：
  - `__init__` 新增 `_poller_paused` 标志（区别于 `_poller_closed` 表示的
    用户手动关闭：暂停是临时挂起，closed 是用户意图关闭）；
  - 新增 `_suspend_poller_for_pipeline()`：定时器勾选时取消已挂 after、
    置 paused=True、输出「[定时器] 文章生成中，轮询已暂停，生成结束
    （成功/失败/终止）后自动恢复计时」；定时器本就关闭则 no-op；
  - `_start()` 在 `_set_busy(True)` 后立即调用暂停（含轮询自动触发路径）；
  - `_start_directory_poller()` 在 paused 时拒绝挂 after；
    `_on_directory_poller_tick()` 的 finally 在 paused 时不续挂——竞态兜底
    （tick 恰在暂停前一刻进入也不会让链复活）；
  - `_on_poller_toggle()`：生成进行中勾选定时器只记意图、不立即挂链，
    日志提示「文章生成结束后自动恢复」；进行中取消勾选仍立即停止；
  - `_resume_after_pipeline()`：先无条件清除 paused（即使用户生成期间关闭
    了定时器也要清，否则下次勾选会被残留 paused 挡住无法启动），再按
    poller_enabled 决定是否重挂完整周期 after + 立即补扫；恢复日志改为
    「流水线完成，继续轮询计时（重新起一个完整周期），每 60 秒轮询一次」。
  - 抽出 `_cancel_poller_after()` 复用 after_cancel 清理。
- `tests/test_directory_poller.py`：新增 TestPollerPauseDuringPipeline
  6 例（暂停取消 pending after 且不动 closed、定时器关闭时 no-op、暂停态
  start/tick 均不挂 after、resume 清标志并重挂、忙碌中勾选延迟启动）；
  TestResumeAfterPipeline 新增「关闭定时器结束也清 paused」用例。
- `tests/test_poller_toggle.py`：test_enable_calls_start 补 is_busy=False
  前置（MagicMock 真值会误入忙碌分支），新增忙碌中勾选不启动用例。
- `tests/test_poller_log.py`：fixture 补 `_poller_paused`。
- 回归：轮询相关 50/50 通过；全量 405 通过（0 失败）。

## v0.1.14.8
取消「连续生成 N 篇后强制休息 20 分钟」机制；轮换计数改为只针对本次生成、不累计历史。
- 背景：日志出现「[账号] 18611596317 连续任务已达休息条件，等待 717 秒
  休息后继续…」。该休息是应用自身的健康度机制（默认连续 4 篇 → 休息 1200
  秒），与豆包无关；且 quota=2 的轮换配额被该机制打断。用户要求：账号只在
  本次生成内按 quota 轮换（如 A 完成 2 篇即切 B 继续），不要强制等待。
- `pipeline/accounts.py`：
  - `DEFAULT_LIMITS` 移除 `consecutive` / `rest_seconds`，仅保留
    `{"daily": 1000}`；`default_account_spec()` 与 `_normalize_spec()` 的
    health 结构移除 `consecutive` / `rest_until`——旧 accounts.json 加载时
    自动剔除这两个键（`_normalize_spec` 按白名单重建，旧值不会回写）；
  - `allow_start()` 删除休息窗口分支与旧数据兼容分支，第三项返回值（等待
    秒数）恒为 `0.0`（保留三元组签名避免调用点改动）；不允许原因只剩
    「当日禁用」「今日额度已用完」；
  - `record_done()` 删除连续计数累加 / 达标设置 `rest_until` 逻辑，只保留
    今日用量、成功清零失败计数、总篇数 total、连续失败 6 篇当日禁用；
  - `_roll_day()` 跨天重置不再涉及 consecutive/rest_until；
  - `rotation_pick()` 删除 resting 列表与「全部休息取等待最短者」分支及
    相关说明；配额满账号的可用判断改为 `allow, reason, _wait`。
- `pipeline/service.py`：
  - `run()` 循环内删除 `wait > 0 → _sleep_breakable` 的休息等待分支及
    「连续任务已达休息条件」日志；
  - **轮换只计本次**：`run()` 在文档收集确认非空后（启用轮换且有账号时）
    先 `reset_rotation()` 归零，从第一个启用账号开始按各账号 quota 轮换
    （两账号 quota=2 → A、A、B、B、A、A…环形）；`finally` 中再次
    `reset_rotation()`（含失败/强制终止路径），注册表不残留历史游标；
  - `_log_account()` 删除 `_rotation_note` 中「休息」状态拼接。
- `pipeline/accounts_cli.py`：移除 `add --consecutive` / `add --rest`
  参数（再传入会报 unrecognized arguments，明确提示已移除）；列表删除
  「连续 x/y」列；`status` 删除「需等待 Ns / 休息中剩 N 秒」输出；模块
  docstring 更新轮换语义。
- 真实注册表 `~/.doubao_bot/accounts/accounts.json`：经 load/save 规范化，
  两账号 limits 仅剩 `daily:1000`，health 仅剩 day/used_today/failures/
  disabled/disabled_reason；历史轮换游标（cursor=18611596317, used=14）
  归零为 `{"cursor":"","used":0}`；两账号 quota 均为 2。
- `tests/test_accounts.py`：
  - 删除休息机制用例（test_consecutive_reaches_rest_window /
    test_failure_resets_consecutive / test_consecutive_resets_after_rest_window
    / test_legacy_full_consecutive_is_normalized）；
  - 新增 `test_many_successes_never_rest`（连做 20 篇 wait 恒 0、health 无
    旧键）、`test_legacy_rest_data_is_ignored`（rest_until 未来时间也不
    等待）、`test_failure_increments_failures`；
  - 轮换 3 个休息用例改写为旧 rest_until 数据不再生效（直接切换/继续使用/
    两账号都不等待）；normalize/roundtrip 用例断言旧键被剔除；
  - TestServiceRotation 新增 4 例：quota=2 本次 5 篇 → A A B B A；
  注册表残留 cursor=B/used=9 时本次仍从 A 开始；生成结束注册表轮换归零；
    连续两次 run 每次都从 A、used=0 开始。
- 文档：README.md「多账号」章节与 `docs/doubao_generation_flow.md` 轮换
  段落同步更新（本次生成语义、环形顺序、休息机制取消说明）。
- 回归：`test_accounts.py` 74/74 通过；全量 395 通过（2 例为本机 Tcl 初始化
  偶发抖动，单独重跑通过，与改动无关）。

## v0.1.14.7
图片下载明细日志改走详细日志通道，主窗口只保留开始/关键失败/完成汇总。
- 背景：`download_http.py` / `download_button.py` 此前所有下载过程日志
  （URL 明细、每张请求/重试/状态码、已保存 KB、URL 汇总等）都走
  `self._log`，直接灌进主窗口运行日志区，每篇下载几十行刷屏；用户
  要求把这些明细保留到详细日志文件即可，主窗口只看摘要。
- `vendors/doubao_bot/models/automation.py`：
  - `DoubaoImageBot.__init__` 新增 `log_verbose: Callable[[str], None] | None`
    参数与 `self._log_verbose` 属性；未注入时回落到 `self._log`，保持
    登录/登出等旧入口（其 `log` 即用户视角运行日志）的既有行为。
- `pipeline/service.py`：两处 `DoubaoImageBot(...)` 创建点均传
  `log_verbose=self._log_debug`，让明细落到 UI 的 `_log_debug` 通道
  （始终写 verbose 日志文件，仅在用户勾选「详细调试日志」时显示到
  主窗口）。
- `vendors/doubao_bot/models/download_http.py`：
  - 新增主窗口开始日志 `开始下载 N 张{mode_label} → {output_dir}`；
  - URL 明细列表 / 每张请求 URL / 回退/已保存 KB / 请求重试/HTTP 状态码 /
    下载结果汇总（URL 明细）等全部改走 `self._log_verbose`；
  - 关键警告仍保留 `self._log`：全局 attempt 预算耗尽、`[错误]原图http
    下载失败原因`、`[index] 第 N 张下载失败`、连续 429 早退、`[错误信息]
    下载图片大小错误`、`共 N 张图片下载失败`。
- `vendors/doubao_bot/models/download_button.py`：
  - 新增主窗口开始日志 `开始点击「下载原图」按钮下载 N 张 → {output_dir}`；
  - 点击/重试/定位/hover/拦截/已捕获下载文件等明细改走 `_log_verbose`；
  - 关键失败仍保留 `self._log`：按钮方案失败回退提示、`未获取到原图`、
    `原图请求下载失败`、`保存下载文件失败`、`下载原图失败（N 次尝试均
    未获取到文件）`、`[错误信息]下载图片大小错误`。
- `tests/test_download_fix.py`：`_Host` / `_OriginalHttpHost` /
  `_make_button_host` 三处最小宿主补 `_log_verbose = _log`（默认回落
  到 `_log`），避免明细日志调用 `AttributeError`；既有 8 例测试断言
  全部通过。
- 回归：`tests/` 全量 393 / 394 通过（1 例为 tk 环境偶发 init.tcl 抖动，
  单独重跑通过，与代码无关）。

## v0.1.14.6
修复「账号当日额度耗尽后应用不停喷跳过日志」与「accounts.json daily 被误设为 8」。
- 背景：用户设定 daily=1000，但 `accounts.json` 实际写入了 `daily:8`，
  导致 18611596317 / doubao_1 各跑到 8 篇就被 `allow_start` 拦下，整轮
  所有文档 `continue` 跳过；流水线"完成"后 `_resume_after_pipeline`
  立即 `_try_auto_start()` 又扫到同一批文档再次启动，60 秒一跳无限
  循环喷「[账号] 跳过 xxx：今日额度已用完（8 篇/天）」。
- `accounts.json`：两账号 `limits.daily` 8 -> 1000（与 `DEFAULT_LIMITS`
  对齐，恢复用户实际意图）。
- `pipeline/models.py`：`PipelineResult` 新增 `account_exhausted: bool`
  字段（默认 False）。
- `pipeline/service.py`：
  - 批量循环两个账号跳过分支（`_rotation_blocked_reason` 与
    `allow_start` 返回 not allow）累加 `skipped_for_account` 计数；
  - 循环结束后若 `not cancelled` 且 `len(items)==0` 且
    `skipped_for_account == total > 0`，置 `result.account_exhausted=True`
    并输出明确日志「暂停自动补扫；跨天或手动点击『开始生成』后恢复」。
- `ui/main_window.py`：
  - `__init__` 新增 `self._account_suspended_date: str = ""`；
  - `_worker` finally 改为 `lambda e=exhausted: self._resume_after_pipeline(e)`，
    把 service 端 `account_exhausted` 透传给 UI；
  - `_resume_after_pipeline(account_exhausted=False)`：True 时跳过立即
    补扫，把 `_account_suspended_date` 记为今日并输出提示日志；
  - `_try_auto_start` 入口先比较 `_account_suspended_date` 与今天：
    - 同日 → 直接 return（静默跳过，不再扫目录）；
    - 跨日 → 自动清空（让跨天后的第一次 tick 立即恢复）；
  - `_start` 入口在 busy 早返回之前清空 `_account_suspended_date`，
    用户手动点击「开始生成」即视为解除暂停态。
- `tests/test_directory_poller.py`：
  - `TestTryAutoStartBehavior._make_window` 与 `TestResumeAfterPipeline._make_window`
    补 `_account_suspended_date=""`，避免 tk `__getattr__` 递归；
  - `TestResumeAfterPipeline` 新增 2 例：account_exhausted 跳过补扫+
    标记暂停+输出日志 / 仍输出「[定时器] 继续…」日志；
  - 新增 `TestAccountSuspendedAutoStart`（3 例：当日暂停跳过 _start /
    跨日自动清空恢复 / 手动 _start 清空暂停态）。
- 回归：`test_directory_poller.py` 23 / 23 通过，`test_accounts.py` 与
  `test_poller_log.py` 81 / 81 通过。

## v0.1.14.5
流水线结束后定时器显式继续（成功 / 强制终止 / 异常三种结束路径均生效）。
- 背景：轮询链原本依赖 `after` 自续，完成后只靠下一周期 tick 继续，
  既无显式保证（忙碌期间 tick 意外丢失即永久停摆），也需等满 60 秒
  才能再扫目录。
- `ui/main_window.py`：
  - 新增 `_resume_after_pipeline()`：`_worker` 的 finally 统一改为
    `_after(self._resume_after_pipeline)`，在 Tk 主线程依次执行：
    1) `_set_busy(False)` 恢复按钮；
    2) 「启动定时器」仍勾选时重置 `_poller_closed=False` 并重新挂链
       （`_start_directory_poller` 幂等，不产生重复定时器）；
    3) 输出简单日志 `[定时器] 流水线完成，继续每 N 秒轮询一次…`；
    4) 立即 `_try_auto_start()` 补扫一次，新放入/未处理完的文档无需
       等满一个周期即被拾取（仍受批量模式/空目录/忙碌态约束）。
  - 用户在流水线运行期间手动取消勾选时不重启轮询、不补扫。
- `tests/test_directory_poller.py`：新增 `TestResumeAfterPipeline`
  （3 例：勾选时重挂+立即补扫+日志 / closed 丢失时恢复 / 运行中
  关闭定时器则不重启）。

## v0.1.14.4
左上锚点 rect 调整为 410x185（原 340x150：w +70、h +35）。
- `vendors/watermark_remove/config.py`：左上 `w 0.1194->0.1440`、
  `h 0.0938->0.1156`（2848x1600 换算 410x185，x=20/y=40 不变）；
  右扩探针绝对宽随之变为 485/525。
- `tests/test_doubao_engine.py`：像素断言 375x150 -> 410x185；探针宽度
  分界与掩码宽度断言同步（410 / 探针 485、525）。

## v0.1.14.3
修复豆包左上锚点水印漏识别（663-育儿补贴「有家长以为这笔钱已经『作废』」）。
- 根因（实测 2848x1600 原图，非裁剪出框）：水印笔画完整在锚点框内，但
  右侧紧邻暗红画面块干扰 RapidOCR 文本行分割，紧框把「生」误识成
  「性/胜」，6 级增强链全部读出 `A性成/A胜成`，漏擦。
- `vendors/watermark_remove/config.py`：
  - 左上锚点宽度 340px→375px（w 归一化 0.1194→0.1317，x/y/h 不变）；
  - 新增 `DOUBAO_ANCHOR_WIDE_CONTEXT=(75, 115)`：紧裁剪 1x 未独立命中
    时，右扩 75/115px 各做一次 1x OCR 探针。
- `vendors/watermark_remove/services/detector.py`：
  - `_region_ocr_chain` 第 1 级后追加横向扩宽探针，单次 OCR **独立命中**
    即判定（663 右扩探针读出 `A生成` 命中）；探针文本不并入跨级累积
    缓冲，避免倒序 `生成AI` 拼出伪 `AI生成` 子序列误擦；
  - 命中后返回的擦除框仍是锚点原宽（375），探针只用于识别、不扩大掩码；
  - 紧框 1x 已命中时跳过探针，常规图零额外开销；复核链同步受益。
- 语料回归（29 张）：27 张原命中全部保持，663 修复后 28 张命中，
  唯一未命中的 076 封面（两角均无水印特征）探针下依旧不命中，无误报；
  663 原图端到端首擦快速链复核 0 残留。
- `tests/test_doubao_engine.py`：锚点像素断言 340→375；新增
  `TestWideContextProbe`（3 例：探针救回误识/倒序探针不累积误报/
  首击即中跳过探针）。
- `tests/test_optim_m0_m8.py`：调用计数随探针更新（全链两锚点
  12→16；max_levels=3 两锚点 6→10；右下单锚点 3→5）。

## v0.1.14.2
【定时器】已开启日志增加当前轮询时间（MM-DD HH:mm:ss）。
- `ui/main_window.py`：
  - `【定时器】已开启，每 {secs} 秒轮询一次】` → `【定时器】已开启，每 {secs} 秒轮询一次，当前轮询时间 {time.strftime('%m-%d %H:%M:%S', time.localtime())}】`；
  - `定时器已开启、未启动`两处都同步更新（仅加时间后缀）。
- `tests/test_poller_log.py`：
  - 新增 `TestPollerEnableLogContainsTimestamp`（3 例）：断言日志含 `当前轮询时间`且匹配 `MM-DD HH:mm:ss` 正则。

## v0.1.14.1
“启动定时器”控件由 Switch 回退为 ttk.Checkbutton（用户反馈 Switch 样式不好看）。
- `ui/main_window.py`：
  - 移除 `from ui.widgets import Switch`；
  - `_build_mode_section`：将 `Switch(...)` 换回 `ttk.Checkbutton(text="启动定时器", variable=self.state.poller_enabled)`。
- `ui/widgets/__init__.py`：移除 Switch 对外导出（文件 `ui/widgets/switch.py` 作为控件库备用代码保留）。
- `tests/test_poller_toggle.py`：
  - `TestBuildModeSectionHasPollerSwitch` 重命名为 `TestBuildModeSectionHasPollerCheckbutton`；
  - 断言改为 `“Checkbutton(” in src`；
  - 反向断言改为 `“Switch(” not in post_section`。
- `tests/test_switch_widget.py`：`from ui.widgets import Switch` 改为 `from ui.widgets.switch import Switch`（Switch 类仍存在，只是不再从包入口导出）。

## v0.1.13.4
Switch 控件样式升级：真圆角矩形 + 圆形滑块 + 阴影 + ON/OFF 内嵌文字 + 悬停高亮。
- `ui/widgets/switch.py`：
  - 背景改为**真圆角矩形**（用 2 个半圆 `create_arc` + 中间 `create_rectangle` 拼接，
    而不是方角矩形），圆角半径 = HEIGHT / 2。
  - 配色优化：
    - 开启态：`#07c160`（微信绿，更柔和）；悬停 `#06ae56`；
    - 关闭态：`#e0e0e0`（浅灰）；悬停 `#d0d0d0`；
    - 滑块：`#ffffff` 圆形，半径比 HEIGHT 略小；
    - 滑块下方有 `#cccccc` 灰色阴影（提升层次感）。
  - 内嵌 **ON/OFF 文字标签**（开启态绿底白字 / 关闭态灰底深灰字，居于控件中央
    偏滑块对侧）。`show_label=True` 控制是否显示（默认 True）。
  - 鼠标悬停（`<Enter>` / `<Leave>`）切换 `_hover` 标志，渲染时使用更深色。
  - **修复 tk 不支持 8 位 hex 颜色**：阴影从 `#00000020` 改为 `#cccccc`。
- `tests/test_switch_widget.py`：
  - `test_render_changes_canvas_bg`：改用 `canvas.itemcget(..., "fill")` 检查
    绘制元素颜色（不再是 canvas.bg，因为 bg 始终为白色透出）。
  - `test_variable_change_triggers_render`：同上，验证 trace 触发重绘。

## v0.1.13.3
「启动定时器」控件由 ttk.Checkbutton 替换为自定义 Switch 控件。
- 新增 `ui/widgets/__init__.py` / `ui/widgets/switch.py`：
  - `Switch(tk.Frame)` 基于 `tk.Canvas` 自绘：圆角矩形 + 圆形滑块。
  - 开启态：绿色背景（#4caf50）+ 滑块靠右；
  - 关闭态：灰色背景（#bdbdbd）+ 滑块靠左；
  - 点击 Canvas 或右侧文字标签都可切换 `variable`；
  - `command` 参数在点击后调用。
- `MainWindow._build_mode_section`：将 `ttk.Checkbutton(text='启动定时器', ...)`
  替换为 `Switch(variable=state.poller_enabled, text='启动定时器')`。
  - variable 写入会触发已有的 `trace_add('write', _on_poller_toggle)` 监听，
    无需额外 command 参数。
- 新增 `tests/test_switch_widget.py`（12 例）：基础创建、点击切换、command
  调用、label 文字、canvas 重绘、variable trace、destroy 清理。
- 更新 `tests/test_poller_toggle.py::TestBuildModeSectionHasPollerCheckbutton`
  → `TestBuildModeSectionHasPollerSwitch`：断言源码里出现 `Switch(` 且
  「启动定时器」之后不再有 Checkbutton。

## v0.1.13.2
修复定时器相关日志重复。
- `MainWindow._start_directory_poller` 之前会输出
  `[轮询] 已启动目录扫描定时器（每 60 秒）`，与 `__init__` /
  `_on_poller_toggle` 中的 `[定时器] 已开启，每 60 秒轮询一次` 重复。
- 删除了 `_start_directory_poller` 中的该日志，仅保留 `self.after(...)` 注册动作。
- 现在统一：定时器状态/轮询时间只在 `_on_poller_toggle`（用户切换）和 `__init__`
  （应用启动）两处输出；`_start_directory_poller` 静默注册 after id。
- 更新 `tests/test_poller_log.py`：
  - `test_start_does_not_log_directly`：验证 `_start_directory_poller` 不再输出日志；
  - `test_no_duplicate_log_on_init`：验证 `__init__` 不重复输出两种「已开启」文案。

## v0.1.13.1
运行日志输出「定时器是否开启」+「当前轮询时间」。
- `MainWindow._on_poller_toggle`：勾选 → 输出简单日志
  `[定时器] 已开启，每 {secs} 秒轮询一次`；取消 → 输出
  `[定时器] 已关闭`。日志走简单通道，始终显示到主窗口。
- `MainWindow._start_directory_poller`：启动日志改为简单日志（默认显示）。
  文案：「[轮询] 已启动目录扫描定时器（每 60 秒）」。
- `MainWindow.__init__`：应用启动时立即输出定时器初始状态日志：
  - 勾选：`[定时器] 已开启，每 60 秒轮询一次`；
  - 未勾选：`[定时器] 未启动（需手动勾选「启动定时器」才会每 60 秒轮询）`。
- 新增 `tests/test_poller_log.py`（6 例）：覆盖 _on_poller_toggle 勾选/取消
  日志内容（含「[定时器]」/「已开启」/「已关闭」/「秒」）、_start_directory_poller
  输出 simple 日志、__init__ 包含 POLL_INTERVAL_MS 引用。

## v0.1.13.0
主界面「文档生成模式」栏末尾增加「启动定时器」复选框，控制目录轮询启停。
- `pipeline.config.DEFAULTS["poller_enabled"] = True`（默认开启，保留 v0.1.11/v0.1.12 行为）。
- `ui.state.AppState.poller_enabled`：BooleanVar 持久化字段，写入 settings.json。
- `MainWindow._build_mode_section`：在「批量配图生成」之后加 `ttk.Checkbutton(
  text="启动定时器", variable=state.poller_enabled, command=_on_poller_toggle)`。
- `MainWindow._on_poller_toggle`：
  - 勾选 → 重置 `_poller_closed = False` 并调 `_start_directory_poller()`；
  - 取消 → 调 `_stop_directory_poller()`。
- `MainWindow.__init__`：
  - 仅当 `state.poller_enabled.get()` 为 True 时才 `after(200, _start_directory_poller)`；
  - 注册 `state.poller_enabled.trace_add("write", _on_poller_toggle)` 监听切换。
- `MainWindow._scan_directory_for_documents`：构造 `PipelineConfig` 前先用
  `dataclasses.fields()` 白名单过滤 DEFAULTS，避免 UI 字段（如 poller_enabled）
  触发 `unexpected keyword argument`。
- 新增 `tests/test_poller_toggle.py`（10 例）：覆盖默认值、AppState 字段、
  _on_poller_toggle 行为、构建源里有 Checkbutton。

## v0.1.12.0
运行日志分为「简单运行日志」与「详细调试日志」两种，按日期各自单独存储。
- **简单运行日志**（默认显示到主窗口运行日志区）：
  - 写入 `Log/YYYY-MM-DD-simple.log`；
  - 关键状态（开始/完成/错误/计数/分割线）。
- **详细调试日志**（仅勾选「详细调试日志」时显示到主窗口）：
  - 写入 `Log/YYYY-MM-DD-verbose.log`；
  - OCR 预热、轮询、目录扫描、识别细节等调试信息。
- 汇总日志 `~/.doubao_bot/pipeline.log` 同时保留两类（不分流）。
- 每篇文档处理前/结尾输出装饰性 `=` × 59 分割线，便于视觉区分。
- `MainWindow._log(msg)` 旧调用继续走简单日志（向后兼容）。
- `MainWindow._log_simple(msg)` / `_log_debug(msg)` 新方法：显式分流。
- `MainWindow._emit_log(msg, kind, show)` 内部统一入口；`_log_debug` 仅当
  `state.verbose_log` 勾选时显示到主窗口。
- `pipeline.config.daily_log_path(today=None, kind="simple")` 支持 kind 参数。
- `pipeline.config.DEFAULTS["verbose_log"]` 默认 `False`（未勾选时只显示简单）。
- `ui/state.AppState.verbose_log` 默认从 `DEFAULTS["verbose_log"]` 读取。
- `pipeline.service.PipelineService._log_doc_banner / _log_doc_tail`：
  - 输出 `===...` 顶/中/底三行；banner 含批次进度 `▶ 开始处理文档 N/M：xxx`，
    tail 含 `✓ 完成 / ✗ 失败` 状态 + 摘要（如 `4 张配图`）。
- `MainWindow` 中以下 11 处调用从 `_log(...)` 改为 `_log_debug(...)`：
  - OCR 引擎预热（成功/失败）
  - 轮询启动 / 扫描 / 跳过 / 异常
  - 目录扫描详情（已选择 / 共找到 / 列举每个）
- `MainWindow._log` 回调 → 改为 `log_debug=self._log_debug`（不再走 `_log`）。
- 删除 `_run_one` / `_run_one_plan` 中旧的 `"=" * 50` 分割线，改为调用 `_log_doc_banner/tail`。
- 新增 `tests/test_log_split.py`（19 个用例）：
  - `TestDailyLogPathKind`：daily_log_path kind 参数；
  - `TestDefaultsVerboseLog`：DEFAULTS verbose_log 默认值；
  - `TestMainWindowLogSplit`：_log_simple / _log_debug / _log 在主窗口的显示策略；
  - `TestAppendDailyLogKind`：_append_daily_log 入队元组 (line, kind)；
  - `TestFlushDailyLogLines`：_flush_daily_log_lines 按 kind 写文件；
  - `TestDocBanner`：_log_doc_banner / _log_doc_tail 输出。
- 更新 `tests/test_pipeline.py`：
  - `TestDailyLogPath::test_daily_log_path_format`：增加 verbose kind 检查；
  - `TestAppendDailyLog::test_daily_log_written`：路径改为 `-simple.log`；
  - `TestOutputLayout::test_separator_after_each_document`：改为 `=` × 30 子串匹配；
  - `TestTryAutoStart::test_skips_when_spec_empty` /
    `test_skips_when_directory_missing`：显式开启 `verbose_log` 才能看到 verbose 日志。
- 更新 `tests/test_optim_c_plan_m5.py::mock_path`：支持 kind 参数。
- 更新 `README.md`：「日志日切归档」→「日志分级 + 日切归档」段落。

## v0.1.11
应用启动 / 修改选择目录不再自动开始生成；改为每 60 秒轮询批量目录。
应用启动 / 修改选择目录不再自动开始生成；改为每 60 秒轮询批量目录。
- 移除 `_schedule_auto_start_debounced` / `_on_auto_start_debounced` /
  `_try_auto_start_startup` 三个旧方法和 `_auto_start_debounce_after_id` /
  `_app_startup_done` 两个旧字段，以及 `input_dir` / `plan_input_dir` 上的
  `trace_add("write", ...)` 自动启动钩子。
- 新增 `MainWindow._start_directory_poller()`：启动 `after(POLL_INTERVAL_MS, _on_directory_poller_tick)`
  定时器；首次输出日志「[轮询] 已启动目录扫描定时器（每 60 秒）」。幂等启动。
- 新增 `MainWindow._on_directory_poller_tick()`：清空 after id → 调用
  `_try_auto_start()` → 重新注册下次 tick。异常被捕获，不影响下次调度。
- 新增 `MainWindow._stop_directory_poller()` / `destroy()` 覆写：窗口销毁时
  干净取消 after 定时器。
- 新增 `MainWindow._scan_directory_for_documents(mode, directory)`：
  - MODE_BATCH 复用 `vendors.doc_merger.core.batch.discover_documents`；
  - MODE_PLAN_BATCH 构造最小 `PipelineConfig`（不跑流水线），复用
    `PipelineService._discover_plan_documents`。
- 新增 `pipeline.config.POLL_INTERVAL_MS = 60_000` 常量。
- `_try_auto_start` 方法体改造：
  - 仅在「目录中存在匹配文档」时才触发 `_start()`，避免每分钟空跑；
  - 日志前缀 `【自动启动】` 改为 `【轮询】`；文案由「跳过自动生成」改为「跳过本次扫描」。
- 新增 `tests/test_directory_poller.py`（15 个用例）：覆盖常量化、生命周期、
  扫描、轮询 tick 行为。
- 更新 `tests/test_optim_c_plan_m5.py::TestM4AutoStartDebounce` →
  `TestM4AutoStartPoller`：检查新字段/方法存在，并断言旧 debounce 字段已删除。
- 更新 `tests/test_pipeline.py::TestTryAutoStart::test_skips_when_spec_empty`
  日志断言 / `test_starts_in_plan_batch_mode` 增加配图文档。
- 更新 `README.md`：「启动 / 改目录自动生成」→「每 60 秒轮询批量目录」。

## v0.1.10

- 远程 main tag：v0.1.10（本版本开始正式发布）
- 当前本地 tag：v0.1.10.0（提交后第四位归零、第三位 +1，开启下一轮开发循环）
- 提交范围：v0.1.9.0 → v0.1.10（含 v0.1.9.1 ∺ v0.1.9.21 共 21 个本地提交，21 个本地 tag）
- 主要变更（按版本号倒序）：
  - v0.1.9.21  OriginalDoc 自动排除 + 移除冗余的“图片加载完成”等待
  - v0.1.9.20  源文件自动归档 + 日志日切归档
  - v0.1.9.19  加载账号注册表时迁移旧阈值下的失败禁用态
  - v0.1.9.18  单账号每日额度从 8 改为 1000
  - v0.1.9.17  单账号连续失败阈值从 3 改为 6（当日暂停）
  - v0.1.9.16  应用启动 / 选目录后自动开始生成（批量模式，含子目录）
  - v0.1.9.15  生成完毕不再弹窗，全部走日志
  - v0.1.9.14  调试模式设置弹窗中“详细调试日志”同行新增“调试模式”总开关
  - v0.1.9.13  优化图片 URL 过滤：直接处理豆包返回的最新数据
  - v0.1.9.12  多豆包账号路由（账号独立 + 按篇数轮换）
  - v0.1.9.11  账号管理 UI 重构（列表渲染 + 新增/登出/删除按钮）
  - v0.1.9.10  账号信息读取（账号下拉菜单 + 详情弹窗）
  - v0.1.9.9   点击“新增账号”直接打开豆包登录页
  - v0.1.9.8   账号管理 UI 原型（调试弹窗中“调试与登录”栏）
  - v0.1.9.7   账号独立 + 按篇数轮换设计落地
  - v0.1.9.6   对话标题匹配逻辑改进（精确匹配 + 过滤噪音项）
  - v0.1.9.5   多账号设计与路由调研
  - v0.1.9.4   加载账号注册表时复用合并代码后的同步逻辑
  - v0.1.9.3   合并 DeepseekArticleGen 后的原图 HTTP 下载修复
  - v0.1.9.2   豆包“只下载原图/只下载浏览图”下载模式修正
  - v0.1.9.1   多账号架构调研 + 路由主键设计
- 本次远程提交动作：
  1. `git push origin main --follow-tags` → 推送 main 分支 + 带 tag 的提交。
  2. 远程 main 上打发布 tag `v0.1.10`（第三位 +1）。
  3. 本地删除 `v0.1.9.21`、新增 `v0.1.10.0`（第四位归零、第三位 +1）。

## v0.1.10.0

- 当前本地 tag：v0.1.10.0
- 修改内容：C 方案完整收益包 M0-M4 + M5（叡现提升、可观测）：
  1. **M0** 配置常量微调（低风险）：
     - POST_SUBMIT_WAIT_MS：1000 → 300
     - INTER_IMAGE_DELAY_SECONDS：1.0 → 0.2
     - _PRELOAD_HISTORY_JS 滚动轮数：6 → 3
     - detect_current_conversation_title 调用 max_wait：2.0 → 0.5
  2. **M1** 结构性优化：
     - OCR 引擎预热：应用启动 200ms 后后台线程加载模型（ui/main_window.py:_prewarm_ocr）
     - recent_conversation_titles 30s TTL 缓存：同一会话内重复调用直接返回缓存列表，
       新建/打开对话后主动失效
  3. **M2** 图级并行与下载：
     - watermark_workers 默认 1 → 2（同步 pipeline/models.py + pipeline/config.py 默认配置）
     - HTTP 并发下载本轮未实现（未来迭代项：M2-10），保留串行实现
  4. **M3** 业务参数调优：
     - BATCH_DEFAULT_DOC_DELAY_SECONDS：15.0 → 6.0（8 篇批量节省 ~72s）
     - 日志同步落盘改为队列 + 100ms 后台线程批量 flush（ui/main_window.py：
       _ensure_daily_log_flusher / _flush_daily_log_lines / _flush_daily_log_pending）
     - 会话结束时 finally 中阶退剩余日志避免末尾 100ms 内日志丢失
  5. **M4** 架构级：
     - WAIT_STABLE_SECONDS：6.0 → 3.0（豆包不再追加图片后 1-2s 即可上面出去）
     - auto_start 3 秒防抖：选择目录连续修改仅在停手 3 秒后才触发，避免调试期频繁切换路径立即跑空
  6. **M5** 可观测：
     - PipelineConfig.slow_stage_threshold = 60.0（默认阈值）
     - _time_stage 超阈值输出 [警告] 日志便于快速定位瓶颈
     - 浏览器启动耗时埋点（vendors/doubao_bot/models/browser.py：_start_t0 / [耗时] 浏览器启动完成）
  7. 测试：新增 tests/test_optim_c_plan_m5.py 共 12 例：
     - M0：POST_SUBMIT / INTER_IMAGE_DELAY / BATCH_DEFAULT_DOC_DELAY / WAIT_STABLE / preload round<3（4+1）
     - M1-7：recent_titles cache hit / miss-then-write（2）
     - M3-13：_flush_daily_log_lines 多行写入（1）
     - M4-14：_try_auto_start debounce 接口检查（1）
     - M5：slow_stage_threshold 字段 + _time_stage 警告/未警告（3）
     - 同步修复：test_conversation_select.test_in_target_conversation_continues 期望 max_wait=0.5
     全量 316 例通过（基线 304 + 新增 12）。
  8. 预计收益（单篇流水线）：
     - doc_delay 15→6：8 篇批量节省 ~72s
     - INTER_IMAGE_DELAY 1→0.2：4 张图节省 ~3s/篇
     - watermark_workers 1→2：4 张图去水印节省 5-15s/篇
     - WAIT_STABLE 6→3：单篇节省 3-6s
     - POST_SUBMIT 1000→300：单篇节省 0.7s
     - preload 6→3：单篇节省 0.9s
     - OCR 预热：首篇节眉 1-3s
     - recent_titles 缓存：重复匹配节省 1-2s/篇
     合计单篇节省 ~13-30s；批量 8 篇总节省 ~3-6 分钟（约 30-50%）。

## v0.1.9.21

- 当前本地 tag：v0.1.9.20
- 修改内容：OriginalDoc 排除 + 移除冗余"图片加载完成"等待：
  1. OriginalDoc 子目录（含递归子目录）不参与文档发现（v0.1.9.20 已实现
     源文件自动归档到 OriginalDoc/，本次避免已归档文档被再次批量处理）。
     - `vendors/doc_merger/core/batch.py:_EXCLUDED_DIRS` 增加 `"originaldoc"`，
       大小写无关（递归 + 非递归共用）。
     - `pipeline/service.py:_PLAN_EXCLUDED_DIRS`（配图模式批量）同步加入
       `"originaldoc"`。
  2. 移除 `vendors/doubao_bot/models/automation.py:wait_and_download()` 中
     `self._wait_images_loaded(page)` 调用。
     - 等待目的：等 `<img>` naturalWidth ≥ 200（解码完成）才进入下一步。
     - 实际场景下豆包图片已成功渲染，等待常因 JS 选择器命中 UI 小图标
       （阈值 200 太严格）或命中历史对话图片而假阳性超时；下一步
       `_order_by_dom` 会重新滚动并按 DOM 收 URL，本身即可拿到稳定的
       当前对话新图，节省最多 45 秒。
     - 方法本体 `_wait_images_loaded()` 保留，避免破坏其他潜在调用方；
       配置常量 `WAIT_IMAGES_LOADED_TIMEOUT_SECONDS / POLL_MS` 保留。
  3. 测试：tests 追加 3 例（共 304 例通过，基线 301 + 3）。
     - tests/test_pipeline.py::TestCollectDocuments 新增
       `test_batch_excludes_originaldoc_top_level` +
       `test_batch_excludes_originaldoc_nested_recursive`
       （覆盖顶层 OriginalDoc/ 与 OriginalDoc/sub/deep/ 嵌套）。
     - tests/test_plan_pipeline.py::TestCollectPlanDocuments 新增
       `test_plan_batch_recursive_excludes_originaldoc`
       （配图模式递归扫描排除 OriginalDoc/ 与 OriginalDoc/sub/）。
  4. 全量 compileall + pytest 通过。

## v0.1.9.20

- 当前本地 tag：v0.1.9.19
- 修改内容：源文件自动归档 + 日志日切归档：
  1. 源文件自动归档（`pipeline/service.py` 新增 `_archive_original_doc(doc)`）
     - 单文档 / 配图文章模式生成成功后，把最初的源文件移动到与源文件同级
       的 `OriginalDoc/` 目录：`pipeline/config.py:ORIGINAL_DOC_SUBDIR = "OriginalDoc"`。
     - 单文档模式移动单个 `.docx` / `.md`；配图模式移动配图说明 `.md` 与文章 `.docx`。
     - 重复运行覆盖；源文件已在 `OriginalDoc/` 时跳过（避免 `OriginalDoc/OriginalDoc/` 循环）。
     - 移动失败仅写日志，不中断流水线。
     - 调用点：`_run_one` 与 `_run_one_plan` 在 `item.ok = True` 之后。
  2. 日志日切归档（`ui/main_window.py` 新增 `_append_daily_log(line)`）
     - 每条运行日志同步追加写入工程根目录下 `Log/YYYY-MM-DD.log`
       （`pipeline/config.py:LOG_DIR` 通过 `Path(__file__).resolve().parent.parent / "Log"` 计算，
       不依赖 `cwd`）。
     - 旧 `~/.doubao_bot/pipeline.log`（`pipeline/config.py:LOG_FILE`）行为保留
       —— 主窗口「详细日志」查看器仍打开旧文件，不受影响。
  3. 测试：tests/test_pipeline.py 新增 3 个测试类共 7 例
     - `TestArchiveOriginalDoc`（4 例）：基本移动、自动建目录、幂等、缺失文件 noop
     - `TestDailyLogPath`（2 例）：LOG_DIR 路径格式、daily_log_path 日期格式化
     - `TestAppendDailyLog`（1 例）：`_log()` 同步落盘到 `Log/YYYY-MM-DD.log`
     - 同步修复 `tests/test_plan_pipeline.py:test_plan_single_full_flow`：
       原文 docx / 配图 md 现在归档到 OriginalDoc，断言路径更新。
     全量 301 例通过。
  4. 同步文档：README.md「简洁主界面」段落补充「源文件自动归档 / 日志日切归档」。

## v0.1.9.19

- 当前本地 tag：v0.1.9.18
- 修改内容：加载账号注册表时迁移旧阈值下的失败禁用态：
  - 现象：v0.1.9.17 把连续失败阈值改为 6 后，已经因「连续失败 3 篇」
    被当日暂停的账号（如 18611596317）仍处于 `health.disabled=True`、
    `disabled_reason="连续失败 3 篇，今日暂停该账号"` 状态；当日
    `_roll_day()` 不重置，`allow_start()` 把旧 reason 当成新 reason
    返回，日志里持续出现「连续失败 3 篇，今日暂停该账号」。
  - 修复：`pipeline/accounts.py:_normalize_spec()` 加载 spec 后，
    若 `health.disabled=True` 且 `disabled_reason` 以「连续失败」开头
    且 `failures < ACCOUNT_DISABLE_AFTER_FAILURES`，自动解除禁用
    （清 `disabled` 与 `disabled_reason`）。
  - 风险信号类禁用（reason 以「命中风控/登录信号」开头）不受影响，
    继续保留禁用状态；下次启动应用后旧阈值下的失败禁用账号即可重试。
  - 测试：tests/test_accounts.py 新增
    `test_migrate_stale_failures_disable_on_load`（3 个场景：阈值上调后
    自动解除 / 已达阈值仍禁用 / 风险信号类不迁移）。全量 294 例通过。

## v0.1.9.18

- 当前本地 tag：v0.1.9.17
- 修改内容：单账号每日额度由 8 篇改为 1000 篇：
  - `pipeline/accounts.py:DEFAULT_LIMITS = {"daily": 1000, ...}`（原为 8）。
  - `allow_start()` 内 `spec["limits"].get("daily", 1000)` 同步兜底。
  - 影响：账号健康字段 `health.failures`、`health.consecutive` 触发的当日
    禁用/休息/额度用完仍生效，但 1000 篇/账号基本上不再会因为「额度用尽」
    而跳过；连续失败 6 篇仍会触发「当日暂停」（v0.1.9.17 已改）。
  - 同步：pipeline/accounts_cli.py 示例与 `--daily` 帮助、README.md 多账号段落。
  - 测试：tests/test_accounts.py 现有「当日额度用尽」用例显式
    `spec["limits"]["daily"] = 8` 把额度做成测试可控（不再依赖默认）；
    新增 `test_default_daily_limit_constant` 直接断言常量 = 1000。
    全量 293 例通过。

## v0.1.9.17

- 当前本地 tag：v0.1.9.16
- 修改内容：单账号连续失败阈值由 3 篇改为 6 篇：
  - `pipeline/accounts.py:ACCOUNT_DISABLE_AFTER_FAILURES = 6`（原为 3）。
    任一豆包账号连续失败达到该次数后当日暂停（防 429/登录失效反复撞墙）。
  - 现有 `test_three_failures_disable` 改写为 `test_disable_after_threshold_consecutive_failures`，
    直接引用 `ACCOUNT_DISABLE_AFTER_FAILURES`，并补「阈值-1 篇仍可用、第 N 篇才暂停」边界断言；
    以后改阈值不再需要改测试硬编码。全量 292 例通过。
  - 同步 README.md 多账号段落描述。

## v0.1.9.16

- 当前本地 tag：v0.1.9.15
- 修改内容：应用启动 / 选目录后自动开始生成 + 普通模式输入持久化：
  1. 新增 `MainWindow._try_auto_start()`：`ui/main_window.py`
     - 仅「批量文档生成 / 批量配图生成」模式生效；单文档 / 单配图文档模式不触发
       （它们的输入是单个文档，不存在「目录」概念）。
     - 跳过忙碌态、空目录、目录路径不存在等无效情形；目录不存在时写
       `[自动启动] 目录不存在，跳过自动生成：…`。
     - 按用户要求「包含子目录的文档」，自动启用「递归扫描子目录」并持久化
       （`state.recursive` 已在 _PERSIST_KEYS 里）；若已启用不再重复写日志。
     - 普通批量模式且「图片要求设定」为空时跳过自动生成，避免 `_validate` 内的
       `askyesno` 模态确认框阻塞无人值守流程；只写
       `[自动启动] 「图片要求设定」为空，跳过自动生成；请填写后手动点击「开始生成」`。
     - 触发点：`state.input_dir` / `state.plan_input_dir` 的 `write` trace
       （`after(50, …)` 防抖）+ `__init__` 末尾 `after_idle(self._try_auto_start)`。
  2. 普通模式输入持久化（修复「重启后上次选择目录丢失」的前置缺陷）：
     - `_PERSIST_KEYS` 增加 `doc_path` / `input_dir` / `output_root`，与
       `plan_doc_path` / `plan_input_dir` 对齐（之前 plan 已持久化，regular 没
       有，行为不一致）。
     - `AppState.__init__` 从 `settings` 读取上述键，无值时回落到空串。
  3. 测试：tests/test_pipeline.py 新增 10 例
     - `TestTryAutoStart`（7 例）：single / spec 空 / 目录不存在 / 忙碌态跳过；
       batch / plan_batch 自动开始；递归已开启时不重复写日志。
     - `TestPersistedInputVars`（3 例）：`doc_path` / `input_dir` / `output_root`
       跨次启动恢复。
     全量 292 例通过。
  4. 同步文档：README.md「简洁主界面」段落补充「启动 / 改目录自动生成」。

## v0.1.9.15

- 当前本地 tag：v0.1.9.14
- 修改内容：生成完毕改日志提示 + 新增「账号切换等待秒数」：
  1. 全部文章生成完毕后不再弹窗提示，改为运行日志输出（`ui/main_window.py:_worker`）：
     - 成功：`[完成] 流水线完成，共成功 N 篇。`
     - 有失败：`[完成] 流水线结束：成功 N 篇，失败 M 篇。详见运行日志。`
     - 异常终止：`[错误] 流水线异常终止：…`（不再 `showerror`，状态栏显示「失败」）
     - 校验类提示弹窗（未选文档等）与「强制终止」流程保持不变。
  2. 调试模式设置弹窗「调试与登录」栏新增**账号切换等待秒数**（`ttk.Spinbox`，
     步长 3 秒，`0` = 不等待）：切换豆包账号时等待基准值 N ± 3 秒区间内的随机秒数
     （例：N=5 → 2~8 秒随机），用于降低高频切号的风控风险。
     - 配置链路：`config.DEFAULTS["account_switch_wait"]` +
       `config.ACCOUNT_SWITCH_WAIT_JITTER = 3` → `PipelineConfig.account_switch_wait`
       → `AppState.account_switch_wait`（持久化键同名字段，`build_config()` 带出）。
     - 服务层：`service._wait_account_switch()` 在 `_activate_account()` 中仅于
       **账号真的发生切换**时触发（首次激活 / 同账号复用会话不等待），走
       `_sleep_breakable()`，可被「强制终止」立即打断；每次等待打印
       `[账号] 账号切换等待 X.X 秒（基准 N 秒，区间 N-3~N+3 秒随机）：A → B`。
  3. 测试：tests/test_accounts.py 新增 9 例（0 不等待 / 首次激活不等待 / 同账号不等待 /
     区间随机 [2,8] 且非固定值 / 走可打断休眠 / 默认值与抖动常量 / 负数基准 /
     小基准下限归零）；tests/test_pipeline.py 全量调试项持久化用例补
     `account_switch_wait`。全量 282 例通过。
  4. 同步文档：README.md、docs/doubao_generation_flow.md。

## v0.1.9.14

- 当前本地 tag：v0.1.9.13
- 修改内容：账号列表列调整（总生成篇数）+ 修复「设了配额却不轮换」：
  1. 账号列表：去掉「手机」列，新增「总生成篇数」列（昵称 / 总生成篇数 /
     每次生成篇数 / 默认账号 / 登录状态 / 操作）：
     - 数据来源 `spec["total"]`：`record_done()` 在**成功**篇结束时 +1，
       失败篇不计入，持久化在账号注册表（`_normalize_spec()` 为旧注册表补 0）。
     - 手机号仍照旧写回 `phone` 字段，只是不再占用列表列。
  2. 修复实测缺陷「设定了 2 个账号各 2 篇，却还是一个账号生成了 4 篇」：
     - 现场：`pipeline_settings.json` 里 `account_rotate=false` 且
       `account_id=doubao_1`（手动指定账号）→ 全部文档都走该账号，配额被静默忽略。
     - `_enable_rotation_for_quota()`：保存「每次生成篇数」> 0 时自动开启
       「按篇数轮换」并取消手动指定账号（写明确日志），让设置自洽。
     - `_strategy_text()`：账号列表下方常显「当前策略：手动指定 X / 按篇数轮换
       A 各 N 篇 → B 各 N 篇 / 未启用轮换」，不再需要靠日志推断。
     - `service._log_account_strategy()`：每次开始生成时先打印一行账号策略；
       手动指定 + 勾选轮换同时存在时额外提示「手动指定账号优先」。
  3. 修复 `rotation_pick()` 的 quota=0 漏洞：0 表示不参与轮换，旧逻辑在该账号
     恰好是游标时会一直返回它（另一账号有配额也轮不到）；现在改为跳过，仅当
     其他账号都不可用时才用它兜底，全部为 0 时沿用当前账号用到底。
  4. 修复连续计数不归零（同一处缺陷）：达到「连续 ≤N 篇」上限进入休息窗口后，
     `consecutive` 未归零，导致休息结束后**每再做 1 篇就又触发一次 20 分钟休息**；
     现在进入休息窗口即归零，休息后可重新连做 N 篇（`record_done()`）。
     （补充）同时兼容旧数据：`allow_start()` 遇到「休息已结束但连续计数仍为上限」
     时按新一轮处理，避免升级后多做一次无谓等待。
  5. 测试：tests/test_accounts.py 新增 10 例（total 只计成功篇 / 旧注册表补 0 /
     quota=0 跳过 / 全 0 用到底 / 账号策略日志三种形态 / 休息后连续计数归零 /
     旧数据归一化）；tests/test_account_list.py 新增 1 例（列表列定义）。
     全量 273 例通过。
  6. 同步文档：README.md、docs/doubao_generation_flow.md（3.1 账号段落）。

## v0.1.9.13

- 当前本地 tag：v0.1.9.12
- 修改内容：账号列表改回系统默认表格样式 + 修复登录昵称/手机号读取：
  1. 账号列表改用系统默认 `ttk.Treeview` 表格（修复「列表发灰、看不到列分隔线」）：
     - `show="headings"` 的表头、列分隔线、行选中高亮全部用系统默认样式，
       不再自绘 Frame + Label + Separator 表头；横/纵向滚动条保留。
     - 「操作」列的「登录 / 登出 / 删除」由按钮改为三段可点文字（Treeview 单元格
       无法内嵌控件）：`_action_at()` 按中文字体实测宽度划分命中区，`_cell_left()`
       校准 Tk `bbox()` 与 `identify_column()` 之间恒定几像素的边界差，
       避免点击落到相邻列。
     - 「每次生成篇数」改为双击就地编辑（`_edit_quota()` 在单元格上叠加 Spinbox，
       回车/失焦写盘、Esc 取消）；`_save_row_quota()` 改为接收数值参数。
     - 列宽改用 Treeview 原生拖拽，`_on_account_release()` 松手写回
       `account_col_widths`（仍由 `parse_col_widths()` 读回）。
     - 移除 canvas/Frame 自绘列表相关方法（`_render_account_header`/
       `_render_account_row`/`_start_col_drag`/`_drag_col`/`_end_col_drag`/
       `_apply_col_widths`/`_on_canvas_configure`/`_clip`）。
  2. 修复「登录后昵称不是豆包昵称、手机号不更新」：
     - 根因：豆包把账号信息 SSR 注入页面内联脚本 `window._ROUTER_DATA`，
       未登录/会话过期时 `accountInfo.data.name` 是错误串（实测
       `account_info_error`、`js_error`，且 `user_id=0`、`error_code=13`、
       `description=会话过期，请重新登录`）。旧逻辑只解析接口响应/本地存储/
       页面文本，SSR 里的真实昵称从未被读取。
     - 新增 `ROUTER_JS` + `extract_router_account()`：只取 `accountInfo` 节点
       （昵称 `name`/`screen_name`、手机号 `mobile`/`phone`、`user_id`/`error_code`），
       错误串一律过滤；`merge_account_info()` 让 SSR 结果优先于接口/存储/文本。
     - `_BAD_NICK_RE` 增加 `account_info_error`；`capture_account_info()` 每轮重读
       SSR，并新增日志「SSR 账号状态：已登录 / 未登录·会话过期」+ SSR 昵称/手机号
       候选（详细调试日志下输出）。
     - UI 双保险：`_capture_login_info()` 拒绝写回错误串并记录日志；
       `display_name()` 让历史脏数据回落到账号名/ID；`_drop_bad_displays()` 在刷新
       列表时把注册表里已有的错误昵称清空并记日志。
     - 手机号：豆包网页端默认不展示手机号，只有豆包下发 `mobile` 字段时该列才有值，
       否则显示 `—` 并记录「豆包未返回手机号」。
  3. 测试：`tests/test_account_info.py` 新增 6 例（SSR 正常/过期占位串/JSON 串与
     整页嵌套/合并优先级/捕获优先 SSR/捕获忽略 SSR 占位串）；
     `tests/test_account_list.py` 新增 2 例（`col_ref()` 列标识、
     `display_name()` 脏昵称回落）；全量 263 例通过。
  4. 同步文档：README.md（多账号章节）、docs/doubao_generation_flow.md（3.1 账号段落）。

## v0.1.9.12

- 当前本地 tag：v0.1.9.11
- 修改内容：账号列表三项改进（昵称被写成 js_error / 列宽可调并记忆 / 新增账号直接扫码建档）：
  1. 修复实测缺陷「登录后昵称被写成 js_error」：
     - vendors/doubao_bot/models/account_info.py：新增 `is_bad_nickname()` 与
       过滤规则——`js_error`/`error`/`undefined`/`null`/`none` 等占位错误串、
       snake_case 内部标识（`user_not_login`）、纯数字、纯符号、不含字母/汉字的
       文本都不再作为昵称；候选值按「首次出现」去重。
     - 嗅探到的接口响应分两桶：URL 命中 user/profile/account/passport/member/
       login/mine/setting 的为主来源，其余豆包接口为兜底，解析时主来源永远排在
       前面，避免报错串抢占；主来源是错误串时自动用存储/文本里的真实昵称兜底。
     - `extract_account_info(..., report=...)` 回填原始候选，读不到昵称/手机号时
       在详细调试日志打印候选（截断、限 5 条），便于定位豆包字段变化。
  2. 账号列表列宽可自由调整并持久化：
     - 表头列名右侧新增 8px 拖拽把手（鼠标变左右箭头），按住横向拖动实时改列宽
       （下限 40px，只影响当前列），松手即写入 `account_col_widths`
       （ui/state.py 持久化到 pipeline_settings.json），下次打开沿用；
       列宽总和超过画布时出现横向滚动条（画布内容宽度取列宽总和与画布宽的较大者）。
     - 新增纯函数 `parse_col_widths()`：缺省/脏数据/列数不符回落默认列宽并做
       最小宽度保护；新增 `_apply_col_widths()` 原地套用（不重建控件，拖动顺滑）。
  3. 「新增账号…」改为直接扫码登录建档：
     - 点击后直接打开豆包登录页（账号 ID 自动分配 doubao_1、doubao_2…，见
       `next_account_id()`），登录成功后自动建档并入列表、自动选中，昵称/手机号/
       指纹随登录一并写入；登录未完成（关窗/超时）不建档，不留空账号；
       重复点击在登录进行中会被拦截并提示。
     - 移除旧的手填表单 `_NewAccountDialog` 与 `_create_account()`（不再需要
       「先建档再登录」）。
  4. 测试：新增 tests/test_account_list.py（列宽解析/最小宽度/往返、账号 ID 分配）
     与 test_account_info.py 新增 6 例（js_error 过滤、错误串回退其它来源、
     snake_case/纯符号拒绝、report 候选、接口优先级、capture 拒绝占位串）；
     全套 255 例通过。GUI 冒烟验证：持久化列宽被读回、拖动后写入设置文件、
     新增账号启动登录线程参数、登录成功后建档并选中、列宽日志与弹窗尺寸。
  5. 文档：README 多账号章节与 docs/doubao_generation_flow.md 3.1 同步
     （昵称过滤与调试日志、列宽拖动记忆、新增账号扫码建档）。
- 涉及模块：vendors/doubao_bot/models/account_info.py、ui/debug_dialog.py、
  ui/state.py、tests/test_account_info.py、tests/test_account_list.py、
  README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-12

## v0.1.9.11

- 当前本地 tag：v0.1.9.10
- 修改内容：账号区改为列表展示（不再用下拉），并补上登录账号信息读取：
  1. ui/debug_dialog.py：「调试与登录」栏账号区重写为「豆包账号列表」——
     一行一个账号，列为「登录账号昵称 / 手机 / 每次生成篇数 / 默认账号 /
     登录状态 / 操作」，行内「登录 / 登出 / 删除」按钮直接作用于该行账号；
     「每次生成篇数」行内 Spinbox 编辑（`<Return>`/`<FocusOut>`/箭头即保存）；
     单击行 = 当前使用账号（▶ 标记），「取消当前使用账号」回到轮换/默认策略；
     双击「默认账号」列设为默认；删除走二次确认（可选是否删除本地登录态目录，
     删除路径限定在 ACCOUNTS_DIR 之内）；空列表显示灰色占位行；
     列表用 Canvas+每行 Frame（grid 统一列宽）而非 Treeview——行内需要真实按钮，
     避免覆盖控件随滚动错位，超过 6 行自动出现滚动条。
  2. 按钮位置：「新增账号…」移到「详细日志」之前、同一行。
  3. 移除下拉/配额行相关方法（_sync_quota_from_selection / _save_quota /
     _set_default_account 无参版），新增 _render_account_rows / _render_account_row
     / _render_account_header / _account_logged_in / _select_account /
     _clear_account_selection / _save_row_quota / _delete_account /
     _remove_account_dir / _scroll_accounts / _clip / _after 等方法。
  4. 登录目标账号化：登录/检查登录状态/登出均支持指定账号（行内按钮点哪个就操作
     哪个并同步选中），登出后自动刷新「登录状态」列；登录成功后新增
     _capture_login_info()，读取昵称/手机号与登录指纹写回注册表并刷新列表。
  5. vendors/doubao_bot/models/account_info.py（新增）：capture_account_info()
     从页面自身用户信息接口响应 → localStorage/sessionStorage → 页面文本兜底
     提取昵称与手机号；extract_account_info() 为纯函数（便于测试）；
     全程尽力而为，读不到返回空串、不阻断登录。
  6. pipeline/accounts.py：账号结构新增 phone 字段（含旧注册表兼容），
     upsert_account() 支持 display/phone/login_fingerprint 覆盖；新增
     fingerprint_from_cookies()（由 uid_tt/sid_tt 等登录 cookie 派生 12 位指纹，
     手机号不可得时的稳定识别依据）。login.py 新增 login_cookies() 读取当前 cookie。
  7. 测试：新增 tests/test_account_info.py 13 例（提取/掩码归一化/裸 name 需用户
     标识/完整号优先/存储与文本兜底/空结果/昵称过滤/指纹稳定性/注册表往返与旧
     注册表兼容/capture 的接口响应、存储兜底、异常与第三方响应过滤）；
     全套 246 例通过。GUI 冒烟验证列渲染、行内操作、篇数保存、设为默认、
     登录状态列、登录目标、删除（含目录）、轮换勾选清空选择、弹窗 841x719。
  8. 文档：README 多账号章节与 docs/doubao_generation_flow.md 3.1 账号段落同步为
     列表式界面与登录账号信息读取说明。
- 涉及模块：ui/debug_dialog.py、pipeline/accounts.py、
  vendors/doubao_bot/models/account_info.py、vendors/doubao_bot/models/login.py、
  tests/test_account_info.py、README.md、docs/doubao_generation_flow.md、
  LOCAL_CHANGELOG.md
- 时间：2026-09-12

## v0.1.9.10

- 当前本地 tag：v0.1.9.9
- 修改内容：多账号改为「账号独立 + 按篇数轮换」的完整可用闭环（此前 GUI 无建档入口）：
  1. ui/debug_dialog.py：「调试与登录」栏补齐账号管理控件——账号下拉 + 刷新 +
     「新增账号…」+「设为默认」+ 灰字提示（未建档 / 共 N 个账号）；「每账号篇数」
     Spinbox +「保存到该账号」+ 语义说明（0 = 不参与轮换、有配额时每 N 篇切换）。
     新增方法：_sync_quota_from_selection() / _save_quota() / _set_default_account() /
     _new_account() / _create_account()；refresh_account_options() 增加提示文案并同步
     quota 显示。
  2. 新增 _NewAccountDialog：图形界面直接建档（账号 ID 校验沿用 _ACCOUNT_ID_RE、
     显示名称、每账号篇数默认 DEFAULT_QUOTA=4），确定后写注册表并回选新账号，
     取消/Esc 关闭，保存失败不关窗。
  3. 移除界面「自动路由」复选框及 _on_auto_route_toggle()：采用「账号独立 + 按篇数
     轮换」后自动路由不再需要；state/config/service 中的 account_auto_route 字段与
     目录名路由分支保留（默认 False），仅作旧配置兼容，不破坏既有行为。
  4. 登录目标账号化：登录豆包 / 检查登录状态 / 登出豆包改为作用于当前下拉选中账号
     （_login_target() 返回 profile_dir/proxy/label，登录态校验取该账号目录下的
     storage_state.json），日志带账号标签；未选账号时回落到默认 legacy 目录，
     单账号行为与改造前一致。
  5. 弹窗尺寸：新控件后请求高度 688，按既有自适应逻辑实际开出 728（min(req+40,
     屏高-40)），版权申明区完整显示、无需滚动。
  6. 测试：全套 233 例通过 + compileall 干净；GUI 冒烟验证空注册表下拉为 ('',)、
     建档后下拉含新账号、非法 ID 被拒、quota 读取/保存正确、设为默认生效、
     勾选轮换清空手动账号、_login_target() 分别命中账号目录与 DEFAULT_PROFILE_DIR、
     _NewAccountDialog 提交成功关闭 / 失败保持打开。
  7. 文档：README 多账号章节改写为「账号独立 + 按篇数轮换」（含 GUI 建档与 quota
     编辑入口、自动路由已降级为兼容保留）；docs/doubao_generation_flow.md 3.1 账号
     段落同步。
- 涉及模块：ui/debug_dialog.py、README.md、docs/doubao_generation_flow.md、
  LOCAL_CHANGELOG.md
- 时间：2026-09-12

## v0.1.9.9

- 当前本地 tag：v0.1.9.8
- 修改内容：账号设置整体迁移到「调试模式设置」弹窗的「调试与登录」栏：
  1. ui/debug_dialog.py：「调试与登录」栏新增两行——账号下拉 + 刷新 + 「（空 = 默认/
     legacy 单账号）」提示；以及「自动路由」「按篇数轮换」两个复选框。新增
     refresh_account_options() / _on_auto_route_toggle() / _on_rotate_toggle()
     三个方法（互斥与清空手动账号的原有行为保持不变），建档后立即刷新一次下拉。
  2. ui/main_window.py：删除主界面「1. 豆包对话标题」里的账号下拉/刷新/两个复选框
     及相关方法，去掉 accounts 模块导入；「开始生成」前的注册表刷新改为转发到弹窗
     （弹窗未打开时不做任何操作），保证运行时账号列表始终最新。
  3. 弹窗尺寸：新增内容后请求尺寸 746x659，按既有自适应逻辑实际开出 746x699，
     版权申明区仍完整显示、无需滚动。
  4. 测试：全套 233 例通过；GUI 冒烟验证账号下拉值来自注册表、两个复选框互斥、
     勾选轮换清空手动账号、build_config 正确带出 account_rotate，且主界面已不再
     暴露账号控件。
  5. 文档：README 多账号章节与 docs/doubao_generation_flow.md 3.1 的界面入口
     说明改为「调试模式设置 → 调试与登录」。
- 涉及模块：ui/debug_dialog.py、ui/main_window.py、README.md、
  docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-12

## v0.1.9.8

- 当前本地 tag：v0.1.9.7
- 修改内容：轮换配额改为「有替代账号才切换」，确认 quota=0 的用到底语义：
  1. accounts.py `rotation_pick()`：配额用满时不再无条件丢弃当前账号——先判断该
     账号当日是否还可用，并继续向后寻找其他可用账号；只有确实存在可接手的账号
     （含休息窗口中的账号，由服务层等待）才切换，否则返回当前账号并注明
     「已达轮换篇数 N，但无其他可用账号，继续使用」。
  2. 硬约束保留：当日额度用尽(daily)、休息窗口、当日禁用仍然生效——配额用满但
     处于休息窗口时继续等待；当日额度用尽/被禁用时本篇跳过（无账号可接手）。
  3. 服务层日志：`_log_account` 在配额已满仍在用时输出「轮换配额已满 N/M
     （无其他可用账号，继续使用）」；`_log_rotation_after_doc` 在无替代账号时输出
     「已生成 N/M 篇（配额已满），无其他可用账号，继续使用该账号」，不再误报
     「自动切换」。
  4. 语义确认：quota=0 = 该账号不参与轮换、一直用到底（改动前已支持，本次在
     README/CLI/流程文档中明确写出）；单账号或其余账号当日不可用时，即使 quota
     为正数也会用到底，剩余文档不再被跳过。
  5. 测试：新增 6 例（单账号配额满仍继续、另一账号被禁用时继续、另一账号休息时
     仍切换等待、配额满+休息仍等待、配额满+当日额度用尽跳过、单账号 quota=1
     批量 3 篇全部由该账号生成），tests/test_accounts.py 共 51 例，全套通过。
  6. 文档：README「按篇数轮换」补充配额切换条件与 quota=0 说明；
     pipeline/accounts_cli.py 帮助文本、docs/doubao_generation_flow.md 同步。
- 涉及模块：pipeline/accounts.py、pipeline/service.py、pipeline/accounts_cli.py、
  tests/test_accounts.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-12

## v0.1.9.7

- 当前本地 tag：v0.1.9.6
- 修改内容：多豆包账号调整——账号彼此独立 + 按篇数自动轮换：
  1. 账号独立：轮换/路由只依据豆包账号注册表（accounts.json）自身的声明顺序与
     各自配额，不与 Deepseek / 头条号等其他项目的账号建立任何绑定或关联字段。
  2. 新增按篇数轮换：每个账号连续生成自己的 quota 篇（默认 4，0=不参与轮换）
     后自动切到下一个启用账号。pipeline/accounts.py 新增 DEFAULT_QUOTA /
     DEFAULT_ROTATION、账号级 quota 字段、注册表 rotation 游标（cursor + used，
     跨次运行保留），AccountRouter 新增 rotation_state / rotation_quota /
     rotation_progress / rotation_pick / record_rotation_use / reset_rotation。
  3. 轮换与限额协同：rotation_pick 跳过「已达轮换配额 / 当日禁用 / 当日额度用尽」
     的账号，休息窗口内的账号排最后（全部在休息时取等待最短者，沿用既有等待逻辑）；
     全部不可用时本篇跳过并打印原因，绝不回退 legacy 默认 profile（防串号）。
  4. 服务层：新增 PipelineConfig.account_rotate（默认 False）与
     _rotation_enabled()；_resolve_account_for_doc() 优先级为「手动选定账号 >
     按篇数轮换 > 输入目录名自动路由」，注册表为空时保持 legacy；每篇结束调用
     record_rotation_use 记账，达到配额即输出「已生成 N/N 篇，自动切换到下一个
     账号：xxx」；_log_account 增加「轮换第 i/N 篇」进度。
  5. UI：主界面账号行新增「按篇数轮换」复选框，与「自动路由」互斥（勾选其一自动
     取消另一个），勾选轮换时清空手动选定账号；未配置账号时两者都自动取消。
  6. CLI：新增 `quota <账号> <篇数>` 与 `rotate-reset [账号]`，`add --quota N`，
     `list/status` 显示「轮换 used/quota 篇」。
  7. 测试：tests/test_accounts.py 新增 TestRotation（默认/规范化/顺序/配额切换/
     失败不计配额/切换清零/额度用尽跳过/禁用跳过/全不可用/全部休息取最短/0=不限/
     注册表往返/重置）与 TestServiceRotation（按配额切换、日志进度、手动优先、
     空注册表回退 legacy、全禁用时跳过并兜底抛错、6 篇批量前 4 篇 A 后 2 篇 B），
     全套 227 例通过。
  8. 文档：README「多账号」章节改写为「按目录路由 / 按篇数轮换」并补充 CLI 与
     优先级说明；docs/doubao_generation_flow.md 3.1 增补轮换实现与代码索引。
- 涉及模块：pipeline/accounts.py、pipeline/service.py、pipeline/config.py、
  pipeline/models.py、pipeline/accounts_cli.py、ui/state.py、ui/main_window.py、
  tests/test_accounts.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-12

## v0.1.9.6

- 当前本地 tag：v0.1.9.5
- 修改内容：等图阶段长对话性能优化（本轮只做 M0 / M3 / M5，M1 / M2 / M4 / M6 未实施）：
  1. M3 完成信号快速检测：image_wait.py 新增 _COMPLETE_FAST_JS，默认只扫描 baseline
     之后的新消息节点文本，不再读取 document.body.innerText（后者触发样式/布局计算，
     长对话下每轮开销大）；仅调试模式回退旧版 _COMPLETE_JS 做正文/toast 兜底排查。
     未命中完成文案时退化为「图片集合稳定 N 秒」退出路径，不影响正确性。
  2. M5 网络响应增量扫描：_collect_image_urls() 改为「游标 _rc_scan_index + 候选缓存
     _rc_pending / _rc_order」增量处理，历史响应只解析一次；输出阶段仍实时套用历史
     基线与 DOM 历史过滤，trust_network=True 时跳过 DOM 过滤。游标失效（响应列表被
     重置）时自动从头扫描，优先保证不漏图。_record_baseline() 记录基线时重置游标与缓存。
  3. M0 耗时埋点：等图循环逐步骤计时（滚动 / 新图 DOM / 历史 DOM / URL 过滤 / 完成
     检测），退出时经 _log_wait_timing() 输出一行汇总，仅在 debug 与 verbose_log 同时
     开启时打印，用于验证开销不再随对话历史增长。
  4. 测试：新增 tests/test_wait_scan_optim.py（15 例）覆盖增量扫描只解析新增响应、
     基线/历史过滤仍生效、候选择优、DOM 过滤实时生效、基线重置清空缓存、游标失效
     与负值兜底、完成检测快速版/调试回退版、耗时日志仅在调试模式输出等；全套 205 例通过。
  5. 文档：docs/doubao_generation_flow.md 新增 3.5.1「长对话下的开销控制（M0/M3/M5）」，
     防漏图要点补「长对话增量扫描」，并按改动后的实际行号重新核对 automation.py /
     image_wait.py / pipeline/service.py 的代码索引。
- 涉及模块：vendors/doubao_bot/models/image_wait.py、vendors/doubao_bot/models/automation.py、
  tests/test_wait_scan_optim.py、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-09-11

## v0.1.9.5

- 当前本地 tag：v0.1.9.4
- 修改内容：调试模式设置弹窗新增「调试模式」总开关，与「详细调试日志」分层：
  1. ui/debug_dialog.py：「详细调试日志」同一行新增「调试模式」复选框；弹窗宽度由
     固定 660px 改为按内容自适应（下限 660、上限屏幕宽-40），避免新增控件被裁剪。
  2. 语义分层：「调试模式」为总开关，勾选后启用调试信息采集（网络拦截、页面状态、
     等待参数等）；「详细调试日志」决定总开关开启时是否把 [调试] 明细输出到运行日志。
  3. 配置：PipelineConfig 新增 verbose_log（默认 True），debug 语义明确为调试模式；
     ui/state.py 持久化键改为 debug_mode / verbose_log（读取兼容旧键 "debug"），
     debug_mode 默认关闭（不再默认输出调试日志）。
  4. DoubaoImageBot 新增 verbose_log 参数，_log_debug 需 debug 与 verbose_log 同时
     开启才输出；callable 形式的日志在关闭时不求值，避免无谓的页面读取开销。
     PipelineService._debug_log 同样按两者与运算判断。
  5. 测试：state 持久化用例改用 debug_mode / verbose_log；全套 190 例通过；
     GUI 冒烟验证确认两个复选框同排、配置接线与持久化正确。
- 涉及模块：ui/debug_dialog.py、ui/state.py、pipeline/models.py、pipeline/config.py、
  pipeline/service.py、vendors/doubao_bot/models/automation.py、tests/test_pipeline.py、
  README.md、LOCAL_CHANGELOG.md
- 时间：2026-09-10

## v0.1.9.4

- 当前本地 tag：v0.1.9.3
- 修改内容：移除合并完成后的 docx 内嵌图水印复核。该复核与阶段 2 的逐图复核
  重复（成稿合并只做压缩与渲染、不改变像素），每篇额外耗时约 30 秒：
  1. pipeline/service.py：单文档与配图模式的 _run_merge 不再调用复核，直接返回
     合并结果；删除 _verify_final_images() 方法本体，以及「检出残留即抛错 /
     开关关闭仅打提示日志」两个分支。
  2. 移除配置项 final_verify_enabled：pipeline/models.py、pipeline/config.py
     DEFAULTS、ui/state.py（保存键列表、tk 变量、build_config）、
     ui/debug_dialog.py 的「最终稿复核」复选框。旧 settings.json 中残留该键会被
     忽略（读取走 defaults 兜底，无需迁移）。
  3. tests/test_optim_m0_m8.py：原「最终稿复核开关关闭跳过复核」用例改为
     「合并后不再复核」，断言日志中无最终稿复核耗时、且复核入口已不存在。
  4. 文档同步：docs/watermark_removal_flow.md 删除「交付兜底复核」章节与流程图
     节点，防漏擦要点改为说明不做二次复核的原因；docs/README.md 摘要同步；
     文档内 pipeline/service.py 行号引用按改动后的实际行数全部重新核对。
- 涉及模块：pipeline/service.py、pipeline/models.py、pipeline/config.py、ui/state.py、
  ui/debug_dialog.py、tests/test_optim_m0_m8.py、docs/watermark_removal_flow.md、
  docs/README.md、LOCAL_CHANGELOG.md
- 时间：2026-09-10

## v0.1.9.3

- 当前本地 tag：v0.1.9.2
- 修改内容：新增流程文档（docs/），梳理阶段 1「豆包生成图片」与阶段 2「去除水印」
  的实现流程，便于对照代码与后续维护：
  1. docs/doubao_generation_flow.md：应用层入口（单文档 / 配图模式）、冷却检查与
     浏览器启动、对话定位、提示词提交与基线快照、等图收集（完成信号 + 收尾缓冲 +
     DOM 兜底 + 空等快失败）、三种下载模式分派、防漏图设计要点。
  2. docs/watermark_removal_flow.md：引擎选择、豆包定点锚点识别（左上优先命中即止、
     六级增强链、零外扩紧裁剪）、掩码构建（按字数羽化 / 方框 / 红色水印特判）、
     lama 擦除、复核闭环与升级重擦、交付兜底复核、防漏擦设计要点。
  3. docs/README.md 文档索引；README.md 新增「流程文档」入口。
  两份文档均含 Mermaid 流程图、文本流程图、分步说明、关键参数表与代码索引，
  文中代码位置（文件:行号）已逐条核对。
- 涉及模块：docs/doubao_generation_flow.md（新增）、docs/watermark_removal_flow.md（新增）、
  docs/README.md（新增）、README.md、LOCAL_CHANGELOG.md
- 时间：2026-09-10

## v0.1.9.1

- 当前本地 tag：v0.1.9.0
- 修改内容：多账号主题路由 M0-M5 落地（规避封号：每账号独立登录态/代理/
  对话标题记忆/限额健康，与 legacy 单账号完全正交）：
  1. M0 账号注册表 accounts.json：版本化读写、字段规范化（非法限额防御）、
     upsert/remove/默认账号维护。
  2. M1 账号目录隔离：每账号独立 profile（登录态）、对话缓存、对话标题记忆
     （~/.doubao_bot/accounts/<id>/），空账号回退全局文件保持旧行为。
  3. M2 主题路由：主键「输入目录第一级子目录名」精确匹配（dir_name），按
     规则声明顺序命中、未命中回退 default_account；预留给标题关键词扩展。
  4. M3 限额与健康：每账号每日 ≤8 篇、连续 ≤4 篇后休息 20 分钟、连续失败
     3 篇当日暂停、跨天自动重置；失败信息命中风控/登录信号立即当日禁用。
  5. M4 每账号独立网络出口：DoubaoImageBot/浏览器启动透传 proxy
     （http/https/socks5），未配置走本机默认网络。
  6. M5 服务层串联：每篇解析账号归属并输出日志；跨文档切换账号先关闭旧
     浏览器会话再以新账号 profile/代理重建；对话标题按账号隔离（自动路由
     绝不套用其它账号/遗留标题，手动指定账号用用户输入标题并记忆）。
  7. 新增账号管理 CLI：python -m pipeline.accounts_cli（list/add/route/
     unroute/default/remove/status）；主界面「豆包对话标题」区新增账号下拉
     （刷新）+ 自动路由勾选，开始生成前自动同步注册表。
  8. 新增 tests/test_accounts.py（23 例）：注册表读写/规范化、dir_name 路由
     命中与回退、限额/休息/禁用/跨天重置、风控信号、账号记忆隔离、服务层
     标题切换与回写。全套 189 例通过。
- 涉及模块：pipeline/accounts.py（新增）、pipeline/accounts_cli.py（新增）、
  pipeline/config.py、pipeline/models.py、pipeline/service.py、ui/state.py、
  ui/main_window.py、vendors/doubao_bot/models/automation.py、
  vendors/doubao_bot/models/browser.py、tests/test_accounts.py（新增）、
  README.md、LOCAL_CHANGELOG.md
- 时间：2026-09-09

## v0.1.8.2

- 当前本地 tag：v0.1.8.1
- 修改内容：豆包定点引擎识别顺序改为「左上优先、命中即止」：
  1. 左上与右下水印在豆包成品图中不会并存，识别水印时先识别左上锚点，
     左上命中即提前结束整轮识别（不再识别右下，省一次锚点 OCR）；
     左上未命中才继续识别右下锚点。
  2. vendors/watermark_remove/services/detector.py detect_doubao_anchors：
     按 DOUBAO_ANCHORS_REL 顺序（左上 -> 右下）逐锚点识别，anchors=None
     全量识别时命中首个锚点即 break；anchors 子集（复核入口 M1）语义不变，
     复核/最终稿兜底仍只对命中的锚点或依次全量检查。
  3. 测试同步：tests/test_doubao_engine.py 原「两锚点共享目标各自独立命中」
     用例改为「左上命中即不再识别右下」+「左上未命中才识别右下」；
     tests/test_optim_m0_m8.py 新增左上命中终止用例。
- 涉及模块：vendors/watermark_remove/services/detector.py、
  tests/test_doubao_engine.py、tests/test_optim_m0_m8.py、LOCAL_CHANGELOG.md
- 时间：2026-09-07

## v0.1.8.1

- 当前本地 tag：v0.1.8.0
- 修改内容：耗时优化 M0-M8 落地（M3 GPU 设备项不执行）：
  1. M0 模块内子段耗时统计：单图「识别/擦除复核/保存」、整批「去水印内部合计」、
     合并「压缩/渲染」子段、最终稿 docx 内嵌图复核耗时日志（前缀 [耗时]），
     与既有模块级 stage_seconds 叠加可精确定位热点。
  2. M1 豆包定点引擎复核只覆盖实际擦除过的锚点：detect_doubao_anchors /
     verify_doubao_anchors 新增可选 anchors 参数；每轮先算 anchor 名，
     支持仅识别/复核指定锚点子集（未擦除过的干净锚点不再重复 OCR）。
  3. M2 首擦复核快速链：_region_ocr_chain 新增 max_levels 截断，
     豆包定点引擎首擦复核用快速链（1x/2x/2x+增强，3 级）判净即收，
     检出残留才升级掩码并走完整 6 级链严格复核；旧桩不支持新参数时自动回退
     完整链（_fn_accepts / _call_verify）。
  4. M4 图级并行去水印实验项：cfg.watermark_workers（默认 1=串行，需实测后
     再启用），并行保持输入顺序、首错整批抛出、进度按序发回。
  5. M5 PIL 压缩并行：compress_images 新增 workers（pipeline 合并阶段默认 4，
     compress_workers），线程池保持输入顺序、进度按完成数汇报，单张失败回退原图。
  6. M6 最终稿复核开关：cfg.final_verify_enabled（默认开）控制 docx 内嵌图
     OCR 二次确认，调试弹窗「去水印」分组新增勾选并持久化；关闭可省约
     25~30s/篇。
  7. M7 空等快失败 + 生成自动重试：DoubaoImageBot / wait_and_download /
     _wait_for_new_image_urls 支持 stall_timeout（无图且无完成信号时提前抛
     TimeoutError，默认 120s）；_generate_retry 与配图模式按
     cfg.generate_retries（默认 1=总 2 次尝试）自动重试异常/空图，
     封面缺失等点位级失败不重试语义保留。
  8. M8 批量限流自适应顺延：run() 篇间等待先探测豆包冷却文件剩余时间
     （_doubao_cooldown_remaining），冷却未结束则自动顺延到冷却窗口结束再补
     3 秒缓冲，不再固定 doc_delay；修复顺延后残留旧 doc_delay 双重等待问题。
  9. 新增 tests/test_optim_m0_m8.py（19 例）：锚点子集/快速链截断、服务级
     anchors+max_levels 接线、图级并行顺序、压缩并行顺序与进度、生成重试次数、
     stall_timeout 透传、冷却顺延、去水印/合并子段日志、最终稿复核开关。
- 涉及模块：pipeline/models.py、pipeline/config.py、pipeline/service.py、
  ui/state.py、ui/debug_dialog.py、vendors/doc_merger/core/compressor.py、
  vendors/doubao_bot/models/automation.py、
  vendors/doubao_bot/models/image_wait.py、
  vendors/watermark_remove/services/detector.py、
  tests/test_optim_m0_m8.py（新增）、LOCAL_CHANGELOG.md
- 时间：2026-09-07

# DocGenStudio 本地修改日志

## v0.1.7.2

- 当前本地 tag：v0.1.7.1
- 修改内容：新增各模块执行耗时统计（时间戳埋点）：
  1. ItemResult 新增 stage_seconds（生成/去水印/合并各阶段耗时，秒）与
     total_seconds（单篇总耗时，秒）字段，结果可直接被界面/脚本读取。
  2. pipeline/service.py 新增 _time_stage 计时埋点：豆包生成下载、去除水印
     （关闭时统计拷贝耗时）、文档图片合并（含最终稿内嵌图复核）三个阶段，
     各输出一条「模块[xx]：开始 → 结束，耗时 xx.xs」日志（前缀 [耗时]）。
  3. 每篇完成统一输出「[耗时] 单篇总耗时 xx.xs：生成 …、去水印 …、合并 …」；
     run() 结束后输出「[耗时] 批量总耗时 …s（含篇间等待）」；异常中断的模块
     也会记录已耗时，便于定位耗时热点与漏处理阶段。
  4. 新增 tests/test_pipeline.py TestStageTiming 与 tests/test_plan_pipeline.py
     TestPlanStageTiming：单篇成功 / 生成失败 / 关闭去水印的耗时字段与日志断言。
- 涉及模块：pipeline/models.py、pipeline/service.py、tests/test_pipeline.py、
  tests/test_plan_pipeline.py、LOCAL_CHANGELOG.md
- 时间：2026-09-07

## v0.1.7.1

- 当前本地 tag：v0.1.7.0
- 修改内容：水印去除改为「豆包专用定点引擎」（方案 B），旧实现整体保留可选：
  1. 新增引擎枚举与默认值：watermark_engine = doubao_fixed（默认，豆包专用定点）；
     full_scan（旧全图扫描引擎，保留可选）。pipeline/config.py 增加
     WATERMARK_ENGINE_* 常量，pipeline/models.py PipelineConfig 增加
     watermark_engine 字段，ui/state.py 持久化键 + build_config，调试弹窗「去水印」
     分组新增「水印引擎」下拉。
  2. 豆包定点引擎只识别/擦除左上「AI 生成」与右下「豆包AI生成」两个固定锚点
     （vendors/watermark_remove/config.py 新增 DOUBAO_ANCHORS_REL 归一化相对
     坐标、DOUBAO_ANCHOR_NAMES、DOUBAO_FEATHER_BY_TARGET 羽化映射），全程不做
     全图 OCR 扫描；WatermarkDetector 新增 detect_doubao_anchors /
     verify_doubao_anchors / _region_ocr_chain（区域级 1x->2x->2x+增强->3x+背景
     扣除->4x+红色提取->4x+CLAHE 增强链，命中即停）。
  3. pipeline/service.py：_remove_watermarks 按引擎分发检测/复核入口并输出引擎
     启用日志；_erase_watermarks_with_verify 支持按引擎口径复核（复核仍残留则
     升级掩码重擦，闭环与 M1-M4 一致）；_verify_final_images 最终稿内嵌图复核
     跟随引擎口径；自定义/旧版探测器缺少定点入口时自动回退全图口径（测试桩兼容）。
  4. 修复锚点 OCR 漏识别（588-东方朔 根因）：region OCR 默认外扩 8px 会把
     角部背景带进裁剪导致全盲，detect_region_text 新增 pad 参数（显式裁剪外扩，
     可为 0），豆包定点引擎对非 bg 增强级统一使用零外扩紧裁剪
     （DOUBAO_ANCHOR_PAD=0）；右下「豆包AI生成」OCR 常读出乱序/缺字
     （588 实测 "包AI生成豆"），每锚点接受双候选目标（targets）且两锚点
     互不按目标去重，消灭 OCR 顺序导致的历史漏擦。
  5. 新增 tests/test_doubao_engine.py：锚点常量与像素换算（2848x1600 ->
     20,40,340x150 / 2550,1500,285x90）、定点检测不调用 ocr_lines（mock 断言）、
     右下锚点命中/乱序文本副目标命中/双锚点去重解耦/无锚点文本不命中/复核
     同口径/压缩小图区域不越界/紧裁剪 pad=0、服务层引擎分发默认豆包定点与
     full_scan 可选、PipelineConfig 默认引擎一致性。
  6. 全量复跑验收（08-25/08-31/09-03 三期 originalImage，62 张 2848x1600 原图，
     内存复跑不落盘）：62/62 右下锚点全部命中并复核干净，61 张首擦即净、
     1 张升级重擦后通过、0 失败 0 漏网；历史漏擦样本 236 / 505 / 588 基图
     全部一次擦净；引擎默认 doubao_fixed，可在调试弹窗切回 full_scan。
- 涉及模块：pipeline/service.py、pipeline/config.py、pipeline/models.py、
  ui/state.py、ui/debug_dialog.py、vendors/watermark_remove/config.py、
  vendors/watermark_remove/services/detector.py、
  tests/test_doubao_engine.py（新增）、tests/test_watermark_verify.py、
  LOCAL_CHANGELOG.md
- 时间：2026-09-03

## v0.1.6.1

- 当前本地 tag：v0.1.6.0
- 修改内容：去水印「每次总有一张漏擦」根治——擦除后复核 + 升级重擦闭环（M1-M6）：
  1. 6 字水印「豆包AI生成」默认羽化 4 → 24px（505-口粮标准 实测 feather4/16 全图
     复核仍可读出水印、feather24 复核通过；取 24 为稳定值，仍低于 4 字水印的 36）。
  2. 新增擦除后复核 WatermarkDetector.verify（与检测同一识别口径，日志前缀 [复核]）。
  3. 复核仍残留时自动升级掩码重擦：build_escalated_mask 把检测框每边外扩并加大羽化
     （24/24 → 36/36 …），达到 WATERMARK_MAX_REPAINT=2 上限仍残留则该图报错、该篇
     不再进入合并（不再静默交付带水印图）。
  4. 配图模式豆包下载改到每篇独立临时目录，再按点位顺序迁入 originalImage，
     杜绝历史同名文件被下载器追加 (1) 后缀、旧水印图在 originalImage/ImageOutput
     累积串扰。
  5. 最终稿复核：合并后提取 docx 内嵌图逐张 OCR，仍检出残留即报错（_verify_final_images）。
  6. 新增 tests/test_watermark_verify.py：羽化默认值、升级掩码范围、verify 透传、
     服务层「升级一次后干净 / 达到上限整篇失败 / 首擦即净不升级」回归。
- 涉及模块：pipeline/service.py、vendors/watermark_remove/config.py、
  vendors/watermark_remove/services/{masks,detector,feather,batch}.py、
  tests/test_pipeline.py、tests/test_plan_pipeline.py、
  tests/test_watermark_verify.py（新增）、LOCAL_CHANGELOG.md
- 时间：2026-09-03

## v0.1.5.13

- 当前本地 tag：v0.1.5.12
- 修改内容：移除「配图（非封面）自动叠加文件名文字」功能：
  1. 该功能原为在去水印后、合并前把配图文件名绘制到图片上（水平居中、垂直
     画面高度 4/5 处、靠近底部）；用户已改为通过豆包提示词实现配图文字，
     不再需要代码叠加。
  2. 移除 pipeline/image_text.py（PIL/GDI+ 双后端渲染模块）、service.py 的
     阶段 2.5（_overlay_figure_text）与相关 import；tests/test_image_text.py
     删除，tests/test_plan_pipeline.py 回退叠加断言/GDI 强制 fixture/图片尺寸。
- 涉及模块：pipeline/service.py、pipeline/image_text.py（删除）、
  tests/test_image_text.py（删除）、tests/test_plan_pipeline.py、
  LOCAL_CHANGELOG.md
- 时间：2026-08-29

## v0.1.5.12

- 当前本地 tag：v0.1.5.11
- 修改内容：配图（非封面）自动叠加文件名文字（水平居中、垂直位于画面高度 4/5 处、
  靠近画面底部）：
  1. 需求：配图中的文字 = 配图文件名（去掉自动编号前缀 NNN-，即 image_keyword），
     文字水平居中、垂直位于画面高度五分之四（4/5）位置、靠近画面底部；封面图不叠加
     （封面文字规范为顶部 1/5，由豆包按提示词绘制）。
  2. 实现：去水印之后、合并之前新增阶段 2.5（_overlay_figure_text）；新增
     pipeline/image_text.py 提供 overlay_figure_text：PIL 进程内渲染优先（白色 +
     黑色描边），子进程探测到 PIL 渲染中文原生崩溃（部分 Pillow/FreeType 组合
     在 Windows 下渲染 CJK 字形访问违例）时自动回退 Windows GDI+（PowerShell
     System.Drawing）批量渲染，保证流水线不中断；可用环境变量
     DOCIMAGE_TEXT_BACKEND=pil|gdip 强制后端。文字块中心位于画面高度 4/5，
     超长文本自动换行/缩字号，横向不超过画面宽度 92%。
- 涉及模块：pipeline/image_text.py（新增）、pipeline/service.py（_run_one_plan
  阶段 2.5 + _overlay_figure_text）、tests/test_image_text.py（新增）、
  tests/test_plan_pipeline.py（全流程叠加断言 + 强制 GDI+ 后端）、
  LOCAL_CHANGELOG.md
- 时间：2026-08-29

## v0.1.5.11

- 当前本地 tag：v0.1.5.10
- 修改内容：配图说明 .md 支持新文档格式（兼容旧格式）：
  1. 新格式段标题「【配图N：对应小节：小节名——图片名】」与旧格式
     「【配图N：配图点：XXX】」统一解析；hint 保留小节名——图片名完整内容。
  2. 提交豆包的标题行去掉「对应小节：」（旧格式仍去掉「配图点：」）；
     图片文件名 = NNN-小节名——图片名。
- 涉及模块：pipeline/plan_reader.py（_POINT_HEADING_RE/_POINT_HEADING_STRIP_RE
  兼容两种格式）、tests/test_plan.py（新格式解析/标题行/文件名用例）、
  LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.10

- 当前本地 tag：v0.1.5.9
- 修改内容：修复最终稿封面图被合并两次（所有封面/配图只合并一次）：
  1. 根因：压缩配图开启时，cover_image 传的是去水印原图路径，而 images 是压缩
     后的同名文件；合并器按路径排除封面失败，压缩版封面进入 body 被 matcher
     再次插入，导致封面出现两次。
  2. 修复：merge_images_into_docx 按文件名归一化排除与封面同名的 body 图片；
     _merge_by_plan 压缩后把 cover_image 同步为压缩产物路径（文件名不变）。
- 涉及模块：vendors/doc_merger/core/docx_renderer.py（cover_names 排除）、
  pipeline/service.py（_merge_by_plan 压缩后同步 cover_image）、
  tests/test_plan_pipeline.py（同名封面去重 + 压缩同步两个回归用例）、
  LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.9

- 当前本地 tag：v0.1.5.8
- 修改内容：UI 输入框合并 + 弹窗高度调整：
  1. 「图片要求设定」与「配图全局要求」合并为一个共享输入框（第 2 区，标题改为
     「2. 图片要求设定 (提示词自定义要求，会放在输入内容前一行)」，去掉标题下
     的说明 Label）：选择
     单文档/批量文档生成时加载并保存「图片要求设定」数据（state.spec），选择
     单配图/批量配图生成时加载并保存「配图全局要求」数据（state.plan_prefix）；
     普通模式 ↔ 配图模式切换时先把当前输入保存回上一类别，再加载新类别内容。
  2. 去掉「豆包对话标题」输入框旁的「清空（新对话）」按钮。
  3. 「调试模式设置」弹窗：版权申明输入框高度由 3 行加大到 8 行，多行版权
     申明可直接完整显示；弹窗高度相应增加（min(reqheight+40, 屏幕高-40)）。
- 涉及模块：ui/main_window.py（_build_conv_section/_build_spec_section/
  _sync_mode_view/_load_spec_content/_on_spec_modified/_start）、
  ui/debug_dialog.py（滚动容器）、LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.8

- 当前本地 tag：v0.1.5.7
- 修改内容：豆包新建对话后回填「豆包对话标题」输入栏（所有文档生成模式一致）：
  1. 豆包前 5 个历史对话未命中而新建对话时，bot 会把新对话标题写入
     current_conversation_title；PipelineService.run() 每处理完一篇文档读取该值，
     若与当前配置不同则：更新 cfg.conversation_title（后续文档复用新对话，避免
     每篇重复新建）、持久化记忆文件、回调 UI 回填「豆包对话标题」输入框。
  2. 修复场景：单配图文档生成输入旧标题（如「赵合德与汉成帝的温柔乡」）未命中
     前 5 个历史对话而新建后，输入栏不再停留在旧标题。
- 涉及模块：pipeline/service.py（on_conversation_title 回调、_sync_conversation_title）、
  ui/main_window.py（_on_conversation_title 回填输入框）、tests/test_plan_pipeline.py
  （TestConversationTitleSync 两个用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.7

- 当前本地 tag：v0.1.5.6
- 修改内容：豆包对话标题匹配规则收紧（噪音过滤 + 精确匹配）：
  1. 读取侧边栏历史对话标题的噪音过滤正则新增「置顶」（原为 加载/展开/收起/
     更多/设置/新建/创建/返回/关闭），避免把「置顶」标签项当作对话标题；
     新建对话标题识别（按 /chat/<id> 反查侧边栏）同样剥离标题前的「置顶」前缀。
  2. 侧边栏定位对话由「精确 → 包含匹配 + 滚动加载更多历史」改为仅「精确匹配」，
     不再滚动加载；未命中时提示「清空对话标题使用第一个对话」。
- 涉及模块：vendors/doubao_bot/models/conversation.py（_FIRST_CONVERSATION_JS、
  _CURRENT_CONV_TITLE_JS、_locate_title、_find_conversation_in_sidebar 提示文案）、
  LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.6

- 当前本地 tag：v0.1.5.5
- 修改内容：配图模式文章 .docx 与 .md 同步生成三位编号 + 配图文件名改用编号：
  1. 配图模式下，关联文章 .docx（及其配图说明 .md）与「单文档生成」一致：无编号
     文档自动生成三位随机编号前缀 NNN-（.md 与 .docx 使用同一编号保持同名前缀；
     docx 已有编号时 .md 同步该编号），生图过程保留编号，最终稿去掉编号。
  2. 配图文件名由「配图N-配图点说明」改为「NNN-配图点说明」（封面=NNN-文章标题），
     matcher 的 image_keyword 自动剥离 NNN- 编号后按配图点说明插入对应段落。
- 涉及模块：pipeline/config.py（doc_number_prefix）、pipeline/service.py
  （_ensure_plan_numbered、_collect_documents 配图分支、_generate_by_plan 传编号）、
  pipeline/plan_reader.py（plan_image_stem 增加 number 参数）、
  tests/test_plan.py、tests/test_plan_pipeline.py、LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.5

- 当前本地 tag：v0.1.5.4
- 修改内容：配图模式提示词改回「原格式一次性提交」+ 图片命名规则调整 + 合并定位修复：
  1. 提交给豆包的提示词保留解析出的原格式标题行（【封面图要求】/【配图N：配图点：XXX】），
     仅去掉「配图点：」，按「标题行 + prompt」逐点位拼接，配图全局要求（首行）+ 全部
     点位一次性提交；不再把点位预览文本混入提交内容。
  2. 图片命名：封面图文件名 = 文章标题（不再加「封面-」前缀）；配图文件名 =
     「配图N-配图点说明」完整保留（不再 24 字截断，上限 80 字）。
  3. 合并器 merge_images_into_docx 新增 cover_image 显式参数，封面文件名=文章标题
     时仍能识别封面并插到首个标题1之后；配图说明文字只对正文配图生成。
  4. 修复真实 docx 合并定位：原文段落间通常没有空段落，原按空行分块会把整篇正文
     并成一个块，导致所有配图插到文末；改为每个非空段落独立成块，matcher 可把
     配图插到最相关内容段落之后。
- 涉及模块：pipeline/plan_reader.py（heading 字段、plan_image_stem/plan_point_heading、
  PLAN_IMAGE_KW_MAX=80）、pipeline/service.py（_generate_by_plan 拼接、_merge_by_plan
  传 cover_image）、vendors/doc_merger/core/docx_renderer.py（cover_image 参数、
  _split_paragraph_blocks 单段落分块）、tests/test_plan.py、tests/test_plan_pipeline.py、
  LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.4

- 当前本地 tag：v0.1.5.3
- 修改内容：配图模式改为「全部点位提示词一次性提交」：
  1. 原来每个配图点位单独调用一次豆包 run()（对话标题相同但交互次数多）；
     现在「配图全局要求（首行）+ 全部点位提示词」拼接成一条完整提示词一次性
     提交豆包，豆包按顺序生成全部图片。
  2. 返回图片按顺序对应点位（第 1 张=封面/第 1 个点位），统一重命名为
     「封面-…」「配图N-配图点」；无图时整次重试 1 次；封面缺失整篇失败，
     正文点位缺失跳过该点位；豆包多生成的图片（多于点位）自动删除。
  3. 一次性提交后配图模式与普通模式行为完全一致：name_prefix=文档名、
     conversation_title 同源传递，「豆包对话标题逻辑在各模式间一致」。
- 涉及模块：pipeline/service.py（_generate_by_plan 重构、移除 _run_point）、
  tests/test_plan_pipeline.py（FakePlanBot 改为一次多图 + 失败次数模拟，新增
  一次性提交/重试/部分缺失/多余图清理用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.3

- 当前本地 tag：v0.1.5.2
- 修改内容：配图模式「配图全局要求」输入框不再显示点位预览 + 模式按钮单行排列：
  1. 配图模式下「配图全局要求」输入框只显示/持久化用户输入的内容（不再自动填充
     点位预览文本），首次使用默认填入平台适配要求（图片适配平台：头条、公众号、
     小红书历史图文… 格式：16:9；封面文字水平居中靠顶、配图左上/右下无文字）。
  2. 提交时每个点位提示词 = 全局要求（首行）+ 点位 prompt（沿用 compose_prompt
     拼接语义）。plan_reader.extract_plan_prefix 已随设计变更移除（不再需要）。
  3. 模式按钮合并为一行：「单文档生成 → 批量文档生成 → 单配图文档生成 → 批量配图生成」。
- 涉及模块：pipeline/config.py（DEFAULT_PLAN_PREFIX）、pipeline/plan_reader.py、
  ui/main_window.py、ui/state.py、tests/test_plan.py、tests/test_plan_pipeline.py、
  LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.2

- 当前本地 tag：v0.1.5.1
- 修改内容：配图模式「配图点位浏览」支持输入全局要求（与「图片要求设定」作用一致）：
  1. 配图模式下「配图点位浏览」输入栏由只读预览改为可输入：自动填充点位预览，
     用户在预览内容之前输入的内容作为全局要求（plan_prefix），持久化记忆，
     重新选择文档/重启应用后自动带出。
  2. 提交时每个点位提示词 = 全局要求（首行）+ 点位 prompt（复用 compose_prompt
     拼接语义），再一起输入到浏览器豆包网页。
  3. plan_reader.extract_plan_prefix 提取「自动点位预览文本之前」的用户输入；
     pipeline/models.py 新增 plan_prefix 字段；ui/state.py 持久化。
- 涉及模块：pipeline/plan_reader.py、pipeline/models.py、pipeline/service.py、
  ui/main_window.py、ui/state.py、tests/test_plan.py、tests/test_plan_pipeline.py、
  LOCAL_CHANGELOG.md
- 时间：2026-08-28

## v0.1.5.1

- 当前本地 tag：v0.1.5.0
- 修改内容：DeepseekArticleGen × DocGenStudio 串联（M1~M7 配图说明文档生成模式）：
  1. 新增「单配图文档生成 / 批量配图生成」两个模式（pipeline/models.py 新增 mode
     plan_single/plan_batch 及 plan_doc_path/plan_input_dir/plan_cover_enabled；
     ui/main_window.py 模式行新增两个单选，配图模式置灰「图片要求设定」并显示
     配图点位只读预览；ui/state.py 持久化新字段）。
  2. 新增 pipeline/plan_reader.py：解析「{标题}_封面配图提示词.md」（兼容 __ 双下划线），
     提取【封面图要求】为封面点位、【配图N：配图点：XXX】为正文点位，并按同目录同名前缀
     关联文章 .docx（兼容 NNN- 编号前缀）。
  3. 图片命名串联：点位图按「配图N-配图点」「封面-提示词前12字」命名，matcher 按
     文件名关键字自动定位插入段落（vendors/doc_merger/core/image_filename.py 正则
     扩展支持「配图N-」前缀）。
  4. pipeline/service.py 配图分支：按点位逐个调用豆包生成（封面失败整篇失败；
     正文点位失败重试 1 次后跳过；每点位仅保留第 1 张），复用去水印流程，
     再通过新增 merge_images_into_docx 把去水印图合并进已有文章 .docx
     （保留原文富文本样式；封面图固定插到首个标题1段落后；最终稿固定 docx 格式）。
- 涉及模块：pipeline/plan_reader.py、pipeline/config.py、pipeline/models.py、
  pipeline/service.py、ui/main_window.py、ui/state.py、
  vendors/doc_merger/core/docx_renderer.py、vendors/doc_merger/core/image_filename.py、
  tests/test_plan.py、tests/test_plan_pipeline.py、LOCAL_CHANGELOG.md
- 时间：2026-08-27

## v0.1.4.2

- 当前本地 tag：v0.1.4.1
- 修改内容：修复「浅暖色背景大块 + 深色水印文字漏擦」（236-皇帝的母亲居然二婚？汉朝皇室为何盛产私生子？.png 右下角"豆包AI生成"水印未擦除，588-东方朔 同根因一并受益）：
  1. 根因：水印是深色笔画文字，叠在覆盖检测框的暖色/红褐背景大块上。上一版按「红:暗 数量比 ≥3」判红色为背景，但 236 红色占比约 20% 且为浅暖色（灰度中位 180），深色文字占比亦高，数量比判据不适用；红色分支只覆盖红+白描边，漏掉深色笔画 → 修复后残留。
  2. 新增 `_red_is_background_block`：取检测框内最大红色连通域，面积占比 ≥15% 且包围盒宽高覆盖 ≥80% 时判定红色为背景大块（236 红块面积 20%/bbox 100%x100%，588 面积 40%/bbox 86%x100%，均触发；69 号图红色水印笔画面积约 2%/bbox 31%x79% 不触发，保护背景正文）。判定在检测框区域内进行（`_stroke_mask_from_crop` 新增 `box_region` 参数），避免外扩裁剪稀释占比。
  3. 判为红色背景时叠加「灰度 <110」深色笔画掩码，并对掩码内暗分量做 3px 膨胀（`DARK_STROKE_DILATE_K=7`）：直接叠加整片暗色时 lama 对暗笔画边缘仍残留半透明暗色（236 实测残留 4510 像素），膨胀 3px 后降至约 1359（其中约 1210 为原图暗色背景内容）；588 旧版残留 485 → 261。
- 涉及模块：vendors/watermark_remove/services/masks.py、tests/test_masks.py（掩码用例断言增强）、LOCAL_CHANGELOG.md
- 时间：2026-08-27

## v0.1.4.1

- 当前本地 tag：v0.1.4.0
- 修改内容：原图Http 直连失败原因分析与运行日志增强：
  1. 根因（依据 2026-08-26 pipeline.log 实测）：豆包 CDN 现在给页面 <img> 的 URL 是
     `~tplv-...-i_pre_wm_16_dk.png` 带水印处理图，其 `x-signature`/`x-expires` 签名绑定
     该处理路径；`to_original_url` 去掉 `~tplv-` 还原出无后缀原图 URL 后，签名与路径
     不匹配，直连 100% 返回 HTTP 403（CDN 鉴权失败：签名已过期或防盗链拦截）。
     因此 original_http 模式直连必然失败，全部转入「点击下载原图」按钮方案（按钮
     拦截到的 `~tplv-...-i_dld_wm_16_dk.png` 无水印原图 URL 可直连 200，6997KB）。
  2. `_download`（download_http.py）在原图Http 模式（prefer_browse=False 且
     allow_fallback=False）下，单图失败（HTTP 错误/网络异常/体积过小）统一输出
     `[错误]原图http 下载失败原因：{describe()}` 日志，含 HTTP 状态码、原因与 URL；
     浏览图模式日志保持普通格式。
- 涉及模块：vendors/doubao_bot/models/download_http.py、tests/test_download_fix.py（新增 2 用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-27

## v0.1.3.1

- 当前本地 tag：v0.1.3.0
- 修改内容：修复「红褐背景上深色水印文字漏擦」（588-东方朔图右下角"豆包AI生成"水印未擦除）：
  1. 根因：水印是深色笔画文字，但检测框内红色像素占比 47%（图片红褐背景），`_has_red_watermark_region` 判为红色水印、改走笔画掩码；红色分支 `watermark_stroke_mask` 只提取红色+白色描边，深色水印笔画未被覆盖 → 修复后残留。
  2. `_stroke_mask_from_crop` 红色分支新增深色笔画兜底：红色像素数超过深色像素 3 倍时（588 实测红:暗≈8:1，红色为背景、深色才是水印），叠加灰度 <110 的深色笔画掩码，水印文字覆盖率 1/886 → 886/886；69 号图（红色水印+深色背景正文，红:暗≈1:2.4）不受影响，仍只覆盖红+白描边保护背后正文。
- 涉及模块：vendors/watermark_remove/services/masks.py、tests/test_masks.py（新增 2 用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-26

## v0.1.2.1

- 当前本地 tag：v0.1.2.0
- 修改内容：无数字编号的文档自动添加三位随机编号前缀 `NNN-`（000~999，无中括号），已带编号（如 `88-`、`[88]-`）的文档保持不变：
  1. `pipeline/config.py` 新增 `ensure_doc_number`（无编号文档物理重命名为 `NNN-文档名`，目标重名时重新随机）与 `strip_doc_number`（最终稿去掉恰好三位的自动编号前缀，两位已有编号如 `88-` 保留）。
  2. `pipeline/service.py` `_collect_documents`（单篇与批量）对无编号文档自动编号；`_run_one` 最终稿文件名去掉 `NNN-`（生图过程 doc.stem 保留编号，图片命名、压缩目录均带编号）。
  3. `naming.py` 编号前缀放宽到三位数（000-999），`build_names` 图片名保留 `NNN-` 前缀；`batch.py` `doc_number` 支持 `NNN-`/`[NNN]-` 格式参与自然排序。
- 涉及模块：pipeline/config.py、pipeline/service.py、vendors/doubao_bot/models/naming.py、vendors/doc_merger/core/batch.py、tests/test_pipeline.py（新增 8 用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-23

## v0.1.1.6

- 当前本地 tag：v0.1.1.0
- 修改内容：合并后的最终稿 docx 第一行（文章标题）固定设置为 Word「标题1」（Heading 1）样式。此前第一行若是 Markdown 标题会用 Title（大标题）样式，若源文档为 .docx 解析出的纯文本标题则被渲染成普通段落；现在无论第一行是否带 `#` 标记，统一剥离标记并设为「标题1」，后续 Markdown 标题仍按级别映射 Heading 2~6。
- 涉及模块：vendors/doc_merger/core/docx_renderer.py、tests/test_pipeline.py（新增 3 用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-23

## v0.1.1.5

- 当前本地 tag：v0.1.1.0
- 修改内容：按用户明确需求校正下载模式行为（此前 `original_http` 会混入浏览图）：
  - `original_http`：仅通过 HTTP 直连下载原图；原图 URL 直连失败（`~tplv-` 还原 403）时转「original」方案——点击豆包「下载原图」按钮获取原图文件/URL，不再回退下载页面处理图（浏览图/`i_pre_wm` 高清处理图）。
  - `browse`：通过 HTTP 只下载浏览图（页面处理图），不点按钮、不还原原图 URL。
  - `original`：通过点击豆包「下载原图」按钮下载原图。
  根因：`_download_original_http` 的 1.5 步在直连失败后以 `prefer_browse=True` 回退下载页面高清处理图，导致一批图里既有原图又有浏览图。已删除该回退分支。
- 涉及模块：vendors/doubao_bot/models/automation.py、tests/test_download_fix.py（新增 2 用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-23

## v0.1.1.4

- 当前本地 tag：v0.1.1.0
- 修改内容：豆包下载原图不再平铺在源文档根目录，统一保存到源文档根目录下 `originalImage` 目录（新增常量 `ORIGINAL_SUBDIR`）。去水印覆盖模式仍在 `originalImage` 内覆盖原位；非覆盖模式仍输出到源文档根目录 `ImageOutput`（位置不变，兼容既有约定）。另核查 `generate_docs.py` 疑问：该文件不是本流水线产物（项目代码无任何生成它的逻辑），为专栏 docx 排版脚本（`OUT_DIR` 硬编码指向用户工作目录），由用户/其他工具手动放置。
- 涉及模块：pipeline/config.py、pipeline/service.py、tests/test_pipeline.py、LOCAL_CHANGELOG.md
- 时间：2026-08-23

## v0.1.1.3

- 当前本地 tag：v0.1.1.0
- 修改内容：修复「刚开启生成，豆包网页却打开历史对话并输入/显示『帮我整理兰陵王相关的历史文献资料』」问题。排查结论：不是测试脚本引入（生产代码与测试均无该文案）；该文字来自浏览器持久化 profile 中豆包网页的历史对话（`~/.doubao_bot/profile/Default/History` 可查）。根因：`launch_persistent_context` 会恢复上次关闭时的页面，若上次停留在用户手动打开过的历史对话页（URL 匹配 `/chat/<id>`），旧版 `run()` 直接走「已处于目标对话中，直接继续」分支，跳过对话标题匹配，把本次提示词发进错误历史对话（污染历史会话，且页面显示历史对话标题造成误读）。修复三处：
  1. `conversation.py` 新增公开方法 `detect_current_conversation_title`：按当前 URL `/chat/<id>` 反查侧边栏对话项标题（只读不改 URL）。
  2. `automation.py` 把对话定位逻辑抽取为 `_select_conversation`：当已在 `/chat/<id>` 页时先核对当前对话标题与用户指定标题，一致才直接继续；不一致（浏览器恢复残留会话）则重新走「前 5 个历史对话匹配 → 打开目标对话 / 新建对话」，杜绝发错会话。
  3. `prompt_writer.py` 输入框清空加固：Ctrl+A+Delete 之后再用 JS 兜底清空 textarea/contenteditable 内容并派发 input 事件，防止豆包草稿恢复或全选失效导致「旧草稿 + 新提示词」拼接发送。
- 涉及模块：vendors/doubao_bot/models/automation.py、vendors/doubao_bot/models/conversation.py、vendors/doubao_bot/models/prompt_writer.py、tests/test_conversation_select.py（新增 8 用例）、LOCAL_CHANGELOG.md
- 时间：2026-08-22

## v0.1.1.2

- 当前本地 tag：v0.1.1.0
- 修改内容：调试模式设置弹窗最下方新增「版权申明」输入框，非空时在最终交付稿（.md / .docx）末尾追加版权申明内容（支持多行，留空不追加）。两点细化需求：
  1. 版权申明不进豆包网页：仅通过合并链路追加到最终交付稿末尾，`compose_prompt` 只拼接「图片要求设定 + 正文」，不会把版权申明发送到浏览器豆包网页输入框。
  2. 交付稿不再重复添加「版权申明」标题：用户内容一般自带「【版权与内容声明】」标题，故 `.docx` 删除 `add_heading("版权申明")`，`.md` 同步删除 `## 版权申明` 标题（保留 `---` 分隔线），仅输出用户输入的段落内容。
- 链路：`ui/debug_dialog.py` 输入框 ↔ `ui/state.py` 持久化（pipeline_settings.json）→ `PipelineConfig.copyright` → `MergeConfig.copyright` → `md_renderer` / `docx_renderer` 文末追加。
- 涉及模块：ui/debug_dialog.py、ui/state.py、pipeline/models.py、pipeline/config.py、pipeline/service.py、vendors/doc_merger/core/models.py、vendors/doc_merger/core/service.py、vendors/doc_merger/core/md_renderer.py、vendors/doc_merger/core/docx_renderer.py、tests/test_pipeline.py、LOCAL_CHANGELOG.md
- 时间：2026-08-22

## v0.1.1.1

- 当前本地 tag：v0.1.1.0
- 修改内容：修复「合并工程后原图Http 下载功能不正常」问题。根因：豆包 <img> 只加载 `~tplv-` 处理图，其签名（x-signature）绑定处理路径，`to_original_url` 还原成无 `~tplv-` 的 URL 后请求必然 403（实测无论 Referer/UA 都 403）；而处理图 URL（`i_pre_wm` / `i_dld_wm`）可直接 HTTP 200 下载且为 2848x1600 原图级。修复三处：
  1. `automation.py` `_download_original_http`：还原 URL 直连失败后回退 HTTP 直连页面高清处理图 URL（`i_pre_wm`），不再空转跳过、全依赖按钮兜底。
  2. `download_button.py` 3a 分支：允许 `i_dld_wm` 下载专用处理图 URL 走 HTTP 直连（此前被 `"~tplv-" not in u` 过滤掉，只能等浏览器下载事件）。
  3. `image_utils.py`：清理合并工程时产生的重复半截函数定义（`_pick_best_url` / `image_identity` / `_extract_image_id` 各出现两次，第一份 `_extract_image_id` 缺实现，靠第二份覆盖才未出错）。
- 涉及模块：vendors/doubao_bot/models/automation.py、vendors/doubao_bot/models/download_button.py、vendors/doubao_bot/models/image_utils.py、tests/test_download_fix.py、LOCAL_CHANGELOG.md
- 时间：2026-08-22

## v0.1.0.2

- 当前本地 tag：v0.1.0.1
- 修改内容：修复「批量生成时个别图片下方水印漏擦」问题。根因不在 lama 擦除模型，而在检测与掩码构建调度，共三处：
  1. `_find_rect_frame` 把水印左侧无关矩形误判为方框水印（78-咸阳一炬图，误检框与 OCR 文字框水平零重叠），掩码构建到错误区域导致水印原样保留。修复：方框候选必须与 OCR 文字框水平重叠 ≥50% 且宽度 ≥80%。
  2. `_has_red_watermark_region` 把图片内容中的少量红色元素误判为红色水印（78-咸阳一炬 两版图实测 1.2% 与 6.6%），full 策略被改道笔画掩码且笔画提取失败导致漏擦。修复：红色判定改为检测框内红色占比 ≥15%（真红色水印文字占比 40% 以上，可稳定区分）；`build_watermark_text_mask` 笔画覆盖率低于检测框 15% 时回退整框。
  3. `76-秦始皇为何举国尚黑` 图 OCR 全盲：全图扫描只识别出标题与「图一」，默认区域 5 级增强全部漏检，走「未检测到水印」分支原样输出。修复：`detect_watermarks` 默认区域兜底链增加第 6 级 4x 放大 + LAB 通道 CLAHE 局部对比度增强（`detect_region_text` 新增 `enhance="clahe"`），可稳定识别「豆包AI生成」。
- 涉及模块：vendors/watermark_remove/services/masks.py、vendors/watermark_remove/services/ocr.py、vendors/watermark_remove/services/detector.py、tests/test_masks.py、tests/test_ocr_clahe.py、LOCAL_CHANGELOG.md
- 时间：2026-08-22

## v0.1.0.1

- 当前本地 tag：v0.1.0.1
- 修改内容：修复 DocGenStudio 会话因连续 `view_image` 两张约 189 万字符 base64 大 PNG 导致 2642869 tokens 超限的问题。新增 AGENTS.md 图片查看规则；历史 `wm76_*.png` 归档到 `.debug_previews/raw/`；新增项目 `.codex/config.toml` 指向本地 guard `57322`；升级 vendored `token_guard.py` 按 base64 长度估算图片 token 并支持 `messages/input`。
- 涉及模块：AGENTS.md、.codex/config.toml、vendors/watermark_remove/services/token_guard.py、tests/test_token_guard.py、.gitignore、LOCAL_CHANGELOG.md
- 时间：2026-08-22
## v0.1.16.17
- 当前本地 tag：v0.1.16.17
- 修改内容：修复豆包固定对话标题未命中前 5 个对话、重复新建的问题。
  1. 侧边栏标题缓存无论调用方 limit 为多少都保留最多 5 条；`first_conversation_title()`
     不再把后续用于前 5 个匹配的缓存错误截成 1 条。
  2. 对话改名提交后立即失效标题缓存，下一篇会重新读取侧边栏并以固定标题命中复用。
  3. 新增回归测试覆盖 limit=1 后仍可在前 5 个匹配，以及改名后缓存失效。
  4. 每次生图提交时，在「图片要求设定 / 配图全局要求」后追加一行
     `【文章标题】{文章标题}`，覆盖普通单篇、批量、兼容批量和配图模式。
- 涉及模块：vendors/doubao_bot/models/conversation.py、docreader.py、batch.py、
  pipeline/service.py、tests/test_optim_c_plan_m5.py、test_conversation_select.py、
  test_optim_m0_m8.py、test_plan_pipeline.py、README.md、docs/doubao_generation_flow.md
- 时间：2026-09-28
## v0.1.21.3（开发中）
- 修改内容：设置简化第二阶段，把四个日常分组与「按篇数轮换」移出弹窗，改为配置文件维护。
  1. 设置弹窗移除「豆包生成 / 去水印 / 合并输出 / 批量文档生成」四个 LabelFrame 与「按篇数轮换」勾选框，只保留「调试与登录」（账号列表 + 调试开关）和「版权申明」；四个分组原有的等待秒数、下载模式、去水印开关、压缩质量、输出格式、递归扫描、失败策略等由 `Config/settings.config` 维护。
  2. `Config/settings.config` 为四个隐藏分组各加分组级中文注释（用途/修改方式/取值规则），并重新生成：豆包生成、去水印、合并输出、批量文档生成、调试与登录、高级配置、版权申明等分组顺序不变，每个 item 的中文注释与可输入值说明保留。
  3. `account_rotate`（按篇数轮换）保留在 XML 「调试与登录」分组，仅可在配置文件维护；`_enable_rotation_for_quota()` 在保存「每次生成篇数」> 0 时仍自动开启轮换，避免「设了配额却没生效」。
  4. 去掉账号列表下方的「设为默认账号」按钮，换默认账号统一走双击「默认账号」列（新增账号时仍自动设为默认）；去掉版权申明输入框下方「仅追加到最终交付稿末尾…」灰字 Label。
  5. 底层持久化、流水线行为不变：隐藏分组与轮换开关仍由 AppState 写入 XML 并在启动时恢复，不改变生成/去水印/合并结果。
- 涉及模块：ui/debug_dialog.py、pipeline/config.py、Config/settings.config、tests/test_settings_config.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05
## v0.1.21.4（开发中）
- 修改内容：将「调试模式」升级为完整设置窗口的展开开关。
  1. 设置弹窗改为可重建内容：默认精简（只显示「调试与登录」+「版权申明」）；勾选「调试模式（含详细日志）」后立即重建为包含全部配置项的完整窗口，恢复「豆包生成 / 去水印 / 合并输出 / 批量文档生成」四个分组与「按篇数轮换」勾选框；取消勾选回到精简窗口，窗口尺寸随内容自适应。
  2. 四个分组恢复原控件（等待秒数、下载模式、去水印开关与覆盖、配图名/压缩/质量/输出格式、递归扫描/失败策略），编辑即写入共享 state 与 Config/settings.config；不显示时仍由配置文件维护。
  3. 「按篇数轮换」勾选框只在调试模式下显示（account_rotate）；配置文件分组注释同步更新为「默认设置窗口已隐藏；开启调试模式后弹窗会显示全部配置项」。
  4. 上轮明确删除的「设为默认账号」按钮与版权申明灰字提示保持移除（换默认账号走双击「默认账号」列，新增账号时自动设为默认）。
  5. 新增 debug_mode 变量监听（切完整 / 精简窗口）与销毁时监听清理，避免弹窗销毁后旧回调引用已销毁控件。
- 涉及模块：ui/debug_dialog.py、pipeline/config.py、Config/settings.config、tests/test_settings_config.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05
## v0.1.21.5
- 当前本地 tag：v0.1.21.5
- 修改内容：调试模式（完整窗口）按「简化第一阶段之前」的版本还原全部配置项。
  1. 豆包生成：补回「冷却秒数」（cooldown_seconds）与「文字输入慢动作ms」（slow_mo）。
  2. 去水印：补回「旧掩码策略」（mask_strategy）、「羽化值」（feather）、「强制左上方去水印」（force_top_left_remove）、「水印引擎」（watermark_engine）、「擦除内核」（watermark_pipeline）、「SS 掩码 / Alpha 反解 / 背景快路径 / 掩码细化」（ss_*），并把「启用自动去水印」文案恢复为简化前版本。
  3. 合并输出：补回「覆盖源文档」（overwrite_source）与「合并后删除原始图片」（delete_images）。
  4. 批量文档生成：补回「文档间隔秒数」（doc_delay）。
  5. 调试与登录：补回「账号切换等待秒数」（account_switch_wait）与「设为默认账号」按钮；账号行仍支持双击「默认账号」列换默认。
  6. 不恢复旧的「download_mode != browse 就强制清空 force_top_left_remove 并删除 XML 键」联动（v0.1.21.1 认定为缺陷），避免打开设置时清掉手工填写的配置值。
  7. 精简窗口（调试模式关闭）行为不变，仍只显示「调试与登录」+「版权申明」；高级项在重启前已构建在调试专属容器中，切换时只做显示/隐藏，不销毁控件。
  8. 配置文件「高级配置」分组注释补充「勾选调试模式后这些选项会随完整窗口恢复显示」。
- 涉及模块：ui/debug_dialog.py、pipeline/config.py、Config/settings.config、tests/test_settings_config.py、README.md、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05

## v0.1.22.1
- 当前本地 tag：v0.1.22.1
- 修改内容：主界面分组标题文案调整。
  1. 「4. 启动和设置」改为「3. 启动和设置」：v0.1.16.9 去掉「3. 输入文档」分组框后编号断档，恢复连续编号。
  2. 「2. 输入文档/目录选择（.md/.docx；配图模式选择配图说明 .md）」改为「2. 待生成文档列表」。
- 涉及模块：ui/main_window.py、LOCAL_CHANGELOG.md
- 时间：2026-10-05

## v0.1.22.2
- 当前本地 tag：v0.1.22.2
- 修改内容：修主界面「2. 待生成文档列表」与「3. 启动和设置」之间的空隙，并让两组高度联动。
  1. 「2. 待生成文档列表」分组与其中的列表容器改为 fill=both + expand，成为上半 pane 唯一的弹性分组：拖分隔条时列表高度随之增减，与下方「3. 启动和设置」联动，两组之间不再留空白。
  2. 分隔条恢复/持久化去掉「上半不高于内容高度」的旧上限（分组 2 固定高度时代用来防空白的），现在只保证下半 pane ≥ _MIN_BOTTOM_PANE_HEIGHT，所以用户拖大的列表高度可以保存并在下次启动恢复。
  3. 自愈逻辑 _ensure_top_pane_visible 只在「上半 < _MIN_TOP_PANE_HEIGHT」被压塌时把分隔条拉回内容高度，不再纠正「上半 > 内容高度」。
  4. 回归测试：新增弹性布局断言与真实窗口几何断言（拖高后列表底边离上半 pane 底边只剩内边距）；更新原「上半不得高于内容」的两条旧断言。
- 涉及模块：ui/main_window.py、tests/test_pending_articles.py、LOCAL_CHANGELOG.md
- 时间：2026-10-05

## v0.1.22.3
- 当前本地 tag：v0.1.22.3
- 修改内容：主界面模式入口与分组标题调整。
  1. 去掉「单文档生成」「单配图文档生成」两个入口，只保留「文档生成」（batch）与「配图生成」（plan_batch）。mode 本就不持久化、启动固定 plan_batch；旧 single / plan_single 路径仅在服务层与兼容调用方保留（服务层单篇测试继续覆盖），主界面不再暴露。
  2. 「批量文档生成」改为「文档生成」，「批量配图生成」改为「配图生成」。
  3. 四个分组标题去掉编号：「文档生成模式」「图片要求设定…」「待生成文档列表」「启动和设置（原 3.）」。
  4. README 功能列表与轮询说明同步新名称；代码注释里残留的旧编号一并对齐。
  5. 新增 UI 回归测试：真实窗口里不再出现旧模式名与带编号分组标题，两个单选仍分别绑定 batch / plan_batch。
- 涉及模块：ui/main_window.py、ui/state.py、tests/test_pending_articles.py、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05

## v0.1.22.4
- 当前本地 tag：v0.1.22.4
- 修改内容：按标准 MVC 重构 UI 层，拆分视图与控制器，清理死代码。
  1. 新增 `ui/views/main_sections.py`（`MainSectionsView`）：四个分区（文档生成模式 / 图片要求设定 / 待生成文档列表 / 启动和设置）的纯控件构建从主窗口抽出，视图层不再含业务判断。
  2. 新增 `ui/controllers/` 控制器层：`base.Controller` 基类 + 日志（`log_controller`）、分隔条（`sash_controller`）、待生成列表（`pending_articles_controller`）、目录轮询（`poller_controller`）、流水线启停（`pipeline_controller`）五个控制器；每个控制器只通过 `self.win` 访问视图与状态，彼此不互相 import。
  3. 新增 `ui/modes.py` 共用模式常量（`MODE_*` / `PLAN_MODES`），让视图与控制器无需反向 import `ui.main_window`，防止循环导入。
  4. `ui/main_window.py` 由约 1500 行降为约 640 行的「组合根」：只装配 PanedWindow、持有 `AppState`、惰性创建五个控制器，并保留全部历史私有方法名与类常量做薄转发（测试与旧调用方零改动）。
  5. 删除死代码：用户否决且无引用的 `ui/widgets/`（Switch 控件）、无引用的 `vendors/doubao_bot/models/batch_scanner.py` 与 `runtime.py`，并从 `models/__init__.py` 移出对应导出。
  6. 文档同步：`docs/ARCHITECTURE.md` 改为 MVC 总览与单向依赖图，README 架构树补充 views / controllers；模块文件头 docstring 补齐职责 / 依赖 / 对外 API。
  7. 行为不变：真实窗口几何、分隔条持久化、日志分类、轮询生命周期、待生成列表刷新与移除、流水线启停、模式切换记忆回填均与重构前一致；全量 601 项测试通过。
- 涉及模块：ui/main_window.py、ui/modes.py、ui/views/、ui/controllers/、vendors/doubao_bot/models/__init__.py、docs/ARCHITECTURE.md、README.md、LOCAL_CHANGELOG.md
- 时间：2026-10-05
## v0.1.23.2（开发中）
- 修改内容：按「Doc 识别/复核 + SS 掩码/Alpha/快路径/LaMa」推荐方案补齐唯一缺口——可切换的擦除推理后端（lama / lama-onnx / migan）。
  1. 新增 `vendors/watermark_remove/services/inpaint_backends.py`：`create_inpainter()` / `get_inpainter()` 后端工厂，按名称选择并做可用性探测，模型或依赖缺失时自动回退 torch 版 lama。
  2. 新增 `services/lama_onnx.py`：onnxruntime 版 LaMa 后端（对称填充到 8 的倍数 + NCHW 预处理 + 裁剪后处理），与 torch 版数值口径对齐。
  3. 新增 `services/migan.py`：MI-GAN 轻量后端适配与能力探测（IOPaint 1.6.0 已移除 migan，不支持时回退 lama）。
  4. `services/inpaint.py`：`get_manager()` 支持按模型名/设备重建管理器；新增 `LamaInpainter` 使后端统一为 `available()` + `inpaint()` 协议。
  5. `services/pipeline_inpaint.py`：`hybrid_inpaint()` 新增 `backend` 参数；默认 lama 路径保持原有裸 LaMa 调用，行为不变。
  6. 配置：`vendors/watermark_remove/config.py` 新增 `INPAINT_BACKEND` / `ONNX_MODEL_PATH`；应用层新增 `ss_inpaint_backend`（默认 lama，写入 `Config/settings.config` 高级分组），`pipeline/service.py` 新增 `_ss_inpaint_backend()` 归一化透传。
  7. 新增 `tests/test_inpaint_backend.py`（后端归一化、回退、ONNX 预处理/后处理、`hybrid_inpaint` 分派、服务层透传）。
  8. `requirements.txt` 标注可选依赖 `onnxruntime`（默认后端不装也可运行）。
- 涉及模块：vendors/watermark_remove/config.py、vendors/watermark_remove/services/inpaint_backends.py、vendors/watermark_remove/services/lama_onnx.py、vendors/watermark_remove/services/migan.py、vendors/watermark_remove/services/inpaint.py、vendors/watermark_remove/services/pipeline_inpaint.py、vendors/watermark_remove/services/__init__.py、pipeline/config.py、pipeline/models.py、pipeline/service.py、requirements.txt、docs/watermark_removal_flow.md、tests/test_inpaint_backend.py、LOCAL_CHANGELOG.md
- 时间：2026-10-06
## v0.1.23.3（开发中）
- 修改内容：把图片下载阶段的运行日志简化为「开始 → 逐张成功（含 URL）→ 汇总」三段式。
  1. `vendors/doubao_bot/models/automation.py`：新增 `_DOWNLOAD_MODE_LABELS` 模式文案表；`wait_and_download()` 开始时输出一行「开始下载图片，当前下载模式=…」，结束时用 `try/finally` 统一输出「N张图片成功下载，M张图片下载失败。耗时：x.x s」，保证中途报错/取消也能写汇总；删除旧的 `wait_and_download:` 前缀与「完成 X/Y 张」文案。
  2. `vendors/doubao_bot/models/download_http.py`：`_download()` 的批次开始/汇总/URL 明细改走详细日志，并在逐张成功时输出运行日志「第N张图片下载成功，url：…」；新增 `log_success` 开关，供上层回退路径复用而不重复计数。
  3. `vendors/doubao_bot/models/download_button.py`：按钮方案开始行改走详细日志；按钮成功与 HTTP 回退成功统一输出「第N张图片下载成功，url：…」。
  4. 新增 `tests/test_download_logging.py`：覆盖开始/逐张/汇总三段式、异常时仍出汇总、按钮回退与 `log_success` 关闭等场景。
- 涉及模块：vendors/doubao_bot/models/automation.py、vendors/doubao_bot/models/download_http.py、vendors/doubao_bot/models/download_button.py、tests/test_download_logging.py、docs/doubao_generation_flow.md、LOCAL_CHANGELOG.md
- 时间：2026-10-06
## v0.5.0.8（2026-10-23）
- 远程发布前保存工作区配置：更新配图提示词、选题去重要求、民生政策解读输出目录以及界面配置；归档现有批量图文生成计划。
- 验证：4 个变更配置文件 XML 解析通过，`git diff --check` 通过。

## v0.5.2.1（2026-10-23）
- 修改内容：新增独立 HTML 交互原型，演示 AI 深度图文生成的原标题筛选与核心立意获取两个步骤，支持分类为空、手动主题、数量不足、空结果与失败状态。
- 范围：仅 design/ai-deep-article-prototype；尚未接入应用、数据库或 API，等待用户审核。
- 验证：浏览器验证两步跳转、原标题选择、切换清空旧立意与部分返回提示；内联 JavaScript 语法检查通过。

