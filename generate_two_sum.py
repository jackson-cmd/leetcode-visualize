"""Generate an animated GIF visualizing the Two Sum algorithm."""

from PIL import Image, ImageDraw, ImageFont
import os

# --- Configuration ---
WIDTH, HEIGHT = 800, 500
BG_COLOR = "#1e1e2e"
TEXT_COLOR = "#cdd6f4"
ACCENT = "#89b4fa"
GREEN = "#a6e3a1"
YELLOW = "#f9e2af"
RED = "#f38ba8"
PEACH = "#fab387"
SURFACE = "#313244"
OVERLAY = "#45475a"

nums = [4, 1, 12, 6, 8, 5]
target = 9

CELL_W, CELL_H = 70, 60
ARRAY_Y = 100
HASHMAP_Y = 300
DURATION_NORMAL = 800  # ms per frame
DURATION_RESULT = 2000


def get_font(size):
    """Try to load a good monospace font."""
    for name in [
        "/System/Library/Fonts/SFMono-Regular.otf",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.dfont",
        "/Library/Fonts/Courier New.ttf",
    ]:
        if os.path.exists(name):
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
    return ImageFont.load_default()


font = get_font(22)
font_sm = get_font(16)
font_lg = get_font(28)
font_title = get_font(20)


def draw_rounded_rect(draw, xy, radius, fill, outline=None):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)


def draw_cell(draw, x, y, value, color=SURFACE, text_color=TEXT_COLOR, outline=None):
    draw_rounded_rect(draw, (x, y, x + CELL_W, y + CELL_H), 10, fill=color, outline=outline)
    text = str(value)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x + (CELL_W - tw) // 2, y + (CELL_H - th) // 2), text, fill=text_color, font=font)


def make_frame(step_info):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Title
    title = f"Two Sum — target = {target}"
    bbox = draw.textbbox((0, 0), title, font=font_lg)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 20), title, fill=ACCENT, font=font_lg)

    # Subtitle / step description
    desc = step_info.get("desc", "")
    bbox = draw.textbbox((0, 0), desc, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 60), desc, fill=YELLOW, font=font_title)

    # Array label
    draw.text((30, ARRAY_Y - 5), "nums[]", fill=TEXT_COLOR, font=font_sm)

    # Draw array
    current_idx = step_info.get("current_idx", -1)
    found_pair = step_info.get("found_pair", None)
    check_idx = step_info.get("check_idx", -1)

    array_start_x = (WIDTH - len(nums) * (CELL_W + 10)) // 2
    for i, num in enumerate(nums):
        x = array_start_x + i * (CELL_W + 10)
        # Index label
        idx_text = str(i)
        bbox = draw.textbbox((0, 0), idx_text, font=font_sm)
        idx_tw = bbox[2] - bbox[0]
        draw.text((x + (CELL_W - idx_tw) // 2, ARRAY_Y - 20), idx_text, fill=OVERLAY, font=font_sm)

        if found_pair and i in found_pair:
            draw_cell(draw, x, ARRAY_Y, num, color="#2d5a2d", outline=GREEN)
        elif i == current_idx:
            draw_cell(draw, x, ARRAY_Y, num, color="#3b3b5a", outline=ACCENT)
        elif i == check_idx:
            draw_cell(draw, x, ARRAY_Y, num, color="#5a3b3b", outline=PEACH)
        else:
            draw_cell(draw, x, ARRAY_Y, num)

    # Arrow for current
    if current_idx >= 0 and not found_pair:
        ax = array_start_x + current_idx * (CELL_W + 10) + CELL_W // 2
        draw.text((ax - 5, ARRAY_Y + CELL_H + 5), "▲", fill=ACCENT, font=font_sm)
        draw.text((ax - 5, ARRAY_Y + CELL_H + 22), "i", fill=ACCENT, font=font_sm)

    # Hash map section
    draw.text((30, HASHMAP_Y - 30), "HashMap { value → index }", fill=TEXT_COLOR, font=font_sm)
    hashmap = step_info.get("hashmap", {})

    if hashmap:
        hm_items = list(hashmap.items())
        cols = min(len(hm_items), 4)
        row_h = 40
        col_w = 170
        hm_start_x = (WIDTH - cols * col_w) // 2
        for idx, (val, orig_idx) in enumerate(hm_items):
            row = idx // cols
            col = idx % cols
            x = hm_start_x + col * col_w
            y = HASHMAP_Y + row * row_h

            entry = f"{val} → {orig_idx}"
            highlight = step_info.get("hm_highlight", None)
            if highlight is not None and val == highlight:
                draw_rounded_rect(draw, (x, y, x + col_w - 10, y + row_h - 5), 8, fill="#2d5a2d", outline=GREEN)
            else:
                draw_rounded_rect(draw, (x, y, x + col_w - 10, y + row_h - 5), 8, fill=SURFACE)
            bbox = draw.textbbox((0, 0), entry, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((x + (col_w - 10 - tw) // 2, y + (row_h - 5 - th) // 2), entry, fill=TEXT_COLOR, font=font)
    else:
        draw.text(((WIDTH - 60) // 2, HASHMAP_Y + 10), "{ empty }", fill=OVERLAY, font=font_sm)

    # Result banner
    if found_pair:
        result_text = f"Found! nums[{found_pair[0]}] + nums[{found_pair[1]}] = {target}  →  [{found_pair[0]}, {found_pair[1]}]"
        bbox = draw.textbbox((0, 0), result_text, font=font_lg)
        tw = bbox[2] - bbox[0]
        y_pos = HEIGHT - 60
        draw_rounded_rect(draw, ((WIDTH - tw) // 2 - 20, y_pos - 10, (WIDTH + tw) // 2 + 20, y_pos + 40), 12, fill="#2d5a2d", outline=GREEN)
        draw.text(((WIDTH - tw) // 2, y_pos), result_text, fill=GREEN, font=font_lg)

    return img


def generate_frames():
    frames = []
    durations = []
    hashmap = {}

    # Frame 0: Initial state
    frames.append(make_frame({"desc": "Initialize empty HashMap", "hashmap": {}}))
    durations.append(DURATION_NORMAL)

    for i in range(len(nums)):
        complement = target - nums[i]

        # Frame: checking current element
        frames.append(make_frame({
            "desc": f"Step {i+1}: Check nums[{i}] = {nums[i]}, complement = {target} - {nums[i]} = {complement}",
            "current_idx": i,
            "hashmap": dict(hashmap),
        }))
        durations.append(DURATION_NORMAL)

        if complement in hashmap:
            # Found!
            j = hashmap[complement]
            # Highlight the complement in hashmap
            frames.append(make_frame({
                "desc": f"complement {complement} found in HashMap at index {j}!",
                "current_idx": i,
                "check_idx": j,
                "hashmap": dict(hashmap),
                "hm_highlight": complement,
            }))
            durations.append(DURATION_NORMAL)

            # Result frame
            frames.append(make_frame({
                "desc": f"Return [{j}, {i}]",
                "found_pair": (j, i),
                "hashmap": dict(hashmap),
                "hm_highlight": complement,
            }))
            durations.append(DURATION_RESULT)
            return frames, durations

        # Add to hashmap
        hashmap[nums[i]] = i
        frames.append(make_frame({
            "desc": f"Add nums[{i}] = {nums[i]} to HashMap",
            "current_idx": i,
            "hashmap": dict(hashmap),
        }))
        durations.append(DURATION_NORMAL)

    return frames, durations


def main():
    frames, durations = generate_frames()
    out_path = os.path.join(os.path.dirname(__file__), "two_sum.gif")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    print(f"Generated {out_path} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
