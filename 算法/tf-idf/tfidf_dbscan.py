'''
tf-idf + dbscan 实现聚类：
ddscan: 密度聚类算法   (该算法较为吃内存)

cikit-learn中的DBSCAN类

主要参数(本身的参数+最近邻度量的参数)

eps： DBSCAN算法参数，即我们的ϵ-邻域的距离阈值，默认值是0.5。一般需要通过在多组值里面选择一个合适的阈值。eps过大，
        则更多的点会落在核心对象的ϵ-邻域，此时我们的类别数可能会减少， 本来不应该是一类的样本也会被划为一类。反之则类别数可能会增大，
        本来是一类的样本却被划分开。
min_samples：
    DBSCAN算法参数，即样本点要成为核心对象所需要的ϵ-邻域的样本数阈值，默认值是5。
        一般需要通过在多组值里面选择一个合适的阈值。通常和eps一起调参。在eps一定的情况下，
        min_samples过大，则核心对象会过少，此时簇内部分本来是一类的样本可能会被标为噪音点。反之min_samples过小的话，则会产生大量的核心对象。

metric：最近邻距离度量参数。可以使用的距离度量较多，一般来说DBSCAN使用默认的欧式距离（即p=2的闵可夫斯基距离）就可以满足我们的需求
algorithm：最近邻搜索算法参数，算法一共有三种，第一种是蛮力实现，第二种是KD树实现，第三种是球树实现。
    对于这个参数，一共有4种可选输入，‘brute’对应第一种蛮力实现，
                                    ‘kd_tree’对应第二种KD树实现，
                                    ‘ball_tree’对应第三种的球树实现，
                                     ‘auto’则会在上面三种算法中做权衡，
                                     选择一个拟合最好的最优算法。需要注意的是，
    如果输入样本特征是稀疏的时候，无论我们选择哪种算法，最后scikit-learn都会去用蛮力实现‘brute’。
    个人的经验，一般情况使用默认的 ‘auto’就够了。 如果数据量很大或者特征也很多，用”auto”建树时间可能会很长，效率不高，
    建议选择KD树实现‘kd_tree’，此时如果发现‘kd_tree’速度比较慢或者已经知道样本分布不是很均匀时，可以尝试用‘ball_tree’。
    而如果输入样本是稀疏的，无论你选择哪个算法最后实际运行的都是‘brute’。

leaf_size：最近邻搜索算法参数，为使用KD树或者球树时， 停止建子树的叶子节点数量的阈值。
    这个值越小，则生成的KD树或者球树就越大，层数越深，建树时间越长，
    反之，则生成的KD树或者球树会小，层数较浅，建树时间较短。默认是30. 因为这个值一般只影响算法的运行速度和使用内存大小，因此一般情况下可以不管它。

p: 最近邻距离度量参数。只用于闵可夫斯基距离和带权重闵可夫斯基距离中p值的选择，p=1为曼哈顿距离， p=2为欧式距离。如果使用默认的欧式距离不需要管这个参数。

以上就是DBSCAN类的主要参数介绍，其实需要调参的就是两个参数eps和min_samples，这两个值的组合对最终的聚类效果有很大的影响。

'''

def loaddata(filepath):
    import codecs
    file = codecs.open(filepath ,'r','utf-8')
    lines = file.readlines()
    #定义加载数据容器
    trandata = {}
    lineid = []
    linemess =[]
    id=0
    for mess in lines:
       lineid.append(id)
       linemess.append(mess)
       id = id+1
    trandata['lineid'] = lineid
    trandata['linemess']= linemess
    return trandata

def tf_idfload(trandata):
    from sklearn.feature_extraction.text import HashingVectorizer
    vector = HashingVectorizer(n_features=20)
    vector.fit_transform(trandata['linemess'])
    tdf_idflinemess = vector.fit_transform(trandata['linemess']).toarray()
    trandata['tdf_idflinemess'] = tdf_idflinemess
    return trandata

def dbsan_train_data(trandata):

    import sklearn.cluster as skc
    from sklearn.preprocessing import StandardScaler
    # 随机变量标准化，使其服从标准正态分布
    # Standardize features by removing the mean and scaling to unit variance
    #X_Norm = StandardScaler.fit_transform(trandata['tdf_idflinemess'])
    #print(X_Norm)
    #cls_object = DBSCAN(eps=eps, min_samples=min_samples).fit(X_Norm)
    #eps:点举例阈值，聚合条数阈值。
    y_pred = skc.DBSCAN(eps=0.4, min_samples=10).fit_predict(trandata['tdf_idflinemess'])
    return y_pred

def save_model(y_pred,save_path):
    from sklearn.externals import joblib
    joblib.dump(y_pred,save_path)





if __name__=='__main__':
    #加载数据
    trandata = loaddata('nenddatasplit.log') #此时原数据字典中有lineid(行号)，linemess(行信息)
    #tf-idf 对行信息进行加权
    trandata = tf_idfload(trandata)
    #DBSCAN进行聚类训练
    y_pred = dbsan_train_data(trandata)
    #保存模型
    save_model(y_pred,'ii.pkl')
    trandata['result'] = y_pred
    #写出训练数据
    output = open('output.log', 'w', encoding='utf-8')  #
    row = 0
    for (i1, i2, i3) in zip(trandata['lineid'],trandata['result'],trandata['linemess']):
        new_line="%s,%s,%s+\n" %(i1,i2,i3.replace("\n", ""))
        output.write(new_line)
        row = row + 1
    print(row)
