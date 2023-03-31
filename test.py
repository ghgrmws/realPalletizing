from collections import namedtuple
from datetime import datetime
import numpy as np
from Algorithms.GeneticAlgorithm import Genetic
from Algorithms.Classes import Coordinate
from methods import get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def test():
    for i in range(10):
        for j in range(10):
            print(i * 10 + j)
            if (i * 10 + j) == 15:
                break
        else:
            continue
        break


def run():
    start = datetime.now()

    N, D, W, H, boxes = get_data("Data\\1.csv")
    ga = Genetic(D, W, H, boxes)
    print('The utilization is %f' % ga.solve())
    print(datetime.now() - start)
    print(ga.check())
    return


if __name__ == '__main__':
    run()
    # test()
