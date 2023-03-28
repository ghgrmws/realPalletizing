import math

import numpy as np
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from methods import get_data


###
# Practical constraints in the container loading problem: Comprehensive formulations and exact algorithm
###


def box_rotation(boxes, N):
    new_boxes = list()
    for b in boxes[:N]:
        new_boxes.append([b[0], b[1], b[2]])
        new_boxes.append([b[2], b[1], b[0]])
    return new_boxes


def print_solution(solver, x, y, z, b, V, v, data, file_path):
    with open(file_path + '.out', 'a') as f:
        f.write("box_id,width,height,depth,x,y,z\n")
        for i in range(V):
            box = v[i]
            f.write(str(box) + ',')  # box id
            f.write(str(data['width'][v[i]]) + ',')
            f.write(str(data['height'][v[i]]) + ',')
            f.write(str(data['depth'][v[i]]) + ',')
            f.write(str(solver.Value(x[i])) + ',')  # placed position x
            f.write(str(solver.Value(y[i])) + ',')
            f.write(str(solver.Value(z[i])) + '\n')
        f.write("box_a,box_b,satisfied_constraint\n")
        for i in range(V):
            for j in range(i + 1, V):
                for k in range(6):
                    if solver.BooleanValue(b[i][j][k]):
                        box_a = v[i]
                        box_b = v[j]
                        f.write(str(box_a) + ',' + str(box_b) + ',' + str(k) + '\n')


def check_correctness(solver, x, y, z, v, V, W, H, D, data):
    s = -np.ones((W + 1, H + 1, D + 1))
    for i in range(V):
        px = solver.Value(x[i])
        py = solver.Value(y[i])
        pz = solver.Value(z[i])
        for w in range(data['width'][v[i]]):
            for h in range(data['height'][v[i]]):
                for d in range(data['depth'][v[i]]):
                    # print(px, py, pz, data['width'][v[i]], data['height'][v[i]], data['depth'][v[i]])
                    if s[px + w][py + h][pz + d] != -1:
                        print("It's incorrect!")
                    else:
                        s[px + w][py + h][pz + d] = v[i]
    print("It's correct!")


def resolve(file_path):
    running_time = 0

    N, W, H, D, boxes = get_data(file_path)

    boxes = box_rotation(boxes, N)
    N = len(boxes)

    data = {
        'width': [box[0] for box in boxes],
        'height': [box[1] for box in boxes],
        'depth': [box[2] for box in boxes],
    }

    outer = pywraplp.Solver.CreateSolver('SCIP')

    u = {}
    arg_u = {}
    for i in range(N):
        u[i] = outer.BoolVar('u[%i]' % i)
        arg_u[u[i]] = i

    outer_constraint = outer.RowConstraint(0, W * H * D, '')
    for i in range(N):
        outer_constraint.SetCoefficient(u[i], data['width'][i] * data['height'][i] * data['depth'][i])
    for i in range(0, N, 2):
        outer_constraint = outer.RowConstraint(0, 1, '')
        outer_constraint.SetCoefficient(u[i], 1)
        outer_constraint.SetCoefficient(u[i + 1], 1)

    outer_objective = outer.Objective()
    for i in range(N):
        outer_objective.SetCoefficient(u[i], data['width'][i] * data['height'][i] * data['depth'][i])
    outer_objective.SetMaximization()

    while True:

        v = {}  # subset of U

        V = 0  # the number of selected boxes in the outer layer
        outer_status = outer.Solve()
        if outer_status == pywraplp.Solver.OPTIMAL:
            running_time += outer.wall_time() / 1000  # transform millisecond to second here
            for i in range(N):
                if u[i].solution_value() > 0:
                    v[V] = arg_u[u[i]]
                    V += 1
        else:
            print('The outer problem does not have an optimal solution.')
            return

        inner = cp_model.CpModel()

        x = {}
        y = {}
        z = {}
        b = [[list() for i in range(V)] for j in range(V)]

        # every box should be totally in the space
        for i in range(V):
            x[i] = inner.NewIntVar(0, W - data['width'][v[i]], 'x[%i]' % i)
            y[i] = inner.NewIntVar(0, H - data['height'][v[i]], 'y[%i]' % i)
            z[i] = inner.NewIntVar(0, D - data['depth'][v[i]], 'z[%i]' % i)
            for j in range(i + 1, V):
                for k in range(6):
                    b[i][j].append(inner.NewBoolVar('b[%i][%i][%i]' % (i, j, k)))

        for i in range(V):
            for j in range(i + 1, V):
                inner.Add(x[i] + data['width'][v[i]] - x[j] <= 0).OnlyEnforceIf(b[i][j][0])
                inner.Add(x[j] + data['width'][v[j]] - x[i] <= 0).OnlyEnforceIf(b[i][j][1])
                inner.Add(y[i] + data['height'][v[i]] - y[j] <= 0).OnlyEnforceIf(b[i][j][2])
                inner.Add(y[j] + data['height'][v[j]] - y[i] <= 0).OnlyEnforceIf(b[i][j][3])
                inner.Add(z[i] + data['depth'][v[i]] - z[j] <= 0).OnlyEnforceIf(b[i][j][4])
                inner.Add(z[j] + data['depth'][v[j]] - z[i] <= 0).OnlyEnforceIf(b[i][j][5])
                inner.AddBoolOr(b[i][j])

        inner_solver = cp_model.CpSolver()

        # Solve.
        inner_status = inner_solver.Solve(inner)

        running_time += inner_solver.WallTime()
        # inner returns in seconds, but outer returns in milliseconds

        if inner_solver.StatusName(inner_status) == 'INFEASIBLE':
            print('Outer objective value =', outer.Objective().Value())
            print('The total running time is %i.' % running_time)
            outer_constraint = outer.RowConstraint(0, V - 1, '')
            for i in range(V):
                outer_constraint.SetCoefficient(u[v[i]], 1)
            print('Number of constraints =', outer.NumConstraints())
        else:
            print('')
            print('Outer objective value =', outer.Objective().Value())
            print('The total running time is %i.' % running_time)
            check_correctness(inner_solver, x, y, z, v, V, W, H, D, data)
            print_solution(inner_solver, x, y, z, b, V, v, data, file_path)
            return


def main():
    resolve("Try\\" + "1.csv")


if __name__ == '__main__':
    main()
