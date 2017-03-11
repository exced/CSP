#!/usr/bin/env python3
# -*- coding: utf-8 -*-

nbBacktrack = 0


class Csp:

    def __init__(self, variables, constraints):
        # {key: [domain]}
        self.variables = variables
        # {key: [key]}
        self.constraints = constraints

    def invalid(self, assignments):
        ''' check if the input sudoku has no error
        '''
        for var in assignments:
            for cons in self.constraints[var]:
                if len(assignments[cons]) == 1 and len(assignments[var]) == 1 and assignments[cons][0] == assignments[var][0]:
                    return True
        return False

    def solve(self):
        ''' backtrack
        '''
        assignments = self.variables
        if not self.invalid(assignments):
            global nbBacktrack
            nbBacktrack = 0
            print(self.backtrack.__doc__)
            self.ac3(assignments) # reduce domain (since Csp has no init error, it would not fail)
            b = self.backtrack(assignments, self.unassigned())
            print("Nb backtrack: ", nbBacktrack)
            return b
        else:
            print("invalid sudoku grid")
        return None

    def print_variables(self, variables):
        ''' stdout variables of csp
        '''
        print(''.join([(str(variables[(i, j)][0]) if len(variables[(
            i, j)]) == 1 else "0") + ("\n" if j == 8 else "") for i in range(9) for j in range(9)]))

    def assigned(self):
        ''' return all assigned variables
        '''
        return {k: self.variables[k] for k in self.variables if len(self.variables[k]) == 1}

    def unassigned(self):
        ''' return all unassigned variables
        '''
        return {k: self.variables[k] for k in self.variables if len(self.variables[k]) > 1}

    def is_complete(self, assignments):
        ''' check if all assignments have singleton domain
        '''
        return all([len(assignments[k]) == 1 for k in assignments])

    def mrvs(self, unassigned):
        ''' return all the values that have the shortest remaining domain
        '''
        mrvs = []
        import math
        mrv = math.inf
        for k in unassigned:
            l = len(unassigned[k])
            if l < mrv:
                mrvs = [{k: unassigned[k]}]
                mrv = l
            elif l == mrv:
                mrvs.append({k: unassigned[k]})
        return mrvs

    def degree_heuristic(self, mrvs, unassigned):
        ''' take the var that have the most constraints on csp
        '''
        return max(mrvs, key=lambda k: len([i for i in self.constraints[next(iter(k))] if i in unassigned if len(self.constraints[i]) > 1]))

    def select_unassigned(self, unassigned):
        ''' degree heuristic on minimum remaining values
        '''
        return self.degree_heuristic(self.mrvs(unassigned), unassigned)

    def count_val_in_neighbors(self, varKey, val, assignments, unassigned):
        ''' count val in neighbors (restricted to unassigned) of var
        '''
        return sum([1 if val in unassigned[i] else 0 for i in self.constraints[varKey] if i in unassigned])

    def order_least_constraining(self, varKey, varValues, assignments, unassigned):
        ''' order by least constraining values
        '''
        return sorted(varValues, key=lambda k: self.count_val_in_neighbors(varKey, k, assignments, unassigned), reverse=True)

    def remove_inconsistent_values(self, xi, xj, assignments):
        ''' remove values that do not satisfy the constraint xi <-> xj 
        '''
        removed = False
        for x in assignments[xi]:
            if len(assignments[xj]) == 1 and assignments[xj][0] == x:
                l = list(assignments[xi])
                l.remove(x)
                assignments[xi] = l
                removed = True
        return removed

    def ac3(self, assignments):
        ''' Arcs consistency
        '''
        queue = [(xi, xj) for xi in assignments for xj in self.constraints[xi]]
        while len(queue):
            xi, xj = queue.pop(0)
            if self.remove_inconsistent_values(xi, xj, assignments):
                if not assignments[xi]:  # invalid var
                    return False
                queue.extend([(xk, xi) for xk in self.constraints[xi]])
        return True

    def backtrack(self, assignments, unassigned):
        ''' backtrack search with AC3, MRV + DH, LCV heuristics
        '''
        global nbBacktrack
        nbBacktrack += 1
        if self.is_complete(assignments):
            return assignments
        var = self.select_unassigned(unassigned)  # MRV + DH
        varKey = list(var.keys())[0]
        varValues = list(var.values())[0]
        order_values = self.order_least_constraining(varKey, varValues, assignments, unassigned)  # LCV
        unassigned_copy = unassigned.copy()
        del unassigned_copy[varKey]
        for value in order_values:
            assignments_copy = assignments.copy()
            assignments_copy[varKey] = [value]
            if self.ac3(assignments_copy):  # AC-3 reduce domains + is_valid
                backtrack = self.backtrack(assignments_copy, unassigned_copy)
                if backtrack is not False:
                    return backtrack
        return False
