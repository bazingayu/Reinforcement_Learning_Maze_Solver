'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: compare_all_algorithms.py
@time: 2023/3/10 19:29
'''
from mazelib import Maze
from mazelib.generate.Prims import Prims
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from random_map import RandomMap
from matplotlib.patches import Rectangle
import a_star
import dfs
import time
import bfs
from node import Node
from point import Point
from mdp_value import Value_MDP
from mdp_policy import Policy_MDP
from tqdm import tqdm

height = 20
width = 20

bfs_time = []
dfs_time = []
astart_time = []
policy_time = []
value_time = []
bfs_num = []
dfs_num = []
astar_num = []
show = True

height = 10
width = height
m = Maze(345)
m.generator = Prims(height, width)
m.generate()
ax = plt.gca()
ax.set_xlim([0, height])
ax.set_ylim([0, width])

for i in range(height*2+1):
    for j in range(width*2+1):
        if m.grid[i][j]:
            rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
        else:
            rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
            ax.add_patch(rec)

rec = Rectangle((1, 1), width = 1, height = 1, facecolor='b')
ax.add_patch(rec)

rec = Rectangle((height*2-1, width*2-1), width = 1, height = 1, facecolor='r')
ax.add_patch(rec)

map = RandomMap(m.grid)

plt.axis('equal')
plt.axis('off')
plt.tight_layout()

start_time = time.time()
dfs_algorithm = dfs.DFS(map)
plt1 = dfs_algorithm.startAndSaveImage(ax, plt, show)
end_time = time.time()
dfs_time.append(end_time-start_time)
dfs_num.append(dfs_algorithm.visited_num)
print("dfs_done")

start_time = time.time()
bfs_algorithm = bfs.BFS(map)
plt2 = bfs_algorithm.start(ax, plt, show)
end_time = time.time()
bfs_time.append(end_time-start_time)
bfs_num.append(bfs_algorithm.visited_num)
print("bfs_done")


start_time = time.time()
aStar = a_star.AStar(map, Node(Point(1, 1)), Node(Point(height*2-1, width*2-1)))
aStar.start(ax, plt, show)
end_time = time.time()
astart_time.append(end_time-start_time)
astar_num.append(aStar.visited_num)
print("astar done")

start_time = time.time()
mdp_p = Policy_MDP(map)
plt4 = mdp_p.start_and_got_the_best(ax, plt, show)
end_time = time.time()
policy_time.append(end_time-start_time)
print("policy done")
#
start_time = time.time()
mdp_v = Value_MDP(map)
plt5 = mdp_v.start_and_got_the_best(ax, plt, show)
end_time = time.time()
value_time.append(end_time-start_time)
print("value done")

