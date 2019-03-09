### Needs Python 3.7 to run
import os
import sys
import time
import configparser
import pygame
from pygame.locals import *
from random import choice

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (20, 90, 200)
ORANGE = (200, 130, 20)

'''@dataclass(init=False)
class Configurations:
    # set the relevant configurations and the default values
    WIDTH: int = 20
    HEIGHT: int = 20
    CELLSIZE: int = 5
    SCREENSHOT_BIN: str = ""
    
    def __init__(self, configfile):
        """Handle the initial configurations"""
        c = configparser.ConfigParser()
        r = c.read(configfile)
        vs = ["WIDTH", "HEIGHT", "CELLSIZE", "SCREENSHOT_BIN"]
        if not r:
            print("creating default")
            # create the configfile
            c["DEFAULT"] = {var: getattr(self, var) for var in vs}
            with open(configfile, "w") as f:
                c.write(f)
        # load the values
        for var in vs:
            # read each parameter and evaluate it to its type
            setattr(self, var, eval(c["DEFAULT"][var]))'''
            
class Configurations(object):
    # set the relevant configurations and the default values
    WIDTH = 20
    HEIGHT = 20
    CELLSIZE = 5
    SCREENSHOT_BIN = ""
    SAVE_FRAMES = False
    
    def __init__(self, configfile):
        """Handle the initial configurations"""
        c = configparser.ConfigParser()
        r = c.read(configfile)
        vs = ["WIDTH", "HEIGHT", "CELLSIZE", "SCREENSHOT_BIN", "SAVE_FRAMES"]
        if not r:
            print("creating default")
            # create the configfile
            c["DEFAULT"] = {var: getattr(self, var) for var in vs}
            with open(configfile, "w") as f:
                c.write(f)
        # load the values
        for var in vs:
            # read each parameter and evaluate it to its type
            setattr(self, var, eval(c["DEFAULT"][var]))

def get_next_start():
    """Generator expression that yields the next cell
        at which a random path should start"""
    x, y = -1, 1
    # there is a new start to find as long as we are inside the legal dims
    while x <= 2*confs.WIDTH and y <= 2*confs.HEIGHT:
        x += 2
        if x > 2*confs.WIDTH:
            x = 1
            y += 2
            if y > 2*confs.HEIGHT:
                break
        # only return this cell if it does not belong to the maze
        if mazedata[x][y] == 0:
            yield [x, y]

def get_random_direction(x, y):
    """Given a position on the maze, returns with uniform probability,
        any possible direction in which the maze could expand"""
    poss_directions = []
    x, y
    if x < 2*confs.WIDTH-1:
        poss_directions.append([1, 0])
    if x > 1:
        poss_directions.append([-1, 0])
    if y < 2*confs.HEIGHT-1:
        poss_directions.append([0, 1])
    if y > 1:
        poss_directions.append([0, -1])
    return choice(poss_directions)

def update(x, y, val):
    """Updates the cell (x,y) to the type val
        Also updates its display on the screen"""
    mazedata[x][y] = val
    colors = {
        0: BLACK,
        2: WHITE,
        1: RED
    }
    pygame.draw.rect(screen, colors[val], rectangles[x][y], 0)
    toUpdate.append(rectangles[x][y])

def erase_self_loop(target):
    """Erases the self-intersecting loop of the current path"""
    while pathStack[-1] != target:
        x, y = pathStack.pop()
        update(x, y, 0)

def accept_walk():
    """Marks the current path as part of the maze"""
    for x, y in pathStack:
        update(x, y, 2)

def colour_sequence(c1, c2):
    """Given two colours, create a degradee from c1 to c2 and back"""
    cs = [list(c1)]
    # from c1 to c2 and then c2 to c1
    for direction in [1, -1]:
        # change one colour band at a time
        for band in range(3):
            sign = direction*((c2[band]>c1[band]) - (c1[band]>c2[band]))
            left = c1[band] if direction == 1 else c2[band]
            right = c2[band] if direction == 1 else c1[band]
            for pixel_value in range(left+sign, right+sign, sign):
                clr = cs[-1][::]
                clr[band] = pixel_value
                cs.append(clr)
    return cs

confs = Configurations("wilsonconfig.ini")

# initialize the screen with the specified configurations
pixelWIDTH = confs.CELLSIZE*(2*confs.WIDTH + 1)
pixelHEIGHT = confs.CELLSIZE*(2*confs.HEIGHT + 1)
screen = pygame.display.set_mode((pixelWIDTH, pixelHEIGHT))
pygame.display.set_caption("Creating a maze")

# create the rectangles that will be needed in advance
rectangles = [
                [pygame.Rect(x*confs.CELLSIZE, y*confs.CELLSIZE,
                            confs.CELLSIZE, confs.CELLSIZE)
                                    for y in range(2*confs.HEIGHT+1)]
                    for x in range(2*confs.WIDTH+1)
            ]
# mazedata[x][y] == i indicates the type of cell
# i == 0 -> wall
# i == 1 -> current path
# i == 2 -> walkable cell (accepted path)
mazedata = [
                [0 for y in range(2*confs.HEIGHT+1)]
                    for x in range(2*confs.WIDTH)
            ]
# distance of the given vertex to the vertex where flooding started
distances = [
                [-1 for y in range(2*confs.HEIGHT+1)]
                    for x in range(2*confs.WIDTH)
            ]
# current path that is trying to connect to the accepted maze
pathStack = []
# flags to know in what part of the program we are
buildingMaze = True
finishedBuilding = False
floodingMaze = False
finishedFlooding = False
# list which will contain the areas of the screen to be updated
toUpdate = []
# generator for the starting positions
generator_gns = get_next_start()

# prepare the maze for the algorithms
x, y = next(generator_gns)
update(x, y, 2)
flooding_this = [[x,y]]    # vertices that must be checked in a given iter
distances[x][y] = 0
x, y = currently_at = next(generator_gns)
update(x, y, 1)
pathStack.append(currently_at)

curr_d = 0  # current distance to the flood starting point
clr_idx = 0 # current colour to be used when colouring the maze
cs = colour_sequence(ORANGE, BLUE)  # colour sequence to be used
flooding_next = []  # vertices that will be checked in the next iter
directions = [[1,0],[-1,0],[0,1],[0,-1]]

frame = 0
while True:
    for ev in pygame.event.get():
        # trying to exit the program
        if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_q):
            pygame.quit()
            sys.exit()
        elif ev.type == KEYDOWN:
            if ev.key == K_s:
                # take a screenshot
                filename = "ss_{}.png".format(time.strftime('%H_%M_%S_%d%m%y'))
                filename = os.path.join(confs.SCREENSHOT_BIN, filename)
                pygame.image.save(screen, filename)
                pygame.display.set_caption("screenshot saved in {}".format(filename))
            elif ev.key == K_f:
                if finishedBuilding and not (floodingMaze or finishedFlooding):
                    floodingMaze = True

    if buildingMaze:
        if confs.SAVE_FRAMES:
            filename = "frames/frame{:05}.png".format(frame)
            pygame.image.save(screen, filename)
            frame += 1
        dx, dy = d = get_random_direction(x, y)
        midx, midy = mid_position = [currently_at[i] + d[i] for i in range(2)]
        nx, ny = next_pos = [currently_at[i] + 2*d[i] for i in range(2)]
        if next_pos in pathStack:
            # this random path intersected itself
            erase_self_loop(next_pos)
            x, y = currently_at = pathStack[-1]
        else:
            # accept this new advancement
            update(midx, midy, 1)
            pathStack.append(mid_position)
            x, y = currently_at = next_pos
            if mazedata[x][y] == 2:
                # we have met the maze, accept the path
                accept_walk()
                try:
                    x, y = currently_at = next(generator_gns)
                    pathStack = [currently_at]
                    update(x, y, 1)
                except StopIteration:
                    # we have reached the end
                    buildingMaze = False
                    finishedBuilding = True
            else:
                update(x, y, 1)
                pathStack.append(next_pos)
    elif floodingMaze:
        # flood the maze
        clr1 = cs[clr_idx % len(cs)]
        clr2 = cs[(clr_idx+1) % len(cs)]
        clr_idx += 2
        for x, y in flooding_this:
            for dx, dy in directions:
                nx = x + 2*dx
                ny = y + 2*dy
                if nx > 0 and nx < 2*confs.WIDTH+1 and \
                                ny > 0 and ny < 2*confs.HEIGHT+1:
                    midx = x + dx
                    midy = y + dy
                    if mazedata[midx][midy] == 2 and distances[nx][ny] == -1 and \
                                    [nx, ny] not in flooding_next:
                        flooding_next.append([nx, ny])
                        distances[midx][midy] = curr_d + 1
                        pygame.draw.rect(screen, clr1, rectangles[midx][midy], 0)
                        toUpdate.append(rectangles[midx][midy])
                        distances[nx][ny] = curr_d + 2
                        pygame.draw.rect(screen, clr2, rectangles[nx][ny], 0)
                        toUpdate.append(rectangles[nx][ny])
        if flooding_next:
            curr_d += 2
        else:
            print(curr_d)
            finishedFlooding = True
            floodingMaze = False
        flooding_this = flooding_next[::]
        flooding_next = []

    if toUpdate:
        pygame.display.update(toUpdate)
        toUpdate = []