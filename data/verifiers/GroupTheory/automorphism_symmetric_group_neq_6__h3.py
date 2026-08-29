import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
        if isinstance(witness, bool):
            return [False, False, False]
        n = int(witness)
        if n != witness:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(n >= 3)
    except Exception:
        h1 = False

    try:
        h2 = bool(n != 6)
    except Exception:
        h2 = False

    try:
        # The conclusion states: "Every automorphism of S_n is an inner automorphism, 
        # and Aut(S_n) is isomorphic to S_n."
        # Mathematically, this is a known theorem that holds for all integers n >= 1 
        # EXCEPT for n = 2 (Aut(S_2) is trivial, S_2 is Z_2, so not isomorphic) 
        # and n = 6 (Aut(S_6) has order 1440, S_6 has order 720, so not isomorphic).
        # For n < 1, S_n is undefined in standard terms, so the conclusion fails.
        if n == 2 or n == 6:
            neg_q = True
        elif n >= 1:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 3",
    "H_2: n != 6",
    "¬Q: Aut(S_n) is not isomorphic to S_n, or not every automorphism is inner"
]

N_HYP = 2
NEG_Q_INDEX = 2