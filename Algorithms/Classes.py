import os
from collections import namedtuple

import numpy as np

point = namedtuple('point', ('x', 'y', 'z'))


def manh_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


class Cube:
    def __init__(self, d, w, h):
        self.depth = d      # x
        self.width = w      # y
        self.height = h     # z
        self.volume = d * w * h

    def set_depth(self, d):
        self.depth = d

    def get_depth(self):
        return self.depth

    def set_width(self, w):
        self.width = w

    def get_width(self):
        return self.width

    def set_height(self, h):
        self.height = h

    def get_height(self):
        return self.height

    def get_volume(self):
        return self.volume

    def set_(self, d, w, h):
        self.depth = d
        self.width = w
        self.height = h
        self.volume = d * w * h


class Box(Cube):
    def __init__(self, d, w, h):
        super().__init__(d, w, h)
        self.rotated = False

    def __repr__(self):
        return 'Box with depth = %i, width = %i, height = %i' % \
            (self.depth, self.width, self.height)

    # def __lt__(self, other):
    #     a, b, c = other.get_position()
    #     if self.z < c:
    #         return True
    #     elif self.z == c:
    #         if self.y < b:
    #             return True
    #         elif self.y == b:
    #             return self.x < a
    #         else:
    #             return False
    #     else:
    #         return False

    # def get_position(self):
    #     return point(x=self.x, y=self.y, z=self.z)

    def rotate(self):  # just support horizontal 90° rotation
        self.rotated = False if self.rotated else True
        t = self.width
        self.width = self.depth
        self.depth = t
        return self.rotated

    # def set_position(self, p):
    #     self.x = p.x
    #     self.y = p.y
    #     self.z = p.z


class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xy = np.array([[0 for j in range(y)] for i in range(x)])
        self.positions = list()
        # self.cod = np.zeros((x, y, z))

    def place_box(self, box):
        p = self.get_place_position(box)
        if p is None:
            return False
        else:
            self.positions.append(p)
            for i in range(p.x, p.x + box.get_depth()):
                for j in range(p.y, p.y + box.get_width()):
                    self.xy[i][j] = p.z + box.get_height()
            return True

    def get_positions(self):
        return self.positions

    def get_place_position(self, box):
        d = box.get_depth()
        w = box.get_width()
        h = box.get_height()

        max_dist = 0
        p = None
        for i in range(self.x):
            for j in range(self.y):
                if (i == 0 or self.xy[i - 1][j] > self.xy[i][j]) and (j == 0 or self.xy[i][j - 1] > self.xy[i][j]) \
                        and self.xy[i][j] + h <= self.z and i + d <= self.x and j + w <= self.y:
                    if self.stable(i, j, d, w, h):
                        dist = manh_dist((i + d, j + w, self.xy[i][j] + h), (self.x, self.y, self.z))
                        if dist > max_dist:
                            p = point(x=i, y=j, z=self.xy[i][j])
                            max_dist = dist
        return p

    def stable(self, x, y, d, w, h):
        # k = np.max(self.xy[x:x+d][y:y+w])
        k = 0
        for i in range(x, x + d):
            for j in range(y, y + w):
                k = max(k, self.xy[i][j])
        if k + h > self.z:
            return False
        return True

