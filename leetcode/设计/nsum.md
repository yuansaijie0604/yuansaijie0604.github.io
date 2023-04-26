
<https://mp.weixin.qq.com/s?__biz=MzAxODQxMDM0Mw==&mid=2247485789&idx=1&sn=efc1167b85011c019e05d2c3db1039e6&chksm=9bd7f755aca07e43405baeac62c76b44d8438fe8a69ae77e87cbb5121e71b6ee46f4c626eb98&scene=21#wechat_redirect>

<https://labuladong.gitee.io/algo/2/21/69/>

## 1. 两数之和
https://leetcode-cn.com/problems/two-sum/

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        算法的时间复杂度降低到 O(N)，但是需要 O(N) 的空间复杂度来存储哈希表
        """
        tmp = {}
        for i,n in enumerate(nums):
            if target-n not in tmp:
                tmp[n] = i
            else:
                return [tmp[target-n], i]

        """
        为后续 nsum 铺路:此方法不适用，该题要的是索引，不是具体数值
                        排序之后，索引已被改变
        """
        # nums.sort()
        # left, right = 0, len(nums)-1
        
        # while left < right:
        #     s = nums[left] + nums[right]
        #     if s == target:
        #         return [left, right]
        #     elif s > target:
        #         right -= 1
        #     else:
        #         left += 1

        # return []
```

## 15. 三数之和
https://leetcode-cn.com/problems/3sum/

题目描述：

给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        优先思考 twoSum 怎么解决
        """
        nums.sort()
        res = []
        i = 0
        while i < len(nums)-1:
            p = nums[i]
            cases = self.twoSum(nums, i+1, -p)
            for k in cases:
                res.append([p, nums[k[0]], nums[k[1]]])
            # 注意去重
            while i < len(nums)-1 and nums[i] == p: i += 1
        return res


    def twoSum(self, nums, start, target) -> List[List[int]]:
        left, right = start, len(nums)-1
        res = []
        while left < right:
            s = nums[left] + nums[right]
            ln, rn = nums[left], nums[right]
            if s == target:
                res.append([left, right])
                # 注意去重
                while left < right and nums[left] == ln: left += 1
                while left < right and nums[right] == rn: right -= 1
            elif s < target:
                while left < right and nums[left] == ln: left += 1
            else:
                while left < right and nums[right] == rn: right -= 1

        return res
```

## 18. 四数之和
https://leetcode-cn.com/problems/4sum/

```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        """
        总结出 Nsum 的递归套路
        """
        nums.sort()
        return self.nSum(nums, 4, 0, target)

    def nSum(self, nums, n, start, target):
        res = []
        if n < 2 or len(nums) < n: return res
        if n == 2:
            left, right = start, len(nums)-1
            while left < right:
                s = nums[left] + nums[right]
                ln, rn = nums[left], nums[right]
                if s == target:
                    res.append([ln, rn])
                    # 注意去重
                    while left < right and nums[left] == ln: left += 1
                    while left < right and nums[right] == rn: right -= 1
                elif s < target:
                    while left < right and nums[left] == ln: left += 1
                else:
                    while left < right and nums[right] == rn: right -= 1
        else:
            i = start
            while i < len(nums):
                p = nums[i]
                cases = self.nSum(nums, n-1, i+1, target-p)
                for k in cases:
                    res.append([p] + k)
                
                # 去重
                while i < len(nums) and nums[i] == p: i += 1

        return res

```

## 170. 两数之和 III - 数据结构设计
https://leetcode-cn.com/problems/two-sum-iii-data-structure-design