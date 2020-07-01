# Python数据结构与算法（4）——动态规划

思路：将一个问题拆成几个子问题，分别求解这些子问题，即可推断出大问题的解。

无后效性： 如果给定某一阶段的状态，则在这一阶段以后过程的发展不受这阶段以前各段状态的影响 。

最优子结构： 大问题的**最优解**可以由小问题的**最优解**推出。

如何判断一个问题能否使用DP解决？

——能将大问题拆成几个小问题，且满足无后效性、最优子结构性质。

### 例1.最长上升子序列

[leetcode 300. ](https://leetcode-cn.com/problems/longest-increasing-subsequence/)给定一个无序的整数数组，找到其中最长上升子序列的长度。 

设dp[i]为nums数组到i的子数组中，最长上升子序列的长度。

分析出递推关系：对于j in nums[:i]，如果nums[i]大于nums[j]，则dp[i] = dp[j]+1，且dp[i]只保留最大的那个结果。代码如下：

```python
def lengthOfLIS(nums: List[int]) -> int:
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

### 例2.最长重复子数组

[718.](https://leetcode-cn.com/problems/maximum-length-of-repeated-subarray/)给两个整数数组 `A` 和 `B` ，返回两个数组中公共的、长度最长的子数组的长度。 

