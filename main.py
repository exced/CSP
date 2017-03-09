#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import *
from csp import Csp


def readints():
    ''' read integer input as format [x1x2x3x4x5...]
    '''
    return list(map(int, stdin.readline().strip()))


def init_from_stdin():
    ''' read sudoku grid from stdin and return its CSP
    '''
    # variables[position] : domain
    rows = [readints() for _ in range(9)]
    variables = {(i, j): (range(1, 10) if rows[i][j] == 0 else [
        rows[i][j]]) for i in range(9) for j in range(9)}
    # constraints[position] : neq in rows / columns / block
    constraints = {(i, j): [(i2, j2) for i2 in range(9) for j2 in range(9) if (i != i2 or j != j2) and (
        i == i2 or j == j2 or ((i2 // 3 == i // 3) and (j2 // 3 == j // 3)))] for i in range(9) for j in range(9)}        
    return Csp(variables, constraints)

def print_variables(variables):
    ''' stdout variables of csp
    '''
    print(''.join([(str(variables[(i, j)][0]) if len(variables[(i, j)]) == 1 else "0") + ("\n" if j == 8 else "") for i in range(9) for j in range(9)]))    


def main():
    ''' read sudoku from stdin and stdout the solution
    '''
    csp = init_from_stdin()
    print_variables(csp.solve())

if __name__ == '__main__':
    main()
