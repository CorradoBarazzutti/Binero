import filecmp
import subprocess
import os
import time

import unittest

import binero_fnc
import BineroIO as io
import Takuzu

class Test(unittest.TestCase):

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


    def test(self, fname, cond = [0,1,2,3]):

        # write conditions
        start_time = time.time()

        dimacs = fname + ".dimacs"
        bin = binero_fnc.Binero_fnc(fname, dimacs)

        bin.solve(cond)

        # solve with minisat
        minsat = fname + "_minsat"
        bashCommand = "minisat" + " " \
                    + self.PATH + "/output/" + dimacs + " " \
                    + self.PATH + "/output/" + minsat

        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        minsat_time = time.time() - start_time
        output, error = process.communicate()
        print(output)

        # test result
        if is_sat(output):

            grid = io.read_minsat(self.PATH + "/output/" + minsat,
                              len(bin.input_grid))


            io.write_binero(self.PATH + "/output/" + fname + "_solved",
                        grid)


            # Solve with z3
            tak = Takuzu.Takuzu("../output/" + fname + "_solved")
            tak.solve(cond=cond)

            #compare grids
            print("comperison succesful? " + str(tak.sat))

        else:
            print("unsat")

def is_sat(str):
    a = str[len(str)-14:len(str)-1]
    if str[len(str)-14:len(str)-1] == b'UNSATISFIABLE':
        return False
    return True

def compare_solutions(fname1, fname2):
        return filecmp.cmp(fname1, fname2, shallow=False)

o = Test()
o.test("petit_binero", cond=[0,1,2])
