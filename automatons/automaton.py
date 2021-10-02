import random


class Automaton:
    """Class that represents a finite state automaton."""

    def __init__(self, state_transitions, terminal_states):
        """Initialises a finite state automaton.

        `state_transitions` is a dictionary representing the state transitions
        and `terminal_states` is a container that holds all the terminal states,
        in such a way that `state in terminal_states` should be able to check
        if a state is a terminal state.

        The `(key, value)` pairs of the dictionary represent the state transitions
        of the automaton in the following format:
         - `key` is a state of the automaton.
         - `value` is a list of pairs `(actions, next_state)`,
         where `actions` is a sequence of actions that take the automaton
         to the state indicated by `next_state`.
        """

        self._state_transitions = state_transitions
        self._terminal_states = terminal_states
        self._count_terminal_paths_cache = {}

    def is_terminal(self, state):
        """Returns whether `state` is a terminal state for the automaton or not."""
        return state in self._terminal_states

    def count_terminal_paths(self, state):
        """Counts how many paths go from `state` to any terminal state."""
        if state not in self._count_terminal_paths_cache:
            acc = int(self.is_terminal(state))
            for actions, next_state in self._state_transitions.get(state, []):
                acc += len(actions) * self.count_terminal_paths(next_state)
            self._count_terminal_paths_cache[state] = acc
        return self._count_terminal_paths_cache[state]

    def walk_random_path(self, state):
        """Generate a random action path through the automaton state space."""
        if self.is_terminal(state):
            return

        transitions = self._state_transitions.get(state, [])
        weights = [len(a) * self.count_terminal_paths(s) for a, s in transitions]
        next_state_index = random.choices(range(len(transitions)), weights)[0]
        # Yield a random action that would take us to the next state.
        yield random.choice(transitions[next_state_index][0])
        # Yield the remainder of the random path.
        yield from self.walk_random_path(transitions[next_state_index][1])


if __name__ == "__main__":
    transitions = {
        0: [("ab", 1)],
        1: [("ab", 2)],
        2: [("ab", 3)],
        3: [],
    }
    terminal_states = [1, 2, 3]
    automaton = Automaton(transitions, terminal_states)
    print(automaton.count_terminal_paths(0))
    print(automaton._count_terminal_paths_cache)
