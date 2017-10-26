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
pygame.display.set_caption("Random walk")
screen.fill(BACKGROUND)
pygame.display.update()

clock = pygame.time.Clock()

walkers = []
try:
    n = int(sys.argv[1])
    for i in range(1, n+1):
        pos = [int(random.random()*WIDTH), int(random.random()*HEIGHT)]
        walkers.append(Walker(screen, pos, size=2*(i%3+2)))
except:
    walkers.append(Walker(screen, [WIDTH//2, HEIGHT//2]))

while True:
    clock.tick(120)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BACKGROUND)
    for walker in walkers:
        walker.walk()
        walker.draw()

    pygame.display.update()
