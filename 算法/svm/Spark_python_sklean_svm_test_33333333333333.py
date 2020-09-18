#coding=utf-8
from sklearn import svm, grid_search, datasets
from spark_sklearn import GridSearchCV
from pyspark import SparkContext, SparkConf
import jieba 
import os 
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer 
#import pandas as pd 
import numpy as np 
import re
import jieba.posseg as psg
from sklearn.cross_validation import train_test_split
from gc import collect
import sys
stopwords = {}.fromkeys([ line.rstrip() for line in open('../file/wordstop.txt') ]) #加载停用词

#def del_stop_words(words,stop_words):#定义一个将分词结果过滤掉停用词的函数 
def del_stop_words(words,stop_words):#定义一个将分词结果过滤掉停用词的函数 
    words = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", ",", words)
    words=words.strip()
    jieba.add_word("航班取消", freq = 20000, tag = None)
    jieba.add_word("航班延误", freq = 20000, tag = None)
    jieba.add_word("航班信息", freq = 20000, tag = None)
    jieba.add_word("大床房", freq = 20000, tag = None)
    jieba.add_word("金鹏", freq = 20000, tag = None)
    jieba.add_word("已出票", freq = 20000, tag = None)
    result=jieba.cut(words, cut_all=False)#分词 
    new_words = [] 
    for i in result:#对分词结果进行遍历 
        if i not in stop_words:#如果词语不在停用词表，是我们需要的词 
            if(len(i.strip())>1):
                new_words.append(i.strip())#将保留下来的词追加到一个新的list中 
    return new_words
            

def create_load_date():
    corpus = [] 
    corpus_y = [] 
    word_set = set() 
    
    for post in open(u'../datainput/ceshisuanfa2.txt', 'r').readlines():
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
    return corpus,corpus_y,word_set   #字段，标签，总字段
'''
def get_label_id(label_id):
    
    
    
    label_id = {}
    
    for line in label_id:
        if line is not None:
            s=line.split('|') 
            key = s[0]
            value = s[1] 
            value_new = value.split('\n')[0]             # 后面跟 ',' 将忽略换行符 
            label_id[key]=int(value_new)
    return label_id
'''

def get_label_id():
    label_id = {}
    filename = '../datainput/shanhang.txt'
    f=open(filename,encoding="gbk")
    line = f.readline()             # 调用文件的 readline()方法 
    while line: 
        if line is not None:
            s=line.split('|') 
            key = s[0]
            value = s[1] 
            value_new = value.split('\n')[0]             # 后面跟 ',' 将忽略换行符 
            label_id[key]=int(value_new)
        line = f.readline() 
        
    f.close()  
    return label_id
def create_data_tfidf(x,c):#字段,总字段
    docs=x#字段
    word_set=c#总字段
   
    docs_vsm = [] 

    """
    以下这两个循环的主要作用是计算每一篇文档的词频，
    并把所有文档的词频全部放在doc_vsm中，
    doc_vsm转换成矩阵docs_matrix，
    这就是一个词频矩阵，每行是一篇文档，列是相应文档里的词，
    矩阵的某个数值表示该词在某篇文档的频数。 
    """

    for i in range(len(docs)):#字段
        #我的实验数据一共13篇文档，所以遍历13次，或许有同学会问为什么不是for doc in docs，我参考的博客资料确实这么写，但是我运行测试以后发现有问题，就是最后有一个函数是计算矩阵docs_matrix每一行的和，出现为0的情况，这显然不对，不可能一篇文档的词总数为0，当我写成for i in range(13):的时候，就没有这种问题，13这个数字可以根据您测试的文档数进行更换。 
        temp_vector = [] 
        for word in word_set:#遍历词表，该词表包含组成文档的所有词   #总字段
                            #字段                
            temp_vector.append(docs[i].count(word) * 1.0)#计算每篇文档每个词的词频， temp_vector临时保存一篇文档的词频 
            #count() 方法用于统计字符串里某个字符出现的次数。
        docs_vsm.append(temp_vector)#将每篇文档的词频依次追加到docs_vsm数据表中 
   
    
    docs_matrix = np.mat(docs_vsm) #创建矩阵
    
    
    column_sum = [ float(len(np.nonzero(docs_matrix[:,i])[0])) for i in range(docs_matrix.shape[1]) ]#计算包含该词的文档数 
    
    
    column_sum = np.array(column_sum)#转换为数组，因为数组可以方便后面的批量除法计算 
    column_sum = docs_matrix.shape[0] / column_sum#用文档总数除以包含某个词的文档总数（根据idf的概念） 
    
    idf = np.log(column_sum)#取对数 
    idf = np.diag(idf)#将数组转换为n*n的对角矩阵 
    
    #以下这个循环主要是根据前面的词频矩阵docs_matrix计算tf值，tf值是词频除以该篇文档的总词数。 
    for doc_v in docs_matrix:
        if doc_v.sum() == 0:
            doc_v = doc_v / 1 
        else: 
            doc_v = doc_v / (doc_v.sum()) 
            
    tfidf = np.dot(docs_matrix,idf)#tf*idf    np.dot 相乘
    
    #print(tfidf,len(tfidf))
    
    #tfidf就是一个词袋了 
    return tfidf

if __name__ == '__main__':
    
    '''
    reload(sys)
    sys.setdefaultencoding('utf-8')
    '''
    conf = SparkConf().setAppName('test').setMaster('local[4]')
    sc = SparkContext(conf=conf)
    
    
    fileRDD = sc.textFile('../datainput/ceshisuanfa2.txt')#'G://test/ceshisuanfa1.txt'     hdfs://lczs02:8020/input/suanfa.log
    label_idRDD = sc.textFile('../datainput/shanhang.txt')  #hdfs://lczs02:8020/input/label_id.log    'G://test/山航标签及编号1.txt'
    
    coll = fileRDD.collect()
    #datasets.load_digits()
    
    label_id = label_idRDD.collect()
    
    
    x0,y0,c0=create_load_date()#字段，标签，总字段
    
    '''
    words=[]
    for x in x0:
        word_new = ''
        for xz in x:
            word_new = word_new + ' ' + xz
        word_new = word_new.strip
        words.append(word_new)
    
    
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(words))  
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
    '''
    
    x=create_data_tfidf(x0,c0)#字段,总字段  return tfidf的向量
    
    
    
    
    
    #加载标签并定义标签编号
    label_id = get_label_id()
    y=[]
    for str0 in y0:
        try:
            id=label_id[str0]
            if id is not None:
                y.append(id)
            else:
                y.append(-1)
        except Exception as e:
            y.append(-1)
        
        
        
    
    
    
    
    print('==============111111111===============')
    #iris = datasets.load_iris(x0)
    #X = iris.data
    #y = iris.target

    #print(X)
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
    print('x_train',len(x_train),' y_train',len(y_train))
    print('x_test',len(x_test),' y_test',len(y_test))
    
    
    parameters = {'kernel':('linear', 'rbf'), 'C':[1,10]} 
    parameters = {'kernel':('linear', 'rbf'), 'C':[1,10],'gamma':[1],'decision_function_shape':['ovo','ovr']}
    #
    print('==============22222222222===============')
    svr = svm.SVC()
    #clf = svm.SVC(C=0.7, kernel='linear', gamma=20, decision_function_shape='ovo')
    print('==============333333333===============')
    clf = GridSearchCV(sc, svr, parameters)
    #GridSearchCV:根据选定的算法（本例是svm），用于系统地遍历多种参数组合，通过交叉验证确定最佳效果参数。
    #根据在parameters中的kernel（kernel有'linear', 'rbf'两种）和C（c中有[1,2,3,4,5,6,7,8,9,10]，可增可减）多个参数
    #根据以上的多个选择，GridSearchCV会自动运行各种组合并算出分数，能直观地看出一个最优的组合，确定一组最优参数
    xx=[]
    yy=[]
    flag_xy = 0
    for x_t in x_train:
        if np.isnan(x_t).any() or len(x_t) <= 1:
            pass
        else:
            y_t=y_train[flag_xy]
            xx.append(x_t)
            yy.append(y_t)
        
        flag_xy = flag_xy+1    
     
    #clf.fit(xx, yy)   
    clf.fit(x_train, y_train)
    print('==============4444444444===============')
    #clf.fit(x, y)
    print('==============5555555555===============')

    
    
    
    y_hat = clf.predict(x_test)
    
    
    
    flag = 0;
    flag_count = 0
    for x1 in y_test:
        s11 = y_hat[flag]
        #print(x1)
        print(s11)
        print('==========')
        if s11 == x1:
            flag_count=flag_count+1
        flag=flag+1
    print('准确率：',str(flag_count/len(x_test)))
    
    
    
    
    
    
    '''
    cv_result = pd.DataFrame.from_dict(clf.cv_results_)
    with open('cv_result.csv','w+') as f:
        cv_result.to_csv(f)
    
    
    print('The parameters of the best model are: ')
    print(clf.best_params_)
    '''
    
    

