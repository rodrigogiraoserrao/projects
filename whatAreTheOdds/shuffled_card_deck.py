# What is the probability that, given a completely shuffled deck of 52 cards (13 cards of each suit),
# there are at least two cards of the same value next to each other?
# This script estimates that probability to be 95.45%, which means only 4.55% of the times no two cards of the same value are in a row.

from random import shuffle

cards = [i for i in range(13)] * 4

trials = pow(10, 6)

all_different = 0   # count how many times the deck *does not* have two equal cards in a row
two_in_a_row = 0    # count how many times the deck has two equal cards in a row
pair_counter = 0    # count how many of these pairs are found in a shuffled deck
how_many_pairs = [] # the history of how many pairs per deck for some stats
three_in_a_row = 0  # count how many times the deck has three equal cards in a row
four_in_a_row = 0   # count how many times the deck has four equal cards in a row

# estimate the probability that a thoroughly shuffled deck contains any two cards in a row with the same value
for i in range(trials):
    if 0 == (i % (trials // 100)):
        print(f"{100 * i / trials}%\r")
    shuffle(cards)
    for j in range(len(cards) - 1):
        if cards[j] == cards[j+1]:
            pair_counter += 1
            # only increment the "two in a row" counter if this is the first pair of this deck
            if pair_counter == 1:
                two_in_a_row += 1
            if j < len(cards) - 2 and cards[j] == cards[j+2]:
                three_in_a_row += 1
                if j < len(cards) - 3 and cards[j] == cards[j+3]:
                    four_in_a_row += 1
    if not pair_counter:
        all_different += 1
    else:
        how_many_pairs.append(pair_counter)
    pair_counter = 0
    
print(all_different + two_in_a_row)
print(f"{round(100*all_different/trials, 2)}% of all shuffles had no two equal cards in a row")
print(f"{round(100*two_in_a_row/trials, 2)}% of all shuffles had two or more cards in a row, once or more times")
print(f"{round(100*three_in_a_row/trials, 2)}% of all shuffles had three or more cards in a row, once or more times")
print(f"{round(100*four_in_a_row/trials, 2)}% of all shuffles had four cards in a row, once or more times")

print()
for i in range(1, 11):
    print(f"{i:02} : {round(100*how_many_pairs.count(i)/trials, 2)}%")
    
"""
Sample output:
4.55% of all shuffles had no two equal cards in a row
95.45% of all shuffles had two or more cards in a row, once or more times
11.77% of all shuffles had three or more cards in a row, once or more times
0.23% of all shuffles had four cards in a row, once or more times

01 : 14.47%
02 : 22.54%
03 : 23.13%
04 : 17.3%
05 : 10.21%
06 : 4.9%
07 : 1.95%
08 : 0.68%
09 : 0.21%
10 : 0.05%
"""
