import sys
import random
import pygame
from pygame.locals import *
from walker import Walker

pygame.init()
WIDTH = 400
HEIGHT = 400
BACKGROUND = (0, 170, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random walk with coloured trail")
screen.fill(BACKGROUND)
pygame.display.update()

clock = pygame.time.Clock()

def move():
    return (random.choice([-2,0,2]),
                            random.choice([-2,0,2]))
pos = [WIDTH//2, HEIGHT//2]
walker = Walker(screen, pos, get_move=move, size=2)

it = 0
while True:
    clock.tick(120)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

    walker.walk()
    walker.c = (55,0,it)
    walker.pos[0] %= WIDTH
    walker.pos[1] %= HEIGHT
    walker.draw()
    it += 1
    it %= 255

    pygame.display.update()