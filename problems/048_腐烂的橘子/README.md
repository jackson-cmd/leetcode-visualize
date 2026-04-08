# 994. 腐烂的橘子

## 题目描述
在给定的 `m x n` 网格中，每个单元格可以是空 (0)、新鲜橘子 (1) 或腐烂橘子 (2)。每分钟，腐烂橘子的上下左右相邻的新鲜橘子都会腐烂。返回直到所有橘子都腐烂所需的最少分钟数，如果不可能返回 -1。

## 解题思路
1. 找到所有初始腐烂的橘子作为 BFS 起点（多源 BFS）
2. 每一轮 BFS 代表一分钟，向四个方向扩散
3. 统计最终需要的分钟数
4. 如果仍有新鲜橘子未被感染，返回 -1

## 代码
```python
from collections import deque

def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, t+1))
                minutes = t + 1
    return -1 if fresh > 0 else minutes
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(m * n)，每个格子最多访问一次
- **空间复杂度**: O(m * n)，用于 BFS 队列
