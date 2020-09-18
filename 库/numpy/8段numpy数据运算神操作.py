''''''
#      1.numpy的array基本操作
'''
# 引入numpy库，并将其别名为np
import numpy as np
# 通过np.array()方法创建一个名为array的array类型，参数是一个list
array = np.array([1,2,3,4])
# 获取该array类型中最大的元素值，结果为:
print(array.max())
# 求该array中元素的平均值，结果为:
print(array.mean())
# 获取该array中元素的最小值：
print(array.min())
# 直接将该array乘以2，Python将该运算符重载，将每一个元素都乘以了2，
print(array*2)
# 将每一个元素都加上1，
print(array+1)
# 将每一个元素都除以2
print(array/2)
# Numpy库除了可以对array实现除法运算，还可以实现取模运算，
print(array%2)
# 获取该组数据中元素值最大的一个数据的索引，下标从0开始
print(array.argmax())
'''

#   2. Numpy对更高维度数据的处理
'''
import numpy as np
# 创建一个二维数组，用以表示一个3行2列的矩阵，名为array
array = np.array([[1,2],[3,4],[5,6]])
print(array)
# 查看数据的维度属性，下面的输出结果元组，代表的是3行2列
print(array.shape)
# 查看array中的元素数量，输出结果为：
print(array.size)
# 查看元素值最大的元素索引，结果为
print(array.argmax())
# 将shape为(3,2)的array转换为一行表示，
print(array.flatten())
# 将array数据从shape为(3,2)的形式转换为(2,3)的形式：
print(array.reshape(2,3))
'''

#  3. Numpy创建特殊类别的array类型
'''
import numpy as np
# 生成所有元素都为0的array，其shape是(2,3,3)
array = np.zeros((2,3,3))
# 生成所有元素都为1的array，其shape是(2,3,3)
array = np.ones((2,3,3))
# 生成一个array，从10递增到100，步长为5，结果为：包括左边不包括右边
print(np.arange(10,100,5))
# 生成一个array，从0递增到10，步长为1，结果为：
print(np.arange(10))
# 生成一个array从0到10递增，分成5个点，
array_linespace = np.linspace(0,10,5)
print(array_linespace)
'''

#   4. Numpy基础计算演示
'''
import numpy as np
# 取绝对值
print(np.abs([1,-2,-3,4]))
# 求余弦值
print(np.sin(np.pi / 2))
# 求反正切值
print(np.arctan(1))
# 求自然常数e的2次方
print(np.exp(2))
# 求2的3次方
print(np.power(2,3))
# 将向量[1,2]与[3,4]求点积，矩阵的积
print(np.dot([1,2],[3,4]))
# 将4开平方，
print(np.sqrt(4))
# 求标准差
print(np.std([1,2,3,4]))
'''

#   5. Numpy提供的线性代数操作
'''
import numpy as np
vector_a = np.array([1,2,3])
vector_b = np.array([2,3,4])
# 将两个向量相乘，在这里也就是点乘
print(vector_a.dot(vector_b))
# print(np.dot(vector_a, vector_b))
# 定义一个2行2列的方阵
matrix_a = np.array([[1,2],[3,4]])
# 这里将该方阵与其转置叉乘，将结果赋予matrix_b变量
matrix_b = np.dot(matrix_a,matrix_a.T)
print(matrix_b)
# 求一个向量的范数的值，如果norm()方法没有指定第二个参数，则默认为求2范数
print(np.linalg.norm([1,2]))
print(np.linalg.norm([1,2], 1))
# 求向量的无穷范数，其中np.inf表示正无穷，也就是向量中元素值最大的那个,同理，求负无穷范数的结果为1，也就是向量中元素的最小值
print(np.linalg.norm([1,2,3,4], np.inf))
print(np.linalg.norm([1,2,3,4], -np.inf))
# 除了向量可以求范数，矩阵也可以有类似的运算，即为F范数，
print(np.linalg.norm(matrix_b))
print(np.linalg.norm(matrix_a))
# 求矩阵matrix_a的迹
print(np.trace(matrix_b))
# 求矩阵的秩，
print(np.linalg.matrix_rank(matrix_b))
# 使用*符号将两个向量相乘，是将两个向量中的元素分别相乘，也就是前面我们所讲到的哈达马乘积，
print(vector_a*vector_b)
# 使用二元运算符**对两个向量进行操作
print(vector_a**vector_b)
# 求矩阵的逆矩阵，方法pinv()求的是伪逆矩阵，结果为：
# array([[-2. ,  1. ],
#        [ 1.5, -0.5]])
# 不使用伪逆矩阵的算法，直接使用逆矩阵的方法是inv()，即
# np.linalg.inv(matrix_a)
# 结果相同，也为：
# array([[-2. ,  1. ],
#        [ 1.5, -0.5]])
print(np.linalg.pinv(matrix_b))
'''

#SVD算法
'''
import numpy as np
matrix = np.array([
    [1,2],
    [3,4]])
#生成一个矩阵another_matrix
another_matrix = np.dot(matrix, matrix.T)
#该矩阵为：array([[ 5, 11],[11, 25]])
print(another_matrix)
# 使用奇异值分解法将该矩阵进行分解，分解得到三个子矩阵U,s,V
U,s,V = np.linalg.svd(another_matrix)
# print(U)
# s向量表示的是分解后的∑矩阵中对角线上的元素
# print(s)
# print(V)
# 在s矩阵的基础上，生成S矩阵为
S = np.array([[s[0],0],[0,s[1]]])
# print(S)
a = U.dot(S).dot(V)
print(a)
'''

#  基于svd实现pca算法
'''
import numpy as np
# 零均值化，即中心化，是数据的预处理方法，axis0代表列 1代表行
def zero_centered(data):
    matrix_mean = np.mean(data, axis=0)
    return data - matrix_mean
def pca_eig(data, n):
    new_data = zero_centered(data)
    cov_mat = np.dot(new_data.T,new_data)
    # 求特征值和特征向量,特征向量是列向量
    eig_values, eig_vectors = np.linalg.eig(np.mat(cov_mat))
    # 将特征值从小到大排序
    value_indices = np.argsort(eig_values)
    # 最大的n个特征值对应的特征向量
    n_vectors = eig_vectors[:, value_indices[-1:-(n+1):-1]]
    # 返回低维特征空间的数据
    return new_data * n_vectors
def pca_svd(data, n):
    new_data = zero_centered(data)
    cov_mat = np.dot(new_data.T, new_data)
    # 将协方差矩阵奇异值分解
    U,s,V = np.linalg.svd(cov_mat)
    # 返回矩阵的第一个列向量即是降维后的结果
    pc = np.dot(new_data, U)
    return pc[:,0]
def unit_test():
    data=np.array(
        [[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0], [2.3, 2.7], [2, 1.6], [1, 1.1], [1.5, 1.6],
         [1.1, 0.9]])
    # 使用常规的特征值分解法，将2维数据降到1维
    result_eig = pca_eig(data, 1)
    print(result_eig)
    # 使用奇异值分解法将协方差矩阵分解，得到降维结果
    result_svd = pca_svd(data, 1)
    print(result_svd)
if __name__ == '__main__':
    unit_test()
'''

#8. Numpy的随机数功能演示
import numpy as np
#设置随机数种子
np.random.seed()
# 从[1,3)中生成一个整数的随机数，连续生成10个
a = np.random.randint(1,3,10)
# 若要连续产生[1,3)之间的浮点数，可以使用下述方法：
b = 2*np.random.random(10) + 1
b = np.random.uniform(1,3,10)
# 生成一个满足正太分布(高斯分布)的矩阵，其维度是4*4
np.random.normal(size=(4,4))
# 随机产生10个，n=5,p=0.5的二项分布数据:
np.random.binomial(n=5,p=0.5,size=10)
# 产生一个0到9的序列
data = np.arange(10)
# 从data数据中随机采集5个样本，采集过程是有放回的
np.random.choice(data, 5)
# 对data进行乱序，返回乱序结果
np.random.permutation(data)
# 对data进行乱序，并替换为新的data
np.random.shuffle(data)