from enum import Enum

class Colour(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

def hinder(img, colour, per=0.5):
    pixel_map = img.load()
    width, height = img.size

    for i in range(width):
        for j in range(height):
            p = list(pixel_map[i, j])
            p[colour] = int(per*p[colour])
            pixel_map[i, j] = tuple(p)

    return img

def hinder_red(img, per=0.5):
    return hinder(img, Colour.RED, per)

def hinder_green(img, per=0.5):
    return hinder(img, Colour.GREEN, per)

def hinder_blue(img, per=0.5):
    return hinder(img, Colour.BLUE, per)

def enhance(img, colour, per=0.5):
    pixel_map = img.load()
    width, height = img.size

    i1 = (colour.value+1)%3
    i2 = 3-i1-colour.value
    for i in range(width):
        for j in range(height):
            p = list(pixel_map[i, j])
            p[i1] = int(per*p[i1])
            p[i2] = int(per*p[i2])
            pixel_map[i, j] = tuple(p)

    return img

def enhance_red(img, per=0.5):
    return enhance(img, Colour.RED, per)

def enhance_green(img, per=0.5):
    return enhance(img, Colour.GREEN, per)

def enhance_blue(img, per=0.5):
    return enhance(img, Colour.BLUE, per)