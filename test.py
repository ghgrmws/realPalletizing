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
        'num_constraints': U * (L * W + L * H, W * H),
        'constraint_coeffs': list(),
        'bounds': [L, W, H, 0, 0, 0, 0, 0, 0, 1, 1]
    }

    # xxx <= L

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
    arg_u = {}
    for i in range(N):
        u[i] = outer.BoolVar('u[%i]' % i)
        arg_u[u[i]] = i

    outer_constraint = outer.RowConstraint(0, L * W * H, '')
    for i in range(N):
        outer_constraint.SetCoefficient(u[i], data['length'][i] * data['width'][i] * data['height'][i])

    outer_objective = outer.Objective()
    for i in range(N):
        outer_objective.SetCoefficient(u[i], data['length'][i] * data['width'][i] * data['height'][i])
    outer_objective.SetMaximization()

    while True:

        v = {}  # subset of U

        V = 0  # the number of selected boxes in the outer layer
        outer_status = outer.Solve()
        if outer_status == pywraplp.Solver.OPTIMAL:
            print('Outer objective value =', outer.Objective().Value())
            for i in range(N):
                if u[i].solution_value() > 0:
                    v[V] = arg_u[u[i]]
                    V += 1
                # print(u[i].name(), ' = ', u[i].solution_value())
            print(v)
            # print('Outer problem solved in %f milliseconds' % outer.wall_time())
        else:
            print('The outer problem does not have an optimal solution.')

        inner = cp_model.CpModel()

        dom = cp_model.Domain(0, 10)
        # print(dom.AllValues())

        x = {}
        y = {}
        z = {}
        b = [[list() for i in range(V)] for j in range(V)]

        # every box should be totally in the space
        for i in range(V):
            x[i] = inner.NewIntVar(0, L - data['length'][i], 'x[%i]' % i)
            y[i] = inner.NewIntVar(0, W - data['width'][i], 'y[%i]' % i)
            z[i] = inner.NewIntVar(0, H - data['height'][i], 'z[%i]' % i)
            for j in range(i + 1, V):
                for k in range(6):
                    b[i][j].append(inner.NewBoolVar('b[%i][%i][%i]' % (i, j, k)))

        # print(b)

        # inner_constraint = make_constraints(V, L, W, H)

        for i in range(V):
            for j in range(i + 1, V):
                inner.Add(x[i] + data['length'][v[i]] - x[j] <= 0).OnlyEnforceIf(b[i][j][0])
                inner.Add(x[j] + data['length'][v[j]] - x[i] <= 0).OnlyEnforceIf(b[i][j][1])
                inner.Add(y[i] + data['width'][v[i]] - y[j] <= 0).OnlyEnforceIf(b[i][j][2])
                inner.Add(y[j] + data['width'][v[j]] - y[i] <= 0).OnlyEnforceIf(b[i][j][3])
                inner.Add(z[i] + data['height'][v[i]] - z[j] <= 0).OnlyEnforceIf(b[i][j][4])
                inner.Add(z[j] + data['height'][v[j]] - z[i] <= 0).OnlyEnforceIf(b[i][j][5])
                inner.AddBoolOr(b[i][j])

        xyz = {}
        xyz.update(x)
        xyz.update(y)
        xyz.update(z)
        inner_solver = cp_model.CpSolver()
        solution_printer = cp_model.VarArraySolutionPrinter(xyz)
        # Enumerate all solutions.
        inner_solver.parameters.enumerate_all_solutions = True
        # Solve.
        inner_status = inner_solver.Solve(inner, solution_printer)
        if inner_solver.StatusName(inner_status) == 'INFEASIBLE':
            outer_constraint = outer.RowConstraint(0, V - 1, '')
            for i in v:
                outer_constraint.SetCoefficient(u[i], 1)
        else:
            print('Status = %s' % inner_solver.StatusName(inner_status))
            print('Number of solutions found: %i' % solution_printer.solution_count())
            return


def run_linear_solver():
    result = resolve_by_linear_solver("Data\\" + "0.csv")


if __name__ == '__main__':
    # run_cp_model()
    run_linear_solver()

