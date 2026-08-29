import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, n = witness
        else:
            R, I, n = None, None, None
            
        # H_1: I is a two-sided ideal of R
        if I is not None and R is not None:
            h1 = True
            
        # H_2: n is a positive integer
        if isinstance(n, int) and n > 0:
            h2 = True
            
        # ¬Q: M_n(R)/M_n(I) is not isomorphic to M_n(R/I)
        # The canonical map from M_n(R) to M_n(R/I) is a surjective ring homomorphism
        # with kernel exactly M_n(I). By the First Isomorphism Theorem, the quotient
        # M_n(R)/M_n(I) is always isomorphic to M_n(R/I) for any ring R and ideal I.
        # Therefore, the conclusion is always true, and its negation is always False.
        neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "H_2: n is a positive integer",
    "¬Q: M_n(R)/M_n(I) is not isomorphic to M_n(R/I)"
]

N_HYP = 2
NEG_Q_INDEX = 2