'''
属性	                说明
ndarray.ndim	    秩，即轴的数量或维度的数量
ndarray.shape	    数组的维度，对于矩阵，n 行 m 列
ndarray.size	    数组元素的总个数，相当于 .shape 中 n*m 的值
ndarray.dtype	    ndarray 对象的元素类型
ndarray.itemsize	ndarray 对象中每个元素的大小，以字节为单位
ndarray.flags	    ndarray 对象的内存信息
ndarray.real	    ndarray元素的实部
ndarray.imag	    ndarray 元素的虚部
ndarray.data	    包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。
'''
import numpy as np

#ndarray.ndim	    秩，即轴的数量或维度的数量
# a = np.arange(24)
# print(a.ndim)       # 1
# #reshape （3,4,2）  代表3个4行两列
# b = a.reshape(3,4,2)
# print(b.ndim)       # 3

# ndarray.shape	    数组的维度，对于矩阵，n 行 m 列
# a = np.array([[1,2,3],[4,5,6]])
# print (a.shape)
# #可以调整矩阵
# a = np.array([[1,2,3],[4,5,6]])
# a.shape =  (3,2)
# print (a)
# #也能用reshape 不同，前者是前者在原基础上修改，reshpae 是修改之后返回一个值
# a = np.array([[1,2,3],[4,5,6]])
# b = a.reshape(3,2)
# print (b)

# ndarray.itemsize	ndarray 对象中每个元素的大小，以字节为单位
# 数组的 dtype 为 int8（一个字节）
# x = np.array([1,2,3,4,5], dtype=np.int8)
# print(x.itemsize)
# y = np.array([1,2,3,4,5], dtype=np.int64)
# print(y.itemsize)


# ndarray.flags 返回 ndarray 对象的内存信息
x = np.array([1,2,3,4,5])   
print (x.flags)