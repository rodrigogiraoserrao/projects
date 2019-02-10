import os
import sys
import time
import pygame
from pygame.locals import *
from random import choice

N = 2
SQUARESIZE = 20

screen = pygame.display.set_mode(((2*N+1)*SQUARESIZE, (2*N+1)*SQUARESIZE))

def get_random_direction(pos):
    directions = []
    if pos[0] > 1:
        directions.append([-1, 0])
    if pos[0] < 2*N-1:
        directions.append([1, 0])
    if pos[1] > 1:
        directions.append([0, -1])
    if pos[1] < 2*N-1:
        directions.append([0, 1])
    return choice(directions)

def next_start():
    i, j = previous_start
    while [i, j] in accepted:
        i += 2
        if i > 2*N:
            i = 1
            j += 2
    return [i, j]

def erase_self_loop(path, target):
    while path[-1] != target:
        path.pop()

def accept_walk(accepted, walk):
    for elem in walk[:-1]:
        accepted.append(elem)

def draw_maze(path, accepted):
    colors = {
        0: (0,0,0),
        2: (255,255,255),
        1: (255,0,0)
    }
    screen.fill(colors[0])
    for square in path:
        y, x = square
        r = pygame.Rect(x*SQUARESIZE, y*SQUARESIZE, SQUARESIZE, SQUARESIZE)
        pygame.draw.rect(screen, colors[1], r, 0)
    for square in accepted:
        y, x = square
        r = pygame.Rect(x*SQUARESIZE, y*SQUARESIZE, SQUARESIZE, SQUARESIZE)
        pygame.draw.rect(screen, colors[2], r, 0)

clock = pygame.time.Clock()

accepted = []
accepted.append([1,1])
previous_start = [1,1]
currently_at = next_start() # position from where we will continue the random walk
previous_start = currently_at
current_walk = [currently_at]
while len(accepted) < 2*N*N-1:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == KEYDOWN:
            draw_maze(current_walk, accepted)
            pygame.display.update()

    direction = get_random_direction(currently_at)
    mid_square = [currently_at[i] + direction[i] for i in range(2)]
    next_position = [currently_at[i] + 2*direction[i] for i in range(2)]
    if next_position in current_walk:
        erase_self_loop(current_walk, next_position)
        if current_walk:
            currently_at = current_walk[-1]
        else:
            currently_at = next_start()
            previous_start = currently_at
            current_walk = [currently_at]
    else:
        current_walk.append(mid_square)
        current_walk.append(next_position)
        currently_at = next_position
        if currently_at in accepted:
            accept_walk(accepted, current_walk)
            currently_at = next_start()
            previous_start = currently_at
            current_walk = [currently_at]

print("done")
# draw the maze
draw_maze([], accepted)
pygame.display.update()
# save the maze
filename = f"wilson_maze_N{N}_p{SQUARESIZE}_{time.strftime('%H_%M_%S_%d%m%Y')}.png"
filepath = os.path.join("bin", filename)
pygame.image.save(screen, filepath)

# flood fill the maze
distances = [[-1 for i in range(2*N+1)] for j in range(2*N+1)]
distances[1][1] = 0
this_iteration = [[1,1]]
next_iteration = []
directions = [[1,0],[-1,0],[0,1],[0,-1]]
d_value = 0
color_sequence = [[35 + i*10,0,0] for i in range(15)] + [[175, 5+i*10, 0] for i in range(18)] + \
                 [[35 + (15-i)*10, 175, 0] for i in range(19)] + [[35, 175 - i*10, 0] for i in range(18)]
color_idx = 0

while this_iteration:
    clock.tick(40)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

    # create a degradee
    c = color_sequence[color_idx]
    color_idx += 1
    color_idx %= len(color_sequence)
    for nx,ny in this_iteration:
        for dx,dy in directions:
            px = nx+2*dx
            py = ny+2*dy
            if px > 0 and px < 2*N+1 and py > 0 and py < 2*N+1:
                if [nx+dx, ny+dy] in accepted and distances[px][py] == -1 and \
                    [px, py] not in next_iteration:
                    next_iteration.append([px,py])
                    distances[nx+dx][ny+dy] = d_value+1
                    r = pygame.Rect((ny+dy)*SQUARESIZE, (nx+dx)*SQUARESIZE, SQUARESIZE, SQUARESIZE)
                    pygame.draw.rect(screen, c, r, 0)
                    distances[px][py] = d_value+2
                    r = pygame.Rect((py)*SQUARESIZE, (px)*SQUARESIZE, SQUARESIZE, SQUARESIZE)
                    pygame.draw.rect(screen, c, r, 0)
    if next_iteration:
        d_value += 2
    this_iteration = next_iteration[::]
    next_iteration = []
    print(d_value)

    pygame.display.update()

# save the flooded maze
filename = filename.replace("maze", "flooded")
filepath = os.path.join("bin", filename)
pygame.image.save(screen, filepath)
print("saved")

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            sys.exit()