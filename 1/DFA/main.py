class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        # Initialize the DFA object with states, alphabet, transitions, start state, and accept states
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        # Check if the DFA accepts the given input string
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet:
                return False
            # Transition to the next state based on the current state and input character
            current_state = self.transitions.get((current_state, char))
            if current_state is None:
                return False
        return current_state in self.accept_states


def parse_dfa_input(filename):
    # Parse the DFA input from a file
    with open(filename, 'r') as file:
        lines = file.readlines()

    alphabet = lines[0].split()          # Read the alphabet from the first line
    states = lines[1].split()            # Read the states from the second line
    start_state = lines[2].strip()       # Read the start state from the third line
    accept_states = lines[3].split()     # Read the accept states from the fourth line

    transitions = {}
    for line in lines[4:]:
        parts = line.split()
        transitions[(parts[0], parts[1])] = parts[2]
        # Create a dictionary of transitions with (current_state, input_char) as the key and the next state as the value

    return DFA(states, alphabet, transitions, start_state, accept_states)


def main():
    dfa_filename = 'DFA_Input_1.txt'
    dfa = parse_dfa_input(dfa_filename)

    input_string = input('Enter a string: ')
    if dfa.accepts(input_string):
        print('Accepted')
    else:
        print('Not accepted')


if __name__ == '__main__':
    main()
