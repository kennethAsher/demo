#Scikit-Learn是基于python的机器学习模块，基于BSD开源许可证。
#scikit-learn的基本功能主要被分为六个部分数据降维，模型选择，数据预处理。包括SVM，决策树，GBDT，KNN，KMEANS，分类，回归，聚类，等等
#Kmeans在scikit包中即已有实现，只要将数据按照算法要求处理好，传入相应参数，即可直接调用其kmeans函数进行聚类

from numpy import *
import time
import matplotlib.pyplot as plt
import kmeans

##step1:加载数据
print('step1: load data')
data_set = []
fileln = open('testSet.txt', 'r', encoding='utf-8')
for line in fileln.readlines():
    lineArr = line.strip().split('\t')
    data_set.append([float(lineArr[0]), float(lineArr[1])])

##step2:聚类
print("step2: clustering...")
k=4
centroids, cluster_assment = kmeans.kmeans(data_set, k)

##step3：显示结果
print('step3:show the result')
showCluster(data_set, k, centroids, cluster_assment)
