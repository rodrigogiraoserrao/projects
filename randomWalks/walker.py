import random
import pygame

class Walker(object):
    def __init__(self, screen, pos, get_move=None, size=2, colour=(0,0,0)):
        self.c = colour
        self.pos = pos
        self.screen = screen
        self.size = size
        if get_move is None:
            def move_():
                return (random.choice([-1,0,1]),
                            random.choice([-1,0,1]))
            self.get_moves = move_
        else:
    	    self.get_moves = get_move

    def walk(self):
        m = self.get_moves()
       	self.pos[0] += m[0]
       	self.pos[1] += m[1]

    def draw(self):
        pygame.draw.circle(self.screen, self.c, self.pos, self.size)
