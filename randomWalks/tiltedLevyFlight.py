import sys
import random
import pygame
from pygame.locals import *
from walker import Walker

# implement a lèvy flight algorithm
# version 2, scales with the length of the step
# tends to walk to the right and down

def get_r():
    n, n1 = 0, 1
    while n1 > n:
        n = random.random()
        n1 = random.random()
        
    return n
    
def move():
    x = int((get_r() * 14) - 7)
    y = int((get_r() * 14) - 7)
        
    return [x, y]

pygame.init()
WIDTH = 400
HEIGHT = 400
BACKGROUND = (0, 170, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tilted levy flight walk")
screen.fill(BACKGROUND)
pygame.display.update()

clock = pygame.time.Clock()

walkers = []
try:
    n = int(sys.argv[1])
    for i in range(1, n+1):
        pos = [int(random.random()*WIDTH), int(random.random()*HEIGHT)]
        walkers.append(Walker(screen, pos, get_move=move, size=6))
except:
    walkers.append(Walker(screen, [WIDTH//6, HEIGHT//6], get_move=move, size=3))

while True:
    clock.tick(15)

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
