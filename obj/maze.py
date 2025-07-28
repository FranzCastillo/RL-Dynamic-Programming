def get_position(state):
    return state // 3, state % 3


class Maze:
    def __init__(self):
        self.START   = 'S'
        self.GOAL    = 'G'
        self.BLOCKED = 'X'
        self.FREE    = ' '

        self.REWARD_GOAL = 100
        self.REWARD_BLOCKED = -25
        self.REWARD_FREE = 0

        self.grid = [
            [self.START,    self.FREE,    self.BLOCKED],
            [self.FREE,     self.BLOCKED, self.FREE],
            [self.FREE,     self.FREE,    self.GOAL]
        ]

        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.states  = list(range(9))

        self.P = self.build_transition_probabilities()
        self.R = self.build_rewards()

    def is_valid_state(self, row, col):
        return (
                0 <= row < 3 and
                0 <= col < 3 and
                self.grid[row][col] != self.BLOCKED
        )

    def get_next_state(self, state, action):
        row, col = get_position(state)
        if action == 'UP':    row -= 1
        elif action == 'DOWN':   row += 1
        elif action == 'LEFT': col -= 1
        elif action == 'RIGHT':  col += 1

        if self.is_valid_state(row, col):
            return row * 3 + col  # From (x, y) to an idx in self.states
        else:
            return state

    def build_transition_probabilities(self):
        P = {}
        for s in self.states:
            P[s] = {}
            for a in self.actions:
                s_prime = self.get_next_state(s, a)
                P[s][a] = {s_prime: 1.0}  # Probability of moving to s' from s with action a
                # Non-stochastic MDP: deterministic transitions
        return P

    def build_rewards(self):
        R = {}
        for s in self.states:
            R[s] = {}
            for a in self.actions:
                s_prime = self.get_next_state(s, a)  # s'
                cell = self.grid[s_prime // 3][s_prime % 3]  # Get the cell type from the grid (FREE, BLOCKED, START, GOAL)

                if cell == self.GOAL:
                    reward = self.REWARD_GOAL
                elif cell == self.BLOCKED or s_prime == s:
                    reward = self.REWARD_BLOCKED
                else:  # Free cell
                    reward = self.REWARD_FREE

                R[s][a] = {s_prime: reward}
        return R

    def is_terminal(self, state):
        return self.grid[state // 3][state % 3] == self.GOAL

    def print_transition_matrix(self):
        print("Matriz de transición P[s][a]:\n")
        for s in self.states:
            print(f"Estado {s}:")
            for a in self.actions:
                print(f"  '{a}': {self.P[s][a]}", end='\n\n')

    def print_reward_function(self):
        print("Función de recompensa R[s][a][s']:\n")
        for s in self.states:
            print(f"Estado {s}:")
            for a in self.actions:
                for s_prime, r in self.R[s][a].items():
                    print(f"  '{a}' → {s_prime}: {r}", end='\n\n')

