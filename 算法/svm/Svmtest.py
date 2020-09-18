# coding = utf-8
'''
    create on 20171121
    @author  YXLang
'''
import re

import pandas as pd
import jieba.posseg as pseg

'''
设计思路：（未完成）
    采用SVM 模型对短信文本数据进行训练。实现已知短信文本的准确分类
设计流程：
    1.数据的加载（清洗==>切分==>）
    
'''
#从磁盘加载数据,并将数据格式化
def loaddata(path ,type1,type2):
    file = open(path)
    line = file.readline()
    line = pd.read_excel(path, name=[type1, type2])
    type = line['type']
    mess = line['mess']
    num_k = 1
    all_message = []
    for (i1, i2) in zip(type, mess):
        # 新建一个字典，来存储数据。
        lines = {}
        lines['key'] = str(num_k)
        lines['msgcount'] = i2
        if (isinstance(i1, float)):
            lines['type'] = '-1'
        else:
            lines['type'] = i1
        all_message.append(lines)
        num_k += 1
    print(len(all_message))
    return all_message
#切分需要处理的数据
def del_stop_word(mess,stopwords):
    words = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", ",", mess)
    words = words.strip()
    words_split = pseg.cut(words)
    result = []
    #获取名词和动词
    for w in words_split:
        if (w.flag == 'v'):
            result.append(w.word)
        if (w.flag == 'n'):
            result.append(w.word)
    # result=jieba.cut(words, cut_all=False)#分词
    new_words = []
    for i in result:  # 对分词结果进行遍历
        if i not in stopwords:  # 如果词语不在停用词表，是我们需要的词
            s_word = i.strip()
            if (len(s_word) > 1):
                new_words.append(i) # 将保留下来的词追加到一个新的list中

    return new_words

def splitdata( lines , stopwords ):
    print (lines)
    word_set = set()
    for line in lines:
        try:
            mess = line['msgcount']
            if( len(mess) > 1 ):
                y = mess
                y = y[0:200]
                mess_splits = del_stop_word(y,stopwords)    #根据文本切分出的词。
                word_set = word_set.union(set(mess_splits))
                print (word_set)
            else:
                print(mess+"0000000")
        except Exception as e:
            print(e)
        lines['doc'] = line_splits
    return  message ,word_set
#流程main
if __name__ == '__main__':
    stopwords = {}.fromkeys([line.rstrip() for line in open('../file/wordstop.txt')])
    #加载数据 并格式化数据。
    lines =loaddata('../datainput/svm.log', 'type', 'mess')
    print(lines)
    #print(stopwords)
    #line,line_split = splitdata(lines,stopwords)


    #数据处理




