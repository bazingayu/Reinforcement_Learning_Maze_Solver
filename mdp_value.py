'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: mdp_value.py
@time: 2023/3/11 14:33
'''

import numpy as np
from tqdm import tqdm
from matplotlib.patches import Rectangle
class Value_MDP:
    def __init__(self, map, gamma=0.7):
        self.map = map
        self.line_num = self.map.size   # 11
        self.state_size = self.line_num**2  # 121
        self.state = np.arange(self.state_size) # 121个状态
        self.actions = np.arange(4)   # 4个方向
        self.rewards=-1*np.ones(self.state_size)  # 121个奖惩函数
        self.rewards[-self.line_num-2] = 0   # 终点的是0
        self.gamma = gamma
        self.random_policy = 2 * np.ones(self.state_size)
        self.num_iteration = 1000
        self.mapping = []
        self.used_iterations = 0
        self.value_table = np.zeros(self.state_size)
        for i in range(self.line_num):
            for j in range(self.line_num):
                self.mapping.append([i, j])


    def p_state_reward(self, state, action):
        # define the state action transfer, give the current state and action, return the transfer probability, next state and the reward
        # move up
        if action  == 0:
            # can't move in the first line
            if state in range(self.line_num): # 第一行不能往上移动
                return ((1, state, -1))
            elif self.map.grid[self.mapping[state-self.line_num][0], self.mapping[state-self.line_num][1]] == 1:
                return ((1, state, -1))
            else:
                return ((1, state-self.line_num, -1))

        # move down
        if action == 2:
            # the last row don't move
            if state in range(self.state_size - self.line_num, self.state_size):
                return ((1, state, -1))
            elif state == self.state_size - self.line_num - 2:
                #it can rechieve the end point
                return ((1, self.state_size-1, 0))
            elif self.map.grid[self.mapping[state+self.line_num][0], self.mapping[state+self.line_num][1]] == 1:
                return ((1, state, -1))
            else:
                return ((1, state+self.line_num, -1))
        # move left
        if action == 3:
            if state in np.arange(0, self.state_size, self.line_num):
                return ((1, state, -1))
            elif self.map.grid[self.mapping[state-1][0], self.mapping[state-1][1]] == 1:
                return ((1, state, -1))
            else:
                return((1, state-1, -1))
        # move right
        if action == 1:
            if(state in np.arange(self.line_num-1, self.state_size+self.line_num-1, self.line_num)):
                return ((1, state, -1))
            if state == self.state_size - self.line_num- 2:
                return((1, self.state_size-1, 0))
            elif self.map.grid[self.mapping[state+1][0], self.mapping[state+1][1]] == 1:
                return ((1, state, -1))
            else:
                return((1, state+1, -1))


    def value_iteration(self, value_table, gamma, n):
        threshold = 1e-20
        policy = np.zeros(self.state_size)
        for i in range(n):
            update_value_table = np.copy(value_table)
            for state in self.state:
                action_value = np.zeros(len(self.actions))
                for action in self.actions:
                    trans_prob, next_state, reward = self.p_state_reward(state, action)
                    action_value[action] = reward + gamma * trans_prob * update_value_table[next_state]
                value_table[state] = max(action_value)
                policy[state] = np.argmax(action_value)

            if np.sum((np.fabs(update_value_table-value_table))) <= threshold:
                self.used_iterations = i+1
                print(f"iteration end, iterations = {i+1}")
                break
        return policy


    def start_and_got_the_best(self, ax, plt, show=False):
        best_policy_value = self.value_iteration(self.value_table, self.gamma, self.num_iteration)
        # the best route, the start position in the second row
        best_route_value = [self.line_num+1]
        next_state = self.line_num+1
        while True:
            # 通过最佳策略求解当前状态下执行最优动作所转移到的下一个状态
            _, next_state, _ = self.p_state_reward(next_state, best_policy_value[next_state])

            # put the next state in the best route
            best_route_value.append(next_state)

            # the last position
            if next_state == self.state_size-self.line_num-2:
                break
        if show:
            for i in best_route_value:
                rec = Rectangle((self.mapping[i][0], self.mapping[i][1]), 1, 1, color='g')
                ax.add_patch(rec)
                plt.draw()

            plt.title("mdp_value_output", y=-0.03)
            plt.show()
            plt.savefig("output/mdp_value_output.png")
        return plt




