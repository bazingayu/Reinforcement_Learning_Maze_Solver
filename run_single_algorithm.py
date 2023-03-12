'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: run_single_algorithm.py
@time: 2023/3/12 14:19
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
import argparse
from tqdm import tqdm
parser = argparse.ArgumentParser(description='argument')

parser.add_argument('--size', '-s', type=int, help='size of the maze')
parser.add_argument('--random', '-r', type=int, help='random seeds', default=1)
parser.add_argument('--method', '-m', type=str, help='Method, Including  dfs, bfs, astar, value, policy', default='dfs')

args = vars(parser.parse_args())
print(args['size'])

height = args['size']
width = args['size']

show = True

m = Maze(args['random'])
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

if args['method'] == "dfs":
    start_time = time.time()
    dfs_algorithm = dfs.DFS(map)
    plt1 = dfs_algorithm.startAndSaveImage(ax, plt, show)
    end_time = time.time()
    print("dfs_done")

elif args['method'] == 'bfs':
    start_time = time.time()
    bfs_algorithm = bfs.BFS(map)
    plt2 = bfs_algorithm.start(ax, plt, show)
    end_time = time.time()
    print("bfs_done")

elif args['method'] == 'astar':
    start_time = time.time()
    aStar = a_star.AStar(map, Node(Point(1, 1)), Node(Point(height*2-1, width*2-1)))
    aStar.start(ax, plt, show)
    end_time = time.time()
    print("astar done")

elif args['method'] == 'policy':
    start_time = time.time()
    mdp_p = Policy_MDP(map)
    plt4 = mdp_p.start_and_got_the_best(ax, plt, show)
    end_time = time.time()
    print("policy done")

elif args['method'] == 'value':
    start_time = time.time()
    mdp_v = Value_MDP(map)
    plt5 = mdp_v.start_and_got_the_best(ax, plt, show)
    end_time = time.time()
    print("value done")

