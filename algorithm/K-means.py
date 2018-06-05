# coding=utf-8  

from numpy import *
from numpy.random.mtrand import power


def loadDataSet(fileName):  # 文件的导入  
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')  # strip()删除开头和结尾的空白符(包括'\n', '\r', '\t', ' ')  
        fltLine = map(float, curLine)  # map对curLine列表使用float函数，float将整数和字符串转换成浮点数  
        dataMat.append(fltLine)
    return dataMat


# 计算两个向量的距离，用的是欧几里的距离  
def distEclud(vecA, vecB):  # 计算欧式距离  
    # vecA,vecB都是numpy的matrix类型  
    vecC = vecA - vecB
    # 对每个元素求平方  
    vecC = multiply(vecC, vecC)

    row = shape(vecC)[0]  # 行数  
    col = shape(vecC)[1]  # 列数  

    result = 0
    for i in range(row):
        for j in range(col):
            result += vecC[i, j]

    return sqrt(result)


def randCent(dataSet, k):  # 构建一个包含k个随机质心的集合  
    n = shape(dataSet)[1]  # 读取dataSet的列数，2列  
    centroids = mat(zeros((k, n)))  # k*2  
    for j in range(n):  # 对每一列  
        minJ = min(dataSet[:, j])   # dataSet[:, j] 取所有数据的第j列 min()返回最小值  
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids   # 共k行，两列，每行是每个质心的x,y  


def kMeans(dataSet, k, distMeas = distEclud, createCent=randCent):
    m = shape(dataSet)[0]  # 读取dataSet的行数，即一共多少个点  
    clusterAssment = mat(zeros((m, 2)))  # 记录每个点前一次离哪个质心最近，第1列是质心的下标，第2列是最小距离的平方  
    centroids = createCent(dataSet, k)  # 构建一个随机取的k个质心的集合  
    clusterChanged = True   # 标记簇是否改变了，是否已收敛  
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # 总数据中给的每个点  
            minDist = inf  # 正无穷  
            minIndex = -1
            for j in range(k):  # 每个质点  
                distJI = distMeas(centroids[j, :], dataSet[i, :])  # 计算每个点到每个质心的欧式距离  
                if distJI < minDist:   # 记录该点到哪个质心的距离最近  
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        # print centroids  
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


# 可视化展示  
def show(dataSet, k, centroids, clusterAssment):
    from matplotlib import pyplot as plt
    numSamples, dim = dataSet.shape  # 求行数和列数  
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    for i in xrange(numSamples): # 使用range生成的是一个列表，xrange生成的是一个生成器，每次调用的时候才取出来  
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)
    plt.show()


dataMat = mat(loadDataSet('testSet.txt'))
myCentroids, clusterAssing = kMeans(dataMat, 6)
# myCentroids是k=4个质心的信息，x,y值  
# 记录每个点前一次离哪个质心最近，第1列是质心的下标，第2列是最小距离的平方  
show(dataMat, 4, myCentroids, clusterAssing)
# 画图展示 
