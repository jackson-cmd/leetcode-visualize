"""
11. 盛最多水的容器 — 可视化
使用 ArrayRenderer 画出柱状图并展示左右指针收缩求最大面积。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    n = len(height)
    max_h = max(height)
    bar_base_y = 380
    bar_top_y = 120
    bar_width = 50
    spacing = 10
    total_w = n * (bar_width + spacing) - spacing
    start_x = (WIDTH - total_w) // 2

    def bar_x(i):
        return start_x + i * (bar_width + spacing)

    def bar_height(val):
        return int((val / max_h) * (bar_base_y - bar_top_y))

    def draw_bars(fb_draw, left, right, area, best_area):
        font = get_font(16)
        font_sm = get_font(13)
        # Draw water area (shaded)
        if left < right:
            water_h = min(height[left], height[right])
            water_px_h = bar_height(water_h)
            x1 = bar_x(left) + bar_width
            x2 = bar_x(right)
            wy = bar_base_y - water_px_h
            draw_rounded_rect(fb_draw, (x1, wy, x2, bar_base_y),
                              0, fill="#1e3a5a", outline=None)

        # Draw bars
        for i in range(n):
            bx = bar_x(i)
            bh = bar_height(height[i])
            by = bar_base_y - bh
            if i == left:
                fill, outline = CellState.LEFT_PTR
            elif i == right:
                fill, outline = CellState.RIGHT_PTR
            elif left < i < right:
                fill = "#2d3b5a"
                outline = Colors.TEAL
            else:
                fill = Colors.OVERLAY
                outline = None
            draw_rounded_rect(fb_draw, (bx, by, bx + bar_width, bar_base_y),
                              4, fill=fill, outline=outline)
            # Value label on top
            tw, _ = text_size(fb_draw, str(height[i]), font_sm)
            fb_draw.text((bx + (bar_width - tw) // 2, by - 18),
                         str(height[i]), fill=Colors.TEXT, font=font_sm)
            # Index below
            tw2, _ = text_size(fb_draw, str(i), font_sm)
            fb_draw.text((bx + (bar_width - tw2) // 2, bar_base_y + 5),
                         str(i), fill=Colors.OVERLAY, font=font_sm)

        # Pointer labels
        if left < n:
            lx = bar_x(left) + bar_width // 2
            draw_pointer(fb_draw, lx, bar_base_y + 20, "L", Colors.SKY)
        if right < n:
            rx = bar_x(right) + bar_width // 2
            draw_pointer(fb_draw, rx, bar_base_y + 20, "R", Colors.PEACH)

        # Area info
        fb_draw.text((30, bar_base_y + 50),
                     f"当前面积: {area}  |  最大面积: {best_area}",
                     fill=Colors.YELLOW, font=font)

    left, right = 0, n - 1
    best_area = 0

    # Frame 1: initial
    def draw_init(fb):
        area = min(height[0], height[n-1]) * (n - 1)
        draw_bars(fb.draw, 0, n - 1, area, area)
    area_init = min(height[0], height[n-1]) * (n - 1)
    best_area = area_init
    yield f"初始: L=0, R={n-1}, 面积={area_init}", draw_init, DURATION_NORMAL

    while left < right:
        area = min(height[left], height[right]) * (right - left)
        best_area = max(best_area, area)

        def draw_step(fb, l=left, r=right, a=area, ba=best_area):
            draw_bars(fb.draw, l, r, a, ba)
        yield f"L={left}, R={right}, 面积={area}", draw_step, DURATION_NORMAL

        if height[left] < height[right]:
            left += 1
            move_desc = "左指针右移"
        else:
            right -= 1
            move_desc = "右指针左移"

        # Show after move
        area_new = min(height[left], height[right]) * (right - left) if left < right else 0
        best_area = max(best_area, area_new)

        def draw_move(fb, l=left, r=right, a=area_new, ba=best_area, md=move_desc):
            draw_bars(fb.draw, l, r, a, ba)
            fb.label(30, bar_base_y + 75, md, Colors.ACCENT)
        yield f"{move_desc}: L={left}, R={right}", draw_move, DURATION_NORMAL

    # Final
    def draw_final(fb, ba=best_area):
        draw_bars(fb.draw, left, right, 0, ba)
        fb.result_banner(f"最大盛水面积 = {ba}")
    yield "计算完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("11. 盛最多水的容器", generate, output_path,
                        width=WIDTH, height=HEIGHT + 50)
