# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : 28.py
@ctime  : 2020/7/8 10:28
@Email  : 1131771202@qq.com
@content: 实现strStr()
"""

''':Question
给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1

输入: haystack = "hello", needle = "ll"
输出: 2

输入: haystack = "aaaaa", needle = "bba"
输出: -1
'''

#速度比较快
def strStr(haystack: str, needle: str) -> int:
    if needle in haystack:
        return haystack.index(needle)
    return -1


#采用方法---差不多
# def strStr(self, haystack: str, needle: str) -> int:
#     if not needle or len(needle) == 0:
#         return 0
#     n = len(needle)
#     i = 0
#     while i <= (len(haystack) - n):  ##等于两个字符串长度相减时，移位完毕
#         if haystack[i:i + n] == needle:  ##依次移位，判断i+n（n为第二个字符串长度）是否相等
#             return i
#         else:
#             i += 1
#     if i > (len(haystack) - n):
#         return -1



haystack = 'hello'
needle = 'll'
print(strStr(haystack, needle))