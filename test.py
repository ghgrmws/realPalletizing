from collections import namedtuple
from datetime import datetime
import numpy as np
from Algorithms.GeneticAlgorithm import Genetic
from Algorithms.Classes import Coordinate
from methods import get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def test():
    with open("Try\\0.csv", "r") as f:
        head = f.readline().split(',')
        D = int(head[0])
        W = int(head[1])
        H = int(head[2])

        contents = f.readline().split(', ')
        data = list()
        for s in contents:
            k = 0
            for c in s:
                if c == '[' or c == ']':
                    continue
                else:
                    k *= 10
                    k += int(c)
            data.append(k)
    with open("Try/0.csv", "a") as f:
        f.write('%i,%i,%i' % (D, W, H))
        for i in range(len(data)):
            if i % 3:
                f.write(',')
            else:
                f.write('\n')
            f.write(str(data[i]))


def run():
    start = datetime.now()
    N, D, W, H, boxes = get_data("Try\\0.csv")  # 0.665602
    ga = Genetic(D, W, H, boxes)
    print('The utilization is %f' % ga.solve())
    print(datetime.now() - start)
    print(ga.check())
    return


if __name__ == '__main__':
    run()
    # test()
