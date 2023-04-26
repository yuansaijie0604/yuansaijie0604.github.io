# 二叉树遍历

## 前中后序遍历

### [144.二叉树的前序遍历]([https://leetcode.cn/problems/binary-tree-preorder-traversal/](https://leetcode.cn/problems/binary-tree-preorder-traversal/))

```python
from typing import List
# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        
        result = []
        if not root: return []

        # 递归前序遍历
        return [root.val] \
                + self.preorderTraversal(root.left) \
                + self.preorderTraversal(root.right)
        
        # 非递归前序遍历
        from collections import deque
        stack = deque()
        stack.append(root)
        while stack:
            t = stack.pop()
            result.append(t.val)

            if t.right: stack.append(t.right)
            if t.left: stack.append(t.left)

        return resultpython
```

### [94.二叉树的中序遍历]([https://leetcode-cn.com/problems/binary-tree-inorder-traversal/](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/))

```python
class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        if not root: return []
        # 递归中序遍历
        return self.inorderTraversal(root.left) \
               + [root.val]
               + self.inorderTraversal(root.right)
        
        # 非递归中序遍历
        from collections import deque
        stack = deque()
        cur = root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            t = stack.pop()
            result.append(t.val)
            cur = t.right
            
        # 非递归中序遍历(更喜欢这个版本， from 代码随想录)
        from collections import deque
        stack = deque()
        cur = root
        while cur or stack:
            # 先迭代访问最底层的左子树结点
            if cur:
                stack.append(cur)
                cur = cur.left
            else:
                cur = stack.pop()
                result.append(cur.val)
                # 取栈顶元素右结点
                cur = cur.right
        
        return result
```

### [145. 二叉树的后序遍历](https://leetcode-cn.com/problems/binary-tree-postorder-traversal/)

```python
class Solution: 
    def postorderTraversal(self, root: TreeNode) -> List[int]: 
        result = [] 
        if not root: return []
        # 递归后序遍历
        return self.postorderTraversal(root.left) \
            + self.postorderTraversal(root.right) \
                + [root.val] 
    
        # 非递归后序遍历
        # 思路1: 仿照前序遍历的思路得到左右中，在逆向打印
        # 思路2: 和其他非递归方式一样，利用栈
        stack = []
        cur = root
    
        stack.append(root)
        while stack:
            t = stack[-1]
            if t.left and t.left != cur and t.right != cur:
                stack.append(t.left)
            elif t.right and t.right!=cur:
                stack.append(t.right)
            else:
                result.append(stack.pop().val)
                cur = t
    
        return result
```

### ❤ 二叉树的统一迭代法

[https://programmercarl.com/二叉树的统一迭代法.html#总结](https://programmercarl.com/二叉树的统一迭代法.html#总结 "https://programmercarl.com/二叉树的统一迭代法.html#总结")

-   对“中”这个位置加一个flag
    ```python
    class Solution:
        def preorderTraversal(self, root: TreeNode) -> List[int]:
            result = []
            st= []
            if root:
                st.append(root)
            while st:
                node = st.pop()
                if node != None:
                    if node.right: #右
                        st.append(node.right)
                    if node.left: #左
                        st.append(node.left)
                    st.append(node) #中
                    st.append(None)
                else:
                    node = st.pop()
                    result.append(node.val)
            return result
    
    ```
    ```python
    class Solution:
        def inorderTraversal(self, root: TreeNode) -> List[int]:
            result = []
            st = []
            if root:
                st.append(root)
            while st:
                node = st.pop()
                if node != None:
                    if node.right: #添加右节点（空节点不入栈）
                        st.append(node.right)
                    
                    st.append(node) #添加中节点
                    st.append(None) #中节点访问过，但是还没有处理，加入空节点做为标记。
                    
                    if node.left: #添加左节点（空节点不入栈）
                        st.append(node.left)
                else: #只有遇到空节点的时候，才将下一个节点放进结果集
                    node = st.pop() #重新取出栈中元素
                    result.append(node.val) #加入到结果集
            return result
    ```
    ```python
    class Solution:
        def postorderTraversal(self, root: TreeNode) -> List[int]:
            result = []
            st = []
            if root:
                st.append(root)
            while st:
                node = st.pop()
                if node != None:
                    st.append(node) #中
                    st.append(None)
                    
                    if node.right: #右
                        st.append(node.right)
                    if node.left: #左
                        st.append(node.left)
                else:
                    node = st.pop()
                    result.append(node.val)
            return result
    ```


## 层序遍历

### [102. 二叉树的层序遍历](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/ "102. 二叉树的层序遍历")

```python
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root: return []

        res = []
        stack = [root]
        while stack:
            levelnode = []
            len_ = len(stack)
            for _ in range(len_):
                t = stack.pop(0)   # 从队首取出元素
                levelnode.append(t.val)
                if t.left:
                    stack.append(t.left)
                if t.right:
                    stack.append(t.right)
            res.append(levelnode)
        
        return res
```

### [107. 二叉树的层序遍历 II](https://leetcode-cn.com/problems/binary-tree-level-order-traversal-ii/ "107. 二叉树的层序遍历 II")

题目描述：给定一个二叉树，返回其节点值自底向上的层序遍历。 （即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）

题解：按照[102. 二叉树的层序遍历](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/ "102. 二叉树的层序遍历")，只要把输出反转打印`res[::-1]`即可。

> 📌为什么不在构建 `res` 的时候，用头部插入？
> 因为根据list特性，这样会增加时间开销。


### [103. 二叉树的锯齿形层序遍历](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/ "103. 二叉树的锯齿形层序遍历")

题目描述：给定一个二叉树，返回其节点值的锯齿形层序遍历。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

例如：给定二叉树 \[3,9,20,null,null,15,7]

3

/ \\

9  20

/  \\

15   7

返回锯齿形层序遍历如下：`[[3], [20, 9], [15, 7]]`

题解：加一个标识符，表示当前应该从左往右还是从右往左。

```python
class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root: return []

        res = []
        stack = [root]
        islr = True
        while stack:
            levelnode = []
            len_ = len(stack)
            for _ in range(len_):
                t = stack.pop(0)   # 从队首取出元素
                levelnode.append(t.val)
                if t.left:
                    stack.append(t.left)
                if t.right:
                    stack.append(t.right)
            if islr:
                res.append(levelnode)
            else:
                res.append(levelnode[::-1])
            islr = not islr

        return res
```

### [116. 填充每个节点的下一个右侧节点指针](https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/ "116. 填充每个节点的下一个右侧节点指针")

题目描述：给定一个 完美二叉树 ，其所有叶子节点都在同一层，每个父节点都有两个子节点。二叉树定义如下：

struct Node {

int val;

Node \*left;

Node \*right;

Node \*next;

}

填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL。

初始状态下，所有 next 指针都被设置为 NULL。

![](../images/image_40STV56bUP.png)

题解：利用层次遍历。

```python
import collections 

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        
        if not root: return root
        
        Q = collections.deque([root])
        
        # 外层的 while 循环迭代的是层数
        while Q:
            len_ = len(Q)   # 记录当前队列大小
            
            # 遍历这一层的所有节点
            for i in range(len_):
                node = Q.popleft()   # 从队首取出元素
                
                # 连接
                if i < len_ - 1:
                    node.next = Q[0]
                
                # 拓展下一层节点
                if node.left:
                    Q.append(node.left)
                if node.right:
                    Q.append(node.right)
        
        # 返回根节点
        return root

```


