"""
1268. 搜索推荐系统 — 可视化
TrieRenderer 展示字典树 + 每输入一个字符显示推荐结果。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
import copy


def generate():
    products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    products.sort()  # Sort lexicographically
    search_word = "mouse"

    # Build trie
    trie = {}
    for word in products:
        node = trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['$'] = True

    renderer = TrieRenderer(y=80, level_gap=55, node_r=16, canvas_width=WIDTH_WIDE)

    # Frame 1: show sorted products and empty trie
    def draw_init(fb):
        fb.label(30, 80, f"产品列表(已排序): {products}", Colors.SUBTEXT)
        fb.label(30, 110, f'搜索词: "{search_word}"', Colors.ACCENT)
        fb.label(30, 150, "排序后构建Trie, 每输入一个字符返回至多3个推荐", Colors.YELLOW)
    yield "初始化: 排序产品列表", draw_init, DURATION_NORMAL

    # Frame 2: show trie built
    def draw_trie(fb):
        renderer.draw(fb.draw, copy.deepcopy(trie))
        fb.label(30, 470, "Trie构建完成, 绿色边框=单词结尾", Colors.GREEN)
    yield "构建Trie前缀树", draw_trie, DURATION_NORMAL

    # Search character by character
    def collect_words(node, prefix, results, limit=3):
        if len(results) >= limit:
            return
        if '$' in node:
            results.append(prefix)
        for ch in sorted(node.keys()):
            if ch == '$':
                continue
            if len(results) >= limit:
                return
            collect_words(node[ch], prefix + ch, results, limit)

    prefix = ""
    node = trie
    for ci, ch in enumerate(search_word):
        prefix += ch
        if ch in node:
            node = node[ch]
            # Collect suggestions
            suggestions = []
            collect_words(node, prefix, suggestions, 3)
        else:
            node = None
            suggestions = []

        def make_draw(pref, suggs, t):
            def draw_fn(fb):
                if t is not None:
                    renderer.draw(fb.draw, copy.deepcopy(trie), current_prefix=pref)
                else:
                    renderer.draw(fb.draw, copy.deepcopy(trie))

                # Show search input and suggestions
                fb.label(30, 440, f'输入: "{pref}"', Colors.ACCENT)
                if suggs:
                    sugg_text = ", ".join(f'"{s}"' for s in suggs)
                    fb.label(30, 465, f"推荐: {sugg_text}", Colors.GREEN)
                else:
                    fb.label(30, 465, "推荐: []", Colors.OVERLAY)
            return draw_fn

        sugg_copy = suggestions[:]
        yield (f'输入"{prefix}" -> {len(suggestions)}个推荐',
               make_draw(prefix, sugg_copy, node), DURATION_NORMAL)

        if node is None:
            break

    # Final frame
    def draw_final(fb):
        renderer.draw(fb.draw, copy.deepcopy(trie))
        fb.result_banner("搜索推荐系统: Trie + DFS 收集前缀匹配")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1268. 搜索推荐系统", generate, output_path,
                        width=WIDTH_WIDE, height=HEIGHT_TALL)
