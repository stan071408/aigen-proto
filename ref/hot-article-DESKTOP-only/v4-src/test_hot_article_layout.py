"""Windows fixed-layout contracts (Figma 36:2474) at the workspace viewport, with no API calls."""
import tkinter as tk
from tkinter import ttk

import pytest

from modules.hot_article.application import HotArticleService
from modules.hot_article.gui import HotArticleWorkspace
from modules.hot_article.repository import Repository
from tests.test_hot_article import FakeEngine, STYLE, run, snapshot


def descendants(parent):
    for widget in parent.winfo_children():
        yield widget
        yield from descendants(widget)


def visible_buttons(parent):
    return {w.cget("text"): w for w in descendants(parent)
            if isinstance(w, tk.Button) and w.winfo_ismapped()}


@pytest.fixture
def workspace(tmp_path):
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tk display unavailable")
    root.geometry("1232x968+20000+20000")  # Figma 1440×1000 frame minus 208 rail and 32 titlebar.
    service = HotArticleService(Repository(tmp_path / "app.db"), FakeEngine(), tmp_path / "work")
    view = HotArticleWorkspace(root, service, lambda _: None)
    view.pack(fill="both", expand=True)
    root.update()
    try:
        yield root, view, service
    finally:
        view.destroy()
        root.destroy()


def choose_inputs(view, service):
    topic = dict(id="toutiao:1", source="toutiao", rank=1, title="老旧小区加装电梯，居民最关心哪些问题", labels=["民生"])
    idea = dict(core_idea="政策是否有效，不只看供给数量，更要看服务能否真正抵达需要的人。", angle="可及性", reason="原标题")
    style = dict(STYLE, writing_style="从标题中的具体细节进入，用生活化的比较提出问题，再补上规则与事实依据。短段落降低阅读负担，让注意力从数字转向解释。")
    style["id"] = service.repo.add_style(style)
    view.rows = [topic]
    view._choose_topic(topic)
    view.ideas, view.styles = [idea], [style]
    view._choose_idea(idea)
    view._choose_style(style)



def footer_buttons(view):
    return visible_buttons(view.footer)


def test_fixed_shell_single_step_and_equal_direction_cards(workspace):
    root, view, service = workspace
    assert view.sections[1].winfo_manager() and all(not view.sections[n].winfo_manager() for n in range(2, 7))
    assert not hasattr(view, "canvas")  # no page-level scrolling in the Windows layout
    choose_inputs(view, service)
    root.update()
    assert view.current_step == 4
    assert [n for n in range(1, 7) if view.sections[n].winfo_manager()] == [4]
    cards = list(view.direction_cards.values())
    assert len({card.winfo_y() for card in cards}) == 1
    assert max(card.winfo_width() for card in cards) - min(card.winfo_width() for card in cards) <= 1
    assert all(card.winfo_height() < 130 for card in cards)
    # Fixed header 88 / step tabs 80 / footer 72, body fills the rest of the 968px workspace.
    header, tabs = view.winfo_children()[0], view.winfo_children()[1]
    # 1px #d5dedc rules are separate frames: tabs 79+1, footer 1+71.
    assert header.winfo_height() == 88 and tabs.winfo_height() + 1 == 80 and view.footer.winfo_height() + 1 == 72
    assert view.footer.winfo_rooty() + 71 == view.winfo_rooty() + view.winfo_height()
    assert view.step_tabs[4][0].cget("bg") == "#e9f4f0" and view.step_tabs[1][0].cget("bg") == "white"
    buttons = footer_buttons(view)
    assert (buttons["开始生成文章"].winfo_width(), buttons["开始生成文章"].winfo_height()) == (184, 40)
    assert buttons["上一步"].winfo_rootx() < buttons["开始生成文章"].winfo_rootx()
    assert all(view.primary_actions[n].winfo_reqwidth() == 184 for n in (1, 2, 3))
    # Log card stays inside the body above the footer.
    log = view.logs[4]
    assert log.winfo_rooty() + log.winfo_height() <= view.footer.winfo_rooty()


def test_radio_clicks_select_without_advancing_and_footer_continues(workspace):
    root, view, service = workspace
    topic = dict(id="toutiao:1", source="toutiao", rank=1, title="社区养老服务", labels=["公共服务"],
                 heat=9523000, collected_at="2026-10-26T09:30:00+08:00", url="https://example.com")
    view.rows = [topic]
    view._render_topics()
    root.update()
    assert footer_buttons(view)["继续提炼立意"].cget("state") == "disabled"
    radio = next(w for w in descendants(view.topic_box) if isinstance(w, tk.Radiobutton))
    radio.invoke()
    root.update()
    assert view.topic == topic and view.current_step == 1
    texts = [w.cget("text") for w in descendants(view.topic_detail) if isinstance(w, tk.Label)]
    assert "头条热榜 · 排名 01" in texts and "采集时间：2026-10-26 09:30" in texts and "来源热度：952.3 万" in texts
    assert "查看来源" in visible_buttons(view.topic_detail)
    assert view.footer_label.cget("text") == "已选 1 个原标题"
    footer_buttons(view)["继续提炼立意"].invoke()
    assert view.current_step == 2


def test_manuscript_tabs_preview_and_footer_actions(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    task = run(service, "write", snapshot())
    view._done(task)
    root.update()
    panel = view.sections[5]
    assert view.current_step == 5
    buttons = visible_buttons(panel)
    assert buttons["导出全部稿件"].winfo_rootx() > buttons["深度稿"].winfo_rootx()
    actions = [footer_buttons(view)[name] for name in ("导出本稿", "生成图文稿", "合并三稿")]
    assert len({w.winfo_rooty() for w in actions}) == 1 and all(w.winfo_width() == 144 for w in actions)
    assert [w.winfo_rootx() for w in actions] == sorted(w.winfo_rootx() for w in actions)
    assert buttons["差异化稿"].cget("bg") == "#e9f4f0"
    buttons["广度稿"].invoke()
    root.update()
    assert view.current_draft[5] == "breadth" and "广度稿" in view.footer_label.cget("text")
    radios = [w for w in descendants(panel) if isinstance(w, tk.Radiobutton) and w.winfo_ismapped()]
    previews = [w for w in descendants(panel) if isinstance(w, tk.Button) and w.cget("text") == "展开" and w.winfo_ismapped()]
    assert len(radios) == 3 and len(previews) == 1
    radios[1].invoke()
    assert {d["direction"]: d["selected"] for d in service.results(task["task_id"])} == {"similarity": 0, "breadth": 1, "depth": 0}
    previews[0].invoke()
    root.update()
    assert previews[0].cget("text") == "收起"
    assert any(isinstance(w, tk.Label) and w.cget("text") == "候选乙" and w.winfo_ismapped() for w in descendants(panel))
    previews[0].invoke()
    root.update()
    assert previews[0].cget("text") == "展开"
    merged = run(service, "merge", dict(source_task=task["task_id"]))
    view._done(merged)
    root.update()
    assert view.current_step == 6
    buttons = footer_buttons(view)
    assert {"返回三稿", "导出本稿", "生成图文稿"} <= buttons.keys() and "合并三稿" not in buttons
    assert "导出全部稿件" not in visible_buttons(view.sections[6])
    assert not view.logs[6].winfo_ismapped()
    buttons["返回三稿"].invoke()
    assert view.current_step == 5


def test_export_dialog_matches_figma_size_and_directory(workspace):
    root, view, service = workspace
    task = run(service, "write", snapshot())
    view._export_dialog(task["task_id"], ["similarity"])
    root.update()
    dialog = next(w for w in descendants(view) if isinstance(w, tk.Toplevel))
    assert (dialog.winfo_width(), dialog.winfo_height()) == (560, 476)
    radios = [w for w in descendants(dialog) if isinstance(w, tk.Radiobutton)]
    assert len(radios) == 2 and radios[1].winfo_rooty() > radios[0].winfo_rooty()
    entry = next(w for w in descendants(dialog) if isinstance(w, tk.Entry))
    assert entry.get() == service.export_directory()
    buttons = visible_buttons(dialog)
    assert buttons["取消"].winfo_rootx() < buttons["确认导出"].winfo_rootx()
    for w in descendants(dialog):
        if w.winfo_ismapped():
            assert w.winfo_rooty() + w.winfo_height() <= dialog.winfo_rooty() + dialog.winfo_height()
    dialog.destroy()


def test_minimum_window_keeps_actions_inside(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    root.geometry("1048x768+20000+20000")  # 1280×800 minimum frame
    root.update()
    for step in (1, 2, 3, 4):
        view._goto(step)
        root.update()
        for button in footer_buttons(view).values():
            assert button.winfo_rootx() >= view.winfo_rootx()
            assert button.winfo_rootx() + button.winfo_width() <= view.winfo_rootx() + view.winfo_width()
    for step in (2, 3):
        button = view.primary_actions[step]
        assert button.winfo_rootx() + button.winfo_width() <= view.winfo_rootx() + view.winfo_width()


def test_reset_keeps_style_and_stored_source_empty_state(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    selected_style = view.style
    view._reset("idea")
    view._choose_idea(dict(core_idea="另一观点", angle="角度", reason="依据"))
    assert view.style == selected_style and view.current_step == 4
    view.style_source.set("stored")
    view._source_changed()
    assert view.styles == [] and view.style is None
    assert view.writing_button.cget("text") == "获取已有风格"
    assert any(isinstance(w, tk.Label) and w.cget("text") == "尚未获取写作风格" for w in descendants(view.style_box))
    task = run(service, "write", snapshot())
    view._restore_log(4, task["task_id"])
    assert "任务完成" in view.logs[4].get("1.0", "end")


def test_category_suggestions_and_busy_inputs(workspace):
    root, view, service = workspace
    assert not view.category_suggestions.winfo_children()
    service.repo.replace_cache("boards", "today", {"rows": [
        dict(source="toutiao", labels=["公共服务", "社区生活"]),
        dict(source="toutiao", labels=["公共服务"]),
    ]})
    view._render_categories()
    root.update()
    assert view.direction_input.cget("values")[0] == "公共服务"
    buttons = visible_buttons(view.category_suggestions)
    buttons["公共服务"].invoke()
    assert view.direction.get() == "公共服务"
    view._set_busy(True)
    root.update()
    assert str(view.direction_input.cget("state")) == "disabled"
    assert view.primary_actions[1].cget("state") == "disabled"
    assert buttons["公共服务"].cget("state") == "disabled"
    assert "停止当前任务" in footer_buttons(view)
    view._set_busy(False)
    root.update()
    assert str(view.direction_input.cget("state")) == "normal"
    assert buttons["公共服务"].cget("state") == "normal"
    assert "停止当前任务" not in footer_buttons(view)


@pytest.mark.parametrize("directions", [["similarity"], ["similarity", "breadth"], ["similarity", "breadth", "depth"]])
def test_generated_directions_control_tabs_and_merge(workspace, directions):
    root, view, service = workspace
    result = run(service, "write", snapshot(directions))
    view._done(result)
    root.update()
    buttons = visible_buttons(view.sections[5])
    assert ("合并三稿" in footer_buttons(view)) == (len(directions) == 3)
    assert ("广度稿" in buttons) == ("breadth" in directions)
    assert ("深度稿" in buttons) == ("depth" in directions)
    assert "导出全部稿件" in buttons


def test_illustrate_handoff_dialog_then_export_selected_single_draft(workspace, tmp_path, monkeypatch):
    import time
    from tkinter import messagebox
    root, view, service = workspace
    errors = []
    monkeypatch.setattr(messagebox, "showerror", lambda *args, **kwargs: errors.append(args))
    service.repo.set_setting("export_directory", str(tmp_path / "exports"))
    result = run(service, "write", snapshot())
    view._done(result)
    root.update()
    handed_off = []
    view.on_handoff = handed_off.append
    visible_buttons(view.sections[5])["广度稿"].invoke()
    root.update()
    radios = [w for w in descendants(view.sections[5]) if isinstance(w, tk.Radiobutton) and w.winfo_ismapped()]
    radios[1].invoke()
    footer_buttons(view)["生成图文稿"].invoke()
    root.update()
    dialog = view.handoff_dialog
    assert (dialog.winfo_width(), dialog.winfo_height()) == (560, 386)
    assert any(isinstance(w, tk.Label) and w.cget("text") == "候选乙" for w in descendants(dialog))
    visible_buttons(dialog)["取消"].invoke()
    assert not handed_off and not view.runner.busy
    assert not (tmp_path / "exports").exists()
    (tmp_path / "exports").mkdir()
    footer_buttons(view)["生成图文稿"].invoke()
    root.update()
    visible_buttons(view.handoff_dialog)["保存并继续"].invoke()
    root.update()
    visible_buttons(view.export_dialog)["确认导出"].invoke()
    deadline = time.monotonic() + 10
    while not handed_off and not errors and time.monotonic() < deadline:
        root.update()
        time.sleep(.01)
    assert not errors
    assert len(handed_off) == 1
    assert handed_off[0]["title"] == "候选乙"
    from pathlib import Path
    assert Path(handed_off[0]["docx"]).is_file() and Path(handed_off[0]["spec"]).is_file()
    assert len(list((tmp_path / "exports").glob("*.docx"))) == 1


def test_real_host_mounts_same_workspace_and_preserves_it_on_navigation(tmp_path, monkeypatch):
    import app_paths
    from modules.hot_article import engine
    from ui.main_window import MainWindow
    from tests.test_article_workspace import _patch_isolated_paths

    _patch_isolated_paths(monkeypatch, tmp_path)
    monkeypatch.setattr(app_paths, "APP_DB", tmp_path / "app.db")
    monkeypatch.setattr(app_paths, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(engine, "configured_engine", lambda *_: FakeEngine())
    for name in ("_prewarm_ocr", "_start_directory_poller", "_bootstrap_relay", "_refresh_pending_articles"):
        monkeypatch.setattr(MainWindow, name, lambda *_: None)
    win = MainWindow()
    try:
        win.wm_state("normal")
        win.geometry("1440x968+20000+20000")
        win._show_hot_article_workspace()
        win.update()
        view = win._hot_article_workspace
        assert view.winfo_ismapped() and not win._pipeline_workspace.winfo_ismapped()
        assert win._navigation._items["AI 热度图文生成"]._active
        assert view.footer.winfo_ismapped()
        assert view.footer.winfo_rooty() + view.footer.winfo_height() <= view.winfo_rooty() + view.winfo_height()
        choose_inputs(view, view.service)
        win._show_pipeline_workspace()
        win.update()
        assert not view.winfo_ismapped()
        win._show_hot_article_workspace()
        win.update()
        assert win._hot_article_workspace is view
        assert view.style is not None
    finally:
        from modules.hot_article.integration import shutdown
        shutdown(win)
        win.destroy()


def test_style_list_and_detail_with_design_indicators(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    view._goto(3)
    root.update()
    radio = next(w for w in descendants(view.style_box) if isinstance(w, tk.Radiobutton))
    assert radio.cget("image") and radio.cget("selectimage")
    assert str(radio.cget("image")) != str(radio.cget("selectimage"))
    card = radio.master.master
    assert card.cget("bg") == "#e9f4f0" and card.cget("highlightbackground") == "#197d72"
    description = next(w for w in descendants(view.style_detail) if isinstance(w, tk.Label)
                       and w.cget("text") == view.style["writing_style"])
    assert description.winfo_height() > 20  # full text in the detail panel
    assert "继续设置文章" in footer_buttons(view)
    check = next(w for w in descendants(view.direction_cards["depth"]) if isinstance(w, tk.Checkbutton))
    check.invoke()
    assert not view.directions["depth"].get()
    assert view.direction_cards["depth"].cget("bg") == "white"
    check.invoke()
    assert view.directions["depth"].get()


def test_step5_title_selection_colors_and_merge_log(workspace):
    root, view, service = workspace
    result = run(service, "write", snapshot())
    view._done(result)
    root.update()
    panel = view.sections[5]
    radios = [w for w in descendants(panel) if isinstance(w, tk.Radiobutton) and w.winfo_ismapped()]
    assert [r.master.master.cget("bg") for r in radios] == ["#e9f4f0", "white", "white"]
    radios[1].invoke()
    assert [r.master.master.cget("bg") for r in radios] == ["white", "#e9f4f0", "white"]
    box = view.logs[5]
    assert not box.winfo_ismapped()
    for second in range(3):
        view._append_log(5, dict(time=f"2026-10-27T12:05:3{second}", message=f"事件{second}", status="running"))
    root.update()
    assert box.winfo_ismapped() and "12:05:30\t事件0" in box.get("1.0", "end")
    assert view.log_states[5].cget("text") == "运行中"


def test_step4_direction_badges_and_running_footer(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    root.update()
    badges = view.direction_badges
    assert not any(b.winfo_manager() for b in badges.values())
    view._job_kind = "write"
    view._set_busy(True)
    root.update()
    buttons = footer_buttons(view)
    assert view.footer_label.cget("text") == "生成中 · 已完成结果将立即保存"
    assert buttons["取消生成"].cget("state") == "normal" and buttons["查看生成结果"].cget("state") == "normal"
    assert buttons["查看生成结果"].winfo_width() == 184
    for key, message in (("similarity", "差异化稿：已完成结构分析，正在撰写正文。"), ("breadth", "广度稿：正在梳理相关群体。"),
                         ("depth", "深度稿：正在分析维护责任与预算机制。")):
        view._append_log(4, dict(time="2026-10-27T14:20:00", message=message, status="running", direction=key))
    root.update()
    assert [b.cget("text") for b in badges.values()] == ["撰写正文", "梳理观点", "分析机制"]
    assert badges["similarity"].cget("bg") == "#e9f4f0" and view.log_states[4].cget("bg") == "#fff5df"
    view._append_log(4, dict(time="2026-10-27T14:21:00", message="深度稿失败：请求超时", status="failed", direction="depth"))
    view._append_log(4, dict(time="2026-10-27T14:21:00", message="差异化稿已保存", status="complete", direction="similarity"))
    assert (badges["depth"].cget("text"), badges["depth"].cget("bg")) == ("请求超时", "#fceef0")
    assert (badges["similarity"].cget("text"), badges["similarity"].cget("bg")) == ("已完成", "#eaf5ef")
    view._set_busy(False)
    view._job_kind = None
    view._render_footers()
    root.update()
    assert "开始生成文章" in footer_buttons(view)


def test_partial_results_state_and_resume(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    service.engine.fail = {"depth"}
    result = run(service, "write", snapshot())
    view._done(result)
    root.update()
    assert view.current_step == 5
    tabs = visible_buttons(view.sections[5])
    assert "深度稿" not in tabs and {"差异化稿", "广度稿"} <= tabs.keys()
    assert "继续生成深度稿" in tabs and tabs["继续生成深度稿"].winfo_width() == 144
    assert any(isinstance(w, tk.Label) and w.cget("text") == "2 稿已完成" for w in descendants(view.sections[5]))
    buttons = footer_buttons(view)
    assert {"导出本稿", "生成图文稿"} <= buttons.keys() and "合并三稿" not in buttons
    view._goto(4)
    root.update()
    assert view.footer_label.cget("text") == "2 稿成功 · 1 稿未完成，续跑只补未完成方向"
    assert [b.cget("text") for b in view.direction_badges.values()] == ["已完成", "已完成", "失败"]
    footer_buttons(view)["处理成功稿"].invoke()
    assert view.current_step == 5
    service.engine.fail = set()
    calls = []
    view._start = lambda kind, data, step, resume=None: calls.append((kind, data, step, resume))
    view._goto(4)
    root.update()
    footer_buttons(view)["继续生成"].invoke()
    view._goto(5)
    root.update()
    visible_buttons(view.sections[5])["继续生成深度稿"].invoke()
    assert calls == [("write", {}, 4, result["task_id"])] * 2


def test_merging_footer_and_status_badge(workspace):
    root, view, service = workspace
    choose_inputs(view, service)
    result = run(service, "write", snapshot())
    view._done(result)
    root.update()
    assert "合并三稿" in footer_buttons(view)
    assert view.log_states[5].label.cget("text") == "未运行"
    view._job_kind = "merge"
    view._set_busy(True)
    view._append_log(5, dict(time="2026-10-27T14:40:10", message="已读取同一输入快照下的完整三稿。", status="running"))
    root.update()
    buttons = footer_buttons(view)
    assert "合并三稿" not in buttons and buttons["查看合并结果"].cget("state") == "normal"
    assert buttons["导出本稿"].cget("state") == "disabled"
    state = view.log_states[5].label
    assert (state.cget("text"), state.cget("bg"), state.cget("fg")) == ("运行中", "#fff5df", "#80530d")
    assert view.logs[5].winfo_ismapped()
    buttons["查看合并结果"].invoke()
    assert view.current_step == 5
    view._set_busy(False)
    view._job_kind = None
    merged = run(service, "merge", dict(source_task=result["task_id"]))
    view._done(merged)
    view._goto(5)
    root.update()
    footer_buttons(view)["查看合并结果"].invoke()
    assert view.current_step == 6


def test_navigation_items_use_figma_icons_with_state_variants(tmp_path):
    from ui.views import navigation
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tk display unavailable")
    try:
        for text, name in navigation.NAV_ICONS.items():
            for state in ("idle", "hover", "active"):
                assert (navigation.NAV_ICON_DIR / f"{name}-{state}.png").stat().st_size > 0
            item = navigation._NavItem(root, text, lambda: None)
            assert item.icon is not None and (item.icon.winfo_reqwidth(), item.icon.winfo_reqheight()) == (19, 21)
            item.set_active(True)
            assert str(item.icon.cget("image")) == str(item._icons["active"])
            item.set_active(False)
            assert str(item.icon.cget("image")) == str(item._icons["idle"])
        assert navigation._NavItem(root, "Relay 接单台", lambda: None).icon is None
    finally:
        root.destroy()
