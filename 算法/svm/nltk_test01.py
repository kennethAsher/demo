#coding=utf-8

import jieba.posseg as pseg
import re
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import xlwt
from sklearn.externals import joblib



#fromkeys:设置字典的所有key，默认的value是None
stop_words = {}.fromkeys([line.strip() for line in open('stop_words.txt',encoding='utf8')])   #loading stop words
# print(stop_words)

dt = pd.read_excel('../datainput/001.xlsx',names=['type','MSGCONT'])   #重命名列名
# print(dt)

def create_type_arr(return_one):
    n_num = 10
    y = []
    y0 = []
    dict1 = {}
    for ii in return_one:
        #将所有类型写到一个队列中
        if (len(ii['type'])>1):
            y0.append(ii['type'])
    #   python的set和其他语言类似, 是一个无序不重复元素集, 基本功能包括关系测试和消除重复元素.
    #    集合对象还支持union(联合), intersection(交), difference(差)和sysmmetric difference(对称差集)等数学运算.
    #   sets 支持 x in set, len(set),和 for x in set。作为一个无序的集合，sets不记录元素位置或者插入点。因此，
    #   sets不支持 indexing, slicing, 或其它类序列（sequence-like）的操作。

    #set 用来消除原数据中重复的 标签，使得标记值唯一。标签数据标记重10开始，用字典形式进行保存
    for str0 in set(y0):
        #标记其唯一id
        dict1[str0] = n_num
        n_num = n_num + 1
    for str1 in return_one:
        #将原有的数据字典加入到标签id的编号。名称为typevalue
        str1['typevalue'] = dict1[str1['type']]
    return return_one, dict1


def del_stop_words(words, stop_words):  #定义一个将分词结果过滤掉停用词的函数
    #正则表达式去掉无用的字符
    words = re.sub('[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]','',words)
    words = words.strip()
    words = pseg.cut(words)   #切分之后又字符，又行词   跑\v   s.word\s.flag(来调用此类词语)(词，词性)
    result = []
    for w in words:
        # print(w)
        if (w.flag == 'v'): result.append(w.word)
        if (w.flag == 'n'): result.append(w.word)
    # result=jieba.cut(words, cut_all=False)#分词
    new_words = []
    for i in result:
        if i not in stop_words:
            s_words = i.strip()
            if len(s_words) > 1:
                new_words.append(i)
    return(new_words)


def create_load_date_xls(return_one):
    for post_str in return_one:
        try:
            post = post_str['msgcont']
            if len(post) > 1:
                y = post[:300]
                doc = del_stop_words(y,stop_words)
            else:
                print(post)
        except Exception as e:
            print(e)
        post_str['doc'] = doc
    # 是否把姓氏这些去掉 ？？？？？ 后续再优化
    return return_one

def word_count_str(wset):
    # 统计词频,并返回前1000个
    word = []
    counter = {}
    for str0 in wset:
        line = str0['doc']
        if len(line) == 0:
            continue
        for w in line:
            if not w in word:
                word.append(w)
            if w not in counter:
                counter[w] = 0
            else:
                counter[w] += 1
    # 采用sorted进行排序，默认升序。
    # 但是sorted对元组（K - V）类型的需要做借助隐函数lambda
    # 其中x是随意拼写的
    # 代表输出。x[1]
    # 代表要排序的位置。
    counter_list = sorted(counter.items(),key=lambda x:x[1], reverse=True)
    #设置要出的关键词的个数
    counter_list = counter_list[:500]
    print('counter_list', len(counter_list))

    new_list = []
    for k,v in counter_list:
        if int(v) > 0:
            new_list.append(k)
    print('new_list', len(new_list))
    return new_list #只要1000个作为特征词

def create_data_tf(return_one,wordlist):
    for is_0 in return_one:
        is_ = is_0['doc']
        temp_vector = []
        # 遍历词表，该词表包含组成文档的所有词
        for word in wordlist:
        # 计算每篇文档每个词的词频， temp_vector临时保存一篇文档的词频
            temp_vector.append(is_.count(word)*1.0)
        is_0['weight'] = temp_vector
    return return_one

if __name__ == '__main__':
    print('贝叶斯分类器')
    """
    1 分词
    2 统计词频
    3 特征提取
    """
    #加载训练数据；
    return_set = dt['type']
    # print(type(return_set))     #类型是<class 'pandas.core.series.Series'>
    demand_set = dt['MSGCONT']
    # print(demand_set)
    print("训练数据加载完成")
    # 用来存储结构原数据结构后的数据（字典类型）
    return_one = []
    num_k = 1
    # print(zip(return_set,demand_set))   #<zip object at 0x000000000B9D6E48>
    # 打包成为元组
    for (i1,i2) in zip(return_set,demand_set):
        # print(i1)
        # print(i2)
        dict_tmp = {}
        dict_tmp['key'] = str(num_k)
        dict_tmp['msgcont'] = i2
        # isinstance(i1,float)  判断i1是不是float类型的
        if isinstance(i1, float):
            dict_tmp['type'] = '-1'
        else:
            dict_tmp['type'] = i1
        return_one.append(dict_tmp)
        num_k = num_k + 1
    # print(return_one)
    # print(len(return_one))
    print("数据第一次结构化完成")
#
    return_one = create_load_date_xls(return_one)  # 进行分词
    print("数据第二次结构化完成，再原有的单条字典上，增加文本切分后的数据。类型为doc")

    return_one, dict_t = create_type_arr(return_one)  #把标注的类型转成数值
    print("数据第三次结构话数据完成。在原有的数据字典中，增加标记数据的唯一ID。类型为typevalue")

    #未标注
    #将元数据中已经标记和没有标记数据分开。
    #用来存储已经标记的数据
    vo_num=[]
    # 用来储存未标记的数据
    vonull_num = []
    for vo in return_one:
        if vo['type'] == '-1':
            vonull_num.append(vo)
        else:
            vo_num.append(vo)

    wordlist=word_count_str(vo_num)#统计高频的词
    print("文本中的关键字获取完成，写入本地作为训练词典")

    # 写入到txt 文件中 关键
    f = open('word_temp.txt','w',encoding='utf8')
    for obj in wordlist:
        f.write(obj+',')
    f.close()
    print("标记的标签信息，写入本地做为分类标准")
    new_dict = {v:k for k,v in dict_t.items()}

    f = open('type_temp.txt','w',encoding='utf8')
    #字典不能直接写入，需要转成str在写入文档
    s = str(new_dict)
    f.writelines(s)
    f.close()

    # 特征提取
    return_one = create_data_tf(return_one,wordlist)
    print("数据第4次结构话数据完成。在原有的数据字典中，增加用唯一词典中数据表示的句子。类型为'weight'")

    x = []
    y = []
    for vo in vo_num:
        x.append(vo['weight'])
        y.append(vo['typevalue'])
    print(x)
    x_null = []
    for vo in vonull_num:
        x_null.append(vo['weight'])

    # Sklearn - train_test_split随机划分训练集和测试集
    x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1, train_size=0.6)
    print("数据第5次结构话数据完成。将正份的数据切分2份数据集用来训练和测试")

    """
        1.np ==》 numpy包
        2.创建数组： .array
            首先需要创建数组才能对其进行其它操作，通过给array函数传递Python的序列对象创建数组，如果传递的是多层嵌套的序列，将创建多维数组(如c):
            若导入numpy用的是import numpy命令，那么在创建数组的时候用a = numpy.array([1, 2, 3, 4])的形式
            若导入numpy用的是import numpy as np命令，那么用 a = np.array([1, 2, 3, 4])"""
    print("————我是分割线————" * 5)

    # 各自创建自身的矩阵 或是2元数组。
    x0 = np.array(x_train)
    y0 = np.array(y_train)

    # 朴素———贝叶斯训练训练
    clf = GaussianNB().fit(x0,y0)  #搞死分布特征
    print('精度训练：',clf.score(x_train,y_train))
    print('测试精度',clf.score(x_test,y_test))

    #朴素贝叶斯分类器
    clf2 = MultinomialNB().fit(x_train,y_train)
    print('训练精度：',clf2.score(x_train,y_train))
    print('测试精度：',clf2.score(x_test,y_test))

    y_null_hat = clf.predict(x_null)
    print(y_null_hat)

    # 创建中文写模块。
    """workbook = xlwt.Workbook(encoding = 'ascii')
        worksheet = workbook.add_sheet('result')
        row_=0

        for (i1, i2) in zip(vonull_num,y_null_hat):
            worksheet.write(row_, 0, str(new_dict[i2]))
            worksheet.write(row_, 1, i1['msgcont'])
            row_=row_
        workbook.save('tt00.xls')"""

    joblib.dump(clf,'svm_hn.pkl')

