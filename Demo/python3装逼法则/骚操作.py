"""
@author : kennethAsher
@fole   : 骚操作.py
@ctime  : 2020/5/12 10:44
@Email  : 1131771202@qq.com
@content: 记录python的骚操作用法
"""

from collections import Counter
from operator import itemgetter


'''
#1 查找列表中出现频次最高的值

list = [1,2,2,2,3,4,5,5]
print(max(set(list), key=list.count))
##########################
cnt = Counter(list)
print(cnt.most_common())  #返回数值以及对应的数量
'''

'''
#2检查两个字符串是不是相同字母不同顺序组成
s1 = 'zhangsan'
s2 = 'sanzhang'
print(Counter(s1)==Counter(s2))
'''

#3反转字符串,列表
a = '12334555467'
print(a[::-1])
a = [1,2,3,4]
print(a[::-1])



#4转置数组
original = [['a','b'],['c','d'],['e','f']]
transposed = zip(*original)
print(list(transposed))



#5 链式比较
b = 6
print(4<b<7)  #true
print(1==b<20) #false



#6 链式函数调用
def product(a,b):
    return a*b
def add(a,b):
    return a+b
b = True
print((product if b else add)(5,7))


#7通过键给排序自断元素
d = {'apple':10, 'orange':20, 'banana':5, 'rotten tomato':1}
print((sorted(d.items(), key = lambda x:x[1])))
print(sorted(d.items(), key=itemgetter(1)))
print(sorted(d, key=d.get))  #只展示名称


#8 for else
for i in a:
    if i == 0:
        break
else:
    print('完蛋')


#9 合并字典
d1 = {'a':1, 'b':2, 'c':3}
d2 = {'c':4, 'd':5}
print({**d1, **d2})
print(dict(d1.items()|d2.items()))
d1.update(d2)
print(d1)


#10合并字典，数值相加
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key,0) for obj in objs])
    return _total

print(union_dict(d1,d2))