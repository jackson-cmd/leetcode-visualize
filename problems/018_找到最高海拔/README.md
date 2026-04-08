# 1732. 找到最高海拔

## 题目描述
有一个自行车手打算进行一场公路骑行，这条路线总共由 `n + 1` 个不同海拔的点组成。自行车手从海拔为 0 的起点出发。给你一个长度为 n 的整数数组 `gain`，其中 `gain[i]` 是第 `i` 个点和第 `i + 1` 个点的净海拔高度差。请返回最高点的海拔。

## 解题思路
1. 从海拔 0 开始，逐步累加 gain 数组的值得到每个点的海拔
2. 这就是一个前缀和问题
3. 在计算过程中维护最大海拔值即可

## 代码
```python
def largestAltitude(gain):
    altitude = 0
    max_alt = 0
    for g in gain:
        altitude += g
        max_alt = max(max_alt, altitude)
    return max_alt
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(n)，遍历一次 gain 数组
- **空间复杂度**: O(1)，只使用常数额外空间
