# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : 167.py
@ctime  : 2020/7/8 11:24
@Email  : 1131771202@qq.com
@content: 两数之和 II - 输入有序数组
"""

''':Question
给定一个已按照升序排列 的有序数组，找到两个数使得它们相加之和等于目标数。
函数应该返回这两个下标值 index1 和 index2，其中 index1 必须小于 index2。

说明:
    返回的下标值（index1 和 index2）不是从零开始的。
    你可以假设每个输入只对应唯一的答案，而且你不可以重复使用相同的元素。

示例:
输入: numbers = [2, 7, 11, 15], target = 9
输出: [1,2]
解释: 2 与 7 之和等于目标数 9 。因此 index1 = 1, index2 = 2 。

'''

def twoSum(numbers, target):
    l = 0
    r = len(numbers)-1
    while l < r:
        sum = numbers[l]+numbers[r]
        if sum < target:
            l = l+1
        elif sum > target:
            r = r-1
        else:
            return [l+1, r+1]
    return 0

numbers = [2, 7, 11, 15]
target = 9
print(twoSum(numbers, target))