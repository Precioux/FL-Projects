class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        # Initialize the NFA with its states, alphabet, transitions, start state, and accept states
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def lambda_closure(self, states):
        # Compute the lambda closure of a set of states in the NFA
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            lambda_transitions = self.transitions.get((state, 'lambda'))

            if lambda_transitions:
                for epsilon_state in lambda_transitions:
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
        return closure

    def move(self, states, symbol):
        # Compute the set of states reachable from a set of states with a given symbol
        move_states = set()
        for state in states:
            symbol_transitions = self.transitions.get((state, symbol))
            if symbol_transitions:
                move_states.update(symbol_transitions)

        return move_states

    def convert_lambda_nfa_to_nfa(self):
        # Convert the lambda-NFA to an NFA by computing epsilon closures and transitions
        new_transitions = {}
        new_accept_states = set()

        for state in self.states:
            lambda_closure = self.lambda_closure({state})

            for symbol in self.alphabet:
                move_states = self.move(lambda_closure, symbol)
                new_transitions[(state, symbol)] = move_states

            if any(state in self.accept_states for state in lambda_closure):
                new_accept_states.add(state)

        return NFA(self.states, self.alphabet, new_transitions, self.start_state, new_accept_states)


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        # Initialize the DFA with its states, alphabet, transitions, start state, and accept states
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def to_dfa(self, nfa):
        # Convert an NFA to a DFA by computing epsilon closures and transitions
        dfa_states = set()
        dfa_start_state = frozenset(nfa.lambda_closure({nfa.start_state}))
        dfa_states.add(dfa_start_state)
        dfa_transitions = {}
        dfa_accept_states = []

        stack = [dfa_start_state]

        while stack:
            current_states = stack.pop()

            for symbol in nfa.alphabet:
                move_states = set()
                for state in current_states:
                    move_states.update(nfa.transitions.get((state, symbol), set()))

                epsilon_closure = set()
                for move_state in move_states:
                    epsilon_closure.update(nfa.lambda_closure({move_state}))

                if epsilon_closure and epsilon_closure not in dfa_states:
                    dfa_states.add(frozenset(epsilon_closure))
                    stack.append(frozenset(epsilon_closure))

                dfa_transitions[(current_states, symbol)] = frozenset(epsilon_closure)

        for dfa_state in dfa_states:
            if any(state in nfa.accept_states for state in dfa_state):
                dfa_accept_states.append(dfa_state)

        dfa_states = [state for state in dfa_states]

        return DFA(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)


def parse_nfa_input(filename):
    # Parse the input file to create an NFA object
    with open(filename, 'r') as file:
        lines = file.readlines()

    alphabet = lines[0].split()
    states = lines[1].split()
    start_state = lines[2].strip()
    accept_states = lines[3].split()

    transitions = {}
    for line in lines[4:]:
        parts = line.split()
        current_state = parts[0]
        s = parts[1]
        if s in alphabet:
            symbol = s
        else:
            symbol = 'lambda'
        next_states = parts[2:]
        transitions.setdefault((current_state, symbol), set()).update(next_states)

    return NFA(states, alphabet, transitions, start_state, accept_states)


def write_dfa_output(dfa, filename):
    # Write the DFA object to the output file
    with open(filename, 'w') as file:
        file.write(' '.join(dfa.alphabet) + '\n')
        file.write(' '.join(str(sorted(state)) for state in dfa.states) + '\n')
        file.write(str(sorted(dfa.start_state)) + '\n')
        file.write(' '.join(str(sorted(state)) for state in dfa.accept_states) + '\n')
        for (current_states, symbol), next_state in dfa.transitions.items():
            current_states_str = ', '.join(sorted(state for state in current_states))
            next_state_str = ', '.join(sorted(state for state in next_state))
            file.write(f'[ {current_states_str} ] {str(symbol)}  [ {next_state_str} ]\n')


def main():
    # Main program execution
    nfa_filename = 'NFA_Input_2.txt'
    dfa_filename = 'DFA_Output_2.txt'

    # Parse the NFA input file
    nfa = parse_nfa_input(nfa_filename)

    # Convert the lambda-NFA to an NFA
    nfa = nfa.convert_lambda_nfa_to_nfa()

    # Create an empty DFA object
    dfa = DFA([], nfa.alphabet, {}, '', [])

    # Convert the NFA to a DFA
    dfa = dfa.to_dfa(nfa)

    # Write the DFA output to a file
    write_dfa_output(dfa, dfa_filename)


if __name__ == '__main__':
    main()
