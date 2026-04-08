# 1268. 搜索推荐系统

## 题目描述
给你一个产品数组 `products` 和一个字符串 `searchWord`。每输入 `searchWord` 的一个字符后，返回产品列表中最多三个字典序最小的、以当前输入为前缀的产品。

## 解题思路
1. 将产品列表排序，确保字典序
2. 构建 Trie 前缀树，将所有产品插入
3. 每输入一个字符，沿 Trie 查找对应节点
4. 从该节点出发 DFS 收集最多 3 个完整单词作为推荐（排序保证字典序最小）

## 代码
```python
def suggestedProducts(products, searchWord):
    products.sort()
    trie = {}
    for word in products:
        node = trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['$'] = True

    def collect(node, prefix, res):
        if len(res) >= 3:
            return
        if '$' in node:
            res.append(prefix)
        for ch in sorted(node):
            if ch != '$':
                collect(node[ch], prefix + ch, res)

    result = []
    node = trie
    prefix = ""
    for ch in searchWord:
        prefix += ch
        if node and ch in node:
            node = node[ch]
            suggestions = []
            collect(node, prefix, suggestions)
            result.append(suggestions)
        else:
            node = None
            result.append([])
    return result
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(N * m + L * 3)，N 为产品数，m 为平均长度，L 为搜索词长度
- **空间复杂度**: O(N * m)，Trie 存储空间
