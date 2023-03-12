'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: bfs.py
@time: 2023/3/10 22:11
'''

'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: dfs.py
@time: 2023/3/10 20:36
'''
import random_map
from matplotlib.patches import Rectangle

class BFS:
    def __init__(self, map):
        self.map = map
        self.visited_num = 0

    def start(self, ax=None, plt=None, show=False):
        queue = []  # 新建队列
        queue.append([1, 1])  # 将初始节点加入到队列中
        visited = list()  # 建立一个集合，后续判断是否重复
        visited.append([1, 1])
        while (len(queue) > 0):
            vertex = queue.pop(0)  # 移出队列的第一个元素
            for w in [[vertex[0]-1, vertex[1]], [vertex[0]+1, vertex[1]], [vertex[0], vertex[1]-1], [vertex[0], vertex[1]+1]]:
                if(self.map.isEndPoint(w[0], w[1])):
                    if show:
                        plt.title("bfs_output", y=-0.03)
                        plt.show()
                        plt.savefig("output/bfs_output.png")
                    return
                if (w not in visited and not self.map.IsObstacle(w[0], w[1])):  # 如果节点不重复，就添加到队列中
                    queue.append(w)
                    visited.append(w)
                    self.visited_num += 1
                    if show:
                        rec = Rectangle((w[0], w[1]), 1, 1, color='g')
                        ax.add_patch(rec)
                        # plt.draw()

        return plt





