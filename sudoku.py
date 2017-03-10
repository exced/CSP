#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from csp import Csp


def readints(file):
    ''' read integer input as format [x1x2x3x4x5...]
    '''
    return list(map(int, file.readline().strip()))

def init_from_file(file):
    ''' read sudoku grid from stdin and return its CSP
    '''
    f = open(file, 'r')
    grid = [readints(f) for _ in range(9)]
    # variables[position] : domain
    variables = {(i, j): (range(1, 10) if grid[i][j] == 0 else [
        grid[i][j]]) for i in range(9) for j in range(9)}
    # constraints[position] : neq in rows / columns / block
    constraints = {(i, j): [(i2, j2) for i2 in range(9) for j2 in range(9) if (i != i2 or j != j2) and (
        i == i2 or j == j2 or ((i2 // 3 == i // 3) and (j2 // 3 == j // 3)))] for i in range(9) for j in range(9)}
    return Csp(variables, constraints)


def main():
    ''' read sudoku from stdin and stdout the solution
        - 81 variables in 9x9 problem with legal values domain
        - 81 variables with 20 constraints -> 1600 constraints (810 different edges)
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input file : 9x9 grid")
    parser.add_argument("-s", help="0 : simple backtrack, 1 : backtrack with AC3, MRV, LCV and DH strategies")
    args = parser.parse_args()
    csp = init_from_file(args.i)
    csp.print_variables(csp.solve(args.s))

if __name__ == '__main__':
    main()
