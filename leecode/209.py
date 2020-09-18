# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : 209.py
@ctime  : 2020/7/9 19:56
@Email  : 1131771202@qq.com
@content: 长度最小的子数组
"""

""":Question
给定一个含有 n 个正整数的数组和一个正整数 s ，找出该数组中满足其和 ≥ s 的长度最小的子数组，并返回其长度。如果不存在符合条件的子数组，返回 0

示例：
    输入：s = 7, nums = [2,3,1,2,4,3]
    输出：2
    解释：子数组 [4,3] 是该条件下的长度最小的子数组。
"""

def funtion(s, nums):
    min_number = len(nums)
    current_number = 0
    current_len = 0
    x = 0
    for i in range(len(nums)):
        current_number = current_number+nums[i]
        current_len += 1
        if current_number >= s:
            min_number = min(min_number, current_len)
            current_len = current_len -1
            current_number = current_number - nums[x]
            x = x+1
    return min_number

nums = [2,3,1,2,4,3]
s = 7
print(funtion(s, nums))
