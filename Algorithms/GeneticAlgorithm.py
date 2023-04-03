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
        num_box = len(self.placed_boxes)
        for i in range(num_box):
            for j in range(i + 1, num_box):
                ap = self.positions[i]
                ab = self.placed_boxes[i]
                bp = self.positions[j]
                bb = self.placed_boxes[j]
                if ap.x + ab.get_depth() <= bp.x or \
                        bp.x + bb.get_depth() <= ap.x or \
                        ap.y + ab.get_width() <= bp.y or \
                        bp.y + bb.get_width() <= ap.y or \
                        ap.z + ab.get_height() <= bp.z or \
                        bp.z + bb.get_height() <= ap.z:
                    continue
                else:
                    print(ap, ab)
                    print(bp, bb)
                    return False
        return True
