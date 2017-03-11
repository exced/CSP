# Constraint Satisfaction Problem - Sudoku

1. Variables: 81 in a 9x9 sudoku.
2. Domains: [1..9]
3. Constraints: Only one occurence of a number in each row, each colum and unit.

Note that we use binary constraints : there are 810 all-different binary constraints between variables.

There are different backtrack strategies available :
0. Simple : test all variables and all domains without ordering them.
1. Arcs consistency, Minimum Remaining Values + Degree Heuristic strategy to choose the next variables and Least Constraining Values to order domain.

To run :
```bash
python3 sudoku.py -i grids/grid1 -s 1
```

