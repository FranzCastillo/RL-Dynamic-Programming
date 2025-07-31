import random
from obj.maze import Maze

class MDP_Solver:
    def __init__(self, maze: Maze, gamma=0.9, theta=0.001):
        self.maze = maze
        self.gamma = gamma
        self.theta = theta
        self.V = {s: 0 for s in self.maze.states}
        self.policy = {s: random.choice(self.maze.actions) for s in self.maze.states}

    def value_iteration(self):
        while True:
            delta = 0
            for s in self.maze.states:
                if self.maze.is_terminal(s):
                    continue
                v = self.V[s]
                self.V[s] = max(
                    sum(self.maze.P[s][a][s2] * (self.maze.R[s][a][s2] + self.gamma * self.V[s2])
                        for s2 in self.maze.P[s][a])
                    for a in self.maze.actions
                )
                delta = max(delta, abs(v - self.V[s]))
            if delta < self.theta:
                break
        return self.V

    def extract_policy(self):
        policy = {}
        for s in self.maze.states:
            if self.maze.is_terminal(s):
                policy[s] = None
                continue
            best_a = max(
                self.maze.actions,
                key=lambda a: sum(
                    self.maze.P[s][a][s2] * (self.maze.R[s][a][s2] + self.gamma * self.V[s2])
                    for s2 in self.maze.P[s][a]
                )
            )
            policy[s] = best_a
        return policy

    def policy_iteration(self):
        policy_stable = False
        while not policy_stable:
            # Evaluar política
            self.evaluate_policy()
            policy_stable = True
            for s in self.maze.states:
                if self.maze.is_terminal(s):
                    continue
                old_action = self.policy[s]
                new_action = max(
                    self.maze.actions,
                    key=lambda a: sum(
                        self.maze.P[s][a][s2] * (self.maze.R[s][a][s2] + self.gamma * self.V[s2])
                        for s2 in self.maze.P[s][a]
                    )
                )
                if old_action != new_action:
                    policy_stable = False
                self.policy[s] = new_action
        return self.policy

    def evaluate_policy(self):
        while True:
            delta = 0
            for s in self.maze.states:
                if self.maze.is_terminal(s):
                    continue
                a = self.policy[s]
                v = self.V[s]
                self.V[s] = sum(
                    self.maze.P[s][a][s2] * (self.maze.R[s][a][s2] + self.gamma * self.V[s2])
                    for s2 in self.maze.P[s][a]
                )
                delta = max(delta, abs(v - self.V[s]))
            if delta < self.theta:
                break
