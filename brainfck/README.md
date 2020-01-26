# Brainf*ck

[Brainf*ck](https://en.wikipedia.org/wiki/Brainfuck) is an esoteric programming language where we program on a tape.

To code in brainf*ck we can move left or right on the tape with `<>`, we can increment or decrement the currenct cell with `+-`, we can read a character to the current (as its ASCII value) or output the character with the ASCII value of the current cell with `,.` and we can loop code within `[]`.

When we reach a `[` we only enter if the current cell is non-zero and when we reach `]` we jump back to the corresponding `[`.

The program `,[.,]` copies the input and outputs it back to the user... [Try it online!](https://tio.run/##SypKzMxLK03O/v9fJ1pPJ/b//8TilDQQVkgshtMK6YlFCkYmpgA)