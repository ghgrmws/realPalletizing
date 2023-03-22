import math
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from methods import get_data


"""
    Practical constraints in the container loading problem: Comprehensive formulations and exact algorithm
"""


# def resolve_by_cp_model(file_path):
#     N, L, W, H, boxes = get_data(file_path)
#
#     outer = cp_model.CpModel()
#     L = outer.NewConstant(L)
#     W = outer.NewConstant(W)
#     H = outer.NewConstant(H)
#
#     b = list()
#     l = list()
#     w = list()
#     h = list()
#     for i in range(N):
#         b.append(outer.NewBoolVar('b' + str(i)))
#         l.append(outer.NewConstant(boxes[i][0]))
#         w.append(outer.NewConstant(boxes[i][1]))
#         h.append(outer.NewConstant(boxes[i][2]))
#
#     print(type(b[0]))
#
#     # outer.Add(sum(b * l * w * h))
#
#     outer.Maximize(sum(b))
#
#     while True:
#         outer_solver = cp_model.CpSolver()
#         # outer_status = outer_solver.Solve(outer)
#
#         solution_printer = cp_model.VarArraySolutionPrinter(b)
#         outer_solver.parameters.enumerate_all_solutions = True
#         outer_status = outer_solver.Solve(outer, solution_printer)
#
#         inner = cp_model.CpModel()
#
#         inner_bs = list()
#         if outer_status == cp_model.OPTIMAL or outer_status == cp_model.FEASIBLE:
#             for i in range(N):
#                 if outer_solver.Value(b[i]):
#                     inner.NewBoolVar(str(b))
#                     inner_bs.append(b)
#         else:
#             print('No solution found in outer layer.')
#             break
#
#     return -1
#
#
# def run_cp_model():
#     result = resolve_by_cp_model("Data\\" + "0.csv")


def make_constraints(U, L, W, H):
    constraints = {
        'bounds': [L, W, H, 0, 0, 0, 0, 0, 0, 1, 1]
    }
    return constraints


def resolve_by_linear_solver(file_path):
    N, L, W, H, boxes = get_data(file_path)

    data = {
        'length': [box[0] for box in boxes],
        'width': [box[1] for box in boxes],
        'height': [box[2] for box in boxes],
    }

    outer = pywraplp.Solver.CreateSolver('SCIP')

    u = {}
    for i in range(N):
        u[i] = outer.BoolVar('u[%i]' % i)

    outer_constraint = outer.RowConstraint(0, L * W * H, '')
    for i in range(N):
        outer_constraint.SetCoefficient(u[i], data['length'][i] * data['width'][i] * data['height'][i])

    outer_objective = outer.Objective()
    for i in range(N):
        outer_objective.SetCoefficient(u[i], data['length'][i] * data['width'][i] * data['height'][i])
    outer_objective.SetMaximization()

    while True:

        inner = pywraplp.Solver.CreateSolver('SCIP')

        sub_u = {}

        U = 0  # the number of selected boxes in the outer layer
        outer_status = outer.Solve()
        if outer_status == pywraplp.Solver.OPTIMAL:
            print('Outer objective value =', outer.Objective().Value())
            for i in range(N):
                if u[i].solution_value() > 0:
                    sub_u[U] = u[i]
                    U += 1
                # print(u[i].name(), ' = ', u[i].solution_value())
            print(sub_u)
            # print('Outer problem solved in %f milliseconds' % outer.wall_time())
        else:
            print('The outer problem does not have an optimal solution.')

        v = {}
        max_ite = U * (L * W + L * H + W * H)
        for i in range(max_ite):
            v[i] = inner.BoolVar('v[%i]' % i)

        constraints = make_constraints(U, L, W, H)
        inner_constraint = inner.RowConstraint(0, H, '')

    return -1


def run_linear_solver():
    result = resolve_by_linear_solver("Data\\" + "0.csv")


if __name__ == '__main__':
    # run_cp_model()
    run_linear_solver()

