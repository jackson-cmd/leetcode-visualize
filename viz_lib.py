"""
LeetCode 75 可视化共享库
========================
提供统一的数据结构渲染器和帧生成引擎，每道题只需写 ~50 行 solution.py。
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
from functools import lru_cache

# ============================================================
# 常量
# ============================================================
WIDTH, HEIGHT = 800, 520
WIDTH_WIDE, HEIGHT_TALL = 900, 620

# Catppuccin Mocha 调色板
class Colors:
    BG       = "#1e1e2e"
    TEXT     = "#cdd6f4"
    SUBTEXT  = "#a6adc8"
    ACCENT   = "#89b4fa"  # 蓝 - 当前/活跃
    GREEN    = "#a6e3a1"  # 绿 - 找到/成功
    YELLOW   = "#f9e2af"  # 黄 - 描述/警告
    RED      = "#f38ba8"  # 红 - 错误/移除
    PEACH    = "#fab387"  # 橙 - 次级高亮
    MAUVE    = "#cba6f7"  # 紫 - 第三高亮
    TEAL     = "#94e2d5"  # 青 - 窗口/区间
    PINK     = "#f5c2e7"  # 粉
    SKY      = "#89dceb"  # 天蓝
    SURFACE  = "#313244"  # 默认格子背景
    OVERLAY  = "#45475a"  # 暗淡/非活跃
    CRUST    = "#11111b"  # 最深背景

# 格子语义状态 (填充色, 边框色)
class CellState:
    DEFAULT   = (Colors.SURFACE, None)
    CURRENT   = ("#3b3b5a", Colors.ACCENT)
    FOUND     = ("#2d5a2d", Colors.GREEN)
    CHECKING  = ("#5a3b3b", Colors.PEACH)
    WINDOW    = ("#2d3b5a", Colors.TEAL)
    REMOVED   = ("#5a2d2d", Colors.RED)
    INACTIVE  = (Colors.OVERLAY, None)
    VISITED   = ("#3b4a3b", Colors.GREEN)
    SELECTED  = ("#4a3b5a", Colors.MAUVE)
    LEFT_PTR  = ("#2d4a5a", Colors.SKY)
    RIGHT_PTR = ("#4a3b2d", Colors.PEACH)

# 帧持续时间 (毫秒)
DURATION_FAST   = 500
DURATION_NORMAL = 1000
DURATION_SLOW   = 1500
DURATION_RESULT = 2500

# ============================================================
# 字体管理 — 等宽字体(英文/数字) + CJK字体(中文)
# ============================================================
_CJK_FONT_PATHS = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

_MONO_FONT_PATHS = [
    "/System/Library/Fonts/SFMono-Regular.otf",
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.dfont",
    "/Library/Fonts/Courier New.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]

def _has_cjk(text: str) -> bool:
    return any('\u4e00' <= c <= '\u9fff' or '\u3000' <= c <= '\u303f' for c in text)

@lru_cache(maxsize=32)
def get_font(size: int, cjk: bool = False) -> ImageFont.FreeTypeFont:
    paths = _CJK_FONT_PATHS if cjk else _MONO_FONT_PATHS
    for name in paths:
        if os.path.exists(name):
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
    # fallback: 如果请求 CJK 但没找到，尝试 mono；反之亦然
    fallback = _MONO_FONT_PATHS if cjk else _CJK_FONT_PATHS
    for name in fallback:
        if os.path.exists(name):
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
    return ImageFont.load_default()

def smart_font(size: int, text: str = "") -> ImageFont.FreeTypeFont:
    """根据文本内容自动选择字体"""
    return get_font(size, cjk=_has_cjk(text))

# ============================================================
# 绘图原语
# ============================================================
def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_text_centered(draw, x, y, w, h, text, color, font):
    tw, th = text_size(draw, text, font)
    draw.text((x + (w - tw) // 2, y + (h - th) // 2), text, fill=color, font=font)

def draw_arrow(draw, x1, y1, x2, y2, color, head_size=8, width=2):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    lx = x2 - head_size * math.cos(angle - math.pi / 6)
    ly = y2 - head_size * math.sin(angle - math.pi / 6)
    rx = x2 - head_size * math.cos(angle + math.pi / 6)
    ry = y2 - head_size * math.sin(angle + math.pi / 6)
    draw.polygon([(x2, y2), (lx, ly), (rx, ry)], fill=color)

def draw_pointer(draw, x, y, label, color, direction="down", font=None):
    f = font or get_font(14)
    symbol = "▼" if direction == "down" else "▲"
    tw, _ = text_size(draw, symbol, f)
    draw.text((x - tw // 2, y), symbol, fill=color, font=f)
    tw2, _ = text_size(draw, label, f)
    draw.text((x - tw2 // 2, y + 16), label, fill=color, font=f)

def draw_bracket(draw, x1, x2, y, color, label=None, font=None):
    """绘制滑动窗口的方括号标记"""
    draw.line([(x1, y - 5), (x1, y + 5)], fill=color, width=2)
    draw.line([(x1, y), (x2, y)], fill=color, width=2)
    draw.line([(x2, y - 5), (x2, y + 5)], fill=color, width=2)
    if label:
        f = font or get_font(14)
        tw, _ = text_size(draw, label, f)
        draw.text(((x1 + x2 - tw) // 2, y + 8), label, fill=color, font=f)

# ============================================================
# FrameBuilder — 帧脚手架
# ============================================================
class FrameBuilder:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.img = Image.new("RGB", (width, height), Colors.BG)
        self.draw = ImageDraw.Draw(self.img)

    def title(self, text):
        font = smart_font(26, text)
        tw, _ = text_size(self.draw, text, font)
        self.draw.text(((self.width - tw) // 2, 15), text, fill=Colors.ACCENT, font=font)
        return self

    def description(self, text):
        font = smart_font(18, text)
        tw, _ = text_size(self.draw, text, font)
        x = max(10, (self.width - tw) // 2)
        self.draw.text((x, 50), text, fill=Colors.YELLOW, font=font)
        return self

    def label(self, x, y, text, color=Colors.TEXT):
        self.draw.text((x, y), text, fill=color, font=smart_font(14, text))
        return self

    def result_banner(self, text):
        font = smart_font(22, text)
        tw, _ = text_size(self.draw, text, font)
        y = self.height - 55
        pad = 20
        draw_rounded_rect(self.draw,
                          ((self.width - tw) // 2 - pad, y - 8,
                           (self.width + tw) // 2 + pad, y + 36),
                          12, fill="#2d5a2d", outline=Colors.GREEN)
        self.draw.text(((self.width - tw) // 2, y), text, fill=Colors.GREEN, font=font)
        return self

    def build(self):
        return self.img

# ============================================================
# ArrayRenderer — 数组/字符串渲染
# ============================================================
class ArrayRenderer:
    def __init__(self, values, x=None, y=110, cell_w=60, cell_h=52,
                 label=None, canvas_width=WIDTH):
        self.values = values
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.y = y
        self.label = label
        self.spacing = 6
        total_w = len(values) * (cell_w + self.spacing) - self.spacing
        self.x = x if x is not None else (canvas_width - total_w) // 2
        self.canvas_width = canvas_width

    def _cell_xy(self, i):
        cx = self.x + i * (self.cell_w + self.spacing)
        return cx, self.y

    def cell_center(self, i):
        cx, cy = self._cell_xy(i)
        return cx + self.cell_w // 2, cy + self.cell_h // 2

    def cell_top(self, i):
        cx, cy = self._cell_xy(i)
        return cx + self.cell_w // 2, cy

    def cell_bottom(self, i):
        cx, cy = self._cell_xy(i)
        return cx + self.cell_w // 2, cy + self.cell_h

    def draw(self, draw, states=None, pointers=None, window=None,
             show_indices=True, values_override=None):
        states = states or {}
        pointers = pointers or {}
        vals = values_override or self.values
        font = get_font(20)
        font_sm = get_font(13)

        if self.label:
            draw.text((self.x, self.y - 22), self.label, fill=Colors.TEXT, font=font_sm)

        # 滑动窗口
        if window:
            wl, wr = window
            x1 = self.x + wl * (self.cell_w + self.spacing) - 3
            x2 = self.x + wr * (self.cell_w + self.spacing) + self.cell_w + 3
            draw_rounded_rect(draw, (x1, self.y - 4, x2, self.y + self.cell_h + 4),
                              8, fill=None, outline=Colors.TEAL, width=2)

        for i, val in enumerate(vals):
            cx, cy = self._cell_xy(i)
            fill, outline = states.get(i, CellState.DEFAULT)
            draw_rounded_rect(draw, (cx, cy, cx + self.cell_w, cy + self.cell_h),
                              8, fill=fill, outline=outline)
            txt = str(val) if val is not None else ""
            draw_text_centered(draw, cx, cy, self.cell_w, self.cell_h,
                               txt, Colors.TEXT, font)
            if show_indices:
                idx_txt = str(i)
                tw, _ = text_size(draw, idx_txt, font_sm)
                draw.text((cx + (self.cell_w - tw) // 2, cy - 16),
                          idx_txt, fill=Colors.OVERLAY, font=font_sm)

        # 指针
        for idx, (lbl, color) in pointers.items():
            if 0 <= idx < len(vals):
                px, _ = self._cell_xy(idx)
                px += self.cell_w // 2
                draw_pointer(draw, px, self.y + self.cell_h + 6, lbl, color)

class StringRenderer(ArrayRenderer):
    def __init__(self, text, **kwargs):
        kwargs.setdefault("cell_w", 46)
        kwargs.setdefault("cell_h", 46)
        super().__init__(list(text), **kwargs)

# ============================================================
# HashMapRenderer — 哈希表渲染
# ============================================================
class HashMapRenderer:
    def __init__(self, x=None, y=300, cols=4, entry_w=165, entry_h=36,
                 canvas_width=WIDTH):
        self.x = x
        self.y = y
        self.cols = cols
        self.entry_w = entry_w
        self.entry_h = entry_h
        self.canvas_width = canvas_width

    def draw(self, draw, entries, highlight_key=None,
             label="HashMap { value → index }"):
        font_sm = get_font(13)
        font = get_font(18)
        draw.text((30, self.y - 25), label, fill=Colors.TEXT, font=font_sm)

        if not entries:
            draw.text(((self.canvas_width - 60) // 2, self.y + 8),
                      "{ empty }", fill=Colors.OVERLAY, font=font_sm)
            return

        items = list(entries.items())
        cols = min(len(items), self.cols)
        start_x = self.x if self.x else (self.canvas_width - cols * self.entry_w) // 2

        for idx, (k, v) in enumerate(items):
            row, col = idx // self.cols, idx % self.cols
            ex = start_x + col * self.entry_w
            ey = self.y + row * (self.entry_h + 4)
            is_hl = highlight_key is not None and k == highlight_key
            fill = "#2d5a2d" if is_hl else Colors.SURFACE
            outline = Colors.GREEN if is_hl else None
            draw_rounded_rect(draw, (ex, ey, ex + self.entry_w - 8, ey + self.entry_h),
                              6, fill=fill, outline=outline)
            entry_text = f"{k} → {v}"
            draw_text_centered(draw, ex, ey, self.entry_w - 8, self.entry_h,
                               entry_text, Colors.TEXT, font)

# ============================================================
# LinkedListRenderer — 链表渲染
# ============================================================
class LinkedListRenderer:
    def __init__(self, values, x=None, y=180, node_w=56, node_h=48,
                 spacing=36, canvas_width=WIDTH):
        self.values = values
        self.node_w = node_w
        self.node_h = node_h
        self.spacing = spacing
        self.y = y
        total_w = len(values) * node_w + (len(values) - 1) * spacing
        self.x = x if x is not None else (canvas_width - total_w) // 2
        self.canvas_width = canvas_width

    def node_center(self, i):
        nx = self.x + i * (self.node_w + self.spacing)
        return nx + self.node_w // 2, self.y + self.node_h // 2

    def draw(self, draw, states=None, pointers=None, connections=None,
             show_null=True):
        states = states or {}
        pointers = pointers or {}
        font = get_font(18)
        font_sm = get_font(13)

        if connections is None:
            connections = [(i, i + 1) for i in range(len(self.values) - 1)]

        # 绘制箭头
        for src, dst in connections:
            sx = self.x + src * (self.node_w + self.spacing) + self.node_w
            sy = self.y + self.node_h // 2
            dx = self.x + dst * (self.node_w + self.spacing)
            dy = self.y + self.node_h // 2
            draw_arrow(draw, sx + 2, sy, dx - 2, dy, Colors.SUBTEXT)

        # 绘制节点
        for i, val in enumerate(self.values):
            nx = self.x + i * (self.node_w + self.spacing)
            fill, outline = states.get(i, CellState.DEFAULT)
            draw_rounded_rect(draw, (nx, self.y, nx + self.node_w, self.y + self.node_h),
                              10, fill=fill, outline=outline)
            draw_text_centered(draw, nx, self.y, self.node_w, self.node_h,
                               str(val), Colors.TEXT, font)

        # null 终止
        if show_null and self.values:
            last_x = self.x + (len(self.values) - 1) * (self.node_w + self.spacing) + self.node_w
            draw.text((last_x + 10, self.y + self.node_h // 2 - 7),
                      "null", fill=Colors.OVERLAY, font=font_sm)

        # 指针标签
        for idx, (lbl, color) in pointers.items():
            if 0 <= idx < len(self.values):
                nx = self.x + idx * (self.node_w + self.spacing) + self.node_w // 2
                draw_pointer(draw, nx, self.y - 28, lbl, color, direction="down")

# ============================================================
# BinaryTreeRenderer — 二叉树渲染
# ============================================================
class BinaryTreeRenderer:
    """层序数组表示 (None = 空节点)"""
    def __init__(self, values, x=None, y=85, node_r=22,
                 level_gap=65, canvas_width=WIDTH, canvas_height=HEIGHT):
        self.values = values
        self.node_r = node_r
        self.level_gap = level_gap
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.y_start = y
        self.positions = {}
        self._compute_positions()

    def _compute_positions(self):
        if not self.values:
            return
        max_level = int(math.log2(len(self.values))) + 1 if self.values else 0
        for i, val in enumerate(self.values):
            if val is None:
                continue
            level = int(math.log2(i + 1))
            pos_in_level = i - (2 ** level - 1)
            nodes_in_level = 2 ** level
            segment = self.canvas_width / nodes_in_level
            x = segment * pos_in_level + segment / 2
            y = self.y_start + level * self.level_gap
            self.positions[i] = (int(x), int(y))

    def node_pos(self, i):
        return self.positions.get(i)

    def draw(self, draw, states=None, path=None, level_highlight=None,
             edge_colors=None):
        states = states or {}
        path_set = set(path or [])
        edge_colors = edge_colors or {}
        font = get_font(16)

        # 层高亮
        if level_highlight is not None:
            ly = self.y_start + level_highlight * self.level_gap
            draw_rounded_rect(draw, (20, ly - self.node_r - 5,
                                     self.canvas_width - 20, ly + self.node_r + 5),
                              8, fill="#1e2a3e", outline=None)

        # 绘制边
        for i in range(len(self.values)):
            if self.values[i] is None or i not in self.positions:
                continue
            px, py = self.positions[i]
            for child in [2 * i + 1, 2 * i + 2]:
                if child < len(self.values) and self.values[child] is not None and child in self.positions:
                    cx, cy = self.positions[child]
                    edge_key = (i, child)
                    ec = edge_colors.get(edge_key, Colors.OVERLAY)
                    if i in path_set and child in path_set:
                        ec = Colors.GREEN
                    draw.line([(px, py + self.node_r), (cx, cy - self.node_r)],
                              fill=ec, width=2)

        # 绘制节点
        for i, val in enumerate(self.values):
            if val is None or i not in self.positions:
                continue
            x, y = self.positions[i]
            fill, outline = states.get(i, CellState.DEFAULT)
            if i in path_set and i not in states:
                fill, outline = CellState.FOUND
            draw.ellipse((x - self.node_r, y - self.node_r,
                          x + self.node_r, y + self.node_r),
                         fill=fill, outline=outline, width=2)
            txt = str(val)
            tw, th = text_size(draw, txt, font)
            draw.text((x - tw // 2, y - th // 2), txt, fill=Colors.TEXT, font=font)

# ============================================================
# StackRenderer — 栈渲染
# ============================================================
class StackRenderer:
    def __init__(self, x=None, y=100, cell_w=80, cell_h=36,
                 max_visible=8, canvas_width=WIDTH, label="Stack"):
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.max_visible = max_visible
        self.y = y
        self.label = label
        self.x = x if x is not None else (canvas_width - cell_w) // 2
        self.canvas_width = canvas_width

    def draw(self, draw, values, states=None, top_label="← top"):
        states = states or {}
        font = get_font(16)
        font_sm = get_font(13)

        draw.text((self.x, self.y - 20), self.label, fill=Colors.TEXT, font=font_sm)
        visible = values[-self.max_visible:] if len(values) > self.max_visible else values

        for vi, val in enumerate(reversed(visible)):
            real_idx = len(values) - 1 - vi
            cy = self.y + vi * (self.cell_h + 4)
            fill, outline = states.get(real_idx, CellState.DEFAULT)
            draw_rounded_rect(draw, (self.x, cy, self.x + self.cell_w, cy + self.cell_h),
                              6, fill=fill, outline=outline)
            draw_text_centered(draw, self.x, cy, self.cell_w, self.cell_h,
                               str(val), Colors.TEXT, font)
            if vi == 0:
                draw.text((self.x + self.cell_w + 8, cy + 8),
                          top_label, fill=Colors.ACCENT, font=font_sm)

# ============================================================
# QueueRenderer — 队列渲染
# ============================================================
class QueueRenderer:
    def __init__(self, x=None, y=200, cell_w=56, cell_h=48,
                 max_visible=10, canvas_width=WIDTH, label="Queue"):
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.max_visible = max_visible
        self.y = y
        self.label = label
        self.spacing = 6
        self.canvas_width = canvas_width
        self.x = x

    def draw(self, draw, values, states=None):
        states = states or {}
        font = get_font(16)
        font_sm = get_font(13)
        visible = values[:self.max_visible]
        total_w = len(visible) * (self.cell_w + self.spacing) - self.spacing if visible else 0
        sx = self.x if self.x else (self.canvas_width - total_w) // 2

        draw.text((sx, self.y - 20), self.label, fill=Colors.TEXT, font=font_sm)
        if not visible:
            draw.text((sx, self.y + 10), "{ empty }", fill=Colors.OVERLAY, font=font_sm)
            return

        for i, val in enumerate(visible):
            cx = sx + i * (self.cell_w + self.spacing)
            fill, outline = states.get(i, CellState.DEFAULT)
            draw_rounded_rect(draw, (cx, self.y, cx + self.cell_w, self.y + self.cell_h),
                              6, fill=fill, outline=outline)
            draw_text_centered(draw, cx, self.y, self.cell_w, self.cell_h,
                               str(val), Colors.TEXT, font)
        draw.text((sx - 35, self.y + 14), "front", fill=Colors.ACCENT, font=font_sm)
        last_x = sx + (len(visible) - 1) * (self.cell_w + self.spacing) + self.cell_w
        draw.text((last_x + 8, self.y + 14), "back", fill=Colors.PEACH, font=font_sm)

# ============================================================
# GraphRenderer — 图渲染（圆形布局）
# ============================================================
class GraphRenderer:
    def __init__(self, n, edges=None, layout="circle", center=None,
                 radius=130, canvas_width=WIDTH, canvas_height=HEIGHT,
                 node_r=22):
        self.n = n
        self.edges = edges or []
        self.node_r = node_r
        cx = canvas_width // 2 if center is None else center[0]
        cy = (canvas_height // 2 + 30) if center is None else center[1]
        self.positions = {}
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            self.positions[i] = (int(cx + radius * math.cos(angle)),
                                 int(cy + radius * math.sin(angle)))

    def draw(self, draw, node_states=None, edge_states=None,
             node_labels=None, directed=False, visit_order=None):
        node_states = node_states or {}
        edge_states = edge_states or {}
        node_labels = node_labels or {i: str(i) for i in range(self.n)}
        visit_order = visit_order or {}
        font = get_font(15)
        font_sm = get_font(11)

        # 边
        for u, v in self.edges:
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            ec = edge_states.get((u, v), edge_states.get((v, u), Colors.OVERLAY))
            if directed:
                angle = math.atan2(y2 - y1, x2 - x1)
                nx2 = x2 - int(self.node_r * math.cos(angle))
                ny2 = y2 - int(self.node_r * math.sin(angle))
                nx1 = x1 + int(self.node_r * math.cos(angle))
                ny1 = y1 + int(self.node_r * math.sin(angle))
                draw_arrow(draw, nx1, ny1, nx2, ny2, ec)
            else:
                draw.line([(x1, y1), (x2, y2)], fill=ec, width=2)

        # 节点
        for i in range(self.n):
            x, y = self.positions[i]
            fill, outline = node_states.get(i, CellState.DEFAULT)
            draw.ellipse((x - self.node_r, y - self.node_r,
                          x + self.node_r, y + self.node_r),
                         fill=fill, outline=outline, width=2)
            lbl = node_labels.get(i, str(i))
            tw, th = text_size(draw, lbl, font)
            draw.text((x - tw // 2, y - th // 2), lbl, fill=Colors.TEXT, font=font)
            if i in visit_order:
                order_txt = str(visit_order[i])
                tw2, _ = text_size(draw, order_txt, font_sm)
                draw.text((x - tw2 // 2, y - self.node_r - 14),
                          order_txt, fill=Colors.YELLOW, font=font_sm)

# ============================================================
# GridRenderer — 二维网格渲染
# ============================================================
class GridRenderer:
    def __init__(self, rows, cols, x=None, y=90, cell_size=42,
                 canvas_width=WIDTH):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.y = y
        total_w = cols * cell_size
        self.x = x if x is not None else (canvas_width - total_w) // 2

    def cell_center(self, r, c):
        return (self.x + c * self.cell_size + self.cell_size // 2,
                self.y + r * self.cell_size + self.cell_size // 2)

    def draw(self, draw, values=None, states=None, path=None):
        states = states or {}
        path_set = set(path or [])
        font = get_font(15)

        for r in range(self.rows):
            for c in range(self.cols):
                cx = self.x + c * self.cell_size
                cy = self.y + r * self.cell_size
                state = states.get((r, c), CellState.DEFAULT)
                if (r, c) in path_set and (r, c) not in states:
                    state = CellState.FOUND
                fill, outline = state
                draw_rounded_rect(draw, (cx + 1, cy + 1,
                                         cx + self.cell_size - 1, cy + self.cell_size - 1),
                                  4, fill=fill, outline=outline)
                if values and r < len(values) and c < len(values[r]):
                    val = str(values[r][c])
                    draw_text_centered(draw, cx, cy, self.cell_size, self.cell_size,
                                       val, Colors.TEXT, font)

# ============================================================
# DPTableRenderer — DP 表格渲染
# ============================================================
class DPTableRenderer:
    def __init__(self, rows=1, cols=1, x=None, y=120, cell_size=48,
                 canvas_width=WIDTH, label="dp[]"):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.y = y
        self.label = label
        self.canvas_width = canvas_width
        actual_cols = cols if rows > 1 else cols
        total_w = actual_cols * cell_size
        self.x = x if x is not None else (canvas_width - total_w) // 2

    def draw(self, draw, values, states=None, arrows=None,
             row_labels=None, col_labels=None):
        states = states or {}
        font = get_font(15)
        font_sm = get_font(12)

        draw.text((self.x, self.y - 20), self.label, fill=Colors.TEXT, font=font_sm)

        # 列标签
        if col_labels:
            for c, lbl in enumerate(col_labels):
                cx = self.x + c * self.cell_size
                draw_text_centered(draw, cx, self.y - 18, self.cell_size, 16,
                                   str(lbl), Colors.OVERLAY, font_sm)

        is_1d = self.rows == 1
        data = values if not is_1d else [values]

        for r in range(len(data)):
            # 行标签
            if row_labels and r < len(row_labels):
                draw.text((self.x - 25, self.y + r * self.cell_size + 14),
                          str(row_labels[r]), fill=Colors.OVERLAY, font=font_sm)

            for c in range(len(data[r])):
                cx = self.x + c * self.cell_size
                cy = self.y + r * self.cell_size
                key = c if is_1d else (r, c)
                fill, outline = states.get(key, CellState.DEFAULT)
                draw_rounded_rect(draw, (cx + 1, cy + 1,
                                         cx + self.cell_size - 1, cy + self.cell_size - 1),
                                  4, fill=fill, outline=outline)
                val = data[r][c]
                txt = str(val) if val is not None else ""
                draw_text_centered(draw, cx, cy, self.cell_size, self.cell_size,
                                   txt, Colors.TEXT, font)

        # 依赖箭头
        if arrows:
            for (fr, fc), (tr, tc) in arrows:
                fx = self.x + fc * self.cell_size + self.cell_size // 2
                fy = self.y + fr * self.cell_size + self.cell_size // 2
                tx = self.x + tc * self.cell_size + self.cell_size // 2
                ty = self.y + tr * self.cell_size + self.cell_size // 2
                draw_arrow(draw, fx, fy, tx, ty, Colors.MAUVE, head_size=6)

# ============================================================
# BitRenderer — 位运算渲染
# ============================================================
class BitRenderer:
    def __init__(self, num_bits=8, x=None, y=200, cell_size=44,
                 canvas_width=WIDTH, label=None):
        self.num_bits = num_bits
        self.cell_size = cell_size
        self.y = y
        self.label = label
        total_w = num_bits * cell_size
        self.x = x if x is not None else (canvas_width - total_w) // 2

    def draw(self, draw, value, bit_states=None, show_decimal=True):
        bit_states = bit_states or {}
        font = get_font(18)
        font_sm = get_font(13)

        if self.label:
            draw.text((self.x, self.y - 20), self.label, fill=Colors.TEXT, font=font_sm)

        bits = format(value, f'0{self.num_bits}b')
        for i, bit in enumerate(bits):
            cx = self.x + i * self.cell_size
            pos = self.num_bits - 1 - i
            fill, outline = bit_states.get(pos, CellState.DEFAULT)
            draw_rounded_rect(draw, (cx + 1, self.y, cx + self.cell_size - 1,
                                     self.y + self.cell_size),
                              4, fill=fill, outline=outline)
            draw_text_centered(draw, cx, self.y, self.cell_size, self.cell_size,
                               bit, Colors.TEXT, font)
            # 位权重
            tw, _ = text_size(draw, str(pos), font_sm)
            draw.text((cx + (self.cell_size - tw) // 2, self.y + self.cell_size + 3),
                      str(pos), fill=Colors.OVERLAY, font=font_sm)

        if show_decimal:
            dec_txt = f"= {value}"
            draw.text((self.x + self.num_bits * self.cell_size + 10,
                       self.y + self.cell_size // 2 - 8),
                      dec_txt, fill=Colors.ACCENT, font=font)

# ============================================================
# IntervalRenderer — 区间渲染
# ============================================================
class IntervalRenderer:
    def __init__(self, min_val, max_val, x=60, y=None, width=680,
                 bar_h=22, gap=6, canvas_width=WIDTH, canvas_height=HEIGHT):
        self.min_val = min_val
        self.max_val = max_val
        self.x = x
        self.width = width
        self.bar_h = bar_h
        self.gap = gap
        self.canvas_height = canvas_height
        self.y_start = y if y else 120

    def _val_to_x(self, val):
        ratio = (val - self.min_val) / max(1, self.max_val - self.min_val)
        return int(self.x + ratio * self.width)

    def draw(self, draw, intervals, states=None, arrows=None, label="Intervals"):
        states = states or {}
        font_sm = get_font(13)
        font = get_font(14)
        draw.text((self.x, self.y_start - 25), label, fill=Colors.TEXT, font=font_sm)

        # 数轴
        draw.line([(self.x, self.y_start), (self.x + self.width, self.y_start)],
                  fill=Colors.OVERLAY, width=1)

        for i, (s, e) in enumerate(intervals):
            x1 = self._val_to_x(s)
            x2 = self._val_to_x(e)
            y = self.y_start + 15 + i * (self.bar_h + self.gap)
            fill, outline = states.get(i, CellState.DEFAULT)
            draw_rounded_rect(draw, (x1, y, x2, y + self.bar_h),
                              4, fill=fill, outline=outline)
            txt = f"[{s},{e}]"
            draw_text_centered(draw, x1, y, x2 - x1, self.bar_h,
                               txt, Colors.TEXT, font_sm)

        if arrows:
            for ax in arrows:
                px = self._val_to_x(ax)
                draw.line([(px, self.y_start - 10), (px, self.y_start + 15 + len(intervals) * (self.bar_h + self.gap))],
                          fill=Colors.RED, width=2)
                draw.text((px - 3, self.y_start - 22), "↓", fill=Colors.RED, font=font)

# ============================================================
# TrieRenderer — 字典树渲染
# ============================================================
class TrieRenderer:
    def __init__(self, x=None, y=90, level_gap=55, node_r=18,
                 canvas_width=WIDTH):
        self.y = y
        self.level_gap = level_gap
        self.node_r = node_r
        self.canvas_width = canvas_width

    def _layout(self, trie, x, y, width):
        """递归计算节点位置"""
        positions = []
        children = {k: v for k, v in trie.items() if k != '$'}
        if not children:
            return positions
        child_w = width / max(len(children), 1)
        for i, (ch, sub) in enumerate(children.items()):
            cx = x + child_w * i + child_w / 2
            cy = y + self.level_gap
            positions.append((ch, int(cx), int(cy), int(x + child_w * i), sub))
            positions.extend(self._layout(sub, x + child_w * i, cy, child_w))
        return positions

    def draw(self, draw, trie, states=None, current_prefix=None):
        states = states or {}
        font = get_font(14)
        # root
        root_x = self.canvas_width // 2
        root_y = self.y
        draw.ellipse((root_x - self.node_r, root_y - self.node_r,
                      root_x + self.node_r, root_y + self.node_r),
                     fill=Colors.SURFACE, outline=Colors.ACCENT, width=2)
        draw_text_centered(draw, root_x - self.node_r, root_y - self.node_r,
                           self.node_r * 2, self.node_r * 2, "root", Colors.TEXT, font)

        positions = self._layout(trie, 0, root_y, self.canvas_width)
        drawn = {"": (root_x, root_y)}

        # build prefix map
        def _build_prefix_map(t, prefix=""):
            result = {}
            for k, v in t.items():
                if k == '$':
                    continue
                p = prefix + k
                result[p] = v
                result.update(_build_prefix_map(v, p))
            return result

        prefix_map = _build_prefix_map(trie)
        # We need to layout properly - simplified version
        children = {k: v for k, v in trie.items() if k != '$'}
        if not children:
            return
        child_w = self.canvas_width / max(len(children), 1)
        self._draw_level(draw, trie, root_x, root_y, 0, self.canvas_width,
                         "", states, current_prefix, font)

    def _draw_level(self, draw, node, parent_x, parent_y, x_start, width,
                    prefix, states, current_prefix, font):
        children = {k: v for k, v in node.items() if k != '$'}
        if not children:
            return
        child_w = width / max(len(children), 1)
        for i, (ch, sub) in enumerate(children.items()):
            cx = int(x_start + child_w * i + child_w / 2)
            cy = parent_y + self.level_gap
            new_prefix = prefix + ch

            # 边
            draw.line([(parent_x, parent_y + self.node_r),
                       (cx, cy - self.node_r)], fill=Colors.OVERLAY, width=2)
            # 边标签
            mid_x = (parent_x + cx) // 2
            mid_y = (parent_y + self.node_r + cy - self.node_r) // 2
            draw.text((mid_x - 4, mid_y - 8), ch, fill=Colors.YELLOW, font=font)

            # 节点
            is_end = '$' in sub
            fill, outline = states.get(new_prefix, CellState.DEFAULT)
            if current_prefix and new_prefix == current_prefix[:len(new_prefix)]:
                fill, outline = CellState.CURRENT
            if is_end:
                outline = Colors.GREEN
            draw.ellipse((cx - self.node_r, cy - self.node_r,
                          cx + self.node_r, cy + self.node_r),
                         fill=fill, outline=outline, width=2)
            draw_text_centered(draw, cx - self.node_r, cy - self.node_r,
                               self.node_r * 2, self.node_r * 2, ch, Colors.TEXT, font)

            self._draw_level(draw, sub, cx, cy, x_start + child_w * i,
                             child_w, new_prefix, states, current_prefix, font)

# ============================================================
# HeapRenderer — 堆渲染 (复用 BinaryTreeRenderer)
# ============================================================
HeapRenderer = BinaryTreeRenderer

# ============================================================
# GIF 生成引擎
# ============================================================
def generate_gif(frames, durations, output_path, optimize=True):
    if not frames:
        print(f"Warning: no frames for {output_path}")
        return
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=optimize,
    )
    print(f"✓ {output_path} ({len(frames)} frames)")


def build_visualization(title, frame_generator, output_path,
                        width=WIDTH, height=HEIGHT):
    """
    高级入口。frame_generator 是一个可调用对象，yield:
        (description: str, draw_fn: Callable[[FrameBuilder], None], duration: int)
    """
    frames = []
    durations = []
    for desc, draw_fn, duration in frame_generator():
        fb = FrameBuilder(width, height)
        fb.title(title)
        fb.description(desc)
        draw_fn(fb)
        frames.append(fb.build())
        durations.append(duration)
    generate_gif(frames, durations, output_path)
