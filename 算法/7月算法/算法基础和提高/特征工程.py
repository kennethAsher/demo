import numpy as np
from sklearn import preprocessing
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

'''
数值型python处理
'''
#幅度调整到[0,1]之间
# X_train = np.array([[1,-1,2],
#                    [2,0,0],
#                     [0,1,-1]],dtype=float)
# min_max_scaler = preprocessing.MinMaxScaler()
# X_train = min_max_scaler.fit_transform(X_train)
# print(X_train)


#归一化   处理大量离散的值 使用归一化
# X_train = np.array([[1,-1,2],
#                    [2,0,0],
#                     [0,1,-1]],dtype=float)
# scaled = preprocessing.scale(X_train)   #均值为0，方差为1
# print(scaled)
# print(scaled.mean(axis=0))   #0表示按照行统计，即求每一列的数值
# print(scaled.std(axis=0))
# scaler = preprocessing.StandardScaler().fit(X_train)
# print(scaler)
# print(scaler.mean_)
# print(scaler.scale_)
# print(scaler.transform(X_train))


#离散化    处理大量连续的值，
# arr = np.random.rand(20)   #去数值，个数，  大小在0，1之间
# print(arr)
# factor = pd.cut(arr,6)     #划分为多个区间   自动划分
# print(factor)
# factor = pd.cut(arr,[-5,-1,0,1,5])   #自己指定分区
# print(factor)


#柱状分布（比例）
# data = np.random.randint(0,7, size=50)   #[0,7) 共需要50个
# print(data)
# s = pd.Series(data)   #将data转化成为dataframe
# print(s.value_counts())
# print(pd.value_counts(data))   #能够直接将data转化成dataframe

#词袋之python处理
# vectorsize = CountVectorizer(min_df=1)
# # print(vectorsize)
# corpurs = [
#     'this is the first document.',
#     'this is the second document.',
#     'this is the thred document.',
#     'is this the first document?'
# ]
# #
# x = vectorsize.fit_transform(corpurs)
# # print(x)
#
# #把词袋中的词扩充到n-gram
# bigram_vecotrizer = CountVectorizer(ngram_range=(1,2),token_pattern=r'\b\w+\b',min_df=1)
# analyze = bigram_vecotrizer.build_analyzer()    #
# # analyze('Bi-gram are cool!') == (['bi','gram','are','cool','bi gram','gram are','are cool'])
# print(analyze('Bi-gram are cool!'))   #分词
# x_2 = bigram_vecotrizer.fit_transform(corpurs).toarray()
# print(x_2)
# feature_index = bigram_vecotrizer.vocabulary_.get('is this')
# print(x_2[:,feature_index])