import sys
import random
import pygame
from pygame.locals import *
from walker import Walker

def move():
    # more likely to go up
    n = random.random()
    if n <= 0.75:
        y = -1
    elif n <= 0.95:
        y = 1
    else:
        y = 0
    n = random.random()
    if n <= 0.5:
        x = 0
    elif n <= 0.75:
        x = 1
    else:
        x = -1
        
    return (x, y)

pygame.init()
WIDTH = 400
HEIGHT = 400
BACKGROUND = (0, 170, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tilted random walk")
screen.fill(BACKGROUND)
pygame.display.update()

clock = pygame.time.Clock()

walkers = []
try:
    n = int(sys.argv[1])
    for i in range(1, n+1):
        pos = [int(random.random()*WIDTH), int(random.random()*HEIGHT)]
        walkers.append(Walker(screen, pos, get_move=move, size=i%3+5))
except:
    walkers.append(Walker(screen, [WIDTH//2, HEIGHT//2], get_move=move))

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
        walker.pos[0] %= WIDTH
        walker.pos[1] %= HEIGHT

    pygame.display.update()
