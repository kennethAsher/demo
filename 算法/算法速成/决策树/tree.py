#-*-coding:utf-8-*-
#熵值越大，决策树分离的效果越好，越小，越差
import numpy as np
import scipy as sp
from sklearn import tree
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split

data = []
lables = []
with open("1.txt", 'r', encoding='utf-8') as file_read:
    for line in file_read:
        tokens = line.strip().split(' ')
        data.append([float(tk) for tk in tokens[:-1]])
        lables.append(tokens[-1])
#list不是array 需要将list 进行array之后才能进行numpy的其他操作
x = np.array(data)
lables = np.array(lables)
y = np.zeros((lables.shape))

''' 标签转换为0/1 '''
y[lables=='fat']=1        #zero之后作为一个array，每行都有属于自己的名字，能够直接对其进行数据的修改 替换

''' 拆分训练数据与测试数据 '''
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)   #test_size测试级占比，

'''使用信息熵作为划分标准，对决策树进行训练'''
clf = tree.DecisionTreeClassifier(criterion='entropy')
print(clf)
clf.fit(x_train, y_train)


'''把决策树结构写入文件'''
with open('tree.dot', 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
print(clf.feature_importances_)
answer = clf.predict(x_train)
print(x_train)
print(answer)
print(y_train)
print(np.mean(answer == y_train))

'''准确率与召回率'''
precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))   #简单理解成绘制
answer = clf.predict_proba(x)[:,1]
print(classification_report(y, answer, target_names = ['thin', 'fat']))


#决策树的保存

