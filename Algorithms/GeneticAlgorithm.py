from Algorithms.Classes import Coordinate
import numpy as np


class Genetic:
    def __init__(self, D, W, H, boxes):
        self.D = D
        self.W = W
        self.H = H
        self.all_boxes = boxes
        self.placed_boxes = list()
        self.positions = list()
        self.utilization = -1

    def solve(self):
        space = Coordinate(self.D, self.W, self.H)
        num_boxes = len(self.all_boxes)
        seq = [i for i in range(num_boxes)]  # genes value & box id
        # random.shuffle(seq)
        v = 0
        for i in seq:
            if space.place_box(self.all_boxes[i]):
                self.placed_boxes.append(self.all_boxes[i])
                v += self.all_boxes[i].get_volume()
        self.positions = space.get_positions()
        self.utilization = v / (self.D * self.W * self.H)
        return self.utilization

    def check(self):
        s = -np.ones((self.D, self.W, self.H))
        NB = len(self.placed_boxes)
        for i in range(NB):
            p = self.positions[i]
            b = self.placed_boxes[i]
            for w in range(b.get_width()):
                for h in range(b.get_width()):
                    for d in range(b.get_width()):
                        if s[p.x + d][p.y + w][p.z + h] != -1:
                            return False
                        else:
                            s[p.x + d][p.y + w][p.z + h] = i
        return True
