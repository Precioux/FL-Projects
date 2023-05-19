class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def is_accepted(self, input_string):
        current_state = self.start_state

        for char in input_string:
            if char not in self.alphabet:
                return False

            current_state = self.transitions.get((current_state, char))

            if current_state is None:
                return False

        return current_state in self.accept_states


def load_dfa_from_file(file_path):
    with open(file_path, 'r') as file:
        dfa_data = file.read()

    dfa = parse_dfa_data(dfa_data)
    return dfa


def parse_dfa_data(dfa_data):
    dfa_lines = dfa_data.split('\n')

    states = dfa_lines[0].split(': ')[1].split(', ')
    alphabet = dfa_lines[1].split(': ')[1].split(', ')
    start_state = dfa_lines[2].split(': ')[1]
    accept_states = dfa_lines[3].split(': ')[1].split(', ')

    transitions = {}
    for line in dfa_lines[4:]:
        if line:
            source, symbol, destination = line.split(', ')
            transitions[(source, symbol)] = destination

    dfa = DFA(states, alphabet, start_state, accept_states, transitions)
    return dfa


def main():
    dfa_file_path = 'DFA_Input_1.txt'
    input_string = input('Enter a string: ')

    dfa = load_dfa_from_file(dfa_file_path)
    if dfa.is_accepted(input_string):
        print('Accepted')
    else:
        print('Not Accepted')


if __name__ == '__main__':
    main()
