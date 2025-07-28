from obj.maze import Maze
from obj.policy import Policy

class Simulator:
    def __init__(self, maze: Maze, policy: Policy):
        self.maze = maze
        self.policy = policy

    def sample_next_state(self, transitions):
        """
        :param transitions:
        :return: next state sampled from the transition probabilities
        """
        return next(iter(transitions))  # Deterministic -> P=1

    def run_episode(self, max_steps=20, start_state=0):
        state = start_state
        total_reward = 0
        steps = 0

        while not self.maze.is_terminal(state) and steps < max_steps:
            a = self.policy.action(state)
            s2 = self.sample_next_state(self.maze.P[state][a])  # s2 = next state, sample return
            r  = self.maze.R[state][a][s2]

            total_reward += r
            state = s2
            steps += 1

        return total_reward

    def simulate_policy_trace(self, max_steps=20, start_state=0):
        print("Simulación paso a paso:")
        state = start_state
        total_reward = 0
        steps = 0

        while not self.maze.is_terminal(state) and steps < max_steps:
            a  = self.policy.action(state)
            s2 = self.sample_next_state(self.maze.P[state][a])
            r  = self.maze.R[state][a][s2]
            print(f" Paso {steps+1}: {state} --[{a}]--> {s2} | Recompensa = {r}")

            total_reward += r
            state = s2
            steps += 1

        print(f"Recompensa acumulada total: {total_reward}\n")

    def evaluate_policy(self, runs=100):
        rewards = [self.run_episode() for _ in range(runs)]
        return sum(rewards) / len(rewards)