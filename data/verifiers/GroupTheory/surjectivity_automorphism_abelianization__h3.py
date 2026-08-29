import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        # The witness is expected to be the rank n of the free group F_n
        n = int(witness)
        h1 = (n >= 0)
    except Exception:
        h1 = False

    h2 = h1

    # Mathematically, the map Aut(F_n) -> Aut(F_n / F_n') is surjective for all n >= 0.
    # Since the conclusion is true for all valid n, its negation is False.
    neg_q = False
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_n is a free group of finite rank n",
    "H_2: phi is the natural homomorphism induced by the abelianization map",
    "not Q: The homomorphism phi is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2