from Algorithms.Classes import Coordinate


def solve(D, W, H, boxes):
    space = Coordinate(D, W, H)
    num_boxes = len(boxes)
    seq = [i for i in range(num_boxes)]  # genes value & box id
    # random.shuffle(seq)

    v = 0
    for i in seq:
        space.place_box(boxes[i])
        v += boxes[i].get_volume()
