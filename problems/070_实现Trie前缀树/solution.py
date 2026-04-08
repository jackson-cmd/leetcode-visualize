"""
208. 实现Trie前缀树 — 可视化
TrieRenderer 展示字典树随着单词插入逐步生长的过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    trie = {}
    operations = [
        ("insert", "apple"),
        ("insert", "app"),
        ("search", "app"),
        ("startsWith", "app"),
    ]

    renderer = TrieRenderer(y=100, level_gap=65, canvas_width=WIDTH)

    # Frame 1: empty trie
    def draw_init(fb):
        renderer.draw(fb.draw, {})
        fb.label(30, 450, "Trie: 前缀树，每个节点存一个字符", Colors.SUBTEXT)
    yield "空的Trie前缀树", draw_init, DURATION_NORMAL

    def insert_word(trie, word):
        node = trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['$'] = True  # end marker

    # Insert "apple" character by character
    word = "apple"
    node = trie
    for ci, ch in enumerate(word):
        if ch not in node:
            node[ch] = {}
        node = node[ch]
        if ci == len(word) - 1:
            node['$'] = True

        prefix = word[:ci + 1]

        def make_draw_insert(t, pref):
            import copy
            snap = copy.deepcopy(t)
            def draw_fn(fb):
                renderer.draw(fb.draw, snap, current_prefix=pref)
                fb.label(30, 450, f'insert("{word}"): 添加字符 \'{pref[-1]}\' -> 前缀 "{pref}"', Colors.YELLOW)
            return draw_fn

        import copy
        yield (f'insert("apple"): 添加 \'{ch}\'',
               make_draw_insert(copy.deepcopy(trie), prefix), DURATION_NORMAL)

    # Frame: apple inserted
    def draw_apple_done(fb):
        import copy
        renderer.draw(fb.draw, copy.deepcopy(trie))
        fb.label(30, 450, 'insert("apple") 完成! "e"节点标记为单词结尾', Colors.GREEN)
    yield 'insert("apple") 完成', draw_apple_done, DURATION_NORMAL

    # Insert "app"
    word2 = "app"
    node = trie
    for ch in word2:
        if ch not in node:
            node[ch] = {}
        node = node[ch]
    node['$'] = True

    def draw_app_insert(fb):
        import copy
        renderer.draw(fb.draw, copy.deepcopy(trie), current_prefix="app")
        fb.label(30, 450, 'insert("app"): 路径已存在, 标记"p"为单词结尾', Colors.YELLOW)
    yield 'insert("app"): 标记结尾', draw_app_insert, DURATION_NORMAL

    def draw_app_done(fb):
        import copy
        renderer.draw(fb.draw, copy.deepcopy(trie))
        fb.label(30, 450, 'insert("app") 完成! 现在"app"和"apple"都是有效单词', Colors.GREEN)
    yield 'insert("app") 完成', draw_app_done, DURATION_NORMAL

    # Search "app"
    def draw_search(fb):
        import copy
        states = {"a": CellState.CHECKING, "ap": CellState.CHECKING, "app": CellState.FOUND}
        renderer.draw(fb.draw, copy.deepcopy(trie), states=states, current_prefix="app")
        fb.label(30, 450, 'search("app"): 沿路径查找, "app"节点有结尾标记 -> True', Colors.GREEN)
    yield 'search("app") = True', draw_search, DURATION_NORMAL

    # StartsWith "app"
    def draw_starts(fb):
        import copy
        states = {"a": CellState.CHECKING, "ap": CellState.CHECKING, "app": CellState.FOUND}
        renderer.draw(fb.draw, copy.deepcopy(trie), states=states, current_prefix="app")
        fb.label(30, 450, 'startsWith("app"): 路径存在即可 -> True', Colors.GREEN)
    yield 'startsWith("app") = True', draw_starts, DURATION_NORMAL

    # Final frame
    def draw_final(fb):
        import copy
        renderer.draw(fb.draw, copy.deepcopy(trie))
        fb.result_banner("Trie 支持 O(m) 的插入和查询 (m为单词长度)")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("208. 实现Trie前缀树", generate, output_path)
