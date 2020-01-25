import pygame
from pygame.locals import *
import math

pygame.init()

WIDTH = 800
HEIGHT = 800

ITERS_PER_POINT = 100

done = []
i = -1

"""
def factory(c):
    def func(x):
        return x*x + c
    return func
"""
    
def hue(x):
    return 200/math.exp(x/ITERS_PER_POINT)
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pxarray = pygame.PixelArray(screen)

x_width = 4
x_left = -2
y_height = 4
y_bottom = -2

def populate(cx, cy):
    global pxarray
    C = pygame.Color(0,0,0)
    cap = 8
    c = complex(cx, cy)
    pygame.display.set_caption("Julia set of {} + {}i".format(cx, cy))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            i = 0
            res = complex(x_left + (x/WIDTH)*x_width, y_bottom + (y/HEIGHT)*y_height)
            while i < ITERS_PER_POINT and abs(res) < cap:
                res = res*res + c
                i += 1
            if abs(res) < 2:
                pxarray[x, y] = (0,0,0)
            else:
                """
                c = colour(i)
                pxarray[x, y] = (c, c, 255-c)
                """
                C.hsva = (360-hue(i), 75, 75, 100)
                pxarray[x, y] = C
        pygame.display.update()

def init():
    screen.fill((255,255,255))
    pygame.draw.line(screen, (0,0,0), (0,HEIGHT/2), (WIDTH, HEIGHT/2))
    pygame.draw.line(screen, (0,0,0), (WIDTH/2, 0), (WIDTH/2, HEIGHT))
    pygame.display.set_caption("Click a point to create its Filled Julia Set")
            
init()
pygame.display.update()
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            break
        elif ev.type == MOUSEBUTTONDOWN:
            nx, ny = ev.pos
            cx = round(nx/WIDTH * x_width + x_left, 3)
            cy = round((1-ny/HEIGHT) * y_height + y_bottom, 3)
            populate(cx, cy)
            pygame.display.update()
            done.append((cx,cy))
            i = len(done)-1
        elif ev.type == KEYDOWN:
            if ev.key == K_LEFT:
                if i > 0:
                    i = i-1
                    populate(*done[i])
            elif ev.key == K_RIGHT:
                if i < len(done)-1:
                    i = i+1
                    populate(*done[i])
            elif ev.key == K_SPACE:
                init()
                pygame.display.update()