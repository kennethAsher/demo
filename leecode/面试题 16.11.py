# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : 面试题 16.11.py
@ctime  : 2020/7/8 20:55
@Email  : 1131771202@qq.com
@content: 跳水板
"""

""":Question
你正在使用一堆木板建造跳水板。有两种类型的木板，其中长度较短的木板长度为shorter，长度较长的木板长度为longer。
你必须正好使用k块木板。编写一个方法，生成跳水板所有可能的长度.
返回的长度需要从小到大排列。

示例：
输入：
shorter = 1
longer = 2
k = 3
输出： {3,4,5,6}


"""

def divingBoard(shorter: int, longer: int, k: int):
    result = []
    if k == 0:
        return result
    if shorter == longer:
        return [shorter*k]
    for i in range(k, -1, -1):
        result.append(shorter*i + longer*(k-i))
    return result




shorter = 1
longer = 2
k = 3
print(divingBoard(shorter, longer, k))