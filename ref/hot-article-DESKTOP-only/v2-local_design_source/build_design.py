"""Build one declarative Windows design source for HTML review and editable Figma import.

This is a design artifact, deliberately independent of the production Tkinter workspace.
Run: python design/hot-article-windows/build_design.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKENS = {
    "canvas": "#F3F6F6", "surface": "#FFFFFF", "subtle": "#F7F9F9",
    "ink": "#162B2A", "secondary": "#4C605D", "muted": "#5D706C",
    "border": "#D5DEDC", "accent": "#197D72", "accentHover": "#136B62",
    "accentSoft": "#E9F4F0", "rail": "#102A27", "railActive": "#20564D",
    "railText": "#F5FBF9", "railSecondary": "#BBD2CB", "success": "#176C50",
    "successSoft": "#EAF5EF", "warning": "#80530D", "warningSoft": "#FFF5DF",
    "error": "#A82935", "errorSoft": "#FCEEF0", "focus": "#0067C0",
}
SCREENS: list[dict] = []
TITLE = "公共健身设施建成后，后续管护如何跟上"
IDEA = "公共服务的价值不仅在于建成数量，更在于持续可用；维护责任、预算与反馈闭环需要一同落地。"
STYLE = "从标题中的具体细节进入，用生活化的比较提出问题，再补上规则与事实依据。短段落降低阅读负担，让注意力从数字转向解释。"
CANDIDATES = [
    "器材装上了，然后呢：一颗螺丝松了之后的事",
    "从报修电话到巡检记录：健身器材管护卡在哪些环节",
    "建得起，管不动：公共健身设施维护难背后的账与责",
]


def text(value, size=16, color="ink", bold=False, w=None, **kw):
    return dict(kind="text", text=value, size=size, color=color, bold=bold, **({"w": w} if w else {}), **kw)


def box(name, children=(), *, axis="V", w=None, h=None, gap=12, pad=0,
        bg=None, border=None, radius=0, fill=False, align="start", **kw):
    return dict(kind="box", name=name, axis=axis, children=list(children), gap=gap,
                pad=pad, radius=radius, fill=fill, align=align,
                **({"w": w} if w else {}), **({"h": h} if h else {}),
                **({"bg": bg} if bg else {}), **({"border": border} if border else {}), **kw)


def row(name, children, **kw):
    return box(name, children, axis="H", align="center", **kw)


def spacer():
    return box("弹性间距", fill=True, h=1, gap=0)


def rule():
    return box("分隔线", h=1, bg="border", gap=0)


def button(label, action=None, variant="secondary", w=None, disabled=False):
    return dict(kind="button", text=label, action=action, variant=variant,
                **({"w": w} if w else {}), disabled=disabled)


def badge(label, tone="accent"):
    return dict(kind="badge", text=label, tone=tone)


def check(label, selected=True, action=None, radio=False, **kw):
    return dict(kind="choice", text=label, selected=selected, action=action,
                radio=radio, **kw)


def input_(value, w=160, **kw):
    return dict(kind="input", text=value, w=w, **kw)


def panel(name, children, **kw):
    return box(name, children, bg="surface", border="border", radius=8, pad=20, gap=16, **kw)


def heading(title, desc=None):
    return box(title, [text(title, 20, bold=True), *([text(desc, 14, "secondary")] if desc else [])], gap=4)


def link(label, action):
    return button(label, action, "quiet")


def logpanel(mode="idle", merge=False, expanded=False):
    label = "三稿合并日志" if merge else "文章生成日志"
    status = {"idle": "等待运行", "running": "运行中", "partial": "部分完成", "done": "已完成"}[mode]
    records = {
        "idle": [("就绪", "任务启动后显示实际阶段与运行记录。")],
        "running": [("14:32:10", "已保存输入快照，开始生成三个方向的稿件。"),
                    ("14:32:11", "差异化稿：已完成结构分析，正在撰写正文。"),
                    ("14:32:12", "广度稿：正在梳理相关群体、观点与信息边界。"),
                    ("14:32:13", "深度稿：正在分析维护责任与预算机制。")],
        "partial": [("14:34:26", "差异化稿与广度稿已完成并保存，可先处理成功稿。"),
                    ("14:34:28", "深度稿请求超时；继续生成仅补齐未完成方向。")],
        "done": [("14:35:08", "三稿已完成并保存，候选标题各 3 个。")],
    }[mode]
    if merge and mode == "running":
        records = [("14:40:10", "已读取同一输入快照下的完整三稿。"),
                   ("14:40:11", "正在整合结构、论据与各方向增量。"),
                   ("14:40:12", "正在生成合并正文和三个候选标题。")]
    title = row(label, [text(label, 16, bold=True), spacer(), badge(status, "warning" if mode in ("running", "partial") else "accent")])
    items = [row("日志记录", [text(t, 14, "muted", w=80), text(msg, 14, "secondary", fill=True)], gap=16) for t, msg in records]
    return panel(label, [title, *items] if expanded or mode != "idle" else [title, *items], gap_override=True)


def footer(lead, actions):
    return row("固定操作栏", [text(lead, 14, "secondary", fill=True), *actions], h=72, pad=[16, 24], bg="surface", border="border", gap=12)


def shell(key, number, content, lead, actions, *, title=None, width=1440, height=1000, enabled=6):
    mainw = width - 208
    steps = ["榜单选题", "核心立意", "写作风格", "生成文章", "三稿处理", "合并稿处理"]
    nav = []
    for i, label in enumerate(steps, 1):
        active = i == number
        nav.append(row(label, [badge(f"{i:02}", "accent" if active else "neutral"), text(label, 16, "accent" if active else "secondary", bold=active)],
                       fill=True, gap=8, pad=12, bg="accentSoft" if active else None, radius=6,
                       action=f"step{i}" if i <= enabled else None))
    rail = box("固定主导航", [
        box("品牌", [text("AIDocStudio", 22, "railText", True), text("图文内容创作工作台", 14, "railSecondary")], pad=[24, 16], gap=8),
        box("导航", [
            button("图文生成", "handoff", "rail", 176),
            button("AI 热度图文生成", "step1", "railActive", 176),
            button("头条发布", None, "rail", 176),
            button("系统设置", None, "rail", 176),
        ], pad=[8, 16], gap=8),
        box("导航留白", fill=True),
        box("环境", [text("当前工作环境", 14, "railSecondary"), text("本地桌面工作区", 16, "railText", True), text("任务与结果自动保存", 14, "railSecondary")], pad=16, gap=8),
        box("API", [button("API 连接设置", None, "rail", 176), text("Windows 桌面版", 14, "railSecondary")], pad=16),
    ], w=208, fill=False, bg="rail", gap=8, h=height-32)
    top = row("页面标题区", [box("页面标题", [text("AI 热度图文生成", 28, bold=True), text("从榜单选题到成稿，让每一步都有据可循。", 14, "secondary")], gap=4, fill=True),
                              badge("已自动保存", "success"), button("历史任务", "history")], h=88, pad=[16, 24], bg="surface", gap=16)
    body = box("当前步骤工作区", content, pad=24, gap=20, fillY=True, scroll=True)
    main = box("工作区", [top, row("六步导航", nav, h=80, pad=[12, 24], gap=8, bg="surface", border="border"), body, footer(lead, actions)], w=mainw, h=height-32, gap=0, bg="canvas")
    frame = box(title or f"Step {number:02} / {steps[number-1]}", [
        row("Windows 标题栏", [text("AIDocStudio", 14, "secondary"), spacer(), text("最小化    最大化    关闭", 14, "secondary")], h=32, pad=[4, 16], bg="surface"),
        row("应用主体", [rail, main], gap=0, align_override=True),
    ], w=width, h=height, gap=0, bg="canvas", key=key)
    SCREENS.append(frame)
    return frame


def topic_summary():
    return row("已选原标题", [box("原标题", [text("榜单原标题", 14, "muted", True), text(TITLE, 18, bold=True)], fill=True, gap=6),
                                   badge("公共服务"), link("重选原标题", "step1")], pad=16, bg="surface", border="border", radius=6)


def build_step1():
    filters = panel("采集条件", [
        row("采集设置", [text("采集平台", 16, bold=True), check("头条热榜"), check("百度热搜"), spacer(), text("文章标题数", 14, "secondary"), input_("10", 96)], gap=20),
        row("主题与采集", [input_("公共服务、社区治理", 580, placeholder="主题方向，可留空"), spacer(), button("获取榜单热门数据", "step1", "primary", 184)], gap=16),
    ])
    titles = [TITLE, "社区养老服务如何走到老年人身边", "老旧小区加装电梯，居民最关心哪些问题", "灵活就业人员如何更方便地参加社会保险", "城市公园如何更好满足居民健身需求", "养老金调整如何影响退休家庭的日常开支"]
    rows = [row("榜单表头", [text("选择", 14, "muted", w=44), text("排名", 14, "muted", w=44), text("榜单原标题", 14, "muted", fill=True), text("平台", 14, "muted", w=88)], h=40, bg="subtle", pad=[0, 16])]
    for i, v in enumerate(titles):
        rows.append(row(f"原标题 {i+1}", [check("", i == 0, "topic", True), text(str(i+1).zfill(2), 16, "muted", w=44), text(v, 16, bold=i == 0, fill=True), text("头条热榜" if i % 2 == 0 else "百度热搜", 14, "secondary", w=88)], h=56, pad=[0, 16], gap=12,
                        bg="accentSoft" if i == 0 else "surface", border="border" if i == 0 else None, action="topic"))
    table = panel("榜单结果", [row("结果标题", [text("榜单热门数据", 18, bold=True), badge("10 条"), spacer(), link("清空数据", "empty1")]), box("原标题列表", rows, gap=0, scroll=True)], fill=True)
    detail = panel("选题详情", [heading("已选原标题"), text(TITLE, 20, bold=True), badge("公共服务"), rule(), text("来源信息", 14, "muted", True), text("头条热榜 · 排名 01", 16), text("采集时间：2026-10-27 14:20", 14, "secondary"), text("榜单话题用于确定创作方向；文章中的事实与素材仍需单独核实。", 14, "secondary", w=288), spacer(), link("查看来源", "source")], w=328)
    shell("step1", 1, [heading("获取榜单，选择创作选题", "可同时采集多个平台，每次选择一个原标题。"), filters, row("榜单与详情", [table, detail], gap=16, fillY=True)],
          "已选 1 个原标题", [button("继续提炼立意", "step2", "primary", 184)])


def build_step2():
    ideas = [IDEA, "从一次报修到一次巡检，服务闭环的效率决定了公共设施的实际使用体验。", "区分建设与管护的资金责任，才能让公共服务从交付走向长期运行。"]
    choices = []
    for i, val in enumerate(ideas):
        choices.append(box(f"立意 {i+1}", [row("立意标题", [check(f"立意 {i+1:02}", i == 0, f"idea{i}", True), spacer(), badge("已选" if i == 0 else "可选择", "accent" if i == 0 else "neutral")]), text(val, 16, w=574)], pad=16, gap=12, bg="accentSoft" if i == 0 else "surface", border="accent" if i == 0 else "border", radius=6, action=f"idea{i}"))
    left = panel("核心立意数据", [row("数据标题", [text("核心立意", 18, bold=True), badge("3 条"), spacer(), link("清空数据", "empty2")]), *choices], fill=True)
    right = panel("立意详情", [heading("如何展开论证"), text("从“有没有”到“好不好用”", 20, bold=True), text("以一处健身器材故障为切入点，追踪发现、报修、维修与复检四个环节，解释持续管护如何影响居民使用。", 16, w=374), rule(), text("与原标题的关联", 14, "muted", True), text("原标题关注设施建成后的运行；本立意将问题聚焦到责任、预算与反馈机制。", 16, w=374), badge("机制分析"), text("重新选择立意会保留当前写作风格。", 14, "secondary", w=374)], w=414)
    shell("step2", 2, [heading("选择原标题，提炼核心立意"), topic_summary(), row("提炼设置", [text("生成条数", 16, bold=True), input_("3", 96), text("条", 16), spacer(), button("获取核心立意", "step2", "primary", 184)], pad=16, bg="surface", border="border", radius=6), row("立意与详情", [left, right], gap=16, fillY=True)],
          "已选立意 01 · 选择结果自动保存", [button("上一步", "step1"), button("继续选择写作风格", "step3", "primary", 184)])


def build_step3(empty=False):
    sources = row("风格获取设置", [check("根据原标题获取", False, "sourceTitle", True), check("从已有风格中选择", True, "sourceSaved", True), spacer(), text("获取数量", 14, "secondary"), input_("5", 88), button("获取写作风格", "step3", "primary", 184)], gap=20, pad=16, bg="surface", border="border", radius=6)
    if empty:
        content = panel("写作风格空状态", [heading("写作风格", "等待获取"), box("空状态", [text("尚未获取写作风格", 20, bold=True), text("选择来源和数量后，点击“获取写作风格”。", 16, "secondary"), text("已有风格按常用优先、使用次数降序排列。", 14, "secondary")], gap=12, pad=40, bg="subtle", radius=6)], fillY=True)
    else:
        names = [("数字反差型", "常用 · 使用 28 次", "从细节与数字进入，回应现实疑问。"), ("政策解释型", "常用 · 使用 19 次", "用问题清单解释规则、适用范围与边界。"), ("人物观察型", "使用 12 次", "从具体人物的行动展开公共议题。"), ("理性评论型", "使用 8 次", "区分事实、判断与观点，论证清晰。")]
        items = []
        for i, (name, info, desc) in enumerate(names):
            items.append(box(name, [row("风格名称", [check(name, i == 0, f"style{i}", True), spacer()]), text(desc, 14, "secondary", w=308), text(info, 14, "muted")], pad=16, gap=8, bg="accentSoft" if i == 0 else "surface", border="accent" if i == 0 else "border", radius=6, action=f"style{i}"))
        listing = panel("写作风格列表", [row("列表标题", [text("写作风格", 18, bold=True), badge("4 条"), spacer(), link("清空数据", "empty3")]), text("常用 2 / 5 · 最多可设 5 个", 14, "secondary"), box("风格列表", items, gap=8, scroll=True)], w=380)
        detail = panel("风格完整详情", [row("详情标题", [text("数字反差型", 22, bold=True), spacer(), button("已设常用", "favorite")]), text("写作风格", 14, "muted", True), text(STYLE, 16, w=720), rule(), row("标签与受众", [box("标签", [text("核心标签", 14, "muted", True), row("标签组", [badge("数字切入"), badge("对比叙事")])], fill=True), box("受众", [text("对话对象", 14, "muted", True), text("关注生活成本和公共事务的普通读者", 16)], fill=True)], gap=24), rule(), text("风格优点 / 核心抓手", 14, "muted", True), text("1. 用具体细节建立阅读入口\n2. 先回应疑问，再展开制度背景", 16), spacer(), row("选择反馈", [badge("当前选用"), text("将用于三个方向的文章创作", 14, "secondary")], pad=12, bg="accentSoft", radius=6)], fill=True)
        content = row("列表与详情分栏", [listing, detail], gap=16, fillY=True)
    shell("empty3" if empty else "step3", 3, [heading("获取并选择写作风格", "常用风格优先，其余按使用次数排序；选择后可查看完整说明。"), sources, content],
          "尚未选择写作风格" if empty else "已选：数字反差型 · 切换立意时保留本选择", [button("上一步", "step2"), button("继续设置文章", "step4", "primary", 184, empty)])


def snapshot():
    return panel("创作输入快照", [
        row("原标题行", [text("榜单原标题", 14, "muted", True, w=100), text(TITLE, 18, bold=True, fill=True)], gap=16),
        rule(), row("立意行", [text("核心立意", 14, "muted", True, w=100), text(IDEA, 16, fill=True), link("重新设定", "step2")], gap=16),
        row("风格行", [text("写作风格", 14, "muted", True, w=100), box("风格内容", [text("数字反差型", 16, bold=True), text(STYLE, 14, "secondary", w=874)], gap=4, fill=True), link("重新设定", "step3")], gap=16),
    ])


def directions(mode="idle"):
    descriptions = ["避开惯常叙事，寻找不同视角与内容增量。", "拓展相关群体与观点，呈现信息边界与争议。", "追问底层逻辑与因果链，解释结构性原因。"]
    names = ["差异化稿", "广度稿", "深度稿"]
    cols = []
    for i, (name, desc) in enumerate(zip(names, descriptions)):
        state = "已完成" if mode == "partial" and i < 2 else "请求超时" if mode == "partial" else ["撰写正文", "梳理观点", "分析机制"][i] if mode == "running" else None
        cols.append(box(name, [row("方向标题", [check(name, True, f"direction{i}" if mode == "idle" else None, False, disabled=mode != "idle"), spacer(), *([badge(state, "error" if state == "请求超时" else "success" if state == "已完成" else "accent")] if state else [])]), text(desc, 14, "secondary", w=336)], fill=True, pad=16, bg="accentSoft", border="accent", radius=6, gap=10, action=f"direction{i}" if mode == "idle" else None))
    return row("生成方向", cols, gap=12)


def build_step4(mode="idle"):
    content = [heading("生成三稿文章", "基于同一原标题、核心立意与写作风格，分别创作 1–3 个方向。"), snapshot(), row("方向说明", [text("选择生成方向", 16, bold=True), text("可多选", 14, "secondary"), spacer(), text("已选 3 个方向", 14, "accent")]), directions(mode)]
    if mode == "idle":
        content += [row("篇幅设置", [text("每稿字数", 16, bold=True), input_("1000", 112), text("至", 16, "secondary"), input_("1200", 112), text("字", 16, "secondary"), spacer(), text("输入变更后，旧稿保留为历史版本。", 14, "secondary")], pad=16, bg="surface", border="border", radius=6), logpanel()]
        actions = [button("上一步", "step3"), button("开始生成文章", "running4", "primary", 184)]
        lead = "3 个方向 · 每稿 1000–1200 字"
    elif mode == "running":
        content += [logpanel("running", expanded=True)]
        actions = [button("取消生成", "partial4"), button("查看生成结果", "step5", "primary", 184)]
        lead = "生成中 · 已完成结果将立即保存"
    else:
        content += [logpanel("partial", expanded=True)]
        actions = [button("处理成功稿", "partial5"), button("继续生成", "running4", "primary", 184)]
        lead = "2 稿成功 · 1 稿超时，续跑只补未完成方向"
    shell("step4" if mode == "idle" else "running4" if mode == "running" else "partial4", 4, content, lead, actions, enabled=5 if mode == "partial" else 6)


def preview(expanded=False):
    if not expanded:
        return row("文章预览入口", [text("预览文章", 16, "accent", True), spacer(), text("展开", 14, "accent")], h=48, pad=[0, 16], bg="subtle", border="border", radius=6, action="preview5")
    return box("文章预览展开", [row("文章预览标题", [text("预览文章", 16, "accent", True), spacer(), link("收起", "step5")]),
        text(CANDIDATES[0], 20, bold=True),
        text("一颗松动的螺丝，可能让一件健身器材暂时停用。器材建成之后，谁发现问题、谁接到报修、谁安排维修，决定了居民何时能够重新使用它。", 16, w=734),
        text("把维护做成一个闭环", 18, bold=True),
        text("从问题登记到维修复核，明确责任人与反馈时限，让建设投入转化为持续可用的公共服务。", 16, w=734),
        text("设计示例正文 · 正式运行以实际生成稿件为准", 14, "secondary")], pad=16, bg="subtle", border="border", radius=6, gap=12, h=272, scroll=True)


def manuscript_card(active="similarity", selected=0, expanded=False, merge=False, partial=False, count=3):
    names = [("similarity", "差异化稿"), ("breadth", "广度稿"), ("depth", "深度稿")]
    if merge:
        tabs = row("合并稿分组标题", [text("三稿合并稿", 18, bold=True), spacer(), badge("合并完成", "success")], h=56, pad=[0, 20], bg="subtle", border="border")
    else:
        tabs = row("稿件方向与批量导出", [*[button(v, f"tab:{k}", "tabActive" if active == k else "tab") for k, v in names[:2 if partial else count]], spacer(), button("导出全部稿件", "exportAll")], h=56, pad=[8, 16], bg="subtle", border="border", gap=8)
    candidates = [box("候选标题说明", [row("候选标题", [text("候选标题", 14, "muted", True), spacer(), text("每稿选择 1 个标题", 14, "secondary")])], gap=0)]
    for i, value in enumerate(CANDIDATES):
        candidates.append(row(f"候选标题 {i+1}", [check(value, i == selected, f"candidate:{i}", True, fill=True)], h=56, pad=[0, 16], bg="accentSoft" if selected == i else "surface", border="accent" if selected == i else "border", radius=6, action=f"candidate:{i}"))
    candidates += [preview(expanded)]
    return box("稿件内容卡片", [tabs, box("候选与预览", candidates, pad=20, gap=10)], bg="surface", border="border", radius=8, fill=True)


def result_aside(merge=False, partial=False, count=3):
    return panel("稿件上下文", [heading("本次创作"), badge("2 稿已完成" if partial else "三稿合并稿" if merge else f"{count} 稿已完成", "success"), text("榜单原标题", 14, "muted", True), text(TITLE, 16, bold=True, w=284), rule(), text("核心立意", 14, "muted", True), text(IDEA, 14, "secondary", w=284), rule(), text("写作风格", 14, "muted", True), text("数字反差型", 16, bold=True), spacer(), text("批量导出使用每稿各自选中的标题。生成图文稿只处理当前显示的一篇。", 14, "secondary", w=284), *([button("继续生成深度稿", "running4")] if partial else [])], w=324)


def build_step5(key="step5", active="similarity", selected=0, expanded=False, partial=False, merging=False, count=3):
    content = [row("步骤标题", [heading("三稿文章处理"), spacer(), badge("2 稿已完成" if partial else f"{count} 稿已完成", "success")]),
               row("稿件与上下文", [manuscript_card(active, selected, expanded, partial=partial, count=count), result_aside(partial=partial, count=count)], gap=16, fillY=True)]
    if merging:
        content += [logpanel("running", merge=True, expanded=True)]
    else:
        content += [row("合并日志折叠栏", [text("三稿合并日志", 16, bold=True), spacer(), text("未运行" if partial else "等待运行", 14, "secondary")], h=48, pad=[0, 16], bg="surface", border="border", radius=6)]
    actions = [button("导出本稿", "exportOne", "primary", 144), button("生成图文稿", "illustrate", "primary", 144)]
    if not partial and count == 3:
        actions.append(button("合并三稿" if not merging else "查看合并结果", "merging5" if not merging else "step6", "primary", 144))
    shell(key, 5, content, "当前稿：" + {"similarity": "差异化稿", "breadth": "广度稿", "depth": "深度稿"}[active] + " · 标题选择已保存", actions)


def build_step6():
    shell("step6", 6, [heading("合并稿文章处理", "合并稿保留三稿中的有效增量，统一结构与表达。"), row("合并稿与上下文", [manuscript_card(merge=True), result_aside(merge=True)], gap=16, fillY=True)],
          "当前稿：三稿合并稿 · 已自动保存", [button("返回三稿", "step5"), button("导出本稿", "exportMerged", "primary", 144), button("生成图文稿", "illustrate", "primary", 144)])


def build_dialogs():
    export = panel("导出文章 / 格式与目录", [heading("导出文章", "选择导出格式与保存位置 · 共 3 稿"),
        check("Word 文档（.docx）", True, "formatDocx", True), check("Markdown（.md）", False, "formatMd", True), rule(),
        text("导出目录", 16, bold=True), row("目录选择", [input_("系统桌面", 356), button("选择目录", "chooseDirectory")]),
        text("首次默认系统桌面；修改后记住上次目录。", 14, "secondary"),
        box("导出规则", [text("同名文件自动避让；全部导出使用每稿选中的标题。", 14, "secondary", w=476)], pad=12, bg="subtle", radius=6),
        row("弹窗操作", [spacer(), button("取消", "close"), button("确认导出", "confirmExport", "primary", 144)]),
    ], w=560)
    export["key"] = "exportDialog"
    export["dialog"] = True
    SCREENS.append(export)
    handoff = panel("图文任务交接", [heading("准备生成图文稿", "只处理当前选中的一篇文章"), badge("差异化稿"), text(CANDIDATES[0], 20, bold=True, w=512), rule(),
        text("1. 按所选格式保存本稿\n2. 基于同一正文准备 DOCX 与配图计划\n3. 进入“图文生成”，填好任务后由你手动开始", 16, w=512),
        text("取消导出或保存失败时，保留在当前页面。", 14, "secondary"),
        row("交接操作", [spacer(), button("取消", "close"), button("保存并继续", "confirmHandoff", "primary", 144)])], w=560)
    handoff["key"] = "handoffDialog"
    handoff["dialog"] = True
    SCREENS.append(handoff)


def build_foundations():
    swatches = [box(name, [box("色值", h=48, bg=name, radius=4), text(name, 14, bold=True), text(value, 14, "secondary")], w=154, gap=8) for name, value in list(TOKENS.items())[:7]]
    return box("Windows / 字体与控件规范", [heading("AIDocStudio · Windows 桌面规范", "以逻辑像素为单位；系统缩放不等于缩小字号。"),
        row("色彩", swatches, gap=12), rule(),
        row("字号层级", [text("页面标题 28", 28, bold=True), text("区块标题 20", 20, bold=True), text("正文 16", 16), text("辅助说明 14", 14, "secondary")], gap=40),
        text("中文：Microsoft YaHei UI，缺失时 Noto Sans SC；英文与数字跟随同一字体，避免基线跳动。", 16),
        row("按钮状态", [button("主要操作", None, "primary", 184), button("次要操作", None, "secondary", 184), button("禁用操作", None, "primary", 184, True), button("键盘焦点", None, "focus", 184)], gap=16),
        row("选择与输入", [check("复选已选"), check("单选已选", True, None, True), check("单选未选", False, None, True), input_("数值输入", 160), input_("获得焦点", 224, focus=True)], gap=24),
        rule(), text("布局与状态约定", 20, bold=True),
        text("窗口基准 1440 × 1000；最小逻辑工作区 1280 × 800。主导航 208，内容边距 24，列间距 16。\n按钮 / 输入框 40px；单选 / 复选视觉尺寸 18px，点击区域不小于 40px。表格行 56px。\n底部操作栏固定 72px；只滚动当前工作区，日志与预览内部可滚动，避免整页跳转。\nWindows 125% / 150% 缩放时按逻辑像素布局；字体 point = px × 72 / 96，16px 对应 12pt。", 16, w=1120),
        text("Tab 按视觉顺序移动；Space 切换选择；Enter 执行当前主要操作；Escape 关闭弹窗。焦点使用 2px 蓝色描边。\n生成 / 合并中禁用输入与重复提交；取消在安全检查点生效，保留已完成稿件。错误信息写明影响与恢复动作。", 16, w=1120),
    ], w=1184, pad=24, gap=24, bg="surface", border="border", radius=8, key="foundations")


def main():
    build_step1()
    build_step2()
    build_step3()
    build_step4()
    build_step5()
    build_step6()
    build_step4("running")
    build_step4("partial")
    build_step5("partial5", partial=True)
    build_step5("single5", count=1)
    build_step5("dual5", count=2)
    build_step5("preview5", expanded=True)
    build_step5("breadth5", active="breadth", selected=1)
    build_step5("depth5", active="depth", selected=2)
    build_step5("merging5", merging=True)
    build_step3(True)
    build_dialogs()
    SCREENS.append(build_foundations())
    # Same physical rules at the minimum logical window; workspace scrolls, footer stays visible.
    compact = json.loads(json.dumps(next(s for s in SCREENS if s.get("key") == "step4")))
    compact.update(key="compact4", name="Windows / 最小窗口 1280 × 800", w=1280, h=800)
    compact["children"][1]["children"][0]["h"] = 768
    compact["children"][1]["children"][1].update(w=1072, h=768)
    # Explicit widths inside the snapshot reduce with the content column.
    def narrow(n):
        if n.get("kind") == "text" and n.get("w") == 874:
            n["w"] = 714
        if n.get("kind") == "text" and n.get("w") == 336:
            n["w"] = 282
        for ch in n.get("children", []):
            narrow(ch)
    narrow(compact)
    SCREENS.append(compact)
    asset_sources = {"image_text": "ui/assets/nav/image_text.svg", "ai_hot_article": "ui/assets/nav/ai_hot_article.svg", "toutiao_publish": "ui/assets/nav/toutiao_publish.svg", "system_settings": "ui/assets/nav/system_settings.svg", "api_settings": "ui/assets/nav/api_settings.svg", "check": "modules/hot_article/assets/figma/check.svg"}
    assets = {key: (ROOT.parents[1] / path).read_text(encoding="utf-8") for key, path in asset_sources.items()}
    data = dict(version="windows-2026-10-27", targetFile="x3uNLbtFAS8MOCnCTPu7aH", page="03 · Windows 桌面版", tokens=TOKENS, assets=assets, assetSources=asset_sources, screens=SCREENS)
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "design.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "design-data.js").write_text("window.WINDOWS_DESIGN = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    template = (ROOT / "figma-plugin" / "renderer.js").read_text(encoding="utf-8")
    helpers = "\n".join(p.read_text(encoding="utf-8") for p in sorted((ROOT / "figma-plugin" / "helpers").glob("*.js")))
    (ROOT / "figma-plugin" / "code.js").write_text("const DESIGN = " + json.dumps(data, ensure_ascii=False) + ";\n" + helpers + "\n" + template, encoding="utf-8")
    print(json.dumps({"screens": len(SCREENS), "keys": [s["key"] for s in SCREENS], "file": str(ROOT / "design.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
