import filecmp
import subprocess
import os
import time

import binero_fnc
import BineroIO as io
import Takuzu

class Test

    PATH = None

    __init__(filename) {
        # abs path of this file
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        # trim file name
        last_slash = 0
        for i, char in enumerate(self.PATH):
            if char == "/":
                last_slash = i
        self.PATH = self.PATH[:last_slash]
    }

    test(fname, cond = [0,1,2,3]):

        # solve with minsat
        start_time = time.time()

        dimacs = fname + ".dimacs"
        bin = binero_fnc.Binero_fnc(fname, dimacs)

        bin.solve(cond)

        minsat = fname + "_minsat"
        bashCommand = "minisat" + " "
                    + self.PATH() + "/output/" + dimacs + " "
                    + self.PATH() + "/output/" + minsat

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)

        grid = io.read_minsat(self.PATH() + "/output/" + minsat) 
        io.write_binero(self.PATH() + "/output/" + fname + "_solved",
                        grid)

        minsat_grid = bin.grid
        minsat_time = time.time() - start_time

        # Solve with z3
        tak = Takuzu.Takuzu(self.PATH() + "/output/" + fname + "_solved")
        tak.solve(fname, cond=cond)
        z3_grid = tak.grid

        #compare grids
        assertEqual(tak.sat, True, msg="unsat")

def compare_solutions(fname1, fname2):
        return filecmp.cmp(fname1, fname2, shallow=False)

test("big", cond=[0,3])
