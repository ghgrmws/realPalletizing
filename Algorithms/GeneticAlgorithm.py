import os
import random

from Algorithms.Classes import Coordinate


def solve(D, W, H, boxes):
    space = Coordinate(D, W, H)
    num_boxes = len(boxes)
    seq = [i for i in range(num_boxes)]  # genes value & box id
    # random.shuffle(seq)
    v = 0
    for b in boxes:
        ps = space.show_legal_corners(b)
        print(ps)
        if len(ps) > 0:
            space.place_box(ps[0], b)
            v += b.get_volume()
        # os.system("pause >nul")
    print(D * W * H, v)
