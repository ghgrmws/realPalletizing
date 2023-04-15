import copy
import os
import random
from collections import namedtuple
from multiprocessing import Pool

from Algorithms.Classes import Tree, TreeNode, Space


point = namedtuple('point', ('x', 'y', 'z'))


def manh_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


class Chromosome:
    def __init__(self, seq, positions, v):
        self.seq = seq
        self.positions = positions
        self.L = len(seq)
        self.cur = 0
        self.value = v

    def randomize(self):
        random.shuffle(self.seq)
        self.cur = 0
        self.value = -1

    def normalization(self, selected):
        L = len(selected)
        for i in range(self.L):
            if selected[self.cur] == self.seq[i]:
                del self.seq[i]
                self.seq.insert(self.cur, selected[self.cur])
                self.cur += 1
            if self.cur >= L:
                break

    def get_seq(self):
        return self.seq

    def new_mutation(self):
        seq = copy.deepcopy(self.seq)

        c = Chromosome()


class Genetic:
    def __init__(self, D, W, H, boxes):
        self.D = D
        self.W = W
        self.H = H
        self.all_boxes = boxes
        self.num_boxes = len(boxes)
        self.limit = [D, W, H]
        for box in boxes:
            d = box.get_depth()
            w = box.get_width()
            h = box.get_height()
            self.limit[0] = min(self.limit[0], d)
            self.limit[1] = min(self.limit[1], w)
            self.limit[2] = min(self.limit[2], h)
        self.positions = None
        self.selected_boxes = None
        self.utilization = None

    # def solve_with_coordinate(self):
    #     space = Coordinate(self.D, self.W, self.H)
    #     num_boxes = len(self.all_boxes)
    #     seq = [i for i in range(num_boxes)]  # genes value & box id
    #     # random.shuffle(seq)
    #     v = 0
    #     for i in seq:
    #         if space.place_box(self.all_boxes[i]):
    #             self.placed_boxes.append(self.all_boxes[i])
    #             v += self.all_boxes[i].get_volume()
    #     self.positions = space.get_positions()
    #     self.utilization = v / (self.D * self.W * self.H)
    #     return self.utilization

    def solve(self, num_process=20):
        positions = None
        selected_boxes = None

        pool = Pool(num_process)
        pool_results = list()
        parent_size = 20
        old_chromosomes = list()
        max_v = 0
        seqs = [i for i in range(self.num_boxes)]
        for i in range(parent_size * 3):
            random.shuffle(seqs)
            pool_results.append(pool.apply_async(self.decode, args=(seqs,)))
        pool.close()
        pool.join()
        for res in pool_results:
            v, seq, ps, bs = res.get()
            if v > max_v:
                max_v = v
                positions = ps
                selected_boxes = bs
            chromosome = Chromosome(seq, positions, v)
            chromosome.normalization(bs)

            old_chromosomes.append()

        max_generation = 20
        generation = 0
        new_chromosomes = list()
        while generation < max_generation:
            for i in range(parent_size):
                a, b = random.sample(old_chromosomes, 2)
                if a[0] > b[0]:
                    new_chromosomes.append(a)
                else:
                    new_chromosomes.append(b)

            pool = Pool(num_process)
            pool_results = list()

            # mutate
            mute_times = 20
            for i in range(mute_times):
                chromosome = random.choice(new_chromosomes)
                a, b = random.sample(range(self.num_boxes), 2)
                t = chromosome[1][a]
                chromosome[1][a] = chromosome[1][b]
                chromosome[1][b] = t
                pool_results.append(pool.apply_async(self.decode, args=(chromosome[1],)))
            pool.close()
            pool.join()
            for re in pool_results:
                ret = re.get()
                new_chromosomes.append([ret[0], ret[1]])
                if ret[0] > max_v:
                    max_v = ret[0]
                    positions = ret[2]
                    selected_boxes = ret[3]
            generation += 1
            print("Generation %i with utilization %f" % (generation, max_v / (self.D * self.W * self.H)))

        self.positions = positions
        self.selected_boxes = selected_boxes
        self.utilization = max_v / (self.D * self.W * self.H)
        return self.utilization

    def decode(self, chromosome):
        print('Run task in (%s)...' % os.getpid())
        seq = chromosome.get_seq()

        positions = list()
        selected_boxes = list()

        space = Space(point(x=0, y=0, z=0), point(x=self.D, y=self.W, z=self.H))

        tree = Tree(space)
        v = 0
        for i in seq:
            leaves = tree.get_all_leaves()
            num_leaves = len(leaves)
            box = self.all_boxes[i]
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
                selected_node = leaves[selected]
                lbb = selected_node.get_obj().get_lbb()
                box_space = Space(lbb, point(x=lbb.x + d, y=lbb.y + w, z=lbb.z + h))

                selected_boxes.append(i)
                positions.append(lbb)

                for node in leaves:
                    sp = node.get_obj()
                    sub_spaces = sp.intersection(box_space)
                    if sub_spaces is not None:
                        children = list()
                        for sb_ps in sub_spaces:
                            if sb_ps.large_enough(self.limit):
                                children.append(TreeNode(node, sb_ps, None))
                        node.set_children(children)

                v += self.all_boxes[i].get_volume()
        return v, seq, positions, selected_boxes

    def check(self):
        num_box = len(self.selected_boxes)
        for i in range(num_box):
            for j in range(i + 1, num_box):
                ap = self.positions[i]
                ab = self.all_boxes[self.selected_boxes[i]]
                bp = self.positions[j]
                bb = self.all_boxes[self.selected_boxes[j]]
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

    def print_solution(self, file_path):
        if self.utilization is None:
            self.utilization = self.solve()
        num_box = len(self.selected_boxes)
        boxes = list()
        for i in range(num_box):
            p = self.positions[i]
            box = self.all_boxes[self.selected_boxes[i]]
            box.set_position(p)
            boxes.append(box)
        boxes.sort()

        with open(file_path, "a+") as f:
            for box in boxes:
                f.write(str(box) + '\n')

        return boxes
