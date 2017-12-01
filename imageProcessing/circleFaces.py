import pygame
import sys
import os
import time
import random
from math import pi, sin, cos, tan, floor, ceil, sqrt

def load_image(name, transparent=False):
    """Function that handles image loading
    Returns the image and its Rect"""
    try:
        img = pygame.image.load(name)
    except pygame.error as e:
        raise SystemExit("Could not load image " + name)
    if not transparent:
        img = img.convert()
    img = img.convert_alpha()
    img_rect = img.get_rect()

    return img, img_rect

def lum(colour):
    return colour[0]*0.2126+colour[1]*0.7152+colour[2]*0.0722
    #return colour[0]

def dist(p, q):
    return sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except Exception:
        path = input("img path >> ")

    screen = pygame.display.set_mode((1, 1))
    img, img_rect = load_image(path)
    REDUCTION = 4
    ZOOM = 2
    screen = pygame.display.set_mode((img_rect.width//REDUCTION, img_rect.height//REDUCTION))
    # set the right size
    BACKGROUND = (255, 255, 255)
    LINES = (15, 15, 15)
    N = 5
    img = pygame.transform.scale(img, (ZOOM*img_rect.width, ZOOM*img_rect.height))
    bigger = pygame.Surface((ZOOM*img_rect.width, ZOOM*img_rect.height))
    bigger.fill(BACKGROUND)
    MID = [ZOOM*img_rect.width//2, ZOOM*img_rect.height//2]
    RADIUS = min(MID[0], MID[1])-2
    NSTEPS = 40
    lastline = time.time()
    go = True

    clock = pygame.time.Clock()
    random.seed(time.time())
    bestangle = 2*pi*random.random()
    while True:
        clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    go = not go
        if go:
            lastline = time.time()
            oldangle = bestangle
            bestL = 255*NSTEPS
            bestangle = None
            for i in range(N):
                L = 0
                newangle = 2*pi*random.random()
                x1 = MID[0] + RADIUS*cos(oldangle)
                y1 = MID[1] - RADIUS*sin(oldangle)
                x2 = MID[0] + RADIUS*cos(newangle)
                y2 = MID[1] - RADIUS*sin(newangle)
                for s in range(NSTEPS):
                    px = x1 + (s/NSTEPS)*(x2-x1)
                    py = y1 + (s/NSTEPS)*(y2-y1)
                    L += lum(img.get_at((int(px), int(py))))
                if L < bestL:
                    bestL = L
                    bestangle = newangle
            x1 = MID[0] + RADIUS*cos(oldangle)
            y1 = MID[1] - RADIUS*sin(oldangle)
            x2 = MID[0] + RADIUS*cos(bestangle)
            y2 = MID[1] - RADIUS*sin(bestangle)
            pygame.draw.line(bigger, LINES,
                            (int(x1), int(y1)),
                            (int(x2), int(y2)), 1)
            pygame.draw.line(img, BACKGROUND,
                            (int(x1), int(y1)),
                            (int(x2), int(y2)), 1)
            screen.blit(pygame.transform.scale(bigger, (img_rect.width//REDUCTION, img_rect.height//REDUCTION)), pygame.Rect(0,0,img_rect.width, img_rect.height))
            pygame.display.update()
