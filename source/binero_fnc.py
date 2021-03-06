# -*- coding: utf-8 -*-
"""
Created on Thu May 24 16:18:15 2018

@author: Stiopa
"""

#Xij = n*i+j+1 
#Yi i' j' = (i+1)*n**2 + n*i' + j' + 1 si i est une ligne
#Yj i' j' = (n+j+1)*n**2 + n*i' + j' + 1 si i est une colone 
import os

import itertools as it
import numpy as np

import BineroIO

class Binero_fnc:

    input_grid = None
    filename = None
    fout = None
    # abs path of project folder
    PATH = None

    def __init__(self, filename, out=""):
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
        if out == "":
            self.fout = self.filename + ".dimacs"
        else:
            self.fout = out

    def boundary_conditions(self):
        result = []
        n = len(self.input_grid)
        for i in range(n):
            for j in range(n):
                var = i * n + j + 1
                if self.input_grid[i][j] == True:
                    result.append([var])
                elif self.input_grid[i][j] == False:
                    result.append([-var])
        return result

    def solve(self, cond=[0,1,2,3]):
        self.boundary_conditions()
        n = len(self.input_grid)
        conditions_dict = { 0: self.boundary_conditions(),
                            1: condition1(n),
                            2: condition2(n),
                            3: condition3(n)}
        binero_c = []
        for i in cond:
            binero_c += conditions_dict[i]
        BineroIO.write_dimacs(
            self.PATH + "/output/" + self.fout,
            binero_c)

def condition1expensive(n):
    result = []
    # first we create a matrix which holds all the possible lines (that have as many 0 as 1)
    # we replace the 0 by -1
    # a recursive function builds the lines
    possible_lines = []
    def possible(i, j, line):
        #i is the length of the line, j the number of 1.
        if i == n:
            possible_lines.append(line)
        # the 2 next cases are if we already have the max amount of 0 or 1
        elif j == n/2:
            possible(i+1, j, line+[-1])
        elif i-j == n/2:
            possible(i+1, j+1, line+[1])
        else :
            possible(i+1, j, line+[-1])
            possible(i+1, j+1, line+[1])
    #we launch the function
    possible(0,0,[])
    
    #now we use it to create the fnc formula for the lines
    for nline in range(n):
        #nline is the number of the line
        for combi in it.product(range(n), repeat = len(possible_lines)):
            clause = []
            for i in range(len(combi)):
                clause = clause+[(n*nline+combi[i]+1)*possible_lines[i][combi[i]]]
            result.append(clause)

    #now we use it to create the fnc formula for the columns
    for ncol in range(n):
        #ncol is the number of the line
        for combi in it.product(range(n), repeat = len(possible_lines)):
            clause = []
            for i in range(len(combi)):
                clause = clause+[(n*combi[i]+ncol+1)*possible_lines[i][combi[i]]]
            result.append(clause)
    
    return(result)


def condition1(n):
    result = []

    # the function order creates clauses so that y1 y2 is x1 x2 but ordered
    def ordre(x1, x2, y1, y2):
        result = [[-y1, x1, x2],
                  [-y2, x1, x2],
                  [y1, -x1, -x2],
                  [y1, -x1, -x2],
                  [-y1, -x1, x2],
                  [-y1, x1, -x2],
                  [y2, -x1, x2],
                  [y2, x1, -x2],
                  [-y1, y2]]
        return (result)

    # ------------fin fonction ordre-----------------
    # pour les lignes---------------------------------------------------------
    # pour comprendre de quoi il s'agit, il faut regarder la formule
    # désolé, mais c'est vraiment trop long à expliquer dans les commentaires
    for i in range(n):
        for j in range(0, n, 2):
            result = result + ordre(n * i + j + 1, n * i + j + 2, (i + 1) * n * n + 0 + j + 1,
                                    (i + 1) * n * n + 0 + j + 2)

        for iprime in range(2, n, 2):
            for jprime in range(0, n, 2):
                result = result + ordre((i + 1) * n * n + (iprime - 1) * n + jprime + 1,
                                        (i + 1) * n * n + (iprime - 1) * n + jprime + 2,
                                        (i + 1) * n * n + (iprime) * n + jprime + 1,
                                        (i + 1) * n * n + (iprime) * n + jprime + 2)

        for iprime in range(1, n, 2):
            # the next lines ensure the leftover vars stay the same
            result.append([(i + 1) * n * n + iprime * n + 0 + 1, -((i + 1) * n * n + (iprime - 1) * n + 0 + 1)])
            result.append([-((i + 1) * n * n + iprime * n + 0 + 1), (i + 1) * n * n + (iprime - 1) * n + 0 + 1])
            result.append(
                [(i + 1) * n * n + iprime * n + (n - 1) + 1, -((i + 1) * n * n + (iprime - 1) * n + (n - 1) + 1)])
            result.append(
                [-((i + 1) * n * n + iprime * n + (n - 1) + 1), (i + 1) * n * n + (iprime - 1) * n + (n - 1) + 1])
            for jprime in range(1, n - 1, 2):
                result = result + ordre((i + 1) * n * n + (iprime - 1) * n + jprime + 1,
                                        (i + 1) * n * n + (iprime - 1) * n + jprime + 2,
                                        (i + 1) * n * n + (iprime) * n + jprime + 1,
                                        (i + 1) * n * n + (iprime) * n + jprime + 2)

        for j in range(n // 2):
            result.append([-((i + 1) * n * n + (n - 1) * n + j + 1)])
        for j in range(n // 2, n):
            result.append([((i + 1) * n * n + (n - 1) * n + j + 1)])

    # pour les colones---------------------------------------------------------
    for j in range(n):
        for i in range(0, n, 2):
            result = result + ordre(n * i + j + 1, n * (i + 1) + j + 1, (n + j + 1) * n * n + i + 1,
                                    (n + j + 1) * n * n + i + 2)

        for iprime in range(2, n, 2):
            for jprime in range(0, n, 2):
                result = result + ordre((n + j + 1) * n * n + (iprime - 1) * n + jprime + 1,
                                        (n + j + 1) * n * n + (iprime - 1) * n + jprime + 2,
                                        (n + j + 1) * n * n + (iprime) * n + jprime + 1,
                                        (n + j + 1) * n * n + (iprime) * n + jprime + 2)

        for iprime in range(1, n, 2):
            # the next lines ensure the leftover vars stay the same
            result.append([(n + j + 1) * n * n + iprime * n + 0 + 1, -((n + j + 1) * n * n + (iprime - 1) * n + 0 + 1)])
            result.append([-((n + j + 1) * n * n + iprime * n + 0 + 1), (n + j + 1) * n * n + (iprime - 1) * n + 0 + 1])
            result.append([(n + j + 1) * n * n + iprime * n + (n - 1) + 1,
                           -((n + j + 1) * n * n + (iprime - 1) * n + (n - 1) + 1)])
            result.append([-((n + j + 1) * n * n + iprime * n + (n - 1) + 1),
                           (n + j + 1) * n * n + (iprime - 1) * n + (n - 1) + 1])
            for jprime in range(1, n - 1, 2):
                result = result + ordre((n + j + 1) * n * n + (iprime - 1) * n + jprime + 1,
                                        (n + j + 1) * n * n + (iprime - 1) * n + jprime + 2,
                                        (n + j + 1) * n * n + (iprime) * n + jprime + 1,
                                        (n + j + 1) * n * n + (iprime) * n + jprime + 2)

        for jprime in range(n // 2):
            result.append([-((n + j + 1) * n * n + (n - 1) * n + jprime + 1)])
        for jprime in range(n // 2, n):
            result.append([((n + j + 1) * n * n + (n - 1) * n + jprime + 1)])

    return (result)


"""
"""
def condition2(n):
    result = []
    #lignes
    for i in range(n):
        for j in range(n-2):
           result.append([n*i+j+1, n*i+j+2,n*i+j+3])
           result.append([-(n*i+j+1), -(n*i+j+2), -(n*i+j+3)])
    
    #colones
    
    for j in range(n):
        for i in range(n-2):
           result.append([n*i+j+1, n*(i+1)+j+1,n*(i+1)+j+1])
           result.append([-(n*i+j+1), -(n*(i+1)+j+1), -(n*(i+2)+j+1)])
          
    return(result)

def condition3_naive(n):
    result = []
    #pas 2 lignes pareilles 
    #i et j représentent les numéros de deux lignes
    for i in range(n):
        for j in range(n):
            if i<j:
                for combi in it.product([-1,1], repeat = n):
                    clause = []
                    #k represente le numéro de la case qu'on considère, au sein de la ligne
                    for k in range(n):
                        clause = clause + [combi[k]*(i*n+k+1), combi[k]*(j*n+k+1)]
                    result.append(clause)

    #pas 2 colones pareilles 
    #i et j représentent les numéros de deux colones
    for i in range(n):
        for j in range(n):
            if i<j:
                for combi in it.product([-1,1], repeat = n):
                    clause = []
                    #k represente le numéro de la case qu'on considère, au sein de la colone
                    for k in range(n):
                        clause = clause + [combi[k]*(k*n+i+1), combi[k]*(k*n+j+1)]
                    result.append(clause)
                    
    return(result)

"""row et col eg"""
def condition3(n):
    result = []
    # 
    def x(i, j):
        return n*i + j + 1
    # 
    def y(i, j, k):
        return 2 * n * n * n + (i) * n**2 + (j) * n + k + 1

    #pas 2 lignes pareilles 
    #i et j représentent les numéros de deux lignes
    for i in range(n):
        for j in range(n):
            if i<j:
                # condition
                result.append([y(i, j, k) for k in range(n)])
                # substitution
                c1, c2, c3, c4 = [], [], [], []
                for k in range(n):
                    c1.append([y(i,j,k), -x(i,k), x(j,k)])
                    c2.append([y(i,j,k), x(i,k), -x(j,k)])
                    c3.append([-y(i,j,k), x(i,k), x(j,k)])
                    c3.append([-y(i,j,k), -x(i,k), -x(j,k)])
                result += c1 + c2 + c3 + c4

    #pas 2 colones pareilles 
    #i et j représentent les numéros de deux colones
    for i in range(n):
        for j in range(n):
            if i<j:
                # condition
                result.append([y(i, j, k) for k in range(n)])
                # substitution
                c1, c2, c3, c4 = [], [], [], []
                for k in range(n):
                    c1.append([y(i,j,k), -x(k,i), x(k,j)])
                    c2.append([y(i,j,k), x(k,i), -x(k,j)])
                    c3.append([-y(i,j,k), x(k,i), x(k,j)])
                    c3.append([-y(i,j,k), -x(k,i), -x(k,j)])
                result += c1 + c2 + c3 + c4
                    
    return(result)