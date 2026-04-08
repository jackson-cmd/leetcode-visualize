# 208. 实现Trie前缀树

## 题目描述
实现一个 Trie（前缀树），包含 `insert`、`search` 和 `startsWith` 三个操作。`insert` 向前缀树中插入字符串，`search` 查找完整单词是否存在，`startsWith` 查找是否有以给定前缀开头的单词。

## 解题思路
1. 使用嵌套字典/哈希表构建树结构，每个节点包含子节点映射
2. 插入：沿路径逐字符插入，不存在则创建新节点，末尾标记为单词结尾
3. 搜索：沿路径逐字符查找，到达末尾时检查是否有结尾标记
4. 前缀查找：类似搜索，但不需要检查结尾标记，路径存在即可

## 代码
```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['$'] = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return '$' in node

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(m)，每个操作的时间复杂度与单词长度 m 成正比
- **空间复杂度**: O(N * m)，N 为插入的单词数，m 为平均长度
