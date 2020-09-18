import codecs
from time import time
# tf-idf + kmeans 实现 聚类算法。
'''
scikit-learn中的KMeans类 （该算法较为吃CPU）

主要参数 
n_clusters：聚类数量，默认为8
init： 初始值选择的方式，默认为k-means++，可以为完全随机选择random或者ndarray
n_init：用不同的初始化质心运行算法的次数。由于K-Means是结果受初始值影响的局部最优的迭代算法，因此需要多跑几次以选择一个较好的聚类效果，默认是10。
max_iter：最大的迭代次数，默认300次。
tol ：容忍的最小误差(默认为0.0001)，当误差小于tol就会退出迭代。
algorithm：默认为auto，不用更改。
random_state：The generator used to initialize the centers. If an integer is given, it fixes the seed(即：给定一个整数后，每次运行的结果都是一致的，否则是随机的)

'''
#


file = codecs.open('kmeans.log', 'r', encoding='utf-8')
lines = file.readlines()
corpus ={}
listid = []
listmess = []
i=0
for line in lines:
    listid.append(i)
    listmess.append(line)
    i = i+1
corpus['id'] = listid
corpus['line'] =listmess
#print(i)
#print(corpus['id'])
#print(corpus['line'])


#tf-idf 应用，文本赋权操作。
'''
from sklearn.feature_extraction.text import TfidfVectorizer
#idf 计算逆向文档率。
#vectorizer = TfidfVectorizer(min_df=5)
vectorizer = TfidfVectorizer()
vectorizer.fit_transform(corpus)
#注意mess_array和num_array
mess_array = vectorizer.get_feature_names()
num_array = vectorizer.fit_transform(corpus).toarray()
print (mess_array)
print(num_array)
'''

# 通过哈希表来实现特征向量
from sklearn.feature_extraction.text import HashingVectorizer
vector=HashingVectorizer(n_features=20)
vector.fit_transform(corpus['line'])
#mess_array_1 =vector.get_feature_names()
num_array_1 = vector.fit_transform(corpus['line']).toarray()
#print (mess_array_1)
#print(num_array_1)


if __name__ == '__main__':

     #kmeans 应用 文本分类
    #第一中分类。
    from sklearn.cluster import KMeans
    num_clusters = 240
     #
    km_cluster = KMeans(n_clusters = num_clusters,max_iter=100, n_init=15,
                    init='k-means++',n_jobs=-1) #n_jobs：并行数，一般等于CPU核数
    #返回各自文本的所被分配到的类索引
    result = km_cluster.fit_predict(num_array_1)
    num = km_cluster.labels_
    corpus['num'] = num

    #分成类别显示。

    #将两个列表 一一对应的合并成字典。
    #dic = dict(zip(corpus['id'],corpus['line'],num))
    #print(dic)
    #根据字典中的num 进行排序
    #result = sorted(dic.items(), key=lambda d: d[2], reverse=True)
    #print(result)

    #print(corpus)

    import xlwt

    #new_dict = {v: k for k, v in corpus.items()} '
    output = open('output.log', 'w',encoding='utf-8')#
    row = 0
    for (i1, i2,i3) in zip(listid, listmess,num):
        new_line="%s,%s,%s+\n"  %(i1,i3 ,i2.replace("\n", ""))
        output.write(new_line)
        row = row + 1
    print(row)











'''
    # 注释语句用来存储你的模型
    from sklearn.externals import joblib
    #保存模型
    joblib.dump(km_cluster,  'doc_cluster.pkl')
    #加载模型
    km=joblib.load('doc_cluster.pkl')
    km.fit_predict(num_array_1)
    print(km.labels_)
    
    from sklearn.cluster import KMeans
    num_clusters = 3
    km = KMeans(n_clusters=num_clusters)
    km.fit(num_array_1)
    clusters = km.labels_.tolist()
    print(clusters)
    '''






