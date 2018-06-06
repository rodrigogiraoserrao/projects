import os
import sys
import time
import configparser
import pygame
from pygame.locals import *
from random import choice

def parse_configurations():
    configfile = "config.ini"
    c = configparser.ConfigParser()
    r = c.read(configfile)
    if not r:
        # create the configfile
        global SQUARE, WIDTH, HEIGHT, FPS, ANIMATE, STYLE
        c["DEFAULT"] = {"SQUARE": 8,
                        "WIDTH": 24,
                        "HEIGHT": 18,
                        "FPS": 60,
                        "ANIMATE": False,
                        "STYLE": "straight"
                        }
        with open(configfile, "w") as f:
            c.write(f)
    # create the globals
    global SQUARE, WIDTH, HEIGHT, FPS, ANIMATE, STYLE
    SQUARE = int(c["DEFAULT"]["SQUARE"])
    WIDTH = int(c["DEFAULT"]["WIDTH"])
    HEIGHT = int(c["DEFAULT"]["HEIGHT"])
    FPS = int(c["DEFAULT"]["FPS"])
    ANIMATE = eval(c["DEFAULT"]["ANIMATE"])
    STYLE = c["DEFAULT"]["STYLE"]

def colour_square(x, y, colour):
    rect = pygame.Rect(x*SQUARE, y*SQUARE, SQUARE, SQUARE)
    pygame.draw.rect(screen, colour, rect)

RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
FRAME_BIN = "./animation_frames"
parse_configurations()

screen = pygame.display.set_mode((WIDTH*SQUARE, HEIGHT*SQUARE))

pygame.display.update()

endpoint = None
position = (0,0)
board = [[BLACK for j in range(HEIGHT)] for i in range(WIDTH)]
board[position[0]][position[1]] = WHITE
path = [position]
how_far = len(path)-1

if ANIMATE:
    if not os.path.isdir(FRAME_BIN):
        os.makedirs(FRAME_BIN)
    frame = 0

# controls the style of the labyrinth
if STYLE == "jagged":
    difs = [[-1,0],[1,0],[0,-1],[0,1]]
else:
    difs = [[-2,0],[2,0],[0,-2],[0,2]]

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)

    if ANIMATE:
        framepath = os.path.join(FRAME_BIN, "mazeframe{:03}.png".format(frame))
        pygame.image.save(screen, framepath)
        frame += 1

    for ev in pygame.event.get():
        if ev.type == QUIT:
            sys.exit()

    # find the next possible positions
    good_moves = []
    for dif in difs:
        p = (position[0]+dif[0], position[1]+dif[1])
        # if we just came from p, ignore it
        if path and p == path[-1]:
            continue
        # if we are trying to leave the board, ignore it
        elif p[0] < 0 or p[0] >= WIDTH or p[1] < 0 or p[1] >= HEIGHT:
            continue
        # verify if the new position or its neighbours haven't
        # been visited yet
        if dif[0] == 0:
            difx = [-1,0,1]
            dify = [0, int(dif[1]/abs(dif[1]))]
        else:
            difx = [0, int(dif[0]/abs(dif[0]))]
            dify = [-1,0,1]
        usable = True
        for dx in difx:
            for dy in dify:
                # verify we are inside the board
                if p[0]+dx < 0 or p[0]+dx >= WIDTH:
                    continue
                elif p[1]+dy < 0 or p[1]+dy >= HEIGHT:
                    continue
                if board[p[0]+dx][p[1]+dy] == WHITE:
                    usable = False
        if usable:
            good_moves.append(p)
    if good_moves:
        move = choice(good_moves)
        colour_square(position[0], position[1], WHITE)
        # when the style is straight, this colours the middle square
        colour_square((position[0]+move[0])/2, (position[1]+move[1])/2, WHITE)
        colour_square(move[0], move[1], RED)
        board[move[0]][move[1]] = WHITE
        position = move
        path.append(position)
        # check if this is the farthest we got so far
        # if it is, mark it as the endpoint
        if len(path)-1 > how_far:
            if endpoint:
                colour_square(endpoint[0], endpoint[1], WHITE)
            endpoint = move
            how_far = len(path)-1
            colour_square(move[0], move[1], RED)
    else:
        if not path:
            break
        else:
            move = path.pop()
            # make sure we don't whiten the endpoint
            if position != endpoint:
                colour_square(position[0], position[1], WHITE)
            colour_square(move[0], move[1], RED)
            position = move

    pygame.display.update()

if not os.path.isdir("./bin"):
    os.makedirs("./bin")
pygame.image.save(screen, "bin/maze_{}.png".format(time.strftime("%H_%M_%S_%d%m%Y")))
pygame.display.set_caption("done")

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            sys.exit()
