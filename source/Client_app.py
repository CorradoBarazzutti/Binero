import filecmp
import os
import time
import subprocess

import binero_fnc
import BineroIO as io
import Takuzu

def compare_solutions(fname1, fname2):
    return filecmp.cmp(fname1, fname2, shallow=False)
 
class Client:

    PATH = None

    def __init__(self) :
        # abs path of this file
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        # trim file name
        last_slash = 0
        for i, char in enumerate(self.PATH):
            if char == "/":
                last_slash = i
        self.PATH = self.PATH[:last_slash]

    def run_minsat(self, fname):
        start_time = time.time()

        dimacs = fname + ".dimacs"
        bin = binero_fnc.Binero_fnc(fname, dimacs)

        bin.solve()

        minsat = fname + "_minsat"
        bashCommand = "minisat" + " " \
                    + self.PATH + "/output/" + dimacs + " " \
                    + self.PATH + "/output/" + minsat

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output)

        grid = io.read_minsat(self.PATH + "/output/" + minsat,
                              len(bin.input_grid))
        io.write_binero(self.PATH + "/output/" + fname + "_solved",
                        grid)
        return time.time() - start_time

    def run_z3(fname):
        tak = Takuzu.Takuzu(fname)
        tak.solve(fname)
        z3_grid = tak.grid

Client().run_minsat("petit binero")



