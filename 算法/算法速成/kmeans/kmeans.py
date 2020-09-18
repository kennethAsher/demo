from numpy import *
#加载数据
def load_data(file_name):
    data_mat = []
    fr = open(file_name)
    for line in fr.readlines():
        cur_line = line.strip().split('\t')
        flt_line = map(float, cur_line)   #变成float类型    #map（方法，数据集）  将数据集的每一个数据都进行前面方法的执行，返回处理之后的结果
        data_mat.append(flt_line)
    return data_mat

#计算欧几里得距离
def dist_ecloud(vec_a, vec_b):
    return sqrt(sum(power(vec_a-vec_b), 2))

#构建聚簇中心， 取k个（此例中为4）随机质心
def rand_cent(data_set, k):
    n = shape(data_set)[1]
    cent_roids = mat(zeros((k,n)))   #每个质心有n个坐标， 总共要k个质心
    for j in range(n):
        min_j = min(data_set[:,j])
        max_j = max(data_set[:,j])
        range_j = float(max_j - min_j)
        cent_roids[:,j] = min_j + range_j*random.rand(k,1)
    return cent_roids

#k_means聚类算法
def kmeans(data_set, k, dist_means=dist_ecloud, create_cent=rand_cent):
    m = shape(data_set)[0]
    cluster_assment = mat(zeros((m,2)))  #将数组变成矩阵   ---用来存放样本属于哪类及质心距离
    cent_roids = create_cent(data_set, k)
    cluster_changed = True
    while cluster_assment:
        cluster_changed = False
        for i in range(m):
            min_dist = inf
            min_index = -1;
            for j in range(k):
                dist_jl = dist_means(cent_roids[j,:], data_set[i,:])
                if dist_jl < min_dist:
                    min_dist = dist_jl
                    min_index = j
            if cluster_assment[i,0] != min_index:
                cluster_changed = True
            cluster_assment[i,:] = min_index, min_dist**2
        print(cent_roids)
        for cent in range(k):
            ptsln_clust = data_set[nonzero(cluster_assment[:,0].A == cent)[0]]  #去第一列等于cent的所有列
            cent_roids[cent,:] = mean(ptsln_clust, axis=0)
    return cent_roids, cluster_assment









