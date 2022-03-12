import itertools
import math
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


def dist(p1, p2):
    return math.sqrt(dist_sq(p1, p2))


def dist_sq(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


if __name__ == "__main__":
    points = [
        (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        for _ in range(POINTS)
    ]
    colours = [random_colour() for _ in range(POINTS)]

    mapped = set()
    dists = []
    for p1 in points:
        p1_dists = [dist_sq(p1, p2) for p2 in points if p1 != p2]
        dists.append((p1, int(math.sqrt(min(p1_dists)) // 2)))

    # Paint the circles that are close enough to each point.
    for (centre, d), colour in zip(dists, colours):
        for dx, dy in itertools.product(range(-d, d + 1), repeat=2):
            p = (centre[0] + dx, centre[1] + dy)
            if dist(p, centre) <= d:
                mapped.add(p)
                screen.set_at(p, colour)
        pygame.display.flip()

    for xy in itertools.product(range(WIDTH), range(HEIGHT)):
        if xy in mapped:  # Skip points already painted.
            continue
        min_dist, min_colour = float("+inf"), (0, 0, 0)
        for point, colour in zip(points, colours):
            d = dist_sq(point, xy)
            if d < min_dist:
                min_dist = d
                min_colour = colour
        screen.set_at(xy, min_colour)

    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
