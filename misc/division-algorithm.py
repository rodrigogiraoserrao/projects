"""
Divides `dividend` by `divisor` and writes it out in a nice way to be used
in the pt-pt (European Portuguese) translations of Khan Academy.

Author: Rodrigo Girão Serrão
Date: 31-01-2020
"""

dividend = 2000
divisor = 3

dividend_str = str(dividend)
dividend_length = len(dividend_str)
divisor_str = str(divisor)
quotient = dividend // divisor
quotient_str = str(quotient)

header = r"$\begin{align*}" + "\n" + r"& \hphantom{0}" + dividend_str + r"\,\,\underline{|\," + divisor_str + r"\hphantom{" + "0"*(dividend_length+1) + r"}}"
footer = r"\end{align*}$"

# Iteratively add two lines to the body of the algorithm
power_offset = dividend_length - 1
printing_offset = 1
next_digit = dividend // pow(10, power_offset)
left = dividend % pow(10, power_offset)
diff = 0
using = 10*diff + next_digit
built_quotient = ""
body = []
while True:
    q = using // divisor
    built_quotient += str(q)
    subtract = q*divisor
    diff = using - subtract

    if power_offset:
        new_digit = left // pow(10, power_offset-1)
    else:
        new_digit = ""

    blank_offset = len(str(using)) - len(str(subtract))
    first_line = r"& \underline{ \hphantom{" + "0"*printing_offset + r"} \llap{-}" + "0"*blank_offset + str(subtract) + r"}"
    if new_digit != "":
        first_line += r" \!\downarrow"


    print("Want to get new digit")
    print(f"left: {left}")
    print(f"using: {using}")
    print(f"new digit: {new_digit}")
    print(f"power offset: {power_offset}")
    print(f"print offset: {printing_offset}")

    zero_offset = len(str(using)) - len(str(diff))
    second_line = r"& \hphantom{" + "0"*printing_offset + r"}" + "0"*zero_offset + f"{diff}" + str(new_digit)
    body.append(first_line)
    body.append(second_line)

    printing_offset += zero_offset
    printing_offset += (diff == 0)
    power_offset -= 1

    if power_offset == -1:
        break

    using = diff*10 + new_digit
    left %= pow(10, power_offset)

    print("#"*30)

# Add the quotient to the first line of the algorithm
body[0] += r"\hphantom{" + "0"*(dividend_length - 2) + r"} \,\,\," + built_quotient

print(
    header + r"\\" + "\n" + "\\\\\n".join(body) + r"\\" + "\n" + footer
)