'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: compare_mdp_parameters.py
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

gamma5_policy_time = []
gamma5_policy_iterations = []
gamma5_value_time = []
gamma5_value_iterations = []

gamma9_policy_time = []
gamma9_policy_iterations = []
gamma9_value_time = []
gamma9_value_iterations = []

gamma6_policy_time = []
gamma6_policy_iterations = []
gamma6_value_time = []
gamma6_value_iterations = []


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
    mdp_p = Policy_MDP(map, 0.9)
    plt4 = mdp_p.start_and_got_the_best(ax, plt, show)
    end_time = time.time()
    gamma9_policy_time.append(end_time-start_time)
    gamma9_policy_iterations.append(mdp_p.used_iterations)
    print("policy done")
    #
    start_time = time.time()
    mdp_v = Value_MDP(map, 0.9)
    plt5 = mdp_v.start_and_got_the_best(ax, plt, show)
    end_time = time.time()
    gamma9_value_time.append(end_time - start_time)
    gamma9_value_iterations.append(mdp_v.used_iterations)
    print("value done")

    start_time = time.time()
    mdp_p = Policy_MDP(map, 0.7)
    plt4 = mdp_p.start_and_got_the_best(ax, plt, show)
    end_time = time.time()
    gamma5_policy_time.append(end_time - start_time)
    gamma5_policy_iterations.append(mdp_p.used_iterations)
    print("policy done")
    #
    start_time = time.time()
    mdp_v = Value_MDP(map, 0.7)
    plt5 = mdp_v.start_and_got_the_best(ax, plt, show)
    end_time = time.time()
    gamma5_value_time.append(end_time - start_time)
    gamma5_value_iterations.append(mdp_v.used_iterations)
    print("value done")
    start_time = time.time()

#
#
#
x = []
for i in sizes:
    x.append(i * 2 + 1)
plt.figure()
plt.plot(x, gamma5_value_time, 'o-', color='r', label='gamma = 0.7 value iteration')
plt.plot(x, gamma5_policy_time, 'o-', color='g', label='gamma = 0.7 policy iteration')
plt.plot(x, gamma9_value_time, 'o-', color='b', label='gamma = 0.9 value iteration')
plt.plot(x, gamma9_policy_time, 'o-', color='orange', label='gamma = 0.9 policy iteration')
plt.xlabel("maze size")
plt.ylabel("FindPathTime")
plt.legend(loc="best")
plt.savefig("./output/gamma_time_compare.png")

plt.figure()
plt.plot(x, gamma5_value_iterations, 'o-', color='r', label='gamma = 0.7 value iteration')
plt.plot(x, gamma5_policy_iterations, 'o-', color='g', label='gamma = 0.7 policy iteration')
plt.plot(x, gamma9_value_iterations, 'o-', color='b', label='gamma = 0.9 value iteration')
plt.plot(x, gamma9_policy_iterations, 'o-', color='orange', label='gamma = 0.9 policy iteration')
plt.xlabel("maze size")
plt.ylabel("iterations")
plt.legend(loc="best")
plt.savefig("./output/gamma_iterations_compare.png")

