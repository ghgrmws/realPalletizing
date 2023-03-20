import os
from ortools.linear_solver import pywraplp
from methods import get_data


def resolve(file_path):
    N, L, W, H, boxes = get_data(file_path)
    outer = pywraplp.Solver.CreateSolver('SAT')
    b = outer.BoolVar('b')
    return -1


def main():
    dirs = os.listdir("Data")
    for file in dirs:
        if file.endswith('.csv'):
            result = resolve("Data\\" + file)
            print(result)
            break


if __name__ == '__main__':
    main()
