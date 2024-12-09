import csv
from collections import defaultdict

class KTapeTuringMachine:
    def __init__(self, title, num_tapes, states, transitions, start_state, accept_state, reject_state):
        self.title = title
        self.num_tapes = num_tapes
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.tapes = [["_"] for _ in range(num_tapes)]  # Initialize tapes with blank symbols
        self.head_positions = [0] * num_tapes  # Initialize head positions
        self.current_state = start_state

    def run(self, input_string):
        # Load input string onto the first tape
        self.tapes[0] = list(input_string) + ["_"]
        self.head_positions = [0] * self.num_tapes
        
        print(" ")
        print(f"Running Turing Machine: {self.title}")
        while self.current_state != self.accept_state and self.current_state != self.reject_state:
            print(f"\nState: {self.current_state}")
            print(f"Head positions: {self.head_positions}")
            for i, tape in enumerate(self.tapes):
                tape_view = "".join(tape)
                print(f"Tape {i+1}: {tape_view} (Head at {self.head_positions[i]})")

            # Get current symbols under each tape head
            current_symbols = tuple(
                self.tapes[i][self.head_positions[i]] if self.head_positions[i] < len(self.tapes[i]) else "_"
                for i in range(self.num_tapes)
            )
            print(f"Current symbols: {current_symbols}")

            # Look up the transition
            key = (self.current_state, *current_symbols)
            if key not in self.transitions:
                print(f"No transition found for {key}. Halting.")
                break

            new_state, writes, moves = self.transitions[key]
            print(f"Transition: {key} -> {new_state}, writes: {writes}, moves: {moves}")

            # Write symbols and move tape heads
            for i in range(self.num_tapes):
                # Write the symbol
                if self.head_positions[i] < len(self.tapes[i]):
                    self.tapes[i][self.head_positions[i]] = writes[i]
                else:
                    self.tapes[i].append(writes[i])

                # Move the head
                if moves[i] == "R":
                    self.head_positions[i] += 1
                elif moves[i] == "L":
                    self.head_positions[i] = max(0, self.head_positions[i] - 1)

            self.current_state = new_state

        if self.current_state == self.accept_state:
            print("Input accepted!")
        elif self.current_state == self.reject_state:
            print("Input rejected!")
        else:
            print("Machine halted unexpectedly. The string is not be in the language! :(")

def parse_csv_to_turing_machine(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)

    # Parse title and number of tapes
    title, num_tapes = lines[0][0].strip('"[]'), int(lines[0][1].strip('"[]'))  # Example: ["Fast binary palindrome", 2] 
    num_tapes = int(num_tapes)

    # Parse states and transitions
    states = set()
    transitions = defaultdict(tuple)
    start_state = None
    accept_state = None
    reject_state = None
    
    # This is where you explicitly set the start state to line 5 (line index 4)
    if len(lines) > 4:
        start_state = lines[4][0].strip()  # Set start state to the state on line 5

    for line in lines[1:]:
        # Skip empty or incomplete lines
        if not line or len(line) == 0:
            continue
        
        # Check for standalone state declarations
        if len(line) == 1:
            state = line[0].strip()
            if state.startswith("qAccept"):
                accept_state = state
            elif state.startswith("qReject"):
                reject_state = state
            elif not start_state:
                start_state = state
            states.add(state)
        elif len(line) >= 2 + 3 * num_tapes:  # Transition line
            current_state = line[0].strip()
            read_symbols = tuple(symbol.strip() for symbol in line[1:1 + num_tapes])
            new_state = line[1 + num_tapes].strip()
            write_symbols = tuple(symbol.strip() for symbol in line[2 + num_tapes:2 + 2 * num_tapes])
            moves = tuple(symbol.strip() for symbol in line[2 + 2 * num_tapes:])
            transitions[(current_state, *read_symbols)] = (new_state, write_symbols, moves)
        
    return KTapeTuringMachine(title, num_tapes, states, transitions, start_state, accept_state, reject_state)

# Example usage of palindromic: Has 2 tape problem solver
filename = "k_tape_palindromic_DTM.csv"
input_string = "$10101"  # Example input that accepts, dollar sign required in front to know where beginning of tape is.
#input_string = "$10100"  # Example input that rejects,

# Example usage of 1^+: Shows that the k tape machine works with only 1 tape
#filename = "k_tape_0_plus_DTM.csv"
#input_string = "00"  # Example input that accepts
#input_string = "0011"  # Example input that rejects

machine = parse_csv_to_turing_machine(filename)
machine.run(input_string)