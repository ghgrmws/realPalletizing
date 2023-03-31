from collections import namedtuple
from datetime import datetime
import numpy as np
from Algorithms import GeneticAlgorithm
from Algorithms.Classes import Coordinate
from methods import propose_strategy, get_data, generate_data

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

    N, D, W, H, boxes = get_data("Try\\1.csv")
    GeneticAlgorithm.solve(D, W, H, boxes)

    print(datetime.now() - start)

    return


if __name__ == '__main__':
    run()
    # test()
