import pygame
from pygame.locals import *
import math

pygame.init()

WIDTH = 400
HEIGHT = 400

"""
def factory(c):
    def func(x):
        return x*x + c
    return func
"""
    
def hue(x):
    return 360/math.exp(x/50)
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pxarray = pygame.PixelArray(screen)

x_width = 2
x_left = -1.5
y_height = 2
y_bottom = -1
zoom = 1

def populate():
    global pxarray
    C = pygame.Color(0,0,0)
    cap = max(8, (10^9)/(zoom*zoom))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = complex(x_left + (x/WIDTH)*x_width, y_bottom + (y/HEIGHT)*y_height)
            i = 0
            res = 0
            while i < 50 and abs(res) < cap:
                res = res*res + c
                i += 1
            if abs(res) < 2:
                pxarray[x, y] = (0,0,0)
            else:
                """
                c = colour(i)
                pxarray[x, y] = (c, c, 255-c)
                """
                C.hsva = (hue(i), 50, 50, 100)
                pxarray[x, y] = C
        pygame.display.update()
            
populate()
pygame.display.update()
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            break
        elif ev.type == MOUSEBUTTONDOWN:
            nx, ny = ev.pos
            cx = nx/WIDTH * x_width + x_left
            cy = ny/HEIGHT * y_height + y_bottom
            x_width /= 4
            y_height /= 4
            x_left = cx - x_width/2
            y_bottom = cy - y_height/2
            zoom *= 4
            pygame.display.set_caption("Zoom level: {}".format(zoom))
            populate()
            pygame.display.update()