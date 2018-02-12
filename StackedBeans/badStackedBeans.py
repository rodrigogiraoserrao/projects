# play the game described in https://mathspp.blogspot.com/2018/02/problem-06-stacks-of-beans.html against a weak opponent

# edit the starting position here
STARTING_POSITION = (19, 20)
# put a 0 if the human goes first, 1 if the computer goes first
GOES_FIRST = 0

from random import randint, random
import sys

known_plays = {(2,0):(0,1),(3,0):(1, 1),(4,0):(2,1),(5,0):(1,2),(0,2):(1,0),(0,3):(1,1),(0,4):(1,2),(0,5):(2,1),(3,1):(1,2),(1,3):(2,1),(4,1):(2,2),(1,4):(2,2),(4,2):(2,3),(2,4):(3,2)}
def make_play(p):
    maxN = max(p)//2
    if pos in known_plays.keys() and random() < 0.5:
        newp = known_plays[p]
    else:
        N = randint(1, maxN)
    if pos[0] >= p[1]:
        newp = (p[0] - 2*N, p[1] + N)
    else:
        newp = (p[0] + N, p[1] - 2*N)
    return newp
    
pos = STARTING_POSITION

if GOES_FIRST:
    if pos in ((0,1),(1,1),(1,0)):
        print("You win!")
        sys.exit()
    newpos = make_play(pos)
    print("we are at{}, computer plays to {}".format(pos, newpos))
    pos = newpos
    
while pos not in ((0,1), (1,0), (1,1)):
    valid = False
    print("we are at {}, input the new position x,y:".format(pos))
    while not valid:
        s = input("x,y >> ")
        try:
            x, y = s.strip().split(",")
        except Exception:
            print("\tcould not parse input play")
            continue
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            print("\tnew pile sizes should be integers")
            continue
        if x < 0 or y < 0:
            print("\tnew pile sizes should be non-negative")
            continue
        dx = pos[0]-x
        dy = pos[1]-y
        if not (-dx == dy/2 or -dy == dx/2):
            print("\tnew pile sizes do not correspond to a legal play")
            continue
        valid = True
        pos = (x, y)
    # check if the computer didn't lose:
    if pos in ((0,1),(1,1),(1,0)):
        print("You win!")
        sys.exit()
    # the computer plays something
    newpos = make_play(pos)
    print("we are at {}, computer plays to {}".format(pos, newpos))
    pos = newpos
    
print("You lost!")
