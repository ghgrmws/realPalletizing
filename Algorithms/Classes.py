from collections import namedtuple

point = namedtuple('point', ('x', 'y', 'z'))


class Box:
    def __init__(self, w, h, d, x=0, y=0, z=0):
        self.width = w
        self.height = h
        self.depth = d
        self.x = x
        self.y = y
        self.z = z
        self.volume = w * h * d

    def __repr__(self):
        return 'Box (with width = %i, height = %i, depth = %i) is placed at (%i, %i, %i)' % \
            (self.width, self.height, self.depth, self.x, self.y, self.z)

    def __lt__(self, other):
        a, b, c = other.get_position()
        if self.z < c:
            return True
        elif self.z == c:
            if self.y < b:
                return True
            elif self.y == b:
                return self.x < a
            else:
                return False
        else:
            return False

    def get_position(self):
        return self.x, self.y, self.z

    def rotate(self):  # just support horizontal 90° rotation
        if self.width == self.depth:
            return False
        else:
            t = self.width
            self.width = self.depth
            self.depth = t
            return self

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


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
