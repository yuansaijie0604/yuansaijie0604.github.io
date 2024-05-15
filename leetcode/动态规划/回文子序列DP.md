

## 516. 最长回文子序列
https://leetcode-cn.com/problems/longest-palindromic-subsequence/

```python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        """
        DPtable：s[i,j]子串的最长回文子序列为 dptable[i,j]
        """ 
        dptable = [[0]*len(s) for _ in range(len(s))]

        for i in range(len(s)):
            dptable[i][i] = 1   # i==j时，即对角线值为 1

        # 根据状态转移，需要 反向遍历 或 对角线遍历
        # dp[i,j-1]     *dp[i][j]*
        # dp[i+1,j-1]   dp[i+1][j]
        for i in range(len(s)-1, -1, -1):
            for j in range(i+1, len(s)):
                if s[i] == s[j]:
                    dptable[i][j] = dptable[i+1][j-1] + 2
                else:
                    dptable[i][j] = max(dptable[i][j-1], \
                                        dptable[i+1][j])

        return dptable[0][len(s)-1]

        """
        状态压缩: 将二维的dp数组转化成一维，空间复杂度从 O(N^2) 降低到 O(N)
        """
        dptable = [1] * len(s)   # 计算i行数据时，仅依赖i+1行的值，竖向压平
        for i in range(len(s)-1, -1, -1):
            pre = 0
            for j in range(i+1, len(s)):
                tmp = dptable[j]
                if s[i] == s[j]:
                    dptable[j] = pre + 2
                else:
                    dptable[j] = max(dptable[j-1], dptable[j])
                pre = tmp

        return dptable[len(s)-1]

```

## 647. 回文子串
https://leetcode-cn.com/problems/palindromic-substrings/

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        dp[i][j]表示区间范围[i,j]的子串是否是回文子串。
        """
        dp = [[False] * len(s) for _ in range(len(s))]
        result = 0
        for i in range(len(s)-1, -1, -1): #注意遍历顺序
            for j in range(i, len(s)):
                if s[i] == s[j] and (j - i <= 1 or dp[i+1][j-1]): 
                    result += 1
                    dp[i][j] = True
        return result
```
双指针解法：首先确定回文串，就是找中心然后想两边扩散看是不是对称的就可以了。
```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        result = 0
        for i in range(len(s)):
            result += self.extend(s, i, i, len(s)) #以i为中心
            result += self.extend(s, i, i+1, len(s)) #以i和i+1为中心
        return result

    def extend(self, s, i, j, n):
        res = 0
        while i >= 0 and j < n and s[i] == s[j]:
            i -= 1
            j += 1
            res += 1
        return res
```

### 5. 最长回文子串
https://leetcode-cn.com/problems/longest-palindromic-substring/

基于上一题，过程中保留最长的回文子串

加入start，end变量记录最长结果
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        dp[i][j]表示区间范围[i,j]的子串是否是回文子串。
        """
        dp = [[False] * len(s) for _ in range(len(s))]

        start, end = 0, 1 # 记录最长结果

        for i in range(len(s)-1, -1, -1):
            for j in range(i, len(s)):
                if s[i]==s[j] and (j-i<=1 or dp[i+1][j-1]):
                    dp[i][j] = True
                    if j-i+1 > end - start:
                        start, end = i, j+1
        
        return s[start:end]
```

双指针解法

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        start, end = 0, 1
        for i in range(len(s)):
            start1, end1 = self.extend(s, i, i, len(s))
            start2, end2 = self.extend(s, i, i+1, len(s))
            if end1-start1+1 > end-start:
                start, end = start1, end1+1
            if end2-start2+1 > end-start:
                start, end = start2, end2+1
        return s[start:end]

    def extend(self, s, i, j, n):
        while i>=0  and j<n and s[i]==s[j]:
            i -= 1
            j += 1
        return i+1, j-1
```

### 131. 分割回文串 - 所有分割方案，分割后的子串均满足回文
https://leetcode-cn.com/problems/palindrome-partitioning/

采用回溯的方式
```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res = []

        def dfs(track, start):
            if start>=len(s):
                res.append(track[:])
            for i in range(start, len(s)):
                if self._isPalindrome(s[start:i+1]):
                    track.append(s[start:i+1])
                    dfs(track, i+1)
                    track.pop(-1)

        dfs([], 0)

        return res

    def _isPalindrome(self, s: str) -> bool:
        i, j = 0, len(s)-1
        while i<j:
            if s[i]!=s[j]:
                return False
            i, j = i+1, j-1
        return True
```

优化方向：采用动态规划，把是否为回文子串的结果计算好。
```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        dp = [[True] * len(s) for _ in range(len(s))] # 反正左下角也用不上，设置什么值都可以，但是对角线得是True

        for i in range(len(s)-1, -1, -1):
            for j in range(i+1, len(s)):
                dp[i][j] = (s[i]==s[j] and dp[i+1][j-1])

        res = []
        track = []
        def dfs(start):
            if start == len(s):
                res.append(track[:])
                return

            for i in range(start, len(s)):
                if dp[start][i]:
                    track.append(s[start:i+1])
                    dfs(i+1)
                    track.pop(-1)
        dfs(0)
        return res
```

### 132. 分割回文串 II - 最少分割次数
https://leetcode-cn.com/problems/palindrome-partitioning-ii/

采用动态规划，把是否为回文串的结果存储好；再进行题干的动态规划。
```python
class Solution:
    def minCut(self, s: str) -> int:
        dp = [[True] * len(s) for _ in range(len(s))]

        for i in range(len(s)-1, -1, -1):
            for j in range(i+1, len(s)):
                dp[i][j] = (s[i]==s[j] and dp[i+1][j-1])

        """
        f[i]:以i为结尾的字符串s的最小分割次数
        """
        f = [float('inf') for _ in range(len(s))]
        for i in range(len(s)):
            if dp[0][i]: # 回文无须分割
                f[i] = 0
            else:
                for j in range(i):
                    if dp[j+1][i]:
                        f[i] = min(f[i], f[j] + 1)
        return f[-1]
```

### 1745. 回文串分割 IV - 限定分割成三个非空的回文子串
https://leetcode-cn.com/problems/palindrome-partitioning-iv/

在131的基础上，修改dfs的内容
```python
class Solution:
    def checkPartitioning(self, s: str) -> bool:
        dp = [[True] * len(s) for _ in range(len(s))]

        for i in range(len(s)-1, -1, -1):
            for j in range(i+1, len(s)):
                dp[i][j] = (s[i]==s[j] and dp[i+1][j-1])

        def dfs(start: int, k: int = 3) -> bool:
            if k==1 and start<len(s):
                return dp[start][-1]  # 尽早返回
            if start==len(s) :
                return False

            for i in range(start, len(s)):
                if dp[start][i]:
                    if dfs(i+1, k-1):
                        return True
            return False
                    
        return dfs(0)
```

## 1278. 分割回文串 III

https://leetcode-cn.com/problems/palindrome-partitioning-iii/

```python
class Solution:
    def palindromePartition(self, s: str, k: int) -> int:

        def cost(l, r):
            # 把s[l,r]变成回文串需要修改多少个字符
            ret, i, j = 0, l, r
            while i < j:
                ret += (0 if s[i] == s[j] else 1)
                i += 1
                j -= 1
            return ret
        """
        f[i][j] 表示对于字符串 s 的前 i 个字符，将它分割成 j 个非空且不相交的回文串，最少需要修改的字符数。
        """
        n = len(s)
        f = [[10**9] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, min(k, i) + 1):
                if j == 1:
                    f[i][j] = cost(0, i - 1)
                else:
                    for i0 in range(j - 1, i):
                        f[i][j] = min(f[i][j], f[i0][j - 1] + cost(i0, i - 1))
        
        return f[n][k]
```

## 其他

### 1771. 由子序列构造的最长回文串的长度

https://leetcode-cn.com/problems/maximize-palindrome-length-from-subsequences/



### 730. 统计不同回文子字符串

https://leetcode-cn.com/problems/count-different-palindromic-subsequences/


