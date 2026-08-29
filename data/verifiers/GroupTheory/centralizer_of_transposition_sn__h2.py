import math
from sympy.combinatorics import Permutation, SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        n, tau = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if isinstance(tau, Permutation):
            supp = tau.support()
            if supp and max(supp) < n:
                c = tau.cyclic_form
                if len(c) == 1 and len(c[0]) == 2:
                    h2 = True
    except Exception:
        h2 = False
        
    try:
        if n == 2:
            # For n=2, S_{n-2} is S_0, which is undefined in standard group theory 
            # and raises an error in SymPy. Thus the conclusion fails.
            neg_q = True
        elif isinstance(n, int) and n >= 3:
            if n <= 6:
                Sn = SymmetricGroup(n)
                expected_order = 2 * math.factorial(n - 2)
                cent_order = sum(1 for p in Sn.generate() if p * tau == tau * p)
                neg_q = (cent_order != expected_order)
            else:
                neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: tau in S_n is a transposition",
    "not Q: The centralizer of tau in S_n is NOT isomorphic to C_2 x S_{n-2}"
]

N_HYP = 2
NEG_Q_INDEX = 2