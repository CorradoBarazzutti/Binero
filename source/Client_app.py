import filecmp
import binero_fnc
import Takuzu

def compare_solutions(fname1, fname2):
    return filecmp.cmp(fname1, fname2, shallow=False)

tak = Takuzu.Takuzu("petit_binero")
tak.solve()
