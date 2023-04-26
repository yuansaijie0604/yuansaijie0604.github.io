<https://labuladong.gitee.io/algo/3/24/>

![](../images/image_KS4WW93SaQ.png)

# 最长公共子序列

## 1143. 最长公共子序列
https://leetcode-cn.com/problems/longest-common-subsequence/

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """
        DPtable: text1[:i] 和 text[:j] 的 LCS 值
        """
        m = len(text1)
        n = len(text2)
        dptable = [[0] * (n+1) for _ in range(m+1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dptable[i][j] = dptable[i-1][j-1] + 1
                else:
                    dptable[i][j] = max(dptable[i-1][j], dptable[i][j-1])
        
        return dptable[m][n]
        
```

## 1035. 不相交的线
https://leetcode-cn.com/problems/uncrossed-lines/

## 718. 最长重复子数组
https://leetcode-cn.com/problems/maximum-length-of-repeated-subarray/

[https://programmercarl.com/0718.最长重复子数组.html](https://programmercarl.com/0718.最长重复子数组.html "https://programmercarl.com/0718.最长重复子数组.html")

## 1458. 两个子序列的最大点积
https://leetcode-cn.com/problems/max-dot-product-of-two-subsequences/

# 最长上升子序列

## 300. 最长递增子序列
https://leetcode-cn.com/problems/longest-increasing-subsequence/

## 354. 俄罗斯套娃信封问题
https://leetcode-cn.com/problems/russian-doll-envelopes/

## 673. 最长递增子序列的个数
https://leetcode-cn.com/problems/number-of-longest-increasing-subsequence/

## 674. 最长连续递增序列
https://leetcode-cn.com/problems/longest-continuous-increasing-subsequence/ 

## 1626. 无矛盾的最佳球队
https://leetcode-cn.com/problems/best-team-with-no-conflicts/

## 1964. 找出到每个位置为止最长的有效障碍赛跑路线
https://leetcode-cn.com/problems/find-the-longest-valid-obstacle-course-at-each-position/

# 其他

## 53.最大子序和
https://leetcode-cn.com/problems/maximum-subarray/

## 1092. 最短公共超序列
https://leetcode-cn.com/problems/shortest-common-supersequence/

## 1218. 最长定差子序列
https://leetcode-cn.com/problems/longest-arithmetic-subsequence-of-given-difference/

## 1911. 最大子序列交替和
https://leetcode-cn.com/problems/maximum-alternating-subsequence-sum/

## 943. 最短超级串
https://leetcode-cn.com/problems/find-the-shortest-superstring/



# 编辑距离

[72. 编辑距离](https://leetcode-cn.com/problems/edit-distance/)

[583. 两个字符串的删除操作](https://leetcode-cn.com/problems/delete-operation-for-two-strings/)

[712. 两个字符串的最小 ASCII 删除和](https://leetcode-cn.com/problems/minimum-ascii-delete-sum-for-two-strings/)

[97. 交错字符串](https://leetcode-cn.com/problems/interleaving-string/)

[1312. 让字符串成为回文串的最少插入次数](https://leetcode-cn.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/)

# 正则表达式匹配

[678. 有效的括号字符串](https://leetcode-cn.com/problems/valid-parenthesis-string/) (中等)

[10. 正则表达式匹配](https://leetcode-cn.com/problems/regular-expression-matching/) (困难)

[44. 通配符匹配](https://leetcode-cn.com/problems/wildcard-matching/) (困难)

[639. 解码方法 2](https://leetcode-cn.com/problems/decode-ways-ii/) (困难)
