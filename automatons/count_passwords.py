"""
Makes use of finite state automatons to count the number of valid passwords
that satisfy a series of different restrictions, namely:

 - restrictions on minimum and maximum length;
 - restrictions on minimum and maximum usages of several types of characters.
"""

import string
import time
from automaton import Automaton


def generate_next_pwd_states(s):
    return [s[:i] + (num + 1,) + s[i + 1 :] for i, num in enumerate(s)]


def generate_state_transitions(classes, max_length):
    queue = [(0,) * len(classes)]
    state_transitions = {}

    while queue:
        state, *queue = queue
        next_states = generate_next_pwd_states(state) if sum(state) < max_length else []
        state_transitions[state] = list(zip(classes, next_states))
        queue.extend(state_ for state_ in next_states if state_ not in queue)

    return state_transitions


def gather_terminal_states(state_transitions, is_valid_pwd):
    return [s for s in state_transitions if is_valid_pwd(s)]


if __name__ == "__main__":
    # Solve https://math.stackexchange.com/q/2452401/329832,
    # which should give 2,684,483,063,360

    # Configure the password:
    classes = [
        string.ascii_uppercase,
        string.digits,
    ]
    MIN_LENGTH = 6
    MAX_LENGTH = 8
    # Predicates:
    predicates = [
        lambda s: MIN_LENGTH <= sum(s) <= MAX_LENGTH,  # valid length?
        lambda s: s[1],  # has a digit?
    ]
    is_valid_pwd = lambda s: all(pred(s) for pred in predicates)

    state_transitions = generate_state_transitions(classes, MAX_LENGTH)
    terminal_states = gather_terminal_states(state_transitions, is_valid_pwd)

    automaton = Automaton(state_transitions, terminal_states)
    start = time.time()
    print(automaton.count_terminal_paths((0,) * len(classes)))
    elapsed = time.time() - start
    print(f"Counted in {round(elapsed, 4)}s.")
