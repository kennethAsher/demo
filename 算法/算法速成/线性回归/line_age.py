#线性回归demo
from math import exp

from numpy import *


def load_data():
    data_mat = []
    lable_mat = []
    file_read = open('testSet.txt', 'r', encoding='utf-8')
    for line in file_read.readlines():
        line_arr = line.strip().split()
        data_mat.append(1.0, float(line_arr[0]), float(line_arr[1]))
        lable_mat.append(float(line_arr[2]))
    return data_mat, lable_mat

def sigmoid(x):
    return 1.0/(1+exp(x))

def grad_ascent(data_mat, class_label):
    data_mat = mat(data_mat)                       #现将实验数据集转变成numpy矩阵
    class_label = mat(class_label).transpose()     #将实验数据集类标签转变成numpy矩阵

    m,n = shape(data_mat, class_label)
    alpha = 0.001                                  #调整逼近步长系数
    max_cycles = 500                               #设置最大迭代次数为500
    weights = ones((n,1))                          #weights就是需要迭代求解的参数向量

    for k in range(max_cycles):
        h = sigmoid(data_mat*weights)              #带入样本向量求得样本y的sigmid转换值
        error = (class_label-h)                     #求差
        weights = weights + alpha*data_mat.transpose() * error   #根据差值调整参数向量
    return weights




