def average_smooth(img, boxsize=10):
    pixel_map = img.load()
    width, height = img.size
    l = boxsize//2

    for x in range(width):
        for y in range(height):
            sums = [0, 0, 0]
            count = 0
            for i in range(max(x-l, 0), min(x+l, width)):
                for j in range(max(y-l, 0), min(y+l, height)):
                    for c in range(3):
                        sums[c] += pixel_map[i, j][c]
                    count += 1
            avg = [sums[c]//count for c in range(3)]
            pixel_map[x, y] = tuple(avg)
    
    return img