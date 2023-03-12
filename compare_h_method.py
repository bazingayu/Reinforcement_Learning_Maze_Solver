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

man_time = []
man_visited = []
eu_time = []
eu_visited = []
show = False

sizes = [3, 5, 10, 15, 20]
for height in tqdm(sizes):
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
    aStar = a_star.AStar(map, Node(Point(1, 1)), Node(Point(height*2-1, width*2-1)))
    plt3 = aStar.start(ax, plt, show)
    end_time = time.time()
    man_time.append(end_time-start_time)
    man_visited.append(aStar.visited_num)

    start_time = time.time()
    aStar = a_star.AStar(map, Node(Point(1, 1)), Node(Point(height * 2 - 1, width * 2 - 1)), h_method=True)
    plt3 = aStar.start(ax, plt, show)
    end_time = time.time()
    eu_time.append(end_time - start_time)
    eu_visited.append(aStar.visited_num)
#
#
#
x = []
for i in sizes:
    x.append(i * 2 + 1)
plt.figure()
plt.plot(x, man_time, 'o-', color='r', label='manhattan time')
plt.plot(x, eu_time, 'o-', color='g', label='Euclidian time')
plt.xlabel("maze size")
plt.ylabel("FindPathTime")
plt.legend(loc="best")
plt.savefig("heuristic_time_compare.png")

plt.figure()
plt.plot(x, man_visited, 'o-', color='r', label='manhattan visited num')
plt.plot(x, eu_visited, 'o-', color='g', label='Euclidian visited num')
plt.xlabel("maze size")
plt.ylabel("visited_cell_nums")
plt.legend(loc="best")
plt.savefig("heuristic_visited_cell_nums.png")

