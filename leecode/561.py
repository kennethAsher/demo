# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : 561.py
@ctime  : 2020/7/8 11:06
@Email  : 1131771202@qq.com
@content: 数组拆分
"""


''':Question
给定长度为 2n 的数组, 你的任务是将这些数分成 n 对, 例如 (a1, b1), (a2, b2), ..., (an, bn) ，
使得从1 到 n 的 min(ai, bi) 总和最大。

输入: [1,4,3,2]

输出: 4
解释: n 等于 2, 最大总和为 4 = min(1, 2) + min(3, 4).

'''

def function(nums):
    nums = sorted(nums)
    return sum(nums[0::2])
s = [1,4,3,2]
print(function(s))