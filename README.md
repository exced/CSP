# Constraint Satisfaction Problem - Sudoku

1. Variables: 81 in a 9x9 sudoku.
2. Domains: [1..9]
3. Constraints: Only one occurence of a number in each row, each colum and unit.

Note that we use binary constraints : there are 810 all-different binary constraints between variables.

To run :
```bash
python3 sudoku.py <grids/grid1
```

# Results

![number of backtrack calls](https://github.com/exced/CSP/tree/master/extras/results.png)

