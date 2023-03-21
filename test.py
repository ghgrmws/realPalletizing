import math

from ortools.sat.python import cp_model
from methods import get_data


def resolve(file_path):
    N, L, W, H, boxes = get_data(file_path)

    outer = cp_model.CpModel()
    L = outer.NewConstant(L)
    W = outer.NewConstant(W)
    H = outer.NewConstant(H)

    b = list()
    l = list()
    w = list()
    h = list()
    for i in range(N):
        b.append(outer.NewBoolVar('b' + str(i)))
        l.append(outer.NewConstant(boxes[i][0]))
        w.append(outer.NewConstant(boxes[i][1]))
        h.append(outer.NewConstant(boxes[i][2]))

    # outer.Add()

    for i in range(N):
        outer.Maximize(b[i] * l[i] * w[i] * h[i])

    while True:
        outer_solver = cp_model.CpSolver()
        outer_status = outer_solver.Solve(outer)

        inner = cp_model.CpModel()

        inner_bs = list()
        if outer_status == cp_model.OPTIMAL or outer_status == cp_model.FEASIBLE:
            for i in range(N):
                if outer_solver.Value(b[i]):
                    inner.NewBoolVar(str(b))
                    inner_bs.append(b)
        else:
            print('No solution found in outer layer.')
            break

    return -1


def run():
    result = resolve("Data\\" + "0.csv")


if __name__ == '__main__':
    run()
