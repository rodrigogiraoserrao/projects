import itertools
import random
import sys

import pygame


POINTS = 100
WIDTH = 640
HEIGHT = 480


pygame.init()
screen = pygame.display.set_mode((640, 480))


def random_colour():
    return [random.randint(0, 255) for _ in range(3)]


if __name__ == "__main__":
    points = [
        (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        for _ in range(POINTS)
    ]
    colours = [random_colour() for _ in range(POINTS)]

    for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
        min_dist, min_colour = float("+inf"), (0, 0, 0)
        for point, colour in zip(points, colours):
            dist = (point[0] - x) ** 2 + (point[1] - y) ** 2
            if dist < min_dist:
                min_dist = dist
                min_colour = colour
        screen.set_at((x, y), min_colour)

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
