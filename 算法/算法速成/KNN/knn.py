from numpy import *
import operator

#创建一个数据集，包含2个类别和4个样本
def create_dataset():
    #生成一个矩阵，每行代表一个样本
    group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
    #4个样本分别所属的类型
    labels = ['A', 'A', 'B', 'B']
    return group, labels

#KNN分类算法函数定义
def knn_classify(new_input, data_set, labels, k):
    num_samples = data_set.shape[0]   #shape[0]表示行数
    ##step1：计算距离
    #tile(A,reps):构造一个矩阵，通过A重复reps次得到
    # the following copy numsamples rows for dataSet
    diff = tile(new_input, (num_samples, 1)) - data_set   #按元素求差值
    squared_diff = diff**2   #将差值求平方
    squared_dist = sum(squared_diff, axis=1)   #按行累加  0是按列排序
    distance = squared_dist ** 0.5 #将差值平方和开方，即得到距离

    #step2：对距离排序
    sorted_dist_indices = argsort(distance)   #argsort对数组进行排序，返回排序之后各坐标的索引值
    class_count = {}
    for i in xrange(k):  #只返回索引，需要list（xrange）才能返回列表
        # step3:选择K个临近值
        vote_label = labels[sorted_dist_indices[i]]
        # step4:计算k个最近邻中各类别出现的次数
        class_count[vote_label] = class_count.get(vote_label, 0) + 1

    #step5: 返回出现的次数最多的类别标签
    max_count = 0
    for key, value in class_count.items():
        if value > max_count:
            max_count = value
            max_index = key
    return max_index



# 测试程序： 交互输入数据获取分类
def classifyPerson():
    resultList = ['根本不可能','有点希望','希望之星']
    percentTats = float(raw_input("玩游戏所花时间百分比？"))
    ffMiles = float(raw_input("每年的飞行里程？"))
    iceCream = float(raw_input("每年吃几升冰激凌？"))
    datingDataMat,datingLabels = file2matrix('D:/PycharmProjects/machinelearningtest/knn/datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print ("你对这个人的感觉：",resultList[classifierResult - 1])
classifyPerson()


# 利用分类器进行手写数字识别测试
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('D:/PycharmProjects/machinelearningtest/knn/digits/trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('D:/PycharmProjects/machinelearningtest/knn/digits/trainingDigits/%s' %fileNameStr)
    testFileList = listdir('D:/PycharmProjects/machinelearningtest/knn/digits/testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('D:/PycharmProjects/machinelearningtest/knn/digits/testDigits/%s' %fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print ("the classifier came back with: %d, the real answer is: %d" %(classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print ("\nthe total number of errors is: %d" %errorCount)
    print ("\nthe total error rate is: %f" %(errorCount/float(mTest)))
# handwritingClassTest()


