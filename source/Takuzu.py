import os
from builtins import print

import z3
import itertools

import BineroIO

"""
this class models and solve the binero problem
"""


class Takuzu:
    input_grid = None
    solver = z3.Solver()
    sat = False

    filename = None
    # abs path of project folder
    PATH = None

    def __init__(self, filename):
        #
        self.filename = filename
        # abs path of this file
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        # trim file name
        last_slash = 0
        for i, char in enumerate(self.PATH):
            if char == "/":
                last_slash = i
        self.PATH = self.PATH[:last_slash]
        # dataIn file abs path
        filename = self.PATH + "/dataIn/" + filename
        self.input_grid = BineroIO.read_binero(filename)

    def solve(self, cond=[0,1,2,3]):

        # get puzzle dimensions
        num_rows = len(self.input_grid)
        num_cols = len(self.input_grid[0])

        # declaring matrix of Bool variables
        X = [[z3.Bool("x_%s_%s" % (i, j)) for i in range(num_rows)]
             for j in range(num_cols)]

        # boundary conditions
        instance_c = [z3.If(self.input_grid[i][j] == None,
                            True,
                            X[i][j] == self.input_grid[i][j])
                      for i in range(num_rows) for j in range(num_cols)]

        # sur chaque colonne ou ligne de la grille, il ne peut y avoir plus de deux 0 ou deux 1 consécutifs
        row_combo = [z3.Implies(X[i][j] == X[i][j + 1], z3.Not(X[i][j + 2] == X[i][j]))
                     for j in range(num_cols - 2)
                     for i in range(num_rows)]
        col_combo = [z3.Implies(X[i][j] == X[i + 1][j], z3.Not(X[i + 2][j] == X[i][j]))
                     for i in range(num_cols - 2)
                     for j in range(num_rows)]

        # il y a le même nombre de 0 et de 1 sur chaque ligne et chaque colonne
        row_par = [z3.Sum([z3.If(X[i][j], 1, 0) for j in range(num_cols)]) == num_cols / 2
                   for i in range(num_rows)]
        col_par = [z3.Sum([z3.If(X[j][i], 1, 0) for j in range(num_rows)]) == num_rows / 2
                   for i in range(num_cols)]

        # il n’y a pas deux lignes (ou deux colonnes) remplies identiquement
        row_eg = [z3.Or([z3.Not(X[i][k] == X[j][k]) for k in range(num_cols)])
                        for j in range(num_rows)
                    for i in range(num_rows) if i != j]
        col_eg = [z3.Or([z3.Not(X[k][i] == X[k][j]) for k in range(num_rows)])
                        for j in range(num_cols)
                    for i in range(num_cols) if i != j]

        # add condition to the solver
        conditions_dict = { 0: instance_c,
                            1: row_par + col_par,
                            2: row_combo + col_combo,
                            3: row_eg + col_eg}
        # select and conditions
        binero_c = []
        for i in cond:
            binero_c += conditions_dict[i]
        self.solver.add(binero_c)
        # solve
        if self.solver.check() == z3.sat:
            self.sat = True
            m = self.solver.model()
            r = [[m.evaluate(X[i][j]) for j in range(num_cols)]
                 for i in range(num_rows)]
            output_grid = [[1 if r[i][j] == True else 0
                            for j in range(num_cols)]
                           for i in range(num_rows)]
            BineroIO.write_binero(self.PATH + "/output/" + self.filename + "_solutionSMT", output_grid)
        else:
            print("failed to solve")
