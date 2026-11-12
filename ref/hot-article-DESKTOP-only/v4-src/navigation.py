# -*- coding: utf-8 -*-
"""U · 左侧深墨青导航栏视图。

职责：
- 构建界面原型中的左侧导航：品牌区、工作区导航项、账号状态卡；
- 把导航点击映射到主窗口既有行为（切换生成模式、定位列表 / 日志、
  打开设置弹窗）；
- 提供 ``set_active_mode()`` / ``set_pending_count()`` / ``refresh_status()``
  三个轻量刷新入口，由主窗口在状态变化时调用。

不负责：
- 不包含业务逻辑（不扫描目录、不做账号 I/O 之外的计算）；
- 不保存任何状态，激活态与计数都由主窗口驱动。

依赖：``ui.theme``（配色与字体）、``pipeline.accounts``（读默认账号展示信息）。

对外 API：
- ``NavigationRail``：导航栏构建器；``.frame`` 为最外层容器。
"""
from __future__ import annotations

from pathlib import Path
import tkinter as tk

from ui import theme


# 下载模式配置值 → 状态卡中文展示名（配置键不变，仅界面文案）
_DOWNLOAD_MODE_LABELS = {
    "browse": "浏览图",
    "original": "网页原图",
    "original_http": "原图下载",
}


NAV_ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "nav"
# 导航文案 → Figma 图标资源名（ui/assets/nav/<name>-<state>.png，源 SVG 同目录）。
NAV_ICONS = {
    "图文生成": "image_text",
    "AI 热度图文生成": "ai_hot_article",
    "头条发布": "toutiao_publish",
    "系统设置": "system_settings",
    "API 连接设置": "api_settings",
}


def _nav_icons(master, name: str | None) -> dict | None:
    """读取某导航项三态图标；资源缺失或 Tk 不可用时返回 ``None``。"""
    if not name:
        return None
    try:
        return {state: tk.PhotoImage(master=master, file=str(NAV_ICON_DIR / f"{name}-{state}.png"))
                for state in ("idle", "hover", "active")}
    except (tk.TclError, OSError):
        return None


class _NavItem:
    """导航项：36px 高的可点击行（图标位留白 + 文案 + 可选计数药丸）。"""

    def __init__(self, parent, text: str, command, *, count: str | None = None):
        self._command = command
        self.frame = tk.Frame(parent, bg=theme.RAIL_BG, height=36, cursor="hand2")
        self.frame.pack_propagate(False)

        # Figma 导航图标（19×21，按 闲置 / 悬停 / 激活 三态预渲染）；无对应资源时保留文案位置不变。
        self._icons = _nav_icons(parent, NAV_ICONS.get(text))
        self.icon = None
        if self._icons:
            self.icon = tk.Label(self.frame, image=self._icons["idle"], bg=theme.RAIL_BG,
                                 bd=0, padx=0, pady=0)
            self.icon.pack(side="left", padx=(10, 0))

        self.label = tk.Label(self.frame, text=text, bg=theme.RAIL_BG,
                              fg=theme.RAIL_TEXT_SECONDARY,
                              font=theme.sans_font(10), anchor="w")
        self.label.pack(side="left", fill="y", padx=(11 if self.icon else 10, 0))

        self.count = None
        if count is not None:
            self.count = tk.Label(self.frame, text=count, bg=theme.RAIL_HOVER,
                                  fg=theme.RAIL_TEXT_SECONDARY,
                                  font=theme.mono_font(9), padx=7, pady=1)
            self.count.pack(side="right", padx=(0, 10))

        self._active = False
        for widget in self._widgets():
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _widgets(self) -> tuple:
        """参与点击 / 悬停反馈的控件（行、文案、计数）。"""
        items = [self.frame, self.label]
        if self.icon is not None:
            items.append(self.icon)
        if self.count is not None:
            items.append(self.count)
        return tuple(items)

    def _on_click(self, _event=None) -> None:
        self._command()

    def _on_enter(self, _event=None) -> None:
        if self._active:
            return
        self.frame.configure(bg=theme.RAIL_HOVER)
        self.label.configure(bg=theme.RAIL_HOVER, fg=theme.RAIL_TEXT)
        self._paint_icon("hover", theme.RAIL_HOVER)
        if self.count is not None:
            self.count.configure(bg=theme.RAIL_HOVER)

    def _on_leave(self, _event=None) -> None:
        if self._active:
            return
        self.frame.configure(bg=theme.RAIL_BG)
        self.label.configure(bg=theme.RAIL_BG, fg=theme.RAIL_TEXT_SECONDARY)
        self._paint_icon("idle", theme.RAIL_BG)
        if self.count is not None:
            self.count.configure(bg=theme.RAIL_HOVER)

    def set_active(self, active: bool) -> None:
        """切换激活态（深墨青高亮 + 加粗）。"""
        self._active = bool(active)
        bg = theme.RAIL_ACTIVE if active else theme.RAIL_BG
        fg = theme.RAIL_TEXT if active else theme.RAIL_TEXT_SECONDARY
        self.frame.configure(bg=bg)
        self._paint_icon("active" if active else "idle", bg)
        self.label.configure(bg=bg, fg=fg,
                             font=theme.sans_font(10, "bold" if active
                                                  else "normal"))
        if self.count is not None:
            self.count.configure(
                bg=theme.RAIL_TEXT if active else theme.RAIL_HOVER,
                fg=theme.RAIL_ACTIVE if active else theme.RAIL_TEXT_SECONDARY)

    def _paint_icon(self, state: str, bg: str) -> None:
        if self.icon is not None:
            self.icon.configure(image=self._icons[state], bg=bg)

    def set_count(self, text: str | None) -> None:
        """更新计数药丸文案（``None`` 表示隐藏）。"""
        if self.count is None:
            return
        self.count.configure(text="" if text is None else str(text))
        if text is None:
            self.count.pack_forget()
        elif not self.count.winfo_manager():
            self.count.pack(side="right", padx=(0, 10))


class NavigationRail:
    """左侧导航栏（品牌 + 工作区导航 + 设置 + 当前账号状态卡）。"""

    WIDTH = 232

    def __init__(self, win, parent) -> None:
        self.win = win
        self.frame = tk.Frame(parent, bg=theme.RAIL_BG, width=self.WIDTH)
        self.frame.pack_propagate(False)
        self._items: dict[str, _NavItem] = {}

        self._build_brand()
        theme.divider(self.frame, bg=theme.RAIL_BORDER).pack(
            fill="x", padx=14, pady=(16, 14))
        tk.Label(self.frame, text="工作区", bg=theme.RAIL_BG,
                 fg=theme.RAIL_TEXT_TERTIARY, font=theme.sans_font(9),
                 anchor="w").pack(fill="x", padx=(22, 14), pady=(0, 8))

        nav_box = tk.Frame(self.frame, bg=theme.RAIL_BG)
        nav_box.pack(fill="x", padx=14)
        self._add_item(nav_box, "图文生成", self._on_doc_mode)
        self._add_item(nav_box, "AI 热度图文生成", lambda: self.win._show_hot_article_workspace())
        self._add_item(nav_box, "头条发布", self._on_toutiao)
        self._add_item(nav_box, "Relay 接单台", self._on_relay_console)
        self._add_item(nav_box, "系统设置", self._open_settings)

        tk.Frame(self.frame, bg=theme.RAIL_BG).pack(fill="both", expand=True)

        bottom = tk.Frame(self.frame, bg=theme.RAIL_BG)
        bottom.pack(fill="x", padx=14, pady=(0, 14))
        self._add_item(bottom, "API 连接设置", self._open_api_settings)
        self._build_status_card(bottom)
        self.refresh_status()

        # 下载模式变化会改变状态卡内容；调试开关变化影响固定标题口径
        for var_name in ("download_mode", "debug_mode"):
            var = getattr(win.state, var_name, None)
            if var is not None:
                try:
                    var.trace_add("write", lambda *_a: self.refresh_status())
                except Exception:  # noqa: BLE001 变量不可监听时忽略
                    pass

    # ------------------------------------------------------------------
    # 构建
    # ------------------------------------------------------------------
    def _build_brand(self) -> None:
        """品牌区：方块标记 + 产品名 + 副标题。"""
        box = tk.Frame(self.frame, bg=theme.RAIL_BG)
        box.pack(fill="x", padx=14, pady=(16, 0))
        mark = tk.Label(box, text="◆", bg=theme.ACCENT, fg=theme.RAIL_BG,
                        font=theme.sans_font(13, "bold"), width=2, height=1)
        mark.pack(side="left")
        text_box = tk.Frame(box, bg=theme.RAIL_BG)
        text_box.pack(side="left", padx=(10, 0))
        tk.Label(text_box, text="DocGenStudio", bg=theme.RAIL_BG,
                 fg=theme.RAIL_TEXT, font=theme.sans_font(10, "bold"),
                 anchor="w").pack(fill="x")
        tk.Label(text_box, text="豆包图片生产工作台", bg=theme.RAIL_BG,
                 fg=theme.RAIL_TEXT_TERTIARY, font=theme.sans_font(9),
                 anchor="w").pack(fill="x")

    def _make_item(self, parent, text: str, command, *,
                   count: str | None = None) -> _NavItem:
        """创建导航项并挂到父容器（默认整行铺满）。"""
        item = _NavItem(parent, text, command, count=count)
        item.frame.pack(fill="x", pady=1)
        return item

    def _add_item(self, parent, text: str, command, *,
                  count: str | None = None) -> _NavItem:
        item = self._make_item(parent, text, command, count=count)
        self._items.setdefault(text, item)
        return item

    def _build_status_card(self, parent) -> None:
        """当前账号状态卡（导航栏底部）。"""
        card = tk.Frame(parent, bg=theme.RAIL_STATUS_BG,
                        highlightbackground=theme.RAIL_STATUS_BORDER,
                        highlightthickness=1, bd=0)
        card.pack(fill="x", pady=(10, 0))

        head = tk.Frame(card, bg=theme.RAIL_STATUS_BG)
        head.pack(fill="x", padx=12, pady=(10, 0))
        self._status_dot = tk.Label(head, text="●", bg=theme.RAIL_STATUS_BG,
                                    fg=theme.SUCCESS, font=theme.sans_font(8))
        self._status_dot.pack(side="left", padx=(0, 6))
        tk.Label(head, text="当前默认豆包账号", bg=theme.RAIL_STATUS_BG,
                 fg=theme.RAIL_TEXT, font=theme.sans_font(10, "bold"),
                 anchor="w").pack(side="left")

        self._status_name = tk.Label(card, text="未配置账号",
                                     bg=theme.RAIL_STATUS_BG,
                                     fg=theme.RAIL_TEXT_SECONDARY,
                                     font=theme.sans_font(9), anchor="w")
        self._status_name.pack(fill="x", padx=12, pady=(6, 0))
        self._status_fixed = tk.Label(card, text="固定对话标题：否",
                                      bg=theme.RAIL_STATUS_BG,
                                      fg=theme.RAIL_TEXT_TERTIARY,
                                      font=theme.mono_font(9), anchor="w")
        self._status_fixed.pack(fill="x", padx=12, pady=(4, 0))
        self._status_download = tk.Label(card, text="下载模式：浏览图",
                                         bg=theme.RAIL_STATUS_BG,
                                         fg=theme.RAIL_TEXT_TERTIARY,
                                         font=theme.mono_font(9), anchor="w")
        self._status_download.pack(fill="x", padx=12, pady=(2, 10))

    # ------------------------------------------------------------------
    # 对外刷新入口
    # ------------------------------------------------------------------
    def set_active_mode(self, _mode: str) -> None:
        """高亮「图文生成」工作区；文档 / 配图模式都在该工作区内切换。"""
        item = self._items.get("图文生成")
        if item is not None:
            item.set_active(True)
        article = self._items.get("原稿生成")
        if article is not None:
            article.set_active(False)
        toutiao = self._items.get("头条发布")
        if toutiao is not None:
            toutiao.set_active(False)

    def set_active_section(self, section: str) -> None:
        """高亮当前工作区：``article`` 高亮原稿生成，其余回到图文生成。"""
        if section == "article":
            for name in ("图文生成",):
                item = self._items.get(name)
                if item is not None:
                    item.set_active(False)
            article = self._items.get("原稿生成")
            if article is not None:
                article.set_active(True)
            toutiao = self._items.get("头条发布")
            if toutiao is not None:
                toutiao.set_active(False)
            return
        try:
            mode = self.win.state.mode.get()
        except Exception:  # noqa: BLE001 轻量测试窗口无状态时忽略高亮
            return
        self.set_active_mode(mode)

    def set_toutiao_active(self, active: bool = True) -> None:
        """高亮「头条发布」工作区，并清除其他工作区入口的激活态。"""
        for name in ("图文生成",):
            item = self._items.get(name)
            if item is not None:
                item.set_active(False)
        article = self._items.get("原稿生成")
        if article is not None:
            article.set_active(False)
        toutiao = self._items.get("头条发布")
        if toutiao is not None:
            toutiao.set_active(active)

    def set_pending_count(self, count: int) -> None:
        """更新「待生成列表」的计数药丸。"""
        item = self._items.get("待生成列表")
        if item is not None:
            item.set_count(str(int(count)))

    def refresh_status(self) -> None:
        """刷新状态卡：默认账号昵称、固定标题开关、当前下载模式。"""
        name, fixed, online = self._account_status()
        try:
            self._status_name.configure(text=name)
            self._status_fixed.configure(
                text=f"固定对话标题：{'是' if fixed else '否'}")
            mode = self.win.state.download_mode.get()
            self._status_download.configure(
                text=f"下载模式：{_DOWNLOAD_MODE_LABELS.get(mode, mode)}")
            self._status_dot.configure(
                fg=theme.SUCCESS if online else theme.WARNING)
        except Exception:  # noqa: BLE001 窗口销毁 / 状态缺失时忽略
            pass

    def _account_status(self) -> tuple[str, bool, bool]:
        """返回 ``(展示名, 是否固定标题, 是否已配置账号)``；异常时安全回落。"""
        try:
            from pipeline import accounts as accounts_mod

            data = accounts_mod.load_registry()
            account_id = accounts_mod.AccountRouter(data).default_account_id()
            account = (accounts_mod.get_account(data, account_id)
                       if account_id else None)
            if not account:
                return "未配置账号", False, False
            label = accounts_mod.spec_label(account, account_id)
            return label, bool(account.get("fixed_conversation_title")), True
        except Exception:  # noqa: BLE001 注册表异常不应影响界面
            return "未配置账号", False, False

    # ------------------------------------------------------------------
    # 导航行为（全部转回主窗口既有入口）
    # ------------------------------------------------------------------
    def _on_doc_mode(self) -> None:
        """切回图文生成工作区（保持当前模式选择，不重置模式）。"""
        opener = getattr(self.win, "_show_pipeline_workspace", None)
        if callable(opener):
            opener()

    def _on_article_section(self) -> None:
        opener = getattr(self.win, "_show_article_workspace", None)
        if callable(opener):
            opener()

    def _on_toutiao(self) -> None:
        """「头条发布」入口：切到内嵌的 ToutiaoPublisher 工作区。"""
        opener = getattr(self.win, "_show_toutiao_workspace", None)
        if callable(opener):
            opener()

    def _on_relay_console(self) -> None:
        """「Relay 接单台」入口：打开独立的 Relay 供给方管理窗口。"""
        opener = getattr(self.win, "_open_relay_console", None)
        if callable(opener):
            opener()

    def _open_settings(self) -> None:
        """「系统设置」入口：打开主窗口的设置弹窗。

        ``_open_debug_dialog`` 是类方法（不在实例 ``__dict__`` 里），必须用
        ``getattr`` 取绑定方法；轻量测试窗口没有该方法时静默跳过。
        """
        opener = getattr(self.win, "_open_debug_dialog", None)
        if callable(opener):
            opener()

    def _open_api_settings(self) -> None:
        """「API 连接设置」入口：打开通道/模型/接口/Key 连接配置弹窗。"""
        opener = getattr(self.win, "_open_api_settings", None)
        if callable(opener):
            opener()


__all__ = ["NavigationRail"]
