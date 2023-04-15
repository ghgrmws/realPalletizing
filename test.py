from collections import namedtuple
from datetime import datetime
import numpy as np
from Algorithms.GeneticAlgorithm import Genetic
from Algorithms.Classes import Coordinate, Space
from methods import get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def test():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    b = [1, 3, 5, 7, 9]
    print(a + b)
    return 0


def run():
    start = datetime.now()
    N, D, W, H, boxes = get_data("Try\\1.csv")  # 0.834807
    ga = Genetic(D, W, H, boxes)
    print('The utilization is %f' % ga.solve())
    print(datetime.now() - start)
    print(ga.check())
    ga.print_solution("out.txt")
    return


if __name__ == '__main__':
    run()
    # test()
