import math

from ortools.sat.python import cp_model
from methods import get_data


def resolve(file_path):
    N, L, W, H, boxes = get_data(file_path)

    outer = cp_model.CpModel()
    bs = list()
    vbs = list()  # volume of boxes
    for i in range(N):
        bs.append(outer.NewBoolVar('b' + str(i)))
        vbs.append(math.prod(boxes[i]))
        print('b' + str(i))

    print(boxes)
    print(vbs)

    outer_solver = cp_model.CpSolver()
    outer_status = outer_solver.Solve(outer)
    if outer_status == cp_model.OPTIMAL or outer_status == cp_model.FEASIBLE:
        for b in bs:
            print(b, "is", outer_solver.Value(b))
    else:
        print('No solution found.')
    return -1


def run():
    result = resolve("Data\\" + "0.csv")


def test():
    # no
    # a = 'abcd'
    # s = next(a)
    # print(a)
    #  哒咩
    return 0


if __name__ == '__main__':
    run()
    # test()
