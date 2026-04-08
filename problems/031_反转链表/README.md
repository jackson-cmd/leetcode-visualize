# 206. 反转链表

## 题目描述
给你单链表的头节点 `head`，请你反转链表，并返回反转后的链表。

## 解题思路
1. 使用三个指针：`prev`（前驱）、`curr`（当前）、`next`（后继）
2. 每一步保存 `curr.next` 到 `next`
3. 将 `curr.next` 指向 `prev`（反转当前链接）
4. 移动 `prev` 和 `curr` 各前进一步
5. 当 `curr` 为 None 时，`prev` 即为新的头节点

## 代码
```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

## 动画演示
![solution](solution.gif)

## 复杂度分析
- **时间复杂度**: O(n)，遍历链表一次
- **空间复杂度**: O(1)，只使用常数额外空间
