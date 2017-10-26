import sys
import random
import pygame
from pygame.locals import *

pygame.init()

WIDTH = 600
HEIGHT = 600
BACKGROUND = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def get_colour():
    r, g, b = (-1,-1,-1)
    while 0 > r or 255 < r:
        r = int(random.gauss(178, 60))
    while 0 > g or 255 < g:
        g = int(random.gauss(178, 60))
    while 0 > b or 255 < b:
        b = int(random.gauss(178, 60))

    return (r,g,b)

def get_pos():
    x = int(random.gauss(WIDTH//2, WIDTH//6))
    y = int(random.gauss(HEIGHT//2, HEIGHT//6))

    return (x, y)

clock = pygame.time.Clock()

while True:
    clock.tick(15)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

    c = get_colour()
    p = get_pos()
    r = int(random.gauss(20, 5))

    pygame.draw.circle(screen, c, p, r)
    pygame.display.update()
