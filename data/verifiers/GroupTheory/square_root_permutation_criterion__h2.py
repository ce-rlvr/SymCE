import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
    "H_1: n >= 1 is an integer",
    "¬Q: Equivalence between having a square root in S_n and the even cycle condition fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            sigma = witness.get('sigma')
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, sigma = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        n_val = int(n)
        h1 = bool((n_val >= 1) and (n_val == n))
    except Exception:
        h1 = False
        
    try:
        if not isinstance(sigma, Permutation):
            neg_q = False
        else:
            cycles = sigma.cyclic_form
            counts = {}
            for c in cycles:
                length = len(c)
                counts[length] = counts.get(length, 0) + 1
                
            rhs = True
            for k, count in counts.items():
                if k % 2 == 0 and count % 2 != 0:
                    rhs = False
                    break
            
            supp = sigma.support()
            in_Sn = all(x < n_val for x in supp) if supp else True
            
            # sigma has a square root in S_n iff it is in S_n and satisfies the even cycle condition
            lhs = in_Sn and rhs
            
            # The conclusion is the equivalence: lhs == rhs
            # The negated conclusion is that this equivalence fails
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]