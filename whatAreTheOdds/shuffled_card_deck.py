# What is the probability that, given a completely shuffled deck of 52 cards (13 cards of each suit),
# there are at least two cards of the same value next to each other?
# This script estimates that probability to be 95.45%, which means only 4.55% of the times no two cards of the same value are in a row.

from random import shuffle

cards = [i for i in range(13)] * 4

trials = pow(10, 6)

all_different = 0
two_in_a_row = 0
found = False

# estimate the probability that a thoroughly shuffled deck contains any two cards in a row with the same value
for i in range(trials):
    if 0 == (i % (trials // 100)):
        print(i / trials)
    shuffle(cards)
    for j in range(len(cards) - 1):
        if cards[j] == cards[j+1]:
            found = True
            two_in_a_row += 1
            break
    if not found:
        all_different += 1
    found = False
    
print(all_different + two_in_a_row)
print(f"{round(100*all_different/trials, 2)}% of all shuffles had no two equal cards in a row")
print(f"{round(100*two_in_a_row/trials, 2)}% of all shuffles had two or more cards in a row, once or more times")
