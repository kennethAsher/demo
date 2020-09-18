#coding=utf-8
'''
Created on 2017年11月21日

@author: lzcs
'''
stopwords = {}.fromkeys([ line.rstrip() for line in open('../file/wordstop.txt') ]) #加载停用词

import jieba.posseg as pseg
import re

import pandas as pd
dt=pd.read_excel('../datainput/0001.xlsx',names=['type1','MSGCONT'])




def word_count_str(wset):    
    #统计词频,并返回前1000个
    word = []
    counter = {}

    for str0 in wset:
        line = str0['doc']
        if len(line) == 0:
            continue
        for w in line:
            if not w in word:
                word.append(w)
            if not w in counter:
                counter[w] = 0
            else:
                counter[w] += 1

    counter_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    counter_list=counter_list[:500]
    
    new_list=[]
    
    print('counter_list',len(counter_list))
    
    for k,v in counter_list:
        if int(v)>0:
            new_list.append(k)
                
    print('new_list',len(new_list))
    
    return new_list #只要1000个作为特征词

    
def create_load_date_xls(return_one):
    for post_str in return_one: 
        try:
            post=post_str['msgcont']
            if (len(post)>1):
                
                y=post
                y=y[0:300]
                doc = del_stop_words(y,stopwords)
                #print (doc)
            else:
                print(post)
        except Exception as e:
            #异常原因暂时未找到。（以下为导致）
            #李佳航INF、施芳芳旅客购买的10月28日13:55 HU7395 兰州(T1) 大连航班，由于公司计划调整，原航班取消，请您尽快致电95339确认新行程，很抱歉给您带来不便.祝您旅途愉快!【海南航空】++++
            #尊敬的CHENG/LINGYAN旅客，您好！这里是海南航空。我司接到阿拉斯加航空的通知，您原定12月30日AS2474 LAX-SEA航班取消，为您保护至AS455 LAX-SEA航班，预计当地时间08:05分起飞，预计11:05分到达。因航班取消，我们需为您重新出票，或我们可以提供全额退票（未使用部分），如有任何疑问，您也可拨打海南航空客服热线：国际长途热线008689895339转6号键，美国区域可拨打001-888-688-8876，或是发送邮件至bzchbcl@hnair.com。感谢您选择海南航空！【海南航空】
            print(e)
        post_str['doc']=doc
        
    
    #是否把姓氏这些去掉 ？？？？？ 后续再优化，
    return return_one
    

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

def create_type_arr(return_one):
    
    n_num=10
    y=[]
    y0=[]
    dict1={}
    
    for ii in return_one:
       
        if (len(ii['type'])>1):
            y0.append(ii['type']) 
            
    for str0 in set(y0):
        dict1[str0]=n_num
        n_num=n_num+1
    
    for str1 in  return_one:
        
        str1['typevalue']=dict1[str1['type']]
        
    
    return return_one,dict1

def create_data_tf(return_one,wordlist):
    
    for is_0 in return_one:
        is_=is_0['doc']
        temp_vector = [] 
        for word in wordlist:#遍历词表，该词表包含组成文档的所有词 
            temp_vector.append(is_.count(word) * 1.0)#计算每篇文档每个词的词频， temp_vector临时保存一篇文档的词频         
        #print(temp_vector)
        is_0['weight']=temp_vector
        
    
    return return_one

import numpy as np 
from sklearn.naive_bayes import GaussianNB  

from sklearn.cross_validation import train_test_split 
import xlwt
from sklearn.externals import joblib


if __name__ == '__main__':
    print('贝叶斯分类')
    """
    1 分词
    2 统计词频
    3 特征提取
    
    """
    #加载训练数据
    #标记类型
    return_set = dt['type1']
    #真实训练数据
    demand_set = dt['MSGCONT']
    print("训练数据加载完成")
    
    #vo_num=[]
    #vonull_num=[]
    #用来存放结构话数数据（字典类型）的对列
    return_one=[]
    
    num_k=1
    
    for (i1, i2) in zip(return_set,demand_set):
        dict_temp={}
        dict_temp['key']=str(num_k)
        dict_temp['msgcont']=i2        
        dict_temp['type']='-1' 
        return_one.append(dict_temp)  
        num_k=num_k+1

    #显示加载所有数据的队列长度。
    print(len(return_one))
    #return_one中的字典 已经多出一类为doc 用来存储切分词
    return_one = create_load_date_xls(return_one) #进行分词
    print("切分词完成")
    
   #加载数据分类类别
    f = open('../temp/word_temp.txt')
    txt = f.read()
    f.close()
    txt = txt.rstrip(',')
    wordlist = txt.split(',')
    print('特征词数量：',len(wordlist))
  
    new_dict = {}
    f = open('../temp/type_temp.txt')
    txt2 = f.read() 
    f.close()
    
    new_dict = eval(txt2)
    print(new_dict)
    #特征提取
    return_one = create_data_tf(return_one,wordlist)
    
    
    
        
    x_null=[]
    
    for vo in return_one:
        x_null.append(vo['weight'])
        
    
    
    clf = joblib.load('../temp/svm_hn.pkl') #加载模型
    y_null_hat = clf.predict(x_null)
    
   
   
    
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('result')
    row_=0
    
    for (i1, i2) in zip(return_one,y_null_hat):
        #print(i1['msgcont'],new_dict[i2])
        worksheet.write(row_, 0, str(new_dict[i2]))
        worksheet.write(row_, 1, i1['msgcont'])
        row_=row_+1
    workbook.save('../dataoutput/tt000.xls')


    