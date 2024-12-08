import csv

class NDTuringMachineK:
    def __init__(self, name, states, sigma, gamma, start_state, accept_state, reject_state, k):
        self.name = name
        self.states = states
        self.sigma = sigma
        self.gamma = gamma
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.k = k # number of k tapes
        self.transitions = {}  # Transition function 

    def trace(self, input_strings, max_steps=1000):
        """Trace the behavior of the k-tape NDTM."""
        
        
        tapes = [list(input_string) for input_string in input_strings]
        head_positions = [0] * self.k
        configurations = [(self.start_state, tapes, head_positions, 0)]  # (state, tapes, head_positions)
        
        transition_count = 0  # Total number of transitions
        max_depth = 0  # Max depth reached during the computation
        found_accept = False
        accept_depth = 0
        
        # Echo the machine's name and initial configuration
        print(f"Machine: {self.name}")
        print(f"Initial string: {input_strings}")
        print("Depth of the tree: ", end="")
        
        # List to store the output in the required format
        output = []
        
        while configurations:
            next_configurations = []
            for state, tapes, heads in configurations:
                # Store the current configuration as part of the output
                output.append([["".join(tape)] for tape in tapes])
                
                if state == self.accept_state:
                    output.append([["".join(tape)] for tape in tapes] + [["qacc", "_", "L"]])
                    return output
                if state == self.reject_state:
                    continue
                
                # Get the symbol under the head, or use '_' if beyond the tape
                read_symbols = [tapes[i][heads[i]] if heads[i] < len(tapes[i]) else '_' for i in range(self.k)]
                key = (state, tuple(read_symbols))
                
                # Check for valid transitions
                if key in self.transitions:
                    for transition in self.transitions[key]:
                        next_state, write_symbols, directions = transition
                        new_tapes = [tape[:] for tape in tapes]
                        new_heads = heads[:]

                        # Update tapes and head positions
                        for i in range(self.k):
                            # Write symbol
                            if new_heads[i] < len(new_tapes[i]):
                                new_tapes[i][new_heads[i]] = write_symbols[i]
                            elif new_heads[i] == len(new_tapes[i]):
                                new_tapes[i].append(write_symbols[i])  # Append when head is at the end
                            
                            # Move head
                            if directions[i] == 'R':
                                new_heads[i] += 1
                            elif directions[i] == 'L':
                                new_heads[i] = max(0, new_heads[i] - 1)

                        # Add new configuration
                        next_configurations.append((next_state, new_tapes, new_heads))

            configurations = next_configurations

        output.append([["".join(tape[i]) for i in range(self.k)] for tape in tapes] + [["qrej", "_", "L"]])
        return output

def load_k_tape_machine_from_csv(file_path, k):
    """Load k-tape configuration and transitions from a single CSV file."""
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
        
        # Initialize the k-tape Turing machine
        ndtm = NDTuringMachineK(name, states, sigma, gamma, start_state, accept_state, reject_state, k)


        # Extract transitions (from line 8 onwards)
        for row in lines[7:]:
            if len(row) < 2 + 3 * k:  # Skip invalid rows
                continue
            current_state = row[0]
            read_symbols = tuple(row[1:k + 1])
            next_state = row[k + 1]
            write_symbols = tuple(row[k + 2:2 * k + 2])
            directions = row[2 * k + 2:3 * k + 2]

            key = (current_state, read_symbols)
            if key not in ndtm.transitions:
                ndtm.transitions[key] = []
            ndtm.transitions[key].append((next_state, write_symbols, directions))

        return ndtm


# Example usage for an a^+ k-tape machine:
csv_file_with_k_tape_transitions = "k_tape_a_plus_DTM.csv"
k = 2  # Number of tapes



input_strings = ["aaa","_"]  # Example of accepted
#input_strings = ["aaaaaaaaaaaaaaaaabaaaaa","_"] # Example of rejected 
#ndtm_k.trace(input_strings)

# Example usage for an palindromic:
#csv_file_with_k_tape_transitions = "k_tape_palindromic_DTM.csv"
#k = 2  # Number of tapes

#input_strings = ["10101","_"]  # Example of accepted
#input_strings = ["10100","_"] # Example of rejected 

ndtm_k = load_k_tape_machine_from_csv(csv_file_with_k_tape_transitions, k)
output = ndtm_k.trace(input_strings)

# Print the output
for step in output:
    print(step)
