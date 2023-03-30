from collections import namedtuple

import numpy as np
from Algorithms import GeneticAlgorithm
from Algorithms.Classes import Coordinate
from methods import propose_strategy, get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def run():
    N, D, W, H, boxes = get_data("Data\\1.csv")
    GeneticAlgorithm.solve(D, W, H, boxes)
    return


if __name__ == '__main__':
    run()
