'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: node.py
@time: 2023/3/10 23:06
'''
import numpy as np
class Node:
    def __init__(self, point, g=0, h=0):
        self.point = point  # 自己的坐标
        self.father = None  # 父节点
        self.g = g  # g值
        self.h = h  # h值

    """
    估价公式：曼哈顿算法
     """

    def manhattan(self, endNode):
        self.h = (abs(endNode.point.x - self.point.x) + abs(endNode.point.y - self.point.y)) * 10

    def Euclidian(self, endNode):
        self.h = np.sqrt((endNode.point.x - self.point.x) ** 2 + (endNode.point.y - self.point.y) ** 2) * 10

    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node
