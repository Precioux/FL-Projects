BLANK = "_"  # Symbol to represent an empty cell on the tape
tapes = {}


class TuringMachine_1:
    def __init__(self, input_number):
        print('FIRST MACHINE STARTED!')
        # Convert the input number to unary representation
        unary_representation = "1" * input_number
        print(f'Input: {unary_representation}')

        # Initialize the tape with the unary representation
        self.tape = list(unary_representation + "0")
        print(f'Tape: {self.tape}')
        self.tape.extend([BLANK] * 15)  # Extend the tape with blank symbols for working space

        # Define the states
        self.states = {
            "find",  # Find the number and repeat each '1' three times
            "halt"  # Termination state
        }

        # Define the transition function as a dictionary
        self.transitions = {
            ("find", "1"): ("find", "111", "R"),  # Repeat each '1' three times
            ("find", "0"): ("halt", "0", "L")  # End of number, halt
        }

        self.current_state = "find"  # Start with repeating the number
        self.current_position = 0  # Start at the beginning of the tape

    def step(self):
        current_symbol = self.tape[self.current_position]

        print(f'State: {self.current_state}, Sym: {current_symbol} ')
        if (self.current_state, current_symbol) in self.transitions:
            next_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.current_position] = write_symbol  # Write the new symbol(s) on the tape
            print(f'changed tape : {self.tape}')

            # Move the tape head based on the direction
            if direction == "R":
                self.current_position += 1
            elif direction == "L":
                self.current_position -= 1

            self.current_state = next_state  # Update the current state
            return True  # Indicate a successful step
        else:
            return False  # Indicate that the Turing machine has halted

    def run(self):
        while self.step():
            pass  # Keep stepping until the Turing machine halts
        tape_string = "".join(self.tape)  # Convert the tape from a list to a string
        result = tape_string.rstrip("_0")  # Remove trailing '_' and '0' symbols
        tapes['first'] = result
        return result


class TuringMachine_2:
    def __init__(self):
        print('SECOND MACHINE STARTED!')
        # getting input from first machine
        unary_representation = tapes['first']

        # Initialize the tape with the unary representation
        self.tape = list(unary_representation + "0")
        print(f'Tape: {self.tape}')
        self.tape.extend([BLANK] * 15)  # Extend the tape with blank symbols for working space

        # Define the states
        self.states = {
            "find",  # Find the number and repeat each '1' three times
            "halt"  # Termination state
        }

        # Define the transition function as a dictionary
        self.transitions = {
            ("find", "1"): ("find", "1", "R"),  # Repeat each '1' three times
            ("find", "0"): ("halt", "1", "L")  # End of number, halt
        }

        self.current_state = "find"  # Start with repeating the number
        self.current_position = 0  # Start at the beginning of the tape

    def step(self):
        current_symbol = self.tape[self.current_position]
        print(f'State: {self.current_state}, Sym: {current_symbol} ')
        if (self.current_state, current_symbol) in self.transitions:
            next_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.current_position] = write_symbol  # Write the new symbol(s) on the tape
            print(f'changed tape : {self.tape}')

            # Move the tape head based on the direction
            if direction == "R":
                self.current_position += 1
            elif direction == "L":
                self.current_position -= 1

            self.current_state = next_state  # Update the current state
            return True  # Indicate a successful step
        else:
            return False  # Indicate that the Turing machine has halted

    def run(self):
        while self.step():
            pass  # Keep stepping until the Turing machine halts
        tape_string = "".join(self.tape)  # Convert the tape from a list to a string
        result = tape_string.rstrip("_0")  # Remove trailing '_' and '0' symbols
        tapes['second'] = result
        return result


class TuringMachine_3:
    def __init__(self):
        print('THIRD MACHINE STARTED!')
        self.stack = []
        # Initialize the tape
        unary_representation = tapes['second']
        self.tape = [BLANK] + list(unary_representation) + ['&', '1'] + [BLANK]
        print(f"Tape: {self.tape}")

        # Define the states
        self.states = {
            "find",
            "change",
            'reverse',
            'remove',
            "halt",
            'star'
        }

        # Define the transition function as a dictionary
        self.transitions = {
            ('find', BLANK): ('find', BLANK, 'R'),
            ('find', '1'): ('find', '1', 'R'),
            ('find', '&'): ('change', '&', 'R'),
            ('change', '1'): ('change', '1', 'R'),
            ('change', BLANK): ('reverse', BLANK, 'L'),
            ("reverse", '1'): ("reverse", '1', 'L'),
            ("reverse", '&'): ("remove", '&', 'L'),
            ("remove", '1'): ("remove", '1', 'L'),
            ("remove", BLANK): ("star", BLANK, 'R'),
            ('star', '1'): ('find', BLANK, 'R'),
            ('halt', '#'): ('halt', BLANK, 'L')
        }

        self.current_state = "find"
        self.current_position = 0

    def step(self):
        current_symbol = self.tape[self.current_position]
        print(f'State: {self.current_state}, Sym: {current_symbol} ')

        if (self.current_state, current_symbol) in self.transitions:
            next_state = ''
            write_symbol = ''
            direction = ''
            if self.current_state == 'find' and current_symbol == '1':
                self.stack.append(1)
                next_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
                self.tape[self.current_position] = write_symbol  # Write the new symbol on the tape

            elif self.current_state == 'change' and current_symbol == '1':
                if len(self.stack) > 0:
                    for i in range(len(self.stack)):
                        write_symbol += '1'
                    next_state, w, direction = self.transitions[(self.current_state, current_symbol)]
                    self.tape[self.current_position] = write_symbol
                else:
                    next_state = 'halt'
                    write_symbol = '#'
                    direction = 'L'


            elif self.current_state == 'change' and current_symbol == BLANK:
                index = 0
                tape_copy = self.tape.copy()
                for i in tape_copy:
                    if len(i) == 1:
                        index += 1
                    else:
                        l = []
                        for o in i:
                            l.append('1')
                        head = self.tape[:index]
                        tail = self.tape[index + 1:]
                        self.tape.clear()
                        self.tape = head + l + tail
                        index += len(i)

                self.stack.clear()
                self.current_position = len(self.tape) - 1
                next_state, w, direction = self.transitions[(self.current_state, current_symbol)]
            else:
                next_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
                self.tape[self.current_position] = write_symbol  # Write the new symbol on the tape

            print(f'changed tape : {self.tape}')

            # Move the tape head based on the direction
            if direction == "R":
                self.current_position += 1
            elif direction == "L":
                self.current_position -= 1

            self.current_state = next_state
            return True  # Indicate a successful step
        else:
            return False  # Indicate that the Turing machine has halted

    def run(self):
        while self.step():
            pass  # Keep stepping until the Turing machine halts

        tape_string = self.tape
        r = []
        for i in self.tape:
            if i == '1':
                r.append(i)
        result = "".join(r)  # Convert the tape from a list to a string
        return result


def run_machine(input_number):
    global tapes
    tapes.clear()
    # 3 * n
    tm1 = TuringMachine_1(input_number)
    result1 = tm1.run()
    print("Result 3 * n:", result1)
    print('*********************************************************************************')
    # 3 * n + 1
    tm2 = TuringMachine_2()
    result2 = tm2.run()
    print(f'Result 3 * n + 1 : {result2}')
    print('*********************************************************************************')
    # (3n+1)!
    tm3 = TuringMachine_3()
    result3 = tm3.run()
    print(f'Result final : {result3}')
    print(f'Cause its hard to count 1s! decimal is {len(result3)}')
    print('*********************************************************************************')


if __name__ == '__main__':
    flag = True
    while flag:
        n = input('Enter number : ')
        run_machine(int(n))
        c = input('If you want to continue enter 1 else 0: ')
        cont = int(c)
        if cont == 0:
            flag = False
