# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author : kennethAsher
@fole   : KMP算法.py
@ctime  : 2020/7/8 10:05
@Email  : 1131771202@qq.com
@content: 内容在  https://leetcode-cn.com/explore/learn/card/array-and-string/200/introduction-to-string/1429/
"""

# 计算next数组
def compute_prefix(p):
    m = len(p)
    res = [-1 for _ in range(m)]
    res[0] = -1
    k = -1
    for q in range(1, m):
        while k > -1 and p[k+1] != p[q]:
            k = res[k]
        if p[k+1] == p[q]:
            k = k+1
        res[q] = k
    return res

#KMP匹配过程
def kmp_matcher(t, p):
    n, m = len(t), len(p)
    nxt = compute_prefix(p)  # 得到next数组
    q = -1
    for i in range(n):
        # 若失位的操作
        while q > -1  and p[q+1] != t[i]:
            q = nxt[q]
        # 从失位恢复处或p最左端继续匹配
        if p[q+1] == t[i]:
            q = q+1
        # 当p字符串的下标q达到m-1时,意味着匹配成功,找到一个目标pattern
        if q == (m-1):
            # 输出pattern起始位置
            print("Pattern occurs with shift", i-m+1)
            # 继续在t中寻找下一个pattern
            q = nxt[q]

#测试
p = "ababababca"
# t中藏了两个ababababca
t = "vhjvgdhacvjchacvajcbcababababcahvcdakcacbcbajhcacvacgacahcjachascababababca"
kmp_matcher(t,p)