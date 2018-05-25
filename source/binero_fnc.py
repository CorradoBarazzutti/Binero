# -*- coding: utf-8 -*-
"""
Created on Thu May 24 16:18:15 2018

@author: Stiopa
"""

#Xij = Xn*i+j+1 
import itertools as it
import numpy as np


def condition1(n):
    result = []
    #first we create a matrix which holds all the possible lines (that have as many 0 as 1)
    #we replace the 0 by -1
    #a recursive function builds the lines
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
        
        
        
def condition2(n):
    result = []
    for i in range(n):
        for j in range(n-2):
           result.append([n*i+j+1, n*i+j+2,n*i+j+3])
           result.append([-(n*i+j+1), -(n*i+j+2), -(n*i+j+3)])

    return(result)
           
           
def condition3(n):
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

