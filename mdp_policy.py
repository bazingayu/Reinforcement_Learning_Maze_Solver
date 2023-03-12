'''
@author: Junwei Yu
@contact : yuju@tcd.ie
@file: mdp_policy.py
@time: 2023/3/11 12:37
'''
import numpy as np
from tqdm import tqdm
from matplotlib.patches import Rectangle
class Policy_MDP:
    def __init__(self, map, gamma=0.7):
        self.map = map
        self.line_num = self.map.size   # 11
        self.state_size = self.line_num**2  # 121
        self.state = np.arange(self.state_size) # 121
        self.actions = np.arange(4)   # 4
        self.rewards=-1*np.ones(self.state_size)  # 121
        self.rewards[-self.line_num-2] = 0   # endpoint reward
        self.gamma = gamma
        self.random_policy = 2 * np.ones(self.state_size)
        self.num_iteration = 1000
        self.mapping = []
        self.used_iterations = 0
        for i in range(self.line_num):
            for j in range(self.line_num):
                self.mapping.append([i, j])


    def p_state_reward(self, state, action):
        # define the state action transfer, give the current state and action, return the transfer probability, next state and the reward
        # move up
        if action  == 0:
            # can't move in the first line
            if state in range(self.line_num): # the first row can't move up
                return ((1, state, -1))
            elif self.map.grid[self.mapping[state-self.line_num][0], self.mapping[state-self.line_num][1]] == 1: #can't move to the obstacle
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

    def compute_value_function(self, policy, gamma):
        threshold = 1e-10
        value_table=np.zeros(self.state_size)
        while True:
            update_value_table = np.copy(value_table)
            for state in self.state:
                if self.map.grid[self.mapping[state][0], self.mapping[state][1]] == 1:
                    continue
                action = policy[state]
                trans_prob, next_state, reward = self.p_state_reward(state, action)
                value_table[state] = reward + gamma * trans_prob * update_value_table[next_state]
            if np.sum((np.fabs(update_value_table-value_table))) <= threshold:
                break
        return value_table

    def next_best_policy(self, value_table, gamma):
        policy = np.zeros(self.state_size)
        for state in self.state:
            action_table = np.zeros(len(self.actions))
            for action in self.actions:
                trans_prob, next_state, reward = self.p_state_reward(state, action)
                action_table[action] = reward + gamma * trans_prob * value_table[next_state]
            policy[state] = np.argmax(action_table)
        return policy

    def policy_iteration(self, random_policy, gamma, n):
        for i in range(n):
            new_value_function = self.compute_value_function(random_policy, gamma)
            new_policy = self.next_best_policy(new_value_function, gamma)
            if np.all(random_policy == new_policy):
                self.used_iterations = i+1
                print(f"iteration down, {i+1} iterations")
                break
            random_policy = new_policy

        return new_policy

    def start_and_got_the_best(self, ax, plt, show):
        best_policy = self.policy_iteration(self.random_policy, self.gamma, self.num_iteration)
        best_route = [self.line_num+1]
        next_state = self.line_num+1
        while True:
            _, next_state, _ = self.p_state_reward(next_state, best_policy[next_state])

            best_route.append(next_state)

            if next_state == self.state_size-self.line_num-2:
                break
        if show:
            for i in best_route:
                rec = Rectangle((self.mapping[i][0], self.mapping[i][1]), 1, 1, color='g')
                ax.add_patch(rec)
                plt.draw()
            plt.title("mdp_policy_output", y=-0.03)
            plt.show()
            plt.savefig("output/mdp_policy_output.png")
        return plt
