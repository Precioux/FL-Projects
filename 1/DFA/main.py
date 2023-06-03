class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet:
                return False
            current_state = self.transitions.get((current_state, char))
            if current_state is None:
                return False
        return current_state in self.accept_states


def parse_dfa_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    alphabet = lines[0].split()
    states = lines[1].split()
    start_state = lines[2].strip()
    accept_states = lines[3].split()

    transitions = {}
    for line in lines[4:]:
        parts = line.split()
        transitions[(parts[0], parts[1])] = parts[2]

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
