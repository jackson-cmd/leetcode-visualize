# 283. 移动零

## 题目描述
给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。必须在不复制数组的情况下原地对数组进行操作。

## 解题思路
1. 使用快慢双指针：`slow` 指向下一个非零元素应放置的位置，`fast` 遍历数组
2. 当 `fast` 遇到非零元素时，与 `slow` 位置交换，然后 `slow` 前进
3. 当 `fast` 遇到零时，直接跳过继续前进
4. 遍历结束后所有零自然被移到末尾

## 代码
```python
def moveZeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(n)，其中 n 为数组长度
- **空间复杂度**: O(1)，原地操作
