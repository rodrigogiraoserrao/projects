### Play the game described in https://mathspp.blogspot.com/2018/02/problem-06-stacks-of-beans.html against the perfect opponent

import sys

# edit the starting position here
START_POSITION = (19, 20)

# player goes first, input a play in the format x,y where x and y are
# integers representing the size of the new piles
pos = START_POSITION
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
    # check if the optimal play is possible and/or legal
    # first case, we can play in such a way that the human player is in a losing position
    a, b = max(pos), min(pos)
    N = round((a-b)/3)
    if N < 1:
        # we cannot make the optimal play and thus must resort to playing something
        N = 1
    if (pos[0] >= pos[1]):
        newpos = (a - 2*N, b + N)
    else:
        newpos = (b + N, a - 2*N)
    print("we are at {}, computer plays to {}".format(pos, newpos))
    pos = newpos
    
print("You lost!")
