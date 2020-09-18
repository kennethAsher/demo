# coding=utf-8
'''

Created on 2017-11-13

@author: lzcs
'''
import jieba 
import os 
import pandas as pd 
import numpy as np 
import re
import numpy as np
import jieba.posseg as psg
import operator
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.cross_validation import train_test_split


from sklearn.externals import joblib
dt =pd.read_excel('../datainput/001.xlsx',names=['type1','MSGCONT'])
stopwords = {}.fromkeys([ line.rstrip() for line in open('../file/wordstop.txt') ]) #加载停用词

import jieba.posseg as pseg

def del_stop_words(words,stop_words):#定义一个将分词结果过滤掉停用词的函数 
    words = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", ",", words)
    words=words.strip()
    words_ =pseg.cut(words)
    result=[]
    for w in words_:
        #print(w)
        if (w.flag=='v'):   result.append(w.word)
        if (w.flag=='n'):   result.append(w.word)

    #result=jieba.cut(words, cut_all=False)#分词 
    new_words = [] 
    for i in result:#对分词结果进行遍历 
        if i not in stop_words:#如果词语不在停用词表，是我们需要的词 
            s_word=i.strip()
            if(len(s_word)>1):
                new_words.append(i)#将保留下来的词追加到一个新的list中 
    return new_words


def create_load_date():
    corpus = [] 
    corpus_y = [] 
    word_set = set() 
    for post in open(u'E:/自然语言处理/document/11.txt', 'r').readlines(): 
        try:

            if (post.find("|")):
                x,y= post.split("|",1) # split(数据，分割位置，轴=1（水平分割） or 0（垂直分割）)。 x 为属性字典  y 对应的类别的集合
            
                doc = del_stop_words(y,stopwords)
                corpus.append(doc)
                corpus_y.append(x)
                word_set= word_set.union(set(doc))
            else:
                print(post) 
        except Exception as e:
            print(e)
        

        
    #是否把姓氏这些去掉 ？？？？？ 后续再优化
    return corpus,corpus_y,word_set


def create_load_date_xls(return_one):
    
    
    # dict_temp['key']=str(num_k)
    # dict_temp['msgcont']=i2
      
    word_set = set()    
    for post_str in return_one: 
        try:
            post=post_str['msgcont']
            if (len(post)>1):
                y=post
                y=y[0:100]
                doc = del_stop_words(y,stopwords)
                word_set= word_set.union(set(doc))
            else:
                print(post) 
        except Exception as e:
            print(e)
        post_str['doc']=doc
    
    #是否把姓氏这些去掉 ？？？？？ 后续再优化
    return return_one,word_set

def create_data_tfidf(x):
    
    corpus=[]
    
    for is_0 in x:
        is_=is_0['doc']
        str_=""
        for i_is in is_:
            str_=str_+" "+i_is
        
        corpus.append(str_)
    
    vectorizer = CountVectorizer()#将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频 
    transformer = TfidfTransformer() #该类会统计每个词语的tf-idf权值 
    
    vs=vectorizer.fit_transform(corpus)
    tfidf = transformer.fit_transform(vs)#第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵 
    word = vectorizer.get_feature_names() #获取词袋模型中的所有词语 
    #print(word)
    weight = tfidf.toarray() #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重 
    print(weight)
    
    for (vo, i2) in zip(x,weight):
        vo['weight']=i2
    
    
    return x,word

def create_type_arr(return_one):
    n_num = 10
    y = []
    y0 = []
    dict1 = {}
    for ii in return_one:
        if (len(ii['type'])>1):
            y0.append(ii['type'])
    for str0 in set(y0):
        dict1[str0] = n_num
        n_num = n_num + 1
    for str1 in  return_one:
        str1['typevalue'] = dict1[str1['type']]
    return return_one, dict1
    
from numpy import NaN
import xlwt

if __name__ == '__main__':
    return_set = dt['type1']
    demand_set = dt['MSGCONT']
    return_one = []
    num_k=1

    for (i1, i2) in zip(return_set,demand_set):
        dict_temp = {}
        dict_temp['key']=str(num_k) #信息编号
        dict_temp['msgcont']=i2    #信息内容
        if(isinstance(i1, float)):   #信息是否有标记
            dict_temp['type']='-1'
        else:
            dict_temp['type']=i1
        return_one.append(dict_temp)  
        num_k=num_k+1

    print(len(return_one))

    #1 加载文件 进行逐行读入，然后分词 只保留动词和名称
    #2 调用sklearn tfidf方法
    #3 用SVM训练模型 测试
    print('----1'*5)

    return_one,c0=create_load_date_xls(return_one)  #返回原数据和是数据产生的特征词。
    print('特征词数量：',len(c0))

    y=[]
    return_one,dict_=create_type_arr(return_one)
    print('类别定义：',dict_)
    print('----2'*5)

    return_one,turn_one, c0 = create_data_tfidf(return_one)

    #将提取出的关键子。写入到txt 文件中
    filename='word_temp.txt'
    f=open(filename,"w+")
    for obj in c0:
        f.write(obj+",")
    f.close()
    

    #把return_one 把没有定义的数据输出到另外的LIST中
    
    x=[]
    y=[]
    x_null=[]
    nolable=[]
    vo_num=[]
    vonull_num=[]

    for vo  in return_one:
        if (vo['type']=='-1'):
            x_null.append(vo['weight'])
            vonull_num.append(vo)
        else:
            x.append(vo['weight'])
            y.append(vo['typevalue'])
            vo_num.append(vo)
    print('----5'*5)

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
    print('x_train',len(x_train),'y_train',len(y_train))
    print('x_test',len(x_test),'y_test',len(y_test))
    print('x_null',len(x_null))
    
    
    
    #3 训练svm分类器
    clf = svm.SVC(C=0.7, kernel='linear', gamma=20, decision_function_shape='ovo') #根据结果准确度 改变 内涵函数
    print('----6'*5)
    clf.fit(x_train, y_train)

    print ('训练精度',clf.score(x_train, y_train))  # 精度
    print ('测试精度',clf.score(x_test, y_test))

    y_null_hat = clf.predict(x_null)
    new_dict = {v:k for k,v in dict_.items()}
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('result')
    row_=0
    for (i1, i2) in zip(vonull_num,y_null_hat):
        #print(i1['msgcont'],new_dict[i2])
        worksheet.write(row_, 0, str(new_dict[i2]))
        worksheet.write(row_, 1, i1['msgcont'])
        row_=row_+1
    workbook.save('tt0.xls')
    #show_accuracy(y_hat, y_test, '测试集') 
    #clf = joblib.load('filename.pkl') 
    #joblib.dump(clf, 'svm_hn.pkl') 
    
    
      

        
        