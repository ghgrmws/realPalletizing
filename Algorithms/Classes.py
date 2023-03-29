from collections import namedtuple

point = namedtuple('point', ('x', 'y', 'z'))


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

    def set_(self, d, w, h):
        self.depth = d
        self.width = w
        self.height = h
        self.volume = d * w * h


class Box(Cube):
    def __init__(self, d, w, h, x, y, z):
        super().__init__(d, w, h)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Box (with depth = %i, width = %i, height = %i) is placed at (%i, %i, %i)' % \
            (self.depth, self.width, self.height, self.x, self.y, self.z)

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
        return point(x=self.x, y=self.y, z=self.z)

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