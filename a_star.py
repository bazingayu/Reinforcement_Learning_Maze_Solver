from point import Point
from node import Node
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

class AStar:
    """
    A* 算法 
    python 2.7 
    """
    def __init__(self, map, startNode, endNode, h_method=False):
        """ 
        map:      寻路数组 
        startNode:  寻路起点 
        endNode:    寻路终点 
        """  
        #开放列表
        self.openList = []
        #封闭列表  
        self.closeList = []
        #地图数据
        self.map = map
        #起点  
        self.startNode = startNode
        #终点
        self.endNode = endNode 
        #当前处理的节点
        self.currentNode = startNode
        #最后生成的路径
        self.pathlist = []
        self.visited_num = 0
        self.h_method = h_method
        return

    def getMinFNode(self):
        """ 
        获得openlist中F值最小的节点 
        """  
        nodeTemp = self.openList[0]  
        for node in self.openList:  
            if node.g + node.h < nodeTemp.g + nodeTemp.h:  
                nodeTemp = node  
        return nodeTemp

    def nodeInOpenlist(self,node):
        for nodeTmp in self.openList:  
            if nodeTmp.point.x == node.point.x \
            and nodeTmp.point.y == node.point.y:  
                return True  
        return False

    def nodeInCloselist(self,node):
        for nodeTmp in self.closeList:  
            if nodeTmp.point.x == node.point.x \
            and nodeTmp.point.y == node.point.y:  
                return True  
        return False

    def endNodeInOpenList(self):  
        for nodeTmp in self.openList:
            if self.map.isEndPoint(nodeTmp.point.x, nodeTmp.point.y):
                return True  
        return False

    def getNodeFromOpenList(self,node):  
        for nodeTmp in self.openList:
            if nodeTmp.point.x == node.point.x and nodeTmp.point.y == node.point.y:
                return nodeTmp  
        return None

    def searchOneNode(self,node):
        """ 
        搜索一个节点
        x为是行坐标
        y为是列坐标
        """  
        #忽略障碍
        if self.map.IsObstacle(node.point.x, node.point.y) == True:
            return  
        #忽略封闭列表
        if self.nodeInCloselist(node):  
            return  
        #G值计算 
        if abs(node.point.x - self.currentNode.point.x) == 1 and abs(node.point.y - self.currentNode.point.y) == 1:  
            gTemp = 14  
        else:  
            gTemp = 10  


        #如果不再openList中，就加入openlist  
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            #H值计算
            if not self.h_method:
                node.manhattan(self.endNode)
            else:
                node.Euclidian(self.endNode)
            self.openList.append(node)
            node.father = self.currentNode
        #如果在openList中，判断currentNode到当前点的G是否更小
        #如果更小，就重新计算g值，并且改变father 
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp  
                nodeTmp.father = self.currentNode  
        return

    def searchNear(self):
        """
        (x-1,y-1)(x-1,y)(x-1,y+1)
        (x  ,y-1)(x  ,y)(x  ,y+1)
        (x+1,y-1)(x+1,y)(x+1,y+1)
        """

        self.searchOneNode(Node(Point(self.currentNode.point.x - 1, self.currentNode.point.y)))
        self.searchOneNode(Node(Point(self.currentNode.point.x + 1, self.currentNode.point.y)))
        self.searchOneNode(Node(Point(self.currentNode.point.x, self.currentNode.point.y - 1)))
        self.searchOneNode(Node(Point(self.currentNode.point.x, self.currentNode.point.y + 1)))

        return

    def start(self, ax, plt, show):
        ''''' 
        开始寻路 
        '''
        #将初始节点加入开放列表
        if not self.h_method:
            self.startNode.manhattan(self.endNode)
        else:
            self.startNode.Euclidian(self.endNode)
        self.startNode.setG(0)
        self.openList.append(self.startNode)

        while True:
            #获取当前开放列表里F值最小的节点
            #并把它添加到封闭列表，从开发列表删除它
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)
            self.searchNear()
            self.visited_num += 1
            if show:
                rec = Rectangle((self.currentNode.point.x, self.currentNode.point.y), 1, 1, color='g')
                ax.add_patch(rec)
                plt.draw()
            #检验是否结束
            if self.endNodeInOpenList():
                nodeTmp = self.getNodeFromOpenList(self.endNode)
                while True:
                    self.pathlist.append(nodeTmp)
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        plt.title("a_star_output", y=-0.03)
                        plt.show()
                        plt.savefig("output/astar_output.png")
                        return True
            elif len(self.openList) == 0:
                print("none")
                return self.visited_num

        return

    def setMap(self):
        for node in self.pathlist:
            self.map.setMap(node.point)
        return