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

def load_machine_from_csv_with_transitions(file_path):
    """Load NDTM configuration and transitions from a single CSV file."""
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = [line for line in reader]
        
        # Extract machine configuration
        name = lines[0][0]
        states = lines[1]
        sigma = lines[2]
        gamma = lines[3]
        start_state = lines[4][0]
        accept_state = lines[5][0]
        reject_state = lines[6][0]
        
        # Initialize the Turing machine
        ndtm = NDTuringMachine(name, states, sigma, gamma, start_state, accept_state, reject_state)
        
        # Extract transitions (from line 8 onwards)
        for row in lines[7:]:
            if len(row) < 5:  # Skip invalid rows
                continue
            current_state, read_symbol, next_state, write_symbol, direction = row
            key = (current_state, read_symbol)
            if key not in ndtm.transitions:
                ndtm.transitions[key] = []
            ndtm.transitions[key].append((next_state, write_symbol, direction))
        
        return ndtm

# Example usage:
csv_file_with_transitions = "a_plus_DTM.csv"

ndtm = load_machine_from_csv_with_transitions(csv_file_with_transitions)

input_string = "aaa"
ndtm.trace(input_string)
