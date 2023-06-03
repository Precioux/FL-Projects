import re

class NFA:
  def __init__(self):
    self.alphabet = set()
    self.states = set()
    self.start_state = None
    self.final_states = set()
    self.transitions = {}

  def add_symbol(self, symbol):
    self.alphabet.add(symbol)

  def add_state(self, state):
    self.states.add(state)

  def set_start_state(self, state):
    self.start_state = state

  def add_final_state(self, state):
    self.final_states.add(state)

  def add_transition(self, source_state, symbol, target_state):
    if source_state not in self.transitions:
      self.transitions[source_state] = {}
    self.transitions[source_state][symbol] = target_state

  def accepts(self, string):
    current_state = self.start_state
    for symbol in string:
      if symbol not in self.transitions[current_state]:
        return False
      current_state = self.transitions[current_state][symbol]
    return current_state in self.final_states

def read_dfa(filename):
  with open(filename, "r") as f:
    alphabet = f.readline().split()
    regular_expression = f.readline()

  nfa = NFA()
  nfa.alphabet = alphabet

  # Create states
  for state in range(1, len(regular_expression) + 1):
    nfa.add_state(state)

  # Create starting state
  nfa.set_start_state(1)

  # Create final states
  for match in re.finditer(r"(?<=^)\w+", regular_expression):
    nfa.add_final_state(int(match.group()))

  # Create state transitions
  for i in range(len(regular_expression) - 1):
    if regular_expression[i] == regular_expression[i + 1]:
      nfa.add_transition(i + 1, i + 1, i + 1)
    else:
      nfa.add_transition(i + 1, i + 2, i + 2)

  return nfa

def write_nfa(nfa, filename):
  with open(filename, "w") as f:
    f.write(" ".join(nfa.alphabet) + "\n")
    f.write(" ".join(str(state) for state in nfa.states) + "\n")
    f.write(str(nfa.start_state) + "\n")
    f.write(" ".join(str(state) for state in nfa.final_states) + "\n")
    for state in nfa.states:
      for symbol in nfa.alphabet:
        f.write(str(state) + " " + symbol + " " + str(nfa.transitions[state][symbol]) + "\n")

if __name__ == "__main__":
  nfa = read_dfa("RE_Input_3.txt")
  write_nfa(nfa, "NFA_Output3.txt")
