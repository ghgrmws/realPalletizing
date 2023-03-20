from ortools.linear_solver import pywraplp
from ortools.algorithms import pywrapknapsack_solver


def linear_programming_example():
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    # [START solver]
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return
    # [END solver]

    # Create the two variables and let them take on any non-negative value.
    # [START variables]
    x = solver.NumVar(0, solver.infinity(), 'x')
    y = solver.NumVar(0, solver.infinity(), 'y')

    print('Number of variables =', solver.NumVariables())
    # [END variables]

    # [START constraints]
    # Constraint 0: x + 2y <= 14.
    solver.Add(x + 2 * y <= 14.0)

    # Constraint 1: 3x - y >= 0.
    solver.Add(3 * x - y >= 0.0)

    # Constraint 2: x - y <= 2.
    solver.Add(x - y <= 2.0)

    print('Number of constraints =', solver.NumConstraints())
    # [END constraints]

    # [START objective]
    # Objective function: 3x + 4y.
    solver.Maximize(3 * x + 4 * y)
    # [END objective]

    # Solve the system.
    # [START solve]
    status = solver.Solve()
    # [END solve]

    # [START print_solution]
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', x.solution_value())
        print('y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')
    # [END print_solution]

    # [START advanced]
    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    # [END advanced]


def knapsack_example():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    values = [
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
        78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
        87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
        312
    ]
    weights = [[
        7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
        42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
        3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
    ]]
    capacities = [850]

    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total weight:', total_weight)
    print('Packed items:', packed_items)
    print('Packed_weights:', packed_weights)


def sat_example():
    # [START solver]
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SAT')
    if not solver:
        return
    # [END solver]
    # [START variables]
    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    x = solver.IntVar(0.0, infinity, 'x')
    y = solver.IntVar(0.0, infinity, 'y')
    print('Number of variables =', solver.NumVariables())
    # [END variables]
    # [START constraints]
    # x + 7 * y <= 17.5.
    solver.Add(x + 7 * y <= 17.5)
    # x <= 3.5.
    solver.Add(x <= 3.5)
    print('Number of constraints =', solver.NumConstraints())
    # [END constraints]
    # [START objective]
    # Maximize x + 10 * y.
    solver.Maximize(x + 10 * y)
    # [END objective]
    # [START solve]
    print(f'Solving with {solver.SolverVersion()}')
    status = solver.Solve()
    # [END solve]
    # [START print_solution]
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', x.solution_value())
        print('y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')
    # [END print_solution]
    # [START advanced]
    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    # [END advanced]


if __name__ == '__main__':
    linear_programming_example()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    knapsack_example()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    sat_example()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
