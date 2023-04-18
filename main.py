from collections import namedtuple
from datetime import datetime
from Algorithms.GeneticAlgorithm import Genetic
from Algorithms.Classes import Coordinate, Space
from methods import get_data, generate_data

point = namedtuple('point', ('x', 'y', 'z'))


def test():

    return 0


def run():
    date_form = '%m-%d %H-%M-%S'
    start = datetime.now()
    N, D, W, H, boxes = get_data("Data\\0.csv")  # 0.834807
    ga = Genetic(D, W, H, boxes)
    print('The utilization is %f' % ga.solve())
    print(datetime.now() - start)
    print(ga.check())
    ga.save_solution("Data\\(0)%s.out" % str(datetime.now().strftime(date_form)))
    return


if __name__ == '__main__':
    run()
    # test()
