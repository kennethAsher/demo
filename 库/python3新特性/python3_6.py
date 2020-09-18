#01 格式化字符串f-string
# # old使用format
# user = 'jane doe'
# action = 'buy'
# log_message = 'User {} has logged in and did an action {}'.format(user,action)
# print(log_message)
# #new使用f-string
# log_message1 = f'User {user} has logged in and did an action {action}'
# print(log_message1)


# 02 路径管理库 Pathlib
# f-string 非常强大，但是有些像文件路径这样的字符串有他们自己的库，这些库使得对它们的操作更加容易。Python 3 提供了一种处理文件路径的抽象库「pathlib」。如果你不知道为什么应该使用 pathlib，请参阅下面这篇 Trey Hunner 编写的炒鸡棒的博文：
# https://treyhunner.com/2018/12/why-you-should-be-using-pathlib/
# from pathlib import Path
# root = Path('post_sub_folder')
# print(root)
# path = root / 'happy_user'
# print(path.resolve())


# 03类型提示 Type hinting
# 静态和动态类型是软件工程中一个热门的话题，几乎每个人 对此有自己的看法。读者应该自己决定何时应该编写何种类型，因此你至少需要知道 Python 3 是支持类型提示的。
# def sentence_has_animal(sentence: str) -> bool:
#     return 'animal' in sentence
# sentence_has_animal("Donald had a farm without animals")



# 04 枚举
# Python 3 支持通过「Enum」类编写枚举的简单方法。枚举是一种封装常量列表的便捷方法，因此这些列表不会在结构性不强的情况下随机分布在代码中。
# from Enum import Enum,auto
# class Monster(Enum):
#     ZOMBIE = auto()
#     WATTER = auto()
#     BEAR = auto()
# print(Monster.ZOMBIE)



# 05 原生 LRU 缓存
# 目前，几乎所有层面上的软件和硬件中都需要缓存。Python 3 将 LRU（最近最少使用算法）
# 缓存作为一个名为「lru_cache」的装饰器，使得对缓存的使用非常简单。
# 下面是一个简单的斐波那契函数，我们知道使用缓存将有助于该函数的计算，因为它会通过递归多次执行相同的工作。
import time
# def fib(number:int) -> int:
#     if number == 0: return 0
#     if number == 1: return 1
#     return fib(number-1)+fib(number-2)
# start = time.time()
# fib(40)
# print(start - time.time())

# from functools import lru_cache
# @lru_cache(maxsize=512)        #有助于函数计算
# def fib(number):
#     if number == 0: return 0
#     if number == 1: return 1
#     return fib(number-1)+fib(number-2)
# start = time.time()
# fib(40)
# print(time.time()-start)



# 06 扩展的可迭代对象解包
# head,*body,tail = range(5)
# print(head,body,tail)
# # 0 [1, 2, 3] 4
# py, filename, *cmds = "python3.7 script.py -n 5 -l 15".split()
# print(py, filename, cmds)
# # python3.7 script.py ['-n', '5', '-l', '15']
# first,_,thred,*_ = range(10)     #相同名称会被覆盖
# print(first,_,thred,_)