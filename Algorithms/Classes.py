import os
from collections import namedtuple

import numpy as np

point = namedtuple('point', ('x', 'y', 'z'))


def manh_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


class Box:
    def __init__(self, d, w, h):
        self.depth = d  # x
        self.width = w  # y
        self.height = h  # z
        self.volume = d * w * h
        self.rotated = False

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

    def rotate(self):  # just support horizontal 90° rotation
        self.rotated = False if self.rotated else True
        t = self.width
        self.width = self.depth
        self.depth = t
        return self.rotated

    def __repr__(self):
        return 'Box with depth = %i, width = %i, height = %i' % \
            (self.depth, self.width, self.height)


# class Space:
#     def __init__(self, pa, pb):
#         self.lbb = pa
#         self.rft = pb
#         self.volume = (pb.x - pa.x) * (pb.y - pa.y) * (pb.z - pa.z)
#
#     def __lt__(self, other):
#         return self.lbb < other.get_lbb()
#
#     def get_lbb(self):  # left back bottom
#         return self.lbb
#
#     def get_rft(self):  # right front top
#         return self.rft
#
#     def get_volume(self):
#         return self.volume
#
#     def intersection(self, other):
#         opa = other.get_lbb()
#         opb = other.get_rft()
#         if self.rft.x < opa.x or self.lbb.x > opb.x or \
#                 self.rft.y < opa.y or self.lbb.y > opb.y or \
#                 self.rft.z < opa.z or self.lbb.z > opb.z:
#             return False
#         else:
#             lbb = point(x=max(self.lbb.x, opa.x), y=max(self.lbb.y, opa.y), z=max(self.lbb.z, opa.z))
#             rft = point(x=min(self.rft.x, opb.x), y=min(self.rft.y, opb.y), z=min(self.rft.z, opb.z))
#
#             return True


class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xy = np.array([[0 for j in range(y)] for i in range(x)])
        self.positions = list()

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

        # p = None
        # for z in range(self.z - h):
        #     ps = set()
        #     for i in range(self.x - d):
        #         j = self.y - 1
        #         while True:
        #             break

        p = None
        max_dist = 0
        for i in range(self.x - d):
            for j in range(self.y - w):
                z = self.stable(i, j, d, w, h)
                if z is not False:
                    dist = manh_dist((i + d, j + w, z + h), (self.x, self.y, self.z))
                    if dist > max_dist:
                        p = point(x=i, y=j, z=z)
                        max_dist = dist
        return p

    def stable(self, x, y, d, w, h):
        # legal_height = np.max(self.xy[x:x+d][y:y+w])
        legal_height = 0
        for i in range(x, x + d):
            for j in range(y, y + w):
                k = max(legal_height, self.xy[i][j])
        if legal_height + h > self.z:
            return False
        else:
            return legal_height
