import csv

class NDTuringMachine:
    def __init__(self, name, states, sigma, gamma, start_state, accept_state, reject_state):
        self.name = name
        self.states = states
        self.sigma = sigma
        self.gamma = gamma
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = {}  # Transition function (e.g., {('q1', '0'): [('q2', '1', 'R'), ...]})

    def load_transitions(self, transitions_file):
        """Load transitions from a CSV file."""
        with open(transitions_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 5:
                    continue
                current_state, read_symbol, next_state, write_symbol, direction = row
                key = (current_state, read_symbol)
                if key not in self.transitions:
                    self.transitions[key] = []
                self.transitions[key].append((next_state, write_symbol, direction))

    def trace(self, input_string):
        """Trace the behavior of the NDTM."""
        configurations = [(self.start_state, input_string, 0)]  # (state, tape, head_position)
        while configurations:
            next_configurations = []
            for state, tape, head in configurations:
                if state == self.accept_state:
                    print("Accepted:", tape)
                    return True
                if state == self.reject_state:
                    continue
                
                read_symbol = tape[head] if head < len(tape) else '_'
                if (state, read_symbol) in self.transitions:
                    for next_state, write_symbol, direction in self.transitions[(state, read_symbol)]:
                        new_tape = list(tape)
                        if head < len(new_tape):
                            new_tape[head] = write_symbol
                        else:
                            new_tape.append(write_symbol)
                        
                        new_head = head + (1 if direction == 'R' else -1)
                        new_head = max(new_head, 0)  # Prevent negative head position
                        next_configurations.append((next_state, ''.join(new_tape), new_head))
            
            configurations = next_configurations
        
        print("Rejected:", input_string)
        return False

def load_machine_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = [line for line in reader]
        name = lines[0][0]
        states = lines[1]
        sigma = lines[2]
        gamma = lines[3]
        start_state = lines[4][0]
        accept_state = lines[5][0]
        reject_state = lines[6][0]
        return NDTuringMachine(name, states, sigma, gamma, start_state, accept_state, reject_state)

# Example usage:
# Assuming CSV format as described and transition rules in "transitions.csv"
csv_file = "ndtm_config.csv"
transitions_file = "transitions.csv"

ndtm = load_machine_from_csv(csv_file)
ndtm.load_transitions(transitions_file)

input_string = "110"
ndtm.trace(input_string)
        