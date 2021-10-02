"""
Uses the `Automaton` class to generate passwords that are uniformly
distributed amongst all the acceptable passwords.
"""

import string

from automaton import Automaton
from count_passwords import (
    gather_terminal_states,
    generate_next_pwd_states,
    generate_state_transitions,
)


def generate_random_password(length, restriction_info):
    """Generate a random password with the following length.

    The `restriction_info` parameter contains the information regarding
    the restrictions that the password must satisfy.
    This parameter is a dictionary; its keys are the classes of characters
    and the values are pairs (min, max) that state the minimum and maximum
    number of characters of that class that must be present.
    Each of min and max can be `None`, meaning no restrictions apply.
    """

    CLASSES = list(restriction_info.keys())
    # Dynamically create a function that checks if a given state is a terminal state.
    def is_terminal_state(state):
        if sum(state) < length:
            return False

        # A state is terminal if, for all of the given character classes,
        # the number inside the tuple is >= the minimum amount of characters
        # of that class and <= the maximum amount of characters of that class.
        is_terminal = True
        for class_count, class_ in zip(state, CLASSES):
            min_, max_ = restriction_info[class_]
            is_terminal = is_terminal and (
                (min_ is None or min_ <= class_count)
                and (max_ is None or max_ >= class_count)
            )
        return is_terminal

    state_transitions = generate_state_transitions(CLASSES, length)
    terminal_states = gather_terminal_states(
        state_transitions,
        is_terminal_state,
    )

    automaton = Automaton(state_transitions, terminal_states)
    return "".join(automaton.walk_random_path((0,) * len(CLASSES)))


if __name__ == "__main__":
    for _ in range(10):
        print(
            generate_random_password(
                10,
                {
                    string.ascii_lowercase: (1, 2),
                    string.ascii_uppercase: (None, 3),
                    string.digits: (2, None),
                    string.punctuation: (1, None),
                },
            )
        )
