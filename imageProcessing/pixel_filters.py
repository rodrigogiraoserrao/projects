from random import shuffle
from math import ceil

def pixelize(img, boxsize=10):
    pixel_map = img.load()
    width, height = img.size

    for i in range(ceil(width/boxsize)):
        for j in range(ceil(height/boxsize)):
            pixels = []
            sums = [0,0,0]
            for xi in range(i*boxsize, min((i+1)*boxsize, width)):
                for yj in range(j*boxsize, min((j+1)*boxsize, height)):
                    pixels.append([xi, yj])
                    for c in range(3):
                        sums[c] += pixel_map[xi,yj][c]
            avg = tuple([int(sums[i]/len(pixels)) for i in range(3)])
            for pix in pixels:
                pixel_map[pix[0], pix[1]] = tuple(avg)

    return img

def pixel_box_shuffle(img, boxsize=10):
    pixel_map = img.load()
    width, height = img.size

    for i in range(ceil(width/boxsize)):
        for j in range(ceil(height/boxsize)):
            pixels = []
            colours = []
            for xi in range(i*boxsize, min((i+1)*boxsize, width)):
                for yj in range(j*boxsize, min((j+1)*boxsize, height)):
                    pixels.append([xi, yj])
                    colours.append(pixel_map[xi, yj])
            shuffle(pixels)
            for k, pix in enumerate(pixels):
                pixel_map[pix[0], pix[1]] = colours[k]

    return img