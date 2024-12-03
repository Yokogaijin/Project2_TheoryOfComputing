import csv

class NDTuringMachine:
    def_init_(self, name, states, sigma, gamma, start_state, accept_state, reject_state):
        self.name = name
        self.states = states
        self.sigma = sigma
        self.gamma = gamma
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = {}  # Transition function (e.g., {('q1', '0'): [('q2', '1', 'R'), ...]})
        