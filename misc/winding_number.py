"""
A small script that produces a pygame animation that helps visualize
    what the winding number of a continuous mapping is
(cf. https://mathspp.blogspot.com/2018/07/pocket-maths-hairy-ball-theorem.html )
"""

from pygame.locals import *
import pygame
import sys
import math

def load_image(name, transparent=False):
    """Function that handles image loading
    Returns the image and its Rect"""
    try:
        img = pygame.image.load(name)
    except pygame.error:
        raise SystemExit("Could not load image " + name)
    if not transparent:
        img = img.convert()
    img = img.convert_alpha()
    img_rect = img.get_rect()

    return img, img_rect

WIDTH = 400
HEIGHT = 200
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

angle = 0
dw = -0.05  # make this 100 times smaller if you are not going to save any frames
n = 1       # winding number
r = 80
idx = 0

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

    angle += dw
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (100, HEIGHT//2), r, 2)
    pygame.draw.circle(screen, WHITE, (300, HEIGHT//2), r, 2)
    dot1p = (r*math.cos(angle)+100, r*math.sin(angle)+HEIGHT//2)
    dot1p = list(map(int, dot1p))
    dot2p = (r*math.cos(n*angle)+300, r*math.sin(n*angle)+HEIGHT//2)
    dot2p = list(map(int, dot2p))

    pygame.draw.circle(screen, WHITE, dot1p, 6)
    pygame.draw.circle(screen, RED, dot2p, 6)

    pygame.display.update()

    # comment this if you do not want to save frames
    if angle > -2*math.pi:
        pygame.image.save(screen, "bin/frame{:04}.jpg".format(idx))
        idx += 1
