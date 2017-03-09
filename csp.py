#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Csp:

    def __init__(self, variables, constraints):
        # 81 variables in 9x9 problem with legal values domain
        self.variables = variables
        # 81 variables with 20 constraints -> 1600 constraints (810 different
        # edges)
        self.constraints = constraints

    def solve(self):
        ''' backtrack
        '''
        return self.backtrack(self.assigned(), self.unassigned())

    def assigned(self):
        ''' return all assigned variables
        '''
        return {k: self.variables[k] for k in self.variables if len(self.variables[k]) == 1}

    def unassigned(self):
        ''' return all unassigned variables
        '''
        return {k: self.variables[k] for k in self.variables if len(self.variables[k]) > 1}

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

    def degree_heuristic(self, mrvs):
        ''' take the var that have the most constraints on csp
        '''
        return max(mrvs, key=lambda k: len([i for i in self.constraints[next(iter(k))] if len(self.constraints[i]) > 1]))

    def select_unassigned(self, unassigned):
        ''' degree heuristic on minimum remaining values
        '''
        return self.degree_heuristic(self.mrvs(unassigned))

    def order_least_constraining(self, var, unassigned):
        ''' order by least constraining values
        '''
        # def count(v):
        #    return sum(var.count(v) for k in self.constraints[keyPicked])
        # return sorted(var, key=, reverse=True)

    def remove_inconsistent_values(self, xi, xj):
        ''' remove values that do not satisfy the constraint xi <-> xj 
        '''
        removed = False
        for x in self.variables[xi]:
            if not any((x != y) for y in self.variables[xj]):
                list(self.variables[xi]).remove(x)
                removed = True
        return removed

    def ac3(self):
        ''' Arcs consistency
        '''
        queue = [(xi, xj) for xi in self.variables for xj in self.constraints[xi]]
        while len(queue):
            xi, xj = queue.pop(0)
            if self.remove_inconsistent_values(xi, xj):
                queue.extend([(xk, xi) for xk in self.constraints[xi]])

    def backtrack(self, assigned, unassigned):
        ''' backtrack search with AC3, MRV + DH, LCV heuristics
        '''
        if len(unassigned) == 0:
            return assigned
        var = self.select_unassigned(unassigned)  # MRV + DH
        varKey = list(var.keys())[0]
        varValues = list(var.values())[0]
        #order_values = self.order_least_constraining(var, unassigned)  # LCV
        order_values = varValues
        del unassigned[varKey]
        for value in order_values:
            unassigned[varKey] = [value]
            self.ac3() # reduce domains
            result = self.backtrack(assigned, unassigned)
            if result:
                return result
        return False
