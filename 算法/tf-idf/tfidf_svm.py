# tf-idf + svm 实现文本分类训练
# author TDLang
# createtime 2017-12-28

'''
该代码只实现了 tf-idf + svm 文本分类训练。还需要实现大数据量的测试。
'''
'''
加载训练数据，并且格式化数据
'''
def loaddata(path) :
    #加载数据的容器
    testdata = {}
    types = []
    typeid = []
    mess = []
    linenum = []
    num = 1
    id = 1
    # 读取数据文件
    file = open(path,'r',encoding='utf-8')
    lines = file.readlines()
    #迭代，初步格式化数据。
    for a in lines:
        line = a.split('|')
        linenum.append(num)
        types.append(line[0])
        mess.append(line[1])
        num += 1
    # 确定类型id
    typemess = list(set(types))
    for type in types:
        if type in typemess:
            typeid.append(typemess.index(type))

    #数据合并入字典：
    testdata['linenum'] = linenum
    testdata['type'] = types
    testdata['mess'] = mess
    testdata['typeid'] =typeid
    print('linenum的数量：',len(testdata['linenum']))
    print('type的数量：', len(testdata['type']))
    print('mess的数量：', len(testdata['mess']))
    print('typeid的数量：', len(testdata['typeid']))
    return  testdata ,types,typemess
'''
采用结巴切词短信进行切分
'''
def splitmess(testdata):
    import re
    import jieba

    splitline=[]
    for linemess in testdata['mess']:
        newline = re.sub("[A-Za-z0-9\[\，\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\【\】\。\,]", ",",linemess).strip()
        cut=jieba.cut(newline)
        words = ''
        for word in cut:
            if( word!=','):
                words =words + word + '\t'
        splitline.append(words)
    testdata['splitline'] = splitline
    return testdata
'''
给分词完的短信信息 加权处理 采用tf-idf 加权
'''
def tf_idfload(testdata):
    from sklearn.feature_extraction.text import HashingVectorizer

    vector = HashingVectorizer(n_features=20)
    vector.fit_transform(testdata['splitline'])
    num_array_1 = vector.fit_transform(testdata['splitline']).toarray()
    testdata['tf-idfnum']= num_array_1
    return testdata
'''
对训练文本进行分割：训练数据集和测速数据集
'''
def split_trian_data(testdata):
    from sklearn.cross_validation import train_test_split
    type_train, type_test, tfidf_train, tdidf_test = train_test_split(testdata['typeid'], testdata['tf-idfnum'],
                                                                      random_state=1, train_size=0.6)
    return type_train, type_test, tfidf_train, tdidf_test
'''
采用svm 进行分类训练
'''
def train_data(type_train, type_test, tfidf_train, tdidf_test ):
    from sklearn import svm
    clf = svm.SVC(C=1.5, kernel='linear', gamma=40, decision_function_shape='ovo')
    clf.fit(tfidf_train, type_train)
    print('训练精度', clf.score(tfidf_train, type_train))  # 精度
    print('测试精度', clf.score(tdidf_test, type_test))
    return clf

'''
保存训生成的模型
'''
def save_model(clf,path):
    from sklearn.externals import joblib

    joblib.dump(clf,path)

'''
下词分类时加载 分类器，注意这里需要将 标记映射出的id进行保存。（考虑写入到数据库，形成映射表）
'''
def load_model(path):
    from sklearn.externals import joblib

    clf = joblib.load('svm_hn.pkl')
    clf.predict('需要分类数据的权重')

''' 处理的主函数'''
if __name__ == '__main__':
    #加载数据并初步格式话数据。
    testdata ,types ,typemess= loaddata('svm.log') # 此时的训练数据字典里有（linenum, type, typeid, mess,）
    #格式化数据 切分词。
    testdata = splitmess(testdata) # 此时的训练数据字典里有（linenum，types，typeid, mess，splitline）
    #tf-idf 加权
    testdata = tf_idfload(testdata) # 此时的训练数据字典里有（linenum，types，typeid, mess，splitline, tf-idfnum）
    #切分训练和测试集。
    type_train, type_test, tfidf_train, tdidf_tes = split_trian_data(testdata)
    # svm 分类训练。
    clf=train_data(type_train, type_test, tfidf_train, tdidf_tes )
    #保存模型
    save_model(clf,'svm_hn.pkl')
    # 分好的类别 分类计算
    result= clf.predict(testdata['tf-idfnum'])
    print(len(typemess))

    # 将分好的数据写出
    output = open('output.log', 'w', encoding='utf-8')
    for(i1,i2,i3,) in zip (testdata['linenum'],result ,testdata['mess']):
        new_line = "%s,%s,%s+\n" % (i1, typemess[i2], i3.replace("\n",""))
        output.write(new_line)



