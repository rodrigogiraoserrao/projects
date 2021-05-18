"""
Simple example of using __getitem__ to define indexing/slicing for custom objects.
Read the article https://mathspp.com/blog/pydonts/inner-workings-of-sequence-slicing for more information.
"""

import sys

class GeometricProgression:
    def __init__(self, start, ratio):
        self.start = start
        self.ratio = ratio

    def __str__(self):
        return f"GeometricProgression({self.start}, {self.ratio})"

    def nth(self, n):
        """Compute the n-th term of the progression, 0-indexed."""
        return self.start*pow(self.ratio, n)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.nth(idx)
        elif isinstance(idx, slice):
            start, stop, step = idx.start or 0, idx.stop or sys.maxsize, idx.step or 1
            return [self.nth(n) for n in range(start, stop, step)]
        elif isinstance(idx, tuple):
            return [self.__getitem__(sub_idx) for sub_idx in idx]
        else:
            raise TypeError("Geo. progression indices should be integers or slices.")

if __name__ == "__main__":
    gp = GeometricProgression(1, 3)
    print(gp)                       # GeometricProgression(1, 3)
    print(gp[0])                    # 1
    print(gp[1])                    # 3
    print(gp[2])                    # 9
    print(gp[0:3])                  # [1, 3, 9]
    print(gp[1:10:3])               # [3, 81, 2187]
    print(gp[0, 1, 4])              # [1, 3, 81]
    print(gp[0:2, 0:2, 1, 0:2])     # [[1, 3], [1, 3], 3, [1, 3]]
