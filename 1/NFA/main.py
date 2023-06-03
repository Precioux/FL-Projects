class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            epsilon_transitions = self.transitions.get((state, ''))

            if epsilon_transitions:
                for epsilon_state in epsilon_transitions:
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)

        return closure

    def move(self, states, symbol):
        move_states = set()

        for state in states:
            symbol_transitions = self.transitions.get((state, symbol))
            if symbol_transitions:
                move_states.update(symbol_transitions)

        return move_states


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def to_dfa(self, nfa):
        dfa_states = set()
        dfa_start_state = nfa.epsilon_closure({nfa.start_state})
        dfa_states.add(tuple(sorted(dfa_start_state)))
        dfa_transitions = {}
        dfa_accept_states = []

        stack = [dfa_start_state]

        while stack:
            current_states = stack.pop()
            for symbol in nfa.alphabet:
                move_states = nfa.move(current_states, symbol)
                epsilon_closure = nfa.epsilon_closure(move_states)

                if epsilon_closure not in dfa_states:
                    dfa_states.add(tuple(sorted(epsilon_closure)))
                    stack.append(epsilon_closure)

                dfa_transitions[(tuple(sorted(current_states)), symbol)] = tuple(sorted(epsilon_closure))

        for dfa_state in dfa_states:
            if any(state in nfa.accept_states for state in dfa_state):
                dfa_accept_states.append(dfa_state)

        dfa_states = [state for state in dfa_states]

        return DFA(dfa_states, nfa.alphabet, dfa_transitions, tuple(sorted(dfa_start_state)), dfa_accept_states)


def parse_nfa_input(filename):
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
        symbol = parts[1]
        next_states = parts[2:]
        transitions.setdefault((current_state, symbol), []).extend(next_states)

    return NFA(states, alphabet, transitions, start_state, accept_states)


def write_dfa_output(dfa, filename):
    with open(filename, 'w') as file:
        file.write(' '.join(dfa.alphabet) + '\n')
        file.write(' '.join(dfa.states) + '\n')
        file.write(dfa.start_state + '\n')
        file.write(' '.join(dfa.accept_states) + '\n')
        for (current_state, symbol), next_state in dfa.transitions.items():
            file.write(current_state + ' ' + symbol + ' ' + next_state + '\n')


def main():
    nfa_filename = 'NFA_Input_2.txt'
    dfa_filename = 'DFA_Output_2.txt'

    nfa = parse_nfa_input(nfa_filename)
    dfa = DFA([], nfa.alphabet, {}, '', [])

    dfa = dfa.to_dfa(nfa)

    write_dfa_output(dfa, dfa_filename)


if __name__ == '__main__':
    main()
