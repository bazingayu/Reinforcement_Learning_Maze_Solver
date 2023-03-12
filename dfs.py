'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: dfs.py
@time: 2023/3/10 20:36
'''
import random_map
from matplotlib.patches import Rectangle

class DFS:
    def __init__(self, map):
        self.map = map
        self.visited_num = 0

    def dfs(self, x, y, visited=None, ax=None, plt=None, show=True):
        if self.map.isEndPoint(x, y):
            print(x, y)
            plt.title("dfs_output", y=-0.03)
            plt.show()
            plt.savefig("output/dfs_output.png")
            return
        if visited is None:
            visited = []
        visited.append([x, y])
        self.visited_num += 1
        if show:
            rec = Rectangle((x, y), 1, 1, color='g')
            ax.add_patch(rec)
            plt.draw()

        if(not self.map.IsObstacle(x-1, y) and [x-1, y] not in visited):
            self.dfs(x-1, y, visited, ax, plt, show)
        if (not self.map.IsObstacle(x+1, y) and [x+1, y] not in visited):
            self.dfs(x+1, y, visited, ax, plt, show)
        if (not self.map.IsObstacle(x, y-1) and [x, y-1] not in visited):
            self.dfs(x, y-1 , visited, ax, plt, show)
        if (not self.map.IsObstacle(x, y+1) and [x, y+1] not in visited):
            self.dfs(x, y+1, visited, ax, plt, show)
        return

    def startAndSaveImage(self, ax, plt, show):
        self.dfs(1, 1, visited=None, ax=ax, plt=plt, show=show)
        return


