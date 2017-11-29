import sys
import os
import pygame
import random
import atexit
from pygame.locals import *
from PIL import Image

def stallTheTerminalFTW():
    print("Please let rodrigomserrao@gmail.com if you crashed his program!")
    input("... hit return to exit ...")

def mazeConverter(imagefilepath, tempfilepath):
    try:
        img = Image.open(imagefilepath)
    except Exception as e:
        print("An error ocurred when opening the image")
        raise(e)

    pixelMap = img.load()
    width, height = img.size

    totalL = 0
    lums = []
    for i in range(width):
        lums.append([])
        for j in range(height):
            p = pixelMap[i, j]
            L = int(p[0]*0.2126)+int(p[1]*0.7152)+int(p[2]*0.0722)
            lums[i].append(L)
            totalL += L
    averageLum = totalL / (width*height)

    for i in range(width):
        for j in range(height):
            pixelMap[i, j] = (0, 0, 0) if lums[i][j] < averageLum \
                                        else (255, 255, 255)

    img.save(tempfilepath)
##############################################################

pygame.init()

PREFIX = "bw_"   # prefix for the temporary file
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
WALL = "x"   # string to mark "wall" pixels
PATH = " "   # string to mark "path" pixels

def kill(msg, error=None):
    """Function that kills the program after printing a custom message
    Prints the error message of the error passed, if one is passed"""
    print(msg)
    print()
    if error is not None:
        print(error)
    sys.exit()

def cleanup(tmpfilepath):
    """Function that tries to delete the temporary file"""
    if os.path.isfile(tmpfilepath):
        try:
            os.remove(tmpfilepath)
            print("temporary file successfully removed")
        except Exception as e:
            kill("Could not delete temporary file {}".format(tmpfilepath), e)

def ask_yes_no(msg):
    """Function to ask for yes/no input after printing a message"""
    print(msg)
    ans = ""
    while not (ans.startswith("y") or ans.startswith("n")):
        ans = input("[y]es or [n]o? >> ")

    return ans.startswith("y")
   
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

class MazeMatrix(object):
    """Class that implements the maze matrix
    A 2D list whose cells correspond to a given pixel in the image
    Each cell can either be a "path" cell or a "wall" cell"""

    def __init__(self, maze_img, bwimg, points):
        """Initialize the matrix"""
        # the actual maze image where the path is drawn
        self.maze_img = maze_img
        # the black and white image used to create the matrix
        self.bwimg = bwimg
        # the rectangle of the image
        self.img_rect = self.bwimg.get_rect()
        # the start and end points
        self.points = points

        self.matrix = []
        # the image is black and white
        # the entry point is of the colour of the path, so find it
        path_colour = self.bwimg.get_at(points[0])
        # create the matrix
        for i in range(self.img_rect.width):
            self.matrix.append([])
            for j in range(self.img_rect.height):
                if self.bwimg.get_at((i, j)) == path_colour:
                    self.matrix[i].append(PATH)
                else:
                    self.matrix[i].append(WALL)

        # mark the beginning
        x, y = self.points[0]
        self.matrix[x][y] = 0
        # no need to mark the end point
        # check the implementation of the solve() method

    def get_neighbours(self, coords):
        """Function that returns the 4 pixels that are adjacent to the given
        Ignores pixels that fall off the image"""
        x, y = coords
        neighbours = []
        # get the top neighbour
        if y > 0:
            neighbours.append((x, y-1))
        # get the bottom neighbour
        if (y+1) < self.img_rect.height:
            neighbours.append((x, y+1))
        # get left neighbour
        if x > 0:
            neighbours.append((x-1, y))
        # get right neighbour
        if (x+1) < self.img_rect.width:
            neighbours.append((x+1, y))

        return neighbours

    def solve(self):
        """Function that implements a pseudo-Djikstra's algorithm
        The algorithm's explanation can be found in the Wikipedia page
            for 'Pathfinding'
        Returns the distance between the two points in pixels"""
        queue = [self.points[0]]
        distance = 0

        while self.points[1] not in queue:
            distance += 1
            next_queue = []
            for pixel in queue:
                Ns = self.get_neighbours(pixel)
                for neighbour in Ns:
                    x, y = neighbour
                    if self.matrix[x][y] == PATH:
                        self.matrix[x][y] = distance
                        next_queue.append(neighbour)
            queue = next_queue[:]
            if not queue:
                kill("Could not find the path")

        return distance

    def get_path(self):
        """Function that draws the path from the start to the end point
        Since a pixel with numbering N must be adjacent to a pixel N-1,
            and so on, if I am standing in a pixel N, as soon as I find
            a neighbour N-1, I can mark that one off and look for a N-2"""
        x, y = self.points[1]
        distance = self.matrix[x][y]
        # pixel we have just drawn in
        # if to_parse is N, look for an adjacent N-1, paint it
        # and make it the new to_parse
        to_parse = self.points[1]
        while distance > 0:
            distance -= 1
            next_parse = []
            Ns = self.get_neighbours(to_parse)
            # randomize to help prevent loads of straight lines
            random.shuffle(Ns)
            for pix in Ns:
                x, y = pix
                if self.matrix[x][y] == distance:
                    # pix is an available N-1 pixel, make it the next to_parse
                    to_parse = pix
                    self.maze_img.set_at(pix, RED)
                    # for graphical purposes, paint all the adjacent pixels
                    # just for a better looking path (1p width is too little)
                    to_draw = self.get_neighbours(pix)
                    for p_d in to_draw:
                        x, y = p_d
                        if self.matrix[x][y] != WALL:
                            self.maze_img.set_at(p_d, RED)
                    break

if __name__ == "__main__":
    # clean the temporary file
    atexit.register(stallTheTerminalFTW)

    print("Welcome to the MazeSolver, by Rodrigo Girao Serrao;\n\tStart by typing the path to the image that holds " + \
            "the maze you want to solve.\n\tClick the two points you want to find a path between\n\t\t(this is generally " + \
            "the start and the end of the maze)\n\tYou will be prompted to confirm the two points are correct\n\tIf they are, " + \
            "the program will attempt to draw a path between the two points and tell you if there is no path.")

    # get the path to the maze image
    try:
        mazePath = sys.argv[1]
    except IndexError:
        print("Input the file path argument:")
        mazePath = input(">> ")

    head, tail = os.path.split(mazePath)
    tmpfilepath = os.path.join(head, PREFIX+tail)
    atexit.register(cleanup, tmpfilepath)
    # make sure it points to a file
    if not os.path.isfile(mazePath):
        kill("File path doesn't point to a valid path")
    else:
        try:
            # try to execute the mazeParser with that image
            mazeConverter(mazePath, tmpfilepath)
        except Exception as e:
            # abort upon error
            kill("Failed to parse the maze image", e)

    # parsing successful
    print("Maze image conversion successful")

    # set_mode so that the load_image function works
    screen = pygame.display.set_mode((1, 1))
    # now we need to find the two entry points
    maze_img, maze_rect = load_image(mazePath)
    bwm_img, bwm_rect = load_image(tmpfilepath)

    # set the right size
    screen = pygame.display.set_mode((maze_rect.width, maze_rect.height))
    screen.blit(maze_img, maze_rect)
    pygame.display.update()

    # loop to ask for the points
    points = []
    print("Click the two points to be connected...")
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                kill("Program aborted")
            elif ev.type == MOUSEBUTTONDOWN:
                pos = ev.pos
                r = pygame.Rect(pos[0]-1, pos[1]-1, 3, 3)
                if ev.button == 1:
                    pygame.draw.rect(screen, RED, r)
                    points.append(pos)

        pygame.display.update()

        # ask for confirmation
        if len(points) == 2:
            if ask_yes_no("Are the two points correct?"):
                if bwm_img.get_at(points[0]) == bwm_img.get_at(points[1]):
                    break
                else:
                    print("The two points aren't in the same surface")
                    screen.blit(maze_img, maze_rect)
                    points = []
            else:
                screen.blit(maze_img, maze_rect)
                points = []
            print("Click the two points to be connected...")

    # create the matrix and initialize it
    maze_matrix = MazeMatrix(maze_img, bwm_img, points)
    # find the distance
    dist = maze_matrix.solve()
    print("Found a path within {} pixels".format(dist))
    print("Drawing path...")

    maze_matrix.get_path()
    screen.blit(maze_matrix.maze_img, maze_rect)
    pygame.display.update()
    print("Path drawn")
    
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()