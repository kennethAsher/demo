import pandas as pd
import numpy as np
from docx import Document
df1 = pd.read_excel('data1.xlsx')
df2 = pd.read_excel('data2.xlsx')

#其中，padnas使用一句话就能找到
conment = df1[df1 != df2]
print(conment)
# 但是上述，只能找到数据是什么，在什么位置，数据量太大，不好找

#还一种方式，先找到有哪些是不同的数值
comparison_values = df1.values == df2.values
#使用numpy根据True/False定位元素位置，将数值改变写入到原来的表格
rows, cols=np.where(comparison_values ==False)

for item in zip(rows, cols):
    df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]])
df1.to_excel('diff.xlsx', index=False, header=True)
#上述就能查找到两个文件不同的内容了


#对比两个docx不相同内容
def getText(wordname):
    '''
    提取文字
    '''
    d = Document(wordname)
    texts = []
    for para in d.paragraphs:
        texts.append(para.text)
    return texts


def is_Chinese(word):
    '''font
    识别中文
    '''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def msplit(s, seperators=',|\.|\?|，|。|？|！|、'):
    '''
    根据标点符号分句
    '''
    return re.split(seperators, s)


def readDocx(docfile):
    '''
    读取文档
    '''
    print(f"======正在读取{docfile}======")
    paras = getText(docfile)
    segs = []
    for p in paras:
        temp = []
        for s in msplit(p):
            if len(s) > 2:
                temp.append(s.replace(' ', ""))
        if len(temp) > 0:
            segs.append(temp)
    return segs
