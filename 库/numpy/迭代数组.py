import numpy as np
# NumPy 迭代器对象 numpy.nditer 提供了一种灵活访问一个或者多个数组元素的方式。
# 迭代器最基本的任务的可以完成对数组元素的访问。
# 接下来我们使用 arange() 函数创建一个 2X3 数组，并使用 nditer 对它进行迭代。
# a = np.arange(6).reshape(2,3)
# print ('原始数组是：')
# print (a)
# print ('\n')
# print ('迭代输出元素：')
# for x in np.nditer(a):
#     print(x, end=",")

# 以上实例不是使用标准 C 或者 Fortran 顺序，选择的顺序是和数组内存布局一致的，
# 这样做是为了提升访问的效率，默认是行序优先（row-major order，或者说是 C-order）。
# 这反映了默认情况下只需访问每个元素，而无需考虑其特定顺序。
# 我们可以通过迭代上述数组的转置来看到这一点，并与以 C 顺序访问数组转置的 copy 方式做对比，如下实例：
# 默认按照数组排序
# a = np.arange(6).reshape((3,2))
# for x in np.nditer(a.T):
#     print(x,end=',')
# print()
# for x in np.nditer(a.T.copy(order='C')):
#     print(x, end=',')
#

# for x in np.nditer(a, order='F'):Fortran order，即是列序优先
# for x in np.nditer(a, order='C'):表示行序优先
# a = np.arange(0,60,5)
# a = a.reshape((3,4))
# print('原始数组：')
# print(a)
# print('原始数组的专职')
# print(a.T)
# print('以F方式排序')
# for x in np.nditer(a.T.copy(order='F')):
#     print(x, end=',')
# print('以C方式排序')
# for x in np.nditer(a.T.copy(order='C')):
#     print(x, end=',')
# print()
# for x in np.nditer(a):
#     print(x, end=',')

# nditer 对象有另一个可选参数 op_flags。 默认情况下，nditer 将视待迭代遍历的数组为只读对象（read-only），为了在遍历数组的同时，实现对数组元素值得修改，必须指定 read-write 或者 write-only 的模式。
# a = np.arange(0,60,5)
# a = a.reshape(3,4)
# print('原始数组')
# print(a)
# print()
# for x in np.nditer(a, op_flags=['readwrite']):
#     x[...]=2*x   #代表全部的值
# print("修改后的数组是")
# print(a)

# nditer类的构造器拥有flags参数，它可以接受下列值：
# 参数	            描述
# c_index	        可以跟踪 C 顺序的索引
# f_index	        可以跟踪 Fortran 顺序的索引
# multi-index	    每次迭代可以跟踪一种索引类型
# external_loop	    给出的值是具有多个值的一维数组，而不是零维数组  及原本的是改成一个数组，在这里改成多个数组
# a = np.arange(0,60,5)
# a = a.reshape(3,4)
# print('primary data')
# print(a)
# print('fixd data')
# for x in np.nditer(a, flags=['external_loop'], order='F'):
#     print(x, end=',')

# 如果两个数组是可广播的，nditer 组合对象能够同时迭代它们。 假设数组 a 的维度为 3X4，数组 b 的维度为 1X4 ，则使用以下迭代器（数组 b 被广播到 a 的大小）。
a = np.arange(0,60,5)
a = a.reshape(3,4)
print('first data')
print(a)
b = np.array([1,2,3,4], dtype=int)
print('second data')
print(b)
print('the fixd data')
for x,y in np.nditer([a,b]):
    print('%d:%d' %(y,x), end=',')