from collections import namedtuple
from datetime import datetime
import numpy as np
from Algorithms.GeneticAlgorithm import Genetic
from Algorithms.Classes import Coordinate, Space
from methods import get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def test():
    # test. test !
    return 0


def run():
    start = datetime.now()
    N, D, W, H, boxes = get_data("Try\\0.csv")  # 0.834807
    ga = Genetic(D, W, H, boxes)
    print('The utilization is %f' % ga.solve())
    print(datetime.now() - start)
    print(ga.check())
    return


if __name__ == '__main__':
    run()
    # test()
