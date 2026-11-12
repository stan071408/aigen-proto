"""Windows 桌面版 Tk 工作区（Figma 36:2474）：固定页眉、六步页签、单步工作区与固定操作栏。

只依赖应用门面；页面不做整页滚动，仅列表/正文/日志在各自卡片内滚动。
"""
from __future__ import annotations

import queue
import tkinter as tk
import tkinter.font
import webbrowser
from tkinter import ttk, filedialog, messagebox

from .application import TaskRunner
from .domain import DIRECTIONS
from .presentation import (Panel, ActionButton, WindowsChoiceImages, font, BG, GREEN,
                           W_INK, W_TEXT, W_MUTED, W_LINE, W_SOFT, W_SUBTLE, W_OK_BG, W_OK,
                           W_ON_ACCENT, W_WARN_BG, W_WARN, W_ERR_BG, W_ERR)

STEPS = ["榜单选题", "核心立意", "写作风格", "生成文章", "三稿处理", "合并稿处理"]
DIRECTION_NOTES = {"similarity": "避开惯常叙事，寻找不同视角与内容增量。",
                   "breadth": "拓展相关群体与观点，呈现信息边界与争议。",
                   "depth": "追问底层逻辑与因果链，解释结构性原因。"}
SOURCES = {"toutiao": "头条热榜", "baidu": "百度热搜"}
BADGES = {"soft": (W_SOFT, GREEN), "ok": (W_OK_BG, W_OK), "neutral": (W_SUBTLE, W_TEXT),
          "warn": (W_WARN_BG, W_WARN), "error": (W_ERR_BG, W_ERR)}
# 运行日志中的阶段关键词 → 方向卡徽标文案（设计稿：撰写正文 / 梳理观点 / 分析机制）。
DIRECTION_PHASES = (("撰写", "撰写正文"), ("梳理", "梳理观点"), ("分析", "分析机制"), ("标题", "拟定标题"), ("结构", "规划结构"))
LOG_STATES = {"complete": "已完成", "failed": "失败", "cancelled": "已停止", "partial": "部分完成"}


class ScrollArea(tk.Frame):
    """卡片内滚动区：内容未溢出时隐藏滚动条；滚轮由工作区按指针位置分发。"""
    def __init__(self, parent, bg="white", padx=0):
        super().__init__(parent, bg=bg, padx=padx)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.bar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.body = tk.Frame(self.canvas, bg=bg)
        self._window = self.canvas.create_window(0, 0, window=self.body, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self._autohide)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._window, width=e.width))
        self.body.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=(0, 0, e.width, e.height)))

    def _autohide(self, first, last):
        self.bar.set(first, last)
        if float(first) <= 0 and float(last) >= 1:
            self.bar.pack_forget()
        elif not self.bar.winfo_manager():
            self.bar.pack(side="right", fill="y", before=self.canvas)

    def scroll(self, units):
        if self.bar.winfo_manager():
            self.canvas.yview_scroll(units, "units")

    def reveal(self, widget):
        self.update_idletasks()
        height = max(1, self.body.winfo_height())
        offset = widget.winfo_rooty() - self.body.winfo_rooty()
        self.canvas.yview_moveto(max(0, offset - 8) / height)

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)

class HotArticleWorkspace(tk.Frame):
    def __init__(self, parent, service, on_handoff):
        super().__init__(parent, bg=BG)
        self.service, self.on_handoff = service, on_handoff
        self.runner = TaskRunner(service)
        self.state = service.saved_state()
        self.rows = self.state.get("rows", [])
        self.ideas = self.state.get("ideas", [])
        self.styles = self.state.get("styles", [])
        self.topic = self.state.get("topic")
        self.idea = self.state.get("idea")
        self.style = self.state.get("style")
        self.write_task = self.state.get("write_task")
        self.merge_task = self.state.get("merge_task")
        self.reset_target = None
        self.current_step = 1
        self.sections, self.logs, self.task_buttons = {}, {}, []
        self.log_states, self.feedback, self.primary_actions = {}, {}, {}
        self.footers, self.footer_texts, self.step_tabs = {}, {}, {}
        self.current_draft = {}
        self._job_kind = None
        self._busy = False
        self._job_step = 1
        self._closed = False
        self.choice_images = WindowsChoiceImages(self)
        self.status = tk.StringVar(master=self, value="就绪 · 数据与模型结果将保存在本地")
        self._build()
        self._render_topics()
        self._render_ideas()
        self._render_styles()
        self._render_anchor()
        for step in (5, 6):
            self._render_empty_drafts(step)
        if self.write_task:
            self._render_drafts(5, self.write_task)
            self._restore_log(4, self.write_task)
        if self.merge_task:
            self._render_drafts(6, self.merge_task)
        self._sync_direction_badges()
        self._render_footers()
        self._goto(1)
        self._poll_id = self.after(100, self._poll)

    # ------------------------------------------------------------------ 基础控件
    def _lbl(self, parent, text, *, size=16, bold=False, color=W_INK, wrap=False, **pack):
        label = tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color, font=font(size, bold),
                         anchor="w", justify="left", padx=0, pady=0)
        if wrap:
            label.bind("<Configure>", lambda e: label.configure(wraplength=max(40, e.width - 2)))
        if pack:
            label.pack(**({"anchor": "w"} | pack))
        return label

    # Older callers/tests use these names.
    def _label(self, parent, text, *, bold=False, size=16, color=W_INK, **pack):
        return self._lbl(parent, text, size=size, bold=bold, color=color, **({"anchor": "w"} | pack))

    def _text(self, parent, text, color=W_INK, *, size=16, bold=False, pady=0):
        return self._lbl(parent, text, size=size, bold=bold, color=color, wrap=True, fill="x", pady=pady)

    def _button(self, parent, text, command, *, style="primary", width=None, side="left", padx=None,
                tracked=False, primary=None, **_ignored):
        if primary is not None:
            style = "primary" if primary else "secondary"
        bold = style in ("primary", "tabActive")
        bg = {"primary": GREEN, "secondary": "white", "tabActive": W_SOFT}.get(style, parent.cget("bg"))
        fg = {"primary": W_ON_ACCENT, "tabActive": GREEN}.get(style, W_INK)
        border = {"primary": GREEN, "secondary": W_LINE, "tabActive": GREEN}.get(style, bg)
        if width is None:
            width = tkinter.font.Font(root=self, font=font(16, bold)).measure(text) + 32
        button = ActionButton(parent, text=text, command=lambda: self._guard(command), pixel_width=width, pixel_height=40,
                              bg=bg, fg=fg, activebackground="#136b62" if style == "primary" else W_SOFT,
                              activeforeground=fg, disabledforeground="#9aa8a5", relief="flat", bd=0,
                              highlightthickness=1, highlightbackground=border, highlightcolor="#0067c0",
                              font=font(16, bold), cursor="hand2")
        button._style = style
        if side:
            button.pack(side=side, padx=padx if padx is not None else ((12, 0) if side == "right" else (0, 12)))
        if tracked:
            self.task_buttons.append(button)
        return button

    def _style_button(self, button, style):
        bold = style in ("primary", "tabActive")
        bg = {"primary": GREEN, "secondary": "white", "tabActive": W_SOFT}.get(style, button.master.cget("bg"))
        border = {"primary": GREEN, "secondary": W_LINE, "tabActive": GREEN}.get(style, bg)
        button.configure(bg=bg, fg={"primary": W_ON_ACCENT, "tabActive": GREEN}.get(style, W_INK),
                         highlightbackground=border, font=font(16, bold))
        button._style = style

    def _badge(self, parent, text, kind="soft", **pack):
        bg, fg = BADGES[kind]
        badge = tk.Label(parent, text=text, bg=bg, fg=fg, font=font(14, True), padx=10, pady=4)
        if pack:
            badge.pack(**pack)
        return badge

    def _card(self, parent, *, padding=20, bg="white", border=W_LINE, **pack):
        pad = (padding, padding) if isinstance(padding, int) else padding
        card = tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground=border,
                        highlightcolor=border, padx=pad[0], pady=pad[1])
        if pack:
            card.pack(**pack)
        return card

    def _divider(self, parent, pady=16):
        tk.Frame(parent, bg=W_LINE, height=1).pack(fill="x", pady=pady)

    def _input(self, parent, variable, width, **pack):
        box = tk.Frame(parent, bg="white", width=width, height=40, highlightthickness=1,
                       highlightbackground=W_LINE, highlightcolor="#0067c0")
        box.pack_propagate(False)
        entry = tk.Entry(box, textvariable=variable, bd=0, relief="flat", font=font(16), bg="white",
                         fg=W_INK, insertbackground=W_INK)
        entry.pack(fill="both", expand=True, padx=12)
        if pack:
            box.pack(**pack)
        return entry

    def _choice(self, parent, text, variable, value=None, command=None, *, kind="radio", size=16, bold=False, color=W_INK):
        bg = parent.cget("bg")
        row = tk.Frame(parent, bg=bg)
        options = dict(variable=variable, bg=bg, activebackground=bg, bd=0, cursor="hand2")
        if command:
            options["command"] = lambda: self._guard(command)
        control = (tk.Radiobutton(row, value=value, **options) if kind == "radio"
                   else tk.Checkbutton(row, **options))
        self.choice_images.apply(control, kind)
        control.pack(side="left")
        label = tk.Label(row, text=text, bg=bg, fg=color, font=font(size, bold), anchor="w", justify="left", cursor="hand2")
        label.pack(side="left", fill="x", expand=True, padx=(12, 0))
        label.bind("<Button-1>", lambda e: control.invoke())
        control.text_label = label
        return row, control

    def _paint(self, widget, bg):
        """递归改背景（选中态切换），保留徽标等自带底色控件。"""
        if getattr(widget, "_keep_bg", False):
            return
        try:
            widget.configure(bg=bg)
            if isinstance(widget, (tk.Radiobutton, tk.Checkbutton)):
                widget.configure(activebackground=bg, selectcolor=bg)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._paint(child, bg)

    def _clear_box(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def _guard(self, command):
        try:
            command()
        except Exception as exc:
            messagebox.showerror("AI 热度图文生成", str(exc), parent=self)

    def _number(self, variable, name, low=1, high=100):
        try:
            value = int(variable.get())
        except (tk.TclError, ValueError):
            raise ValueError(f"{name}请输入整数")
        if not low <= value <= high:
            raise ValueError(f"{name}需在 {low}–{high} 之间")
        return value

    def _empty(self, parent, title, detail):
        box = tk.Frame(parent, bg=parent.cget("bg"))
        box.pack(fill="both", expand=True, pady=24)
        tk.Label(box, text=title, bg=box.cget("bg"), fg=W_INK, font=font(16, True)).pack(pady=(24, 8))
        tk.Label(box, text=detail, bg=box.cget("bg"), fg=W_TEXT, font=font(14), justify="center").pack()
        return box

    # ------------------------------------------------------------------ 外壳
    def _build(self):
        header = tk.Frame(self, bg="white", height=88, padx=24)
        header.pack(fill="x")
        header.pack_propagate(False)
        titles = tk.Frame(header, bg="white")
        titles.pack(side="left", fill="y", pady=(10, 0))
        self._lbl(titles, "AI 热度图文生成", size=28, bold=True, anchor="w")
        self._lbl(titles, "从榜单选题到成稿，让每一步都有据可循。", size=14, color=W_TEXT, anchor="w", pady=(4, 0))
        more = tk.Menubutton(header, text="更多", bg="white", fg=W_INK, activebackground=W_SOFT, font=font(16),
                             relief="flat", bd=0, padx=12, cursor="hand2")
        menu = tk.Menu(more, tearoff=False)
        menu.add_command(label="模块模型设置", command=lambda: self._guard(self._settings))
        menu.add_command(label="刷新当天榜单", command=lambda: self._guard(lambda: self._fetch_boards(True)))
        more.configure(menu=menu)
        more.pack(side="right", padx=(8, 0))
        self.more_menu = menu
        self._button(header, "历史任务", self._history, style="secondary", width=96, side="right", padx=(16, 0))
        self.autosave_badge = self._badge(header, "已自动保存", "ok", side="right")
        tabs = tk.Frame(self, bg="white", height=79, padx=24)
        tabs.pack(fill="x")
        tk.Frame(self, bg=W_LINE, height=1).pack(fill="x")
        tabs.grid_propagate(False)
        tabs.rowconfigure(0, weight=1)
        for n, name in enumerate(STEPS, 1):
            tabs.columnconfigure(n - 1, weight=1, uniform="step")
            tab = tk.Frame(tabs, bg="white", padx=12, pady=12, cursor="hand2")
            tab.grid(row=0, column=n - 1, sticky="ew", padx=(0 if n == 1 else 4, 0 if n == 6 else 4), pady=(12, 12))
            number = tk.Label(tab, text=f"{n:02}", font=font(14, True), padx=10, pady=4)
            number.pack(side="left")
            label = tk.Label(tab, text=name, font=font(16), padx=0)
            label.pack(side="left", padx=(8, 0))
            for widget in (tab, number, label):
                widget.bind("<Button-1>", lambda e, step=n: self._guard(lambda: self._goto(step)))
            self.step_tabs[n] = (tab, number, label)
        self.footer = tk.Frame(self, bg="white", height=71, padx=24)
        self.footer.pack(side="bottom", fill="x")
        tk.Frame(self, bg=W_LINE, height=1).pack(side="bottom", fill="x")
        self.footer.pack_propagate(False)
        self.footer_label = tk.Label(self.footer, text="", bg="white", fg=W_TEXT, font=font(14), anchor="w")
        self.footer_label.pack(side="left", fill="x", expand=True)
        self.stop_button = self._button(self.footer, "停止当前任务", self.runner.cancel, style="secondary", side=None)
        self.status_bar = self.stop_button
        self.page_host = tk.Frame(self, bg=BG, padx=24, pady=24)
        self.page_host.pack(fill="both", expand=True)
        for n in range(1, 7):
            self.sections[n] = tk.Frame(self.page_host, bg=BG)
            self.footers[n] = tk.Frame(self.footer, bg="white")
        self._build_one()
        self._build_two()
        self._build_three()
        self._build_four()
        self._wheel_binding = self.winfo_toplevel().bind("<MouseWheel>", self._wheel, add="+")

    def _title(self, parent, title, description=None, badge=None):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 20))
        copy = tk.Frame(row, bg=BG)
        copy.pack(side="left", fill="x", expand=True)
        self._lbl(copy, title, size=20, bold=True, anchor="w")
        if description:
            self._lbl(copy, description, size=14, color=W_TEXT, anchor="w", pady=(4, 0))
        if badge:
            return self._badge(row, badge, "ok", side="right", anchor="n")
        return None

    def _footer(self, step, text, buttons):
        frame = self.footers[step]
        self._clear_box(frame)
        self.footer_texts[step] = text
        self.footer_primary = getattr(self, "footer_primary", {})
        self.footer_primary.pop(step, None)
        self.footer_live = getattr(self, "footer_live", {})
        self.footer_live[step] = False
        for spec in reversed(buttons):
            name, command, style, width = spec[:4]
            live = len(spec) > 5 and spec[5]
            button = self._button(frame, name, command, style=style, width=width, side="right", tracked=not live)
            if (len(spec) > 4 and not spec[4]) or (self._busy and not live):
                button.configure(state="disabled")
            if live:
                self.footer_live[step] = True
            if step in (1, 2, 3, 4) and style == "primary" and name.startswith(("继续", "开始")):
                self.footer_primary[step] = button
        if self.current_step == step:
            self._show_footer()

    def _show_footer(self):
        for n, frame in self.footers.items():
            if n != self.current_step:
                frame.pack_forget()
        if self._busy and not getattr(self, "footer_live", {}).get(self.current_step):
            self.footers[self.current_step].pack_forget()
            if not self.stop_button.winfo_manager():
                self.stop_button.pack(side="right")
            self.footer_label.configure(text=self.status.get())
        elif self._busy:
            # 设计稿的运行中操作栏（生成中 / 合并中）：保留状态文案与可用操作。
            self.stop_button.pack_forget()
            self.footers[self.current_step].pack(side="right")
            self.footer_label.configure(text=self.footer_texts.get(self.current_step, ""))
        else:
            self.stop_button.pack_forget()
            self.footers[self.current_step].pack(side="right")
            self.footer_label.configure(text=self.footer_texts.get(self.current_step, ""))

    def _goto(self, step, target=None):
        for n, frame in self.sections.items():
            if n != step:
                frame.pack_forget()
        self.sections[step].pack(fill="both", expand=True)
        self.current_step = step
        self._highlight_guide(step)
        self._show_footer()
        if target is not None:
            area = target
            while area is not None and not isinstance(area, ScrollArea):
                area = area.master
            if area is not None:
                area.reveal(target)

    def _highlight_guide(self, step):
        for n, (tab, number, label) in self.step_tabs.items():
            active = n == step
            tab.configure(bg=W_SOFT if active else "white")
            number.configure(bg=W_SOFT if active else W_SUBTLE, fg=GREEN if active else W_TEXT)
            label.configure(bg=W_SOFT if active else "white", fg=GREEN if active else W_TEXT, font=font(16, active))

    def _sync_visibility(self):
        """固定布局下各步骤始终可切换；仅刷新操作栏状态。"""
        self._render_footers()

    def _responsive(self, event=None):
        return

    def _wheel(self, event):
        if not self.winfo_ismapped():
            return
        widget = self.winfo_containing(event.x_root, event.y_root)
        while widget is not None and not isinstance(widget, (ScrollArea, tk.Text)):
            if widget is self:
                return
            widget = widget.master
        if isinstance(widget, ScrollArea):
            widget.scroll(-int(event.delta / 120))

    def _persist(self):
        self.service.save_state(dict(rows=self.rows, ideas=self.ideas, styles=self.styles,
            topic=self.topic, idea=self.idea, style=self.style, write_task=self.write_task, merge_task=self.merge_task))

    def _invalidate(self):
        self.write_task = self.merge_task = None
        for key in DIRECTIONS:
            self._direction_badge(key)
        for step in (5, 6):
            self._render_empty_drafts(step)
        self._render_anchor()
        self._persist()

    def _show_feedback(self, step, message, error=False):
        self.feedback[step] = message
        if step == self.current_step and not self.runner.busy:
            self.footer_label.configure(text=message, fg="#b54949" if error else W_TEXT)
            self.after(6000, lambda: self.winfo_exists() and self.footer_label.configure(fg=W_TEXT))

    def _render_footers(self):
        topic, idea, style = self.topic, self.idea, self.style
        self._footer(1, "已选 1 个原标题" if topic else "尚未选择原标题",
                     [("继续提炼立意", lambda: self._continue(2), "primary", 184, bool(topic))])
        index = next((i for i, v in enumerate(self.ideas) if v == idea), None)
        self._footer(2, f"已选立意 {index + 1:02} · 选择结果自动保存" if idea and index is not None else
                     "已选核心立意 · 选择结果自动保存" if idea else "尚未选择核心立意",
                     [("上一步", lambda: self._goto(1), "secondary", 80),
                      ("继续选择写作风格", lambda: self._continue(3), "primary", 184, bool(idea))])
        self._footer(3, f"已选：{style['style_name']} · 切换立意时保留本选择" if style else "尚未选择写作风格",
                     [("上一步", lambda: self._goto(2), "secondary", 80),
                      ("继续设置文章", lambda: self._continue(4), "primary", 184, bool(style))])
        count = sum(v.get() for v in self.directions.values())
        try:
            words = f"每稿 {int(self.word_min.get())}–{int(self.word_max.get())} 字"
        except (tk.TclError, ValueError):
            words = "请填写字数范围"
        partial = self._partial_write()
        if self._busy and self._job_kind == "write":
            self._footer(4, "生成中 · 已完成结果将立即保存",
                         [("取消生成", self.runner.cancel, "secondary", 96, True, True),
                          ("查看生成结果", self._view_running, "primary", 184, True, True)])
        elif partial:
            done, failed, timeout = partial
            self._footer(4, f"{done} 稿成功 · {failed} 稿{'超时' if timeout else '未完成'}，续跑只补未完成方向",
                         [("处理成功稿", lambda: self._goto(5), "secondary", 112, done > 0),
                          ("继续生成", self._resume_write, "primary", 184)])
        else:
            self._footer(4, f"{count} 个方向 · {words}",
                         [("上一步", lambda: self._goto(3), "secondary", 80),
                          ("开始生成文章", self._generate, "primary", 184, count > 0)])
        if 4 in self.footer_primary:
            self.primary_actions[4] = self.footer_primary[4]
        # 设计稿运行中 / 部分完成状态不显示篇幅设置，日志卡上移占满剩余高度。
        hide_length = (self._busy and self._job_kind == "write") or bool(partial)
        if hide_length and self.length_card.winfo_manager():
            self.length_card.pack_forget()
        elif not hide_length and not self.length_card.winfo_manager():
            self.length_card.pack(fill="x", pady=(20, 0), before=self.write_log_card)
        for refresh in list(getattr(self, "_draft_footers", {}).values()):
            refresh()

    def _write_state(self):
        if not self.write_task:
            return None
        try:
            return self.service.task(self.write_task)
        except Exception:
            return None

    def _partial_write(self):
        """(成功稿数, 未完成稿数, 是否超时)；非部分完成时返回 None。"""
        state = self._write_state()
        if not state or state.get("status") not in ("partial", "failed", "cancelled", "interrupted"):
            return None
        wanted = [d for d in (state.get("snapshot", {}).get("directions") or DIRECTIONS) if d in DIRECTIONS]
        done = {d["direction"] for d in self.service.results(self.write_task)}
        missing = [d for d in wanted if d not in done]
        if not missing:
            return None
        messages = {v["direction"]: v.get("message") or "" for v in self._direction_states(self.write_task)}
        timeout = "超时" in (state.get("error") or "") or any("超时" in messages.get(d, "") for d in missing)
        return len(done & set(wanted)), len(missing), timeout

    def _direction_states(self, task):
        try:
            return self.service.repo.direction_states(task)
        except Exception:
            return []

    def _direction_badge(self, key, status=None, message=""):
        """第四步方向卡右上角的运行徽标（Figma 36:3791 / 36:3994）。"""
        badge = getattr(self, "direction_badges", {}).get(key)
        if badge is None or not badge.winfo_exists():
            return
        if status is None:
            badge.pack_forget()
            return
        text, kind = {"queued": ("等待中", "neutral"), "running": ("生成中", "soft"), "complete": ("已完成", "ok"),
                      "cancelled": ("已停止", "neutral"), "interrupted": ("已中断", "warn")}.get(status, ("失败", "error"))
        if status == "failed" and "超时" in message:
            text = "请求超时"
        if status == "running" and message:
            text = next((phase for word, phase in DIRECTION_PHASES if word in message), text)
        bg, fg = BADGES[kind]
        badge.configure(text=text, bg=bg, fg=fg)
        if not badge.winfo_manager():
            badge.pack(side="right", before=badge._anchor)

    def _sync_direction_badges(self):
        for key in DIRECTIONS:
            self._direction_badge(key)
        if self.write_task:
            for state in self._direction_states(self.write_task):
                self._direction_badge(state["direction"], state["status"], state.get("message") or "")

    def _resume_write(self):
        if not self.write_task:
            raise ValueError("没有可续跑的生成任务")
        self._start("write", {}, 4, resume=self.write_task)

    def _view_running(self):
        task = getattr(self, "_running_task", None)
        if task and self.service.results(task):
            self._render_drafts(5, task)
        self._goto(5)

    def _continue(self, step):
        requirement = {2: (self.topic, "请先选择榜单原标题"), 3: (self.idea, "请先选择核心立意"),
                       4: (self.style, "请先选择写作风格")}[step]
        if not requirement[0]:
            raise ValueError(requirement[1])
        self._goto(step)

    # ------------------------------------------------------------------ 第一步
    def _build_one(self):
        frame = self.sections[1]
        self._title(frame, "获取榜单，选择创作选题", "可同时采集多个平台，每次选择一个原标题。")
        form = self._card(frame, padding=20, fill="x")
        row = tk.Frame(form, bg="white")
        row.pack(fill="x")
        self._lbl(row, "采集平台", bold=True, side="left")
        self.sources = {s: tk.BooleanVar(master=self, value=True) for s in SOURCES}
        self.source_checks = {}
        for key, name in SOURCES.items():
            item, control = self._choice(row, name, self.sources[key], kind="check")
            item.pack(side="left", padx=(24, 0))
            self.source_checks[key] = control
        self.board_count = tk.IntVar(master=self, value=5)
        self.board_count_input = self._input(row, self.board_count, 96, side="right")
        self._lbl(row, "文章标题数", size=14, color=W_TEXT, side="right", padx=(0, 12))
        row = tk.Frame(form, bg="white")
        row.pack(fill="x", pady=(16, 0))
        self.direction = tk.StringVar(master=self)
        holder = tk.Frame(row, bg="white", width=580, height=40)
        holder.pack(side="left")
        holder.pack_propagate(False)
        style = ttk.Style(self)
        style.configure("HotArticle.TCombobox", padding=(10, 6))
        self.direction_input = ttk.Combobox(holder, textvariable=self.direction, font=font(16), style="HotArticle.TCombobox")
        self.direction_input.pack(fill="both", expand=True)
        self.primary_actions[1] = self._button(row, "获取榜单热门数据", lambda: self._fetch_boards(False), width=184, side="right", padx=0, tracked=True)
        self.category_suggestions = tk.Frame(row, bg="white")
        self.category_suggestions.pack(side="left", fill="x", expand=True, padx=(12, 12))
        self._render_categories()
        split = tk.Frame(frame, bg=BG)
        split.pack(fill="both", expand=True, pady=(20, 0))
        detail = self._card(split, padding=20, side="right", fill="y", padx=(16, 0))
        detail.configure(width=328)
        detail.pack_propagate(False)
        self.topic_detail = detail
        results = self._card(split, padding=0, side="left", fill="both", expand=True)
        head = tk.Frame(results, bg="white", padx=20, pady=16)
        head.pack(fill="x")
        self._lbl(head, "榜单热门数据", size=18, bold=True, side="left")
        self.topic_badge_count = self._badge(head, "0 条", "soft", side="left", padx=(12, 0))
        self.topic_clear = self._button(head, "清空数据", self._clear_topics, style="quiet", width=96, side="right", padx=0, tracked=True)
        table = tk.Frame(results, bg=W_SUBTLE, height=40, padx=16)
        table.pack(fill="x")
        table.pack_propagate(False)
        self._table_columns(table, ("选择", "排名", "榜单原标题", "平台"), header=True)
        self.topic_area = ScrollArea(results, bg="white")
        self.topic_area.pack(fill="both", expand=True)
        self.topic_box = self.topic_area.body
        self.log_states[1] = tk.Label(self, text="等待运行")
        self.logs[1] = self._hidden_log()
        self.board_request_count = 5

    def _hidden_log(self):
        """第一至三步不再展示日志卡；保留日志文本以便状态栏与历史复用。"""
        box = tk.Text(self, height=1)
        box._rules = []
        return box

    def _table_columns(self, row, values, header=False, bg=None, bold=False):
        bg = bg or row.cget("bg")
        for index, width in enumerate((44, 44, 0, 88)):
            row.columnconfigure(index, minsize=width, weight=1 if not width else 0)
        widgets = []
        for index, value in enumerate(values):
            if isinstance(value, tk.Widget):
                widget = value
            else:
                widget = tk.Label(row, text=value, bg=bg, anchor="w", justify="left",
                                  fg=W_MUTED if header or index == 1 else W_TEXT if index == 3 else W_INK,
                                  font=font(14 if header or index == 3 else 16, bold and index == 2))
            widget.grid(row=0, column=index, sticky="w" if index != 2 else "ew", padx=(0, 0 if index == 3 else 12))
            widgets.append(widget)
        row.rowconfigure(0, weight=1)
        return widgets

    def _fetch_boards(self, refresh):
        count = self._number(self.board_count, "文章标题数")
        sources = [s for s, v in self.sources.items() if v.get()]
        if not sources:
            raise ValueError("请至少选择一个采集平台")
        self.board_request_count = count
        self._start("boards", dict(sources=sources, direction=self.direction.get(), count=count, refresh=refresh), 1)

    def _clear_topics(self):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        self.rows, self.topic, self.idea, self.style, self.ideas, self.styles = [], None, None, None, [], []
        self._invalidate()
        self._render_topics()
        self._render_ideas()
        self._render_styles()

    def _render_categories(self):
        self._clear_box(self.category_suggestions)
        categories = self.service.topic_categories()
        self.direction_input.configure(values=categories)
        for category in categories[:4]:
            button = tk.Button(self.category_suggestions, text=category, command=lambda name=category: self.direction.set(name),
                               font=font(14), bg=W_SUBTLE, fg=W_TEXT, activebackground=W_SOFT, bd=0, padx=10, pady=4, cursor="hand2")
            button.pack(side="left", padx=(0, 8))
            self.task_buttons.append(button)

    def _render_topics(self):
        self._clear_box(self.topic_box)
        self.topic_badge_count.configure(text=f"{len(self.rows)} 条" if self.rows else "等待获取",
                                         bg=W_SOFT if self.rows else W_SUBTLE, fg=GREEN if self.rows else W_TEXT)
        self.topic_area.scroll_to_top()
        if not self.rows:
            self._empty(self.topic_box, "尚未获取榜单数据", "选择平台与条数后点击“获取榜单热门数据”。")
        elif len(self.rows) < self.board_request_count:
            note = tk.Label(self.topic_box, text=f"实际匹配 {len(self.rows)} 条，少于设定的 {self.board_request_count} 条，已返回全部可用结果。",
                            bg=W_WARN_BG, fg=W_WARN, font=font(14), anchor="w", padx=16, pady=8)
            note.pack(fill="x")
        selected = tk.StringVar(master=self, value=self.topic.get("id", "") if self.topic else "")
        self.topic_rows = []
        for item in self.rows:
            active = bool(self.topic and self.topic.get("id") == item["id"])
            bg = W_SOFT if active else "white"
            row = tk.Frame(self.topic_box, bg=bg, height=56, padx=16, cursor="hand2")
            row.pack(fill="x")
            row.pack_propagate(False)
            row.grid_propagate(False)
            radio = tk.Radiobutton(row, variable=selected, value=item["id"], bg=bg, activebackground=bg, bd=0, cursor="hand2",
                                   command=lambda value=item: self._guard(lambda: self._choose_topic(value, advance=False)))
            self.choice_images.apply(radio, "radio")
            labels = self._table_columns(row, (radio, f'{item["rank"]:02}', item["title"], SOURCES.get(item["source"], item["source"])), bg=bg, bold=active)
            labels[2].configure(text=self._clip(labels[2], item["title"], 520))
            for widget in [row] + labels[1:]:
                widget.bind("<Button-1>", lambda e, control=radio: control.invoke())
            tk.Frame(self.topic_box, bg=W_LINE, height=1).pack(fill="x")
            self.topic_rows.append(row)
        self._render_topic_detail()
        self._render_footers()

    def _clip(self, widget, text, width):
        measure = tkinter.font.Font(root=self, font=widget.cget("font")).measure
        if measure(text) <= width:
            return text
        while text and measure(text + "…") > width:
            text = text[:-1]
        return text + "…"

    def _render_topic_detail(self):
        box = self.topic_detail
        self._clear_box(box)
        item = self.topic
        self._lbl(box, "已选原标题", size=20, bold=True, anchor="w")
        if not item:
            self._lbl(box, "从左侧选择一条榜单原标题后，在此查看来源信息。", size=14, color=W_TEXT, wrap=True, fill="x", pady=(16, 0))
            return
        self._lbl(box, item["title"], size=20, bold=True, wrap=True, fill="x", pady=(16, 0))
        for label in item.get("labels", [])[:3]:
            self._badge(box, label, "soft", anchor="w", pady=(12, 0))
        self._divider(box, pady=16)
        self._lbl(box, "来源信息", size=14, bold=True, color=W_MUTED, anchor="w")
        self._lbl(box, f'{SOURCES.get(item["source"], item["source"])} · 排名 {item["rank"]:02}', anchor="w", pady=(8, 0))
        meta = []
        if item.get("collected_at"):
            meta.append("采集时间：" + item["collected_at"][:16].replace("T", " "))
        if item.get("heat") is not None:
            heat = int(item["heat"])
            meta.append("来源热度：" + (f"{heat / 10000:.1f} 万" if heat >= 10000 else str(heat)))
        for text in meta:
            self._lbl(box, text, size=14, color=W_TEXT, anchor="w", pady=(8, 0))
        self._lbl(box, "榜单话题用于确定创作方向；文章中的事实与素材仍需单独核实。", size=14, color=W_TEXT, wrap=True, fill="x", pady=(16, 0))
        if item.get("url"):
            self._button(box, "查看来源", lambda: webbrowser.open(item["url"]), style="secondary", width=96, side=None).pack(side="bottom", anchor="w")

    def _choose_topic(self, item, advance=True):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        if self.topic != item:
            self.topic, self.idea, self.ideas = item, None, []
            self.style, self.styles = None, []
            self._invalidate()
        self._render_topics()
        self._render_ideas()
        self._render_styles()
        if advance:
            self._goto(2)

    # ------------------------------------------------------------------ 第二步
    def _build_two(self):
        frame = self.sections[2]
        self._title(frame, "选择原标题，提炼核心立意")
        topic = self._card(frame, padding=(20, 16), fill="x")
        self._button(topic, "重选原标题", lambda: self._goto(1), style="quiet", width=96, side="right", padx=(12, 0))
        self.topic_category = tk.Frame(topic, bg="white")
        self.topic_category.pack(side="right")
        copy = tk.Frame(topic, bg="white")
        copy.pack(side="left", fill="x", expand=True)
        self._lbl(copy, "榜单原标题", size=14, bold=True, color=W_MUTED, anchor="w")
        self.selected_topic = self._lbl(copy, "请先选择一条榜单原标题", size=18, bold=True, anchor="w", pady=(4, 0))
        settings = self._card(frame, padding=(20, 16), fill="x", pady=(20, 0))
        self.idea_count = tk.IntVar(master=self, value=3)
        self._lbl(settings, "生成条数", bold=True, side="left")
        self._input(settings, self.idea_count, 96, side="left", padx=(16, 8))
        self._lbl(settings, "条", side="left")
        self.primary_actions[2] = self._button(settings, "获取核心立意", lambda: self._analysis("ideas"), width=184, side="right", padx=0, tracked=True)
        split = tk.Frame(frame, bg=BG)
        split.pack(fill="both", expand=True, pady=(20, 0))
        self.idea_detail = self._card(split, padding=20, side="right", fill="y", padx=(16, 0))
        self.idea_detail.configure(width=414)
        self.idea_detail.pack_propagate(False)
        ideas = self._card(split, padding=0, side="left", fill="both", expand=True)
        head = tk.Frame(ideas, bg="white", padx=20, pady=16)
        head.pack(fill="x")
        self._lbl(head, "核心立意", size=18, bold=True, side="left")
        self.idea_badge = self._badge(head, "等待获取", "neutral", side="left", padx=(12, 0))
        self._button(head, "清空数据", self._clear_ideas, style="quiet", width=96, side="right", padx=0, tracked=True)
        self.idea_area = ScrollArea(ideas, bg="white", padx=20)
        self.idea_area.pack(fill="both", expand=True, pady=(0, 20))
        self.idea_box = self.idea_area.body
        self.idea_box.surface = self.idea_box
        self.log_states[2] = tk.Label(self, text="等待运行")
        self.logs[2] = self._hidden_log()

    def _clear_ideas(self):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        self.ideas, self.idea = [], None
        self._invalidate()
        self._render_ideas()

    def _analysis(self, kind):
        if not self.topic:
            raise ValueError("请先选择榜单原标题")
        count = self._number(self.idea_count if kind == "ideas" else self.style_count, "生成条数" if kind == "ideas" else "获取数量", 1, 20)
        self._start(kind, dict(title=self.topic["title"], labels=self.topic.get("labels", []), count=count), 2 if kind == "ideas" else 3)

    def _render_ideas(self):
        self._clear_box(self.idea_box)
        self.idea_badge.configure(text=f"{len(self.ideas)} 条" if self.ideas else "等待获取",
                                  bg=W_SOFT if self.ideas else W_SUBTLE, fg=GREEN if self.ideas else W_TEXT)
        if not self.ideas:
            self._empty(self.idea_box, "原标题已选定，等待提炼立意" if self.topic else "等待选择原标题",
                        "设置条数后点击“获取核心立意”。")
        selected = tk.IntVar(master=self, value=next((i for i, v in enumerate(self.ideas) if self.idea == v), -1))
        for index, item in enumerate(self.ideas):
            active = index == selected.get()
            card = self._card(self.idea_box, padding=16, bg=W_SOFT if active else "white",
                              border=GREEN if active else W_LINE, fill="x", pady=(0, 12))
            top = tk.Frame(card, bg=card.cget("bg"))
            top.pack(fill="x")
            row, radio = self._choice(top, f"立意 {index + 1:02}", selected, index,
                                      lambda value=item: self._choose_idea(value, advance=False))
            row.pack(side="left")
            self._badge(top, "已选" if active else "可选择", "soft" if active else "neutral", side="right")
            text = self._lbl(card, item["core_idea"], wrap=True, fill="x", pady=(12, 0))
            for widget in (card, top, text):
                widget.bind("<Button-1>", lambda e, control=radio: control.invoke())
        self._render_idea_detail()
        self._render_footers()

    def _render_idea_detail(self):
        box = self.idea_detail
        self._clear_box(box)
        self._lbl(box, "如何展开论证", size=20, bold=True, anchor="w")
        if not self.idea:
            self._lbl(box, "选择左侧立意后，在此查看论证思路与原标题关联。", size=14, color=W_TEXT, wrap=True, fill="x", pady=(16, 0))
            return
        angle = self.idea.get("angle", "")
        if angle and len(angle) <= 24:
            self._lbl(box, angle, size=20, bold=True, wrap=True, fill="x", pady=(16, 0))
            self._lbl(box, self.idea["core_idea"], wrap=True, fill="x", pady=(12, 0))
        else:
            self._lbl(box, self.idea["core_idea"], size=20, bold=True, wrap=True, fill="x", pady=(16, 0))
            if angle:
                self._lbl(box, angle, wrap=True, fill="x", pady=(12, 0))
        self._divider(box, pady=16)
        self._lbl(box, "与原标题的关联", size=14, bold=True, color=W_MUTED, anchor="w")
        if self.idea.get("reason"):
            self._lbl(box, self.idea["reason"], wrap=True, fill="x", pady=(8, 0))
        for label in (self.topic or {}).get("labels", [])[:2]:
            self._badge(box, label, "soft", anchor="w", pady=(12, 0))
        self._lbl(box, "重新选择立意会保留当前写作风格。", size=14, color=W_TEXT, side="bottom", anchor="w")

    def _choose_idea(self, value, advance=True):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        self.idea = value
        self._invalidate()
        self._render_ideas()
        if advance:
            destination = 4 if self.reset_target == "idea" and self.style else 3
            self.reset_target = None
            self._goto(destination)
        elif self.reset_target == "idea" and self.style:
            self.reset_target = None
            self._goto(4)

    # ------------------------------------------------------------------ 第三步
    def _build_three(self):
        frame = self.sections[3]
        self._title(frame, "获取并选择写作风格", "常用风格优先，其余按使用次数排序；选择后可查看完整说明。")
        settings = self._card(frame, padding=(20, 16), fill="x")
        self.style_source = tk.StringVar(master=self, value="title")
        self.source_cards = {}
        for key, name in (("title", "根据原标题获取"), ("stored", "从已有风格中选择")):
            row, radio = self._choice(settings, name, self.style_source, key, self._source_changed)
            row.pack(side="left", padx=(0, 24))
            self.source_cards[key] = row
        self.style_count = tk.IntVar(master=self, value=5)
        self.writing_button = self._button(settings, "获取写作风格", self._get_styles, width=184, side="right", padx=0, tracked=True)
        self.primary_actions[3] = self.writing_button
        self._input(settings, self.style_count, 88, side="right", padx=(12, 16))
        self._lbl(settings, "获取数量", size=14, color=W_TEXT, side="right")
        self.style_topic = tk.Label(self)
        split = tk.Frame(frame, bg=BG)
        split.pack(fill="both", expand=True, pady=(20, 0))
        listing = self._card(split, padding=0, side="left", fill="y")
        listing.configure(width=380)
        listing.pack_propagate(False)
        head = tk.Frame(listing, bg="white", padx=20, pady=16)
        head.pack(fill="x")
        self._lbl(head, "写作风格", size=18, bold=True, side="left")
        self.style_badge = self._badge(head, "等待获取", "neutral", side="left", padx=(12, 0))
        self._button(head, "清空数据", self._clear_styles, style="quiet", width=96, side="right", padx=0, tracked=True)
        self.favorite_note = self._lbl(listing, "", size=14, color=W_TEXT, anchor="w", padx=20, pady=(0, 12))
        self.style_area = ScrollArea(listing, bg="white", padx=20)
        self.style_area.pack(fill="both", expand=True, pady=(0, 20))
        self.style_box = self.style_area.body
        self.style_box.surface = self.style_box
        self.style_detail = self._card(split, padding=20, side="left", fill="both", expand=True, padx=(16, 0))
        self.log_states[3] = tk.Label(self, text="等待运行")
        self.logs[3] = self._hidden_log()

    def _source_changed(self):
        self.writing_button.configure(text="获取已有风格" if self.style_source.get() == "stored" else "获取写作风格")
        # 切换来源会清空本次结果/选择；持久风格库不变。
        self._clear_styles()

    def _get_styles(self):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        if self.style_source.get() == "stored":
            self.styles = self.service.stored_styles(self._number(self.style_count, "获取数量", 1, 20))
            self._persist()
            self._render_styles()
            self._show_feedback(3, f"已获取 {len(self.styles)} 条已有写作风格，常用风格优先，其余按使用次数排序。")
            self._goto(3)
        else:
            self._analysis("styles")

    def _clear_styles(self):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        self.styles, self.style = [], None
        self._invalidate()
        self._render_styles()

    def _stored_styles(self):
        try:
            return {v["id"]: v for v in self.service.stored_styles(10000)}
        except Exception:
            return {}

    def _render_styles(self):
        self._clear_box(self.style_box)
        stored = self._stored_styles()
        favorites = sum(v.get("favorite", False) for v in stored.values())
        self.favorite_note.configure(text=f"常用 {favorites} / 5 · 最多可设 5 个")
        self.style_badge.configure(text=f"{len(self.styles)} 条" if self.styles else "等待获取",
                                   bg=W_SOFT if self.styles else W_SUBTLE, fg=GREEN if self.styles else W_TEXT)
        if not self.styles:
            stored_source = self.style_source.get() == "stored"
            self._empty(self.style_box, "尚未获取写作风格",
                        "点击“获取已有风格”读取风格库。" if stored_source else "点击“获取写作风格”，\n根据原标题生成可选风格。")
        selected = tk.IntVar(master=self, value=next((i for i, v in enumerate(self.styles) if self.style and v["writing_style"] == self.style["writing_style"]), -1))
        for index, item in enumerate(self.styles):
            active = index == selected.get()
            card = self._card(self.style_box, padding=16, bg=W_SOFT if active else "white",
                              border=GREEN if active else W_LINE, fill="x", pady=(0, 8))
            row, radio = self._choice(card, item["style_name"], selected, index,
                                      lambda value=item: self._choose_style(value, advance=False), bold=active)
            row.pack(fill="x")
            summary = self._lbl(card, "", size=14, color=W_TEXT, anchor="w", fill="x", pady=(8, 0))
            summary.configure(text=self._clip(summary, item["writing_style"].splitlines()[0], 300))
            info = stored.get(item.get("id"), {})
            uses = info.get("use_count", info.get("uses", item.get("use_count")))
            meta = " · ".join(v for v in ("常用" if info.get("favorite") else "", f"使用 {uses} 次" if uses is not None else "") if v)
            widgets = [card, summary]
            if meta:
                widgets.append(self._lbl(card, meta, size=14, color=W_MUTED, anchor="w", pady=(8, 0)))
            for widget in widgets:
                widget.bind("<Button-1>", lambda e, control=radio: control.invoke())
        self._render_style_detail(stored)
        self._render_footers()

    def _render_style_detail(self, stored):
        box = self.style_detail
        self._clear_box(box)
        item = self.style
        if not item:
            self._empty(box, "尚未选择写作风格", "从左侧列表选择一种风格后查看完整说明。")
            return
        head = tk.Frame(box, bg="white")
        head.pack(fill="x")
        favorite = stored.get(item.get("id"), {}).get("favorite", False)
        if item.get("id"):
            self._button(head, "已设常用" if favorite else "设为常用", lambda: self._favorite(item, not favorite),
                         style="secondary", width=96, side="right", padx=0)
        self._lbl(head, item["style_name"], size=22, bold=True, side="left")
        self._lbl(box, "写作风格", size=14, bold=True, color=W_MUTED, anchor="w", pady=(16, 8))
        self._lbl(box, item["writing_style"], wrap=True, fill="x")
        self._divider(box, pady=16)
        cols = tk.Frame(box, bg="white")
        cols.pack(fill="x")
        for i, name in enumerate(("核心标签", "对话对象")):
            cols.columnconfigure(i, weight=1, uniform="style")
            col = tk.Frame(cols, bg="white")
            col.grid(row=0, column=i, sticky="nsew", padx=(0, 16) if i == 0 else 0)
            self._lbl(col, name, size=14, bold=True, color=W_MUTED, anchor="w", pady=(0, 8))
            if i == 0:
                tags = tk.Frame(col, bg="white")
                tags.pack(fill="x")
                for tag in item.get("core_tags", [])[:4]:
                    self._badge(tags, tag, "soft", side="left", padx=(0, 8))
            else:
                self._lbl(col, item.get("audience", ""), wrap=True, fill="x")
        self._divider(box, pady=16)
        self._lbl(box, "风格优点 / 核心抓手", size=14, bold=True, color=W_MUTED, anchor="w", pady=(0, 4))
        for i, value in enumerate(item.get("strengths_or_hooks", [])[:4], 1):
            self._lbl(box, f"{i}. {value}", wrap=True, fill="x", pady=(4, 0))
        bar = tk.Frame(box, bg=W_SOFT, padx=12, pady=12)
        bar.pack(side="bottom", fill="x")
        self._badge(bar, "当前选用", "soft", side="left").configure(bg="white")
        self._lbl(bar, "将用于三个方向的文章创作", size=14, color=GREEN, side="left", padx=(12, 0))

    def _favorite(self, value, enabled):
        self.service.favorite(value["id"], enabled)
        self._render_styles()

    def _choose_style(self, value, advance=True):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        if not self.idea:
            raise ValueError("请先选择核心立意")
        self.style = value
        back = self.reset_target == "style"
        self.reset_target = None
        self._invalidate()
        self._render_styles()
        if advance or back:
            self._goto(4)

    # ------------------------------------------------------------------ 第四步
    def _build_four(self):
        frame = self.sections[4]
        self._title(frame, "生成三稿文章", "基于同一原标题、核心立意与写作风格，分别创作 1–3 个方向。")
        self.anchor_box = self._card(frame, padding=20, fill="x")
        self.draft_form = self.anchor_box
        caption = tk.Frame(frame, bg=BG)
        caption.pack(fill="x", pady=(20, 0))
        self._lbl(caption, "选择生成方向", bold=True, side="left")
        self._lbl(caption, "可多选", size=14, color=W_TEXT, side="left", padx=(12, 0))
        self.direction_count = self._lbl(caption, "", size=14, color=GREEN, side="right")
        options = tk.Frame(frame, bg=BG)
        options.pack(fill="x", pady=(12, 0))
        self.directions, self.direction_cards = {}, {}
        for index, (key, label) in enumerate(DIRECTIONS.items()):
            options.columnconfigure(index * 2, weight=1, uniform="direction")
            if index:
                options.columnconfigure(index * 2 - 1, minsize=12)
            card = self._card(options, padding=16)
            card.grid(row=0, column=index * 2, sticky="nsew")
            self.direction_cards[key] = card
            self.directions[key] = tk.BooleanVar(master=self, value=True)
            row, check = self._choice(card, label, self.directions[key], kind="check")
            row.pack(fill="x")
            self.direction_badges = getattr(self, "direction_badges", {})
            badge = tk.Label(row, font=font(14, True), padx=10, pady=4)
            badge._keep_bg = True
            badge._anchor = check
            self.direction_badges[key] = badge
            note = self._lbl(card, DIRECTION_NOTES.get(key, ""), size=14, color=W_TEXT, wrap=True, fill="x", pady=(10, 0))
            for widget in (card, note):
                widget.bind("<Button-1>", lambda e, control=check: control.invoke())
            self.directions[key].trace_add("write", lambda *_, k=key: self._direction_changed(k))
        length = self._card(frame, padding=(20, 16), fill="x", pady=(20, 0))
        self.length_card = length
        self._lbl(length, "每稿字数", bold=True, side="left")
        self.word_min, self.word_max = tk.IntVar(master=self, value=1000), tk.IntVar(master=self, value=1200)
        self._input(length, self.word_min, 112, side="left", padx=(16, 8))
        self._lbl(length, "至", side="left")
        self._input(length, self.word_max, 112, side="left", padx=8)
        self._lbl(length, "字", side="left")
        self._lbl(length, "输入变更后，旧稿保留为历史版本。", size=14, color=W_TEXT, side="right")
        for variable in (self.word_min, self.word_max):
            variable.trace_add("write", lambda *_: self._render_footers())
        log = self._log_box(frame, 4, "文章生成日志")
        log.pack(fill="both", expand=True, pady=(20, 0))
        self.write_log_card = log
        for key in self.directions:
            self._direction_changed(key)

    def _direction_changed(self, key):
        card = self.direction_cards[key]
        selected = self.directions[key].get()
        card.configure(highlightbackground=GREEN if selected else W_LINE, highlightcolor=GREEN if selected else W_LINE)
        self._paint(card, W_SOFT if selected else "white")
        self.direction_count.configure(text=f"已选 {sum(v.get() for v in self.directions.values())} 个方向")
        if len(self.directions) == len(DIRECTIONS) and hasattr(self, "word_max"):
            self._render_footers()

    def _render_anchor(self):
        self._clear_box(self.anchor_box)
        self.selected_topic.configure(text=self.topic["title"] if self.topic else "请先在第一步选择榜单原标题")
        self._clear_box(self.topic_category)
        for label in (self.topic or {}).get("labels", [])[:1]:
            self._badge(self.topic_category, label, "soft", side="left")
        rows = (("榜单原标题", None), ("核心立意", "idea"), ("写作风格", "style"))
        for label, reset in rows:
            if reset:
                self._divider(self.anchor_box, pady=12)
            row = tk.Frame(self.anchor_box, bg="white")
            row.pack(fill="x")
            caption = tk.Frame(row, bg="white", width=100, height=24)
            caption.pack(side="left", anchor="n")
            caption.pack_propagate(False)
            tk.Label(caption, text=label, bg="white", fg=W_MUTED, font=font(14, True), anchor="w").pack(fill="both")
            if reset:
                self._button(row, "重新设定", lambda value=reset: self._reset(value), style="quiet", width=96, side="right", padx=(16, 0))
            copy = tk.Frame(row, bg="white")
            copy.pack(side="left", fill="x", expand=True, padx=(16, 0))
            if reset is None:
                self._lbl(copy, self.topic["title"] if self.topic else "尚未选择原标题", size=18, bold=True, wrap=True, fill="x")
            elif reset == "idea":
                self._lbl(copy, self.idea["core_idea"] if self.idea else "尚未选择核心立意", wrap=True, fill="x")
            elif self.style:
                self._lbl(copy, self.style["style_name"], bold=True, anchor="w")
                desc = self._lbl(copy, "", size=14, color=W_TEXT, fill="x")
                desc.configure(text=self._clip(desc, self.style["writing_style"].splitlines()[0], 640))
            else:
                self._lbl(copy, "尚未选择写作风格", anchor="w")
        self._render_footers()

    def _reset(self, target):
        if self.runner.busy:
            raise ValueError("请先等待当前任务结束")
        self.reset_target = target
        self._goto(2 if target == "idea" else 3)

    def _generate(self):
        if not self.topic or not self.idea or not self.style:
            raise ValueError("请先选择原标题、核心立意和写作风格")
        low, high = self._number(self.word_min, "最少字数", 100, 20000), self._number(self.word_max, "最多字数", 100, 20000)
        if low > high:
            raise ValueError("最少字数不能大于最多字数")
        directions = [k for k, v in self.directions.items() if v.get()]
        if not directions:
            raise ValueError("请至少选择一个生成方向")
        self._start("write", dict(anchor=dict(title=self.topic["title"], core_idea=self.idea["core_idea"], writing_style=self.style,
                    evidence="", origins={"board": self.topic}), words=[low, high], directions=directions), 4)

    # ------------------------------------------------------------------ 日志
    def _log_box(self, parent, step, title):
        card = self._card(parent, padding=(20, 16))
        head = tk.Frame(card, bg="white")
        head.pack(fill="x")
        self._lbl(head, title, bold=True, side="left")
        self.log_states[step] = self._badge(head, "等待运行", "soft", side="right")
        box = tk.Text(card, height=3, bg="white", fg=W_TEXT, relief="flat", highlightthickness=0, wrap="word",
                      font=font(14), padx=0, pady=0, spacing1=6, spacing3=6, cursor="arrow")
        gap = 96
        box.configure(tabs=(gap,))
        box.tag_configure("time", foreground=W_MUTED)
        box.tag_configure("message", foreground=W_TEXT, lmargin2=gap)
        box.insert("end", "就绪\t", "time")
        box.insert("end", "任务启动后显示实际阶段与运行记录。", "message")
        box.configure(state="disabled")
        box.pack(fill="both", expand=True, pady=(8, 0))
        box._rules = []
        self.logs[step] = box
        card.surface = card
        return card

    def _append_log(self, step, value):
        box = self.logs.get(step)
        if not box or not box.winfo_exists():
            return
        state = self.log_states[step]
        box.configure(state="normal")
        if state.cget("text") == "等待运行":
            box.delete("1.0", "end")
        elif box.get("1.0", "end-1c").strip():
            box.insert("end", "\n")
        box.insert("end", value["time"][11:19] + "\t", "time")
        box.insert("end", value["message"], "message")
        box.see("end")
        box.configure(state="disabled")
        text = {"complete": "已完成", "failed": "失败", "cancelled": "已停止", "partial": "部分完成"}.get(value.get("status"), "运行中")
        kind = {"已完成": "ok", "失败": "error", "部分完成": "warn", "已停止": "neutral"}.get(text, "warn")
        bg, fg = BADGES[kind]
        state.configure(text=text, bg=bg, fg=fg)
        if step == 4 and value.get("direction") in DIRECTIONS:
            self._direction_badge(value["direction"], value.get("status", "running"), value.get("message", ""))
        if step == 5 and hasattr(self, "_merge_log_expand"):
            self._merge_log_expand(True)

    def _restore_log(self, step, task):
        for event in self.service.logs(task):
            self._append_log(step, event)

    # ------------------------------------------------------------------ 任务
    def _start(self, kind, data, step, resume=None):
        self.runner.start(kind, data, resume)
        self._job_kind, self._job_step = kind, step
        self.status.set({"boards": "正在获取匹配榜单…", "ideas": "正在提炼核心立意…", "styles": "正在获取写作风格…",
                         "write": "正在生成所选方向的文章…", "merge": "正在合并三稿…"}.get(kind, "正在处理…"))
        self._action_labels = {button: button.cget("text") for button in self.primary_actions.values() if button.winfo_exists()}
        if step in self.primary_actions and self.primary_actions[step].winfo_exists():
            self.primary_actions[step].configure(text={"boards": "正在获取…", "ideas": "正在获取…", "styles": "正在获取…",
                                                       "write": "正在生成文章…"}.get(kind, "正在处理…"))
        if kind == "write":
            self._running_task = resume
            self.log_states[4].configure(text="等待运行")  # 新一轮运行从空日志开始
            wanted = data.get("directions")
            if resume and not wanted:
                try:
                    wanted = self.service.task(resume)["snapshot"].get("directions")
                except Exception:
                    wanted = None
            done = {d["direction"] for d in self.service.results(resume)} if resume else set()
            for key in DIRECTIONS:
                self._direction_badge(key, ("complete" if key in done else "queued") if key in (wanted or DIRECTIONS) else None)
        self._set_busy(True)

    def _set_busy(self, busy):
        self._busy = busy
        if busy:
            self._locked_inputs = []
            def lock(parent):
                for child in parent.winfo_children():
                    if isinstance(child, (tk.Entry, tk.Radiobutton, tk.Checkbutton, ttk.Combobox)):
                        self._locked_inputs.append((child, child.cget("state")))
                        child.configure(state="disabled")
                    lock(child)
            lock(self)
        else:
            for widget, state in getattr(self, "_locked_inputs", []):
                if widget.winfo_exists():
                    widget.configure(state=state)
            self._locked_inputs = []
        self.task_buttons = [button for button in self.task_buttons if button.winfo_exists()]
        for button in self.task_buttons:
            button.configure(state="disabled" if busy else "normal")
        self._render_footers()
        self._show_footer()

    def _poll(self):
        if self._closed:
            return
        while True:
            try:
                kind, value = self.runner.events.get_nowait()
            except queue.Empty:
                break
            if kind == "log":
                self._append_log(self._job_step, value)
                self.status.set(value["message"])
                if value.get("task_id") and self._job_kind == "write":
                    self._running_task = value["task_id"]
                if self.runner.busy and not getattr(self, "footer_live", {}).get(self.current_step):
                    self.footer_label.configure(text=value["message"])
            else:
                self._set_busy(False)
                self._guard(lambda v=value: self._done(v))
        self._poll_id = self.after(100, self._poll)

    def _done(self, value):
        for button, label in getattr(self, "_action_labels", {}).items():
            if button.winfo_exists():
                button.configure(text=label)
        kind, task = value["kind"], value.get("task_id")
        if kind == "write" and task:
            self.write_task, self.merge_task = task, None
            self._render_empty_drafts(6)
            self._render_drafts(5, task)
            if self.service.results(task):
                self._goto(5)
        elif kind == "merge" and task and value.get("drafts"):
            self.merge_task = task
            self._render_drafts(6, task)
            self._goto(6)
        elif not value.get("error") and not value.get("cancelled"):
            if kind == "boards":
                self.rows = value["rows"]
                self.topic = self.idea = self.style = None
                self.ideas, self.styles = [], []
                self._invalidate()
                self._render_topics()
                self._render_categories()
                self._render_ideas()
                self._render_styles()
                self._goto(1)
                self._show_feedback(1, f"已返回 {len(self.rows)} 条榜单数据，请选择一个原标题。" if self.rows else "未找到匹配的原标题，请调整平台或主题方向后重新获取。")
            elif kind == "ideas":
                self.ideas = value["items"]
                self._render_ideas()
                self._goto(2)
                self._show_feedback(2, f"已获取 {len(self.ideas)} 条核心立意。" if self.ideas else "暂无可用立意，请调整条件后重试。")
            elif kind == "styles":
                self.styles = value["items"]
                self._render_styles()
                count = len(self.styles)
                self._goto(3)
                self._show_feedback(3, f"已获取 {count} 条写作风格。" + ("不足设定数量，已返回全部可用数据。" if count < self.style_count.get() else ""))
            elif kind in ("export", "illustrate"):
                if value.get("handoff"):
                    self.on_handoff(value["handoff"])
                else:
                    messagebox.showinfo("导出结果", f'成功导出 {len(value.get("paths", []))} 篇\n' + "\n".join(value.get("errors", [])), parent=self)
        self._persist()
        if value.get("error"):
            self.status.set(value["error"])
            self._show_feedback(self.current_step, value["error"], True)
            messagebox.showerror("任务未完成", value["error"], parent=self)
        elif value.get("errors"):
            self.status.set("部分操作失败，成功结果已保存，请查看日志并续跑")
        else:
            self.status.set("已停止，完成结果已保存" if value.get("cancelled") else "任务已完成")
        if kind == "write":
            self._sync_direction_badges()
        self._render_footers()

    # ------------------------------------------------------------------ 第五 / 六步
    def _render_empty_drafts(self, step):
        getattr(self, "_draft_footers", {}).pop(step, None)
        frame = self.sections[step]
        self._clear_box(frame)
        if step == 5:
            self._title(frame, "三稿文章处理")
            self.logs.pop(5, None)
        else:
            self._title(frame, "合并稿文章处理", "合并稿保留三稿中的有效增量，统一结构与表达。")
            self.logs[6] = self._hidden_log()
            self.log_states[6] = tk.Label(self, text="等待运行")
        card = self._card(frame, padding=20, fill="both", expand=True)
        self._empty(card, "尚未生成文章" if step == 5 else "尚未合并三稿",
                    "完成第四步“开始生成文章”后，在此选择标题并导出。" if step == 5 else "三稿全部完成后，在第五步点击“合并三稿”。")
        self._footer(step, "尚无可处理的稿件", [("上一步", lambda s=step: self._goto(s - 1), "secondary", 80)])

    def _context_card(self, parent, step, task, count, partial):
        card = self._card(parent, padding=20, side="right", fill="y", padx=(16, 0))
        card.configure(width=324)
        card.pack_propagate(False)
        self._lbl(card, "本次创作", size=20, bold=True, anchor="w")
        self._badge(card, f"{count} 稿已完成" if step == 5 else "三稿合并稿", "ok" if step == 5 else "soft", anchor="w", pady=(8, 0))
        anchor = {}
        try:
            source = self.write_task if step == 6 and self.write_task else task
            anchor = self.service.task(source).get("snapshot", {}).get("anchor", {}) or {}
        except Exception:
            anchor = {}
        title = anchor.get("title") or (self.topic or {}).get("title", "")
        idea = anchor.get("core_idea") or (self.idea or {}).get("core_idea", "")
        style = (anchor.get("writing_style") or self.style or {}).get("style_name", "")
        for index, (name, text, size, bold, color) in enumerate((("榜单原标题", title, 16, True, W_INK),
                                                                 ("核心立意", idea, 14, False, W_TEXT),
                                                                 ("写作风格", style, 16, True, W_INK))):
            if index:
                self._divider(card, pady=16)
            else:
                tk.Frame(card, bg="white", height=16).pack()
            self._lbl(card, name, size=14, bold=True, color=W_MUTED, anchor="w", pady=(0, 8))
            self._lbl(card, text, size=size, bold=bold, color=color, wrap=True, fill="x")
        if partial:
            missing = [DIRECTIONS[d] for d in partial]
            self._button(card, f"继续生成{'、'.join(missing)}" if len(missing) == 1 else "继续生成未完成稿",
                         lambda: self._start("write", {}, 4, resume=task), style="secondary", side=None,
                         tracked=True).pack(side="bottom", anchor="w", pady=(16, 0))
        self._lbl(card, "批量导出使用每稿各自选中的标题。生成图文稿只处理当前显示的一篇。" if step == 5 else
                  "导出与生成图文稿使用合并稿选中的标题。", size=14, color=W_TEXT, wrap=True, side="bottom", fill="x")
        return card

    def _render_drafts(self, step, task):
        frame = self.sections[step]
        self._clear_box(frame)
        results = self.service.results(task)
        state = self.service.task(task) if step == 5 else {}
        partial = None
        if step == 5 and state.get("status") in ("partial", "failed", "cancelled", "interrupted"):
            wanted = state.get("snapshot", {}).get("directions") or list(DIRECTIONS)
            done = {d["direction"] for d in results}
            partial = [d for d in wanted if d not in done and d in DIRECTIONS] or ["similarity"]
        if step == 5:
            self._title(frame, "三稿文章处理", badge=f"{len(results)} 稿已完成" if results else None)
        else:
            self._title(frame, "合并稿文章处理", "合并稿保留三稿中的有效增量，统一结构与表达。")
            self.logs[6] = self._hidden_log()
            self.log_states[6] = tk.Label(self, text="等待运行")
        merge_bar = None
        if step == 5:
            merge_bar = self._card(frame, padding=0, side="bottom", fill="x", pady=(20, 0))
            self._merge_log(merge_bar)
        split = tk.Frame(frame, bg=BG)
        split.pack(fill="both", expand=True)
        self._context_card(split, step, task, len(results), partial)
        shell = self._card(split, padding=0, side="left", fill="both", expand=True)
        header = tk.Frame(shell, bg=W_SUBTLE, height=56, padx=16)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Frame(shell, bg=W_LINE, height=1).pack(fill="x")
        book = tk.Frame(shell, bg="white", padx=20, pady=20)
        book.pack(fill="both", expand=True)
        if not results:
            self._empty(book, "尚无完成稿", "可在右侧继续生成未完成稿。")
            self._footer(step, "尚无完成稿", [("上一步", lambda: self._goto(4), "secondary", 80)])
            if step == 5 and self.merge_task:
                self._restore_log(5, self.merge_task)
            return
        panels, tabs = [], []
        if step == 5:
            self._button(header, "导出全部稿件", lambda: self._export_dialog(task, [d["direction"] for d in results]),
                         style="secondary", side="right", padx=0, tracked=True)
        else:
            self._lbl(header, "三稿合并稿", size=18, bold=True, side="left")
            self._badge(header, "合并完成", "ok", side="left", padx=(12, 0))
        complete = step == 5 and {d["direction"] for d in results} == set(DIRECTIONS)

        def activate(index):
            for i, panel in enumerate(panels):
                panel.pack_forget()
                if tabs:
                    self._style_button(tabs[i], "tabActive" if i == index else "quiet")
            panels[index].pack(fill="both", expand=True)
            direction = results[index]["direction"]
            self.current_draft[step] = direction
            name = DIRECTIONS.get(direction, "三稿合并稿") if step == 5 else "三稿合并稿"
            buttons = [("导出本稿", lambda d=direction: self._export_dialog(task, [d]), "primary", 144),
                       ("生成图文稿", lambda d=direction: self._illustrate(task, d), "primary", 144)]
            if step == 5:
                merging = self._busy and self._job_kind == "merge"
                if merging or (complete and self.merge_task):
                    if merging:
                        buttons.insert(0, ("停止合并", self.runner.cancel, "secondary", 96, True, True))
                    buttons.append(("查看合并结果", self._view_merge, "primary", 144, True, True))
                elif complete:
                    buttons.append(("合并三稿", lambda: self._start("merge", dict(source_task=task), 5), "primary", 144))
                self._footer(5, f"当前稿：{name} · 标题选择已保存", buttons)
            else:
                self._footer(6, "当前稿：三稿合并稿 · 已自动保存",
                             [("返回三稿", lambda: self._goto(5), "secondary", 96)] + buttons)

        for draft in results:
            direction = draft["direction"]
            index = len(panels)
            if step == 5:
                tab = self._button(header, DIRECTIONS.get(direction, direction), lambda i=index: activate(i),
                                   style="quiet", side="left", padx=(0, 8))
                tab.pack_configure(pady=8)
                def move_tab(event, i=index):
                    target = 0 if event.keysym == "Home" else len(panels) - 1 if event.keysym == "End" else (i + (1 if event.keysym == "Right" else -1)) % len(panels)
                    activate(target)
                    tabs[target].focus_set()
                    return "break"
                for key in ("<Left>", "<Right>", "<Home>", "<End>"):
                    tab.bind(key, move_tab)
                tabs.append(tab)
            panel = tk.Frame(book, bg="white")
            panels.append(panel)
            caption = tk.Frame(panel, bg="white")
            caption.pack(fill="x", pady=(0, 10))
            self._lbl(caption, "候选标题", size=14, bold=True, color=W_MUTED, side="left")
            self._lbl(caption, "每稿选择 1 个标题", size=14, color=W_TEXT, side="right")
            selected = tk.IntVar(master=self, value=draft["selected"])
            title_cards = []
            titles = tk.Frame(panel, bg="white")
            titles.pack(fill="x")
            bar = tk.Frame(panel, bg=W_SUBTLE, height=48, padx=16, highlightthickness=1, highlightbackground=W_LINE)
            bar.pack(fill="x", pady=(10, 0))
            bar.pack_propagate(False)
            self._lbl(bar, "预览文章", bold=True, color=GREEN, side="left")
            preview = tk.Frame(panel, bg="white", highlightthickness=1, highlightbackground=W_LINE)
            heading = self._lbl(preview, draft["titles"][draft["selected"]], size=18, bold=True, wrap=True, fill="x", padx=16, pady=(12, 4))
            body = tk.Text(preview, height=6, wrap="word", bg="white", fg=W_TEXT, relief="flat", highlightthickness=0,
                           font=font(16), padx=16, pady=8, spacing1=4, spacing3=4)
            body.tag_configure("heading", font=font(16, True), foreground=W_INK, spacing1=10)
            for line in draft["body"].splitlines():
                body.insert("end", (line[4:] if line.startswith("### ") else line) + "\n", "heading" if line.startswith("### ") else "body")
            body.configure(state="disabled")
            body.pack(fill="both", expand=True)
            toggle_button = tk.Button(bar, text="展开", bg=W_SUBTLE, activebackground=W_SOFT, fg=GREEN, activeforeground=GREEN,
                                      font=font(14), bd=0, relief="flat", cursor="hand2")
            toggle_button.pack(side="right")
            def toggle(box=preview, button=toggle_button, rows=titles):
                if box.winfo_manager():
                    box.pack_forget()
                    rows.pack(fill="x", before=box._bar)
                    button.configure(text="展开")
                else:
                    rows.pack_forget()
                    box.pack(fill="both", expand=True, pady=(10, 0))
                    button.configure(text="收起")
            toggle_button.configure(command=toggle)
            preview._bar, preview._toggle = bar, toggle_button
            for widget in (bar,) + tuple(bar.winfo_children()[:1]):
                widget.bind("<Button-1>", lambda e, b=toggle_button: b.invoke())
            for i, title in enumerate(draft["titles"]):
                active = i == selected.get()
                card = tk.Frame(titles, bg=W_SOFT if active else "white", height=56, padx=16,
                                highlightthickness=1, highlightbackground=GREEN if active else W_LINE)
                card.pack(fill="x", pady=(0, 10) if i < len(draft["titles"]) - 1 else 0)
                card.pack_propagate(False)
                row, radio = self._choice(card, title, selected, i, bold=active)
                row.pack(fill="x", expand=True)
                card.bind("<Button-1>", lambda e, control=radio: control.invoke())
                title_cards.append((card, radio))
                def choose(t=task, d=direction, var=selected, label=heading, titles=draft["titles"], cards=title_cards):
                    self.service.select_title(t, d, var.get())
                    label.configure(text=titles[var.get()])
                    for k, (content, control) in enumerate(cards):
                        on = k == var.get()
                        content.configure(highlightbackground=GREEN if on else W_LINE)
                        self._paint(content, W_SOFT if on else "white")
                        control.text_label.configure(font=font(16, on))
                radio.configure(command=lambda fn=choose: self._guard(fn))
        activate(0)
        self._draft_footers = getattr(self, "_draft_footers", {})
        self._draft_footers[step] = lambda: activate(next((i for i, d in enumerate(results)
                                                           if d["direction"] == self.current_draft.get(step)), 0))
        if step == 5 and self.merge_task:
            self._restore_log(5, self.merge_task)

    def _view_merge(self):
        """合并中展开日志；合并完成后进入第六步。"""
        if self._busy and self._job_kind == "merge":
            if hasattr(self, "_merge_log_expand"):
                self._merge_log_expand(True)
            return
        if self.merge_task:
            self._goto(6)

    def _merge_log(self, card):
        head = tk.Frame(card, bg="white", height=48, padx=16, cursor="hand2")
        head.pack(fill="x")
        head.pack_propagate(False)
        self._lbl(head, "三稿合并日志", bold=True, side="left")
        state = self._lbl(head, "未运行", size=14, color=W_TEXT, side="right")
        state._keep_bg = False
        body = tk.Frame(card, bg="white", height=132, padx=16)
        body.pack_propagate(False)
        box = tk.Text(body, height=4, bg="white", fg=W_TEXT, relief="flat", highlightthickness=0, wrap="word",
                      font=font(14), padx=0, pady=0, spacing1=6, spacing3=6, tabs=(96,), cursor="arrow")
        box.tag_configure("time", foreground=W_MUTED)
        box.tag_configure("message", foreground=W_TEXT, lmargin2=96)
        box.pack(fill="both", expand=True, pady=(0, 12))
        box.configure(state="disabled")
        box._rules = []
        self.logs[5] = box

        class StateLabel:
            """合并日志折叠栏的状态文字（非徽标）。"""
            def __init__(self, label):
                self.label, self.text = label, "等待运行"
            def cget(self, key):
                return self.text
            def configure(self, text=None, bg=None, fg=None, **_):
                if text:
                    self.text = text
                if self.text == "等待运行":
                    label.configure(text="未运行", bg="white", fg=W_TEXT, font=font(14), padx=0, pady=0)
                else:
                    label.configure(text=self.text, bg=bg or W_WARN_BG, fg=fg or W_WARN, font=font(14, True), padx=10, pady=4)
            config = configure
        label = state
        self.log_states[5] = StateLabel(state)

        def expand(show=None):
            show = not body.winfo_manager() if show is None else show
            if show and not body.winfo_manager():
                tk.Frame(card, bg=W_LINE, height=1).pack(fill="x")
                body.pack(fill="x")
            elif not show and body.winfo_manager():
                for child in card.winfo_children():
                    if child not in (head, body):
                        child.destroy()
                body.pack_forget()
        self._merge_log_expand = expand
        for widget in (head,) + tuple(head.winfo_children()):
            widget.bind("<Button-1>", lambda e: expand())

    # ------------------------------------------------------------------ 对话框
    def _dialog(self, title, width, height):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.configure(bg="white")
        dialog.geometry(f"{width}x{height}")
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.bind("<Escape>", lambda event: dialog.destroy())
        frame = tk.Frame(dialog, bg="white", padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        dialog.update_idletasks()
        host = self.winfo_toplevel()
        dialog.geometry(f"+{host.winfo_rootx() + max(0, (host.winfo_width() - width) // 2)}+{host.winfo_rooty() + max(0, (host.winfo_height() - height) // 2)}")
        try:
            dialog.grab_set()
        except tk.TclError:
            pass
        return dialog, frame

    def _illustrate(self, task, direction):
        if self.runner.busy:
            raise ValueError("当前任务尚未结束")
        draft = next((d for d in self.service.results(task) if d["direction"] == direction), None)
        dialog, frame = self._dialog("准备生成图文稿", 560, 386)
        self.handoff_dialog = dialog
        self._lbl(frame, "准备生成图文稿", size=20, bold=True, anchor="w")
        self._lbl(frame, "只处理当前选中的一篇文章", size=14, color=W_TEXT, anchor="w", pady=(4, 16))
        self._badge(frame, DIRECTIONS.get(direction, "三稿合并稿") if task == self.write_task else "三稿合并稿", "soft", anchor="w")
        if draft:
            self._lbl(frame, draft["titles"][draft["selected"]], size=20, bold=True, wrap=True, fill="x", pady=(12, 0))
        self._divider(frame, pady=16)
        self._lbl(frame, "1. 按所选格式保存本稿\n2. 基于同一正文准备 DOCX 与配图计划\n3. 进入“图文生成”继续配图与排版",
                  color=W_INK, anchor="w")
        self._lbl(frame, "取消导出或保存失败时，保留在当前页面。", size=14, color=W_TEXT, anchor="w", pady=(12, 0))
        row = tk.Frame(frame, bg="white")
        row.pack(side="bottom", fill="x")
        def proceed():
            dialog.destroy()
            self._export_dialog(task, [direction], True)
        self._button(row, "保存并继续", proceed, side="right", padx=0, width=144)
        self._button(row, "取消", dialog.destroy, style="secondary", side="right", padx=(0, 12), width=80)
        return dialog

    def _export_dialog(self, task, directions, illustrate=False):
        if self.runner.busy:
            raise ValueError("当前任务尚未结束")
        dialog, frame = self._dialog("保存文章并准备图文任务" if illustrate else "导出文章", 560, 476)
        self._lbl(frame, "导出文章", size=20, bold=True, anchor="w")
        self._lbl(frame, f"选择导出格式与保存位置 · 共 {len(directions)} 稿", size=14, color=W_TEXT, anchor="w", pady=(4, 16))
        fmt = tk.StringVar(master=self, value="docx")
        for key, name in (("docx", "Word 文档（.docx）"), ("md", "Markdown（.md）")):
            row, radio = self._choice(frame, name, fmt, key)
            row.pack(fill="x", pady=(0, 12))
        self._divider(frame, pady=(4, 16))
        self._lbl(frame, "导出目录", bold=True, anchor="w", pady=(0, 8))
        directory = tk.StringVar(master=self, value=self.service.export_directory())
        row = tk.Frame(frame, bg="white")
        row.pack(fill="x")
        self._input(row, directory, 356, side="left")
        def choose():
            value = filedialog.askdirectory(parent=dialog, initialdir=directory.get(), mustexist=True)
            if value:
                directory.set(value)
        self._button(row, "选择目录", choose, style="secondary", side="left", padx=(12, 0), width=96)
        self._lbl(frame, "首次默认系统桌面；修改后记住上次目录。", size=14, color=W_TEXT, anchor="w", pady=(8, 0))
        rule = tk.Label(frame, text="同名文件自动避让；全部导出使用每稿选中的标题。", bg=W_SUBTLE, fg=W_TEXT,
                        font=font(14), anchor="w", padx=12, pady=10)
        rule.pack(fill="x", pady=(16, 0))
        row = tk.Frame(frame, bg="white")
        row.pack(side="bottom", fill="x")
        def confirm():
            data = self.service.export_request(task, directions, directory.get(), fmt.get(), illustrate)
            self._start("illustrate" if illustrate else "export", data, 5 if task == self.write_task else 6)
            dialog.destroy()
        self._button(row, "确认导出", confirm, side="right", padx=0, width=144)
        self._button(row, "取消", dialog.destroy, style="secondary", side="right", padx=(0, 12), width=80)
        self.export_dialog = dialog
        return dialog

    def _history(self):
        dialog = tk.Toplevel(self)
        dialog.title("任务历史与恢复")
        dialog.geometry("690x420")
        tree = ttk.Treeview(dialog, columns=("time", "kind", "status"), show="headings")
        for key, label in (("time", "创建时间"), ("kind", "任务"), ("status", "状态")):
            tree.heading(key, text=label)
        tree.pack(fill="both", expand=True)
        for task in self.service.history():
            if task["kind"] in ("write", "merge"):
                tree.insert("", "end", iid=task["id"], values=(task["created_at"], task["snapshot"].get("anchor", {}).get("title", "三稿合并"), task["status"]))
        def open_task():
            if self.runner.busy:
                raise ValueError("请等待当前任务结束")
            if not tree.selection():
                return
            task = self.service.task(tree.selection()[0])
            if task["kind"] == "write":
                snap = task["snapshot"]
                self.topic = snap["anchor"]["origins"].get("board", {"id": "manual", "rank": 1, "source": "手动输入", "title": snap["anchor"]["title"]})
                self.idea = dict(core_idea=snap["anchor"]["core_idea"], angle="", reason="")
                self.style = snap["anchor"]["writing_style"]
                self.rows, self.ideas, self.styles = [self.topic], [self.idea], [self.style]
                self.word_min.set(snap["words"][0])
                self.word_max.set(snap["words"][1])
                for direction, var in self.directions.items():
                    var.set(direction in snap["directions"])
                self.write_task, self.merge_task = task["id"], None
                self.sections[6].pack_forget()
                self._render_topics()
                self._render_ideas()
                self._render_styles()
                self._render_anchor()
                self._sync_visibility()
                self._render_drafts(5, task["id"])
                self._goto(5)
                for event in self.service.logs(task["id"]):
                    self._append_log(4, event)
            else:
                self.merge_task = task["id"]
                self._render_drafts(6, task["id"])
                self._goto(6)
            self._persist()
            dialog.destroy()
        ttk.Button(dialog, text="打开所选任务", command=lambda: self._guard(open_task)).pack(pady=8)

    def _settings(self):
        if self.runner.busy:
            raise ValueError("请等待当前任务结束后再修改模型设置")
        dialog = tk.Toplevel(self)
        dialog.title("模块模型设置 · 留空沿用 API 连接设置")
        book = ttk.Notebook(dialog)
        book.pack(fill="both", expand=True, padx=14, pady=14)
        values = self.service.model_overrides()
        variables = {}
        for stage, name in (("research", "榜单分类与筛选"), ("analysis", "立意与风格"), ("writing", "写稿与合并"), ("illustration", "配图计划")):
            page = ttk.Frame(book, padding=16)
            book.add(page, text=name)
            variables[stage] = {}
            for row, (key, label) in enumerate((("base_url", "API 基础地址"), ("model", "模型名称"), ("api_key", "API Key"), ("wire_api", "协议 chat_completions / responses"), ("timeout", "超时秒数 10–900"))):
                ttk.Label(page, text=label).grid(row=row * 2, column=0, sticky="w", pady=(8, 2))
                var = tk.StringVar(master=self, value=str(values[stage].get(key, "")))
                variables[stage][key] = var
                ttk.Entry(page, textvariable=var, width=55, show="*" if key == "api_key" else "").grid(row=row * 2 + 1, column=0, sticky="ew")
        def save():
            data = {stage: {k: v.get().strip() for k, v in fields.items() if v.get().strip()} for stage, fields in variables.items()}
            self.service.save_model_overrides(data)
            dialog.destroy()
        ttk.Button(dialog, text="保存", command=lambda: self._guard(save)).pack(pady=8)

    def shutdown(self):
        if self._closed:
            return
        self._closed = True
        self.runner.cancel()
        self.after_cancel(self._poll_id)
        self.winfo_toplevel().unbind("<MouseWheel>", self._wheel_binding)
        self._persist()

    def destroy(self):
        if not self._closed:
            self.shutdown()
        super().destroy()
