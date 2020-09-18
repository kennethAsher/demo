import knn
from numpy import *

#生成数据集和类别标签
data_set, labels = knn.create_dataset()
#定义一个未知类别的数据
testX = array([1.2, 1.0])
k = 3
#调用分类器函数对未知数据进行分类
output_label = knn.knn_classify(testX, data_set, labels, 3)
print(output_label)