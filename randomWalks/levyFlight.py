import sys
import random
import pygame
from pygame.locals import *
from walker import Walker

# implement a lèvy flight algorithm

def move_():
    c = [-1, 0, 1]
    x = random.choice(c)
    y = random.choice(c)
        
    return (x, y)
    
def move():
    m = list(move_())
    n = random.random()
    if n >= 0.97:
        m[0] *=15
        m[1] *=15
        
    return m

pygame.init()
WIDTH = 400
HEIGHT = 400
BACKGROUND = (0, 170, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKGROUND)
pygame.display.update()
pygame.display.set_caption("Levy flight walk")

clock = pygame.time.Clock()

walkers = []
try:
    n = int(sys.argv[1])
    for i in range(1, n+1):
        pos = [int(random.random()*WIDTH), int(random.random()*HEIGHT)]
        walkers.append(Walker(screen, pos, get_move=move, size=6))
except:
    walkers.append(Walker(screen, [WIDTH//2, HEIGHT//2], get_move=move))

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

    pygame.display.update()
