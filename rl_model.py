import numpy as np
import random

class StudySchedulerRL:
    def __init__(self, num_subjects, num_days):
        self.num_subjects = num_subjects
        self.num_days = num_days
        self.q_table = np.zeros((num_days, num_subjects))  # Q-table for states (days) and actions (subjects)
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.num_subjects - 1)  # Explore
        return np.argmax(self.q_table[state])  # Exploit

    def update(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state, action] += self.alpha * (
            reward + self.gamma * self.q_table[next_state, best_next_action] - self.q_table[state, action]
        )