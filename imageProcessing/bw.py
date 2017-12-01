from PIL import Image
import sys
import os

def makeBlackAndWhite(imgpath):
    img = Image.open(imgpath)
    pixelMap = img.load()
    width, height = img.size

    totalL = 0
    for i in range(width):
        for j in range(height):
            p = pixelMap[i, j]
            L = int(p[0]*0.2126)+int(p[1]*0.7152)+int(p[2]*0.0722)
            pixelMap[i, j] = (L, L, L)

    head, tail = os.path.split(imgpath)
    newpath = os.path.join(head, "BW"+tail)
    img.save(newpath)

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except Exception:
        path = input("img path >> ")
    makeBlackAndWhite(path)