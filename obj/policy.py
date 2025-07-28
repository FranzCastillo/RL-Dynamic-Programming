import random

class Policy:
    def __init__(self):
        # Política ajustada al nuevo grid:
        self.policy = {
            0: 'DOWN',  # 0 → 3
            1: 'LEFT',  # 1 → 0 (2 está bloqueado)
            2: 'LEFT',  # bloqueado, pero por si acaso
            3: 'DOWN',  # 3 → 6
            4: 'LEFT',  # bloqueado
            5: 'DOWN',  # 5 → 8 (meta)
            6: 'RIGHT',  # 6 → 7
            7: 'RIGHT',  # 7 → 8
            8: 'UP'  # GOAL
        }

    def action(self, state):
        return self.policy.get(
            state,
            random.choice(list(self.policy.values()))
        )

    def print_policy(self):
        print("Política π (estado → acción):\n")
        for s in sorted(self.policy):
            print(f"  Estado {s}: '{self.policy[s]}'", end="\n\n")
