# 452. 用最少数量的箭引爆气球

## 题目描述
有一些球形气球贴在墙上，给你一个数组 `points`，其中 `points[i] = [start, end]` 表示第 `i` 个气球的水平直径范围。在 x 处射一支箭，可以引爆所有满足 `start <= x <= end` 的气球。求引爆所有气球所需的最少箭数。

## 解题思路
1. 按气球的右端点升序排序
2. 贪心策略：在当前最早结束的气球的右端点处放箭，尽可能多地引爆后续气球
3. 遍历排序后的气球，若当前气球的起点 > 上一支箭的位置，则需要新箭
4. 否则当前气球被已有的箭引爆

## 代码
```python
def findMinArrowShots(points):
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    for s, e in points[1:]:
        if s > end:
            arrows += 1
            end = e
    return arrows
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(n log n)，排序占主导
- **空间复杂度**: O(1)，只使用常数变量（不计排序空间）
