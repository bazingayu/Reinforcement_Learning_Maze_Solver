'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: random_map.py
@time: 2023/3/1 18:17
'''
import numpy as np
import point

class RandomMap:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)

    def IsObstacle(self, i, j):
        if (i < 0  or j <0 or i > self.size-2 or j > self.size-2 or self.grid[i][j] == 1):
            return True
        else:
            return False
    def isEndPoint(self, i, j):
        if(i == self.size-2 and j == self.size-2):
            return True
        else:
            return False