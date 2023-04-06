from collections import namedtuple

from Algorithms.Classes import Coordinate, Tree, TreeNode, Space


point = namedtuple('point', ('x', 'y', 'z'))


def manh_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


class Genetic:
    def __init__(self, D, W, H, boxes):
        self.D = D
        self.W = W
        self.H = H
        self.all_boxes = boxes
        self.num_boxes = len(boxes)
        self.placed_boxes = list()
        self.positions = list()
        self.utilization = -1

    def solve_with_coordinate(self):
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

    def solve(self):
        seq = [i for i in range(self.num_boxes)]

    def solve_with_tree(self, seq):
        space = Space(point(x=0, y=0, z=0), point(x=self.D, y=self.W, z=self.H))
        # seq = [i for i in range(num_boxes)]  # genes value & box id

        tree = Tree(space)
        v = 0
        for i in seq:
            leaves = tree.get_all_leaves()
            num_leaves = len(leaves)
            box = self.all_boxes[seq[i]]
            d = box.get_depth()
            w = box.get_width()
            h = box.get_height()

            max_dist = 0
            selected = None
            for j in range(num_leaves):
                sp = leaves[j].get_obj()
                lbb = sp.get_lbb()
                rft = sp.get_rft()
                if rft.x - lbb.x >= d and rft.y - lbb.y >= w and rft.z - lbb.z >= h:
                    dist = manh_dist(point(x=lbb.x + d, y=lbb.y + w, z=lbb.z + h), point(x=self.D, y=self.W, z=self.H))
                    if dist > max_dist:
                        max_dist = dist
                        selected = j

            if selected is not None:
                lbb = leaves[selected].get_obj().get_lbb()
                box_space = Space(lbb, point(x=lbb.x + d, y=lbb.y + w, z=lbb.z + h))
                for node in leaves:
                    sp = node.get_obj()
                    sub_spaces = sp.intersection(box_space)
                    if sub_spaces is not None:
                        children = list()
                        for sb_ps in sub_spaces:
                            children.append(TreeNode(node, sb_ps, None))
                        node.set_children(children)

                self.positions.append(lbb)
                self.placed_boxes.append(box)
                v += self.all_boxes[i].get_volume()

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
