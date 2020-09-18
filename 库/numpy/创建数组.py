import numpy as np

# numpy.empty 方法用来创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组：
# numpy.empty(shape, dtype = float, order = 'C')

# 下面是一个创建空数组的实例：  元组数值为随机值，并没有初始化
# a = np.empty([3,2], dtype=float)
# print(a)

# numpy.zeros   创建指定大小的数组，数组元素以 0 来填充：
# 默认为浮点型
# x = np.zeros(5)
# print(x)
# # 设置类型为整数
# x = np.zeros((5,), dtype=np.int)
# print(x)
# # 自定义类型
# x = np.zeros((2,2), dtype=[('x', 'i4'),('y','i4')])
# print(x)

# numpy.ones    创建只都是1的数组
# x = np.ones(5)
# print(x)
# x = np.ones((5,),dtype=int)
# print(x)