from collections import namedtuple

point = namedtuple('point', ('x', 'y', 'z'))


class Box:
    def __init__(self, w, h, d):
        self.width = w
        self.height = h
        self.depth = d
        self.volume = w * h * d

    def rotate(self):  # just support horizontal 90° rotation
        if self.width == self.depth:
            return False
        else:
            t = self.width
            self.width = self.depth
            self.depth = t
            return self


class Space:
    def __init__(self, w, h, d):
        self.width = w
        self.height = h
        self.depth = d
        self.volume = w * h * d
        self.legal_x = [0]
        self.legal_y = [0]
        self.legal_z = [0]
        self.box_sequence = list()

    def all_legal_points(self):
        points = set()
        for x in self.legal_x:
            for y in self.legal_y:
                for z in self.legal_z:
                    points.add(point(x=x, y=y, z=z))

        return points

