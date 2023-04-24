# 二叉树遍历

## 前中后序遍历

### \[144.二叉树的前序遍历]\([https://leetcode.cn/problems/binary-tree-preorder-traversal/](https://leetcode.cn/problems/binary-tree-preorder-traversal/))

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

### \[94.二叉树的中序遍历]\([https://leetcode-cn.com/problems/binary-tree-inorder-traversal/](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/))

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

### [**145. 二叉树的后序遍历**](https://leetcode-cn.com/problems/binary-tree-postorder-traversal/)

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

