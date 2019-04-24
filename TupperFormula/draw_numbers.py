import sys
import time
import pygame
import decimal  # for large floats
from pygame.locals import *
from math import floor

WIDTH = 106
HEIGHT = 17
SQUARESIZE = 10
SEPSIZE = 0
S = SQUARESIZE + SEPSIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
NUMBIN = "number2draw.txt"
DEFAULT_N = 1221322481876768438713287934800381857708152649910978121180786421254382388398740869470697712246308584011671056630712267974134050493867001320856888821005299303921801316683645677302622143870718584846979670873016154296513741473937956563160891636618952837487052172390116097060807868050511693382187731376177088729125713669605452982357546269337014477766928988826056980026066837670822393954509223734065291107763700438960200533468388160205905094514064044895424741376

width = SQUARESIZE*WIDTH + SEPSIZE*(WIDTH-1)
height = SQUARESIZE*HEIGHT + SEPSIZE*(HEIGHT-1)
screen = pygame.display.set_mode((width, height))
decimal.getcontext().prec = 100000

def mod(a, b):
    m = a%b
    if m < 0:
        return m+b
    else:
        return m

def f(x, y):
    xd = decimal.Decimal(x)
    yd = decimal.Decimal(y)
    arg = floor(yd/decimal.Decimal(17)) * decimal.Decimal(2)**(decimal.Decimal(-17)*xd - mod(yd,decimal.Decimal(17)))
    return floor(mod(arg, decimal.Decimal(2)))

def draw_grid(N):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x*S, (HEIGHT-y-1)*S, SQUARESIZE, SQUARESIZE)
            val = f(x, y+N)
            colour = BLACK if val > 1/2 else WHITE
            pygame.draw.rect(screen, colour, rect)
            pygame.display.flip()

def get_number_to_draw():
    try:
        with open(NUMBIN, "r") as f:
            N = int(f.read())
        return N
    except Exception:
        # try to give some helpful message
        pygame.display.set_caption("Try changing the number inside this file: {}".format(NUMBIN))
        # create the right file
        with open(NUMBIN, "w") as f:
            f.write(str(DEFAULT_N))
        # return a default number that shows an error :P
        return DEFAULT_N

N = get_number_to_draw()
draw_grid(N)
pygame.display.set_caption(str(N))
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == KEYDOWN:
            if ev.key == K_n or ev.key == K_s:
                filename = "plot{}.png".format(time.strftime('%y%m%d%H%M%S'))
                pygame.image.save(screen, filename)
                with open(NUMBIN, "a") as f:
                    f.write("Plot '{}' goes with the number {}\n".format(filename, N))