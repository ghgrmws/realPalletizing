from collections import namedtuple
from datetime import datetime
import numpy as np
from Algorithms.GeneticAlgorithm import Genetic
from Algorithms.Classes import Coordinate, Space
from methods import get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def test():
    # a = point(x=0, y=0, z=0)
    # b = point(x=2, y=2, z=2)
    # c = point(x=1, y=1, z=1)
    # d = point(x=3, y=3, z=3)
    #
    # sa = Space(a, b)
    # sb = Space(c, d)
    # sin = sb.intersection(sa)
    # print(sa.cut_space(sin))

    s = set()
    s.add(3)
    s.add(4)
    s.add(5)
    cas = 0
    for k in s:
        s.remove(k)
        for i in range(k):
            s.add(cas)
            cas += 1
            print(s)
            a =  10
    return 0


def run():
    start = datetime.now()
    N, D, W, H, boxes = get_data("Try\\0.csv")  # 0.665602
    ga = Genetic(D, W, H, boxes)
    print('The utilization is %f' % ga.solve())
    print(datetime.now() - start)
    print(ga.check())
    return


if __name__ == '__main__':
    # run()
    test()
