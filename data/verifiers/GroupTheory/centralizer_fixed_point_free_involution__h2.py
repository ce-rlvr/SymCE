import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "¬Q: The centralizer of sigma in S_{2m} is not isomorphic to S_2 \\wr S_m"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        m, sigma = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        if isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool):
            if m > 0:
                h1 = True
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        elif not isinstance(sigma, Permutation):
            neg_q = False
        else:
            supp = sigma.support()
            if supp and max(supp) >= 2*m:
                neg_q = False
            else:
                c_k = {}
                moved = 0
                for cycle in sigma.cyclic_form:
                    k = len(cycle)
                    c_k[k] = c_k.get(k, 0) + 1
                    moved += k
                
                c_1 = 2*m - moved
                if c_1 > 0:
                    c_k[1] = c_k.get(1, 0) + c_1
                
                is_iso = (c_k.get(2, 0) == m) or (m == 1 and c_k.get(1, 0) == 2)
                neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, neg_q]