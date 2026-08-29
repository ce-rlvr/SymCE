import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup
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

def conditions(witness):
    try:
        # The witness can be either the integer n or the group S_n itself
        if hasattr(witness, 'degree') and isinstance(witness, SymmetricGroup):
            n = witness.degree
        else:
            n = int(witness)
            
        # H_1: Assume n != 6
        h1 = (n != 6)
        
        # H_2: Let S_n be the symmetric group on n elements (n must be a positive integer)
        h2 = (n >= 1)
        
        # Conclusion: Every automorphism of S_n is an inner automorphism, and Aut(S_n) is isomorphic to S_n.
        # Mathematically, this conclusion is TRUE for all n >= 1 EXCEPT n = 2 and n = 6.
        # - For n = 2: Aut(S_2) is trivial (order 1), but S_2 has order 2. They are not isomorphic.
        # - For n = 6: S_6 has outer automorphisms, so not every automorphism is inner.
        concl = (n != 2 and n != 6)
        
        # neg_Q is True when the conclusion FAILS
        neg_q = not concl
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: n != 6",
    "H_2: n is a positive integer",
    "¬Q: Aut(S_n) is not isomorphic to S_n or has outer automorphisms"
]

N_HYP = 2
NEG_Q_INDEX = 2