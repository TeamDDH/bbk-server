# coding=utf-8
import numpy as np
from math import sqrt
import time
import matplotlib.pylab as pl


# 定义一个簇单元
class ClusterUnit:
    def __init__(self):
        self.node_list = []  # 该簇存在的节点列表
        self.node_num = 0  # 该簇节点数
        self.centroid = None  # 该簇质心

    def add_node(self, node, node_vec):
        """
        为本簇添加指定节点，并更新簇心
         node_vec:该节点的特征向量
         node:节点
         return:null
        """
        self.node_list.append(node)
        try:
            self.centroid = (self.node_num * self.centroid + node_vec) / (self.node_num + 1)  # 更新簇心
        except TypeError:
            self.centroid = np.array(node_vec) * 1  # 初始化质心
        self.node_num += 1  # 节点数加1

    def remove_node(self, node):
        # 移除本簇指定节点
        try:
            self.node_list.remove(node)
            self.node_num -= 1
        except ValueError:
            raise ValueError("%s not in this cluster" % node)  # 该簇本身就不存在该节点，移除失败

    def move_node(self, node, another_cluster):
        # 将本簇中的其中一个节点移至另一个簇
        self.remove_node(node=node)
        another_cluster.add_node(node=node)

        # cluster_unit = ClusterUnit()


# cluster_unit.add_node(1, [1, 1, 2])
# cluster_unit.add_node(5, [2, 1, 2])
# cluster_unit.add_node(3, [3, 1, 2])
# print cluster_unit.centroid


def euclidian_distance(vec_a, vec_b):
    # 计算向量a与向量b的欧式距离
    diff = vec_a - vec_b
    return sqrt(np.dot(diff, diff))  # dot计算矩阵内积


class OnePassCluster:
    def __init__(self, t, vector_list):
        # t:一趟聚类的阈值
        self.threshold = t  # 一趟聚类的阈值
        self.vectors = np.array(vector_list)
        self.cluster_list = []  # 聚类后簇的列表
        t1 = time.time()
        self.clustering()
        t2 = time.time()
        self.cluster_num = len(self.cluster_list)  # 聚类完成后 簇的个数
        self.spend_time = t2 - t1  # 聚类花费的时间

    def clustering(self):
        self.cluster_list.append(ClusterUnit())  # 初始新建一个簇
        self.cluster_list[0].add_node(0, self.vectors[0])  # 将读入的第一个节点归于该簇
        for index in range(len(self.vectors))[1:]:
            min_distance = euclidian_distance(vec_a=self.vectors[0],
                                              vec_b=self.cluster_list[0].centroid)  # 与簇的质心的最小距离
            min_cluster_index = 0  # 最小距离的簇的索引
            for cluster_index, cluster in enumerate(self.cluster_list[1:]):
                # enumerate会将数组或列表组成一个索引序列
                # 寻找距离最小的簇，记录下距离和对应的簇的索引
                distance = euclidian_distance(vec_a=self.vectors[index],
                                              vec_b=cluster.centroid)
                if distance < min_distance:
                    min_distance = distance
                    min_cluster_index = cluster_index + 1
            if min_distance < self.threshold:  # 最小距离小于阈值，则归于该簇
                self.cluster_list[min_cluster_index].add_node(index, self.vectors[index])
            else:  # 否则新建一个簇
                new_cluster = ClusterUnit()
                new_cluster.add_node(index, self.vectors[index])
                self.cluster_list.append(new_cluster)
                del new_cluster

    def print_result(self, label_dict=None):
        # 打印出聚类结果
        # label_dict:节点对应的标签字典
        print
        "*******  one-pass cluster result  ***********"
        for index, cluster in enumerate(self.cluster_list):
            print
            "cluster:%s" % index  # 簇的序号
            print
            cluster.node_list  # 该簇的节点列表
            if label_dict is not None:
                print
                " ".join([label_dict[n] for n in cluster.node_list])  # 若有提供标签字典，则输出该簇的标签
            print
            "node num: %s" % cluster.node_num
            print
            "-------------"
        print
        "the number of nodes %s" % len(self.vectors)
        print
        "the number of cluster %s" % self.cluster_num
        print
        "spend time %.9fs" % (self.spend_time / 1000)


        # 读取测试集


temperature_all_city = np.loadtxt('c2.txt', delimiter=",", usecols=(3, 4))  # 读取聚类特征
xy = np.loadtxt('c2.txt', delimiter=",", usecols=(8, 9))  # 读取各地经纬度
f = open('c2.txt', 'r')
lines = f.readlines()
zone_dict = [i.split(',')[1] for i in lines]  # 读取地区并转化为字典
f.close()

# 构建一趟聚类器
clustering = OnePassCluster(vector_list=temperature_all_city, t=9)
clustering.print_result(label_dict=zone_dict)

# 将聚类结果导出图
fig, ax = pl.subplots()
fig = zone_dict
c_map = pl.get_cmap('jet', clustering.cluster_num)
c = 0
for cluster in clustering.cluster_list:
    for node in cluster.node_list:
        ax.scatter(xy[node][0], xy[node][1], c=c, s=30, cmap=c_map, vmin=0, vmax=clustering.cluster_num)
    c += 1
pl.show()