import sys
import time
import pygame
from pygame.locals import *

# width and height, in squares, for the region of the graph
WIDTH = 106
HEIGHT = 17
# pixel size of each square
SQUARESIZE = 10
# pixel size of the separator between squares
SEPSIZE = 1
S = SQUARESIZE + SEPSIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
SEPCOLOUR = BLACK
# file where the numbers are dumped
NUMBIN = "numbers.txt"
# height for the help text area
TEXTAREAHEIGHT = 125
FONTSIZE = 20

pygame.font.init()
# width and height are pixel dimensions of the grid area, only
width = SQUARESIZE*WIDTH + SEPSIZE*(WIDTH-1)
height = SQUARESIZE*HEIGHT + SEPSIZE*(HEIGHT-1)
screen = pygame.display.set_mode((width, height + TEXTAREAHEIGHT))

def draw_grid():
    """Prints the grid to the screen, with the right colour in each square."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            rect = pygame.Rect(c*S, r*S, SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(screen, cell, rect)
    for r in range(len(grid)-1):
        srs = SQUARESIZE + r*S
        pygame.draw.line(screen, SEPCOLOUR, (0, srs), (width, srs))
    for c in range(len(grid[0])):
        scs = SQUARESIZE + c*S
        pygame.draw.line(screen, SEPCOLOUR, (scs, 0), (scs, height))

def flip_colours(md, mu):
    """In click mode, after dragging the mouse, fill all the selected squares
    with the target colour of the square that was clicked first;
    i.e. if the pixel we clicked was colour1,
    all selected squares will now become colour2."""
    global last_grid
    last_grid = [[grid[i][j] for j in range(len(grid[0]))] for i in range(len(grid))]
    # flip all the squares to the colour that the square we clicked first does not have
    # i.e. if we started by clicking in a BLACK square, make every square now WHITE
    target_colour = WHITE if grid[md[1]][md[0]] == BLACK else BLACK
    # the directions in which we will traverse the area selected
    xdir = 1 if mu[0] - md[0] >= 0 else -1
    ydir = 1 if mu[1] - md[1] >= 0 else -1
    for x in range(abs(mu[0]-md[0])+1):
        for y in range(abs(mu[1]-md[1])+1):
            grid[ydir*y+md[1]][xdir*x+md[0]] = target_colour

def show_selected(md, ma):
    """Show in the grid the pixels that are currently selected."""
    # paint as gray all squares between where the mouse went down (md)
    # and where the mouse is at (ma)
    xdir = 1 if ma[0] - md[0] >= 0 else -1
    ydir = 1 if ma[1] - md[1] >= 0 else -1
    for x in range(abs(md[0]-ma[0])+1):
        for y in range(abs(md[1]-ma[1])+1):
            rect = pygame.Rect((xdir*x + md[0])*S, (ydir*y + md[1])*S, SQUARESIZE, SQUARESIZE)
            if x == 0 and y == 0: # show the final colour of the first square
                target_colour = WHITE if grid[md[1]][md[0]] == BLACK else BLACK
                pygame.draw.rect(screen, target_colour, rect)
                continue
            pygame.draw.rect(screen, GRAY, rect)

def get_number():
    """Traverse the current canvas and generate the number that can later
    be used to plot the same picture with Tupper's self-referential formula."""
    n = ""
    for x in range(WIDTH):
        for y in range(HEIGHT-1, -1, -1):
            n += "1" if grid[y][x] == BLACK else "0"
    return n[::-1]

def draw_help():
    """Draws the help text to the screen."""
    default_font_name = pygame.font.get_default_font()
    default_font = pygame.font.SysFont(default_font_name, FONTSIZE)
    help_text = [
        "There are two drawing modes, 'click' mode and 'paint' mode; check the window title. Click T to Toggle between the two."
      , "In paint mode, simply paint with your left mouse button (black) or with your right mouse button (white)."
      , "In click mode, clicking a square will flip its colour and dragging the mouse will fill an entire area."
      , (
          "Press W to paint the whole canvas with White."
        , "Press B to paint the whole canvas with Black."
      )
      , (
          "Press S to Save the current number encoding the image you painted."
        , "Press U to Undo the last change in Click mode."
      )
      , "Press H to toggle this Help message."
    ]
    ypad = 5
    for i, elem in enumerate(help_text):
        if isinstance(elem, str):
            # render the text directly
            rendered = default_font.render(elem, True, WHITE)
            screen.blit(rendered, (0, ypad + height + i*FONTSIZE))
        else:
            left, right = elem
            rleft = default_font.render(left, True, WHITE)
            rright = default_font.render(right, True, WHITE)
            screen.blit(rleft, (0, ypad + height + i*FONTSIZE))
            screen.blit(rright, (width//2, ypad + height + i*FONTSIZE))

last_grid = []
grid = [[WHITE for x in range(WIDTH)] for y in range(HEIGHT)]
mouse_down = None
mode = "Paint"
pygame.display.set_caption("Drawing mode: {}".format(mode))
left_down = False
right_down = False

help_visible = True
draw_help()

# be sure to save just the part with the plot, not the help text
# so create a subsurface that only holds that area
plotAreaRect = pygame.Rect(0, 0, width, height)
plotAreaSurf = screen.subsurface(plotAreaRect)

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == KEYDOWN:
            if ev.key == K_w:
                last_grid = grid
                grid = [[WHITE for x in range(WIDTH)] for y in range(HEIGHT)]
            elif ev.key == K_b:
                last_grid = grid
                grid = [[BLACK for x in range(WIDTH)] for y in range(HEIGHT)]
            elif ev.key == K_u:
                grid = last_grid
            elif ev.key == K_t:
                mode = "Click" if mode == "Paint" else "Paint"
                pygame.display.set_caption("Drawing mode: {}".format(mode))
            elif ev.key == K_n or ev.key == K_s:
                n = 17*int(get_number(), 2)
                filename = "plot{}.png".format(time.strftime('%y%m%d%H%M%S'))
                pygame.image.save(plotAreaSurf, filename)
                with open(NUMBIN, "a") as f:
                    f.write("Image '{}' goes with the number {}\n".format(filename, n))
            elif ev.key == K_h:
                help_visible = not help_visible
                if help_visible:
                    screen = pygame.display.set_mode((width, height + TEXTAREAHEIGHT))
                    draw_help()
                else:
                    screen = pygame.display.set_mode((width, height))
        elif ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                left_down = True
                mouse_down = (ev.pos[0]//S, ev.pos[1]//S)
            elif ev.button == 3:
                right_down = True
        elif ev.type == MOUSEBUTTONUP:
            if ev.button == 1:
                left_down = False
                if mode == "Click":
                    mouse_up = (ev.pos[0]//S, ev.pos[1]//S)
                    flip_colours(mouse_down, mouse_up)
                mouse_down = None
            elif ev.button == 3:
                right_down = False
        elif ev.type == MOUSEMOTION and mode == "Paint":
            p = pygame.mouse.get_pos()
            p = (p[0]//S, p[1]//S)
            colour = None
            if left_down:
                colour = BLACK
            elif right_down:
                colour = WHITE
            if colour is not None:
                grid[p[1]][p[0]] = colour

    draw_grid()
    # check if we are holding the mouse button down, to show the gray area
    # that is currently selected to be filled in
    if mouse_down is not None and mode == "Click":
        mouse_at = pygame.mouse.get_pos()
        mouse_at = (mouse_at[0]//S, mouse_at[1]//S)
        show_selected(mouse_down, mouse_at)
    pygame.display.flip()