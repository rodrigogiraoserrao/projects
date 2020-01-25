#! /usr/bin/python3

import sys

MEM_SIZE = 256

def interpret(code: str) -> (list, int, str, str):
    memory = [0]
    ptr = 0
    inp = input(" (brainfck input) >> ")
    out = ""

    return evaluate(code, memory, ptr, inp, out)

def evaluate(
    code: str, memory: list, ptr: int, inp: str, out: str
) -> (list, int, str, str):
    """Take a partial brainfck program and interpret it."""

    code_ptr = 0
    while code_ptr < len(code):
        char = code[code_ptr]

        if char not in "+-<>[],.":
            code_ptr += 1
            continue

        if char == '+':     # increment memory
            memory[ptr] = (memory[ptr] + 1) % MEM_SIZE

        elif char == '-':   # decrement memory
            memory[ptr] = (memory[ptr] - 1) % MEM_SIZE

        elif char == '>':   # move right on the tape
            ptr += 1
            if ptr >= len(memory):
                memory.append(0)

        elif char == '<':   # move left on the tape
            ptr -= 1
            while ptr < 0:
                memory.insert(0, 0)
                ptr += 1
                
        elif char == ',':   # read one input character
            if inp:
                memory[ptr] = ord(inp[0]) % MEM_SIZE
                inp = inp[1:]
            else:
                memory[ptr] = 0

        elif char == '.':   # output the tape position
            out += chr(memory[ptr])

        elif char == '[':   # enter this code 
            sub_code = ''
            nesting_level = 1
            look_to = code_ptr + 1
            while nesting_level and look_to < len(code):
                if code[look_to] == ']':
                    nesting_level -= 1
                else:
                    sub_code += code[look_to]
                    if code[look_to] == '[':
                        nesting_level += 1

                look_to += 1

            if look_to == len(code):
                raise Exception("Reached brainfck EOF.")
            
            while memory[ptr]:
                memory, ptr, inp, out = evaluate(sub_code, memory, ptr, inp, out)

            code_ptr = look_to - 1

        elif char == ']':
            raise Exception("Unbalanced [] expression.")

        code_ptr += 1

    return memory, ptr, inp, out

if __name__ == "__main__":

    while (s := input(" >> ")):
        memory, ptr, inp, out = interpret(s)

        print(f"""output: '{out}'.
memory layout: {memory}
pointer @ position {ptr}, input left to consume: '{inp}'""")