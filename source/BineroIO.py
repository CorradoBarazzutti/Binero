import numpy as np


"""
this func reads the binero file format as defined in sec 3.2
"""
def read_binero(filename):

    grid = None
    inputfile = open(filename)

    # go trough all the lines in the file
    while True:
        line = inputfile.readline()
        if not line:
            break
        line = line.split()
        # skip blank lines
        if len(line) == 0:
            pass
        # skip comments
        elif line[0] == "c":
            pass
        # read the game
        elif line[0] == "binero":
            num_cols = int(float(line[1]))
            num_rows = int(float(line[2]))
            grid = []
            for i in range(num_rows):
                row = inputfile.readline()
                grid.append([None if elem == "." else bool(float(elem)) for elem in row.split()])

    inputfile.close()

    return grid

def write_binero(filename, grid):
    outputfile = open(filename, "w")
    for row in grid:
        outputfile.writelines(str(row) + "\n")
    outputfile.close()

def read_dimacs(filename):
    pass

def write_dimacs(filename, conditions):
    out = open(filename, "w")
    # comment
    out.writelines("c\n" + "c " + filename + "\n" + "c\n")
    # entete
    out.writelines("p cnf " 
        + str(max([max(row) for row in conditions])) + " "
        + str(len(conditions)) + "\n")
    # clauses
    for cond in conditions:
        cond += [0]
        print(cond)
        for var in cond:
            out.writelines(str(var) + " ")
        out.writelines("\n")
    out.close()

def read_minsat(filename, n):
    grid = None
    inputfile = open(filename)

    line = inputfile.readline()
    line = line.split()
    if line[0] == "SAT":
        line = inputfile.readline()
        x = line.split()[:n*n]
        grid = []
        def sgn(number):
            return 1 if number >= 0 else 0
        for i in range(n):
            grid.append([sign(x[i][j]) for j in range(n)])
    return grid

    # go trough all the lines in the file
    while True:
        line = inputfile.readline()
        if not line:
            break
        line = line.split()
        # skip blank lines
        if len(line) == 0:
            pass
        # skip comments
        elif line[0] == "c":
            pass
        # read the game
        elif line[0] == "binero":
            num_cols = int(float(line[1]))
            num_rows = int(float(line[2]))
            grid = []
            for i in range(num_rows):
                row = inputfile.readline()
                grid.append([None if elem == "." else bool(float(elem)) for elem in row.split()])

    inputfile.close()

    return grid