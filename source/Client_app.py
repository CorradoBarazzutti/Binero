import filecmp
import binero_fnc

def compare_solutions(fname1, fname2):
    return filecmp.cmp(fname1, fname2, shallow=False)

tak = binero_fnc.Binero_fnc("petit_binero")
tak.solve()
