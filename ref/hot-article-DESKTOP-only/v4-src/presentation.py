"""Prototype-derived Tk presentation primitives; no business dependencies."""
import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path

from PIL import Image, ImageDraw, ImageTk

BG = "#f3f6f6"
INK = "#16211f"
MUTED = "#7b8986"
SECONDARY = "#52615e"
GREEN = "#197d72"
BLUE = "#edf3fb"
BLUE_BORDER = "#bfd4eb"
PURPLE = "#f7f4fc"
PURPLE_BORDER = "#dcd2ee"
PURPLE_TEXT = "#756484"
BORDER = "#d8e2df"
# Windows 桌面版设计令牌（Figma x3uNLbtFAS8MOCnCTPu7aH · 36:2474）。
W_INK = "#162b2a"
W_TEXT = "#4c605d"
W_MUTED = "#5d706c"
W_LINE = "#d5dedc"
W_SOFT = "#e9f4f0"
W_SUBTLE = "#f7f9f9"
W_OK_BG = "#eaf5ef"
W_OK = "#176c50"
W_ON_ACCENT = "#f5fbf9"
W_WARN_BG = "#fff5df"
W_WARN = "#80530d"
W_ERR_BG = "#fceef0"
W_ERR = "#a82935"
_FONT_FAMILY = None


def font(size=13, bold=False):
    global _FONT_FAMILY
    if _FONT_FAMILY is None:
        families = set(tkfont.families())
        # Windows 设计稿（Figma 36:2474）优先 Microsoft YaHei UI，缺失时回退 Noto Sans SC。
        _FONT_FAMILY = next((name for name in ("Microsoft YaHei UI", "Noto Sans SC") if name in families), "TkDefaultFont")
    # Figma uses pixel sizes; negative Tk sizes avoid Windows point/DPI conversion.
    return (_FONT_FAMILY, -size, "bold" if bold else "normal")


class ActionButton(tk.Button):
    """Native keyboard/focus behaviour with design dimensions in pixels."""
    def __init__(self, parent, *, pixel_width=None, pixel_height=37, **kwargs):
        self._spacer = tk.PhotoImage(master=parent, width=1, height=1)
        text_font = kwargs.get("font", font(12))
        if pixel_width is None:
            pixel_width = tkfont.Font(root=parent, font=text_font).measure(kwargs.get("text", "")) + 40
        super().__init__(parent, image=self._spacer, compound="center",
                         width=pixel_width-2, height=pixel_height-2,
                         padx=0, pady=0, **kwargs)


class ChoiceImages:
    """Figma indicators on native check/radio controls (selection and keys intact).

    Only the geometric indicator container is painted here. The check/dot itself
    is the downloaded design asset, rendered at its original SVG dimensions.
    """
    def __init__(self, master):
        self.master, self.cache = master, {}

    def apply(self, control, kind="radio-green"):
        if kind not in self.cache:
            root = Path(__file__).with_name("assets") / "figma"
            with Image.open(root / f"{kind}.png") as source:
                mark = source.convert("RGBA")
            states = []
            radio = kind.startswith("radio")
            size = 13 if radio or kind == "check-source" else 16
            accent = "#8065a1" if kind == "radio-purple" else GREEN
            for selected in (False, True):
                image = Image.new("RGBA", (size + 9, 20))
                painter = ImageDraw.Draw(image)
                y = (20 - size) // 2
                bounds = (0, y, size-1, y+size-1)
                if radio:
                    painter.ellipse(bounds, fill="white", outline=accent if selected else "#767676")
                else:
                    painter.rounded_rectangle(bounds, radius=2, fill=accent if selected else "white", outline=accent if selected else "#767676")
                if selected:
                    image.alpha_composite(mark, ((size-mark.width)//2, y+(size-mark.height)//2))
                states.append(ImageTk.PhotoImage(image, master=self.master))
            self.cache[kind] = states
        control.configure(indicatoron=False, image=self.cache[kind][0], selectimage=self.cache[kind][1],
                          compound="left", highlightthickness=0, selectcolor=control.cget("bg"))


class Panel(tk.Canvas):
    """Rounded card with a real widget content frame and content-driven height."""
    def __init__(self, parent, *, bg="white", border=BORDER, padding=20, radius=7):
        super().__init__(parent, bg=parent.cget("bg"), height=1, width=1,
                         highlightthickness=0, bd=0)
        self.fill, self.border, self.padding, self.radius = bg, border, padding, radius
        self.pad_x, self.pad_y = (padding, padding) if isinstance(padding, int) else padding
        self.body = tk.Frame(self, bg=bg)
        self.window = self.create_window(self.pad_x, self.pad_y, window=self.body, anchor="nw", state="hidden")
        # Canvas window items otherwise keep embedded children mapped while a tab
        # ancestor is hidden, which can paint controls over the active tab.
        self.bind("<Map>", lambda event: self.itemconfigure(self.window, state="normal"))
        self.bind("<Unmap>", lambda event: self.itemconfigure(self.window, state="hidden"))
        self.bind("<Configure>", self._resize)
        self.body.bind("<Configure>", self._height)

    def _height(self, event=None):
        target = self.body.winfo_reqheight() + self.pad_y * 2
        if int(float(self.cget("height"))) != target:
            self.configure(height=target)
        self._paint(self.winfo_width(), target)

    def _resize(self, event):
        self.itemconfigure(self.window, width=max(1, event.width - self.pad_x * 2))
        self._height()

    def _paint(self, width, height):
        self.delete("surface")
        r = self.radius
        points = [r, 1, width-r, 1, width-1, 1, width-1, r,
                  width-1, height-r, width-1, height-1, width-r, height-1,
                  r, height-1, 1, height-1, 1, height-r, 1, r, 1, 1]
        self.create_polygon(points, smooth=True, splinesteps=24, fill=self.fill,
                            outline=self.border, tags="surface")
        self.tag_lower("surface")

    def colors(self, bg, border):
        self.fill, self.border = bg, border
        self.body.configure(bg=bg)
        self._height()


class WindowsChoiceImages:
    """Figma `Windows/radio` 与 `Windows/check` 组件的 18px 原始导出 PNG。"""
    def __init__(self, master):
        root = Path(__file__).with_name("assets") / "windows"
        self.images = {name: tk.PhotoImage(master=master, file=str(root / f"{name}.png"))
                       for name in ("radio-off", "radio-on", "check-off", "check-on")}

    def apply(self, control, kind="radio"):
        control.configure(indicatoron=False, image=self.images[f"{kind}-off"],
                          selectimage=self.images[f"{kind}-on"], compound="left",
                          highlightthickness=0, offrelief="flat", relief="flat",
                          overrelief="flat", selectcolor=control.cget("bg"), padx=0)
