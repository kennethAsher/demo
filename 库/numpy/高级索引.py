import numpy as np

# 整数数组索引：以下实例获取数组中(0,0)，(1,1)和(2,0)位置处的元素。
# x = np.array([[1,  2],  [3,  4],  [5,  6]])
# y = x[[0,1,2],  [0,1,0]]
# print(y)

# 以下实例获取了 4X3 数组中的四个角的元素。 行索引是 [0,0] 和 [3,3]，而列索引是 [0,2] 和 [0,2]。
# x = np.array([[  0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])
# print ('我们的数组是：' )
# print (x)
# print ('\n')
# rows = np.array([[0,0],[3,3]])
# cols = np.array([[0,2],[0,2]])
# y = x[rows,cols]
# print  ('这个数组的四个角元素是：')
# print (y)

# 返回的结果是包含每个角元素的 ndarray 对象。可以借助切片 : 或 … 与索引数组组合。如下面例子：
# a = np.array([[1,2,3], [4,5,6],[7,8,9]])
# b = a[1:3, 1:3]
# c = a[1:3,[1,2]]
# d = a[:,1:]
# print(b)
# print(c)
# print(d)

# 布尔索引
# 我们可以通过一个布尔数组来索引目标数组
# 布尔索引通过布尔运算（如：比较运算符）来获取符合指定条件的元素的数组。
# 以下实例获取大于 5 的元素：
# x = np.array([[  0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])
# print ('我们的数组是：')
# print (x)
# print ('\n')
# # 现在我们会打印出大于 5 的元素
# print  ('大于 5 的元素是：')
# print(x[x>5])   #自动将多维度数组降低维度，然后筛选

# 以下实例使用了 ~（取补运算符）来过滤 NaN
# a = np.array([np.nan,  1,2,np.nan,3,4,5])
# print (a[~np.isnan(a)])

# 以下实例演示如何从数组中过滤掉非复数元素    iscomplex判断是否是复数
# a = np.array([1,  2+6j,  5,  3.5+5j])
# print(a[np.iscomplex(a)])

# 花式索引指的是利用整数数组进行索引。
# 花式索引根据索引数组的值作为目标数组的某个轴的下标来取值。对于使用一维整型数组作为索引，如果目标是一维数组，那么索引的结果就是对
# 应位置的元素；如果目标是二维数组，那么就是对应下标的行
# 花式索引跟切片不一样，它总是将数据复制到新数组中。
# 1、传入顺序索引数组(输入的行数)
# x = np.arange(32).reshape((8,4))
# # print(x)
# print(x[[2,5,1,3]])
# 2、传入倒序索引数组
# x=np.arange(32).reshape((8,4))
# print (x[[-4,-2,-1,-7]])
# 3、传入多个索引数组（要使用np.ix_）
# x=np.arange(32).reshape((8,4))
# print(x)
# print(x[np.ix_([1,5,7,2],[0,3,1,2])])  #前者为所取得行数，后者为索取的每个数值重新排列